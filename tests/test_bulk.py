"""Tests for gem.batch — parallel replay parsing."""

from __future__ import annotations

import concurrent.futures
from pathlib import Path
from unittest.mock import patch

import pytest

import gem
from gem.batch import ParseResult, _collect_paths, parse_many
from gem.models import ParsedMatch

# ---------------------------------------------------------------------------
# Synchronous executor — avoids multiprocessing entirely in unit tests.
# Replaces ProcessPoolExecutor with a fake that runs _parse_one in-process,
# so monkeypatching _parse_one works without any pickling.
# ---------------------------------------------------------------------------


class _SyncExecutor:
    """Drop-in for ProcessPoolExecutor that runs tasks synchronously."""

    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def submit(self, fn, *args, **kwargs):
        future: concurrent.futures.Future = concurrent.futures.Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except Exception as exc:
            future.set_exception(exc)
        return future


# ---------------------------------------------------------------------------
# Fake _parse_one implementations
# ---------------------------------------------------------------------------


def _ok(path: Path) -> tuple[Path, ParsedMatch | None, Exception | None]:
    return path, ParsedMatch(match_id=int(path.stem) if path.stem.isdigit() else 0), None


def _fail(path: Path) -> tuple[Path, ParsedMatch | None, Exception | None]:
    return path, None, ValueError("corrupt replay")


def _mixed(path: Path) -> tuple[Path, ParsedMatch | None, Exception | None]:
    return _fail(path) if path.name == "bad.dem" else _ok(path)


# ---------------------------------------------------------------------------
# _collect_paths
# ---------------------------------------------------------------------------


class TestCollectPaths:
    def test_list_of_paths(self, tmp_path):
        f1, f2 = tmp_path / "a.dem", tmp_path / "b.dem"
        f1.touch()
        f2.touch()
        assert set(_collect_paths([f1, f2], recursive=False)) == {f1, f2}

    def test_directory_non_recursive(self, tmp_path):
        (tmp_path / "a.dem").touch()
        (tmp_path / "b.dem").touch()
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "c.dem").touch()
        result = _collect_paths(tmp_path, recursive=False)
        assert len(result) == 2
        assert all(p.parent == tmp_path for p in result)

    def test_directory_recursive(self, tmp_path):
        (tmp_path / "a.dem").touch()
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "b.dem").touch()
        assert len(_collect_paths(tmp_path, recursive=True)) == 2

    def test_empty_directory_raises(self, tmp_path):
        with pytest.raises(ValueError, match="No .dem files found"):
            _collect_paths(tmp_path, recursive=False)

    def test_single_file_treated_as_list(self, tmp_path):
        f = tmp_path / "match.dem"
        f.touch()
        assert _collect_paths(f, recursive=False) == [f]


# ---------------------------------------------------------------------------
# parse_many
# ---------------------------------------------------------------------------


class TestParseMany:
    def test_returns_one_result_per_path(self, tmp_path):
        paths = [tmp_path / f"{i}.dem" for i in range(3)]
        for p in paths:
            p.touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_ok),
        ):
            results = parse_many(paths, progress=False)

        assert len(results) == 3
        assert all(isinstance(r, ParseResult) for r in results)
        assert all(r.ok for r in results)

    def test_failed_replay_captured_not_raised(self, tmp_path):
        p = tmp_path / "bad.dem"
        p.touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_fail),
        ):
            results = parse_many([p], progress=False)

        assert len(results) == 1
        assert not results[0].ok
        assert isinstance(results[0].error, ValueError)
        assert results[0].match is None

    def test_mixed_success_and_failure(self, tmp_path):
        good, bad = tmp_path / "good.dem", tmp_path / "bad.dem"
        good.touch()
        bad.touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_mixed),
        ):
            results = parse_many([good, bad], progress=False)

        assert len([r for r in results if r.ok]) == 1
        assert len([r for r in results if not r.ok]) == 1

    def test_workers_capped_at_path_count(self, tmp_path):
        p = tmp_path / "a.dem"
        p.touch()

        captured: dict[str, int] = {}

        class _CapturingSyncExecutor(_SyncExecutor):
            def __init__(self, **kwargs):
                captured["max_workers"] = kwargs.get("max_workers")
                super().__init__(**kwargs)

        with (
            patch("gem.batch.ProcessPoolExecutor", _CapturingSyncExecutor),
            patch("gem.batch._parse_one", side_effect=_ok),
        ):
            parse_many([p], workers=16, progress=False)

        assert captured["max_workers"] == 1

    def test_directory_source(self, tmp_path):
        for i in range(3):
            (tmp_path / f"{i}.dem").touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_ok),
        ):
            results = parse_many(tmp_path, progress=False)

        assert len(results) == 3

    def test_parse_result_ok_property(self):
        assert ParseResult(path=Path("a.dem"), match=ParsedMatch(), error=None).ok is True
        assert ParseResult(path=Path("b.dem"), match=None, error=ValueError()).ok is False


# ---------------------------------------------------------------------------
# parse_many_to_dataframe
# ---------------------------------------------------------------------------


class TestParseManyToDataframe:
    def test_returns_dict_with_match_path_column(self, tmp_path):
        for i in range(2):
            (tmp_path / f"{i}.dem").touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_ok),
        ):
            dfs = gem.parse_many_to_dataframe(tmp_path, progress=False)

        assert isinstance(dfs, dict)
        assert "players" in dfs
        assert "match_path" in dfs["players"].columns

    def test_skips_failed_replays(self, tmp_path):
        good, bad = tmp_path / "good.dem", tmp_path / "bad.dem"
        good.touch()
        bad.touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_mixed),
        ):
            dfs = gem.parse_many_to_dataframe([good, bad], progress=False)

        assert all("bad.dem" not in str(v) for v in dfs["match"]["match_path"])

    def test_match_path_column_is_string(self, tmp_path):
        p = tmp_path / "123.dem"
        p.touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_ok),
        ):
            dfs = gem.parse_many_to_dataframe([p], progress=False)

        assert dfs["match"]["match_path"].dtype == object

    def test_rows_concatenated_across_replays(self, tmp_path):
        for i in range(3):
            (tmp_path / f"{i}.dem").touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_ok),
        ):
            dfs = gem.parse_many_to_dataframe(tmp_path, progress=False)

        # match table has one row per replay → 3 rows
        assert len(dfs["match"]) == 3


# ---------------------------------------------------------------------------
# parse_many_to_parquet
# ---------------------------------------------------------------------------


class TestParseManyToParquet:
    @pytest.mark.skipif(
        not __import__("importlib").util.find_spec("pyarrow"),
        reason="pyarrow not installed",
    )
    def test_writes_subdir_per_replay(self, tmp_path):
        replay_dir = tmp_path / "replays"
        replay_dir.mkdir()
        out_dir = tmp_path / "out"
        for name in ("123", "456"):
            (replay_dir / f"{name}.dem").touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_ok),
        ):
            written = gem.parse_many_to_parquet(replay_dir, out_dir, progress=False)

        subdirs = {p.parent.name for p in written}
        assert {"123", "456"}.issubset(subdirs)
        assert all(p.suffix == ".parquet" for p in written)
        assert all(p.exists() for p in written)

    def test_skips_failed_replays(self, tmp_path):
        p = tmp_path / "bad.dem"
        p.touch()

        with (
            patch("gem.batch.ProcessPoolExecutor", _SyncExecutor),
            patch("gem.batch._parse_one", side_effect=_fail),
        ):
            written = gem.parse_many_to_parquet([p], tmp_path / "out", progress=False)

        assert written == []
