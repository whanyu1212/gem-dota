"""Compatibility shim for :mod:`gem.analysis.map_context`."""

from gem.analysis.map_context import (
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
