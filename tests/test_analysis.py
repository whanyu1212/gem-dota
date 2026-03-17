"""Tests for gem.analysis — position_at_tick and group_ability_hits."""

from __future__ import annotations

from unittest.mock import MagicMock

from gem.analysis import group_ability_hits, position_at_tick
from gem.combatlog import CombatLogEntry

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _player(position_log: list[tuple[int, float, float]]) -> MagicMock:
    p = MagicMock()
    p.position_log = position_log
    return p


def _entry(**kwargs) -> CombatLogEntry:
    defaults = {
        "tick": 0,
        "log_type": "DAMAGE",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_antimage",
        "inflictor_name": "axe_berserkers_call",
        "value": 100,
        "attacker_is_hero": True,
        "target_is_hero": True,
        "damage_type": "magical",
        "stun_duration": 0.0,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


# ---------------------------------------------------------------------------
# position_at_tick
# ---------------------------------------------------------------------------


class TestPositionAtTick:
    def test_empty_log_returns_none(self) -> None:
        player = _player([])
        assert position_at_tick(player, 100) is None

    def test_single_entry_always_returned(self) -> None:
        player = _player([(500, 1.0, 2.0)])
        assert position_at_tick(player, 0) == (1.0, 2.0)
        assert position_at_tick(player, 500) == (1.0, 2.0)
        assert position_at_tick(player, 9999) == (1.0, 2.0)

    def test_exact_tick_match(self) -> None:
        player = _player([(100, 10.0, 20.0), (200, 30.0, 40.0)])
        assert position_at_tick(player, 100) == (10.0, 20.0)
        assert position_at_tick(player, 200) == (30.0, 40.0)

    def test_tick_before_first_entry_returns_first(self) -> None:
        player = _player([(100, 10.0, 20.0), (200, 30.0, 40.0)])
        assert position_at_tick(player, 50) == (10.0, 20.0)

    def test_tick_after_last_entry_returns_last(self) -> None:
        player = _player([(100, 10.0, 20.0), (200, 30.0, 40.0)])
        assert position_at_tick(player, 500) == (30.0, 40.0)

    def test_picks_closer_of_two_samples(self) -> None:
        player = _player([(100, 1.0, 1.0), (200, 2.0, 2.0)])
        # tick 130 is 30 away from 100 and 70 away from 200 → picks (100)
        assert position_at_tick(player, 130) == (1.0, 1.0)
        # tick 180 is 80 away from 100 and 20 away from 200 → picks (200)
        assert position_at_tick(player, 180) == (2.0, 2.0)

    def test_equidistant_prefers_earlier(self) -> None:
        player = _player([(100, 1.0, 1.0), (200, 2.0, 2.0)])
        # tick 150 is 50 away from both — tie goes to the earlier (before)
        assert position_at_tick(player, 150) == (1.0, 1.0)

    def test_multiple_entries(self) -> None:
        log = [(i * 30, float(i), float(i)) for i in range(100)]
        player = _player(log)
        pos = position_at_tick(player, 30 * 50)
        assert pos == (50.0, 50.0)


# ---------------------------------------------------------------------------
# group_ability_hits
# ---------------------------------------------------------------------------


class TestGroupAbilityHits:
    def test_empty_log_returns_empty(self) -> None:
        assert group_ability_hits([]) == []

    def test_entries_without_inflictor_excluded(self) -> None:
        e = _entry(inflictor_name="")
        result = group_ability_hits([e])
        assert result == []

    def test_non_damage_entries_excluded(self) -> None:
        e = _entry(log_type="ABILITY")
        result = group_ability_hits([e])
        assert result == []

    def test_single_hit_becomes_single_cast(self) -> None:
        e = _entry(tick=100, value=200)
        casts = group_ability_hits([e])
        assert len(casts) == 1
        c = casts[0]
        assert c.tick == 100
        assert c.caster == "npc_dota_hero_axe"
        assert c.ability == "axe_berserkers_call"
        assert c.targets == ["npc_dota_hero_antimage"]
        assert c.total_damage == 200

    def test_two_hits_within_window_merged(self) -> None:
        e1 = _entry(tick=100, target_name="npc_dota_hero_antimage", value=150)
        e2 = _entry(
            tick=103, target_name="npc_dota_hero_axe", value=150, attacker_name="npc_dota_hero_axe"
        )
        # Same caster + ability, 3 ticks apart (within default window of 5)
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 1
        assert casts[0].total_damage == 300
        assert len(casts[0].targets) == 2

    def test_two_hits_outside_window_are_separate_casts(self) -> None:
        e1 = _entry(tick=100, value=150)
        e2 = _entry(tick=110, value=150)  # 10 ticks apart, window=5
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 2

    def test_different_abilities_are_separate_casts(self) -> None:
        e1 = _entry(tick=100, inflictor_name="axe_berserkers_call", value=100)
        e2 = _entry(tick=101, inflictor_name="axe_culling_blade", value=200)
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 2

    def test_different_casters_are_separate_casts(self) -> None:
        e1 = _entry(tick=100, attacker_name="npc_dota_hero_axe", value=100)
        e2 = _entry(tick=101, attacker_name="npc_dota_hero_antimage", value=100)
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 2

    def test_custom_window(self) -> None:
        e1 = _entry(tick=100, value=100)
        e2 = _entry(tick=108, value=100)  # 8 ticks apart
        # window=5: separate; window=10: merged
        assert len(group_ability_hits([e1, e2], window_ticks=5)) == 2
        assert len(group_ability_hits([e1, e2], window_ticks=10)) == 1

    def test_stun_duration_carried(self) -> None:
        e = _entry(tick=100, stun_duration=1.5)
        casts = group_ability_hits([e])
        assert casts[0].stun_duration == 1.5

    def test_damage_type_carried(self) -> None:
        e = _entry(tick=100, damage_type="magical")
        casts = group_ability_hits([e])
        assert casts[0].damage_type == "magical"

    def test_output_sorted_by_tick(self) -> None:
        entries = [_entry(tick=t, inflictor_name=f"spell_{t}") for t in [300, 100, 200]]
        casts = group_ability_hits(entries)
        ticks = [c.tick for c in casts]
        assert ticks == sorted(ticks)

    def test_entries_reference_preserved(self) -> None:
        e1 = _entry(tick=100, value=50)
        e2 = _entry(tick=102, target_name="npc_dota_hero_sf", value=60)
        casts = group_ability_hits([e1, e2])
        assert len(casts[0].entries) == 2
        assert casts[0].entries[0] is e1
        assert casts[0].entries[1] is e2
