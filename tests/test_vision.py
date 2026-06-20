"""Tests for estimate_vision, is_daytime, and vision modifier reveals."""

from __future__ import annotations

from unittest.mock import MagicMock

from gem.analysis import estimate_vision, is_daytime
from gem.extractors.wards import WardEvent
from gem.results.models import VisionModifierEvent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DAY_VISION = 1800
_NIGHT_VISION = 800
_WARD_VISION = 1600

# game_start_tick=0 → tick 0 = game time 0:00 (daytime).
# Dota's cycle is 10 min: day 0:00–5:00, night 5:00–10:00, repeating.
# Night starts at 5:00 = 9000 ticks into a cycle.
_NIGHT_TICK = 11000  # well into night (5:00–10:00 → 9000–18000 ticks)
_DAY_TICK = 5000  # well into day (< 9000 ticks from game start)


def _player(team: int, position_log: list[tuple[int, float, float]]) -> MagicMock:
    p = MagicMock()
    p.team = team
    p.hero_name = f"npc_dota_hero_axe_{team}"
    p.position_log = position_log
    p.player_id = 0
    return p


def _ward(
    team: int,
    x: float,
    y: float,
    tick: int = 0,
    killed_tick: int | None = None,
    expires_tick: int | None = None,
    ward_type: str = "observer",
) -> WardEvent:
    return WardEvent(
        tick=tick,
        player_id=0,
        placer="npc_dota_hero_axe",
        ward_type=ward_type,
        team=team,
        x=x,
        y=y,
        expires_tick=expires_tick,
        killed_tick=killed_tick,
        killer="",
    )


def _mod(
    modifier_name: str,
    target_name: str,
    caster_name: str,
    caster_team: int,
    tick: int = 0,
    end_tick: int | None = None,
) -> VisionModifierEvent:
    return VisionModifierEvent(
        tick=tick,
        end_tick=end_tick,
        modifier_name=modifier_name,
        target_name=target_name,
        caster_name=caster_name,
        caster_team=caster_team,
    )


def _match(
    players: list,
    wards: list,
    game_start_tick: int = 0,
    vision_modifiers: list | None = None,
) -> MagicMock:
    m = MagicMock()
    m.players = players
    m.wards = wards
    m.game_start_tick = game_start_tick
    m.vision_modifiers = vision_modifiers or []
    return m


# ---------------------------------------------------------------------------
# is_daytime
# ---------------------------------------------------------------------------


class TestIsDaytime:
    # Dota's cycle is 10 min (18000 ticks): day 0:00–5:00, night 5:00–10:00.
    # Night starts at 5:00 = 9000 ticks. Reference:
    # https://liquipedia.net/dota2/Time_of_Day

    def test_game_start_is_daytime(self) -> None:
        assert is_daytime(0, 0) is True

    def test_early_game_is_daytime(self) -> None:
        assert is_daytime(0, 5000) is True  # 2:46, day

    def test_tick_just_before_night_is_day(self) -> None:
        # 8999 ticks = 4:59.96 — last tick of the first day.
        assert is_daytime(0, 8999) is True

    def test_night_starts_exactly_at_5min(self) -> None:
        # 9000 ticks = 5:00 — the first night tick (boundary is night).
        assert is_daytime(0, 9000) is False

    def test_well_into_first_night(self) -> None:
        assert is_daytime(0, 11000) is False  # 6:06, night

    def test_day_returns_exactly_at_10min(self) -> None:
        # 18000 ticks = 10:00 — one full cycle, back to day.
        assert is_daytime(0, 18000) is True

    def test_second_night_starts_at_15min(self) -> None:
        # 27000 ticks = 15:00 — start of the second night (was day under the
        # old, buggy 15-minute cycle).
        assert is_daytime(0, 27000) is False

    def test_third_day_at_20min(self) -> None:
        assert is_daytime(0, 36000) is True  # 20:00, day again

    def test_game_start_tick_offset(self) -> None:
        # If game started at tick 1000, game time 0 = tick 1000.
        assert is_daytime(1000, 1000) is True
        assert is_daytime(1000, 1000 + 9000) is False  # 5:00 → night

    def test_none_game_start_treated_as_zero(self) -> None:
        assert is_daytime(None, 5000) is True
        assert is_daytime(None, 11000) is False

    def test_underscore_alias_preserved(self) -> None:
        # `_is_daytime` is a backwards-compat alias for the renamed public
        # `is_daytime`; both must import from gem.analysis and be the same object.
        from gem.analysis import _is_daytime, is_daytime

        assert _is_daytime is is_daytime


# ---------------------------------------------------------------------------
# estimate_vision — hero vision
# ---------------------------------------------------------------------------


class TestEstimateVisionHero:
    def test_no_players_no_vision(self) -> None:
        match = _match([], [])
        assert estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0) == []

    def test_allied_hero_within_day_range(self) -> None:
        p = _player(2, [(_DAY_TICK, 0.0, 0.0)])
        match = _match([p], [])
        result = estimate_vision(match, 2, _DAY_TICK, 1000.0, 0.0)
        assert len(result) == 1
        assert result[0].kind == "hero"
        assert result[0].vision_radius == _DAY_VISION

    def test_allied_hero_outside_day_range(self) -> None:
        p = _player(2, [(_DAY_TICK, 0.0, 0.0)])
        match = _match([p], [])
        result = estimate_vision(match, 2, _DAY_TICK, 2000.0, 0.0)
        assert result == []

    def test_night_uses_reduced_radius(self) -> None:
        # Hero at (0,0), query at (1000, 0) — within day range but not night range
        p = _player(2, [(_NIGHT_TICK, 0.0, 0.0)])
        match = _match([p], [], game_start_tick=0)
        # Day: 1000 < 1800 → vision
        result_day = estimate_vision(match, 2, _DAY_TICK, 1000.0, 0.0)
        assert len(result_day) == 1
        assert result_day[0].vision_radius == _DAY_VISION
        # Night: 1000 > 800 → no vision
        result_night = estimate_vision(match, 2, _NIGHT_TICK, 1000.0, 0.0)
        assert result_night == []

    def test_enemy_hero_not_counted(self) -> None:
        p = _player(3, [(_DAY_TICK, 0.0, 0.0)])  # team 3 = Dire
        match = _match([p], [])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)  # ask for Radiant vision
        assert result == []

    def test_hero_exactly_at_range_boundary(self) -> None:
        p = _player(2, [(_DAY_TICK, 0.0, 0.0)])
        match = _match([p], [])
        result = estimate_vision(match, 2, _DAY_TICK, float(_DAY_VISION), 0.0)
        assert len(result) == 1

    def test_hero_one_unit_beyond_range(self) -> None:
        p = _player(2, [(_DAY_TICK, 0.0, 0.0)])
        match = _match([p], [])
        result = estimate_vision(match, 2, _DAY_TICK, float(_DAY_VISION + 1), 0.0)
        assert result == []

    def test_multiple_heroes_sorted_by_distance(self) -> None:
        p_far = _player(2, [(_DAY_TICK, 1500.0, 0.0)])
        p_near = _player(2, [(_DAY_TICK, 100.0, 0.0)])
        match = _match([p_far, p_near], [])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert len(result) == 2
        assert result[0].distance < result[1].distance

    def test_hero_with_no_position_log_excluded(self) -> None:
        p = _player(2, [])
        match = _match([p], [])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []


# ---------------------------------------------------------------------------
# estimate_vision — ward vision
# ---------------------------------------------------------------------------


class TestEstimateVisionWard:
    def test_live_observer_ward_provides_vision(self) -> None:
        w = _ward(team=2, x=0.0, y=0.0, tick=0)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 1000.0, 0.0)
        assert len(result) == 1
        assert result[0].kind == "ward"
        assert result[0].name == "observer_ward"
        assert result[0].vision_radius == _WARD_VISION

    def test_ward_not_yet_placed(self) -> None:
        w = _ward(team=2, x=0.0, y=0.0, tick=_DAY_TICK + 100)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_ward_already_killed(self) -> None:
        w = _ward(team=2, x=0.0, y=0.0, tick=0, killed_tick=_DAY_TICK - 1)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_ward_already_expired(self) -> None:
        w = _ward(team=2, x=0.0, y=0.0, tick=0, expires_tick=_DAY_TICK - 1)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_sentry_ward_does_not_count(self) -> None:
        w = _ward(team=2, x=0.0, y=0.0, tick=0, ward_type="sentry")
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_enemy_ward_does_not_count(self) -> None:
        w = _ward(team=3, x=0.0, y=0.0, tick=0)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_ward_outside_vision_radius(self) -> None:
        w = _ward(team=2, x=0.0, y=0.0, tick=0)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, float(_WARD_VISION + 1), 0.0)
        assert result == []

    def test_ward_with_no_coordinates_excluded(self) -> None:
        w = _ward(team=2, x=None, y=None, tick=0)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_ward_still_alive_at_query_tick(self) -> None:
        # Killed tick is in the future — ward still alive
        w = _ward(team=2, x=0.0, y=0.0, tick=0, killed_tick=_DAY_TICK + 100)
        match = _match([], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert len(result) == 1


# ---------------------------------------------------------------------------
# estimate_vision — combined hero + ward, result ordering
# ---------------------------------------------------------------------------


class TestEstimateVisionCombined:
    def test_hero_and_ward_both_returned(self) -> None:
        p = _player(2, [(_DAY_TICK, 500.0, 0.0)])
        w = _ward(team=2, x=200.0, y=0.0, tick=0)
        match = _match([p], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        kinds = {s.kind for s in result}
        assert "hero" in kinds
        assert "ward" in kinds

    def test_result_sorted_by_distance(self) -> None:
        p = _player(2, [(_DAY_TICK, 1000.0, 0.0)])
        w = _ward(team=2, x=300.0, y=0.0, tick=0)
        match = _match([p], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result[0].distance <= result[1].distance

    def test_empty_result_means_no_vision(self) -> None:
        # Hero and ward both out of range
        p = _player(2, [(_DAY_TICK, 9000.0, 0.0)])
        w = _ward(team=2, x=8000.0, y=0.0, tick=0)
        match = _match([p], [w])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []


# ---------------------------------------------------------------------------
# estimate_vision — vision modifier reveals
# ---------------------------------------------------------------------------


class TestEstimateVisionModifier:
    def test_active_modifier_reveals_enemy_hero(self) -> None:
        # Slardar on Radiant (team=2) applied Corrosive Haze to Dire hero at (500, 0).
        # Query is at (500, 0) — the revealed hero's position.
        revealed = _player(3, [(_DAY_TICK, 500.0, 0.0)])  # Dire hero
        mod = _mod(
            modifier_name="modifier_slardar_amplify_damage",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_slardar",
            caster_team=2,
            tick=0,
        )
        match = _match([revealed], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 500.0, 0.0)
        assert len(result) == 1
        assert result[0].kind == "modifier"
        assert result[0].name == "modifier_slardar_amplify_damage"
        assert result[0].vision_radius == 0

    def test_modifier_not_yet_applied(self) -> None:
        revealed = _player(3, [(_DAY_TICK, 0.0, 0.0)])
        mod = _mod(
            modifier_name="modifier_slardar_amplify_damage",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_slardar",
            caster_team=2,
            tick=_DAY_TICK + 1,  # applied in the future
        )
        match = _match([revealed], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_modifier_already_removed(self) -> None:
        revealed = _player(3, [(_DAY_TICK, 0.0, 0.0)])
        mod = _mod(
            modifier_name="modifier_slardar_amplify_damage",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_slardar",
            caster_team=2,
            tick=0,
            end_tick=_DAY_TICK - 1,  # expired before query
        )
        match = _match([revealed], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_modifier_from_wrong_team_ignored(self) -> None:
        # Dire applied a modifier — Radiant is querying their OWN vision
        revealed = _player(2, [(_DAY_TICK, 0.0, 0.0)])  # Radiant hero
        mod = _mod(
            modifier_name="modifier_bounty_hunter_track",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_bounty_hunter",
            caster_team=3,  # Dire caster
        )
        match = _match([revealed], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        # Radiant should not see a VisionSource from Dire's tracker
        assert not any(s.kind == "modifier" for s in result)

    def test_modifier_still_active_at_end_tick(self) -> None:
        # end_tick == query tick — modifier is still active at this exact tick
        revealed = _player(3, [(_DAY_TICK, 0.0, 0.0)])
        mod = _mod(
            modifier_name="modifier_item_dustofappearance",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_crystal_maiden",
            caster_team=2,
            tick=0,
            end_tick=_DAY_TICK,
        )
        match = _match([revealed], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        # end_tick < tick is the exclusion condition; end_tick == tick is still active
        assert len(result) == 1
        assert result[0].kind == "modifier"

    def test_modifier_target_hero_not_in_players(self) -> None:
        # The modifier's target_name doesn't match any player — no crash, no result
        mod = _mod(
            modifier_name="modifier_bounty_hunter_track",
            target_name="npc_dota_hero_nonexistent",
            caster_name="npc_dota_hero_bounty_hunter",
            caster_team=2,
        )
        match = _match([], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_modifier_distance_computed_from_revealed_hero_position(self) -> None:
        # Revealed hero is at (300, 0). Query is at (0, 0). Distance should be ~300.
        revealed = _player(3, [(_DAY_TICK, 300.0, 0.0)])
        mod = _mod(
            modifier_name="modifier_item_gem_of_true_sight",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_crystal_maiden",
            caster_team=2,
        )
        match = _match([revealed], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert len(result) == 1
        assert abs(result[0].distance - 300.0) < 1.0
