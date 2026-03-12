"""Unit tests for gem.extractors.objectives.

Covers ObjectivesExtractor (roshan kills, tower kills, barracks kills,
aegis events), _find_team helper, and _AEGIS_EVENT_TYPE dispatch.
All tests use fake combat log entries — no real .dem files.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from gem.combatlog import CombatLogEntry

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_combat_log_entry(**kwargs):
    defaults = {
        "tick": 100,
        "log_type": "DEATH",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_juggernaut",
        "inflictor_name": "",
        "value": 0,
        "attacker_is_hero": True,
        "target_is_hero": True,
        "attacker_is_illusion": False,
        "target_is_illusion": False,
        "ability_level": 0,
        "gold_reason": 0,
        "xp_reason": 0,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


class FakeParser:
    def __init__(self) -> None:
        self._combat_log_handlers = []
        self._chat_event_handlers = []

    def on_combat_log_entry(self, handler) -> None:
        self._combat_log_handlers.append(handler)

    def on_chat_event(self, handler) -> None:
        self._chat_event_handlers.append(handler)

    def on_game_start(self, handler) -> None:
        pass

    def on_game_end(self, handler) -> None:
        pass

    def fire_combat_log(self, entry) -> None:
        for h in self._combat_log_handlers:
            h(entry)


# ---------------------------------------------------------------------------
# ObjectivesExtractor
# ---------------------------------------------------------------------------


class TestObjectivesExtractor:
    def _make(self):
        from gem.extractors.objectives import ObjectivesExtractor

        e = ObjectivesExtractor()
        parser = FakeParser()
        e.attach(parser)
        return e, parser

    def test_attach_registers_combat_log_callback(self):
        _, parser = self._make()
        assert len(parser._combat_log_handlers) == 1

    def test_roshan_kill_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=500, target_name="npc_dota_roshan", attacker_name="npc_dota_hero_axe"
            )
        )
        assert len(ext.roshan_kills) == 1
        kill = ext.roshan_kills[0]
        assert kill.tick == 500
        assert kill.killer == "npc_dota_hero_axe"
        assert kill.kill_number == 1

    def test_roshan_kill_number_increments(self):
        ext, parser = self._make()
        for tick in (500, 2000, 4000):
            parser.fire_combat_log(_make_combat_log_entry(tick=tick, target_name="npc_dota_roshan"))
        assert [k.kill_number for k in ext.roshan_kills] == [1, 2, 3]

    def test_tower_kill_radiant_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=300,
                target_name="npc_dota_goodguys_tower1_top",
                attacker_name="npc_dota_hero_axe",
            )
        )
        assert len(ext.tower_kills) == 1
        tk = ext.tower_kills[0]
        assert tk.team == 2
        assert tk.tower_name == "npc_dota_goodguys_tower1_top"

    def test_tower_kill_dire_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=300,
                target_name="npc_dota_badguys_tower1_top",
                attacker_name="npc_dota_hero_juggernaut",
            )
        )
        assert len(ext.tower_kills) == 1
        assert ext.tower_kills[0].team == 3

    def test_barracks_kill_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=700,
                target_name="npc_dota_goodguys_melee_rax_top",
                attacker_name="npc_dota_hero_axe",
            )
        )
        assert len(ext.barracks_kills) == 1
        bk = ext.barracks_kills[0]
        assert bk.team == 2
        assert bk.killer == "npc_dota_hero_axe"

    def test_non_death_entry_ignored(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(log_type="DAMAGE", target_name="npc_dota_roshan")
        )
        assert ext.roshan_kills == []
        assert ext.tower_kills == []

    def test_hero_death_not_captured(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(log_type="DEATH", target_name="npc_dota_hero_axe")
        )
        assert ext.roshan_kills == []
        assert ext.tower_kills == []
        assert ext.barracks_kills == []


# ---------------------------------------------------------------------------
# _find_team helper
# ---------------------------------------------------------------------------


class TestFindTeam:
    def test_radiant_tower(self):
        from gem.extractors.objectives import _TOWER_TEAM, _find_team

        assert _find_team("npc_dota_goodguys_tower1", _TOWER_TEAM) == 2

    def test_dire_tower(self):
        from gem.extractors.objectives import _TOWER_TEAM, _find_team

        assert _find_team("npc_dota_badguys_tower3", _TOWER_TEAM) == 3

    def test_unknown_returns_zero(self):
        from gem.extractors.objectives import _TOWER_TEAM, _find_team

        assert _find_team("npc_dota_roshan", _TOWER_TEAM) == 0

    def test_radiant_barracks(self):
        from gem.extractors.objectives import _BARRACKS_TEAM, _find_team

        assert _find_team("npc_dota_goodguys_melee_rax_top", _BARRACKS_TEAM) == 2

    def test_dire_barracks(self):
        from gem.extractors.objectives import _BARRACKS_TEAM, _find_team

        assert _find_team("npc_dota_badguys_range_rax_bot", _BARRACKS_TEAM) == 3


# ---------------------------------------------------------------------------
# _AEGIS_EVENT_TYPE dispatch and _on_chat_event
# ---------------------------------------------------------------------------


class TestAegisEventType:
    def test_all_three_types_mapped(self):
        from gem.extractors.objectives import (
            _AEGIS_EVENT_TYPE,
            _CHAT_MSG_AEGIS,
            _CHAT_MSG_AEGIS_STOLEN,
            _CHAT_MSG_DENIED_AEGIS,
        )

        assert _AEGIS_EVENT_TYPE[_CHAT_MSG_AEGIS] == "pickup"
        assert _AEGIS_EVENT_TYPE[_CHAT_MSG_AEGIS_STOLEN] == "stolen"
        assert _AEGIS_EVENT_TYPE[_CHAT_MSG_DENIED_AEGIS] == "denied"

    def test_unknown_type_not_present(self):
        from gem.extractors.objectives import _AEGIS_EVENT_TYPE

        assert _AEGIS_EVENT_TYPE.get(9999) is None

    def test_on_chat_event_pickup(self):
        from gem.extractors.objectives import _CHAT_MSG_AEGIS, ObjectivesExtractor

        ext = ObjectivesExtractor()
        msg = MagicMock(type=_CHAT_MSG_AEGIS, playerid_1=3)
        ext._on_chat_event(msg, tick=1000)
        assert ext.aegis_events[0].event_type == "pickup"
        assert ext.aegis_events[0].player_id == 3

    def test_on_chat_event_stolen(self):
        from gem.extractors.objectives import _CHAT_MSG_AEGIS_STOLEN, ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_AEGIS_STOLEN, playerid_1=7), tick=2000)
        assert ext.aegis_events[0].event_type == "stolen"

    def test_on_chat_event_denied(self):
        from gem.extractors.objectives import _CHAT_MSG_DENIED_AEGIS, ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_DENIED_AEGIS, playerid_1=5), tick=3000)
        assert ext.aegis_events[0].event_type == "denied"

    def test_on_chat_event_ignores_unknown(self):
        from gem.extractors.objectives import ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=9999), tick=500)
        assert ext.aegis_events == []
