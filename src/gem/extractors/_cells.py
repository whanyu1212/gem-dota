"""OpenDota's map-cell coordinates, rounded exactly as its parser rounds them.

OpenDota reports positions in cell units: ``(cell * 128 + vec) / 128`` computed in
Java ``float`` (float32), i.e. world units / 128. Keys such as ``lane_pos`` and the
ward ``obs``/``sen`` maps are ``[Math.round(x), Math.round(y)]``. ``expand()`` first
rounds each coordinate to one decimal (``Math.round(x * 10.0) / 10.0f``) for every
entry it processes, so ward keys are rounded twice. Interval entries only pass
through ``expand()`` from game time 0, so a ``lane_pos`` sample is rounded twice in
game and once before the horn.

Java's ``Math.round`` rounds half up; Python's ``round`` rounds half to even, which
put ward keys one cell off (``[91,156]`` for OpenDota's ``[92,156]``).

Reference: odota/parser src/main/java/opendota/Parse.java ``getPreciseLocation``
and src/main/java/opendota/CreateParsedDataBlob.java ``expand``,
``handleInterval`` (pinned revision in CLAUDE.md).
"""

from __future__ import annotations

import math

import numpy as np

#: World units per OpenDota cell (``CBodyComponent`` cell size).
WORLD_UNITS_PER_CELL = 128.0

_F32_CELL = np.float32(WORLD_UNITS_PER_CELL)
_F32_TEN = np.float32(10.0)


def _java_round(value: float) -> int:
    """Round half up, as Java's ``Math.round`` does."""
    floor = math.floor(value)
    return floor + 1 if value - floor >= 0.5 else floor


def od_cell(world: float) -> float:
    """Convert a world coordinate to OpenDota's float32 cell coordinate.

    Args:
        world: World coordinate (``cell * 128 + vec``).

    Returns:
        The coordinate in cell units, with float32 precision.
    """
    return float(np.float32(world) / _F32_CELL)


def od_one_decimal(cell: float) -> float:
    """Round a cell coordinate to one decimal the way ``expand()`` does.

    Args:
        cell: Cell coordinate from :func:`od_cell`.

    Returns:
        ``Math.round(cell * 10.0) / 10.0f`` with float32 precision.
    """
    return float(np.float32(_java_round(cell * 10.0)) / _F32_TEN)


def od_cell_index(world: float, *, expanded: bool = True) -> int:
    """Return OpenDota's integer cell for a world coordinate.

    Args:
        world: World coordinate.
        expanded: Whether the entry went through ``expand()`` (one-decimal rounding)
            before its key was built. True for wards and in-game ``lane_pos``
            samples, False for pre-horn ``lane_pos`` samples.

    Returns:
        ``Math.round`` of the (optionally one-decimal) cell coordinate.
    """
    cell = od_cell(world)
    if expanded:
        cell = od_one_decimal(cell)
    return _java_round(cell)
