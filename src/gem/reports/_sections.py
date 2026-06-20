"""Backward-compatible shim for the report section builders.

The section builders used to live in this single ~3,700-line module. They now
live in the :mod:`gem.reports.sections` package, split by domain
(``match``, ``economy``, ``combat``, ``vision``). This module re-exports the
public ``build_*`` functions so existing imports such as
``from gem.reports._sections import build_rosh_conversion`` keep working.

Prefer importing from :mod:`gem.reports.sections` in new code.
"""

from __future__ import annotations

from gem.reports.sections import (
    build_buybacks,
    build_chat,
    build_combat_timeseries_chart,
    build_damage,
    build_draft,
    build_farming,
    build_gold_xp_chart,
    build_header,
    build_hero_timeseries_chart,
    build_kill_feed,
    build_laning,
    build_objectives,
    build_purchases,
    build_rosh_conversion,
    build_runes,
    build_scoreboard,
    build_teamfights,
    build_wards,
)

__all__ = [
    "build_buybacks",
    "build_chat",
    "build_combat_timeseries_chart",
    "build_damage",
    "build_draft",
    "build_farming",
    "build_gold_xp_chart",
    "build_header",
    "build_hero_timeseries_chart",
    "build_kill_feed",
    "build_laning",
    "build_objectives",
    "build_purchases",
    "build_rosh_conversion",
    "build_runes",
    "build_scoreboard",
    "build_teamfights",
    "build_wards",
]
