"""Bulk replay parsing — process many ``.dem`` files in parallel.

Provides three public functions:

- :func:`parse_many` — parse a list/folder of replays, return
  ``list[ParseResult]``.
- :func:`parse_many_to_dataframe` — same, but concatenate all successful
  results into a ``dict[str, DataFrame]`` (one row-set per table, with a
  ``match_path`` column added for provenance).
- :func:`parse_many_to_parquet` — parse-and-write each replay into its own
  subdirectory under ``output_dir``, one ``.parquet`` file per table.
  Replays are processed and discarded one at a time to keep memory bounded.

All three functions use worker processes for true parallelism (CPU-bound work)
and display a Rich progress bar by default. Optional timeouts are enforced per
replay with portable worker termination.
"""

from __future__ import annotations

import multiprocessing as mp
import os
import queue
import time
from collections import deque
from collections.abc import Iterator, Sequence
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from gem.errors import ReplayParseError, ReplayTimeoutError

if TYPE_CHECKING:
    import pandas as pd

    from gem.results.models import ParsedMatch


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------


@dataclass
class ParseResult:
    """Outcome of parsing a single replay.

    Args:
        path: Absolute path to the ``.dem`` file.
        match: Populated :class:`~gem.results.models.ParsedMatch`, or ``None`` on failure.
        error: Exception raised during parsing, or ``None`` on success.
    """

    path: Path
    match: ParsedMatch | None
    error: Exception | None

    @property
    def ok(self) -> bool:
        """Return ``True`` when parsing succeeded."""
        return self.error is None

    @property
    def error_type(self) -> str:
        """Return a stable display type for the parse error, or ``""`` on success."""
        return type(self.error).__name__ if self.error is not None else ""

    @property
    def error_message(self) -> str:
        """Return a display message for the parse error, or ``""`` on success."""
        return str(self.error) if self.error is not None else ""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _collect_paths(
    source: str | Path | Sequence[str | Path],
    *,
    recursive: bool,
) -> list[Path]:
    """Resolve *source* to a flat list of ``.dem`` paths.

    Args:
        source: A single directory path, or an explicit list of replay paths.
        recursive: When *source* is a directory, whether to scan recursively.

    Returns:
        Sorted list of resolved ``.dem`` :class:`~pathlib.Path` objects.

    Raises:
        ValueError: If *source* is a directory that contains no ``.dem`` files.
    """
    if isinstance(source, (str, Path)):
        root = Path(source)
        if root.is_dir():
            pattern = "**/*.dem" if recursive else "*.dem"
            paths = sorted(root.glob(pattern))
            if not paths:
                raise ValueError(f"No .dem files found in {root}")
            return paths
        # Treat a single file path as a one-element list
        return [root]

    return [Path(p) for p in source]


def _validate_timeout(timeout: float | None) -> None:
    if timeout is None:
        return
    if timeout <= 0:
        raise ValueError("timeout must be a positive number of seconds")


def _parse_one(path: Path) -> tuple[Path, ParsedMatch | None, Exception | None]:
    """Top-level worker function — must be importable at module level for pickling.

    Args:
        path: Path to the ``.dem`` replay file.

    Returns:
        Tuple of ``(path, match_or_None, exception_or_None)``.
    """
    try:
        from gem import parse  # local import — each worker process loads gem fresh

        return path, parse(path), None
    except Exception as exc:  # noqa: BLE001
        return path, None, exc


@dataclass
class _ActiveParseWorker:
    """One running replay parse process used for cross-platform timeouts."""

    path: Path
    process: mp.Process
    queue: Any
    started_at: float


def _parse_one_process(path: Path, result_queue: Any) -> None:
    """Run one parse in a child process and send the result through a queue."""
    result_queue.put(_parse_one(path))


def _timeout_error(path: Path, timeout: float) -> ReplayTimeoutError:
    """Build the public timeout error for one replay."""
    return ReplayTimeoutError(f"Parsing {path} timed out after {timeout:g} seconds")


def _stop_process(process: mp.Process) -> None:
    """Terminate a timed-out worker process and wait briefly for exit."""
    if process.is_alive():
        process.terminate()
        process.join(timeout=1)
    if process.is_alive() and hasattr(process, "kill"):
        process.kill()
        process.join(timeout=1)


def _close_queue(result_queue: Any) -> None:
    """Close a multiprocessing queue without surfacing cleanup errors."""
    with suppress(Exception):
        result_queue.close()
    with suppress(Exception):
        result_queue.join_thread()


def _result_from_worker(worker: _ActiveParseWorker) -> ParseResult | None:
    """Return a completed worker result, or ``None`` if it is still running."""
    try:
        result_path, match, error = worker.queue.get_nowait()
    except queue.Empty:
        if worker.process.is_alive():
            return None
        worker.process.join()
        try:
            result_path, match, error = worker.queue.get_nowait()
        except queue.Empty:
            error = ReplayParseError(
                f"Worker exited without returning a result (exit code {worker.process.exitcode})"
            )
            return ParseResult(path=worker.path, match=None, error=error)
    else:
        worker.process.join()

    return ParseResult(path=result_path, match=match, error=error)


def _timeout_context() -> Any:
    """Return a multiprocessing context suitable for timeout-managed workers."""
    if "fork" in mp.get_all_start_methods():
        return mp.get_context("fork")
    return mp.get_context()


def _iter_parse_results_with_process_timeout(
    paths: Sequence[Path],
    *,
    workers: int,
    timeout: float,
) -> Iterator[ParseResult]:
    """Yield parse results using one process per replay so timeouts are portable."""
    ctx = _timeout_context()
    pending = deque(paths)
    active: list[_ActiveParseWorker] = []

    def _submit_next() -> None:
        if not pending:
            return
        path = pending.popleft()
        result_queue = ctx.Queue(maxsize=1)
        process = ctx.Process(target=_parse_one_process, args=(path, result_queue))
        process.start()
        active.append(
            _ActiveParseWorker(
                path=path,
                process=process,
                queue=result_queue,
                started_at=time.monotonic(),
            )
        )

    for _ in range(workers):
        _submit_next()

    while active:
        yielded = False
        now = time.monotonic()
        for worker in list(active):
            result = _result_from_worker(worker)
            if result is not None:
                active.remove(worker)
                _close_queue(worker.queue)
                _submit_next()
                yielded = True
                yield result
                continue

            if now - worker.started_at >= timeout:
                _stop_process(worker.process)
                active.remove(worker)
                _close_queue(worker.queue)
                _submit_next()
                yielded = True
                yield ParseResult(
                    path=worker.path, match=None, error=_timeout_error(worker.path, timeout)
                )

        if not yielded and active:
            time.sleep(0.05)


def _iter_parse_results(
    paths: Sequence[Path],
    *,
    workers: int | None,
    progress: bool,
    timeout: float | None,
) -> Iterator[ParseResult]:
    """Yield parse results as worker futures complete, with bounded in-flight work."""
    _validate_timeout(timeout)
    if not paths:
        return

    n_workers = min(workers or os.cpu_count() or 1, len(paths))

    from rich.progress import (
        BarColumn,
        MofNCompleteColumn,
        Progress,
        TaskID,
        TextColumn,
        TimeElapsedColumn,
    )

    rich_progress: Progress | None = (
        Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        if progress
        else None
    )
    task_id: TaskID | None = None

    def _run(executor: ProcessPoolExecutor) -> Iterator[ParseResult]:
        path_iter = iter(paths)
        future_to_path: dict[Future[tuple], Path] = {}

        def _submit_next() -> None:
            try:
                path = next(path_iter)
            except StopIteration:
                return
            future_to_path[executor.submit(_parse_one, path)] = path

        for _ in range(n_workers):
            _submit_next()

        while future_to_path:
            future = next(as_completed(future_to_path))
            path = future_to_path.pop(future)
            try:
                result_path, match, error = future.result()
            except Exception as exc:  # noqa: BLE001
                result_path, match, error = path, None, exc
            _submit_next()
            if rich_progress is not None and task_id is not None:
                rich_progress.advance(task_id)
            yield ParseResult(path=result_path, match=match, error=error)

    def _execute() -> Iterator[ParseResult]:
        if timeout is not None:
            for result in _iter_parse_results_with_process_timeout(
                paths,
                workers=n_workers,
                timeout=timeout,
            ):
                if rich_progress is not None and task_id is not None:
                    rich_progress.advance(task_id)
                yield result
            return

        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            yield from _run(pool)

    if rich_progress is not None:
        with rich_progress:
            task_id = rich_progress.add_task(
                f"[cyan]Parsing {len(paths)} replay(s)…[/cyan]", total=len(paths)
            )
            yield from _execute()
    else:
        yield from _execute()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_many(
    source: str | Path | Sequence[str | Path],
    *,
    workers: int | None = None,
    recursive: bool = False,
    progress: bool = True,
    timeout: float | None = None,
) -> list[ParseResult]:
    """Parse multiple replays in parallel and return a result per replay.

    Args:
        source: Either a directory path (all ``.dem`` files inside) or an
            explicit list of replay paths.
        workers: Number of worker processes.  Defaults to ``os.cpu_count()``,
            capped at the number of replays.
        recursive: When *source* is a directory, scan subdirectories too.
        progress: Show a Rich progress bar while parsing.
        timeout: Per-replay parsing timeout in seconds, enforced after a worker
            starts a replay on platforms with ``signal.SIGALRM``/``setitimer``.
            Timed-out replays return ``ParseResult(error=TimeoutError(...))``.
            Unsupported platforms raise once before workers start. ``None`` means
            no limit.

    Returns:
        List of :class:`ParseResult` in completion order.  Failed replays have
        ``result.ok == False`` and carry the exception in ``result.error``.
    """
    paths = _collect_paths(source, recursive=recursive)
    return list(
        _iter_parse_results(
            paths,
            workers=workers,
            progress=progress,
            timeout=timeout,
        )
    )


def parse_many_to_dataframe(
    source: str | Path | Sequence[str | Path],
    *,
    workers: int | None = None,
    recursive: bool = False,
    progress: bool = True,
    timeout: float | None = None,
) -> dict[str, pd.DataFrame]:
    """Parse multiple replays and concatenate results into per-table DataFrames.

    Each DataFrame gets a ``match_path`` column added so rows can be traced
    back to their source replay.

    Args:
        source: Directory path or explicit list of replay paths.
        workers: Number of worker processes (default: ``os.cpu_count()``).
        recursive: Scan subdirectories when *source* is a directory.
        progress: Show a Rich progress bar while parsing.
        timeout: Per-replay parsing timeout in seconds.

    Returns:
        ``dict[str, DataFrame]`` with the same keys as
        :func:`~gem.parse_to_dataframe`, containing rows from all successful
        replays concatenated together.
    """
    import pandas as pd

    from gem.results.dataframes import build_dataframes

    results = parse_many(
        source, workers=workers, recursive=recursive, progress=progress, timeout=timeout
    )

    per_table: dict[str, list[pd.DataFrame]] = {}
    for result in results:
        if not result.ok or result.match is None:
            continue
        dfs = build_dataframes(result.match)
        for key, df in dfs.items():
            df = df.copy()
            df.insert(0, "match_path", str(result.path))
            per_table.setdefault(key, []).append(df)

    return {key: pd.concat(frames, ignore_index=True) for key, frames in per_table.items()}


def parse_many_to_parquet(
    source: str | Path | Sequence[str | Path],
    output_dir: str | Path,
    *,
    workers: int | None = None,
    recursive: bool = False,
    progress: bool = True,
    timeout: float | None = None,
    index: bool = False,
) -> list[Path]:
    """Parse multiple replays and write each to its own parquet subdirectory.

    Each replay is written and discarded immediately to keep memory usage
    bounded regardless of batch size.  The output layout is::

        output_dir/
          <replay_stem>/
            players.parquet
            combat_log.parquet
            ...

    Args:
        source: Directory path or explicit list of replay paths.
        output_dir: Root directory to write parquet subdirectories into.
        workers: Number of worker processes (default: ``os.cpu_count()``).
        recursive: Scan subdirectories when *source* is a directory.
        progress: Show a Rich progress bar while parsing.
        timeout: Per-replay parsing timeout in seconds.
        index: Whether to include the DataFrame index in parquet output.

    Returns:
        List of all parquet file paths written.
    """
    from gem import to_parquet

    paths = _collect_paths(source, recursive=recursive)
    out_root = Path(output_dir)
    written: list[Path] = []

    for result in _iter_parse_results(
        paths,
        workers=workers,
        progress=progress,
        timeout=timeout,
    ):
        if not result.ok or result.match is None:
            continue
        subdir = out_root / result.path.stem
        written.extend(to_parquet(result.match, subdir, index=index))

    return written
