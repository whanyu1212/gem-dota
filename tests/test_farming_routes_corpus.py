"""Replay-backed factual checks for the farming-route regression corpus."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_farming_routes import summarize_match

CORPUS_PATH = Path(__file__).parent / "fixtures" / "opendota" / "farming_routes_corpus.json"
MANIFEST_PATH = CORPUS_PATH.parent / "manifest.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_corpus_uses_active_real_replays_and_declares_targeted_gaps() -> None:
    corpus = _load(CORPUS_PATH)
    manifest = _load(MANIFEST_PATH)
    active_ids = {entry["match_id"] for entry in manifest["matches"] if entry["status"] == "active"}
    match_ids = [entry["match_id"] for entry in corpus["matches"]]

    assert corpus["schema_version"] == 1
    assert len(match_ids) >= 7
    assert len(match_ids) == len(set(match_ids))
    assert set(match_ids) <= active_ids
    assert "early, mid, and late segments" in corpus["coverage"]["real_replay"]
    assert "enemy-side and triangle segments" in corpus["coverage"]["real_replay"]
    assert "teleport and large-jump boundaries" in corpus["coverage"]["targeted_synthetic_tests"]
    assert "subjective route quality labels" in corpus["coverage"]["non_goals"]


def test_corpus_spans_route_strength_phase_and_topology() -> None:
    matches = _load(CORPUS_PATH)["matches"]

    assert {key for entry in matches for key in entry["evidence_strength_counts"]} == {
        "strong_farm_evidence",
        "weak_farm_evidence",
        "transit_like",
    }
    assert {key for entry in matches for key in entry["phase_counts"]} == {
        "early",
        "mid",
        "late",
    }
    assert {key for entry in matches for key in entry["camp_area_counts"]} == {
        "jungle",
        "triangle",
        "river",
        "flooded",
    }
    assert not any(key.startswith("context_") for entry in matches for key in entry)


@pytest.mark.slow
@pytest.mark.integration
def test_canonical_replay_matches_committed_factual_summary(
    canonical_parsed_match,
) -> None:
    corpus = _load(CORPUS_PATH)
    expected = next(
        entry for entry in corpus["matches"] if entry["match_id"] == canonical_parsed_match.match_id
    )

    assert summarize_match(canonical_parsed_match) == expected
