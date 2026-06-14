"""Compatibility shim for :mod:`gem.results.assembly`."""

from gem.results.assembly import (
    _LANE_GRID,
    _LANE_WINDOW,
    _radiant_win_from_ancient,
    build_parsed_match,
)

__all__ = ["_LANE_GRID", "_LANE_WINDOW", "_radiant_win_from_ancient", "build_parsed_match"]
