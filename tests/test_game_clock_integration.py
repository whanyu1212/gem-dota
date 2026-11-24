"""Offline regression coverage for the pause-aware game clock on a paused replay."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import pytest

from gem.results.models import ParsedMatch
from gem.state.game_clock import GamePause


@pytest.fixture(scope="module")
def paused_match(performance_baseline_replay_path: Path) -> ParsedMatch:
    import gem

    return gem.parse(str(performance_baseline_replay_path))


@pytest.fixture(scope="module")
def paused_reference(performance_baseline_replay_path: Path) -> dict:
    reference = performance_baseline_replay_path.with_suffix(".opendota.json")
    if not reference.exists():
        pytest.skip(f"OpenDota reference JSON not available: {reference.name}")
    return json.loads(reference.read_text())


@pytest.mark.integration
@pytest.mark.slow
def test_replay_records_pauses_and_post_game(paused_match: ParsedMatch) -> None:
    """Match 9098298585 pauses before the horn and twice in game, and records ~15 min
    after the Ancient falls."""
    clock = paused_match.game_clock
    assert clock is not None
    assert clock.pauses == [
        GamePause(start_tick=24239, end_tick=25495),
        GamePause(start_tick=52245, end_tick=52764),
        GamePause(start_tick=98223, end_tick=98385),
    ]
    assert clock.net_tick_offset == 1746

    post_game_tick = paused_match.post_game_tick
    assert post_game_tick is not None
    assert paused_match.game_end_tick - post_game_tick > 15 * 60 * 30
    post_game_seconds = clock.game_seconds_at(post_game_tick)
    assert post_game_seconds is not None
    assert abs(post_game_seconds - paused_match.duration) <= 1


@pytest.mark.integration
@pytest.mark.slow
def test_objective_times_match_opendota(paused_match: ParsedMatch, paused_reference: dict) -> None:
    """Pause-aware objective times agree with OpenDota; raw ticks drift by each pause."""
    reference: defaultdict[tuple[str, str | None], list[int]] = defaultdict(list)
    for objective in paused_reference["objectives"]:
        key = objective.get("key") if objective["type"] == "building_kill" else None
        reference[(objective["type"], key)].append(objective["time"])

    compared = 0
    for objective in paused_match.objectives:
        if objective["type"] not in {
            "building_kill",
            "CHAT_MESSAGE_ROSHAN_KILL",
            "CHAT_MESSAGE_MINIBOSS_KILL",
        }:
            continue
        key = objective.get("key") if objective["type"] == "building_kill" else None
        candidates = reference.get((objective["type"], key))
        if not candidates:
            continue
        delta = min(abs(objective["time"] - time) for time in candidates)
        if objective["type"] == "building_kill":
            assert delta == 0, objective
        else:
            # Chat-message events can land on a half-second rounding boundary.
            assert delta <= 1, objective
        compared += 1
    assert compared >= 20


@pytest.mark.corpus
@pytest.mark.slow
def test_ward_left_times_match_opendota(paused_match: ParsedMatch, paused_reference: dict) -> None:
    """Ward removal timestamps stay aligned with OpenDota across multiple pauses."""
    for player_gem, player_od in zip(
        paused_match.players, paused_reference["players"], strict=True
    ):
        for key in ("obs_left_log", "sen_left_log"):
            gem_times = [entry["time"] for entry in getattr(player_gem, key)]
            od_times = [entry["time"] for entry in player_od[key]]
            assert gem_times == od_times, (player_gem.player_id, key)
