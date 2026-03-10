"""High-level replay parser for Dota 2 Source 2 .dem files.

Ties together the stream reader, sendtable schema, string tables, entity
manager, game events, and combat log into a single ``ReplayParser`` class.
Callers register callbacks for the events they care about and then call
``parse()`` to drive the loop.

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

Reference: manta/parser.go, manta/demo_packet.go, manta/game_event.go
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

# Proto side-effect import order is critical
from google.protobuf import descriptor_pb2  # noqa: F401

from gem.combatlog import CombatLogHandler, CombatLogProcessor
from gem.entities import Entity, EntityManager, EntityOp
from gem.game_events import GameEventHandler, GameEventManager
from gem.models import ChatEntry
from gem.proto.dota2 import (
    dota_commonmessages_pb2,  # noqa: F401
    dota_shared_enums_pb2,  # noqa: F401
    network_connection_pb2,  # noqa: F401
    networkbasetypes_pb2,  # noqa: F401
)
from gem.proto.dota2.demo_pb2 import CDemoClassInfo, CDemoFileInfo, CDemoFullPacket, CDemoPacket
from gem.proto.dota2.dota_shared_enums_pb2 import CMsgDOTACombatLogEntry
from gem.proto.dota2.dota_usermessages_pb2 import (
    CDOTAUserMsg_ChatEvent,
    CDOTAUserMsg_ChatMessage,
    CDOTAUserMsg_CombatLogBulkData,
)
from gem.proto.dota2.gameevents_pb2 import (
    CMsgSource1LegacyGameEvent,
    CMsgSource1LegacyGameEventList,
)
from gem.proto.dota2.netmessages_pb2 import (
    CSVCMsg_CreateStringTable,
    CSVCMsg_PacketEntities,
    CSVCMsg_ServerInfo,
    CSVCMsg_UpdateStringTable,
    CSVCMsg_UserMessage,
)
from gem.reader import BitReader
from gem.sendtable import parse_send_tables
from gem.stream import DemoStream
from gem.string_table import StringTables, handle_create, handle_update

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
_DOTA_UM_CHAT_MESSAGE = 612  # CDOTAUserMsg_ChatMessage (direct)

_CHAT_MSG_RUNE_PICKUP = 22  # DOTA_CHAT_MESSAGE.CHAT_MESSAGE_RUNE_PICKUP

# CombatLogNames string table name
_COMBAT_LOG_NAMES_TABLE = "CombatLogNames"

EntityCallback = Callable[[Entity, EntityOp], None]
ChatCallback = Callable[["ChatEntry"], None]
ChatEventCallback = Callable[["CDOTAUserMsg_ChatEvent", int], None]


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
        game_build: Build number extracted from CSVCMsg_ServerInfo.
        string_tables: All string tables created so far.
        entity_manager: Live entity table.
        game_event_manager: Game event schema and handler registry.
        combat_log: Combat log processor for S1 and S2 entries.
    """

    def __init__(self, source: str | Path | bytes) -> None:
        self._source = source
        self.tick: int = 0
        self.net_tick: int = 0
        self.game_build: int = 0
        self.string_tables = StringTables()
        self.entity_manager: EntityManager | None = None
        self.game_event_manager = GameEventManager()
        self.combat_log = CombatLogProcessor()
        self._entity_callbacks: list[EntityCallback] = []
        self._chat_callbacks: list[ChatCallback] = []
        self._chat_event_callbacks: list[ChatEventCallback] = []
        self._stop_at_tick: int | None = None
        self._pending_server_info: CSVCMsg_ServerInfo | None = None
        self.match_id: int = 0
        self.game_mode: int = 0
        self.leagueid: int = 0

    # ------------------------------------------------------------------
    # Public callback registration
    # ------------------------------------------------------------------

    def on_entity(self, callback: EntityCallback) -> None:
        """Register a handler called for every entity create/update/delete.

        Args:
            callback: ``(Entity, EntityOp) -> None``.
        """
        self._entity_callbacks.append(callback)
        if self.entity_manager is not None:
            self.entity_manager.on_entity(callback)

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
        except Exception:
            # Truncated files raise on final corrupt snappy block — that's OK
            pass

        # Read match metadata from CDOTAGamerulesProxy entity if DEM_FileInfo
        # didn't populate them (e.g. truncated replays or early stop).
        # Reference: refs/parser/src/main/java/opendota/Parse.java — uses
        # CDOTAGamerulesProxy.m_pGameRules.m_unMatchID64 / m_iGameMode
        if self.entity_manager is not None and (not self.match_id or not self.game_mode):
            grp = self.entity_manager.find_by_class_name("CDOTAGamerulesProxy")
            if grp is not None:
                if not self.match_id:
                    v, ok = grp.get_uint32("m_pGameRules.m_unMatchID64")
                    if ok and v:
                        self.match_id = v
                if not self.game_mode:
                    v, ok = grp.get_int32("m_pGameRules.m_iGameMode")
                    if ok and v:
                        self.game_mode = v
                if not self.leagueid:
                    v, ok = grp.get_uint32("m_pGameRules.m_unLeagueID")
                    if ok and v:
                        self.leagueid = v

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

    def _dispatch_inner(self, type_id: int, payload: bytes) -> None:
        if type_id == _NET_TICK:
            # net_Tick is tiny — just skip (tick already set from outer)
            pass

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
            self.entity_manager.on_packet_entities(pe_msg)

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
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                self.combat_log.process_s2_entry(entry_msg, name_table, tick=self.tick)

        elif type_id == _DOTA_UM_CHAT_EVENT:
            chat_event = CDOTAUserMsg_ChatEvent()
            chat_event.ParseFromString(payload)
            if chat_event.type == _CHAT_MSG_RUNE_PICKUP:
                self.combat_log.process_rune_pickup(
                    chat_event.playerid_1, chat_event.value, tick=self.tick
                )
            for cb in self._chat_event_callbacks:
                cb(chat_event, self.tick)

        elif type_id == _DOTA_UM_CHAT_MESSAGE:
            self._emit_chat_message(payload)

    # ------------------------------------------------------------------
    # Subsystem handlers
    # ------------------------------------------------------------------

    def _on_send_tables(self, data: bytes) -> None:
        serializers = parse_send_tables(data, self.game_build)
        self.entity_manager = EntityManager(serializers, self.string_tables)
        for cb in self._entity_callbacks:
            self.entity_manager.on_entity(cb)
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
        schema = self.game_event_manager._schemas_by_id.get(msg.eventid)
        if schema is not None and schema.name == "dota_combatlog":
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                from gem.game_events import GameEvent

                event = GameEvent(schema=schema, msg=msg)
                self.combat_log.process_s1_event(event, name_table, tick=self.tick)

    def _on_user_message(self, msg: CSVCMsg_UserMessage) -> None:
        if msg.msg_type in (_DOTA_UM_COMBAT_LOG_DATA, _DOTA_UM_COMBAT_LOG_BULK_DATA):
            bulk_msg = CDOTAUserMsg_CombatLogBulkData()
            bulk_msg.ParseFromString(msg.msg_data)
            name_table = self.string_tables.get_by_name(_COMBAT_LOG_NAMES_TABLE)
            if name_table is not None:
                self.combat_log.process_s2_bulk(bulk_msg, name_table, tick=self.tick)

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
