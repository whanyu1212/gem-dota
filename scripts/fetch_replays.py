"""Download and decompress a Dota 2 replay from OpenDota.

Thin CLI wrapper around ``gem.replay_fetch``. Fetches the replay URL from
the OpenDota API (``/api/matches/{match_id}``), downloads the ``.dem.bz2``
file, and decompresses it to a ``.dem`` file.

Usage::

    uv run python scripts/fetch_replays.py <match_id>
    uv run python scripts/fetch_replays.py <match_id> --out /path/to/dir
    uv run python scripts/fetch_replays.py <match_id> --out /path/to/dir --force
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gem.replay_fetch import download_and_decompress, fetch_replay_url


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and decompress a Dota 2 replay from OpenDota.",
    )
    parser.add_argument("match_id", type=int, help="Steam match ID.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path.cwd(),
        metavar="DIR",
        help="Output directory (default: current working directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if the .dem file already exists.",
    )
    args = parser.parse_args()

    from rich.console import Console

    console = Console()

    args.out.mkdir(parents=True, exist_ok=True)
    dem_path = args.out / f"{args.match_id}.dem"

    if dem_path.exists() and not args.force:
        console.print(
            f"[dim]Already exists: {dem_path} ({dem_path.stat().st_size / 1_000_000:.1f} MB). "
            "Use --force to re-download.[/dim]"
        )
        sys.exit(0)

    try:
        replay_url = fetch_replay_url(args.match_id)
    except ValueError as exc:
        console.print(f"[bold red]ERROR:[/] {exc}")
        sys.exit(1)

    console.print(f"Downloading [bold]{replay_url}[/bold] ...")
    dem_path = download_and_decompress(args.match_id, replay_url, args.out)
    console.print(
        f"  saved to [green]{dem_path}[/green] ({dem_path.stat().st_size / 1_000_000:.1f} MB)"
    )


if __name__ == "__main__":
    main()
