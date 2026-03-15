"""CLI entry point: ``python -m gem <replay.dem>``.

Parses a replay file and prints a summary of key statistics by default.
Supports JSON and parquet export modes.
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
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from gem import __version__, parse, parse_to_json, parse_to_parquet
from gem.models import ParsedMatch


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gem",
        description="Parse a Dota 2 Source 2 replay (.dem).",
        epilog=(
            "Examples:\n"
            "  python -m gem match.dem\n"
            "  python -m gem match.dem --format json\n"
            "  python -m gem match.dem --format json --output out.json\n"
            "  python -m gem match.dem --format parquet --output ./parquet_out\n"
            "  python -m gem match.dem --quiet\n"
            "  python -m gem match.dem --progress --timings"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", help="Path to replay file (.dem)")
    parser.add_argument(
        "--format",
        dest="format",
        choices=("summary", "json", "parquet"),
        default="summary",
        help="Output format (default: summary)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file (json) or directory (parquet). If omitted for json, prints to stdout.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress banner and non-essential progress/info messages.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Hide ASCII art banner (summary/content still printed).",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show phase progress with elapsed time.",
    )
    parser.add_argument(
        "--timings",
        action="store_true",
        help="Show timing breakdown at the end.",
    )
    return parser


# Human-readable labels for each phase key.
_PHASE_LABELS: dict[str, str] = {
    "parse": "Parsing replay",
    "render_summary": "Rendering summary",
    "parse_serialize_json": "Parsing & serialising JSON",
    "write_json": "Writing JSON file",
    "parse_export_parquet": "Parsing & exporting Parquet",
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
        self._task_ids: dict[str, object] = {}

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


def _print_banner(console: Console) -> None:
    # Pixel-art block letters: each cell = "██" (filled) or "  " (empty)
    B, S = "██", "  "
    _G = [
        [S, B, B, B, S],
        [B, S, S, S, S],
        [B, S, B, B, B],
        [B, S, S, S, B],
        [S, B, B, B, B],
    ]
    _E = [
        [B, B, B, B],
        [B, S, S, S],
        [B, B, B, S],
        [B, S, S, S],
        [B, B, B, B],
    ]
    _M = [
        [B, S, S, S, B],
        [B, B, S, B, B],
        [B, S, B, S, B],
        [B, S, S, S, B],
        [B, S, S, S, B],
    ]

    # Neon gradient: pink → purple → blue → cyan
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

    # Derived match-level counts
    hero_kills = sum(1 for e in match.combat_log if e.log_type == "DEATH" and e.target_is_hero)
    total_buybacks = sum(len(pp.buyback_log) for pp in match.players)
    total_runes = sum(len(pp.runes_log) for pp in match.players)

    # Duration from last sample tick (ticks / 30 ≈ seconds)
    all_ticks = [t for pp in match.players for t in pp.times]
    if all_ticks:
        last_tick = max(all_ticks)
        total_secs = int(last_tick / 30)
        duration_str = f"{total_secs // 60}:{total_secs % 60:02d}"
    else:
        duration_str = "?"

    # --- match stats bar ---
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

    # --- per-player table ---
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
        is_radiant = pp.team == 2
        team_str = "[green]Radiant[/green]" if is_radiant else "[red]Dire[/red]"
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


def main() -> None:
    """Parse a replay and output summary/json/parquet."""
    args = _build_parser().parse_args()

    # When piping JSON to stdout, keep stdout clean — send all Rich output to stderr.
    json_to_stdout = args.format == "json" and args.output is None
    console = Console(stderr=json_to_stdout)

    emit_banner = not args.quiet and not args.no_banner and not json_to_stdout
    if emit_banner:
        _print_banner(console)

    tracker = _PhaseTracker(
        progress=args.progress and not args.quiet,
        timings=args.timings,
        console=console,
    )

    try:
        if args.format == "summary":
            tracker.start("parse")
            match = parse(args.path)
            tracker.end("parse")

            tracker.start("render_summary")
            _print_summary(match, console, quiet=args.quiet, path=args.path)
            tracker.end("render_summary")
            return

        if args.format == "json":
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
            return

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
                f"[green]✓[/green] Wrote [bold]{len(written)}[/bold] parquet file(s) to [bold]{args.output}[/bold]"
            )
    finally:
        tracker.report()


if __name__ == "__main__":
    main()
