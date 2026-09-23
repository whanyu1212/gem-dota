"""Replay-backed factual checks for the Roshan conversion calibration corpus."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gem.analysis import AegisFateSource, RoshTeamAttributionSource
from gem.analysis.roshan import build_rosh_conversions

CORPUS_PATH = Path(__file__).parent / "fixtures" / "opendota" / "roshan_conversion_corpus.json"
DENIAL_REPLAY = CORPUS_PATH.parent / "8974053011.dem"


def _corpus() -> dict:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def test_corpus_declares_real_and_targeted_edge_case_coverage() -> None:
    corpus = _corpus()

    assert corpus["schema_version"] == 1
    assert len(corpus["matches"]) >= 6
    assert "denied Aegis" in corpus["coverage"]["real_replay"]
    assert "stolen pickup" in corpus["coverage"]["real_replay"]
    assert "fight already underway at acquisition" in corpus["coverage"]["real_replay"]
    assert "missing pickup event" in corpus["coverage"]["targeted_synthetic_tests"]
    assert "allied tower and barracks denies" in corpus["coverage"]["targeted_synthetic_tests"]


@pytest.mark.slow
@pytest.mark.integration
def test_real_denial_fixture_preserves_observed_and_inferred_lifecycle_sources() -> None:
    if not DENIAL_REPLAY.exists():
        pytest.skip(
            "Roshan denial fixture is not available; sync match 8974053011 "
            "with scripts/sync_opendota_fixtures.py"
        )

    import gem

    conversions = build_rosh_conversions(gem.parse(DENIAL_REPLAY))

    assert len(conversions) == 2
    denied, later_pickup = conversions
    assert denied.rosh_tick == 54362
    assert denied.roshan_team == 3
    assert denied.roshan_team_source is RoshTeamAttributionSource.PROTOCOL
    assert denied.conversion_team_source is RoshTeamAttributionSource.PROTOCOL
    assert denied.aegis_fate == "denied"
    assert denied.aegis_fate_source is AegisFateSource.DENIAL_EVENT
    assert denied.aegis_fate_inferred is False
    assert denied.extended_end_tick == later_pickup.rosh_tick - 1
    assert later_pickup.aegis_fate == "consumed"
    assert later_pickup.aegis_fate_source is AegisFateSource.HOLDER_DEATH_INFERENCE
    assert later_pickup.aegis_fate_inferred is True
