"""One-call bundle of gem's evidence-first post-parse analyses.

:func:`analyze` runs every public match-level analysis builder with its default
configuration and returns the results as one :class:`MatchAnalysis`, which
:func:`gem.to_json` can embed alongside the match.

Reference: gem-original composition over ``analysis/smoke.py``,
``analysis/smoke_fight.py``, ``analysis/roshan.py``, ``analysis/farming.py``,
and ``analysis/teamfight_positioning.py``; see those modules for the upstream
event semantics each builder consumes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.analysis.farming import FarmingRoute, build_farming_routes
from gem.analysis.roshan import RoshConversion, build_rosh_conversions
from gem.analysis.smoke import SmokeAnalysis, build_smoke_analysis
from gem.analysis.smoke_fight import SmokeFightInsight, build_smoke_fight_insights
from gem.analysis.teamfight_positioning import (
    TeamfightPositioning,
    build_teamfight_positioning,
)

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch


@dataclass
class MatchAnalysis:
    """Results of every default post-parse analysis for one match.

    Attributes:
        smoke: Smoke of Deceit lifecycle summaries (:func:`gem.build_smoke_analysis`).
        smoke_fights: Bounded smoke-to-fight insights
            (:func:`gem.build_smoke_fight_insights`).
        roshan_conversions: Per-Roshan conversion evidence
            (:func:`gem.build_rosh_conversions`).
        farming_routes: Per-player camp-route reconstructions
            (:func:`gem.build_farming_routes`).
        teamfight_positioning: Per-fight positioning snapshots
            (:func:`gem.build_teamfight_positioning`).
    """

    smoke: list[SmokeAnalysis] = field(default_factory=list)
    smoke_fights: list[SmokeFightInsight] = field(default_factory=list)
    roshan_conversions: list[RoshConversion] = field(default_factory=list)
    farming_routes: list[FarmingRoute] = field(default_factory=list)
    teamfight_positioning: list[TeamfightPositioning] = field(default_factory=list)


def analyze(match: ParsedMatch) -> MatchAnalysis:
    """Run every default post-parse analysis on a parsed match.

    Each builder runs with its default configuration. Call the individual
    ``build_*`` helpers directly when you need non-default options.

    Args:
        match: A fully populated :class:`ParsedMatch`, from :func:`gem.parse`
            or :func:`gem.load_json`.

    Returns:
        A :class:`MatchAnalysis` holding every analysis result.
    """
    return MatchAnalysis(
        smoke=build_smoke_analysis(match),
        smoke_fights=build_smoke_fight_insights(match),
        roshan_conversions=build_rosh_conversions(match),
        farming_routes=build_farming_routes(match),
        teamfight_positioning=build_teamfight_positioning(match),
    )
