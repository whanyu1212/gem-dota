"""CLI entry point: ``python -m gem <replay.dem>``.

Parses a replay file and prints a summary of key statistics by default.
Supports JSON and parquet export modes.

Subcommands
-----------
``parse``  (default)
    Parse a single replay — summary, JSON, or parquet output.

``batch``
    Parse many replays in parallel — parquet or dataframe output.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from rich.align import Align
from rich.box import HEAVY
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TaskID, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from gem import __version__, parse, parse_to_json, parse_to_parquet
from gem.models import ParsedMatch

# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gem",
        description="Parse Dota 2 Source 2 replays (.dem).",
        epilog=(
            "Examples:\n"
            "  python -m gem match.dem\n"
            "  python -m gem match.dem --format json\n"
            "  python -m gem parse match.dem --format parquet --output ./out\n"
            "  python -m gem batch replays/ --format parquet --output ./out\n"
            "  python -m gem batch replays/ --format dataframe --output ./out\n"
            "  python -m gem batch replays/ --workers 4 --recursive\n"
            "  python -m gem parse match.dem --progress --timings"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    # ── parse subcommand ────────────────────────────────────────────────────
    parse_cmd = subparsers.add_parser(
        "parse",
        help="Parse a single replay file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parse_cmd.add_argument("path", help="Path to replay file (.dem)")
    parse_cmd.add_argument(
        "--format",
        dest="format",
        choices=("summary", "json", "parquet"),
        default="summary",
        help="Output format (default: summary)",
    )
    parse_cmd.add_argument(
        "--output",
        type=Path,
        help="Output file (json) or directory (parquet). Omit for json to print to stdout.",
    )
    _add_common_flags(parse_cmd)

    # ── batch subcommand ────────────────────────────────────────────────────
    batch_cmd = subparsers.add_parser(
        "batch",
        help="Parse many replays in parallel.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    batch_cmd.add_argument(
        "source",
        help="Directory of .dem files, or a space-separated list of paths.",
        nargs="+",
    )
    batch_cmd.add_argument(
        "--format",
        dest="format",
        choices=("parquet", "dataframe"),
        default="parquet",
        help="Output format: parquet (one subdir per replay) or dataframe (concatenated, requires --output). Default: parquet",
    )
    batch_cmd.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory.",
    )
    batch_cmd.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel worker processes (default: os.cpu_count()).",
    )
    batch_cmd.add_argument(
        "--recursive",
        action="store_true",
        help="Scan source directory recursively for .dem files.",
    )
    _add_common_flags(batch_cmd)

    return parser


def _add_common_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress banner and non-essential messages."
    )
    p.add_argument("--no-banner", action="store_true", help="Hide ASCII art banner.")
    p.add_argument("--progress", action="store_true", help="Show live progress.")
    p.add_argument("--timings", action="store_true", help="Show timing breakdown at the end.")


# ---------------------------------------------------------------------------
# Phase tracker
# ---------------------------------------------------------------------------

_PHASE_LABELS: dict[str, str] = {
    "parse": "Parsing replay",
    "render_summary": "Rendering summary",
    "parse_serialize_json": "Parsing & serialising JSON",
    "write_json": "Writing JSON file",
    "parse_export_parquet": "Parsing & exporting Parquet",
    "batch_parquet": "Batch → Parquet",
    "batch_dataframe": "Batch → DataFrame",
    "write_dataframe": "Writing DataFrames",
}


class _PhaseTracker:
    """Tracks per-phase durations and renders Rich progress/timing output."""

    def __init__(self, *, progress: bool, timings: bool, console: Console) -> None:
        self._show_progress = progress
        self._timings = timings
        self._console = console
        self._t0 = time.perf_counter()
        self._active: dict[str, float] = {}
        self._durations: dict[str, float] = {}
        self._progress_ctx: Progress | None = None
        self._task_ids: dict[str, TaskID] = {}

        if self._show_progress:
            self._progress_ctx = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
                transient=False,
            )
            self._progress_ctx.start()

    def start(self, name: str) -> None:
        self._active[name] = time.perf_counter()
        if self._progress_ctx is not None:
            label = _PHASE_LABELS.get(name, name)
            task_id = self._progress_ctx.add_task(f"[cyan]{label}…[/cyan]", total=None)
            self._task_ids[name] = task_id

    def end(self, name: str) -> None:
        start = self._active.pop(name, None)
        if start is None:
            return
        elapsed = time.perf_counter() - start
        self._durations[name] = self._durations.get(name, 0.0) + elapsed

        if self._progress_ctx is not None:
            task_id = self._task_ids.pop(name, None)
            if task_id is not None:
                label = _PHASE_LABELS.get(name, name)
                self._progress_ctx.update(
                    task_id,
                    description=f"[green]✓[/green] [bold]{label}[/bold]",
                    completed=1,
                    total=1,
                )

    def report(self) -> None:
        if self._progress_ctx is not None:
            self._progress_ctx.stop()

        if not self._timings:
            return

        total = time.perf_counter() - self._t0

        table = Table(title="Timing summary", show_header=True, header_style="bold magenta")
        table.add_column("Phase", style="cyan", no_wrap=True)
        table.add_column("Elapsed", justify="right", style="green")

        for name, elapsed in self._durations.items():
            label = _PHASE_LABELS.get(name, name)
            table.add_row(label, f"{elapsed:.3f}s")

        table.add_section()
        table.add_row("[bold]Total[/bold]", f"[bold]{total:.3f}s[/bold]")

        self._console.print()
        self._console.print(table)


# ---------------------------------------------------------------------------
# Banner & summary
# ---------------------------------------------------------------------------


def _print_banner(console: Console) -> None:
    B, S = "██", "  "
    _G = [[S, B, B, B, S], [B, S, S, S, S], [B, S, B, B, B], [B, S, S, S, B], [S, B, B, B, B]]
    _E = [[B, B, B, B], [B, S, S, S], [B, B, B, S], [B, S, S, S], [B, B, B, B]]
    _M = [[B, S, S, S, B], [B, B, S, B, B], [B, S, B, S, B], [B, S, S, S, B], [B, S, S, S, B]]

    palette = ["color(213)", "color(177)", "color(141)", "color(105)", "color(69)"]
    gap = "    "

    content = Text(justify="center")
    for i in range(5):
        row = gap.join(["".join(_G[i]), "".join(_E[i]), "".join(_M[i])])
        content.append(row + "\n", style=palette[i])
    content.append("\n")
    content.append("From replay bytes to model-ready signals.", style="italic color(117)")

    panel = Panel(
        Align.center(content),
        box=HEAVY,
        border_style="color(213)",
        padding=(1, 4),
        expand=False,
        subtitle=f"[dim color(117)]v{__version__}[/]",
    )
    console.print(Align.center(panel))


def _print_summary(
    match: ParsedMatch, console: Console, *, quiet: bool = False, path: str = ""
) -> None:
    if not quiet:
        console.print(f"[dim]Parsing[/dim] [bold]{path}[/bold] [dim]...[/dim]")

    hero_kills = sum(1 for e in match.combat_log if e.log_type == "DEATH" and e.target_is_hero)
    total_buybacks = sum(len(pp.buyback_log) for pp in match.players)
    total_runes = sum(len(pp.runes_log) for pp in match.players)

    all_ticks = [t for pp in match.players for t in pp.times]
    if all_ticks:
        last_tick = max(all_ticks)
        total_secs = int(last_tick / 30)
        duration_str = f"{total_secs // 60}:{total_secs % 60:02d}"
    else:
        duration_str = "?"

    stats_parts = [
        f"[bold]{hero_kills}[/bold] hero kills",
        f"[bold]{len(match.towers)}[/bold] towers",
        f"[bold]{len(match.barracks)}[/bold] barracks",
        f"[bold]{len(match.roshans)}[/bold] Roshan kill(s)",
        f"[bold]{len(match.aegis_events)}[/bold] aegis event(s)",
        f"[bold]{len(match.wards)}[/bold] wards",
        f"[bold]{total_buybacks}[/bold] buybacks",
        f"[bold]{total_runes}[/bold] runes",
        f"[bold]{len(match.chat)}[/bold] chat msgs",
        f"duration [bold]{duration_str}[/bold]",
    ]
    console.print()
    console.print("  " + "  |  ".join(stats_parts))

    table = Table(show_header=True, header_style="bold")
    table.add_column("Team", width=7)
    table.add_column("Hero", min_width=30)
    table.add_column("LH", justify="right")
    table.add_column("Gold", justify="right")
    table.add_column("Purchases", justify="right")
    table.add_column("Runes", justify="right")
    table.add_column("Buybacks", justify="right")

    for pp in match.players:
        if not pp.hero_name:
            continue
        team_str = "[green]Radiant[/green]" if pp.team == 2 else "[red]Dire[/red]"
        final_gold = pp.gold_t[-1] if pp.gold_t else 0
        final_lh = pp.lh_t[-1] if pp.lh_t else 0
        table.add_row(
            team_str,
            pp.hero_name,
            str(final_lh),
            str(final_gold),
            str(len(pp.purchase_log)),
            str(len(pp.runes_log)),
            str(len(pp.buyback_log)),
        )

    console.print()
    console.print(table)


# ---------------------------------------------------------------------------
# Batch result summary
# ---------------------------------------------------------------------------


def _print_batch_summary(
    results: list,
    console: Console,
    *,
    quiet: bool = False,
) -> None:
    ok = [r for r in results if r.ok]
    failed = [r for r in results if not r.ok]

    if not quiet:
        console.print(
            f"\n[green]✓[/green] [bold]{len(ok)}[/bold] succeeded  "
            f"[red]✗[/red] [bold]{len(failed)}[/bold] failed"
        )

    if failed:
        table = Table(title="Failed replays", show_header=True, header_style="bold red")
        table.add_column("Path", style="dim")
        table.add_column("Error")
        for r in failed:
            table.add_row(str(r.path), str(r.error))
        console.print(table)


# ---------------------------------------------------------------------------
# Single-replay handler
# ---------------------------------------------------------------------------


def _run_parse(args: argparse.Namespace, console: Console) -> None:
    json_to_stdout = args.format == "json" and args.output is None
    tracker = _PhaseTracker(
        progress=args.progress and not args.quiet,
        timings=args.timings,
        console=Console(stderr=True) if json_to_stdout else console,
    )

    try:
        if args.format == "summary":
            tracker.start("parse")
            match = parse(args.path)
            tracker.end("parse")
            tracker.start("render_summary")
            _print_summary(match, console, quiet=args.quiet, path=str(args.path))
            tracker.end("render_summary")

        elif args.format == "json":
            tracker.start("parse_serialize_json")
            payload = parse_to_json(args.path, indent=2)
            tracker.end("parse_serialize_json")

            if args.output is None:
                print(payload)
                return

            tracker.start("write_json")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
            tracker.end("write_json")

            if not args.quiet:
                console.print(f"[green]✓[/green] Wrote JSON: [bold]{args.output}[/bold]")

        else:  # parquet
            if args.output is None:
                Console(stderr=True).print(
                    "[red]Error:[/red] --output is required when --format parquet is selected."
                )
                sys.exit(2)

            tracker.start("parse_export_parquet")
            written = parse_to_parquet(args.path, args.output)
            tracker.end("parse_export_parquet")

            if not args.quiet:
                console.print(
                    f"[green]✓[/green] Wrote [bold]{len(written)}[/bold] "
                    f"parquet file(s) to [bold]{args.output}[/bold]"
                )
    finally:
        tracker.report()


# ---------------------------------------------------------------------------
# Batch handler
# ---------------------------------------------------------------------------


def _run_batch(args: argparse.Namespace, console: Console) -> None:
    from gem.batch import parse_many_to_dataframe, parse_many_to_parquet

    # source is a list (nargs="+") — unwrap to single path if it's a directory
    source: list[Path] | Path = (
        Path(args.source[0]) if len(args.source) == 1 else [Path(p) for p in args.source]
    )

    tracker = _PhaseTracker(
        progress=args.progress and not args.quiet,
        timings=args.timings,
        console=console,
    )

    try:
        if args.format == "parquet":
            tracker.start("batch_parquet")
            # batch already shows its own Rich progress bar; suppress tracker's
            # bar to avoid two overlapping bars when --progress is set
            results = parse_many_to_parquet(
                source,
                args.output,
                workers=args.workers,
                recursive=args.recursive,
                progress=not args.quiet,
            )
            tracker.end("batch_parquet")

            # parse_many_to_parquet returns file paths; recover ParseResults for summary
            # by re-running parse_many (already done internally) — instead, call parse_many
            # directly so we can show the failure table.  For the simple case just report counts.
            if not args.quiet:
                console.print(
                    f"[green]✓[/green] Wrote [bold]{len(results)}[/bold] "
                    f"parquet file(s) to [bold]{args.output}[/bold]"
                )

        else:  # dataframe
            tracker.start("batch_dataframe")
            dfs = parse_many_to_dataframe(
                source,
                workers=args.workers,
                recursive=args.recursive,
                progress=not args.quiet,
            )
            tracker.end("batch_dataframe")

            tracker.start("write_dataframe")
            args.output.mkdir(parents=True, exist_ok=True)
            written = []
            for key, df in dfs.items():
                p = args.output / f"{key}.parquet"
                try:
                    df.to_parquet(p, index=False)
                except ImportError as exc:
                    raise ImportError(
                        "Parquet export requires 'pyarrow' or 'fastparquet'."
                    ) from exc
                written.append(p)
            tracker.end("write_dataframe")

            if not args.quiet:
                console.print(
                    f"[green]✓[/green] Wrote [bold]{len(written)}[/bold] "
                    f"concatenated parquet file(s) to [bold]{args.output}[/bold]"
                )
    finally:
        tracker.report()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse one or many replays and output summary/json/parquet."""
    # Legacy compat: `python -m gem match.dem [--flag ...]`
    # If the first non-flag token isn't a known subcommand, inject "parse" so
    # argparse sees `python -m gem parse match.dem [--flag ...]`.
    argv = sys.argv[1:]
    if argv:
        first_positional = next((a for a in argv if not a.startswith("-")), None)
        if first_positional is not None and first_positional not in ("parse", "batch"):
            idx = argv.index(first_positional)
            argv = argv[:idx] + ["parse"] + argv[idx:]
            sys.argv = [sys.argv[0]] + argv

    args = _build_parser().parse_args()

    if args.subcommand is None:
        _build_parser().print_help()
        sys.exit(0)

    json_to_stdout = args.subcommand == "parse" and args.format == "json" and args.output is None
    console = Console(stderr=json_to_stdout)

    emit_banner = not args.quiet and not args.no_banner and not json_to_stdout
    if emit_banner:
        _print_banner(console)

    if args.subcommand == "parse":
        _run_parse(args, console)
    else:
        _run_batch(args, console)


if __name__ == "__main__":
    main()
