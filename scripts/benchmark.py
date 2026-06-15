"""Benchmark script for gem replay parsing performance.

Measures end-to-end parse time across one or more replay files. The default
``plain`` mode times ``gem.parse()`` directly so it is suitable for before/after
optimization baselines. The optional ``instrumented`` mode adds lightweight
phase probes and Python heap tracking to explain where time is going.

Instrumented phases
-------------------
``instrumented`` mode monkey-patches a few dispatch points with
``time.perf_counter`` wrappers:

  entity_update - full ``on_packet_entities`` handler including field reads
                  and FieldState writes.
  extractors    - representative ``PlayerExtractor._on_entity`` callback time.
  other         - everything else: protobuf decode, string tables, game events,
                  combat log, post-processing, and uninstrumented callbacks.

This script does not claim direct ``BitReader`` timing. Use ``--profile`` first
to prove whether binary helpers are hot before optimizing them.

Usage
-----
::

    # Quick baseline — one run per file
    uv run python scripts/benchmark.py

    # Average over 3 runs
    uv run python scripts/benchmark.py --runs 3

    # Coarse phase breakdown with monkey-patched probes
    uv run python scripts/benchmark.py --mode instrumented --runs 3

    # Single file
    uv run python scripts/benchmark.py --file tests/fixtures/opendota/8822520406.dem

    # Full cProfile dump (slowest but most detailed)
    uv run python scripts/benchmark.py --profile --profile-sort cumulative

    # Save cProfile binary stats outside the repo
    uv run python scripts/benchmark.py --profile --profile-output /tmp/gem-profiles

    # Machine-readable JSON output
    uv run python scripts/benchmark.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import tracemalloc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

ParseMode = Literal["plain", "instrumented"]
ProfileSort = Literal["cumulative", "tottime", "calls"]

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
OPENDOTA_FIXTURES_DIR = FIXTURES_DIR / "opendota"

# Default replay files used when no --file is given.
DEFAULT_FILES: list[Path] = [
    OPENDOTA_FIXTURES_DIR / "8822520406.dem",
    OPENDOTA_FIXTURES_DIR / "8822593932.dem",
]


def _ensure_src_path() -> None:
    """Make local ``src/`` imports win when running from a checkout."""
    src_path = str(REPO_ROOT / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass
class PhaseBreakdown:
    """Wall-clock time (seconds) spent in each parse phase.

    Attributes:
        entity_update: Time inside ``on_packet_entities`` — the dominant cost.
        extractors: Time in extractor ``_on_entity`` callbacks.
        other: Everything else (protobuf, string tables, game events, post-processing).
        total: Total end-to-end parse time including gem.parse() overhead.
    """

    entity_update: float = 0.0
    extractors: float = 0.0
    other: float = 0.0
    total: float = 0.0


@dataclass
class RunResult:
    """Result of a single parse run.

    Attributes:
        mode: Benchmark mode used for this run.
        elapsed: Wall-clock seconds for the full parse.
        peak_mb: Peak Python heap in MB from ``tracemalloc`` when available.
        phases: Per-phase time breakdown.
    """

    mode: ParseMode
    elapsed: float
    peak_mb: float | None
    phases: PhaseBreakdown


@dataclass
class FileResult:
    """Aggregated benchmark result for one replay file.

    Attributes:
        path: Absolute path to the replay file.
        size_mb: File size in megabytes.
        mode: Benchmark mode used for all runs.
        runs: Individual run results.
        mean_s: Mean parse time across all runs.
        min_s: Fastest run.
        mb_per_s: Throughput based on mean time.
        mean_peak_mb: Mean peak Python heap when available.
        phases: Mean per-phase breakdown.
    """

    path: Path
    size_mb: float
    mode: ParseMode
    runs: list[RunResult] = field(default_factory=list)
    mean_s: float = 0.0
    min_s: float = 0.0
    mb_per_s: float = 0.0
    mean_peak_mb: float | None = None
    phases: PhaseBreakdown = field(default_factory=PhaseBreakdown)

    def summarise(self) -> None:
        """Compute aggregate statistics from individual run results."""
        if not self.runs:
            return
        elapsed = [r.elapsed for r in self.runs]
        self.mean_s = sum(elapsed) / len(elapsed)
        self.min_s = min(elapsed)
        self.mb_per_s = self.size_mb / self.mean_s if self.mean_s > 0 else 0.0
        peak_values = [r.peak_mb for r in self.runs if r.peak_mb is not None]
        self.mean_peak_mb = sum(peak_values) / len(peak_values) if peak_values else None
        self.phases = PhaseBreakdown(
            entity_update=sum(r.phases.entity_update for r in self.runs) / len(self.runs),
            extractors=sum(r.phases.extractors for r in self.runs) / len(self.runs),
            other=sum(r.phases.other for r in self.runs) / len(self.runs),
            total=self.mean_s,
        )


# ---------------------------------------------------------------------------
# Parse runners
# ---------------------------------------------------------------------------


def _parse_plain(path: Path) -> RunResult:
    """Run ``gem.parse()`` with minimal benchmark overhead.

    Args:
        path: Path to the .dem replay file.

    Returns:
        A ``RunResult`` with elapsed wall-clock time.
    """
    _ensure_src_path()

    import gem

    t_start = time.perf_counter()
    gem.parse(str(path))
    elapsed = time.perf_counter() - t_start

    return RunResult(
        mode="plain",
        elapsed=elapsed,
        peak_mb=None,
        phases=PhaseBreakdown(total=elapsed),
    )


def _parse_instrumented(path: Path) -> RunResult:
    """Run gem.parse() with lightweight timing probes and memory tracking.

    Monkey-patches ``EntityManager.on_packet_entities`` and the extractor
    ``_on_entity`` dispatch point to record wall-clock time per phase.
    The patches are removed after the parse completes.

    Args:
        path: Path to the .dem replay file.

    Returns:
        A ``RunResult`` with elapsed time, peak memory, and phase breakdown.
    """
    _ensure_src_path()

    import gem
    from gem.extractors.players import PlayerExtractor
    from gem.state.entities import EntityManager

    phase = PhaseBreakdown()

    # --- Patch EntityManager.on_packet_entities ---
    _orig_ope: Any = EntityManager.on_packet_entities

    def _timed_ope(self: EntityManager, *args: object, **kwargs: object) -> None:
        t0 = time.perf_counter()
        _orig_ope(self, *args, **kwargs)
        phase.entity_update += time.perf_counter() - t0

    EntityManager.on_packet_entities = _timed_ope  # type: ignore[assignment,method-assign]

    # --- Patch PlayerExtractor._on_entity (representative extractor) ---
    _orig_oe: Any = PlayerExtractor._on_entity

    def _timed_oe(self: PlayerExtractor, *args: object, **kwargs: object) -> None:
        t0 = time.perf_counter()
        _orig_oe(self, *args, **kwargs)
        phase.extractors += time.perf_counter() - t0

    PlayerExtractor._on_entity = _timed_oe  # type: ignore[method-assign]

    # --- Run parse with memory tracking ---
    try:
        tracemalloc.start()
        t_start = time.perf_counter()
        gem.parse(str(path))
        elapsed = time.perf_counter() - t_start
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
        EntityManager.on_packet_entities = _orig_ope  # type: ignore[method-assign]
        PlayerExtractor._on_entity = _orig_oe  # type: ignore[method-assign]

    phase.total = elapsed
    phase.other = max(0.0, elapsed - phase.entity_update - phase.extractors)

    return RunResult(
        mode="instrumented",
        elapsed=elapsed,
        peak_mb=peak / 1024 / 1024,
        phases=phase,
    )


def _parse_once(path: Path, mode: ParseMode) -> RunResult:
    """Run one parse benchmark in the requested mode."""
    if mode == "plain":
        return _parse_plain(path)
    return _parse_instrumented(path)


# ---------------------------------------------------------------------------
# cProfile run
# ---------------------------------------------------------------------------


def _resolve_profile_output(
    path: Path, output_arg: str | None, sort_by: ProfileSort
) -> Path | None:
    """Resolve an optional profile output file or directory."""
    if output_arg is None:
        return None

    output = Path(output_arg)
    if output.suffix:
        output.parent.mkdir(parents=True, exist_ok=True)
        return output

    output.mkdir(parents=True, exist_ok=True)
    return output / f"{path.stem}-{sort_by}.prof"


def _parse_profile(
    path: Path,
    *,
    top_n: int = 25,
    sort_by: ProfileSort = "cumulative",
    output: Path | None = None,
) -> None:
    """Run gem.parse() under cProfile and print the top N hottest call sites.

    Args:
        path: Path to the .dem replay file.
        top_n: Number of functions to show in the profile report.
        sort_by: pstats sort key.
        output: Optional path for binary cProfile stats.
    """
    import cProfile
    import io
    import pstats

    _ensure_src_path()

    import gem

    pr = cProfile.Profile()
    pr.enable()
    try:
        gem.parse(str(path))
    finally:
        pr.disable()

    if output is not None:
        pr.dump_stats(output)
        print(f"Saved cProfile stats to {output}")

    buf = io.StringIO()
    ps = pstats.Stats(pr, stream=buf).strip_dirs().sort_stats(sort_by)
    ps.print_stats(top_n)
    print(buf.getvalue())


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _bar(fraction: float, width: int = 20) -> str:
    """Return a simple ASCII progress bar for a fraction 0.0–1.0."""
    filled = round(fraction * width)
    return "█" * filled + "░" * (width - filled)


def print_results(results: list[FileResult], n_runs: int, mode: ParseMode) -> None:
    """Print a Rich-formatted benchmark summary table.

    Args:
        results: One ``FileResult`` per replay file.
        n_runs: Number of runs performed per file.
        mode: Benchmark mode used.
    """
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()
    console.print()
    console.print(
        Panel(
            f"[bold cyan]gem benchmark[/]  ·  {mode} mode  ·  {n_runs} run(s) per file",
            style="cyan",
        )
    )

    # --- Summary table ---
    summary = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold")
    summary.add_column("File", style="dim")
    summary.add_column("Size", justify="right")
    summary.add_column("Mean", justify="right")
    summary.add_column("Best", justify="right")
    summary.add_column("Throughput", justify="right")
    if mode == "instrumented":
        summary.add_column("Peak heap", justify="right")

    for r in results:
        mean_style = "green" if r.mean_s < 30 else "yellow" if r.mean_s < 120 else "red"
        row = [
            r.path.name,
            f"{r.size_mb:.1f} MB",
            f"[{mean_style}]{r.mean_s:.1f} s[/]",
            f"{r.min_s:.1f} s",
            f"{r.mb_per_s:.2f} MB/s",
        ]
        if mode == "instrumented":
            peak = f"{r.mean_peak_mb:.0f} MB" if r.mean_peak_mb is not None else "n/a"
            row.append(peak)
        summary.add_row(*row)

    console.print("[bold]Summary[/]")
    console.print(summary)

    if mode != "instrumented":
        return

    # --- Phase breakdown per file ---
    for r in results:
        p = r.phases
        total = r.mean_s or 1.0
        breakdown = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
        breakdown.add_column("Phase")
        breakdown.add_column("Time", justify="right")
        breakdown.add_column("Share", justify="right")
        breakdown.add_column("", no_wrap=True)

        def _row(name: str, t: float, _total: float = total, _breakdown: Table = breakdown) -> None:
            frac = t / _total
            _breakdown.add_row(
                name,
                f"{t:.2f} s",
                f"{frac * 100:.1f}%",
                _bar(frac),
            )

        _row("entity_update", p.entity_update)
        _row("extractors", p.extractors)
        _row("other", p.other)

        console.print(f"\n[bold]{r.path.name}[/] — phase breakdown (mean over {n_runs} run(s))")
        console.print(breakdown)


def print_json_results(results: list[FileResult]) -> None:
    """Print benchmark results as JSON for machine consumption.

    Args:
        results: One ``FileResult`` per replay file.
    """

    def _serialise(r: FileResult) -> dict:
        return {
            "file": str(r.path),
            "mode": r.mode,
            "size_mb": round(r.size_mb, 2),
            "mean_s": round(r.mean_s, 3),
            "min_s": round(r.min_s, 3),
            "mb_per_s": round(r.mb_per_s, 3),
            "mean_peak_mb": (round(r.mean_peak_mb, 1) if r.mean_peak_mb is not None else None),
            "phases": (
                {
                    "entity_update_s": round(r.phases.entity_update, 3),
                    "extractors_s": round(r.phases.extractors, 3),
                    "other_s": round(r.phases.other, 3),
                }
                if r.mode == "instrumented"
                else None
            ),
            "runs": [
                {
                    "mode": run.mode,
                    "elapsed_s": round(run.elapsed, 3),
                    "peak_mb": round(run.peak_mb, 1) if run.peak_mb is not None else None,
                }
                for run in r.runs
            ],
        }

    print(json.dumps([_serialise(r) for r in results], indent=2))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for the benchmark script."""
    parser = argparse.ArgumentParser(
        description="Benchmark gem replay parsing performance.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage")[1] if "Usage" in (__doc__ or "") else "",
    )
    parser.add_argument(
        "--file",
        action="append",
        metavar="PATH",
        help="Replay file to benchmark (repeatable). Defaults to both fixture files.",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        metavar="N",
        help="Number of parse runs per file (default: 1).",
    )
    parser.add_argument(
        "--mode",
        choices=("plain", "instrumented"),
        default="plain",
        help=(
            "Benchmark mode: 'plain' times gem.parse() directly; "
            "'instrumented' adds phase probes and tracemalloc (default: plain)."
        ),
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Run cProfile on the first file and print the top hottest call sites.",
    )
    parser.add_argument(
        "--profile-top",
        type=int,
        default=25,
        metavar="N",
        help="Number of functions to show in cProfile output (default: 25).",
    )
    parser.add_argument(
        "--profile-sort",
        choices=("cumulative", "tottime", "calls"),
        default="cumulative",
        help="pstats sort key for --profile output (default: cumulative).",
    )
    parser.add_argument(
        "--profile-output",
        metavar="PATH",
        help=(
            "Optional cProfile stats output file or directory. "
            "Use /tmp/gem-profiles to keep generated files out of the repo."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of Rich tables.",
    )
    args = parser.parse_args()
    mode: ParseMode = args.mode
    profile_sort: ProfileSort = args.profile_sort

    if args.runs < 1:
        print("ERROR: --runs must be >= 1", file=sys.stderr)
        sys.exit(1)

    files = [Path(f) for f in args.file] if args.file else DEFAULT_FILES
    missing = [f for f in files if not f.exists()]
    if missing:
        for f in missing:
            print(f"ERROR: file not found: {f}", file=sys.stderr)
        sys.exit(1)

    # cProfile mode — single file, single run, no benchmark table
    if args.profile:
        target = files[0]
        print(f"Profiling {target.name} ({target.stat().st_size / 1024**2:.1f} MB) ...")
        profile_output = _resolve_profile_output(
            target,
            args.profile_output,
            profile_sort,
        )
        _parse_profile(
            target,
            top_n=args.profile_top,
            sort_by=profile_sort,
            output=profile_output,
        )
        return

    # Benchmark mode
    results: list[FileResult] = []
    progress_stream = sys.stderr if args.json else sys.stdout

    for path in files:
        size_mb = path.stat().st_size / 1024 / 1024
        fr = FileResult(path=path, size_mb=size_mb, mode=mode)
        print(
            f"Benchmarking {path.name} ({size_mb:.1f} MB) × {args.runs} run(s) [{mode}] ...",
            file=progress_stream,
        )

        for i in range(args.runs):
            print(
                f"  run {i + 1}/{args.runs} ...",
                end=" ",
                flush=True,
                file=progress_stream,
            )
            run = _parse_once(path, mode)
            fr.runs.append(run)
            if run.peak_mb is None:
                print(f"{run.elapsed:.1f} s", file=progress_stream)
            else:
                print(
                    f"{run.elapsed:.1f} s  peak_heap={run.peak_mb:.0f} MB",
                    file=progress_stream,
                )

        fr.summarise()
        results.append(fr)

    if args.json:
        print_json_results(results)
    else:
        print_results(results, n_runs=args.runs, mode=mode)


if __name__ == "__main__":
    main()
