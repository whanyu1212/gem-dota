"""Tests for ability levels, courier state, draft extraction, and stun duration.

Unit tests use fake objects. Integration tests parse a real .dem fixture and
verify plausible output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"


# ---------------------------------------------------------------------------
# Shared fake helpers
# ---------------------------------------------------------------------------


class FakeClass:
    def __init__(self, name: str) -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _make_entity(class_name: str, state: dict | None = None):
    from gem.entities import Entity

    e = Entity(index=0, serial=0, cls=FakeClass(class_name))
    if state:
        e._state.update(state)
    return e


class FakeParser:
    def __init__(self, tick: int = 0) -> None:
        self.tick = tick
        self._entity_handlers = []
        self.entity_manager = None
        self.string_tables = type("ST", (), {"get_by_name": lambda self, n: None})()

    def on_entity(self, handler) -> None:
        self._entity_handlers.append(handler)

    def fire_entity(self, entity, op) -> None:
        for h in self._entity_handlers:
            h(entity, op)


# ---------------------------------------------------------------------------
# 8a — Ability levels (PlayerStateSnapshot field)
# ---------------------------------------------------------------------------


class TestAbilityLevels:
    def test_snapshot_has_ability_levels_field(self):
        from gem.extractors.players import PlayerStateSnapshot

        snap = PlayerStateSnapshot(
            tick=0,
            player_id=0,
            npc_name="npc_dota_hero_axe",
            team=2,
            level=5,
            xp=1000,
            gold=500,
            net_worth=500,
            lh=10,
            dn=0,
            hp=800,
            max_hp=1000,
            mana=200.0,
            max_mana=300.0,
            x=None,
            y=None,
        )
        assert snap.ability_levels == {}

    def test_snapshot_ability_levels_can_be_set(self):
        from gem.extractors.players import PlayerStateSnapshot

        snap = PlayerStateSnapshot(
            tick=0,
            player_id=0,
            npc_name="npc_dota_hero_axe",
            team=2,
            level=5,
            xp=1000,
            gold=500,
            net_worth=500,
            lh=10,
            dn=0,
            hp=800,
            max_hp=1000,
            mana=200.0,
            max_mana=300.0,
            x=None,
            y=None,
            ability_levels={"axe_berserkers_call": 3, "axe_battle_hunger": 2},
        )
        assert snap.ability_levels["axe_berserkers_call"] == 3


# ---------------------------------------------------------------------------
# 8b — CourierExtractor
# ---------------------------------------------------------------------------


class TestCourierExtractor:
    def _make(self):
        from gem.extractors.courier import CourierExtractor

        ext = CourierExtractor(sample_interval=1)
        parser = FakeParser(tick=100)
        ext.attach(parser)
        return ext, parser

    def test_attach_registers_entity_callback(self):
        _, parser = self._make()
        assert len(parser._entity_handlers) == 1

    def test_non_courier_entity_ignored(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity("CDOTA_Unit_Hero_Axe", {"m_iTeamNum": 2})
        parser.fire_entity(entity, EntityOp.CREATED)
        assert ext.snapshots == []

    def test_courier_entity_creates_snapshot(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity(
            "CDOTA_Unit_Courier",
            {"m_iTeamNum": 2, "m_iCourierState": 1, "m_bFlyingCourier": False},
        )
        parser.fire_entity(entity, EntityOp.CREATED)
        assert len(ext.snapshots) == 1
        snap = ext.snapshots[0]
        assert snap.tick == 100
        assert snap.team == 2
        assert snap.state == 1
        assert snap.flying is False
        assert snap.x is None
        assert snap.y is None

    def test_courier_deleted_removes_from_tracking(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity("CDOTA_Unit_Courier", {"m_iTeamNum": 2})
        entity_idx = entity.get_index()
        parser.fire_entity(entity, EntityOp.CREATED)
        assert len(ext._couriers) == 1

        parser.fire_entity(entity, EntityOp.DELETED)
        assert entity_idx not in ext._couriers

    def test_sample_interval_throttles_snapshots(self):
        from gem.extractors.courier import CourierExtractor

        ext = CourierExtractor(sample_interval=100)
        parser = FakeParser(tick=0)
        ext.attach(parser)

        from gem.entities import EntityOp

        entity = _make_entity("CDOTA_Unit_Courier", {"m_iTeamNum": 2})
        parser.fire_entity(entity, EntityOp.CREATED)
        assert len(ext.snapshots) == 1  # first sample always fires

        # Advance tick slightly — below interval, no new snapshot
        parser.tick = 50
        parser.fire_entity(entity, EntityOp.UPDATED)
        assert len(ext.snapshots) == 1

        # Advance past interval — new snapshot
        parser.tick = 101
        parser.fire_entity(entity, EntityOp.UPDATED)
        assert len(ext.snapshots) == 2


# ---------------------------------------------------------------------------
# 8c — DraftExtractor
# ---------------------------------------------------------------------------


class TestDraftExtractor:
    def _make(self):
        from gem.extractors.draft import DraftExtractor

        ext = DraftExtractor()
        parser = FakeParser(tick=500)
        ext.attach(parser)
        return ext, parser

    def test_attach_registers_entity_callback(self):
        _, parser = self._make()
        assert len(parser._entity_handlers) == 1

    def test_non_grp_entity_ignored(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity("CDOTA_Unit_Hero_Axe")
        parser.fire_entity(entity, EntityOp.CREATED)
        assert ext.draft_events == []

    def test_ban_detected(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 1},  # hero_id=1
        )
        parser.fire_entity(entity, EntityOp.UPDATED)
        bans = [e for e in ext.draft_events if not e.is_pick]
        assert len(bans) == 1
        assert bans[0].hero_id == 1
        assert bans[0].slot_index == 0
        assert bans[0].is_pick is False
        assert bans[0].tick == 500

    def test_pick_detected(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_SelectedHeroes.0000": 2},  # hero_id=2
        )
        parser.fire_entity(entity, EntityOp.UPDATED)
        picks = [e for e in ext.draft_events if e.is_pick]
        assert len(picks) == 1
        assert picks[0].hero_id == 2
        assert picks[0].is_pick is True

    def test_idempotent_no_duplicate_events(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_SelectedHeroes.0000": 5},
        )
        # Fire same entity state multiple times
        parser.fire_entity(entity, EntityOp.UPDATED)
        parser.fire_entity(entity, EntityOp.UPDATED)
        parser.fire_entity(entity, EntityOp.UPDATED)
        assert len(ext.draft_events) == 1

    def test_zero_hero_id_ignored(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 0},
        )
        parser.fire_entity(entity, EntityOp.UPDATED)
        assert ext.draft_events == []

    def test_deleted_clears_grp(self):
        ext, parser = self._make()
        from gem.entities import EntityOp

        entity = _make_entity("CDOTAGamerulesProxy")
        parser.fire_entity(entity, EntityOp.CREATED)
        parser.fire_entity(entity, EntityOp.DELETED)
        assert ext._grp is None

    def test_hero_name_resolved_from_constants(self):
        from gem.extractors.draft import _HERO_ID_TO_NPC

        # The mapping should be non-empty
        assert len(_HERO_ID_TO_NPC) > 100
        # All values should be npc_dota_hero_* strings
        for npc in _HERO_ID_TO_NPC.values():
            assert npc.startswith("npc_dota_hero_")


# ---------------------------------------------------------------------------
# 8d — Stun duration
# ---------------------------------------------------------------------------


class TestStunDuration:
    def test_combat_log_entry_has_stun_duration_default(self):
        from gem.combatlog import CombatLogEntry

        e = CombatLogEntry(tick=0, log_type="DAMAGE")
        assert e.stun_duration == 0.0

    def test_stun_duration_stored_on_entry(self):
        from gem.combatlog import CombatLogEntry

        e = CombatLogEntry(tick=100, log_type="DAMAGE", stun_duration=1.5)
        assert e.stun_duration == 1.5

    def test_s2_entry_with_stun_duration(self):
        """process_s2_entry populates stun_duration via HasField."""
        from gem.combatlog import CombatLogProcessor

        class FakeMsg:
            type = 0  # DAMAGE
            attacker_name = 0
            target_name = 0
            inflictor_name = 0
            value = 10
            is_attacker_hero = True
            is_target_hero = True
            is_attacker_illusion = False
            is_target_illusion = False
            ability_level = 0
            gold_reason = 0
            xp_reason = 0
            stun_duration = 2.5

            def HasField(self, name):
                return name == "stun_duration"

        class FakeTable:
            def get(self, idx, default=""):
                return {1: "npc_dota_hero_axe", 2: "npc_dota_hero_lina"}.get(idx, default)

        FakeMsg.attacker_name = 1
        FakeMsg.target_name = 2

        proc = CombatLogProcessor()
        collected = []
        proc.on_combat_log_entry(collected.append)
        proc.process_s2_entry(FakeMsg(), FakeTable(), tick=1000)

        assert len(collected) == 1
        assert collected[0].stun_duration == 2.5

    def test_s2_entry_without_stun_duration_defaults_zero(self):
        from gem.combatlog import CombatLogProcessor

        class FakeMsg:
            type = 0
            attacker_name = 0
            target_name = 0
            inflictor_name = 0
            value = 5
            is_attacker_hero = False
            is_target_hero = False
            is_attacker_illusion = False
            is_target_illusion = False
            ability_level = 0
            gold_reason = 0
            xp_reason = 0
            stun_duration = 0.0

            def HasField(self, name):
                return False

        class FakeTable:
            def get(self, idx, default=""):
                return default

        proc = CombatLogProcessor()
        collected = []
        proc.on_combat_log_entry(collected.append)
        proc.process_s2_entry(FakeMsg(), FakeTable(), tick=500)

        assert collected[0].stun_duration == 0.0

    def test_parsed_player_has_stuns_dealt(self):
        from gem.models import ParsedPlayer

        pp = ParsedPlayer(player_id=0)
        assert pp.stuns_dealt == 0.0


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.slow
@pytest.mark.integration
class TestPhase8Integration:
    @pytest.fixture(scope="class")
    def match(self):
        import gem

        return gem.parse(str(FIXTURE))

    def test_ability_levels_populated(self, match):
        from gem.extractors.players import PlayerExtractor

        # Re-parse to access snapshots directly
        from gem.parser import ReplayParser

        p = ReplayParser(str(FIXTURE))
        ext = PlayerExtractor()
        ext.attach(p)
        p.parse()
        # At least one snapshot should have non-empty ability_levels
        snaps_with_abilities = [s for s in ext.snapshots if s.ability_levels]
        assert snaps_with_abilities, "Expected at least one snapshot with ability levels"
        # All levels should be in valid range 0-7
        for snap in snaps_with_abilities:
            for level in snap.ability_levels.values():
                assert 0 <= level <= 7, f"Unexpected ability level {level}"

    def test_courier_snapshots_populated(self, match):
        assert len(match.courier_snapshots) > 0

    def test_courier_teams_valid(self, match):
        for snap in match.courier_snapshots:
            assert snap.team in (2, 3), f"Unexpected courier team {snap.team}"

    def test_draft_events_populated(self, match):
        # TI14 finals is CM — should have bans and picks
        assert len(match.draft) > 0

    def test_draft_picks_count(self, match):
        picks = [e for e in match.draft if e.is_pick]
        assert 1 <= len(picks) <= 10

    def test_draft_bans_count(self, match):
        bans = [e for e in match.draft if not e.is_pick]
        assert len(bans) <= 14

    def test_draft_hero_names_resolved(self, match):
        picks = [e for e in match.draft if e.is_pick]
        resolved = [e for e in picks if e.hero_name.startswith("npc_dota_hero_")]
        assert len(resolved) > 0, "Expected at least some picks to have resolved hero names"

    def test_stuns_dealt_non_negative(self, match):
        for pp in match.players:
            assert pp.stuns_dealt >= 0.0

    def test_stuns_dealt_nonzero_for_some_players(self, match):
        # In a real match at least some heroes deal stuns
        total = sum(pp.stuns_dealt for pp in match.players)
        assert total > 0, "Expected non-zero total stun duration in a real match"
