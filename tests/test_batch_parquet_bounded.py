"""Scheduling and lifetime regressions for bounded batch Parquet export."""

from __future__ import annotations

import gc
import multiprocessing
import weakref
from concurrent.futures import Future, ProcessPoolExecutor, TimeoutError
from pathlib import Path

import pandas as pd
import pytest

import gem
from gem.replays import batch
from gem.results.models import ParsedMatch


class ControlledPool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.jobs = {}
        self.submitted = []
        self.closed = False
        self.on_submit = lambda path: None

    def submit(self, fn, path):
        self.on_submit(path)
        future = Future()
        self.jobs[path] = future
        self.submitted.append(path)
        return future

    def complete(self, path, error=None):
        future = self.jobs.pop(path)
        future.set_result((path, None if error else ParsedMatch(match_id=int(path.stem)), error))
        return future

    def shutdown(self, *, wait, cancel_futures):
        assert wait and cancel_futures
        self.closed = True
        for future in self.jobs.values():
            future.cancel()
        self.jobs.clear()


@pytest.fixture
def scheduler(monkeypatch):
    pools = []

    def create(max_workers):
        pool = ControlledPool(max_workers)
        pools.append(pool)
        return pool

    monkeypatch.setattr(batch, "ProcessPoolExecutor", create)
    return pools


def test_slow_writer_bounds_work_and_releases_results(monkeypatch, tmp_path, scheduler):
    paths = [Path(f"{i}.dem") for i in range(7)]
    exported = []
    matches = []

    def wait(futures, **kwargs):
        pool = scheduler[0]
        assert len(futures) <= 2
        # Complete the later submission first; no input-order blocking.
        path = list(pool.jobs)[-1]
        completed = pool.complete(path)
        return {completed}, set(futures) - {completed}

    def export(match, output, *, index):
        pool = scheduler[0]
        assert index
        assert len(pool.submitted) - len(exported) == 2 or len(pool.submitted) == len(paths)
        assert match.match_id == int(output.name)
        matches.append(weakref.ref(match))
        # While the writer is busy, every remaining parse can complete. There
        # must still be no submission beyond the original bounded window.
        for path in list(pool.jobs):
            pool.complete(path)
        exported.append(match.match_id)
        return [output / "match.parquet"]

    def check_released(path):
        gc.collect()
        assert all(ref() is None for ref in matches)

    def next_completion(futures, **kwargs):
        pool = scheduler[0]
        pool.on_submit = check_released
        ready = {f for f in futures if f.done()}
        return (ready, set(futures) - ready) if ready else wait(futures, **kwargs)

    monkeypatch.setattr(batch, "wait", next_completion)
    monkeypatch.setattr(gem, "to_parquet", export)
    written = gem.parse_many_to_parquet(paths, tmp_path, workers=2, progress=False, index=True)
    assert exported[0] == 1
    assert sorted(exported) == list(range(7))
    assert written == [tmp_path / str(i) / "match.parquet" for i in exported]
    assert scheduler[0].closed
    gc.collect()
    assert all(ref() is None for ref in matches)


@pytest.mark.parametrize("failure", ["parse", "future", "export", "submit", "interrupt"])
def test_failures_and_cleanup(monkeypatch, tmp_path, scheduler, failure):
    paths = [Path(f"{i}.dem") for i in range(5)]
    exported = []
    marker = tmp_path / "partial.parquet"

    def wait(futures, **kwargs):
        pool = scheduler[0]
        path = next(iter(pool.jobs))
        if failure == "future":
            future = pool.jobs.pop(path)
            future.set_exception(RuntimeError("worker transport"))
        else:
            future = pool.complete(
                path, ValueError("bad replay") if path.stem == "0" and failure == "parse" else None
            )
        if failure == "submit":

            def fail(path):
                raise RuntimeError("submission")

            pool.on_submit = fail
        return {future}, set()

    def export(match, output, *, index):
        marker.write_text("partial")
        exported.append(match.match_id)
        if failure == "export":
            raise OSError("disk failure")
        if failure == "interrupt":
            raise KeyboardInterrupt()
        return [output / "match.parquet"]

    monkeypatch.setattr(batch, "wait", wait)
    monkeypatch.setattr(gem, "to_parquet", export)
    if failure == "parse":
        written = gem.parse_many_to_parquet(paths, tmp_path, workers=2, progress=False)
        assert exported == [1, 2, 3, 4]
        assert len(written) == 4
    else:
        expected = {
            "future": RuntimeError,
            "export": OSError,
            "submit": RuntimeError,
            "interrupt": KeyboardInterrupt,
        }[failure]
        with pytest.raises(expected):
            gem.parse_many_to_parquet(paths, tmp_path, workers=2, progress=False)
        assert len(scheduler[0].submitted) == 2
        assert marker.exists() == (failure != "future")
    assert scheduler[0].closed
    assert not scheduler[0].jobs


@pytest.mark.parametrize("where", ["initial", "wait", "write", "final_write"])
def test_cooperative_deadline(monkeypatch, tmp_path, scheduler, where):
    clock = [0.0]
    monkeypatch.setattr(batch, "monotonic", lambda: clock[0])
    paths = [Path(f"{i}.dem") for i in range(1 if where == "final_write" else 4)]
    marker = tmp_path / "written.parquet"

    def wait(futures, *, timeout, return_when):
        assert timeout == 10.0
        if where == "wait":
            clock[0] = 10.0
            return set(), set(futures)
        pool = scheduler[0]
        return {pool.complete(next(iter(pool.jobs)))}, set()

    def export(match, output, *, index):
        marker.write_text("complete")
        clock[0] = 11.0
        return [marker]

    monkeypatch.setattr(batch, "wait", wait)
    monkeypatch.setattr(gem, "to_parquet", export)
    with pytest.raises(TimeoutError, match="Batch Parquet export timed out"):
        gem.parse_many_to_parquet(
            paths, tmp_path, workers=2, progress=False, timeout=0 if where == "initial" else 10
        )
    assert marker.exists() == (where in {"write", "final_write"})
    assert len(scheduler[0].submitted) == (0 if where == "initial" else min(2, len(paths)))
    assert scheduler[0].closed


@pytest.mark.parametrize("progress", [False, True])
def test_progress_and_parse_failure(monkeypatch, tmp_path, scheduler, progress):
    events = []

    class Progress:
        def __init__(self, *args):
            pass

        def __enter__(self):
            events.append("enter")
            return self

        def __exit__(self, *args):
            events.append("exit")

        def add_task(self, description, *, total):
            assert total == 2
            return 7

        def advance(self, task_id):
            assert task_id == 7
            events.append("advance")

    def wait(futures, **kwargs):
        pool = scheduler[0]
        return {pool.complete(next(iter(pool.jobs)), ValueError("corrupt"))}, set()

    monkeypatch.setattr("rich.progress.Progress", Progress)
    monkeypatch.setattr(batch, "wait", wait)
    assert (
        gem.parse_many_to_parquet(["0.dem", "1.dem"], tmp_path, workers=8, progress=progress) == []
    )
    assert scheduler[0].max_workers == 2
    assert events == (["enter", "advance", "advance", "exit"] if progress else [])


def test_empty_input_keeps_executor_validation(tmp_path):
    with pytest.raises(ValueError, match="max_workers must be greater than 0"):
        gem.parse_many_to_parquet([], tmp_path, progress=False)


@pytest.mark.parametrize("index", [False, True])
def test_spawned_parquet_roundtrip(tmp_path, monkeypatch, index):
    pytest.importorskip("pyarrow")
    replay = Path(__file__).parent / "fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem"
    source = tmp_path / "inputs"
    source.mkdir()
    (source / "nested").mkdir()
    for path in [source / "first.dem", source / "nested/second.dem"]:
        path.symlink_to(replay.resolve())
    monkeypatch.setattr(
        batch,
        "ProcessPoolExecutor",
        lambda **kw: ProcessPoolExecutor(mp_context=multiprocessing.get_context("spawn"), **kw),
    )
    expected = gem.to_parquet(gem.parse(replay), tmp_path / "expected", index=index)
    written = gem.parse_many_to_parquet(
        source, tmp_path / "actual", workers=1, recursive=True, progress=False, index=index
    )
    assert {p.parent.name for p in written} == {"first", "second"}
    assert len(written) == 2 * len(expected)
    for p in written:
        pd.testing.assert_frame_equal(
            pd.read_parquet(p), pd.read_parquet(tmp_path / "expected" / p.name)
        )


def test_failure_traceback_releases_other_results(monkeypatch, tmp_path, scheduler):
    refs = []

    def wait(futures, **kwargs):
        pool = scheduler[0]
        first = pool.complete(Path("0.dem"))
        second = pool.complete(Path("1.dem"))
        refs.append(weakref.ref(second.result()[1]))
        return {first}, {second}

    def export(match, output, *, index):
        raise OSError("write failed")

    monkeypatch.setattr(batch, "wait", wait)
    monkeypatch.setattr(gem, "to_parquet", export)
    with pytest.raises(OSError) as caught:
        gem.parse_many_to_parquet(["0.dem", "1.dem"], tmp_path, workers=2, progress=False)
    assert caught.value.__traceback__ is not None
    gc.collect()
    assert refs[0]() is None


def test_duplicate_stems_still_write_serially(monkeypatch, tmp_path, scheduler):
    paths = [Path("a/0.dem"), Path("b/0.dem"), Path("c/1.dem")]
    outputs = []

    def wait(futures, **kwargs):
        pool = scheduler[0]
        return {pool.complete(next(iter(pool.jobs)))}, set()

    def export(match, output, *, index):
        outputs.append(output)
        return [output / "one.parquet", output / "two.parquet"]

    monkeypatch.setattr(batch, "wait", wait)
    monkeypatch.setattr(gem, "to_parquet", export)
    written = gem.parse_many_to_parquet(paths, tmp_path, workers=2, progress=False)
    assert outputs == [tmp_path / "0", tmp_path / "0", tmp_path / "1"]
    assert written == [
        output / name for output in outputs for name in ["one.parquet", "two.parquet"]
    ]
