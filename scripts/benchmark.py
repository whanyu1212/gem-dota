"""Benchmark script for gem replay parsing performance.

Measures end-to-end parse time and optionally per-phase breakdown across
one or more replay files.  Produces a reproducible baseline so that each
optimisation attempt can be measured against it.

Phases tracked
--------------
The inner parse loop is instrumented via lightweight ``time.perf_counter``
wrappers injected at key dispatch points:

  bit_io       — time spent inside ``BitReader`` (read_bits, read_bytes,
                 varint decodes); approximated as total entity-update time
                 minus field-path and field-decode sub-phases.
  field_paths  — Huffman field-path decoding (``read_field_paths``).
  entity_update — full ``on_packet_entities`` handler including field reads
                 and FieldState writes.
  extractors   — ``_on_entity`` callbacks fired for every entity event
                 (PlayerExtractor, CourierExtractor, etc.).
  other        — everything else: protobuf decode, string tables, game
                 events, combat log, post-processing.

Usage
-----
::

    # Quick baseline — one run per file
    uv run python scripts/benchmark.py

    # Average over 3 runs
    uv run python scripts/benchmark.py --runs 3

    # Single file
    uv run python scripts/benchmark.py --file tests/fixtures/8520062186.dem

    # Full cProfile dump (slowest but most detailed)
    uv run python scripts/benchmark.py --profile

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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"

# Default replay files used when no --file is given.
DEFAULT_FILES: list[Path] = [
    FIXTURES_DIR / "ti14_finals_g1_xg_vs_falcons.dem",
    FIXTURES_DIR / "8520062186.dem",
]


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
        elapsed: Wall-clock seconds for the full parse.
        peak_mb: Peak RSS memory in MB (tracemalloc).
        phases: Per-phase time breakdown.
    """

    elapsed: float
    peak_mb: float
    phases: PhaseBreakdown


@dataclass
class FileResult:
    """Aggregated benchmark result for one replay file.

    Attributes:
        path: Absolute path to the replay file.
        size_mb: File size in megabytes.
        runs: Individual run results.
        mean_s: Mean parse time across all runs.
        min_s: Fastest run.
        mb_per_s: Throughput based on mean time.
        mean_peak_mb: Mean peak memory usage.
        phases: Mean per-phase breakdown.
    """

    path: Path
    size_mb: float
    runs: list[RunResult] = field(default_factory=list)
    mean_s: float = 0.0
    min_s: float = 0.0
    mb_per_s: float = 0.0
    mean_peak_mb: float = 0.0
    phases: PhaseBreakdown = field(default_factory=PhaseBreakdown)

    def summarise(self) -> None:
        """Compute aggregate statistics from individual run results."""
        if not self.runs:
            return
        elapsed = [r.elapsed for r in self.runs]
        self.mean_s = sum(elapsed) / len(elapsed)
        self.min_s = min(elapsed)
        self.mb_per_s = self.size_mb / self.mean_s if self.mean_s > 0 else 0.0
        self.mean_peak_mb = sum(r.peak_mb for r in self.runs) / len(self.runs)
        self.phases = PhaseBreakdown(
            entity_update=sum(r.phases.entity_update for r in self.runs) / len(self.runs),
            extractors=sum(r.phases.extractors for r in self.runs) / len(self.runs),
            other=sum(r.phases.other for r in self.runs) / len(self.runs),
            total=self.mean_s,
        )


# ---------------------------------------------------------------------------
# Instrumented parse
# ---------------------------------------------------------------------------


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
    import gem
    from gem.entities import EntityManager
    from gem.extractors.players import PlayerExtractor

    phase = PhaseBreakdown()

    # --- Patch EntityManager.on_packet_entities ---
    from typing import Any

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
    tracemalloc.start()
    t_start = time.perf_counter()

    gem.parse(str(path))

    elapsed = time.perf_counter() - t_start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Restore originals ---
    EntityManager.on_packet_entities = _orig_ope  # type: ignore[method-assign]
    PlayerExtractor._on_entity = _orig_oe  # type: ignore[method-assign]

    phase.total = elapsed
    phase.other = max(0.0, elapsed - phase.entity_update - phase.extractors)

    return RunResult(
        elapsed=elapsed,
        peak_mb=peak / 1024 / 1024,
        phases=phase,
    )


# ---------------------------------------------------------------------------
# cProfile run
# ---------------------------------------------------------------------------


def _parse_profile(path: Path, top_n: int = 25) -> None:
    """Run gem.parse() under cProfile and print the top N hottest call sites.

    Args:
        path: Path to the .dem replay file.
        top_n: Number of functions to show in the profile report.
    """
    import cProfile
    import io
    import pstats

    import gem

    pr = cProfile.Profile()
    pr.enable()
    gem.parse(str(path))
    pr.disable()

    buf = io.StringIO()
    ps = pstats.Stats(pr, stream=buf).sort_stats("cumulative")
    ps.print_stats(top_n)
    print(buf.getvalue())


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _bar(fraction: float, width: int = 20) -> str:
    """Return a simple ASCII progress bar for a fraction 0.0–1.0."""
    filled = round(fraction * width)
    return "█" * filled + "░" * (width - filled)


def print_results(results: list[FileResult], n_runs: int) -> None:
    """Print a Rich-formatted benchmark summary table.

    Args:
        results: One ``FileResult`` per replay file.
        n_runs: Number of runs performed per file.
    """
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()
    console.print()
    console.print(
        Panel(
            f"[bold cyan]gem benchmark[/]  ·  {n_runs} run(s) per file",
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
    summary.add_column("Peak RAM", justify="right")

    for r in results:
        mean_style = "green" if r.mean_s < 30 else "yellow" if r.mean_s < 120 else "red"
        summary.add_row(
            r.path.name,
            f"{r.size_mb:.1f} MB",
            f"[{mean_style}]{r.mean_s:.1f} s[/]",
            f"{r.min_s:.1f} s",
            f"{r.mb_per_s:.2f} MB/s",
            f"{r.mean_peak_mb:.0f} MB",
        )

    console.print("[bold]Summary[/]")
    console.print(summary)

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
            "size_mb": round(r.size_mb, 2),
            "mean_s": round(r.mean_s, 3),
            "min_s": round(r.min_s, 3),
            "mb_per_s": round(r.mb_per_s, 3),
            "mean_peak_mb": round(r.mean_peak_mb, 1),
            "phases": {
                "entity_update_s": round(r.phases.entity_update, 3),
                "extractors_s": round(r.phases.extractors, 3),
                "other_s": round(r.phases.other, 3),
            },
            "runs": [
                {
                    "elapsed_s": round(run.elapsed, 3),
                    "peak_mb": round(run.peak_mb, 1),
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
        "--json",
        action="store_true",
        help="Output results as JSON instead of Rich tables.",
    )
    args = parser.parse_args()

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
        _parse_profile(target, top_n=args.profile_top)
        return

    # Benchmark mode
    sys.path.insert(0, str(REPO_ROOT / "src"))
    results: list[FileResult] = []

    for path in files:
        size_mb = path.stat().st_size / 1024 / 1024
        fr = FileResult(path=path, size_mb=size_mb)
        print(f"Benchmarking {path.name} ({size_mb:.1f} MB) × {args.runs} run(s) ...")

        for i in range(args.runs):
            print(f"  run {i + 1}/{args.runs} ...", end=" ", flush=True)
            run = _parse_instrumented(path)
            fr.runs.append(run)
            print(f"{run.elapsed:.1f} s  peak={run.peak_mb:.0f} MB")

        fr.summarise()
        results.append(fr)

    if args.json:
        print_json_results(results)
    else:
        print_results(results, n_runs=args.runs)


if __name__ == "__main__":
    main()
