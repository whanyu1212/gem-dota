"""High-level replay parser for Dota 2 Source 2 .dem files.

Ties together the stream reader, sendtable schema, string tables, and entity
manager into a single ``ReplayParser`` class.  Callers register callbacks for
the events they care about and then call ``parse()`` to drive the loop.

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
  ubit_var   → message type ID  (SVC_Messages / NET_Messages)
  varuint32  → byte length
  bytes      → protobuf payload

Relevant inner IDs:
  net_Tick               =  4
  svc_ServerInfo         = 40
  svc_CreateStringTable  = 44
  svc_UpdateStringTable  = 45
  svc_PacketEntities     = 55

Reference: manta/parser.go, manta/demo_packet.go
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

# Proto side-effect import order is critical
from google.protobuf import descriptor_pb2  # noqa: F401

from gem.entities import Entity, EntityManager, EntityOp
from gem.proto.dota2 import (
    network_connection_pb2,  # noqa: F401
    networkbasetypes_pb2,  # noqa: F401
)
from gem.proto.dota2.demo_pb2 import CDemoClassInfo, CDemoFullPacket, CDemoPacket
from gem.proto.dota2.netmessages_pb2 import (
    CSVCMsg_CreateStringTable,
    CSVCMsg_PacketEntities,
    CSVCMsg_ServerInfo,
    CSVCMsg_UpdateStringTable,
)
from gem.reader import BitReader
from gem.sendtable import parse_send_tables
from gem.stream import DemoStream
from gem.string_table import StringTables, handle_create, handle_update

# ---------------------------------------------------------------------------
# Outer EDemoCommands IDs (stripped of DEM_IsCompressed = 0x40)
# ---------------------------------------------------------------------------
_DEM_SEND_TABLES = 4
_DEM_CLASS_INFO = 5
_DEM_PACKET = 7
_DEM_SIGNON_PACKET = 8
_DEM_FULL_PACKET = 13

# Inner SVC/NET message IDs
_NET_TICK = 4
_SVC_SERVER_INFO = 40
_SVC_CREATE_STRING_TABLE = 44
_SVC_UPDATE_STRING_TABLE = 45
_SVC_PACKET_ENTITIES = 55

EntityCallback = Callable[[Entity, EntityOp], None]


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
        parser.parse()

    Attributes:
        tick: Current game tick.
        net_tick: Current net tick (from net_Tick inner messages).
        game_build: Build number extracted from CSVCMsg_ServerInfo.
        string_tables: All string tables created so far.
        entity_manager: Live entity table.
    """

    def __init__(self, source: str | Path | bytes) -> None:
        self._source = source
        self.tick: int = 0
        self.net_tick: int = 0
        self.game_build: int = 0
        self.string_tables = StringTables()
        self.entity_manager: EntityManager | None = None
        self._entity_callbacks: list[EntityCallback] = []
        self._stop_at_tick: int | None = None
        self._pending_server_info: CSVCMsg_ServerInfo | None = None

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

    # ------------------------------------------------------------------
    # Outer message dispatch
    # ------------------------------------------------------------------

    def _dispatch_outer(self, msg_type: int, data: bytes) -> None:
        if msg_type == _DEM_SEND_TABLES:
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
