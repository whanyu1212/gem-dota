"""The deprecation helpers, and the 0.12 deprecations removed in 0.13 (HY-96, HY-103)."""

from __future__ import annotations

import dataclasses
import warnings
from typing import Any, cast

import pytest

import gem
import gem.analysis
from gem._deprecation import (
    deprecated,
    deprecated_field,
    deprecated_module_attrs,
    read_quietly,
    warn_deprecated,
)
from gem.analysis import (
    FarmingRouteSegment,
    MatchAnalysis,
    RoshConversion,
    RoshDifferentialProfile,
)
from gem.extractors.objectives import AegisEvent, RoshanKill
from gem.results.models import ParsedMatch, ParsedPlayer

#: Names deprecated in 0.12 and removed in 0.13.
REMOVED_NAMES = (
    # map_context and estimate_vision (HY-98)
    "CampVisitContext",
    "MapContextBucket",
    "build_map_context_timeline",
    "score_camp_visit_context",
    "estimate_vision",
    # farming segment context (HY-100)
    "FarmingSegmentContext",
    "FarmingContextTag",
    "FarmingContextConfig",
    "DEFAULT_FARMING_CONTEXT_CONFIG",
    # smoke-fight insights (HY-101)
    "build_smoke_fight_insights",
    "SmokeFightInsight",
    "SmokeFightMemberInsight",
    "SmokeFightStatus",
    "ExactEventEvidence",
    "ExactEventKind",
    "FightCentroidSource",
    "FightOutcome",
    "FollowUpBoundary",
    "FollowUpEvent",
    "FollowUpKind",
    "FollowUpWindow",
    "FormationEvidence",
    "MemberPositionEvidence",
    "SampledNearFightEvidence",
    "TeamRelation",
    # Roshan tags and territory (HY-99)
    "RoshTagThresholds",
    "DEFAULT_ROSH_TAG_THRESHOLDS",
    "RoshTerritoryConfig",
    "RoshTerritoryWindow",
    "RoshCoverageCell",
)

REMOVED_FIELDS = {
    RoshConversion: (
        "conversion_score",
        "conversion_label",
        "aegis_outcome",
        "drivers",
        "conversion_tags",
        "enemy_half_farm_share_before",
        "enemy_half_farm_share_during",
        "enemy_half_farm_share_delta",
    ),
    RoshDifferentialProfile: (
        "before_territory",
        "during_territory",
        "conversion_coverage_swing_pct",
        "opponent_coverage_swing_pct",
        "coverage_swing_pct",
        "conversion_depth_swing",
        "opponent_depth_swing",
        "depth_swing",
        "tags",
        "tag_ruleset",
    ),
    FarmingRouteSegment: ("context",),
    MatchAnalysis: ("smoke_fights",),
}


def _warnings(func) -> list[str]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        func()
    return [str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)]


# ---------------------------------------------------------------------------
# The helpers stay for future deprecations.
# ---------------------------------------------------------------------------


def test_warn_deprecated_names_the_removal_and_the_alternative() -> None:
    with pytest.warns(DeprecationWarning, match=r"gem\.x is deprecated .* gem 0\.13; use gem\.y"):
        warn_deprecated("gem.x", alternative="gem.y")


def test_deprecated_decorator_warns_on_every_call() -> None:
    @deprecated("gem.f")
    def f(value: int) -> int:
        return value + 1

    assert _warnings(lambda: f(1)) == ["gem.f is deprecated and will be removed in gem 0.13."]
    assert f.__name__ == "f"


def test_deprecated_module_attrs_falls_back_and_raises() -> None:
    getattr_ = deprecated_module_attrs(
        "m", {"old": (1, None, True)}, fallback=lambda name: {"renamed": 2}[name]
    )
    with pytest.warns(DeprecationWarning, match="m.old"):
        assert getattr_("old") == 1
    assert getattr_("renamed") == 2
    with pytest.raises(KeyError):
        getattr_("missing")
    with pytest.raises(AttributeError):
        deprecated_module_attrs("m", {})("missing")


@dataclasses.dataclass
class _Record:
    kept: int = 0
    old: list[int] = dataclasses.field(
        default=cast(
            Any,
            deprecated_field("old", "gem._Record.old", alternative="kept", default_factory=list),
        ),
        repr=False,
        compare=False,
    )


def test_deprecated_fields_warn_on_read_only() -> None:
    record = _Record(old=[1])
    # Printing, comparing and serializing stay silent.
    assert _warnings(lambda: (repr(record), record == _Record(), gem.to_dict(record))) == []
    messages = _warnings(lambda: record.old)
    assert messages == [
        "gem._Record.old is deprecated and will be removed in gem 0.13; use kept instead."
    ]
    # Each instance gets its own default list.
    assert read_quietly(_Record(), "old") is not read_quietly(_Record(), "old")


def test_read_quietly_skips_the_warning() -> None:
    record = _Record(old=[1])
    assert _warnings(lambda: read_quietly(record, "old")) == []
    assert read_quietly(record, "old") == [1]
    assert read_quietly(record, "kept") == 0


# ---------------------------------------------------------------------------
# The 0.12 deprecations are gone in 0.13.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("module", [gem, gem.analysis])
@pytest.mark.parametrize("name", REMOVED_NAMES)
def test_removed_names_are_gone(module: object, name: str) -> None:
    assert name not in module.__all__
    with pytest.raises(AttributeError):
        getattr(module, name)


def test_world_in_bounds_is_gone() -> None:
    with pytest.raises(AttributeError):
        gem.analysis.world_in_bounds  # noqa: B018


@pytest.mark.parametrize(
    "module",
    [
        "gem.analysis.map_context",
        "gem.analysis.smoke_fight",
        "gem.analysis.farming_context",
        "gem.analysis._territory",
    ],
)
def test_removed_modules_are_gone(module: str) -> None:
    with pytest.raises(ModuleNotFoundError):
        __import__(module)


@pytest.mark.parametrize(
    ("cls", "name"), [(cls, name) for cls, names in REMOVED_FIELDS.items() for name in names]
)
def test_removed_fields_are_gone(cls: type, name: str) -> None:
    assert name not in {field.name for field in dataclasses.fields(cls)}


def test_removed_parameters_are_rejected() -> None:
    match = ParsedMatch()
    with pytest.raises(TypeError):
        gem.build_rosh_conversions(match, tag_thresholds=None)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        gem.build_rosh_conversions(match, territory_config=None)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        gem.build_farming_routes(match, context_config=None)  # type: ignore[call-arg]


def test_analyze_and_its_outputs_are_silent() -> None:
    from gem.results.dataframes import build_dataframes

    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20_000,
        players=[ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe")],
        roshans=[RoshanKill(tick=1_000, killer="npc_dota_hero_axe", kill_number=1)],
        aegis_events=[AegisEvent(tick=1_010, player_id=0, event_type="pickup")],
    )
    assert (
        _warnings(
            lambda: (
                gem.to_json(match, analysis=gem.analyze(match)),
                build_dataframes(match, include=["analysis"]),
            )
        )
        == []
    )
