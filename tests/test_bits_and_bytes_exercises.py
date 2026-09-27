"""The bits & bytes practice files in examples/ keep working.

The grader in examples/bits_and_bytes_exercises.py checks learners' answers
against real replay bytes and gem's BitReader, so a change to either should
fail here rather than leave the exercises broken.
"""

from __future__ import annotations

import importlib
import types
from pathlib import Path

import pytest

_EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.fixture
def exercises(monkeypatch: pytest.MonkeyPatch) -> types.ModuleType:
    monkeypatch.syspath_prepend(str(_EXAMPLES))
    return importlib.import_module("bits_and_bytes_exercises")


@pytest.fixture
def solutions(exercises: types.ModuleType) -> types.ModuleType:
    return importlib.import_module("bits_and_bytes_solutions")


def test_solutions_pass_every_exercise(exercises, solutions, capsys):
    passed, total = exercises.grade(solutions)
    assert passed == total, capsys.readouterr().out


def test_unstarted_exercises_are_reported_not_done(exercises, capsys):
    passed, total = exercises.grade(exercises)
    out = capsys.readouterr().out
    assert passed == 0
    assert out.count("not done yet") == total


def test_grader_rejects_msb_first_bitstream(exercises, solutions, capsys):
    class MsbFirstStream(solutions.BitStream):
        """A common mistake: reading each byte's bits from the left."""

        def read_bits(self, n: int) -> int:
            value = 0
            for i in range(n):
                byte = self.data[self.pos // 8]
                value |= ((byte >> (7 - self.pos % 8)) & 1) << i
                self.pos += 1
            return value

    wrong = types.ModuleType("wrong")
    wrong.__dict__.update(vars(solutions))
    wrong.BitStream = MsbFirstStream

    passed, total = exercises.grade(wrong)
    out = capsys.readouterr().out
    assert passed < total
    assert "✗  BitStream.read_bits" in out
