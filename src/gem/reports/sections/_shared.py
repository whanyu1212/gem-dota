"""Shared helpers used by more than one report section module.

Split out of the former monolithic ``_sections.py`` (see that module's
shim for backward-compatible re-exports).
"""

from __future__ import annotations

from gem.analysis import ward_vision_impact
from gem.results.models import ParsedMatch

_RADIANT_COLORS = ["#4caf50", "#81c784", "#a5d6a7", "#2e7d32", "#66bb6a"]


_DIRE_COLORS = ["#f44336", "#ff7043", "#ef9a9a", "#b71c1c", "#ff8a65"]


def _ward_enemies_seen(ward: object, match: ParsedMatch) -> int:
    """Count distinct enemy heroes that passed within observer ward vision radius."""
    return ward_vision_impact(ward, match)
