"""
Tests for gem.game_events — event schema registration and typed dispatch.

Reference: manta/game_event.go
"""

import pytest


@pytest.fixture
def game_event_manager():
    from gem.game_events import GameEventManager

    return GameEventManager()


class TestGameEventManager:
    def test_register_schema(self, game_event_manager):
        schema = {
            "eventid": 1,
            "name": "dota_combatlog",
            "keys": [
                {"name": "type", "type": 5},  # byte
                {"name": "value", "type": 3},  # long
                {"name": "sourcename", "type": 1},  # string
            ],
        }
        game_event_manager.register_schema(schema)
        assert game_event_manager.has_event("dota_combatlog")

    def test_unknown_event_not_registered(self, game_event_manager):
        assert not game_event_manager.has_event("nonexistent_event")

    def test_on_game_event_called(self, game_event_manager):
        schema = {
            "eventid": 2,
            "name": "player_death",
            "keys": [
                {"name": "userid", "type": 4},  # short
            ],
        }
        game_event_manager.register_schema(schema)

        received = []
        game_event_manager.on_game_event("player_death", lambda e: received.append(e))

        # Simulate dispatching a raw event with eventid=2
        # We construct a minimal fake raw event
        class FakeKey:
            def __init__(self, t, val):
                self._type = t
                self._val = val

            def get_type(self):
                return self._type

            def get_val_short(self):
                return self._val

        class FakeRawEvent:
            def get_eventid(self):
                return 2

            def get_keys(self):
                return [FakeKey(4, 7)]

        game_event_manager.dispatch(FakeRawEvent())

        assert len(received) == 1

    def test_no_handlers_no_crash(self, game_event_manager):
        schema = {"eventid": 3, "name": "unused_event", "keys": []}
        game_event_manager.register_schema(schema)

        class FakeRawEvent:
            def get_eventid(self):
                return 3

            def get_keys(self):
                return []

        # Should not raise even with no handlers registered
        game_event_manager.dispatch(FakeRawEvent())

    def test_multiple_handlers_per_event(self, game_event_manager):
        schema = {"eventid": 4, "name": "multi_event", "keys": []}
        game_event_manager.register_schema(schema)

        calls = []
        game_event_manager.on_game_event("multi_event", lambda e: calls.append("h1"))
        game_event_manager.on_game_event("multi_event", lambda e: calls.append("h2"))

        class FakeRawEvent:
            def get_eventid(self):
                return 4

            def get_keys(self):
                return []

        game_event_manager.dispatch(FakeRawEvent())
        assert calls == ["h1", "h2"]


class TestGameEvent:
    @pytest.fixture
    def game_event_cls(self):
        from gem.game_events import GameEvent

        return GameEvent

    def _make_event(self, game_event_cls, fields, keys_data):
        """
        fields: dict of name → (index, type)
        keys_data: list of (type, value) tuples
        """

        class FakeKey:
            def __init__(self, t, v):
                self._t = t
                self._v = v

            def get_type(self):
                return self._t

            def get_val_string(self):
                return self._v if self._t == 1 else ""

            def get_val_float(self):
                return self._v if self._t == 2 else 0.0

            def get_val_long(self):
                return self._v if self._t == 3 else 0

            def get_val_short(self):
                return self._v if self._t == 4 else 0

            def get_val_byte(self):
                return self._v if self._t == 5 else 0

            def get_val_bool(self):
                return self._v if self._t == 6 else False

            def get_val_uint64(self):
                return self._v if self._t == 7 else 0

        class FakeMsg:
            def get_keys(self):
                return [FakeKey(t, v) for t, v in keys_data]

        from gem.game_events import GameEventSchema

        schema = GameEventSchema(event_id=1, name="test", fields=fields)
        return game_event_cls(schema=schema, msg=FakeMsg())

    def test_get_string(self, game_event_cls):
        e = self._make_event(game_event_cls, fields={"name": (0, 1)}, keys_data=[(1, "hero_axe")])
        val, err = e.get_string("name")
        assert err is None
        assert val == "hero_axe"

    def test_get_int32_from_long(self, game_event_cls):
        e = self._make_event(game_event_cls, fields={"value": (0, 3)}, keys_data=[(3, 42)])
        val, err = e.get_int32("value")
        assert err is None
        assert val == 42

    def test_get_bool(self, game_event_cls):
        e = self._make_event(game_event_cls, fields={"flag": (0, 6)}, keys_data=[(6, True)])
        val, err = e.get_bool("flag")
        assert err is None
        assert val is True

    def test_missing_field_returns_error(self, game_event_cls):
        e = self._make_event(game_event_cls, fields={}, keys_data=[])
        val, err = e.get_string("missing")
        assert err is not None

    def test_type_mismatch_returns_error(self, game_event_cls):
        e = self._make_event(
            game_event_cls,
            fields={"val": (0, 3)},  # type=long
            keys_data=[(3, 10)],
        )
        val, err = e.get_string("val")  # asking for string but it's a long
        assert err is not None
