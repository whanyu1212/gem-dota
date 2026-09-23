"""Replay-backed factual checks for the farming-context calibration corpus."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pytest

from gem.analysis import DEFAULT_FARMING_CONTEXT_CONFIG
from scripts.calibrate_farming_context import summarize_match

CORPUS_PATH = Path(__file__).parent / "fixtures" / "opendota" / "farming_context_corpus.json"
MANIFEST_PATH = CORPUS_PATH.parent / "manifest.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_corpus_uses_active_real_replays_and_declares_targeted_gaps() -> None:
    corpus = _load(CORPUS_PATH)
    manifest = _load(MANIFEST_PATH)
    active_ids = {entry["match_id"] for entry in manifest["matches"] if entry["status"] == "active"}
    match_ids = [entry["match_id"] for entry in corpus["matches"]]

    assert corpus["schema_version"] == 1
    assert corpus["config"] == asdict(DEFAULT_FARMING_CONTEXT_CONFIG)
    assert len(match_ids) >= 7
    assert len(match_ids) == len(set(match_ids))
    assert set(match_ids) <= active_ids
    assert "early, mid, and late segments" in corpus["coverage"]["real_replay"]
    assert "enemy-side and triangle segments" in corpus["coverage"]["real_replay"]
    assert "active enemy Aegis windows" in corpus["coverage"]["real_replay"]
    assert "incomplete comparative inputs" in corpus["coverage"]["targeted_synthetic_tests"]
    assert "teleport and large-jump boundaries" in corpus["coverage"]["targeted_synthetic_tests"]
    assert "subjective route quality labels" in corpus["coverage"]["non_goals"]


def test_corpus_spans_route_strength_phase_topology_and_context_tags() -> None:
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
    observed_tags = {key for entry in matches for key in entry["context_tag_counts"]}
    assert {
        "own_side",
        "enemy_side",
        "border",
        "high_enemy_presence",
        "vision_disadvantage",
        "tower_disadvantage",
        "enemy_aegis_active",
        "territorial_advance",
    } <= observed_tags


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
