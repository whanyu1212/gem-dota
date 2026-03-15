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

All three functions use ``ProcessPoolExecutor`` for true parallelism (CPU-bound
work) and display a Rich progress bar by default.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

    from gem.models import ParsedMatch


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------


@dataclass
class ParseResult:
    """Outcome of parsing a single replay.

    Args:
        path: Absolute path to the ``.dem`` file.
        match: Populated :class:`~gem.models.ParsedMatch`, or ``None`` on failure.
        error: Exception raised during parsing, or ``None`` on success.
    """

    path: Path
    match: ParsedMatch | None
    error: Exception | None

    @property
    def ok(self) -> bool:
        """Return ``True`` when parsing succeeded."""
        return self.error is None


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
        timeout: Per-replay timeout in seconds.  ``None`` means no limit.

    Returns:
        List of :class:`ParseResult` in completion order.  Failed replays have
        ``result.ok == False`` and carry the exception in ``result.error``.
    """
    paths = _collect_paths(source, recursive=recursive)
    n_workers = min(workers or os.cpu_count() or 1, len(paths))

    results: list[ParseResult] = []

    if progress:
        from rich.progress import (
            BarColumn,
            MofNCompleteColumn,
            Progress,
            TextColumn,
            TimeElapsedColumn,
        )

        rich_progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
    else:
        rich_progress = None

    def _run(executor: ProcessPoolExecutor) -> None:
        future_to_path: dict[Future[tuple], Path] = {
            executor.submit(_parse_one, p): p for p in paths
        }
        for future in as_completed(future_to_path, timeout=timeout):
            path, match, error = future.result()
            results.append(ParseResult(path=path, match=match, error=error))
            if rich_progress is not None:
                rich_progress.advance(task_id)

    def _execute() -> None:
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            _run(pool)

    if rich_progress is not None:
        with rich_progress:
            task_id = rich_progress.add_task(
                f"[cyan]Parsing {len(paths)} replay(s)…[/cyan]", total=len(paths)
            )
            _execute()
    else:
        _execute()

    return results


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
        timeout: Per-replay timeout in seconds.

    Returns:
        ``dict[str, DataFrame]`` with the same keys as
        :func:`~gem.parse_to_dataframe`, containing rows from all successful
        replays concatenated together.
    """
    import pandas as pd

    from gem.dataframes import build_dataframes

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
        timeout: Per-replay timeout in seconds.
        index: Whether to include the DataFrame index in parquet output.

    Returns:
        List of all parquet file paths written.
    """
    from gem import to_parquet

    results = parse_many(
        source, workers=workers, recursive=recursive, progress=progress, timeout=timeout
    )

    out_root = Path(output_dir)
    written: list[Path] = []

    for result in results:
        if not result.ok or result.match is None:
            continue
        subdir = out_root / result.path.stem
        written.extend(to_parquet(result.match, subdir, index=index))

    return written
