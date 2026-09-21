"""Offline integration coverage for evidence-aware point vision."""

from __future__ import annotations

import pytest

from gem.analysis import PointVisionStatus, assess_point_vision
from gem.results.models import ParsedMatch


@pytest.mark.integration
@pytest.mark.slow
def test_exact_player_sample_supports_point_with_provenance(
    canonical_parsed_match: ParsedMatch,
) -> None:
    player = next(
        player
        for player in canonical_parsed_match.players
        if player.team in (2, 3) and player.hero_name and player.position_log
    )
    tick, x, y = player.position_log[len(player.position_log) // 2]

    result = assess_point_vision(
        canonical_parsed_match,
        player.team,
        tick,
        x,
        y,
        target_player_id=player.player_id,
    )

    own_source = next(
        source
        for source in result.sources
        if source.kind == "hero" and source.player_id == player.player_id
    )
    assert result.status is PointVisionStatus.SUPPORTED
    assert own_source.position_tick == tick
    assert own_source.position_age_ticks == 0
    assert result.authoritative_applicable is True
