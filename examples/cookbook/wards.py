"""Where did each team ward, how long did the wards last, and what could they see?

Every ward (``match.wards``) with its exact position, when it went up and how it
ended (killed, and by whom, or expired), and its map region (``gem.region_of``).
Then two summaries:

- how long observers lasted, by team and region, and how many were killed;
- how much of each team's observer coverage the replay confirms. gem draws an
  observer's vision as a flat 1,600-unit circle (``OBSERVER_VISION_RADIUS``);
  the game's real vision is cut by cliffs and trees. For every second an enemy
  hero stood inside a live observer circle, the replay's own visibility
  (``gem.hero_visibility_at``) says whether the warding team could see them.

    python examples/cookbook/wards.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import bisect
import math
import sys
from collections import defaultdict

import pandas as pd

import gem
from gem.analysis.vision import OBSERVER_VISION_RADIUS

TEAMS = {2: "radiant", 3: "dire"}
WARD_COLUMNS = [
    "match_id", "team", "type", "placer", "placed", "placed_s", "ended_s",
    "lasted_s", "how", "killer", "region", "side", "x", "y", "placed_tick", "end_tick",
]  # fmt: skip
SAMPLE_COLUMNS = ["match_id", "team", "hero", "tick", "distance", "state"]
STATES = ["visible", "hidden", "unknown", "smoked"]


def ward_table(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return one row per placed ward: who, where, when, and how it ended.

    A ward is up from its placement tick until it was killed or expired (half
    open: it is gone on that tick). ``how`` is ``killed``, ``expired``, or
    ``up at the end`` when the recording ended first. Times are in-game seconds,
    pauses excluded.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame with one row per ward that has a position.
    """
    clock = match.game_clock
    heroes = {player.player_id: player.hero_name for player in match.players}
    end_of_recording = match.post_game_tick or match.game_end_tick
    rows = []
    for ward in match.wards:
        if ward.x is None or ward.y is None or ward.team not in TEAMS:
            continue
        if ward.killed_tick is not None:
            end_tick, how = ward.killed_tick, "killed"
        elif ward.expires_tick is not None:
            end_tick, how = ward.expires_tick, "expired"
        else:
            end_tick, how = end_of_recording, "up at the end"
        region = gem.region_of(ward.x, ward.y)
        placed_s = clock.game_time_at(ward.tick) if clock else None
        ended_s = clock.game_time_at(end_tick) if clock and end_tick is not None else None
        rows.append(
            {
                "match_id": match.match_id,
                "team": TEAMS[ward.team],
                "type": ward.ward_type,
                # The player's hero, joined on the player slot.
                "placer": heroes.get(ward.player_id, ward.placer),
                "placed": clock.format_tick(ward.tick) if clock else str(ward.tick),
                "placed_s": placed_s,
                "ended_s": ended_s,
                "lasted_s": None if placed_s is None or ended_s is None else ended_s - placed_s,
                "how": how,
                "killer": ward.killer if how == "killed" else "",
                "region": region,
                "side": _side(TEAMS[ward.team], region),
                "x": ward.x,
                "y": ward.y,
                "placed_tick": ward.tick,
                "end_tick": end_tick,
            }
        )
    return pd.DataFrame(rows, columns=WARD_COLUMNS)


def _side(team: str, region: str) -> str:
    """The region as the warding team sees it: its own half, the enemy's, or the river."""
    if region.endswith("_half"):
        return "own half" if region == f"{team}_half" else "enemy half"
    return "river"  # the river and its lotus pools


def observer_lifetimes(wards: pd.DataFrame) -> pd.DataFrame:
    """Return how long observers lasted and how many were killed, by team and side of the map."""
    observers = wards[(wards["type"] == "observer") & wards["lasted_s"].notna()]
    return (
        observers.groupby(["team", "side"])
        .agg(
            placed=("lasted_s", "size"),
            median_lasted_s=("lasted_s", "median"),
            killed=("how", lambda how: int((how == "killed").sum())),
        )
        .reset_index()
    )


def _states(match: gem.ParsedMatch) -> dict[int, tuple[list[int], list[object]]]:
    """Each player's visibility events, sorted by tick, for bisecting.

    Equivalent to ``gem.hero_visibility_at``: the last event at or before a
    tick wins, and on one tick the later event in the list.
    """
    events: dict[int, list] = defaultdict(list)
    for event in match.hero_visibility_events:
        events[event.player_id].append(event)
    lookup = {}
    for player_id, rows in events.items():
        rows.sort(key=lambda event: event.tick)  # stable: same-tick order kept
        lookup[player_id] = ([event.tick for event in rows], rows)
    return lookup


def visibility_at(
    lookup: dict[int, tuple[list[int], list]], player_id: int, team: int, tick: int
) -> str:
    """Return ``visible``, ``hidden`` or ``unknown``: the team's view of the hero at the tick."""
    ticks, rows = lookup.get(player_id, ([], []))
    i = bisect.bisect_right(ticks, tick)
    if i == 0:
        return "unknown"
    event = rows[i - 1]
    state = event.radiant_state if team == 2 else event.dire_state
    return gem.VisibilityState(state).value


def circle_samples(match: gem.ParsedMatch, wards: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return every second an enemy hero stood inside one of a team's live observer circles.

    Each row is one of the enemy hero's position samples (``position_log``,
    about one a second) while it was alive and within ``OBSERVER_VISION_RADIUS``
    of at least one of the warding team's live observers, with the distance to
    the nearest one. ``state`` is the replay's visibility of the hero for the
    warding team then: ``visible``, ``hidden`` or ``unknown``; or ``smoked``
    under Smoke of Deceit, which hides a hero from wards whatever the terrain.

    Args:
        match: A parsed match.
        wards: ``ward_table(match)``, if already built.

    Returns:
        One row per sample: ``match_id``, ``team`` (the warding team), ``hero``,
        ``tick``, ``distance`` (world units) and ``state``.
    """
    wards = ward_table(match) if wards is None else wards
    observers = wards[wards["type"] == "observer"]
    lookup = _states(match)
    smoked: dict[int, list[tuple[int, int]]] = defaultdict(list)
    end = match.post_game_tick or match.game_end_tick or 0
    for smoke in gem.build_smoke_analysis(match):
        for member in smoke.members:
            if member.player_id is not None:
                smoked[member.player_id].append((member.applied_tick, member.removed_tick or end))
    rows = []
    for team_id, team in TEAMS.items():
        circles = observers[observers["team"] == team][["x", "y", "placed_tick", "end_tick"]]
        live = [tuple(row) for row in circles.itertuples(index=False)]
        for player in match.players:
            if player.team == team_id or player.team not in TEAMS:
                continue
            hp = dict(zip(player.times, player.hp_t, strict=False))
            for tick, x, y in player.position_log:
                if hp.get(tick, 1) <= 0:
                    continue  # dead: hidden whatever the wards
                distance = min(
                    (
                        math.dist((x, y), (wx, wy))
                        for wx, wy, start, stop in live
                        if start <= tick < stop
                    ),
                    default=math.inf,
                )
                if distance > OBSERVER_VISION_RADIUS:
                    continue
                if any(start <= tick < stop for start, stop in smoked[player.player_id]):
                    state = "smoked"
                else:
                    state = visibility_at(lookup, player.player_id, team_id, tick)
                rows.append(
                    {
                        "match_id": match.match_id,
                        "team": team,
                        "hero": player.hero_name,
                        "tick": tick,
                        "distance": distance,
                        "state": state,
                    }
                )
    return pd.DataFrame(rows, columns=SAMPLE_COLUMNS)


def circle_summary(samples: pd.DataFrame) -> pd.DataFrame:
    """Count each warding team's samples by state: the seconds enemies spent in its circles."""
    counts = samples.pivot_table(
        index=["match_id", "team"], columns="state", aggfunc="size", fill_value=0
    )
    counts = counts.reindex(columns=STATES, fill_value=0).reset_index()
    counts.columns.name = None
    counts.insert(2, "seconds", counts[["visible", "hidden", "unknown"]].sum(axis=1))
    return counts


def by_distance(samples: pd.DataFrame, step: int = 400) -> pd.DataFrame:
    """Return the share of unsmoked seconds the warding team saw the hero, by distance from the ward."""
    seen = samples[samples["state"].isin(["visible", "hidden"])]
    band = (seen["distance"] // step * step).astype(int)
    table = seen.groupby(band)["state"].agg(
        seconds="size", visible=lambda s: int((s == "visible").sum())
    )
    table.index = [f"{lo}-{lo + step}" for lo in table.index]
    table["visible_pct"] = (100 * table["visible"] / table["seconds"]).round(1)
    return table.rename_axis("distance").reset_index()


def main(paths: list[str]) -> None:
    """Print the wards, observer lifetimes by region, and the circle check."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    wards = [ward_table(match) for match in matches]
    table = pd.concat(wards, ignore_index=True)
    if table.empty:
        print("No wards in these replays.")
        return
    shown = ["match_id", "team", "type", "placer", "placed", "lasted_s", "how", "killer", "region"]
    print(table[shown].round({"lasted_s": 0}).to_string(index=False))

    print("\nObservers by team and side of the map:")
    print(observer_lifetimes(table).round({"median_lasted_s": 0}).to_string(index=False))

    samples = pd.concat(
        [circle_samples(match, w) for match, w in zip(matches, wards, strict=True)],
        ignore_index=True,
    )
    print("\nSeconds enemy heroes spent inside live observer circles:")
    print(circle_summary(samples).to_string(index=False))
    print("\nHow often the warding team could see them, by distance from the ward:")
    print(by_distance(samples).to_string(index=False))


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
