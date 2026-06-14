"""Deprecated compatibility shim for :mod:`gem.analysis.map_context`."""

import warnings

warnings.warn(
    "gem.map_context is deprecated; import from gem.analysis.map_context instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.analysis.map_context import (  # noqa: E402
    CampVisitContext,
    MapContextBucket,
    build_map_context_timeline,
    score_camp_visit_context,
    world_in_bounds,
)

__all__ = [
    "CampVisitContext",
    "MapContextBucket",
    "build_map_context_timeline",
    "score_camp_visit_context",
    "world_in_bounds",
]
