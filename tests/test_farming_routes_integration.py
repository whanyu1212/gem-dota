"""Offline replay regression coverage for evidence-first farming routes."""

from __future__ import annotations

import pytest

from gem.analysis import FarmingEvidenceStrength, build_farming_routes
from gem.results.models import ParsedMatch


@pytest.mark.integration
@pytest.mark.slow
def test_canonical_replay_farming_routes_are_stable_and_evidence_mixed(
    canonical_parsed_match: ParsedMatch,
) -> None:
    routes = build_farming_routes(canonical_parsed_match)
    segments = [segment for route in routes for segment in route.segments]

    assert len(routes) == 10
    assert sum(len(route.points) for route in routes) == 11_430
    assert len(segments) == 294
    assert all(route.status == "complete" for route in routes)
    assert all(route.camp_catalog_version == 1 for route in routes)
    assert all(route.camp_map_patch == "7.40" for route in routes)
    assert {
        strength: sum(segment.evidence_strength is strength for segment in segments)
        for strength in FarmingEvidenceStrength
    } == {
        FarmingEvidenceStrength.TRANSIT_LIKE: 143,
        FarmingEvidenceStrength.WEAK: 97,
        FarmingEvidenceStrength.STRONG: 54,
    }
    assert any(segment.neutral_kills > 0 for segment in segments)
    assert any(segment.micro_exit_merged for segment in segments)
