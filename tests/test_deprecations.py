"""Names deprecated in 0.12 keep working, warn once per use, and leave the public lists (HY-96)."""

from __future__ import annotations

import warnings

import pytest

import gem
import gem.analysis
from gem._deprecation import deprecated, deprecated_module_attrs, warn_deprecated
from gem.results.models import ParsedMatch

_DEPRECATED = (
    "CampVisitContext",
    "MapContextBucket",
    "build_map_context_timeline",
    "score_camp_visit_context",
    "estimate_vision",
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
@pytest.mark.parametrize("name", ["CampVisitContext", "MapContextBucket"])
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
    assert callable(gem.assess_point_vision)
    assert callable(gem.hero_visibility_at)
    for messages in (
        _warnings(lambda: gem.MapContextBucket),
        _warnings(lambda: gem.build_map_context_timeline(ParsedMatch(), 2)),
    ):
        assert all("region_of" not in message for message in messages)


def test_world_in_bounds_is_not_added_to_the_top_level() -> None:
    with pytest.raises(AttributeError):
        gem.world_in_bounds  # noqa: B018
