"""Lane assignment from a player's first-10-minute ``lane_pos`` heatmap.

Ports OpenDota's server-side lane computation. ``lane_pos`` counts one sample per
once-a-second interval, keyed by OpenDota map cell (world units / 128, see
:mod:`gem.extractors._cells`). Each cell maps to one of five lanes through a
128 x 128 grid over cells 64-191. The most common lane wins, and a player whose
most common lane holds under 45% of the samples is flagged as roaming. Roaming
is a flag beside the lane role, not a role of its own.

Reference: odota/core svc/util/compute.ts ``getLaneFromPosData``,
svc/util/laneMappings.ts and svc/util/utility.ts ``modeWithCount``, read at
7b4256f (odota/core is not one of the pinned parsers; it computes these fields
from the parser's ``lane_pos``). The parity fixtures' OpenDota JSON confirms the
results.
"""

from __future__ import annotations

from dataclasses import dataclass

#: OpenDota lane ids (``lane``).
LANE_BOT = 1
LANE_MID = 2
LANE_TOP = 3
LANE_RADIANT_JUNGLE = 4
LANE_DIRE_JUNGLE = 5

#: OpenDota lane roles (``lane_role``); ``0`` means no lane could be assigned.
ROLE_SAFE = 1
ROLE_MID = 2
ROLE_OFF = 3
ROLE_JUNGLE = 4

#: Below this share of samples in the most common lane, a player is roaming.
_ROAMING_SHARE = 0.45

# laneMappings covers cells 64-191 on each axis: 128 rows, indexed from the top.
_GRID_ORIGIN = 64
_GRID_SIZE = 128


def lane_for_cell(x: int, y: int) -> int | None:
    """Return OpenDota's lane for a map cell.

    Args:
        x: Cell x (world x / 128, rounded).
        y: Cell y (world y / 128, rounded).

    Returns:
        A lane id (``LANE_BOT`` ... ``LANE_DIRE_JUNGLE``), or ``None`` for a cell
        outside the grid, which OpenDota skips.
    """
    col = x - _GRID_ORIGIN
    row = _GRID_SIZE - (y - _GRID_ORIGIN)
    if not (0 <= row < _GRID_SIZE and 0 <= col < _GRID_SIZE):
        return None
    if abs(row - (_GRID_SIZE - 1 - col)) < 8:
        return LANE_MID
    if col < 27 or row < 27:
        return LANE_TOP
    if col >= 100 or row >= 100:
        return LANE_BOT
    if row < 50:
        return LANE_DIRE_JUNGLE
    if row >= 77:
        return LANE_RADIANT_JUNGLE
    return LANE_MID


@dataclass(frozen=True, slots=True)
class LaneAssignment:
    """A player's lane, lane role and roaming flag.

    Attributes:
        lane: Most common lane: 1 bot, 2 mid, 3 top, 4 Radiant jungle,
            5 Dire jungle; ``0`` when no sample fell on the grid.
        lane_role: 1 safe lane, 2 mid, 3 off lane, 4 jungle; ``0`` when unknown.
        is_roaming: Whether the most common lane holds under 45% of samples.
    """

    lane: int = 0
    lane_role: int = 0
    is_roaming: bool = False


def assign_lane(lane_pos: dict[str, dict[str, int]], team: int) -> LaneAssignment:
    """Assign a lane from a ``lane_pos`` heatmap, as OpenDota does.

    Ties go to the lane that first reaches a strictly higher count while cells
    are read in OpenDota's order: x ascending, then y ascending (JavaScript
    orders integer object keys numerically), each cell counted ``count`` times.

    Args:
        lane_pos: Sample counts as ``{x: {y: count}}`` with cell-number keys.
        team: Team number (2 = Radiant, 3 = Dire).

    Returns:
        The player's :class:`LaneAssignment`.
    """
    counts: dict[int, int] = {}
    total = 0
    mode, mode_count = 0, 0
    for x in sorted(lane_pos, key=int):
        column = lane_pos[x]
        for y in sorted(column, key=int):
            lane = lane_for_cell(int(x), int(y))
            if lane is None:
                continue
            for _ in range(column[y]):
                total += 1
                counts[lane] = counts.get(lane, 0) + 1
                if counts[lane] > mode_count:
                    mode, mode_count = lane, counts[lane]
    if total == 0:
        return LaneAssignment()
    radiant = team == 2
    role = {
        LANE_BOT: ROLE_SAFE if radiant else ROLE_OFF,
        LANE_MID: ROLE_MID,
        LANE_TOP: ROLE_OFF if radiant else ROLE_SAFE,
        LANE_RADIANT_JUNGLE: ROLE_JUNGLE,
        LANE_DIRE_JUNGLE: ROLE_JUNGLE,
    }[mode]
    return LaneAssignment(lane=mode, lane_role=role, is_roaming=mode_count / total < _ROAMING_SHARE)
