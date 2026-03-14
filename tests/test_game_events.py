"""Tests for gem.game_events — event schema registration and typed dispatch.

Reference: manta/game_event.go
"""

from gem.game_events import GameEvent, GameEventManager, GameEventSchema

# ---------------------------------------------------------------------------
# Shared fake key / message helpers
# ---------------------------------------------------------------------------


class FakeKey:
    """Minimal stand-in for CMsgSource1LegacyGameEvent.key_t.

    Uses proto-style attribute names (val_string, val_long, etc.) to match
    the real CMsgSource1LegacyGameEvent.key_t protobuf message.
    """

    def __init__(self, type_id: int, value):
        self.type = type_id
        self.val_string = value if type_id == 1 else ""
        self.val_float = value if type_id == 2 else 0.0
        self.val_long = value if type_id == 3 else 0
        self.val_short = value if type_id == 4 else 0
        self.val_byte = value if type_id == 5 else 0
        self.val_bool = value if type_id == 6 else False
        self.val_uint64 = value if type_id == 7 else 0


class FakeRawEvent:
    """Minimal stand-in for CMsgSource1LegacyGameEvent.

    Uses proto-style attribute names (eventid, keys) to match the real
    CMsgSource1LegacyGameEvent protobuf message.
    """

    def __init__(self, event_id: int, keys: list):
        self.eventid = event_id
        self.keys = keys


def make_event(fields: dict, keys_data: list) -> GameEvent:
    """Build a GameEvent with the given schema fields and key values."""
    schema = GameEventSchema(event_id=99, name="test_event", fields=fields)
    msg = FakeRawEvent(99, [FakeKey(t, v) for t, v in keys_data])
    return GameEvent(schema=schema, msg=msg)


# ---------------------------------------------------------------------------
# GameEventManager — schema registration
# ---------------------------------------------------------------------------


class TestGameEventManagerSchema:
    def test_register_single_schema(self):
        mgr = GameEventManager()
        mgr.register_schema(
            {"eventid": 1, "name": "dota_combatlog", "keys": [{"name": "type", "type": 5}]}
        )
        assert mgr.has_event("dota_combatlog")

    def test_register_multiple_schemas(self):
        mgr = GameEventManager()
        for i, name in enumerate(["event_a", "event_b", "event_c"], start=1):
            mgr.register_schema({"eventid": i, "name": name, "keys": []})
        assert mgr.has_event("event_a")
        assert mgr.has_event("event_b")
        assert mgr.has_event("event_c")

    def test_unknown_event_not_registered(self):
        assert not GameEventManager().has_event("nonexistent")

    def test_schema_stored_by_id_and_name(self):
        mgr = GameEventManager()
        mgr.register_schema({"eventid": 42, "name": "my_event", "keys": []})
        assert 42 in mgr._schemas_by_id
        assert "my_event" in mgr._schemas_by_name

    def test_schema_field_indices(self):
        mgr = GameEventManager()
        mgr.register_schema(
            {
                "eventid": 1,
                "name": "ev",
                "keys": [
                    {"name": "alpha", "type": 3},
                    {"name": "beta", "type": 1},
                ],
            }
        )
        schema = mgr._schemas_by_name["ev"]
        assert schema.fields["alpha"] == (0, 3)
        assert schema.fields["beta"] == (1, 1)

    def test_register_schema_with_no_keys(self):
        mgr = GameEventManager()
        mgr.register_schema({"eventid": 5, "name": "empty_event", "keys": []})
        assert mgr.has_event("empty_event")
        schema = mgr._schemas_by_name["empty_event"]
        assert schema.fields == {}


# ---------------------------------------------------------------------------
# GameEventManager — handler dispatch
# ---------------------------------------------------------------------------


class TestGameEventManagerDispatch:
    def test_handler_called_on_matching_event(self):
        mgr = GameEventManager()
        mgr.register_schema({"eventid": 2, "name": "player_death", "keys": []})
        received = []
        mgr.on_game_event("player_death", lambda e: received.append(e))
        mgr.dispatch(FakeRawEvent(2, []))
        assert len(received) == 1

    def test_multiple_handlers_all_called(self):
        mgr = GameEventManager()
        mgr.register_schema({"eventid": 3, "name": "multi", "keys": []})
        calls = []
        mgr.on_game_event("multi", lambda e: calls.append("h1"))
        mgr.on_game_event("multi", lambda e: calls.append("h2"))
        mgr.on_game_event("multi", lambda e: calls.append("h3"))
        mgr.dispatch(FakeRawEvent(3, []))
        assert calls == ["h1", "h2", "h3"]

    def test_unknown_event_id_no_crash(self):
        mgr = GameEventManager()
        mgr.dispatch(FakeRawEvent(999, []))  # not registered — should be a no-op

    def test_no_handlers_registered_no_crash(self):
        mgr = GameEventManager()
        mgr.register_schema({"eventid": 4, "name": "unsubscribed", "keys": []})
        mgr.dispatch(FakeRawEvent(4, []))  # schema exists, no handler — no-op

    def test_handler_receives_game_event_object(self):
        mgr = GameEventManager()
        mgr.register_schema(
            {"eventid": 5, "name": "typed_event", "keys": [{"name": "damage", "type": 3}]}
        )
        received = []
        mgr.on_game_event("typed_event", lambda e: received.append(e))
        mgr.dispatch(FakeRawEvent(5, [FakeKey(3, 42)]))
        assert isinstance(received[0], GameEvent)

    def test_handler_not_called_for_different_event(self):
        mgr = GameEventManager()
        mgr.register_schema({"eventid": 10, "name": "event_x", "keys": []})
        mgr.register_schema({"eventid": 11, "name": "event_y", "keys": []})
        calls = []
        mgr.on_game_event("event_x", lambda e: calls.append("x"))
        mgr.dispatch(FakeRawEvent(11, []))
        assert calls == []


# ---------------------------------------------------------------------------
# GameEvent — typed field accessors
# ---------------------------------------------------------------------------


class TestGameEventGetString:
    def test_get_string_ok(self):
        e = make_event({"name": (0, 1)}, [(1, "hero_axe")])
        val, err = e.get_string("name")
        assert err is None
        assert val == "hero_axe"

    def test_get_string_empty_string(self):
        e = make_event({"name": (0, 1)}, [(1, "")])
        val, err = e.get_string("name")
        assert err is None
        assert val == ""

    def test_get_string_type_mismatch(self):
        e = make_event({"name": (0, 3)}, [(3, 99)])  # long, not string
        val, err = e.get_string("name")
        assert err is not None
        assert val == ""

    def test_get_string_missing_field(self):
        e = make_event({}, [])
        val, err = e.get_string("missing")
        assert err is not None
        assert val == ""


class TestGameEventGetFloat:
    def test_get_float_ok(self):
        e = make_event({"speed": (0, 2)}, [(2, 3.14)])
        val, err = e.get_float("speed")
        assert err is None
        assert abs(val - 3.14) < 0.001

    def test_get_float_type_mismatch(self):
        e = make_event({"speed": (0, 3)}, [(3, 5)])
        val, err = e.get_float("speed")
        assert err is not None
        assert val == 0.0


class TestGameEventGetInt32:
    def test_get_int32_from_long(self):
        e = make_event({"damage": (0, 3)}, [(3, 500)])
        val, err = e.get_int32("damage")
        assert err is None
        assert val == 500

    def test_get_int32_from_short(self):
        e = make_event({"level": (0, 4)}, [(4, 25)])
        val, err = e.get_int32("level")
        assert err is None
        assert val == 25

    def test_get_int32_from_byte(self):
        e = make_event({"type": (0, 5)}, [(5, 7)])
        val, err = e.get_int32("type")
        assert err is None
        assert val == 7

    def test_get_int32_type_mismatch(self):
        e = make_event({"val": (0, 1)}, [(1, "text")])  # string, not int
        val, err = e.get_int32("val")
        assert err is not None
        assert val == 0

    def test_get_int32_missing_field(self):
        e = make_event({}, [])
        val, err = e.get_int32("nope")
        assert err is not None


class TestGameEventGetBool:
    def test_get_bool_true(self):
        e = make_event({"flag": (0, 6)}, [(6, True)])
        val, err = e.get_bool("flag")
        assert err is None
        assert val is True

    def test_get_bool_false(self):
        e = make_event({"flag": (0, 6)}, [(6, False)])
        val, err = e.get_bool("flag")
        assert err is None
        assert val is False

    def test_get_bool_type_mismatch(self):
        e = make_event({"flag": (0, 3)}, [(3, 1)])
        val, err = e.get_bool("flag")
        assert err is not None
        assert val is False


class TestGameEventGetUint64:
    def test_get_uint64_ok(self):
        big = (1 << 48) + 12345
        e = make_event({"handle": (0, 7)}, [(7, big)])
        val, err = e.get_uint64("handle")
        assert err is None
        assert val == big

    def test_get_uint64_type_mismatch(self):
        e = make_event({"handle": (0, 3)}, [(3, 1)])
        val, err = e.get_uint64("handle")
        assert err is not None
        assert val == 0


class TestGameEventMultipleFields:
    def test_multiple_fields_correct_indices(self):
        fields = {"a": (0, 3), "b": (1, 1), "c": (2, 6)}
        keys = [(3, 42), (1, "hello"), (6, True)]
        e = make_event(fields, keys)

        v, err = e.get_int32("a")
        assert err is None and v == 42

        v2, err2 = e.get_string("b")
        assert err2 is None and v2 == "hello"

        v3, err3 = e.get_bool("c")
        assert err3 is None and v3 is True

    def test_out_of_range_key_index(self):
        fields = {"x": (5, 3)}  # index 5, but only 1 key
        e = make_event(fields, [(3, 1)])
        val, err = e.get_int32("x")
        assert err is not None


# ---------------------------------------------------------------------------
# GameEventManager — register_schema from CMsgSource1LegacyGameEventList shape
# ---------------------------------------------------------------------------


class TestGameEventManagerFromProtoShape:
    """Simulate the shape of data coming from the real proto descriptor."""

    def test_register_from_proto_like_descriptor(self):
        """register_schema accepts the dict shape built from proto descriptors."""
        mgr = GameEventManager()

        # Simulates what parser._on_game_event_list builds
        descriptors = [
            {
                "eventid": 100,
                "name": "dota_hero_killed",
                "keys": [
                    {"name": "kills", "type": 3},
                    {"name": "victim", "type": 1},
                    {"name": "multikill", "type": 6},
                ],
            },
            {
                "eventid": 101,
                "name": "dota_building_kill",
                "keys": [
                    {"name": "teamnumber", "type": 5},
                ],
            },
        ]

        for d in descriptors:
            mgr.register_schema(d)

        assert mgr.has_event("dota_hero_killed")
        assert mgr.has_event("dota_building_kill")
        assert not mgr.has_event("dota_roshan_killed")

        schema = mgr._schemas_by_name["dota_hero_killed"]
        assert schema.fields["kills"] == (0, 3)
        assert schema.fields["victim"] == (1, 1)
        assert schema.fields["multikill"] == (2, 6)
