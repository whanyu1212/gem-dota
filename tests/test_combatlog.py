"""
Tests for gem.combatlog — S1 (game event) and S2 (user message) combat log ingestion.

Reference: clarity/CombatLog.java, odota/Parse.java
"""

import pytest


@pytest.fixture
def combatlog_processor():
    from gem.combatlog import CombatLogProcessor

    return CombatLogProcessor()


class TestCombatLogProcessor:
    def test_on_entry_handler_registered(self, combatlog_processor):
        received = []
        combatlog_processor.on_combat_log_entry(lambda e: received.append(e))
        assert len(combatlog_processor._handlers) == 1

    def test_multiple_handlers(self, combatlog_processor):
        calls = []
        combatlog_processor.on_combat_log_entry(lambda e: calls.append("h1"))
        combatlog_processor.on_combat_log_entry(lambda e: calls.append("h2"))
        combatlog_processor._emit(object())  # emit a fake entry
        assert calls == ["h1", "h2"]


class TestCombatLogEntry:
    """Test the CombatLogEntry dataclass."""

    @pytest.fixture
    def entry_cls(self):
        from gem.combatlog import CombatLogEntry

        return CombatLogEntry

    def test_basic_fields(self, entry_cls):
        e = entry_cls(
            tick=100,
            log_type="DAMAGE",
            attacker_name="npc_dota_hero_axe",
            target_name="npc_dota_hero_juggernaut",
            inflictor_name="axe_berserkers_call",
            value=250,
            attacker_is_hero=True,
            target_is_hero=True,
            attacker_is_illusion=False,
            target_is_illusion=False,
        )
        assert e.tick == 100
        assert e.log_type == "DAMAGE"
        assert e.attacker_name == "npc_dota_hero_axe"
        assert e.value == 250

    def test_defaults(self, entry_cls):
        e = entry_cls(tick=0, log_type="HEAL")
        assert e.attacker_name == ""
        assert e.target_name == ""
        assert e.value == 0
        assert e.attacker_is_hero is False

    def test_all_log_types_importable(self):
        from gem.combatlog import COMBAT_LOG_TYPES

        required = {
            "DAMAGE",
            "HEAL",
            "MODIFIER_ADD",
            "MODIFIER_REMOVE",
            "DEATH",
            "ABILITY",
            "ITEM",
            "GOLD",
            "XP",
            "PURCHASE",
            "BUYBACK",
            "KILLSTREAK",
        }
        for t in required:
            assert t in COMBAT_LOG_TYPES, f"Missing combat log type: {t}"


class TestS2CombatLogEntry:
    """Test parsing of CMsgDOTACombatLogEntry (S2 path)."""

    def test_parse_damage_entry(self, combatlog_processor):
        # Build a minimal fake CMsgDOTACombatLogEntry
        class FakeNameTable:
            def __init__(self):
                self._names = {0: "npc_dota_hero_axe", 1: "npc_dota_hero_juggernaut"}

            def get(self, idx, default=""):
                return self._names.get(idx, default)

        class FakeMsg:
            type = 0  # DAMAGE
            attacker_name = 0
            target_name = 1
            inflictor_name = 0
            value = 100
            attacker_hero = True
            target_hero = True
            attacker_illusion = False
            target_illusion = False
            ability_level = 0
            gold_reason = 0
            xp_reason = 0

        received = []
        combatlog_processor.on_combat_log_entry(lambda e: received.append(e))

        name_table = FakeNameTable()
        combatlog_processor.process_s2_entry(FakeMsg(), name_table)

        assert len(received) == 1
        entry = received[0]
        assert entry.value == 100
        assert entry.attacker_name == "npc_dota_hero_axe"
        assert entry.target_name == "npc_dota_hero_juggernaut"
