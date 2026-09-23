"""Offline replay regression coverage for Smoke of Deceit lifecycles."""

from __future__ import annotations

import pytest

from gem.analysis.smoke import SmokeLifecycleStatus, build_smoke_analysis
from gem.analysis.smoke_fight import SmokeFightStatus, build_smoke_fight_insights
from gem.results.models import ParsedMatch, VisibilityState


@pytest.mark.integration
@pytest.mark.slow
def test_canonical_replay_preserves_smoke_lifecycles(
    canonical_parsed_match: ParsedMatch,
) -> None:
    """Keep the fixture's known smoke activations and per-member timing stable."""
    match = canonical_parsed_match

    assert len(match.smoke_events) == 4
    assert sum(len(event.participants) for event in match.smoke_events) == 12
    assert any(
        participant.modifier_duration_s == pytest.approx(45.0)
        for event in match.smoke_events
        for participant in event.participants
    )
    assert all(
        participant.applied_tick >= event.tick
        for event in match.smoke_events
        for participant in event.participants
    )
    assert any(
        participant.applied_tick - event.tick == 82
        for event in match.smoke_events
        for participant in event.participants
    )

    analyses = build_smoke_analysis(match)
    members = [member for analysis in analyses for member in analysis.members]

    assert any(member.lifecycle_status is SmokeLifecycleStatus.EXPIRED for member in members)
    early = [member for member in members if member.lifecycle_status is SmokeLifecycleStatus.EARLY]
    assert early
    assert any(member.visibility_at_remove is VisibilityState.HIDDEN for member in early)
    assert any(member.visibility_at_remove is VisibilityState.VISIBLE for member in early)

    insights = build_smoke_fight_insights(match)
    assert [insight.status for insight in insights] == [
        SmokeFightStatus.LINKED,
        SmokeFightStatus.PREEXISTING,
        SmokeFightStatus.LINKED,
        SmokeFightStatus.TEMPORAL_ONLY,
        SmokeFightStatus.LINKED,
    ]

    first_link = insights[0]
    assert first_link.smoke_index == 0
    assert first_link.fight_index == 0
    assert first_link.activation.tick == match.smoke_events[0].tick == 19_204
    assert first_link.first_death is not None
    assert first_link.first_death.tick == match.teamfights[0].first_death_tick == 21_002
    assert len(first_link.active_smoked_player_ids) == 5
    assert len(first_link.follow_ups) == 1

    for insight in insights:
        assert insight.activation.tick == match.smoke_events[insight.smoke_index].tick
        if insight.fight_index is not None and insight.first_death is not None:
            assert (
                insight.first_death.tick == match.teamfights[insight.fight_index].first_death_tick
            )
