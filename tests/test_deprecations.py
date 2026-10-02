"""Names deprecated in 0.12 keep working, warn once per use, and leave the public lists (HY-96)."""

from __future__ import annotations

import dataclasses
import warnings

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
from gem.results.models import ParsedMatch

_FARMING_CONTEXT = (
    "FarmingSegmentContext",
    "FarmingContextTag",
    "FarmingContextConfig",
    "DEFAULT_FARMING_CONTEXT_CONFIG",
)
_SMOKE_FIGHT_TYPES = (
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
)
_DEPRECATED = (
    "CampVisitContext",
    "MapContextBucket",
    "build_map_context_timeline",
    "score_camp_visit_context",
    "estimate_vision",
    "build_smoke_fight_insights",
    *_FARMING_CONTEXT,
    *_SMOKE_FIGHT_TYPES,
)


def _warnings(func) -> list[str]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        func()
    return [str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)]


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


@pytest.mark.parametrize("name", _DEPRECATED)
def test_deprecated_names_leave_all_but_still_resolve(name: str) -> None:
    assert name not in gem.__all__
    assert name not in gem.analysis.__all__
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        assert getattr(gem, name) is getattr(gem.analysis, name)


@pytest.mark.parametrize("module", [gem, gem.analysis])
@pytest.mark.parametrize(
    "name", ["CampVisitContext", "MapContextBucket", *_FARMING_CONTEXT, *_SMOKE_FIGHT_TYPES]
)
def test_deprecated_classes_warn_on_access(module: object, name: str) -> None:
    messages = _warnings(lambda: getattr(module, name))
    assert len(messages) == 1
    assert f"{module.__name__}.{name} is deprecated" in messages[0]


def test_deprecated_functions_warn_once_per_call() -> None:
    match = ParsedMatch()
    messages = _warnings(lambda: gem.estimate_vision(match, 2, 0, 0.0, 0.0))
    assert messages == [
        "gem.estimate_vision is deprecated and will be removed in gem 0.13; use "
        "gem.assess_point_vision(...).sources for modelled coverage of a point, "
        "or gem.hero_visibility_at for replay visibility instead."
    ]
    assert len(_warnings(lambda: gem.build_map_context_timeline(match, 2))) == 1
    assert len(_warnings(lambda: gem.analysis.world_in_bounds(0.0, 0.0))) == 1


def test_alternatives_name_public_api() -> None:
    # Every replacement a warning recommends must exist (Codex review on #265).
    for name in ("assess_point_vision", "hero_visibility_at", "region_of"):
        assert name in gem.__all__
        assert callable(getattr(gem, name))
    messages = _warnings(lambda: gem.MapContextBucket)
    assert "gem.region_of" in messages[0]


def test_smoke_fight_insights_warn_once_per_call_and_point_at_first_fight() -> None:
    messages = _warnings(lambda: gem.build_smoke_fight_insights(ParsedMatch()))
    assert messages == [
        "gem.build_smoke_fight_insights is deprecated and will be removed in gem 0.13; "
        "use SmokeAnalysis.first_fight from gem.build_smoke_analysis instead."
    ]


def test_gem_internals_use_the_deprecated_builders_silently() -> None:
    # analyze() and the report keep producing these outputs until 0.13 without warning.
    from gem.results.models import ParsedPlayer

    match = ParsedMatch(players=[ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe")])
    assert _warnings(lambda: gem.analyze(match)) == []


def test_deprecated_fields_warn_on_read_only() -> None:
    from gem.analysis.bundle import MatchAnalysis
    from gem.analysis.farming import FarmingRouteSegment

    analysis = MatchAnalysis(smoke_fights=[])
    # Printing, comparing and serializing stay silent.
    assert (
        _warnings(lambda: (repr(analysis), analysis == MatchAnalysis(), gem.to_dict(analysis)))
        == []
    )
    messages = _warnings(lambda: analysis.smoke_fights)
    assert len(messages) == 1
    assert "gem.MatchAnalysis.smoke_fights is deprecated" in messages[0]
    # Each instance gets its own default list.
    first, second = MatchAnalysis(), MatchAnalysis()
    assert read_quietly(first, "smoke_fights") is not read_quietly(second, "smoke_fights")

    # The field keeps its name, so serialized output and DataFrames are unchanged.
    assert "context" in {f.name for f in dataclasses.fields(FarmingRouteSegment)}
    assert isinstance(vars(FarmingRouteSegment)["context"], deprecated_field)


def test_read_quietly_skips_the_warning() -> None:
    from gem.analysis.bundle import MatchAnalysis

    analysis = MatchAnalysis(smoke_fights=[1])
    assert _warnings(lambda: read_quietly(analysis, "smoke_fights")) == []
    assert read_quietly(analysis, "smoke_fights") == [1]
    assert read_quietly(analysis, "smoke") == []


def test_context_config_warns_even_without_a_camp_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    from gem.analysis import farming

    def missing() -> dict:
        raise OSError("no catalog")

    monkeypatch.setattr(farming, "load_camp_zones", missing)
    with pytest.warns(DeprecationWarning, match=r"context_config"):
        farming.build_farming_routes(ParsedMatch(), context_config=farming.FarmingContextConfig())


def test_world_in_bounds_is_not_added_to_the_top_level() -> None:
    with pytest.raises(AttributeError):
        gem.world_in_bounds  # noqa: B018
