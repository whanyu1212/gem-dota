"""Regression checks for statistical-profile attribution, without replay I/O."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from scripts.profile_parser import _sample_summary


def _frame(name: str, elapsed: float, children: list | None = None) -> SimpleNamespace:
    children = children or []
    return SimpleNamespace(
        function=name,
        file_path="example.py",
        line_no=1,
        time=elapsed,
        children=children,
        is_synthetic=name == "[self]",
        total_self_time=elapsed - sum(c.time for c in children if not c.is_synthetic),
    )


def _summary(frame: SimpleNamespace) -> dict:
    session = SimpleNamespace(
        root_frame=lambda: frame, duration=frame.time, cpu_time=frame.time, sample_count=10
    )
    return {f["function"]: f for f in _sample_summary(session)["functions"]}


def test_synthetic_self_samples_belong_to_the_parent_function() -> None:
    inner = _frame("decode", 0.6, [_frame("[self]", 0.6)])
    root = _frame("parse", 1.0, [_frame("[self]", 0.4), inner])
    functions = _summary(root)
    assert "[self]" not in functions
    assert functions["parse"]["self_s"] == pytest.approx(0.4)
    assert functions["decode"]["self_s"] == pytest.approx(0.6)
    assert sum(f["self_s"] for f in functions.values()) == pytest.approx(1.0)


def test_recursive_inclusive_time_is_counted_once_per_stack() -> None:
    inner = _frame("decode", 0.6, [_frame("[self]", 0.6)])
    outer = _frame("decode", 1.0, [_frame("[self]", 0.4), inner])
    functions = _summary(outer)
    assert functions["decode"]["self_s"] == pytest.approx(1.0)
    assert functions["decode"]["inclusive_s"] == pytest.approx(1.0)
