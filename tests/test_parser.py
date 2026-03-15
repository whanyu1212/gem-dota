"""Tests for gem.parser — ReplayParser unit tests.

Covers:
- _read_inner_messages (pure function)
- ReplayParser initial state
- Callback registration (on_entity, on_combat_log_entry, on_game_event, etc.)
- stop_after_tick
- _dispatch_outer: DEM_FILE_INFO, game-winner resolution
- _dispatch_inner: routing, priority sorting, server-info caching,
  game-end callbacks, chat message emission, rune pickup routing
- _on_server_info: pending cache pattern
- _on_game_event_list + _on_game_event via registered schema
- _emit_chat_message

Integration path (requires DemoStream + real proto data) is limited to
the pieces that can be tested with synthetic/minimal protobufs.

Reference: manta/parser.go, manta/demo_packet.go
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from gem.parser import (
    _DEM_FILE_INFO,
    _DOTA_UM_CHAT_EVENT,
    _DOTA_UM_CHAT_MESSAGE,
    _DOTA_UM_COMBAT_LOG_HLTV,
    _NET_TICK,
    _SVC_CREATE_STRING_TABLE,
    _SVC_PACKET_ENTITIES,
    _SVC_UPDATE_STRING_TABLE,
    _SVC_USER_MESSAGE,
    ReplayParser,
    _read_inner_messages,
)

# ---------------------------------------------------------------------------
# Helpers — build synthetic inner message blobs
# ---------------------------------------------------------------------------


class _BitWriter:
    """Write values into a LSB-first bit stream, matching BitReader's encoding."""

    def __init__(self) -> None:
        self._bits: list[int] = []

    def write_bits(self, value: int, n: int) -> None:
        for i in range(n):
            self._bits.append((value >> i) & 1)

    def write_ubit_var(self, value: int) -> None:
        """Encode matching BitReader.read_ubit_var (6-bit group, 2-bit selector)."""
        if value < 16:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(0, 2)  # selector 00
        elif value < 256:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(1, 2)  # selector 01
            self.write_bits((value >> 4) & 0x0F, 4)
        elif value < 4096:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(2, 2)  # selector 10
            self.write_bits((value >> 4) & 0xFF, 8)
        else:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(3, 2)  # selector 11
            self.write_bits((value >> 4) & 0x0FFFFFFF, 28)

    def write_varuint32(self, value: int) -> None:
        while True:
            b = value & 0x7F
            value >>= 7
            if value:
                self.write_bits(b | 0x80, 8)
            else:
                self.write_bits(b, 8)
                break

    def write_bytes(self, data: bytes) -> None:
        for b in data:
            self.write_bits(b, 8)

    def to_bytes(self) -> bytes:
        bits = self._bits + [0] * (-len(self._bits) % 8)
        out = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte |= bits[i + j] << j
            out.append(byte)
        return bytes(out)


def _make_inner_blob(messages: list[tuple[int, bytes]]) -> bytes:
    """Build a CDemoPacket.data bit-stream from (type_id, payload) pairs."""
    bw = _BitWriter()
    for type_id, payload in messages:
        bw.write_ubit_var(type_id)
        bw.write_varuint32(len(payload))
        bw.write_bytes(payload)
    return bw.to_bytes()


# ---------------------------------------------------------------------------
# _read_inner_messages
# ---------------------------------------------------------------------------


class TestReadInnerMessages:
    def test_empty_data_returns_empty_list(self):
        assert _read_inner_messages(b"") == []

    def test_single_message(self):
        payload = b"\x01\x02\x03"
        blob = _make_inner_blob([(4, payload)])
        result = _read_inner_messages(blob)
        assert len(result) == 1
        assert result[0] == (4, payload)

    def test_multiple_messages_in_order(self):
        msgs = [(4, b"tick"), (44, b"create"), (55, b"entities")]
        blob = _make_inner_blob(msgs)
        result = _read_inner_messages(blob)
        assert len(result) == 3
        assert result[0][0] == 4
        assert result[1][0] == 44
        assert result[2][0] == 55

    def test_payload_content_preserved(self):
        payload = bytes(range(20))
        blob = _make_inner_blob([(99, payload)])
        result = _read_inner_messages(blob)
        assert result[0][1] == payload

    def test_empty_payload(self):
        blob = _make_inner_blob([(4, b"")])
        result = _read_inner_messages(blob)
        assert len(result) == 1
        assert result[0] == (4, b"")


# ---------------------------------------------------------------------------
# ReplayParser init state
# ---------------------------------------------------------------------------


class TestReplayParserInit:
    def test_tick_starts_at_zero(self):
        p = ReplayParser(b"")
        assert p.tick == 0

    def test_net_tick_starts_at_zero(self):
        p = ReplayParser(b"")
        assert p.net_tick == 0

    def test_game_build_starts_at_zero(self):
        p = ReplayParser(b"")
        assert p.game_build == 0

    def test_match_id_starts_at_zero(self):
        p = ReplayParser(b"")
        assert p.match_id == 0

    def test_game_mode_starts_at_zero(self):
        p = ReplayParser(b"")
        assert p.game_mode == 0

    def test_leagueid_starts_at_zero(self):
        p = ReplayParser(b"")
        assert p.leagueid == 0

    def test_radiant_win_starts_none(self):
        p = ReplayParser(b"")
        assert p.radiant_win is None

    def test_game_start_tick_starts_none(self):
        p = ReplayParser(b"")
        assert p.game_start_tick is None

    def test_entity_manager_starts_none(self):
        p = ReplayParser(b"")
        assert p.entity_manager is None

    def test_string_tables_empty(self):
        from gem.string_table import StringTables

        p = ReplayParser(b"")
        assert isinstance(p.string_tables, StringTables)

    def test_stop_at_tick_none(self):
        p = ReplayParser(b"")
        assert p._stop_at_tick is None

    def test_grp_game_start_not_seen(self):
        p = ReplayParser(b"")
        assert p._grp_game_start_seen is False

    def test_game_ended_false(self):
        p = ReplayParser(b"")
        assert p._game_ended is False


# ---------------------------------------------------------------------------
# Callback registration
# ---------------------------------------------------------------------------


class TestCallbackRegistration:
    def test_on_entity_appends_callback(self):
        p = ReplayParser(b"")

        def cb(e, op):
            return None

        p.on_entity(cb)
        assert cb in p._entity_callbacks

    def test_on_entity_also_registers_with_entity_manager_when_present(self):
        p = ReplayParser(b"")
        em = MagicMock()
        p.entity_manager = em

        def cb(e, op):
            return None

        p.on_entity(cb)
        em.on_entity.assert_called_once_with(cb)

    def test_on_entity_multiple_callbacks(self):
        p = ReplayParser(b"")

        def cb1(e, op):
            return None

        def cb2(e, op):
            return None

        p.on_entity(cb1)
        p.on_entity(cb2)
        assert len(p._entity_callbacks) == 2

    def test_on_chat_message_appends_callback(self):
        p = ReplayParser(b"")

        def cb(entry):
            return None

        p.on_chat_message(cb)
        assert cb in p._chat_callbacks

    def test_on_chat_event_appends_callback(self):
        p = ReplayParser(b"")

        def cb(evt, tick):
            return None

        p.on_chat_event(cb)
        assert cb in p._chat_event_callbacks

    def test_on_game_start_appends_callback(self):
        p = ReplayParser(b"")

        def cb(tick):
            return None

        p.on_game_start(cb)
        assert cb in p._game_start_callbacks

    def test_on_game_end_appends_callback(self):
        p = ReplayParser(b"")

        def cb(tick):
            return None

        p.on_game_end(cb)
        assert cb in p._game_end_callbacks

    def test_stop_after_tick_sets_internal_state(self):
        p = ReplayParser(b"")
        p.stop_after_tick(9000)
        assert p._stop_at_tick == 9000

    def test_on_game_event_delegates_to_game_event_manager(self):
        p = ReplayParser(b"")

        def cb(event):
            return None

        with patch.object(p.game_event_manager, "on_game_event") as mock_reg:
            p.on_game_event("dota_combatlog", cb)
            mock_reg.assert_called_once_with("dota_combatlog", cb)

    def test_on_combat_log_entry_delegates_to_combat_log(self):
        p = ReplayParser(b"")

        def cb(entry):
            return None

        with patch.object(p.combat_log, "on_combat_log_entry") as mock_reg:
            p.on_combat_log_entry(cb)
            mock_reg.assert_called_once_with(cb)


# ---------------------------------------------------------------------------
# _dispatch_outer — DEM_FILE_INFO
# ---------------------------------------------------------------------------


class TestDispatchOuterFileInfo:
    """Test the DEM_FILE_INFO branch by mocking CDemoFileInfo parsing.

    The dota_gcmessages_common_match_management_pb2 module depends on
    steammessages.proto which is not always loadable in test environments.
    We mock CDemoFileInfo.ParseFromString and its attributes directly.
    """

    def _make_mock_file_info(self, match_id=0, game_mode=0, leagueid=0, game_winner=0):
        mock_dota = MagicMock()
        mock_dota.match_id = match_id
        mock_dota.game_mode = game_mode
        mock_dota.leagueid = leagueid
        mock_dota.game_winner = game_winner
        mock_game_info = MagicMock()
        mock_game_info.dota = mock_dota
        mock_fi = MagicMock()
        mock_fi.game_info = mock_game_info
        return mock_fi

    def _dispatch_with_mock(self, p, match_id=0, game_mode=0, leagueid=0, game_winner=0):
        mock_fi = self._make_mock_file_info(match_id, game_mode, leagueid, game_winner)
        with patch("gem.parser.CDemoFileInfo") as MockFI:
            MockFI.return_value = mock_fi
            p._dispatch_outer(_DEM_FILE_INFO, b"")

    def test_file_info_sets_match_id(self):
        p = ReplayParser(b"")
        self._dispatch_with_mock(p, match_id=12345)
        assert p.match_id == 12345

    def test_file_info_sets_game_mode(self):
        p = ReplayParser(b"")
        self._dispatch_with_mock(p, game_mode=22)
        assert p.game_mode == 22

    def test_file_info_sets_leagueid(self):
        p = ReplayParser(b"")
        self._dispatch_with_mock(p, leagueid=15000)
        assert p.leagueid == 15000

    def test_file_info_radiant_win_winner_2(self):
        p = ReplayParser(b"")
        self._dispatch_with_mock(p, game_winner=2)
        assert p.radiant_win is True

    def test_file_info_radiant_win_winner_3(self):
        p = ReplayParser(b"")
        self._dispatch_with_mock(p, game_winner=3)
        assert p.radiant_win is False

    def test_file_info_radiant_win_winner_0_stays_none(self):
        p = ReplayParser(b"")
        self._dispatch_with_mock(p, game_winner=0)
        assert p.radiant_win is None


# ---------------------------------------------------------------------------
# _on_server_info — pending cache pattern
# ---------------------------------------------------------------------------


class TestOnServerInfo:
    def test_server_info_before_entity_manager_is_cached(self):
        p = ReplayParser(b"")
        assert p.entity_manager is None
        msg = MagicMock()
        p._on_server_info(msg)
        assert p._pending_server_info is msg

    def test_server_info_after_entity_manager_delegates_directly(self):
        p = ReplayParser(b"")
        em = MagicMock()
        em.game_build = 1234
        p.entity_manager = em
        msg = MagicMock()
        p._on_server_info(msg)
        em.on_server_info.assert_called_once_with(msg)
        assert p.game_build == 1234

    def test_pending_server_info_applied_when_send_tables_processed(self):
        """If server_info arrived before send_tables, applying send_tables
        must consume _pending_server_info and pass it to the entity manager."""
        p = ReplayParser(b"")
        msg = MagicMock()
        p._pending_server_info = msg

        em = MagicMock()
        em.game_build = 999

        # Patch EntityManager creation and _on_server_info
        with (
            patch("gem.parser.parse_send_tables", return_value={}),
            patch("gem.parser.EntityManager", return_value=em),
        ):
            p._on_send_tables(b"\x00" * 4)  # minimal payload (will be passed to parse_send_tables)

        em.on_server_info.assert_called_once_with(msg)
        assert p._pending_server_info is None


# ---------------------------------------------------------------------------
# _dispatch_inner — routing
# ---------------------------------------------------------------------------


class TestDispatchInnerRouting:
    def test_net_tick_is_a_noop(self):
        """_NET_TICK must not raise and must not change any state."""
        p = ReplayParser(b"")
        # Just prove it doesn't raise
        p._dispatch_inner(_NET_TICK, b"")

    def test_svc_packet_entities_skipped_when_no_entity_manager(self):
        p = ReplayParser(b"")
        assert p.entity_manager is None
        # Should not raise
        p._dispatch_inner(_SVC_PACKET_ENTITIES, b"\x00" * 4)

    def test_svc_packet_entities_skipped_when_class_id_size_zero(self):
        p = ReplayParser(b"")
        em = MagicMock()
        em.class_id_size = 0
        p.entity_manager = em
        p._dispatch_inner(_SVC_PACKET_ENTITIES, b"\x00" * 4)
        em.on_packet_entities.assert_not_called()

    def test_svc_user_message_dispatches_to_on_user_message(self):
        p = ReplayParser(b"")
        from gem.proto.dota2.netmessages_pb2 import CSVCMsg_UserMessage

        um = CSVCMsg_UserMessage()
        um.msg_type = 9999  # unknown type, but should not raise
        payload = um.SerializeToString()
        # Should not raise, and will silently ignore unknown msg_type
        p._dispatch_inner(_SVC_USER_MESSAGE, payload)

    def test_dota_um_combat_log_hltv_with_no_name_table_silently_skips(self):
        """If CombatLogNames table doesn't exist, S2 entry must be silently ignored."""
        p = ReplayParser(b"")
        from gem.proto.dota2.dota_shared_enums_pb2 import CMsgDOTACombatLogEntry

        entry = CMsgDOTACombatLogEntry()
        entry.type = 0
        payload = entry.SerializeToString()
        # No CombatLogNames table → should not raise
        p._dispatch_inner(_DOTA_UM_COMBAT_LOG_HLTV, payload)

    def test_dota_um_chat_message_skipped_when_no_callbacks(self):
        """When no chat callbacks are registered, parsing should be skipped."""
        p = ReplayParser(b"")
        from gem.proto.dota2.dota_usermessages_pb2 import CDOTAUserMsg_ChatMessage

        msg = CDOTAUserMsg_ChatMessage()
        msg.channel_type = 11
        msg.source_player_id = 0
        msg.message_text = "hello"
        payload = msg.SerializeToString()
        # Should not raise
        p._dispatch_inner(_DOTA_UM_CHAT_MESSAGE, payload)


# ---------------------------------------------------------------------------
# _dispatch_inner — game-end callback
# ---------------------------------------------------------------------------


class TestGameEndCallback:
    def _make_combat_log_hltv_payload(self, type_id: int, value: int) -> bytes:
        from gem.proto.dota2.dota_shared_enums_pb2 import CMsgDOTACombatLogEntry

        entry = CMsgDOTACombatLogEntry()
        entry.type = type_id
        entry.value = value
        return entry.SerializeToString()

    def test_game_end_callback_fires_on_type9_value6(self):
        p = ReplayParser(b"")
        called = []
        p.on_game_end(lambda tick: called.append(tick))
        p.tick = 50000

        # Add a CombatLogNames table so the entry is processed
        from gem.string_table import StringTable

        st = StringTable(index=0, name="CombatLogNames")
        p.string_tables.add(st)

        payload = self._make_combat_log_hltv_payload(type_id=9, value=6)
        p._dispatch_inner(_DOTA_UM_COMBAT_LOG_HLTV, payload)
        assert called == [50000]

    def test_game_end_callback_fires_only_once(self):
        """The game-end callback must fire at most once even if type9/value6 is seen twice."""
        p = ReplayParser(b"")
        called = []
        p.on_game_end(lambda tick: called.append(tick))

        from gem.string_table import StringTable

        st = StringTable(index=0, name="CombatLogNames")
        p.string_tables.add(st)

        payload = self._make_combat_log_hltv_payload(type_id=9, value=6)
        p._dispatch_inner(_DOTA_UM_COMBAT_LOG_HLTV, payload)
        p._dispatch_inner(_DOTA_UM_COMBAT_LOG_HLTV, payload)
        assert len(called) == 1

    def test_game_end_callback_does_not_fire_for_other_types(self):
        p = ReplayParser(b"")
        called = []
        p.on_game_end(lambda tick: called.append(tick))

        from gem.string_table import StringTable

        st = StringTable(index=0, name="CombatLogNames")
        p.string_tables.add(st)

        # type=0, value=0 — not a game-end signal
        payload = self._make_combat_log_hltv_payload(type_id=0, value=0)
        p._dispatch_inner(_DOTA_UM_COMBAT_LOG_HLTV, payload)
        assert called == []


# ---------------------------------------------------------------------------
# _dispatch_inner — chat message emission
# ---------------------------------------------------------------------------


class TestEmitChatMessage:
    def test_chat_callback_receives_entry(self):
        from gem.models import ChatEntry
        from gem.proto.dota2.dota_usermessages_pb2 import CDOTAUserMsg_ChatMessage

        p = ReplayParser(b"")
        received = []
        p.on_chat_message(received.append)
        p.tick = 1000

        msg = CDOTAUserMsg_ChatMessage()
        msg.channel_type = 11  # all-chat
        msg.source_player_id = 3
        msg.message_text = "wp"
        p._dispatch_inner(_DOTA_UM_CHAT_MESSAGE, msg.SerializeToString())

        assert len(received) == 1
        entry = received[0]
        assert isinstance(entry, ChatEntry)
        assert entry.tick == 1000
        assert entry.player_slot == 3
        assert entry.channel == "all"
        assert entry.text == "wp"

    def test_team_chat_channel_label(self):
        from gem.proto.dota2.dota_usermessages_pb2 import CDOTAUserMsg_ChatMessage

        p = ReplayParser(b"")
        received = []
        p.on_chat_message(received.append)

        msg = CDOTAUserMsg_ChatMessage()
        msg.channel_type = 5  # non-all → team
        msg.source_player_id = 1
        msg.message_text = "push"
        p._dispatch_inner(_DOTA_UM_CHAT_MESSAGE, msg.SerializeToString())

        assert received[0].channel == "team"

    def test_multiple_chat_callbacks_all_receive_entry(self):
        from gem.proto.dota2.dota_usermessages_pb2 import CDOTAUserMsg_ChatMessage

        p = ReplayParser(b"")
        recv1, recv2 = [], []
        p.on_chat_message(recv1.append)
        p.on_chat_message(recv2.append)

        msg = CDOTAUserMsg_ChatMessage()
        msg.channel_type = 11
        msg.source_player_id = 0
        msg.message_text = "test"
        p._dispatch_inner(_DOTA_UM_CHAT_MESSAGE, msg.SerializeToString())

        assert len(recv1) == 1
        assert len(recv2) == 1


# ---------------------------------------------------------------------------
# _dispatch_inner — chat event (rune pickup)
# ---------------------------------------------------------------------------


class TestChatEventRune:
    def test_rune_pickup_routes_to_combat_log_processor(self):
        from gem.proto.dota2.dota_usermessages_pb2 import CDOTAUserMsg_ChatEvent

        p = ReplayParser(b"")
        p.tick = 2000

        msg = CDOTAUserMsg_ChatEvent()
        msg.type = 22  # CHAT_MESSAGE_RUNE_PICKUP
        msg.playerid_1 = 5
        msg.value = 3  # rune type

        with patch.object(p.combat_log, "process_rune_pickup") as mock_rune:
            p._dispatch_inner(_DOTA_UM_CHAT_EVENT, msg.SerializeToString())
            mock_rune.assert_called_once_with(5, 3, tick=2000)

    def test_non_rune_chat_event_does_not_call_process_rune_pickup(self):
        from gem.proto.dota2.dota_usermessages_pb2 import CDOTAUserMsg_ChatEvent

        p = ReplayParser(b"")
        msg = CDOTAUserMsg_ChatEvent()
        msg.type = 9  # AEGIS pickup, not rune

        with patch.object(p.combat_log, "process_rune_pickup") as mock_rune:
            p._dispatch_inner(_DOTA_UM_CHAT_EVENT, msg.SerializeToString())
            mock_rune.assert_not_called()

    def test_chat_event_callbacks_receive_event_and_tick(self):
        from gem.proto.dota2.dota_usermessages_pb2 import CDOTAUserMsg_ChatEvent

        p = ReplayParser(b"")
        p.tick = 3000
        received = []
        p.on_chat_event(lambda evt, tick: received.append((evt.type, tick)))

        msg = CDOTAUserMsg_ChatEvent()
        msg.type = 9
        p._dispatch_inner(_DOTA_UM_CHAT_EVENT, msg.SerializeToString())

        assert received == [(9, 3000)]


# ---------------------------------------------------------------------------
# _dispatch_inner — priority sorting in _dispatch_inner_packet
# ---------------------------------------------------------------------------


class TestInnerPacketPriority:
    def test_string_table_create_processed_before_packet_entities(self):
        """svc_CreateStringTable (priority -10) must be processed before
        svc_PacketEntities (priority +5) regardless of order in the blob.

        We patch _dispatch_inner to capture call order without actually
        parsing any proto payload.
        """
        p = ReplayParser(b"")
        call_order = []

        # Build blob with PacketEntities first, then CreateStringTable
        blob = _make_inner_blob(
            [
                (_SVC_PACKET_ENTITIES, b""),
                (_SVC_CREATE_STRING_TABLE, b""),
            ]
        )

        with patch.object(p, "_dispatch_inner", side_effect=lambda t, pl: call_order.append(t)):
            p._dispatch_inner_packet(blob)

        # CreateStringTable (-10) should come before PacketEntities (+5)
        create_idx = call_order.index(_SVC_CREATE_STRING_TABLE)
        entities_idx = call_order.index(_SVC_PACKET_ENTITIES)
        assert create_idx < entities_idx

    def test_update_string_table_before_packet_entities(self):
        p = ReplayParser(b"")
        call_order = []

        blob = _make_inner_blob(
            [
                (_SVC_PACKET_ENTITIES, b""),
                (_SVC_UPDATE_STRING_TABLE, b""),
            ]
        )

        with patch.object(p, "_dispatch_inner", side_effect=lambda t, pl: call_order.append(t)):
            p._dispatch_inner_packet(blob)

        upd_idx = call_order.index(_SVC_UPDATE_STRING_TABLE)
        ent_idx = call_order.index(_SVC_PACKET_ENTITIES)
        assert upd_idx < ent_idx

    def test_net_tick_processed_before_packet_entities(self):
        """net_Tick (priority -10) must come before PacketEntities (+5)."""
        p = ReplayParser(b"")
        call_order = []

        blob = _make_inner_blob(
            [
                (_SVC_PACKET_ENTITIES, b""),
                (_NET_TICK, b""),
            ]
        )

        with patch.object(p, "_dispatch_inner", side_effect=lambda t, pl: call_order.append(t)):
            p._dispatch_inner_packet(blob)

        tick_idx = call_order.index(_NET_TICK)
        ent_idx = call_order.index(_SVC_PACKET_ENTITIES)
        assert tick_idx < ent_idx

    def test_empty_data_does_not_raise(self):
        p = ReplayParser(b"")
        p._dispatch_inner_packet(b"")  # should not raise


# ---------------------------------------------------------------------------
# _on_game_event_list + _on_game_event schema registration
# ---------------------------------------------------------------------------


class TestGameEventListAndEvent:
    def test_game_event_list_registers_schemas(self):
        from gem.proto.dota2.gameevents_pb2 import (
            CMsgSource1LegacyGameEventList,
        )

        p = ReplayParser(b"")
        gel = CMsgSource1LegacyGameEventList()
        desc = gel.descriptors.add()
        desc.eventid = 42
        desc.name = "test_event"
        k = desc.keys.add()
        k.name = "val"
        k.type = 3

        p._on_game_event_list(gel)
        assert p.game_event_manager.has_event("test_event")

    def test_game_event_dispatches_to_game_event_manager(self):
        from gem.proto.dota2.gameevents_pb2 import (
            CMsgSource1LegacyGameEvent,
            CMsgSource1LegacyGameEventList,
        )

        p = ReplayParser(b"")
        # Register a schema first
        gel = CMsgSource1LegacyGameEventList()
        desc = gel.descriptors.add()
        desc.eventid = 99
        desc.name = "my_event"
        p._on_game_event_list(gel)

        received = []
        p.on_game_event("my_event", received.append)

        ge = CMsgSource1LegacyGameEvent()
        ge.eventid = 99
        p._on_game_event(ge)

        assert len(received) == 1


# ---------------------------------------------------------------------------
# _on_class_info routing
# ---------------------------------------------------------------------------


class TestOnClassInfo:
    def test_on_class_info_calls_entity_manager_when_present(self):
        p = ReplayParser(b"")
        em = MagicMock()
        p.entity_manager = em

        from gem.proto.dota2.demo_pb2 import CDemoClassInfo

        ci = CDemoClassInfo()

        p._on_class_info(ci)
        em.on_class_info.assert_called_once_with(ci)
        em.on_baseline_updated.assert_called_once()

    def test_on_class_info_noop_when_no_entity_manager(self):
        p = ReplayParser(b"")
        assert p.entity_manager is None
        from gem.proto.dota2.demo_pb2 import CDemoClassInfo

        ci = CDemoClassInfo()
        # Should not raise
        p._on_class_info(ci)


# ---------------------------------------------------------------------------
# stop_after_tick is honoured during parse()
# ---------------------------------------------------------------------------


class TestStopAfterTick:
    def test_stop_after_tick_attribute(self):
        p = ReplayParser(b"")
        p.stop_after_tick(1234)
        assert p._stop_at_tick == 1234

    def test_parse_breaks_when_tick_exceeds_stop_tick(self):
        """When the outer loop tick > _stop_at_tick, parse() should stop early."""
        p = ReplayParser(b"")
        p.stop_after_tick(100)

        # Capture how many outer dispatches happen
        dispatch_calls = []
        p._dispatch_outer = lambda t, d: dispatch_calls.append(t)

        ticks_and_types = [(50, 7, b""), (150, 7, b"")]

        with patch("gem.parser.DemoStream") as MockStream:
            MockStream.return_value.__enter__.return_value = iter(ticks_and_types)
            p.parse()

        # Only tick=50 should have been dispatched; tick=150 > 100 → break
        assert len(dispatch_calls) == 1
