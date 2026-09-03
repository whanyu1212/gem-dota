"""Internal replay-parsing orchestrator for Dota 2 Source 2 .dem files.

Ties together the stream reader, sendtable schema, string tables, entity
manager, game events, and combat log into a single ``ReplayParser`` class.
Callers register callbacks for the events they care about and then call
``parse()`` to drive the loop.

This is the low-level engine. Most users should call :func:`gem.api.parse`
(re-exported as ``gem.parse``), which wires ``ReplayParser`` up with all
extractors and returns a structured :class:`~gem.results.models.ParsedMatch`.
Use ``ReplayParser`` directly only when you need raw callback-level access.

Outer message layout
--------------------
Each outer message has one of these EDemoCommands type IDs:

  DEM_SendTables   (4) → CDemoSendTables  (build serializer schema)
  DEM_ClassInfo    (5) → CDemoClassInfo   (map class IDs → names)
  DEM_Packet       (7) → CDemoPacket      (contains inner net messages)
  DEM_SignonPacket (8) → CDemoPacket      (same format, signon phase)
  DEM_FullPacket  (13) → CDemoFullPacket  (.string_table + .packet)

Inner message layout inside CDemoPacket.data
--------------------------------------------
Each inner message is encoded as:
  ubit_var   → message type ID  (SVC_Messages / NET_Messages / EBaseGameEvents)
  varuint32  → byte length
  bytes      → protobuf payload

Relevant inner IDs:
  net_Tick                        =   4
  svc_ServerInfo                  =  40
  svc_CreateStringTable           =  44
  svc_UpdateStringTable           =  45
  svc_PacketEntities              =  55
  svc_UserMessage                 =  72
  GE_Source1LegacyGameEventList   = 205
  GE_Source1LegacyGameEvent       = 207
  DOTA_UM_CombatLogDataHLTV       = 554  (direct)
  DOTA_UM_MatchMetadata           = 557  (direct)
  DOTA_UM_MatchDetails            = 558  (direct postgame summary)

Reference: manta/parser.go, manta/demo_packet.go, manta/game_event.go
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

# Proto side-effect import order is critical
from google.protobuf import descriptor_pb2  # noqa: F401

from gem.binary.reader import BitReader
from gem.binary.stream import DemoStream
from gem.catalog import item_key_by_id
from gem.combat.log import CombatLogHandler, CombatLogProcessor
from gem.proto import (
    dota_commonmessages_pb2,  # noqa: F401
    dota_shared_enums_pb2,  # noqa: F401
    network_connection_pb2,  # noqa: F401
    networkbasetypes_pb2,  # noqa: F401
)
from gem.proto.demo_pb2 import CDemoClassInfo, CDemoFileInfo, CDemoFullPacket, CDemoPacket
from gem.proto.dota_gcmessages_common_pb2 import CMsgDOTAMatch
from gem.proto.dota_match_metadata_pb2 import CDOTAMatchMetadataFile
from gem.proto.dota_shared_enums_pb2 import CMsgDOTACombatLogEntry
from gem.proto.dota_usermessages_pb2 import (
    CDOTAUserMsg_ChatEvent,
    CDOTAUserMsg_ChatMessage,
    CDOTAUserMsg_CombatLogBulkData,
    CDOTAUserMsg_FoundNeutralItem,
    DOTA_UM_MatchDetails,
    DOTA_UM_MatchMetadata,
)
from gem.proto.gameevents_pb2 import (
    CMsgSource1LegacyGameEvent,
    CMsgSource1LegacyGameEventList,
)
from gem.proto.netmessages_pb2 import (
    CSVCMsg_CreateStringTable,
    CSVCMsg_PacketEntities,
    CSVCMsg_ServerInfo,
    CSVCMsg_UpdateStringTable,
    CSVCMsg_UserMessage,
)
from gem.proto.networkbasetypes_pb2 import CNETMsg_Tick
from gem.results.models import ChatEntry, NeutralItemFoundEvent
from gem.schema.sendtable import parse_send_tables
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import Entity, EntityManager, EntityOp
from gem.state.game_events import GameEventHandler, GameEventManager
from gem.state.string_table import StringTables, handle_create, handle_update

logger = logging.getLogger(__name__)

_GAMERULES_FIELDS = FieldAccessPlan(
    (
        "m_pGameRules.m_flGameStartTime",
        "m_pGameRules.m_fGameTime",
        "m_pGameRules.m_bGamePaused",
        "m_pGameRules.m_nPauseStartTick",
        "m_pGameRules.m_nTotalPausedTicks",
        "m_pGameRules.m_unMatchID64",
        "m_pGameRules.m_iGameMode",
        "m_pGameRules.m_unLeagueID",
        "m_pGameRules.m_nGameWinner",
    )
)

# ---------------------------------------------------------------------------
# Outer EDemoCommands IDs (stripped of DEM_IsCompressed = 0x40)
# ---------------------------------------------------------------------------
_DEM_FILE_INFO = 2
_DEM_SEND_TABLES = 4
_DEM_CLASS_INFO = 5
_DEM_PACKET = 7
_DEM_SIGNON_PACKET = 8
_DEM_FULL_PACKET = 13

# Inner SVC/NET/Game-event message IDs
_NET_TICK = 4
_SVC_SERVER_INFO = 40
_SVC_CREATE_STRING_TABLE = 44
_SVC_UPDATE_STRING_TABLE = 45
_SVC_PACKET_ENTITIES = 55
_SVC_USER_MESSAGE = 72
_GE_GAME_EVENT_LIST = 205
_GE_GAME_EVENT = 207

# DOTA user-message sub-type IDs (inside CSVCMsg_UserMessage.msg_type)
_DOTA_UM_COMBAT_LOG_DATA = 468  # CDOTAUserMsg_CombatLogBulkData (S2)
_DOTA_UM_COMBAT_LOG_BULK_DATA = 470  # CDOTAUserMsg_CombatLogBulkData (alternate)

# Direct inner message types (not wrapped in svc_UserMessage)
_DOTA_UM_COMBAT_LOG_HLTV = 554  # CMsgDOTACombatLogEntry (direct, one entry per message)
_DOTA_UM_CHAT_EVENT = 466  # CDOTAUserMsg_ChatEvent (direct)
_DOTA_UM_MATCH_METADATA = DOTA_UM_MatchMetadata  # CDOTAMatchMetadataFile (direct)
_DOTA_UM_MATCH_DETAILS = DOTA_UM_MatchDetails  # CMsgDOTAMatch postgame summary (direct)
_DOTA_UM_FOUND_NEUTRAL_ITEM = 593  # CDOTAUserMsg_FoundNeutralItem (direct)
_DOTA_UM_CHAT_MESSAGE = 612  # CDOTAUserMsg_ChatMessage (direct)

_CHAT_MSG_RUNE_PICKUP = 22  # DOTA_CHAT_MESSAGE.CHAT_MESSAGE_RUNE_PICKUP

# CombatLogNames string table name
_COMBAT_LOG_NAMES_TABLE = "CombatLogNames"


def _round_positive_seconds(value: float) -> int:
    """Round positive replay seconds the same way Java ``Math.round`` does."""
    return int(value + 0.5)


EntityCallback = Callable[[Entity, EntityOp], None]
TickStartCallback = Callable[[int], None]
ChatCallback = Callable[["ChatEntry"], None]
ChatEventCallback = Callable[["CDOTAUserMsg_ChatEvent", int], None]
NeutralItemFoundCallback = Callable[["NeutralItemFoundEvent"], None]


@dataclass(frozen=True, slots=True)
class _EntityCallbackRegistration:
    """A pending catch-all or internally filtered entity callback."""

    callback: EntityCallback
    class_names: frozenset[str] = frozenset()
    class_prefixes: tuple[str, ...] = ()

    @property
    def filtered(self) -> bool:
        """Return whether this registration has a class filter."""
        return bool(self.class_names or self.class_prefixes)


def _read_inner_messages(data: bytes) -> list[tuple[int, bytes]]:
    """Unpack the inner message sequence from a CDemoPacket.data blob.

    Format: repeated { ubit_var type_id, varuint32 size, bytes payload }.

    Args:
        data: The raw bytes from CDemoPacket.data.

    Returns:
        List of (type_id, payload_bytes) pairs.
    """
    r = BitReader(data)
    messages: list[tuple[int, bytes]] = []
    while r.rem_bits() >= 8:
        type_id = r.read_ubit_var()
        size = r.read_varuint32()
        payload = r.read_bytes(size)
        messages.append((type_id, payload))
    return messages


class ReplayParser:
    """Drives a full Source 2 replay parse, wiring all subsystems together.

    Usage::

        parser = ReplayParser("game.dem")
        parser.on_entity(lambda e, op: print(e, op))
        parser.on_game_event("dota_combatlog", lambda e: print(e))
        parser.on_combat_log_entry(lambda e: print(e))
        parser.parse()

    Attributes:
        tick: Current game tick.
        net_tick: Current net tick (from net_Tick inner messages).
        game_time_s: Rounded game-relative clock refreshed at network tick start.
        game_build: Build number extracted from CSVCMsg_ServerInfo.
        string_tables: All string tables created so far.
        entity_manager: Live entity table.
        game_event_manager: Game event schema and handler registry.
        combat_log: Combat log processor for S1 and S2 entries.
        match_details: Embedded ``CMsgDOTAMatch`` postgame summary, when present.
    """

    def __init__(self, source: str | Path | bytes) -> None:
        self._source = source
        self.tick: int = 0
        self.net_tick: int = 0
        self._net_tick_seen: bool = False
        self.game_build: int = 0
        self.string_tables = StringTables()
        self.entity_manager: EntityManager | None = None
        self.game_event_manager = GameEventManager()
        self.combat_log = CombatLogProcessor()
        self._entity_callbacks: list[_EntityCallbackRegistration] = []
        self._tick_start_callbacks: list[TickStartCallback] = []
        self._chat_callbacks: list[ChatCallback] = []
        self._chat_event_callbacks: list[ChatEventCallback] = []
        self._neutral_item_found_callbacks: list[NeutralItemFoundCallback] = []
        self._stop_at_tick: int | None = None
        self._grp_game_start_seen: bool = False
        self._pending_server_info: CSVCMsg_ServerInfo | None = None
        self.match_id: int = 0
        self.game_mode: int = 0
        self.leagueid: int = 0
        self.match_metadata: CDOTAMatchMetadataFile | None = None
        self.match_details: CMsgDOTAMatch | None = None
        self.radiant_win: bool | None = None
        self.game_start_tick: int | None = None
        self.game_time_s: int | None = None
        # Horn-anchored timestamp of the latest combat-log entry. This is an
        # event clock, not a continuously advancing sampling clock; interval
        # consumers use ``game_time_s`` refreshed at CNETMsg_Tick start instead.
        self.combat_log_time_s: int | None = None
        # OpenDota-style match duration in seconds: the horn-anchored combat-log
        # time at GAME_STATE==6 (ancient destroyed). None until that state is seen.
        self.duration_s: int | None = None
        # Set when the stream loop terminates on an exception rather than running
        # to completion. ``parse_error`` is the exception, ``truncated_at_tick``
        # the last tick reached. Both stay None on a clean parse. This is the
        # programmatic counterpart to the WARNING logged in ``parse()``: an
        # expected truncated-tail and a genuine mid-stream bug are
        # indistinguishable here, so consumers can inspect these to tell whether a
        # ``ParsedMatch`` is complete instead of trusting silent partial output.
        self.parse_error: Exception | None = None
        self.truncated_at_tick: int | None = None
        self._game_start_callbacks: list[Callable[[int], None]] = []
        self._game_end_callbacks: list[Callable[[int], None]] = []
        self._game_ended: bool = False
        # Tick at which a GAME_STATE==6 (postGame) marker was seen this packet,
        # pending callback dispatch. Game-end callbacks are deferred to the end
        # of the inner-packet loop so that same-packet entity deltas (sorted at a
        # higher priority than the wrapped svc_UserMessage combat-log path) are
        # applied before terminal consumers (e.g. IntervalExtractor) flush.
        self._pending_game_end_tick: int | None = None
        self._game_start_time_s: int | None = None
        self._combat_log_game_start_time_s: int | None = None
        self._on_entity_filtered(
            self._on_entity_game_start,
            class_names=("CDOTAGamerulesProxy",),
        )

    # ------------------------------------------------------------------
    # Public callback registration
    # ------------------------------------------------------------------

    def on_entity(self, callback: EntityCallback) -> None:
        """Register a handler called for every entity create/update/delete.

        Args:
            callback: ``(Entity, EntityOp) -> None``.
        """
        self._register_entity_callback(_EntityCallbackRegistration(callback=callback))

    def _on_entity_filtered(
        self,
        callback: EntityCallback,
        *,
        class_names: Iterable[str] = (),
        class_prefixes: Iterable[str] = (),
    ) -> None:
        """Register an internal callback for selected entity classes."""
        names = frozenset(class_names)
        prefixes = tuple(dict.fromkeys(class_prefixes))
        if not names and not prefixes:
            raise ValueError("filtered entity callbacks require a class name or prefix")
        if any(not value for value in names) or any(not value for value in prefixes):
            raise ValueError("entity class names and prefixes must be non-empty")
        self._register_entity_callback(
            _EntityCallbackRegistration(
                callback=callback,
                class_names=names,
                class_prefixes=prefixes,
            )
        )

    def _register_entity_callback(self, registration: _EntityCallbackRegistration) -> None:
        self._entity_callbacks.append(registration)
        if self.entity_manager is None:
            return
        if registration.filtered:
            self.entity_manager._on_entity_filtered(
                registration.callback,
                class_names=registration.class_names,
                class_prefixes=registration.class_prefixes,
            )
        else:
            self.entity_manager.on_entity(registration.callback)

    def on_tick_start(self, callback: TickStartCallback) -> None:
        """Register a handler called before the current tick's entity deltas.

        ``CNETMsg_Tick`` is dispatched ahead of ``svc_PacketEntities``. The
        callback therefore sees the reconstructed entity table at the same
        pre-update boundary as Clarity's ``@OnTickStart``, which OpenDota uses
        for interval snapshots.

        Args:
            callback: ``(net_tick: int) -> None``.
        """
        self._tick_start_callbacks.append(callback)

    def _on_entity_game_start(self, entity: Entity, op: EntityOp) -> None:
        if entity.get_class_name() != "CDOTAGamerulesProxy":
            return
        self._update_game_clock(entity)
        if self._grp_game_start_seen:
            return
        game_start = entity._resolve_fields(_GAMERULES_FIELDS)[0]
        v = entity._get_float32_resolved(game_start)
        if v is None or v == 0.0:
            return
        self._grp_game_start_seen = True
        self.game_start_tick = self.tick
        for cb in self._game_start_callbacks:
            cb(self.tick)

    def _update_game_clock(self, entity: Entity) -> None:
        """Track OpenDota-style game time from ``CDOTAGamerulesProxy``.

        OpenDota timestamps interval records by reading ``m_fGameTime`` when
        available, or falling back to ``(tick - paused_ticks) / 30``. The stored
        output time is then shifted by ``m_flGameStartTime``. Keep this as
        separate metadata so public raw-tick fields remain unchanged.
        """
        fields = entity._resolve_fields(_GAMERULES_FIELDS)
        start = entity._get_float32_resolved(fields[0])
        if start is not None and start != 0.0:
            self._game_start_time_s = _round_positive_seconds(start)

        if self._game_start_time_s is None:
            return

        game_time = entity._get_float32_resolved(fields[1])
        if game_time is not None:
            raw_time_s = _round_positive_seconds(game_time)
        else:
            paused = entity._get_bool_resolved(fields[2]) or False
            pause_start_tick = entity._get_int32_resolved(fields[3])
            total_paused_ticks = entity._get_int32_resolved(fields[4]) or 0
            parser_tick = self.net_tick if self._net_tick_seen else self.tick
            time_tick = pause_start_tick if paused and pause_start_tick is not None else parser_tick
            raw_time_s = _round_positive_seconds((time_tick - total_paused_ticks) / 30.0)

        self.game_time_s = raw_time_s - self._game_start_time_s

    def on_game_event(self, name: str, handler: GameEventHandler) -> None:
        """Register a handler for the named game event.

        Args:
            name: Event name, e.g. ``"dota_combatlog"``.
            handler: ``(GameEvent) -> None``.
        """
        self.game_event_manager.on_game_event(name, handler)

    def on_combat_log_entry(self, handler: CombatLogHandler) -> None:
        """Register a handler for all combat log entries (S1 + S2).

        Args:
            handler: ``(CombatLogEntry) -> None``.
        """
        self.combat_log.on_combat_log_entry(handler)

    def on_chat_message(self, handler: ChatCallback) -> None:
        """Register a handler for all-chat and team-chat messages.

        Args:
            handler: ``(ChatEntry) -> None``.
        """
        self._chat_callbacks.append(handler)

    def on_chat_event(self, handler: ChatEventCallback) -> None:
        """Register a handler for all CDOTAUserMsg_ChatEvent messages.

        Args:
            handler: ``(CDOTAUserMsg_ChatEvent, tick) -> None``.
        """
        self._chat_event_callbacks.append(handler)

    def on_neutral_item_found(self, handler: NeutralItemFoundCallback) -> None:
        """Register a handler for neutral item found messages.

        Args:
            handler: ``(NeutralItemFoundEvent) -> None``.
        """
        self._neutral_item_found_callbacks.append(handler)

    def on_game_start(self, callback: Callable[[int], None]) -> None:
        """Register a handler called once when game time reaches zero.

        The callback receives the game-start tick as its only argument.
        Fires when ``m_pGameRules.m_flGameStartTime`` transitions from 0 to
        non-zero on the ``CDOTAGamerulesProxy`` entity.

        Args:
            callback: ``(game_start_tick: int) -> None``.
        """
        self._game_start_callbacks.append(callback)

    def on_game_end(self, callback: Callable[[int], None]) -> None:
        """Register a handler called once when the ancient is destroyed.

        The callback receives the final game tick as its only argument.
        Fires when ``DOTA_COMBATLOG_GAME_STATE == 6`` is seen in the
        combat log, matching OpenDota's ``postGame`` sentinel.

        Args:
            callback: ``(tick: int) -> None``.
        """
        self._game_end_callbacks.append(callback)

    def _mark_game_end(self, tick: int) -> None:
        """Record a GAME_STATE==6 (postGame) marker for deferred dispatch.

        The actual game-end callbacks are not invoked here. They are flushed at
        the end of the inner-packet loop (see :meth:`_flush_game_end`) so that
        same-packet entity deltas — sorted at a higher priority than the wrapped
        ``svc_UserMessage`` combat-log path — are applied first. This keeps the
        three combat-log ingestion paths (direct HLTV, S1 game event, wrapped
        user message) consistent: terminal consumers always observe the final
        entity state, not a stale pre-delta snapshot.

        Args:
            tick: The game tick at which the postGame marker was seen.
        """
        if self._game_ended:
            return
        self._game_ended = True
        self._pending_game_end_tick = tick

    def _flush_game_end(self) -> None:
        """Dispatch any deferred game-end callbacks for the current packet."""
        if self._pending_game_end_tick is None:
            return
        tick = self._pending_game_end_tick
        self._pending_game_end_tick = None
        for cb in self._game_end_callbacks:
            cb(tick)

    def stop_after_tick(self, tick: int) -> None:
        """Stop parsing after this tick (inclusive).

        Args:
            tick: Game tick at which to stop.
        """
        self._stop_at_tick = tick

    # ------------------------------------------------------------------
    # Parse entry point
    # ------------------------------------------------------------------

    def parse(self) -> None:
        """Parse the replay from start to finish (or until stop_after_tick).

        Processes every outer message in order, decoding inner net messages
        from DEM_Packet / DEM_SignonPacket / DEM_FullPacket, and routing
        each to the appropriate subsystem handler.
        """
        try:
            with DemoStream(self._source) as stream:
                for tick, msg_type, data in stream:
                    self.tick = tick
                    if self._stop_at_tick is not None and tick > self._stop_at_tick:
                        break
                    self._dispatch_outer(msg_type, data)
        except Exception as exc:
            # Truncated files raise on the final corrupt snappy block — that is
            # expected for partial replays, so parsing continues with whatever was
            # read. Log at warning level: a genuine mid-stream decoder/extractor
            # bug is indistinguishable here from an expected truncated tail, so
            # surface it rather than letting silent partial output look complete.
            # Record it on the parser too, so consumers can detect a partial
            # parse programmatically instead of scraping logs.
            self.parse_error = exc
            self.truncated_at_tick = self.tick
            logger.warning("Replay stream ended early at tick %d: %r", self.tick, exc)

        # Read match metadata from CDOTAGamerulesProxy entity if DEM_FileInfo
        # didn't populate them (e.g. truncated replays or early stop).
        # Reference: refs/parser/src/main/java/opendota/Parse.java — uses
        # CDOTAGamerulesProxy.m_pGameRules.m_unMatchID64 / m_iGameMode
        if self.entity_manager is not None:
            grp = self.entity_manager.find_by_class_name("CDOTAGamerulesProxy")
            if grp is not None:
                fields = grp._resolve_fields(_GAMERULES_FIELDS)
                if not self.match_id:
                    v = grp._get_uint32_resolved(fields[5])
                    if v:
                        self.match_id = v
                if not self.game_mode:
                    v = grp._get_int32_resolved(fields[6])
                    if v:
                        self.game_mode = v
                if not self.leagueid:
                    v = grp._get_uint32_resolved(fields[7])
                    if v:
                        self.leagueid = v
                # Fallback for radiant_win when CDemoFileInfo.game_winner == 0
                # (common in tournament/HLTV replays). Uses EMatchOutcome:
                # 2 = RadVictory, 3 = DireVictory.
                # Reference: refs/manta/dota/dota_shared_enums.proto
                if self.radiant_win is None:
                    v = grp._get_int32_resolved(fields[8])
                    if v == 2:
                        self.radiant_win = True
                    elif v == 3:
                        self.radiant_win = False

    # ------------------------------------------------------------------
    # Outer message dispatch
    # ------------------------------------------------------------------

    def _dispatch_outer(self, msg_type: int, data: bytes) -> None:
        if msg_type == _DEM_FILE_INFO:
            fi = CDemoFileInfo()
            fi.ParseFromString(data)
            dota = fi.game_info.dota
            self.match_id = dota.match_id
            self.game_mode = dota.game_mode
            self.leagueid = dota.leagueid
            # game_winner: 2 = Radiant, 3 = Dire, 0 = unknown
            if dota.game_winner == 2:
                self.radiant_win = True
            elif dota.game_winner == 3:
                self.radiant_win = False

        elif msg_type == _DEM_SEND_TABLES:
            self._on_send_tables(data)

        elif msg_type == _DEM_CLASS_INFO:
            ci_msg = CDemoClassInfo()
            ci_msg.ParseFromString(data)
            self._on_class_info(ci_msg)

        elif msg_type in (_DEM_PACKET, _DEM_SIGNON_PACKET):
            pkt_msg = CDemoPacket()
            pkt_msg.ParseFromString(data)
            self._dispatch_inner_packet(pkt_msg.data)

        elif msg_type == _DEM_FULL_PACKET:
            full_msg = CDemoFullPacket()
            full_msg.ParseFromString(data)
            # String tables snapshot first, then inner packet
            if full_msg.HasField("packet"):
                self._dispatch_inner_packet(full_msg.packet.data)

    # ------------------------------------------------------------------
    # Inner packet dispatch
    # ------------------------------------------------------------------

    def _dispatch_inner_packet(self, data: bytes) -> None:
        if not data:
            return

        # Collect and sort: string table updates before packet entities
        messages = _read_inner_messages(data)

        def _priority(type_id: int) -> int:
            if type_id in (
                _NET_TICK,
                _SVC_SERVER_INFO,
                _SVC_CREATE_STRING_TABLE,
                _SVC_UPDATE_STRING_TABLE,
            ):
                return -10
            if type_id == _SVC_PACKET_ENTITIES:
                return 5
            if type_id in (_GE_GAME_EVENT, _DOTA_UM_COMBAT_LOG_HLTV):
                return 10
            return 0

        messages.sort(key=lambda m: _priority(m[0]))

        for type_id, payload in messages:
            self._dispatch_inner(type_id, payload)

        # Fire deferred game-end callbacks only after every message in this
        # packet — crucially the priority-5 svc_PacketEntities deltas — has been
        # applied, so terminal flushes read final entity state.
        self._flush_game_end()

    def _dispatch_inner(self, type_id: int, payload: bytes) -> None:
        if type_id == _NET_TICK:
            tick_msg = CNETMsg_Tick()
            tick_msg.ParseFromString(payload)
            self.net_tick = tick_msg.tick
            self._net_tick_seen = True

            # Match OpenDota/Clarity's @OnTickStart ordering: compute the clock
            # and notify samplers from the entity table reconstructed through
            # the previous tick, before this packet's entity deltas are applied.
            if self.entity_manager is not None:
                grp = self.entity_manager.find_by_class_name("CDOTAGamerulesProxy")
                if grp is not None:
                    self._update_game_clock(grp)
            for callback in self._tick_start_callbacks:
                callback(self.net_tick)

        elif type_id == _SVC_SERVER_INFO:
            m = CSVCMsg_ServerInfo()
            m.ParseFromString(payload)
            self._on_server_info(m)

        elif type_id == _SVC_CREATE_STRING_TABLE:
            create_msg = CSVCMsg_CreateStringTable()
            create_msg.ParseFromString(payload)
            table = handle_create(create_msg, self.string_tables)
            if self.entity_manager is not None and table.name == "instancebaseline":
                self.entity_manager.on_baseline_updated()

        elif type_id == _SVC_UPDATE_STRING_TABLE:
            update_msg = CSVCMsg_UpdateStringTable()
            update_msg.ParseFromString(payload)
            table = handle_update(update_msg, self.string_tables)
            if self.entity_manager is not None and table.name == "instancebaseline":
                self.entity_manager.on_baseline_updated()

        elif (
            type_id == _SVC_PACKET_ENTITIES
            and self.entity_manager is not None
            and self.entity_manager.class_id_size > 0
        ):
            pe_msg = CSVCMsg_PacketEntities()
            pe_msg.ParseFromString(payload)
            self.entity_manager._on_packet_entities(pe_msg)

        elif type_id == _SVC_USER_MESSAGE:
            um_msg = CSVCMsg_UserMessage()
            um_msg.ParseFromString(payload)
            self._on_user_message(um_msg)

        elif type_id == _GE_GAME_EVENT_LIST:
            gel_msg = CMsgSource1LegacyGameEventList()
            gel_msg.ParseFromString(payload)
            self._on_game_event_list(gel_msg)

        elif type_id == _GE_GAME_EVENT:
            ge_msg = CMsgSource1LegacyGameEvent()
            ge_msg.ParseFromString(payload)
            self._on_game_event(ge_msg)

        elif type_id == _DOTA_UM_COMBAT_LOG_HLTV:
            entry_msg = CMsgDOTACombatLogEntry()
            entry_msg.ParseFromString(payload)
            game_time_s = self._combat_log_game_time_s(entry_msg)
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                self.combat_log.process_s2_entry(
                    entry_msg, name_table, tick=self.tick, game_time_s=game_time_s
                )
            # DOTA_COMBATLOG_GAME_STATE == 6 → ancient destroyed (postGame)
            # Reference: refs/parser/src/main/java/opendota/Parse.java line 373
            if entry_msg.type == 9 and entry_msg.value == 6:
                self._mark_game_end(self.tick)

        elif type_id == _DOTA_UM_CHAT_EVENT:
            chat_event = CDOTAUserMsg_ChatEvent()
            chat_event.ParseFromString(payload)
            if chat_event.type == _CHAT_MSG_RUNE_PICKUP:
                self.combat_log.process_rune_pickup(
                    chat_event.playerid_1, chat_event.value, tick=self.tick
                )
            for chat_cb in self._chat_event_callbacks:
                chat_cb(chat_event, self.tick)

        elif type_id == _DOTA_UM_MATCH_METADATA:
            self._on_match_metadata(payload)

        elif type_id == _DOTA_UM_MATCH_DETAILS:
            self._on_match_details(payload)

        elif type_id == _DOTA_UM_FOUND_NEUTRAL_ITEM:
            self._emit_neutral_item_found(payload)

        elif type_id == _DOTA_UM_CHAT_MESSAGE:
            self._emit_chat_message(payload)

    # ------------------------------------------------------------------
    # Subsystem handlers
    # ------------------------------------------------------------------

    def _on_send_tables(self, data: bytes) -> None:
        serializers = parse_send_tables(data, self.game_build)
        self.entity_manager = EntityManager(serializers, self.string_tables)
        for registration in self._entity_callbacks:
            if registration.filtered:
                self.entity_manager._on_entity_filtered(
                    registration.callback,
                    class_names=registration.class_names,
                    class_prefixes=registration.class_prefixes,
                )
            else:
                self.entity_manager.on_entity(registration.callback)
        # Apply ServerInfo if it arrived before the send tables
        if self._pending_server_info is not None:
            self._on_server_info(self._pending_server_info)
            self._pending_server_info = None

    def _on_server_info(self, msg: CSVCMsg_ServerInfo) -> None:
        if self.entity_manager is None:
            # Entity manager not built yet — cache and apply after send tables
            self._pending_server_info = msg
            return
        self.entity_manager.on_server_info(msg)
        self.game_build = self.entity_manager.game_build

    def _on_class_info(self, msg: CDemoClassInfo) -> None:
        if self.entity_manager is not None:
            self.entity_manager.on_class_info(msg)
            self.entity_manager.on_baseline_updated()

    def _on_game_event_list(self, msg: CMsgSource1LegacyGameEventList) -> None:
        for descriptor in msg.descriptors:
            schema_dict = {
                "eventid": descriptor.eventid,
                "name": descriptor.name,
                "keys": [{"name": k.name, "type": k.type} for k in descriptor.keys],
            }
            self.game_event_manager.register_schema(schema_dict)

    def _on_game_event(self, msg: CMsgSource1LegacyGameEvent) -> None:
        self.game_event_manager.dispatch(msg)

        # S1 combat log path: dota_combatlog game event
        schema = self.game_event_manager.get_schema(msg.eventid)
        if schema is not None and schema.name == "dota_combatlog":
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                from gem.state.game_events import GameEvent

                event = GameEvent(schema=schema, msg=msg)
                self.combat_log.process_s1_event(event, name_table, tick=self.tick)
                # DOTA_COMBATLOG_GAME_STATE == 6 → ancient destroyed (postGame)
                type_val, _ = event.get_int32("type")
                value_val, _ = event.get_int32("value")
                if type_val == 9 and value_val == 6:
                    self._mark_game_end(self.tick)

    def _on_user_message(self, msg: CSVCMsg_UserMessage) -> None:
        if msg.msg_type in (_DOTA_UM_COMBAT_LOG_DATA, _DOTA_UM_COMBAT_LOG_BULK_DATA):
            bulk_msg = CDOTAUserMsg_CombatLogBulkData()
            bulk_msg.ParseFromString(msg.msg_data)
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                for entry_msg in bulk_msg.combat_entries:
                    game_time_s = self._combat_log_game_time_s(entry_msg)
                    self.combat_log.process_s2_entry(
                        entry_msg, name_table, tick=self.tick, game_time_s=game_time_s
                    )
                    if entry_msg.type == 9 and entry_msg.value == 6:
                        self._mark_game_end(self.tick)
        elif msg.msg_type == _DOTA_UM_MATCH_METADATA:
            self._on_match_metadata(msg.msg_data)
        elif msg.msg_type == _DOTA_UM_MATCH_DETAILS:
            self._on_match_details(msg.msg_data)

    def _combat_log_game_time_s(self, msg: CMsgDOTACombatLogEntry) -> int | None:
        """Return OpenDota-style game-relative combat-log time for an S2 entry.

        OpenDota anchors combat-log time at the GAME_STATE==5 timestamp, then
        subtracts that rounded timestamp from subsequent combat-log timestamps.
        Keep this separate from raw ticks so public replay timing remains tick-
        based while parity checks can use the OpenDota clock.

        Side effect: refreshes :attr:`combat_log_time_s`, the running combat-log
        axis clock, so entity-driven consumers (e.g. the interval extractor) can
        sample minute boundaries on the same axis OpenDota uses.
        """
        timestamp = getattr(msg, "timestamp", None)
        if timestamp is None:
            return None

        raw_time_s = _round_positive_seconds(timestamp)
        if msg.type == 9 and msg.value == 5 and self._combat_log_game_start_time_s is None:
            self._combat_log_game_start_time_s = raw_time_s

        if self._combat_log_game_start_time_s is None:
            return None
        game_time_s = raw_time_s - self._combat_log_game_start_time_s
        self.combat_log_time_s = game_time_s
        # The GAME_STATE==6 (ancient destroyed / postGame) timestamp on the
        # horn-anchored combat-log axis is OpenDota's match ``duration``. Capture
        # it once, before the game-end callbacks fire. Reference:
        # refs/parser/src/main/java/opendota/Parse.java postGame handling.
        if msg.type == 9 and msg.value == 6 and self.duration_s is None:
            self.duration_s = game_time_s
        return game_time_s

    def _on_match_metadata(self, payload: bytes) -> None:
        metadata = CDOTAMatchMetadataFile()
        metadata.ParseFromString(payload)
        self.match_metadata = metadata

    def _on_match_details(self, payload: bytes) -> None:
        """Store the embedded Game Coordinator postgame match summary."""
        details = CMsgDOTAMatch()
        details.ParseFromString(payload)
        self.match_details = details
        if not self.match_id and details.HasField("match_id"):
            self.match_id = int(details.match_id)

    def _emit_chat_message(self, payload: bytes) -> None:
        if not self._chat_callbacks:
            return
        chat_msg = CDOTAUserMsg_ChatMessage()
        chat_msg.ParseFromString(payload)
        # channel_type 11 = all-chat; anything else treated as team-chat
        channel = "all" if chat_msg.channel_type == 11 else "team"
        entry = ChatEntry(
            tick=self.tick,
            player_slot=chat_msg.source_player_id,
            channel=channel,
            text=chat_msg.message_text,
        )
        for cb in self._chat_callbacks:
            cb(entry)

    def _emit_neutral_item_found(self, payload: bytes) -> None:
        if not self._neutral_item_found_callbacks:
            return
        msg = CDOTAUserMsg_FoundNeutralItem()
        msg.ParseFromString(payload)
        event = NeutralItemFoundEvent(
            tick=self.tick,
            player_id=msg.player_id,
            item_ability_id=msg.item_ability_id,
            item_key=item_key_by_id(msg.item_ability_id) or "",
            item_tier=msg.item_tier,
            tier_item_count=msg.tier_item_count,
            enhancement_ability_id=msg.enhancement_ability_id,
            enhancement_key=item_key_by_id(msg.enhancement_ability_id) or "",
            enhancement_level=msg.enhancement_level,
            trinket_level=msg.trinket_level,
        )
        for cb in self._neutral_item_found_callbacks:
            cb(event)
