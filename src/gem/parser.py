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
from pathlib import Path

from google.protobuf.message import DecodeError, Message

from gem.binary.packet import read_inner_messages
from gem.binary.stream import DemoStream
from gem.catalog import item_key_by_id
from gem.combat.log import CombatLogHandler, CombatLogProcessor, CombatLogSource
from gem.errors import ReplayDataError
from gem.proto.demo_pb2 import (
    CDemoClassInfo,
    CDemoFileInfo,
    CDemoFullPacket,
    CDemoPacket,
    DEM_ClassInfo,
    DEM_FileInfo,
    DEM_FullPacket,
    DEM_Packet,
    DEM_SendTables,
    DEM_SignonPacket,
)
from gem.proto.dota_gcmessages_common_pb2 import CMsgDOTAMatch
from gem.proto.dota_match_metadata_pb2 import CDOTAMatchMetadataFile
from gem.proto.dota_shared_enums_pb2 import (
    DOTA_COMBATLOG_GAME_STATE,
    DOTA_GAMERULES_STATE_POST_GAME,
    CMsgDOTACombatLogEntry,
    DOTAChannelType_GameAll,
    DOTAChannelType_GameAllies,
)
from gem.proto.dota_usermessages_pb2 import (
    CHAT_MESSAGE_RUNE_PICKUP,
    CDOTAUserMsg_ChatEvent,
    CDOTAUserMsg_ChatMessage,
    CDOTAUserMsg_CombatLogBulkData,
    CDOTAUserMsg_FoundNeutralItem,
    DOTA_UM_ChatEvent,
    DOTA_UM_ChatMessage,
    DOTA_UM_CombatLogBulkData,
    DOTA_UM_CombatLogData,
    DOTA_UM_CombatLogDataHLTV,
    DOTA_UM_FoundNeutralItem,
    DOTA_UM_MatchDetails,
    DOTA_UM_MatchMetadata,
)
from gem.proto.gameevents_pb2 import (
    CMsgSource1LegacyGameEvent,
    CMsgSource1LegacyGameEventList,
    GE_Source1LegacyGameEvent,
    GE_Source1LegacyGameEventList,
)
from gem.proto.netmessages_pb2 import (
    CSVCMsg_CreateStringTable,
    CSVCMsg_PacketEntities,
    CSVCMsg_ServerInfo,
    CSVCMsg_UpdateStringTable,
    CSVCMsg_UserMessage,
    svc_ClearAllStringTables,
    svc_CreateStringTable,
    svc_PacketEntities,
    svc_ServerInfo,
    svc_UpdateStringTable,
    svc_UserMessage,
)
from gem.proto.networkbasetypes_pb2 import CNETMsg_Tick, net_Tick
from gem.results.models import ChatEntry, NeutralItemFoundEvent
from gem.schema.sendtable import parse_send_tables
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import (
    Entity,
    EntityManager,
    EntityOp,
    EntityTracker,
    game_build_from_game_dir,
)
from gem.state.game_clock import GameClock, GameClockTracker
from gem.state.game_events import GameEvent, GameEventHandler, GameEventManager
from gem.state.string_table import StringTables, handle_create, handle_update

logger = logging.getLogger(__name__)

# Match metadata read from the game-rules entity when DEM_FileInfo lacks it.
_MATCH_FIELDS = FieldAccessPlan(
    (
        "m_pGameRules.m_unMatchID64",
        "m_pGameRules.m_iGameMode",
        "m_pGameRules.m_unLeagueID",
        "m_pGameRules.m_nGameWinner",
    )
)

# ---------------------------------------------------------------------------
# Outer EDemoCommands IDs (stripped of DEM_IsCompressed = 0x40)
# ---------------------------------------------------------------------------
_DEM_FILE_INFO = DEM_FileInfo
_DEM_SEND_TABLES = DEM_SendTables
_DEM_CLASS_INFO = DEM_ClassInfo
_DEM_PACKET = DEM_Packet
_DEM_SIGNON_PACKET = DEM_SignonPacket
_DEM_FULL_PACKET = DEM_FullPacket

# Inner NET/SVC/game-event message IDs
_NET_TICK = net_Tick
_SVC_SERVER_INFO = svc_ServerInfo
_SVC_CLEAR_ALL_STRING_TABLES = svc_ClearAllStringTables
_SVC_CREATE_STRING_TABLE = svc_CreateStringTable
_SVC_UPDATE_STRING_TABLE = svc_UpdateStringTable
_SVC_PACKET_ENTITIES = svc_PacketEntities
_SVC_USER_MESSAGE = svc_UserMessage
_GE_GAME_EVENT_LIST = GE_Source1LegacyGameEventList
_GE_GAME_EVENT = GE_Source1LegacyGameEvent

# Combat-log IDs accepted inside CSVCMsg_UserMessage.msg_type. Both carry a
# CDOTAUserMsg_CombatLogBulkData. Unverified: no replay we have contains these, and
# Clarity doesn't parse them either (skadistats/clarity CombatLog.java logs a warning
# asking for such a replay, issue #58). Current replays send one
# DOTA_UM_CombatLogDataHLTV per combat-log line instead.
_DOTA_UM_COMBAT_LOG_DATA = DOTA_UM_CombatLogData
_DOTA_UM_COMBAT_LOG_BULK_DATA = DOTA_UM_CombatLogBulkData

# Dota user messages sent directly as inner messages (not wrapped in svc_UserMessage)
_DOTA_UM_COMBAT_LOG_HLTV = DOTA_UM_CombatLogDataHLTV  # CMsgDOTACombatLogEntry, one per message
_DOTA_UM_CHAT_EVENT = DOTA_UM_ChatEvent  # CDOTAUserMsg_ChatEvent
_GAME_RULES_CLASS = "CDOTAGamerulesProxy"
_DOTA_UM_MATCH_METADATA = DOTA_UM_MatchMetadata  # CDOTAMatchMetadataFile
_DOTA_UM_MATCH_DETAILS = DOTA_UM_MatchDetails  # CMsgDOTAMatch postgame summary
_DOTA_UM_FOUND_NEUTRAL_ITEM = DOTA_UM_FoundNeutralItem  # CDOTAUserMsg_FoundNeutralItem
_DOTA_UM_CHAT_MESSAGE = DOTA_UM_ChatMessage  # CDOTAUserMsg_ChatMessage

_CHAT_MSG_RUNE_PICKUP = CHAT_MESSAGE_RUNE_PICKUP


def _chat_channel_label(channel_type: int) -> str:
    """Return the ``ChatEntry.channel`` label for a ``DOTAChatChannelType_t`` value.

    All-chat and team chat get names. Every other channel (spectator, coach,
    broadcast, ...) keeps its raw number as a string, as OpenDota does
    (odota/parser ``Parse.java`` ``onAllChatMessage``).
    """
    if channel_type == DOTAChannelType_GameAll:
        return "all"
    if channel_type == DOTAChannelType_GameAllies:
        return "team"
    return str(channel_type)


def _is_game_state(log_type: int, value: int, state: int) -> bool:
    """Return whether a combat-log entry is a ``DOTA_COMBATLOG_GAME_STATE`` change to ``state``.

    OpenDota anchors game time on the ``GAME_IN_PROGRESS`` entry and marks the end of
    the match on ``POST_GAME`` (odota/parser ``Parse.java``, pinned in CLAUDE.md).
    """
    return log_type == DOTA_COMBATLOG_GAME_STATE and value == state


# CombatLogNames string table name
_COMBAT_LOG_NAMES_TABLE = "CombatLogNames"


def _parse_proto(message: Message, payload: bytes) -> None:
    """Decode *payload* into *message*, reporting bad bytes as replay-data errors.

    Only gem's own decoding goes through here, so a ``DecodeError`` raised inside
    a callback is not mistaken for corrupt replay data.
    """
    try:
        message.ParseFromString(payload)
    except DecodeError as exc:
        raise ReplayDataError(f"invalid {type(message).__name__} payload") from exc


EntityCallback = Callable[[Entity, EntityOp], None]
TickStartCallback = Callable[[int], None]
PacketEndCallback = Callable[[int], None]
ChatCallback = Callable[["ChatEntry"], None]
ChatEventCallback = Callable[["CDOTAUserMsg_ChatEvent", int], None]
NeutralItemFoundCallback = Callable[["NeutralItemFoundEvent"], None]


class ReplayParser:
    """Drives a full Source 2 replay parse, wiring all subsystems together.

    Usage::

        parser = ReplayParser("game.dem")
        parser.on_entity(lambda e, op: print(e, op))
        parser.on_combat_log_entry(lambda e: print(e))
        parser.parse()

    Attributes:
        tick: Current game tick.
        net_tick: Current net tick (from net_Tick inner messages).
        game_time_s: Rounded game-relative clock refreshed at network tick start.
        game_clock: Pause-aware tick/game-time anchors and observed pauses.
        post_game_tick: Tick of the GAME_STATE==6 (postGame) marker, when seen.
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
        self._clock = GameClockTracker()
        self.game_build: int = 0
        self.string_tables = StringTables()
        self.entity_manager: EntityManager | None = None
        self.game_event_manager = GameEventManager()
        self.combat_log = CombatLogProcessor()
        # Handlers can be registered before the schema arrives, so the parser
        # owns the tracker and hands it to the entity manager once it exists.
        self._entity_tracker = EntityTracker()
        self._tick_start_callbacks: list[TickStartCallback] = []
        self._packet_end_callbacks: list[PacketEndCallback] = []
        self._chat_callbacks: list[ChatCallback] = []
        self._chat_event_callbacks: list[ChatEventCallback] = []
        self._game_rules: Entity | None = None
        self._neutral_item_found_callbacks: list[NeutralItemFoundCallback] = []
        self._stop_at_tick: int | None = None
        self._pending_server_info: CSVCMsg_ServerInfo | None = None
        self.match_id: int = 0
        self.game_mode: int = 0
        self.leagueid: int = 0
        self.match_metadata: CDOTAMatchMetadataFile | None = None
        self.match_details: CMsgDOTAMatch | None = None
        self.radiant_win: bool | None = None
        self.post_game_tick: int | None = None
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
        self._on_entity_filtered(
            self._on_entity_game_start,
            class_names=("CDOTAGamerulesProxy",),
        )

    # ------------------------------------------------------------------
    # Clock readings (kept by GameClockTracker)
    # ------------------------------------------------------------------

    @property
    def net_tick(self) -> int:
        """Current net tick (from ``net_Tick`` inner messages)."""
        return self._clock.net_tick

    @net_tick.setter
    def net_tick(self, value: int) -> None:
        self._clock.net_tick = value

    @property
    def game_time_s(self) -> int | None:
        """Rounded game-relative clock, refreshed at network-tick start."""
        return self._clock.game_time_s

    @game_time_s.setter
    def game_time_s(self, value: int | None) -> None:
        self._clock.game_time_s = value

    @property
    def raw_game_time_s(self) -> int | None:
        """Rounded server game time before the game-start shift, from pregame on."""
        return self._clock.raw_time_s

    @property
    def opendota_tick_start_raw_s(self) -> int | None:
        """OpenDota's running clock at this outer tick's start, before the game-start shift.

        OpenDota stamps chat events (rune pickups, first blood, courier and
        Roshan kills, Aegis) with this value; subtract :attr:`opendota_start_s`.
        """
        return self._clock.tick_start_raw_s

    @property
    def opendota_start_s(self) -> int | None:
        """OpenDota's rounded game-start anchor, latched when first seen."""
        return self._clock.opendota_start_s

    def _game_rules_entity(self) -> Entity | None:
        """Return the live ``CDOTAGamerulesProxy``, caching the lookup."""
        em = self.entity_manager
        if em is None:
            return None
        cached = self._game_rules
        # A deleted entity leaves the manager's table but keeps ``active``, so
        # trust the cache only while it is still the live entity at its index.
        if (
            cached is not None
            and cached.active
            and 0 <= cached.get_index() < len(em.entities)
            and em.entities[cached.get_index()] is cached
        ):
            return cached
        self._game_rules = em.find_by_class_name(_GAME_RULES_CLASS)
        return self._game_rules

    @property
    def game_clock(self) -> GameClock:
        """Pause-aware tick/game-time anchors and observed pauses."""
        return self._clock.clock

    @game_clock.setter
    def game_clock(self, value: GameClock) -> None:
        self._clock.clock = value

    @property
    def game_start_tick(self) -> int | None:
        """Replay tick at which the game start (horn) was first seen."""
        return self._clock.game_start_tick

    @game_start_tick.setter
    def game_start_tick(self, value: int | None) -> None:
        self._clock.game_start_tick = value

    @property
    def combat_log_time_s(self) -> int | None:
        """Horn-anchored time of the latest timed combat-log entry.

        This is an event clock, not a continuously advancing sampling clock;
        interval consumers use ``game_time_s`` instead.
        """
        return self._clock.combat_log_time_s

    @combat_log_time_s.setter
    def combat_log_time_s(self, value: int | None) -> None:
        self._clock.combat_log_time_s = value

    @property
    def duration_s(self) -> int | None:
        """OpenDota-style match duration: combat-log time at ``POST_GAME``."""
        return self._clock.duration_s

    @duration_s.setter
    def duration_s(self, value: int | None) -> None:
        self._clock.duration_s = value

    # ------------------------------------------------------------------
    # Public callback registration
    # ------------------------------------------------------------------

    def on_entity(self, callback: EntityCallback) -> None:
        """Register a handler called for every entity create/update/delete.

        Args:
            callback: ``(Entity, EntityOp) -> None``.
        """
        self._entity_tracker.on_entity(callback)

    def _on_entity_filtered(
        self,
        callback: EntityCallback,
        *,
        class_names: Iterable[str] = (),
        class_prefixes: Iterable[str] = (),
    ) -> None:
        """Register an internal callback for selected entity classes."""
        self._entity_tracker._on_entity_filtered(
            callback, class_names=class_names, class_prefixes=class_prefixes
        )

    def _on_entity_fields(
        self,
        callback: EntityCallback,
        *,
        required_fields: Iterable[str],
        changed_fields: Iterable[str] = (),
    ) -> None:
        """Register an internal callback for schema and decoded-path changes."""
        self._entity_tracker._on_entity_fields(
            callback, required_fields=required_fields, changed_fields=changed_fields
        )

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

    def _on_packet_end(self, callback: PacketEndCallback) -> None:
        """Register an internal completed-packet callback.

        Callbacks run after every sorted inner message has been dispatched and
        before a deferred game-end flush. This boundary is intentionally private:
        it exists for extractors that need a stable entity view, not as a public
        replay-parser event API.
        """
        self._packet_end_callbacks.append(callback)

    def _on_entity_game_start(self, entity: Entity, op: EntityOp) -> None:
        if entity.get_class_name() != "CDOTAGamerulesProxy":
            return
        if self._clock.observe_game_start(entity, self.tick):
            for cb in self._game_start_callbacks:
                cb(self.tick)

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
        Fires when a ``DOTA_COMBATLOG_GAME_STATE`` entry with value
        ``DOTA_GAMERULES_STATE_POST_GAME`` is seen in the combat log, matching
        OpenDota's ``postGame`` sentinel.

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
        self.post_game_tick = tick
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

        A problem in the replay data (a :class:`gem.ReplayDataError`: a truncated
        file, or a corrupt frame, protobuf, or bitstream) ends the parse early: the reason is stored in
        :attr:`parse_error` and :attr:`truncated_at_tick`, a warning is logged,
        and everything read so far is kept. Any other exception, such as a bug in
        a registered callback, propagates.

        Raises:
            Exception: Whatever a registered callback or extractor raised.
        """
        try:
            with DemoStream(self._source) as stream:
                outer_tick = None
                for tick, msg_type, data in stream:
                    self.tick = tick
                    if self._stop_at_tick is not None and tick > self._stop_at_tick:
                        break
                    if tick != outer_tick:
                        # OpenDota's @OnTickStart clock: before this tick's
                        # messages, so the network tick has not advanced yet.
                        outer_tick = tick
                        self._clock.snapshot_tick_start(self._game_rules_entity())
                    self._dispatch_outer(msg_type, data)
        except ReplayDataError as exc:
            # Truncated or corrupt replays keep what was read. Record the reason,
            # so consumers can tell a partial parse from a complete one.
            self.parse_error = exc
            self.truncated_at_tick = self.tick
            logger.warning("Replay stream ended early at tick %d: %r", self.tick, exc)

        # A replay that ended mid-pause keeps the pause open-ended.
        self._clock.finish()

        # Read match metadata from CDOTAGamerulesProxy entity if DEM_FileInfo
        # didn't populate them (e.g. truncated replays or early stop).
        # Reference: odota/parser src/main/java/opendota/Parse.java — uses
        # CDOTAGamerulesProxy.m_pGameRules.m_unMatchID64 / m_iGameMode
        if self.entity_manager is not None:
            grp = self.entity_manager.find_by_class_name("CDOTAGamerulesProxy")
            if grp is not None:
                fields = grp._resolve_fields(_MATCH_FIELDS)
                if not self.match_id:
                    v = grp._get_uint32_resolved(fields[0])
                    if v:
                        self.match_id = v
                if not self.game_mode:
                    v = grp._get_int32_resolved(fields[1])
                    if v:
                        self.game_mode = v
                if not self.leagueid:
                    v = grp._get_uint32_resolved(fields[2])
                    if v:
                        self.leagueid = v
                # Fallback for radiant_win when CDemoFileInfo.game_winner == 0
                # (common in tournament/HLTV replays). Uses EMatchOutcome:
                # 2 = RadVictory, 3 = DireVictory.
                # Reference: dota_shared_enums.proto
                if self.radiant_win is None:
                    v = grp._get_int32_resolved(fields[3])
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
            _parse_proto(fi, data)
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
            _parse_proto(ci_msg, data)
            self._on_class_info(ci_msg)

        elif msg_type in (_DEM_PACKET, _DEM_SIGNON_PACKET):
            pkt_msg = CDemoPacket()
            _parse_proto(pkt_msg, data)
            self._dispatch_inner_packet(pkt_msg.data)

        elif msg_type == _DEM_FULL_PACKET:
            full_msg = CDemoFullPacket()
            _parse_proto(full_msg, data)
            # The string_table snapshot is skipped, as in Manta: the string tables are
            # already current from the svc_*StringTable messages.
            if full_msg.HasField("packet"):
                self._dispatch_inner_packet(full_msg.packet.data)

    # ------------------------------------------------------------------
    # Inner packet dispatch
    # ------------------------------------------------------------------

    def _dispatch_inner_packet(self, data: bytes) -> None:
        # Collect and sort: string table updates before packet entities
        messages = read_inner_messages(data)

        def _priority(type_id: int) -> int:
            # The sort is stable, so string-table messages keep their stream order.
            if type_id in (
                _NET_TICK,
                _SVC_SERVER_INFO,
                _SVC_CLEAR_ALL_STRING_TABLES,
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

        for callback in self._packet_end_callbacks:
            callback(self.tick)

        # Fire deferred game-end callbacks only after every message in this
        # packet — crucially the priority-5 svc_PacketEntities deltas — has been
        # applied, so terminal flushes read final entity state.
        self._flush_game_end()

    def _dispatch_inner(self, type_id: int, payload: bytes) -> None:
        if type_id == _NET_TICK:
            tick_msg = CNETMsg_Tick()
            _parse_proto(tick_msg, payload)
            self._clock.on_net_tick(tick_msg.tick)

            # Match OpenDota/Clarity's @OnTickStart ordering: compute the clock
            # and notify samplers from the entity table reconstructed through
            # the previous tick, before this packet's entity deltas are applied.
            grp = self._game_rules_entity()
            if grp is not None:
                self._clock.update(grp, self.tick)
            for callback in self._tick_start_callbacks:
                callback(self.net_tick)

        elif type_id == _SVC_SERVER_INFO:
            m = CSVCMsg_ServerInfo()
            _parse_proto(m, payload)
            self._on_server_info(m)

        elif type_id == _SVC_CLEAR_ALL_STRING_TABLES:
            # Replays send this once, alone, before any table exists (Clarity
            # handles it the same way: S2StringTableEmitter.clearAllStringTables).
            self.string_tables.clear()

        elif type_id == _SVC_CREATE_STRING_TABLE:
            create_msg = CSVCMsg_CreateStringTable()
            _parse_proto(create_msg, payload)
            table = handle_create(create_msg, self.string_tables)
            if self.entity_manager is not None and table.name == "instancebaseline":
                self.entity_manager.on_baseline_updated()

        elif type_id == _SVC_UPDATE_STRING_TABLE:
            update_msg = CSVCMsg_UpdateStringTable()
            _parse_proto(update_msg, payload)
            table = handle_update(update_msg, self.string_tables)
            if self.entity_manager is not None and table.name == "instancebaseline":
                self.entity_manager.on_baseline_updated()

        elif (
            type_id == _SVC_PACKET_ENTITIES
            and self.entity_manager is not None
            and self.entity_manager.class_id_size > 0
        ):
            pe_msg = CSVCMsg_PacketEntities()
            _parse_proto(pe_msg, payload)
            self.entity_manager._on_packet_entities(pe_msg)

        elif type_id == _SVC_USER_MESSAGE:
            um_msg = CSVCMsg_UserMessage()
            _parse_proto(um_msg, payload)
            self._on_user_message(um_msg)

        elif type_id == _GE_GAME_EVENT_LIST:
            gel_msg = CMsgSource1LegacyGameEventList()
            _parse_proto(gel_msg, payload)
            self._on_game_event_list(gel_msg)

        elif type_id == _GE_GAME_EVENT:
            ge_msg = CMsgSource1LegacyGameEvent()
            _parse_proto(ge_msg, payload)
            self._on_game_event(ge_msg)

        elif type_id == _DOTA_UM_COMBAT_LOG_HLTV:
            entry_msg = CMsgDOTACombatLogEntry()
            _parse_proto(entry_msg, payload)
            game_time_s = self._combat_log_time(entry_msg)
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                self.combat_log.process_s2_entry(
                    entry_msg, name_table, tick=self.tick, game_time_s=game_time_s
                )
            if _is_game_state(entry_msg.type, entry_msg.value, DOTA_GAMERULES_STATE_POST_GAME):
                self._mark_game_end(self.tick)

        elif type_id == _DOTA_UM_CHAT_EVENT:
            chat_event = CDOTAUserMsg_ChatEvent()
            _parse_proto(chat_event, payload)
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
        self.entity_manager = EntityManager(
            serializers, self.string_tables, tracker=self._entity_tracker
        )
        # Apply ServerInfo if it arrived before the send tables
        if self._pending_server_info is not None:
            self._on_server_info(self._pending_server_info)
            self._pending_server_info = None

    def _on_server_info(self, msg: CSVCMsg_ServerInfo) -> None:
        # Record the build now, as Manta does: DEM_SendTables arrives after
        # ServerInfo, and its build-specific field patches depend on it.
        build = game_build_from_game_dir(msg.game_dir)
        if build:
            self.game_build = build
        if self.entity_manager is None:
            # Entity manager not built yet — cache and apply after send tables
            self._pending_server_info = msg
            return
        self.entity_manager.on_server_info(msg)
        self.game_build = self.entity_manager.game_build

    def _on_class_info(self, msg: CDemoClassInfo) -> None:
        if self.entity_manager is not None:
            self.entity_manager.on_class_info(msg)

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

        # S1 combat log path: dota_combatlog game events, used by older replays (current
        # replays declare the event but send DOTA_UM_CombatLogDataHLTV instead). Clarity
        # handles the same path (skadistats/clarity CombatLog.java).
        schema = self.game_event_manager.get_schema(msg.eventid)
        if schema is not None and schema.name == "dota_combatlog":
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                event = GameEvent(schema=schema, msg=msg)
                self.combat_log.process_s1_event(event, name_table, tick=self.tick)
                type_val, _ = event.get_int32("type")
                value_val, _ = event.get_int32("value")
                if _is_game_state(type_val, value_val, DOTA_GAMERULES_STATE_POST_GAME):
                    self._mark_game_end(self.tick)

    def _on_user_message(self, msg: CSVCMsg_UserMessage) -> None:
        if msg.msg_type in (_DOTA_UM_COMBAT_LOG_DATA, _DOTA_UM_COMBAT_LOG_BULK_DATA):
            bulk_msg = CDOTAUserMsg_CombatLogBulkData()
            _parse_proto(bulk_msg, msg.msg_data)
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                for entry_msg in bulk_msg.combat_entries:
                    game_time_s = self._combat_log_time(entry_msg)
                    self.combat_log.process_s2_entry(
                        entry_msg,
                        name_table,
                        tick=self.tick,
                        game_time_s=game_time_s,
                        source=CombatLogSource.S2_BULK,
                    )
                    if _is_game_state(
                        entry_msg.type, entry_msg.value, DOTA_GAMERULES_STATE_POST_GAME
                    ):
                        self._mark_game_end(self.tick)
        elif msg.msg_type == _DOTA_UM_MATCH_METADATA:
            self._on_match_metadata(msg.msg_data)
        elif msg.msg_type == _DOTA_UM_MATCH_DETAILS:
            self._on_match_details(msg.msg_data)

    def _combat_log_time(self, msg: CMsgDOTACombatLogEntry) -> int | None:
        """Return OpenDota-style game-relative time for an S2 combat-log entry."""
        timestamp = msg.timestamp if msg.HasField("timestamp") else None
        game_state = msg.value if msg.type == DOTA_COMBATLOG_GAME_STATE else None
        return self._clock.combat_log_time(timestamp, game_state)

    def _on_match_metadata(self, payload: bytes) -> None:
        metadata = CDOTAMatchMetadataFile()
        _parse_proto(metadata, payload)
        self.match_metadata = metadata

    def _on_match_details(self, payload: bytes) -> None:
        """Store the embedded Game Coordinator postgame match summary."""
        details = CMsgDOTAMatch()
        _parse_proto(details, payload)
        self.match_details = details
        if not self.match_id and details.HasField("match_id"):
            self.match_id = int(details.match_id)

    def _emit_chat_message(self, payload: bytes) -> None:
        if not self._chat_callbacks:
            return
        chat_msg = CDOTAUserMsg_ChatMessage()
        _parse_proto(chat_msg, payload)
        channel = _chat_channel_label(chat_msg.channel_type)
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
        _parse_proto(msg, payload)
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
