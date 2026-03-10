"""Tests for gem.combatlog — S1 (game event) and S2 (user message) combat log.

Reference: clarity/CombatLog.java, odota/Parse.java
"""

from gem.combatlog import (
    COMBAT_LOG_TYPES,
    CombatLogEntry,
    CombatLogProcessor,
    _resolve_name,
)

# ---------------------------------------------------------------------------
# Helpers — fake objects
# ---------------------------------------------------------------------------


class FakeNameTable:
    """Mimics a StringTable with .items dict[int, (key_str, value_bytes)]."""

    def __init__(self, names: dict[int, str]):
        self.items = {idx: (name, b"") for idx, name in names.items()}


class FakeGameEvent:
    """Mimics a GameEvent with typed accessors (get_int32, get_bool)."""

    def __init__(self, int_fields: dict[str, int], bool_fields: dict[str, bool]):
        self._ints = int_fields
        self._bools = bool_fields

    def get_int32(self, name: str) -> tuple[int, str | None]:
        if name in self._ints:
            return self._ints[name], None
        return 0, f"missing field {name!r}"

    def get_bool(self, name: str) -> tuple[bool, str | None]:
        if name in self._bools:
            return self._bools[name], None
        return False, f"missing field {name!r}"


class FakeS2Entry:
    """Mimics a CMsgDOTACombatLogEntry proto message."""

    def __init__(
        self,
        type=0,
        attacker_name=0,
        target_name=0,
        inflictor_name=0,
        value=0,
        is_attacker_hero=False,
        is_target_hero=False,
        is_attacker_illusion=False,
        is_target_illusion=False,
        ability_level=0,
        gold_reason=0,
        xp_reason=0,
    ):
        self.type = type
        self.attacker_name = attacker_name
        self.target_name = target_name
        self.inflictor_name = inflictor_name
        self.value = value
        self.is_attacker_hero = is_attacker_hero
        self.is_target_hero = is_target_hero
        self.is_attacker_illusion = is_attacker_illusion
        self.is_target_illusion = is_target_illusion
        self.ability_level = ability_level
        self.gold_reason = gold_reason
        self.xp_reason = xp_reason


class FakeBulkMsg:
    """Mimics CDOTAUserMsg_CombatLogBulkData."""

    def __init__(self, entries: list):
        self.combat_entries = entries


# ---------------------------------------------------------------------------
# COMBAT_LOG_TYPES — completeness
# ---------------------------------------------------------------------------


class TestCombatLogTypes:
    def test_all_required_types_present(self):
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
        assert required <= COMBAT_LOG_TYPES

    def test_is_frozenset(self):
        assert isinstance(COMBAT_LOG_TYPES, frozenset)


# ---------------------------------------------------------------------------
# CombatLogEntry — dataclass
# ---------------------------------------------------------------------------


class TestCombatLogEntry:
    def test_required_fields(self):
        e = CombatLogEntry(tick=100, log_type="DAMAGE")
        assert e.tick == 100
        assert e.log_type == "DAMAGE"

    def test_defaults(self):
        e = CombatLogEntry(tick=0, log_type="HEAL")
        assert e.attacker_name == ""
        assert e.target_name == ""
        assert e.inflictor_name == ""
        assert e.value == 0
        assert e.attacker_is_hero is False
        assert e.target_is_hero is False
        assert e.attacker_is_illusion is False
        assert e.target_is_illusion is False
        assert e.ability_level == 0
        assert e.gold_reason == 0
        assert e.xp_reason == 0

    def test_all_fields_set(self):
        e = CombatLogEntry(
            tick=500,
            log_type="ABILITY",
            attacker_name="npc_dota_hero_axe",
            target_name="npc_dota_hero_juggernaut",
            inflictor_name="axe_berserkers_call",
            value=200,
            attacker_is_hero=True,
            target_is_hero=True,
            attacker_is_illusion=False,
            target_is_illusion=False,
            ability_level=3,
            gold_reason=0,
            xp_reason=0,
        )
        assert e.attacker_name == "npc_dota_hero_axe"
        assert e.value == 200
        assert e.ability_level == 3


# ---------------------------------------------------------------------------
# _resolve_name helper
# ---------------------------------------------------------------------------


class TestResolveName:
    def test_index_zero_returns_empty(self):
        table = FakeNameTable({0: "should_not_appear"})
        assert _resolve_name(table, 0) == ""

    def test_valid_index_resolves(self):
        table = FakeNameTable({1: "npc_dota_hero_axe", 2: "axe_berserkers_call"})
        assert _resolve_name(table, 1) == "npc_dota_hero_axe"
        assert _resolve_name(table, 2) == "axe_berserkers_call"

    def test_missing_index_returns_empty(self):
        table = FakeNameTable({1: "hero"})
        assert _resolve_name(table, 99) == ""


# ---------------------------------------------------------------------------
# CombatLogProcessor — handler registration
# ---------------------------------------------------------------------------


class TestCombatLogProcessorHandlers:
    def test_register_handler(self):
        p = CombatLogProcessor()
        received = []
        p.on_combat_log_entry(lambda e: received.append(e))
        assert len(p._handlers) == 1

    def test_multiple_handlers_all_called(self):
        p = CombatLogProcessor()
        calls = []
        p.on_combat_log_entry(lambda e: calls.append("h1"))
        p.on_combat_log_entry(lambda e: calls.append("h2"))
        p._emit(CombatLogEntry(tick=0, log_type="DAMAGE"))
        assert calls == ["h1", "h2"]

    def test_no_handlers_emit_no_crash(self):
        p = CombatLogProcessor()
        p._emit(CombatLogEntry(tick=0, log_type="DAMAGE"))  # should not raise


# ---------------------------------------------------------------------------
# CombatLogProcessor — S1 path (dota_combatlog game event)
# ---------------------------------------------------------------------------


class TestS1CombatLog:
    def _make_processor_with_handler(self):
        p = CombatLogProcessor()
        received = []
        p.on_combat_log_entry(received.append)
        return p, received

    def _make_event(
        self,
        type_val=0,
        attacker=1,
        target=2,
        inflictor=0,
        value=100,
        attacker_hero=True,
        target_hero=True,
        attacker_illusion=False,
        target_illusion=False,
        ability_level=1,
        gold_reason=0,
        xp_reason=0,
    ):
        return FakeGameEvent(
            int_fields={
                "type": type_val,
                "attackername": attacker,
                "targetname": target,
                "inflictorname": inflictor,
                "value": value,
                "ability_level": ability_level,
                "gold_reason": gold_reason,
                "xp_reason": xp_reason,
            },
            bool_fields={
                "attackerhero": attacker_hero,
                "targethero": target_hero,
                "attackerillusion": attacker_illusion,
                "targetillusion": target_illusion,
            },
        )

    def test_damage_entry(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({1: "npc_dota_hero_axe", 2: "npc_dota_hero_juggernaut"})
        p.process_s1_event(self._make_event(type_val=0, value=250), table, tick=1000)
        assert len(received) == 1
        e = received[0]
        assert e.log_type == "DAMAGE"
        assert e.attacker_name == "npc_dota_hero_axe"
        assert e.target_name == "npc_dota_hero_juggernaut"
        assert e.value == 250
        assert e.tick == 1000

    def test_all_log_types_mapped(self):
        """Each integer type 0..11 should map to a known log type string."""
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        for type_val in range(12):
            received.clear()
            p.process_s1_event(self._make_event(type_val=type_val), table)
            assert received[0].log_type in COMBAT_LOG_TYPES

    def test_unknown_type_defaults_to_damage(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        p.process_s1_event(self._make_event(type_val=99), table)
        assert received[0].log_type == "DAMAGE"

    def test_hero_flags(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        p.process_s1_event(self._make_event(attacker_hero=True, target_hero=False), table)
        e = received[0]
        assert e.attacker_is_hero is True
        assert e.target_is_hero is False

    def test_illusion_flags(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        p.process_s1_event(self._make_event(attacker_illusion=True, target_illusion=True), table)
        e = received[0]
        assert e.attacker_is_illusion is True
        assert e.target_is_illusion is True

    def test_gold_reason(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        p.process_s1_event(self._make_event(type_val=8, gold_reason=5), table)
        e = received[0]
        assert e.log_type == "GOLD"
        assert e.gold_reason == 5

    def test_xp_reason(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        p.process_s1_event(self._make_event(type_val=10, xp_reason=3), table)
        e = received[0]
        assert e.log_type == "XP"
        assert e.xp_reason == 3

    def test_name_index_zero_resolves_empty(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        p.process_s1_event(self._make_event(attacker=0, target=0), table)
        e = received[0]
        assert e.attacker_name == ""
        assert e.target_name == ""

    def test_tick_propagated(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        p.process_s1_event(self._make_event(), table, tick=42000)
        assert received[0].tick == 42000


# ---------------------------------------------------------------------------
# CombatLogProcessor — S2 path (CMsgDOTACombatLogEntry)
# ---------------------------------------------------------------------------


class TestS2CombatLog:
    def _make_processor_with_handler(self):
        p = CombatLogProcessor()
        received = []
        p.on_combat_log_entry(received.append)
        return p, received

    def test_damage_entry(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({1: "npc_dota_hero_axe", 2: "npc_dota_hero_juggernaut"})
        msg = FakeS2Entry(
            type=0,
            attacker_name=1,
            target_name=2,
            value=150,
            is_attacker_hero=True,
            is_target_hero=True,
        )
        p.process_s2_entry(msg, table, tick=5000)
        assert len(received) == 1
        e = received[0]
        assert e.log_type == "DAMAGE"
        assert e.attacker_name == "npc_dota_hero_axe"
        assert e.target_name == "npc_dota_hero_juggernaut"
        assert e.value == 150
        assert e.tick == 5000
        assert e.attacker_is_hero is True

    def test_heal_entry(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({1: "npc_dota_hero_omniknight"})
        msg = FakeS2Entry(type=1, attacker_name=1, value=300)
        p.process_s2_entry(msg, table)
        assert received[0].log_type == "HEAL"
        assert received[0].value == 300

    def test_death_entry(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({3: "npc_dota_hero_axe"})
        msg = FakeS2Entry(type=4, target_name=3)
        p.process_s2_entry(msg, table)
        assert received[0].log_type == "DEATH"
        assert received[0].target_name == "npc_dota_hero_axe"

    def test_ability_entry_with_level(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({1: "npc_dota_hero_axe", 5: "axe_berserkers_call"})
        msg = FakeS2Entry(
            type=5, attacker_name=1, inflictor_name=5, ability_level=3, is_attacker_hero=True
        )
        p.process_s2_entry(msg, table)
        e = received[0]
        assert e.log_type == "ABILITY"
        assert e.inflictor_name == "axe_berserkers_call"
        assert e.ability_level == 3

    def test_gold_entry(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        msg = FakeS2Entry(type=8, value=200, gold_reason=6)
        p.process_s2_entry(msg, table)
        e = received[0]
        assert e.log_type == "GOLD"
        assert e.value == 200
        assert e.gold_reason == 6

    def test_all_twelve_types(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        for t in range(12):
            received.clear()
            p.process_s2_entry(FakeS2Entry(type=t), table)
            assert received[0].log_type in COMBAT_LOG_TYPES

    def test_illusion_flags(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})
        msg = FakeS2Entry(is_attacker_illusion=True, is_target_illusion=False)
        p.process_s2_entry(msg, table)
        assert received[0].attacker_is_illusion is True
        assert received[0].target_is_illusion is False

    def test_name_index_zero_empty(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({1: "hero"})
        msg = FakeS2Entry(attacker_name=0, target_name=0)
        p.process_s2_entry(msg, table)
        assert received[0].attacker_name == ""
        assert received[0].target_name == ""

    def test_missing_name_index_empty(self):
        p, received = self._make_processor_with_handler()
        table = FakeNameTable({})  # empty — index 5 not present
        msg = FakeS2Entry(attacker_name=5)
        p.process_s2_entry(msg, table)
        assert received[0].attacker_name == ""


# ---------------------------------------------------------------------------
# CombatLogProcessor — S2 bulk path
# ---------------------------------------------------------------------------


class TestS2BulkCombatLog:
    def test_bulk_emits_one_entry_per_combat_entry(self):
        p = CombatLogProcessor()
        received = []
        p.on_combat_log_entry(received.append)
        table = FakeNameTable({1: "hero_a", 2: "hero_b"})
        entries = [
            FakeS2Entry(type=0, attacker_name=1, target_name=2, value=100),
            FakeS2Entry(type=1, attacker_name=2, target_name=1, value=50),
            FakeS2Entry(type=4, target_name=2),
        ]
        p.process_s2_bulk(FakeBulkMsg(entries), table, tick=9000)
        assert len(received) == 3
        assert received[0].log_type == "DAMAGE"
        assert received[1].log_type == "HEAL"
        assert received[2].log_type == "DEATH"

    def test_bulk_empty_entries_no_crash(self):
        p = CombatLogProcessor()
        received = []
        p.on_combat_log_entry(received.append)
        p.process_s2_bulk(FakeBulkMsg([]), FakeNameTable({}))
        assert received == []

    def test_bulk_tick_propagated_to_all(self):
        p = CombatLogProcessor()
        received = []
        p.on_combat_log_entry(received.append)
        entries = [FakeS2Entry(), FakeS2Entry(), FakeS2Entry()]
        p.process_s2_bulk(FakeBulkMsg(entries), FakeNameTable({}), tick=12345)
        assert all(e.tick == 12345 for e in received)


# ---------------------------------------------------------------------------
# S1 vs S2 parity — same entry from both paths
# ---------------------------------------------------------------------------


class TestS1S2Parity:
    """Both paths should produce equivalent CombatLogEntry for the same event."""

    def test_damage_parity(self):
        table = FakeNameTable({1: "npc_dota_hero_axe", 2: "npc_dota_hero_juggernaut"})

        p = CombatLogProcessor()
        s1_entries: list[CombatLogEntry] = []
        s2_entries: list[CombatLogEntry] = []
        p.on_combat_log_entry(s1_entries.append)

        s1_event = FakeGameEvent(
            int_fields={
                "type": 0,
                "attackername": 1,
                "targetname": 2,
                "inflictorname": 0,
                "value": 250,
                "ability_level": 0,
                "gold_reason": 0,
                "xp_reason": 0,
            },
            bool_fields={
                "attackerhero": True,
                "targethero": True,
                "attackerillusion": False,
                "targetillusion": False,
            },
        )
        p.process_s1_event(s1_event, table, tick=100)

        p2 = CombatLogProcessor()
        p2.on_combat_log_entry(s2_entries.append)
        s2_msg = FakeS2Entry(
            type=0,
            attacker_name=1,
            target_name=2,
            value=250,
            is_attacker_hero=True,
            is_target_hero=True,
        )
        p2.process_s2_entry(s2_msg, table, tick=100)

        assert len(s1_entries) == 1
        assert len(s2_entries) == 1
        s1 = s1_entries[0]
        s2 = s2_entries[0]

        assert s1.log_type == s2.log_type
        assert s1.attacker_name == s2.attacker_name
        assert s1.target_name == s2.target_name
        assert s1.value == s2.value
        assert s1.attacker_is_hero == s2.attacker_is_hero
        assert s1.target_is_hero == s2.target_is_hero
        assert s1.tick == s2.tick
