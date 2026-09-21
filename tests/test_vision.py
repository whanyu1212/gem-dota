"""Tests for point-vision geometry, authoritative state, and target reveals."""

from __future__ import annotations

from typing import Literal
from unittest.mock import MagicMock

import pytest

import gem
from gem.analysis import (
    PointVisionStatus,
    assess_point_vision,
    estimate_vision,
    is_daytime,
)
from gem.extractors.wards import WardEvent
from gem.results.models import (
    HeroVisibilityEvent,
    VisibilityState,
    VisionModifierCloseEvidence,
    VisionModifierEvent,
    VisionModifierLifecycleStatus,
    VisionModifierPairingStatus,
    VisionModifierSemantic,
)

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
    x: float | None,
    y: float | None,
    tick: int = 0,
    killed_tick: int | None = None,
    expires_tick: int | None = None,
    ward_type: Literal["observer", "sentry"] = "observer",
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
    end_tick: int | None = 30000,
    add_modifier_duration_s: float | None = 600.0,
    semantic: VisionModifierSemantic = VisionModifierSemantic.DIRECT_TARGET_REVEAL,
    target_is_hero: bool = True,
    target_is_illusion: bool = False,
    target_team: int = 0,
    lifecycle_status: VisionModifierLifecycleStatus = VisionModifierLifecycleStatus.REMOVED,
    close_evidence: VisionModifierCloseEvidence = VisionModifierCloseEvidence.OBSERVED,
    pairing_status: VisionModifierPairingStatus = VisionModifierPairingStatus.EXACT,
) -> VisionModifierEvent:
    return VisionModifierEvent(
        tick=tick,
        end_tick=end_tick,
        modifier_name=modifier_name,
        target_name=target_name,
        caster_name=caster_name,
        caster_team=caster_team,
        add_modifier_duration_s=add_modifier_duration_s,
        semantic=semantic,
        target_is_hero=target_is_hero,
        target_is_illusion=target_is_illusion,
        target_team=target_team,
        lifecycle_status=lifecycle_status,
        close_evidence=close_evidence,
        pairing_status=pairing_status,
    )


def _match(
    players: list,
    wards: list,
    game_start_tick: int = 0,
    game_end_tick: int = 30_000,
    vision_modifiers: list | None = None,
) -> MagicMock:
    m = MagicMock()
    m.players = players
    m.wards = wards
    m.game_start_tick = game_start_tick
    m.game_end_tick = game_end_tick
    m.vision_modifiers = vision_modifiers or []
    m.hero_visibility_events = []
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
        assert result[0].position_tick == _DAY_TICK
        assert result[0].position_age_ticks == 0
        assert result[0].position_provenance == "sampled_player_position"

    def test_allied_hero_outside_day_range(self) -> None:
        p = _player(2, [(_DAY_TICK, 0.0, 0.0)])
        match = _match([p], [])
        result = estimate_vision(match, 2, _DAY_TICK, 2000.0, 0.0)
        assert result == []

    def test_night_uses_reduced_radius(self) -> None:
        # Hero at (0,0), query at (1000, 0) — within day range but not night range
        p = _player(2, [(_DAY_TICK, 0.0, 0.0), (_NIGHT_TICK, 0.0, 0.0)])
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
# Direct-target reveals stay separate from estimate_vision geometry
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
        assert estimate_vision(match, 2, _DAY_TICK, 500.0, 0.0) == []

        assessment = assess_point_vision(
            match,
            2,
            _DAY_TICK,
            500.0,
            0.0,
            target_player_id=revealed.player_id,
        )
        assert assessment.status is PointVisionStatus.INCOMPLETE
        assert assessment.sources == []
        assert assessment.direct_target_reveals[0].modifier_name == (
            "modifier_slardar_amplify_damage"
        )

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

    def test_modifier_is_inactive_at_end_tick(self) -> None:
        # Removal bounds a half-open interval: [application, removal).
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
        assessment = assess_point_vision(
            match,
            2,
            _DAY_TICK,
            0.0,
            0.0,
            target_player_id=revealed.player_id,
        )
        assert assessment.direct_target_reveals == []

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

    def test_gem_carrier_is_not_treated_as_direct_reveal(self) -> None:
        revealed = _player(3, [(_DAY_TICK, 300.0, 0.0)])
        mod = _mod(
            modifier_name="modifier_item_gem_of_true_sight",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_crystal_maiden",
            caster_team=2,
            semantic=VisionModifierSemantic.AURA_CARRIER,
        )
        match = _match([revealed], [], vision_modifiers=[mod])
        result = estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0)
        assert result == []

    def test_unbounded_open_modifier_is_not_active_forever(self) -> None:
        revealed = _player(3, [(_DAY_TICK, 0.0, 0.0)])
        mod = _mod(
            modifier_name="modifier_bounty_hunter_track",
            target_name=revealed.hero_name,
            caster_name="npc_dota_hero_bounty_hunter",
            caster_team=2,
            end_tick=None,
            add_modifier_duration_s=None,
        )

        assert (
            estimate_vision(
                _match([revealed], [], vision_modifiers=[mod]),
                2,
                _DAY_TICK,
                0.0,
                0.0,
            )
            == []
        )

    def test_incomplete_nonhero_or_illusion_direct_reveal_is_ignored(self) -> None:
        revealed = _player(3, [(_DAY_TICK, 0.0, 0.0)])
        common = {
            "modifier_name": "modifier_slardar_amplify_damage",
            "target_name": revealed.hero_name,
            "caster_name": "npc_dota_hero_slardar",
            "caster_team": 2,
        }
        incomplete = _mod(
            **common,
            lifecycle_status=VisionModifierLifecycleStatus.INCOMPLETE,
            pairing_status=VisionModifierPairingStatus.AMBIGUOUS,
        )
        nonhero = _mod(**common, target_is_hero=False)
        illusion = _mod(**common, target_is_illusion=True)

        match = _match([revealed], [], vision_modifiers=[incomplete, nonhero, illusion])
        assert estimate_vision(match, 2, _DAY_TICK, 0.0, 0.0) == []


# ---------------------------------------------------------------------------
# assess_point_vision — structured evidence contract
# ---------------------------------------------------------------------------


class TestAssessPointVision:
    def test_fresh_hero_support_and_provenance(self) -> None:
        player = _player(2, [(_DAY_TICK - 30, 0.0, 0.0)])

        result = assess_point_vision(_match([player], []), 2, _DAY_TICK, 100.0, 0.0)

        assert result.status is PointVisionStatus.SUPPORTED
        assert result.gaps == []
        assert result.sources[0].kind == "hero"
        assert result.sources[0].position_tick == _DAY_TICK - 30
        assert result.sources[0].position_age_ticks == 30
        assert result.sources[0].position_provenance == "sampled_player_position"

    def test_fresh_out_of_range_is_unsupported_not_hidden(self) -> None:
        player = _player(2, [(_DAY_TICK, 0.0, 0.0)])

        result = assess_point_vision(_match([player], []), 2, _DAY_TICK, 5_000.0, 0.0)

        assert result.status is PointVisionStatus.UNSUPPORTED
        assert result.sources == []
        assert result.gaps == []

    def test_missing_and_stale_allied_positions_are_incomplete(self) -> None:
        missing = _player(2, [])
        stale = _player(2, [(_DAY_TICK - 151, 0.0, 0.0)])
        stale.hero_name = "npc_dota_hero_bane"

        result = assess_point_vision(_match([missing, stale], []), 2, _DAY_TICK, 0.0, 0.0)

        assert result.status is PointVisionStatus.INCOMPLETE
        assert {gap.code for gap in result.gaps} == {
            "allied_hero_position_missing",
            "allied_hero_position_stale",
        }

    def test_position_age_bound_is_configurable(self) -> None:
        player = _player(2, [(_DAY_TICK - 151, 0.0, 0.0)])

        default = assess_point_vision(_match([player], []), 2, _DAY_TICK, 0.0, 0.0)
        relaxed = assess_point_vision(
            _match([player], []),
            2,
            _DAY_TICK,
            0.0,
            0.0,
            max_position_age_ticks=151,
        )

        assert default.status is PointVisionStatus.INCOMPLETE
        assert relaxed.status is PointVisionStatus.SUPPORTED

    def test_supported_status_retains_other_source_gaps(self) -> None:
        fresh = _player(2, [(_DAY_TICK, 0.0, 0.0)])
        missing = _player(2, [])
        missing.hero_name = "npc_dota_hero_bane"

        result = assess_point_vision(_match([fresh, missing], []), 2, _DAY_TICK, 0.0, 0.0)

        assert result.status is PointVisionStatus.SUPPORTED
        assert [gap.code for gap in result.gaps] == ["allied_hero_position_missing"]

    def test_empty_allied_roster_is_incomplete(self) -> None:
        result = assess_point_vision(_match([], []), 2, _DAY_TICK, 0.0, 0.0)

        assert result.status is PointVisionStatus.INCOMPLETE
        assert result.gaps[0].code == "allied_roster_empty"

    def test_ward_interval_is_half_open_and_sentries_do_not_source(self) -> None:
        placement = 100
        removal = 200
        observer = _ward(2, 0.0, 0.0, tick=placement, killed_tick=removal)
        sentry = _ward(2, 0.0, 0.0, tick=placement, ward_type="sentry")
        match = _match([], [observer, sentry])

        at_placement = assess_point_vision(match, 2, placement, 0.0, 0.0)
        at_removal = assess_point_vision(match, 2, removal, 0.0, 0.0)

        assert [source.kind for source in at_placement.sources] == ["observer_ward"]
        assert at_placement.sources[0].position_tick == placement
        assert at_placement.sources[0].position_age_ticks is None
        assert at_removal.sources == []

    def test_ward_uses_earliest_kill_or_expiry_boundary(self) -> None:
        ward = _ward(2, 0.0, 0.0, killed_tick=300, expires_tick=200)

        result = assess_point_vision(_match([], [ward]), 2, 250, 0.0, 0.0)

        assert result.sources == []

    def test_live_allied_ward_missing_coordinates_is_a_gap(self) -> None:
        ward = _ward(2, None, None, killed_tick=_DAY_TICK + 1)

        result = assess_point_vision(_match([], [ward]), 2, _DAY_TICK, 0.0, 0.0)

        assert "observer_ward_position_missing" in {gap.code for gap in result.gaps}

    def test_live_unknown_team_observer_is_a_gap(self) -> None:
        ward = _ward(0, 0.0, 0.0, killed_tick=_DAY_TICK + 1)

        result = assess_point_vision(_match([], [ward]), 2, _DAY_TICK, 0.0, 0.0)

        assert "observer_ward_team_unknown" in {gap.code for gap in result.gaps}

    def test_open_ward_requires_known_query_horizon(self) -> None:
        ward = _ward(2, 0.0, 0.0)
        unknown = assess_point_vision(_match([], [ward], game_end_tick=0), 2, _DAY_TICK, 0.0, 0.0)
        beyond = assess_point_vision(
            _match([], [ward], game_end_tick=_DAY_TICK - 1), 2, _DAY_TICK, 0.0, 0.0
        )
        observed = assess_point_vision(
            _match([], [ward], game_end_tick=_DAY_TICK), 2, _DAY_TICK, 0.0, 0.0
        )

        assert "observer_ward_lifetime_unknown" in {gap.code for gap in unknown.gaps}
        assert "observer_ward_lifetime_unknown" in {gap.code for gap in beyond.gaps}
        assert [source.kind for source in observed.sources] == ["observer_ward"]

    def test_direct_reveal_is_target_specific_not_point_support(self) -> None:
        target = _player(3, [(_DAY_TICK, 0.0, 0.0)])
        target.player_id = 5
        target.hero_name = "npc_dota_hero_bane"
        modifier = _mod(
            modifier_name="modifier_slardar_amplify_damage",
            target_name=target.hero_name,
            caster_name="npc_dota_hero_slardar",
            caster_team=2,
        )

        result = assess_point_vision(
            _match([target], [], vision_modifiers=[modifier]),
            2,
            _DAY_TICK,
            99_999.0,
            99_999.0,
            target_player_id=target.player_id,
        )

        assert result.sources == []
        assert len(result.direct_target_reveals) == 1
        assert result.direct_target_reveals[0].target_player_id == 5
        reveal_payload = gem.to_dict(result)["direct_target_reveals"][0]
        assert reveal_payload["start_tick"] == modifier.tick
        assert "tick" not in reveal_payload

    @pytest.mark.parametrize(
        ("event_changes", "gap_code"),
        [
            (
                {"lifecycle_status": VisionModifierLifecycleStatus.INCOMPLETE},
                "direct_target_reveal_incomplete",
            ),
            (
                {"pairing_status": VisionModifierPairingStatus.AMBIGUOUS},
                "direct_target_reveal_ambiguous",
            ),
            ({"end_tick": None}, "direct_target_reveal_unbounded"),
            (
                {"close_evidence": VisionModifierCloseEvidence.DURATION_INFERRED},
                "direct_target_reveal_unbounded",
            ),
        ],
    )
    def test_unusable_matching_direct_reveal_creates_gap(
        self, event_changes: dict, gap_code: str
    ) -> None:
        target = _player(3, [])
        target.player_id = 5
        target.hero_name = "npc_dota_hero_bane"
        ally = _player(2, [(_DAY_TICK, 5_000.0, 0.0)])
        modifier = _mod(
            modifier_name="modifier_bounty_hunter_track",
            target_name=target.hero_name,
            caster_name="npc_dota_hero_bounty_hunter",
            caster_team=2,
            **event_changes,
        )

        result = assess_point_vision(
            _match([ally, target], [], vision_modifiers=[modifier]),
            2,
            _DAY_TICK,
            0.0,
            0.0,
            target_player_id=5,
        )

        assert gap_code in {gap.code for gap in result.gaps}
        assert result.direct_target_reveals == []
        assert result.status is PointVisionStatus.UNSUPPORTED

    def test_duplicate_target_hero_name_prevents_reveal_attribution(self) -> None:
        target = _player(3, [])
        target.player_id = 5
        target.hero_name = "npc_dota_hero_bane"
        duplicate = _player(3, [])
        duplicate.player_id = 6
        duplicate.hero_name = target.hero_name
        modifier = _mod(
            modifier_name="modifier_bounty_hunter_track",
            target_name=target.hero_name,
            caster_name="npc_dota_hero_bounty_hunter",
            caster_team=2,
            target_team=3,
        )

        result = assess_point_vision(
            _match([target, duplicate], [], vision_modifiers=[modifier]),
            2,
            _DAY_TICK,
            0.0,
            0.0,
            target_player_id=target.player_id,
        )

        assert result.authoritative_applicable is True
        assert result.direct_target_reveals == []
        assert "target_identity_ambiguous" in {gap.code for gap in result.gaps}

    def test_conflicting_modifier_target_team_prevents_reveal_attribution(self) -> None:
        target = _player(3, [])
        target.player_id = 5
        target.hero_name = "npc_dota_hero_bane"
        modifier = _mod(
            modifier_name="modifier_slardar_amplify_damage",
            target_name=target.hero_name,
            caster_name="npc_dota_hero_slardar",
            caster_team=2,
            target_team=2,
        )

        result = assess_point_vision(
            _match([target], [], vision_modifiers=[modifier]),
            2,
            _DAY_TICK,
            0.0,
            0.0,
            target_player_id=target.player_id,
        )

        assert result.direct_target_reveals == []
        assert "direct_target_reveal_target_team_conflict" in {gap.code for gap in result.gaps}

    @pytest.mark.parametrize(
        ("target_team", "gap_code"),
        [
            (0, "target_team_unknown"),
            (2, "direct_target_reveal_target_team_conflict"),
        ],
    )
    def test_target_team_must_be_known_opponent(self, target_team: int, gap_code: str) -> None:
        target = _player(target_team, [])
        target.player_id = 5
        target.hero_name = "npc_dota_hero_bane"
        modifier = _mod(
            modifier_name="modifier_slardar_amplify_damage",
            target_name=target.hero_name,
            caster_name="npc_dota_hero_slardar",
            caster_team=2,
        )

        result = assess_point_vision(
            _match([target], [], vision_modifiers=[modifier]),
            2,
            _DAY_TICK,
            0.0,
            0.0,
            target_player_id=target.player_id,
        )

        assert result.authoritative_applicable is True
        assert result.direct_target_reveals == []
        assert gap_code in {gap.code for gap in result.gaps}

    def test_ended_modifier_does_not_add_current_evidence_gap(self) -> None:
        target = _player(3, [])
        target.player_id = 5
        target.hero_name = "npc_dota_hero_bane"
        historical = _mod(
            modifier_name="modifier_bounty_hunter_track",
            target_name=target.hero_name,
            caster_name="npc_dota_hero_bounty_hunter",
            caster_team=0,
            tick=0,
            end_tick=_DAY_TICK,
            lifecycle_status=VisionModifierLifecycleStatus.INCOMPLETE,
        )

        result = assess_point_vision(
            _match([target], [], vision_modifiers=[historical]),
            2,
            _DAY_TICK,
            0.0,
            0.0,
            target_player_id=target.player_id,
        )

        assert result.direct_target_reveals == []
        assert not any(gap.code.startswith("direct_target_reveal") for gap in result.gaps)

    @pytest.mark.parametrize(
        ("state", "expected"),
        [
            (VisibilityState.VISIBLE, VisibilityState.VISIBLE),
            (VisibilityState.HIDDEN, VisibilityState.HIDDEN),
            (VisibilityState.UNKNOWN, VisibilityState.UNKNOWN),
        ],
    )
    def test_authoritative_target_visibility_is_separate(
        self, state: VisibilityState, expected: VisibilityState
    ) -> None:
        target = _player(3, [])
        target.player_id = 5
        target.hero_name = "npc_dota_hero_bane"
        match = _match([target], [])
        match.hero_visibility_events = [
            HeroVisibilityEvent(
                tick=_DAY_TICK,
                player_id=5,
                hero_name=target.hero_name,
                entity_index=7,
                entity_serial=1,
                radiant_state=state,
                dire_state=VisibilityState.UNKNOWN,
            )
        ]

        result = assess_point_vision(
            match, 2, _DAY_TICK, 0.0, 0.0, target_player_id=target.player_id
        )

        assert result.authoritative_applicable is True
        assert result.authoritative_visibility is expected

    def test_unknown_target_is_not_authoritatively_applicable(self) -> None:
        ally = _player(2, [(_DAY_TICK, 5_000.0, 0.0)])
        result = assess_point_vision(
            _match([ally], []), 2, _DAY_TICK, 0.0, 0.0, target_player_id=99
        )

        assert result.authoritative_applicable is False
        assert result.authoritative_visibility is VisibilityState.UNKNOWN
        assert result.status is PointVisionStatus.UNSUPPORTED
        assert result.gaps == [
            gem.PointVisionGap(code="target_player_missing", subject="player:99")
        ]

    def test_validation(self) -> None:
        with pytest.raises(ValueError, match="team"):
            assess_point_vision(_match([], []), 1, 0, 0.0, 0.0)
        with pytest.raises(ValueError, match="nonnegative"):
            assess_point_vision(_match([], []), 2, 0, 0.0, 0.0, max_position_age_ticks=-1)

    def test_public_exports_and_generic_serialization(self) -> None:
        result = assess_point_vision(
            _match([_player(2, [(_DAY_TICK, 0.0, 0.0)])], []),
            2,
            _DAY_TICK,
            0.0,
            0.0,
        )

        assert gem.assess_point_vision is assess_point_vision
        assert gem.PointVisionStatus is PointVisionStatus
        assert "PointVisionAssessment" in gem.__all__
        payload = gem.to_dict(result)
        assert payload["status"] == "supported"
        assert payload["sources"][0]["name"].startswith("npc_dota_hero_")
        assert payload["sources"][0]["vision_radius"] == _DAY_VISION
        assert payload["sources"][0]["position_tick"] == _DAY_TICK
