"""Report section builders, split by domain.

Importing from this package (or the legacy ``gem.reports._sections`` shim)
yields the same ``build_*`` functions as before the split.
"""

from __future__ import annotations

from gem.reports.sections.combat import (
    build_combat_timeseries_chart,
    build_kill_feed,
    build_teamfights,
)
from gem.reports.sections.economy import (
    build_buybacks,
    build_damage,
    build_gold_xp_chart,
    build_hero_timeseries_chart,
    build_purchases,
    build_runes,
)
from gem.reports.sections.match import (
    build_chat,
    build_draft,
    build_header,
    build_objectives,
    build_rosh_conversion,
    build_scoreboard,
)
from gem.reports.sections.vision import (
    build_farming,
    build_laning,
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
