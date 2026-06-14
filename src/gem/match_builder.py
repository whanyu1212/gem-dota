"""Deprecated compatibility shim for :mod:`gem.results.assembly`."""

import warnings

warnings.warn(
    "gem.match_builder is deprecated; import from gem.results.assembly instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.results.assembly import (  # noqa: E402
    _LANE_GRID,
    _LANE_WINDOW,
    _radiant_win_from_ancient,
    build_parsed_match,
)

__all__ = ["_LANE_GRID", "_LANE_WINDOW", "_radiant_win_from_ancient", "build_parsed_match"]
