"""Regression checks for profile attribution and validation, without replay I/O."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import profile_parser
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


def test_public_output_rejects_changed_details_with_identical_metadata(monkeypatch) -> None:
    import gem

    match = SimpleNamespace(match_id=8822520406, duration=1397, players=[None] * 10, combat_log=[])
    output = {"match_id": match.match_id, "duration": match.duration, "gold": [100, 200]}
    expected = hashlib.sha256(
        json.dumps(output, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    monkeypatch.setitem(profile_parser.EXPECTED_OUTPUT_SHA256, match.match_id, expected)
    monkeypatch.setattr(gem, "to_dict", lambda _: output)
    assert profile_parser._checked_output(match)["sha256"] == expected
    output["gold"][1] = 201
    with pytest.raises(RuntimeError, match="Public output mismatch"):
        profile_parser._checked_output(match)


@pytest.fixture
def parser_checkout(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.run(
            ["git", "-C", str(tmp_path), *args], check=True, capture_output=True, text=True
        ).stdout.strip()

    git("init")
    source = tmp_path / "src/gem/parser.py"
    source.parent.mkdir(parents=True)
    source.write_text("original = True\n")
    manifest = tmp_path / profile_parser.FIXTURE_MANIFEST
    manifest.parent.mkdir(parents=True)
    manifest.write_text('{"matches": []}\n')
    (tmp_path / ".gitignore").write_text("__pycache__/\n")
    git("add", ".")
    git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "fixture")
    monkeypatch.setattr(profile_parser, "ROOT", tmp_path)
    return tmp_path, git


def test_clean_parser_allows_unrelated_edits_and_ignored_bytecode(parser_checkout) -> None:
    root, git = parser_checkout
    (root / "notes.md").write_text("unrelated\n")
    cache = root / "src/gem/__pycache__"
    cache.mkdir()
    (cache / "parser.pyc").write_bytes(b"cache")
    assert profile_parser._parser_commit() == git("rev-parse", "HEAD")


@pytest.mark.parametrize("change", ["unstaged", "staged", "deleted", "untracked"])
def test_dirty_parser_is_rejected(parser_checkout, change) -> None:
    root, git = parser_checkout
    source = root / "src/gem/parser.py"
    if change == "deleted":
        source.unlink()
    elif change == "untracked":
        (source.parent / "extra.py").write_text("extra = True\n")
    else:
        source.write_text("original = False\n")
        if change == "staged":
            git("add", "src/gem/parser.py")
    with pytest.raises(RuntimeError, match="dirty parser sources"):
        profile_parser._parser_commit()


@pytest.mark.parametrize("change", ["unstaged", "staged", "deleted"])
def test_dirty_fixture_manifest_is_rejected(parser_checkout, change) -> None:
    root, git = parser_checkout
    manifest = root / profile_parser.FIXTURE_MANIFEST
    if change == "deleted":
        manifest.unlink()
    else:
        manifest.write_text('{"matches": [{"dem": "different.dem"}]}\n')
        if change == "staged":
            git("add", profile_parser.FIXTURE_MANIFEST)
    with pytest.raises(RuntimeError, match="fixture manifest"):
        profile_parser._parser_commit()


def test_parser_provenance_fails_when_git_is_unavailable(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(profile_parser, "ROOT", tmp_path)
    with pytest.raises(subprocess.CalledProcessError):
        profile_parser._parser_commit()


def test_recorded_public_hashes_match_enforced_baselines() -> None:
    records = Path(__file__).resolve().parents[1] / "docs/benchmarks/2026-09-08-parser"
    paths = list(records.glob("*-public-*.json"))
    assert len(paths) == 11
    for path in paths:
        record = json.loads(path.read_text())
        assert (
            record["output"]["sha256"]
            == profile_parser.EXPECTED_OUTPUT_SHA256[record["fixture"]["match_id"]]
        )
