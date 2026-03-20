"""Download and decompress a Dota 2 replay from OpenDota.

Fetches the replay URL from the OpenDota API (``/api/matches/{match_id}``),
downloads the ``.dem.bz2`` file, and decompresses it to a ``.dem`` file.

Usage::

    uv run python scripts/fetch_replays.py <match_id>
    uv run python scripts/fetch_replays.py <match_id> --out /path/to/dir
    uv run python scripts/fetch_replays.py <match_id> --out /path/to/dir --force

The decompressed ``.dem`` file is saved as ``<match_id>.dem`` in the output
directory (default: current working directory).

Notes
-----
- OpenDota's ``replay_url`` field points to the Valve CDN ``.dem.bz2``.
  It is only populated for matches that OpenDota has ingested; very old or
  untracked matches may return ``null``.
- To force re-download of an already existing file, use ``--force``.
"""

from __future__ import annotations

import argparse
import bz2
import json
import ssl
import sys
import urllib.request
from pathlib import Path

OPENDOTA_API = "https://api.opendota.com/api/matches"

# Relax SSL verification for CDN hosts that occasionally present cert issues.
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


def fetch_replay_url(match_id: int) -> str:
    """Fetch the replay download URL for a match from OpenDota.

    Args:
        match_id: Steam match ID.

    Returns:
        The ``replay_url`` string from the OpenDota API response.

    Raises:
        SystemExit: If the API call fails or the field is missing/null.
    """
    url = f"{OPENDOTA_API}/{match_id}"
    from rich.console import Console

    console = Console()
    console.print(f"Fetching match metadata from [dim]{url}[/dim] ...")
    req = urllib.request.Request(url, headers={"User-Agent": "gem/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except Exception as exc:
        console.print(f"[bold red]ERROR:[/] OpenDota request failed: {exc}")
        sys.exit(1)

    replay_url = data.get("replay_url")
    if not replay_url:
        console.print(
            f"[bold red]ERROR:[/] OpenDota returned no replay_url for match {match_id}.\n"
            "The match may not have been ingested yet. Try:\n"
            f"  curl -X POST https://api.opendota.com/api/request/{match_id}\n"
            "then wait a few minutes and retry."
        )
        sys.exit(1)

    return replay_url


def download_and_decompress(match_id: int, replay_url: str, out_dir: Path) -> Path:
    """Download and decompress a replay .dem.bz2 to out_dir/<match_id>.dem.

    Args:
        match_id: Steam match ID (used for the output filename).
        replay_url: Direct URL to the ``.dem.bz2`` file.
        out_dir: Directory to write the decompressed ``.dem`` file into.

    Returns:
        Path to the decompressed ``.dem`` file.
    """
    from rich.console import Console

    console = Console()

    dem_path = out_dir / f"{match_id}.dem"
    bz2_path = out_dir / f"{match_id}.dem.bz2"

    console.print(f"Downloading [bold]{replay_url}[/bold] ...")
    req = urllib.request.Request(replay_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=SSL_CONTEXT) as resp:
        bz2_path.write_bytes(resp.read())
    console.print(f"  downloaded {bz2_path.stat().st_size / 1_000_000:.1f} MB")

    console.print("Decompressing ...")
    dem_path.write_bytes(bz2.decompress(bz2_path.read_bytes()))
    bz2_path.unlink()
    console.print(
        f"  decompressed to [green]{dem_path}[/green] ({dem_path.stat().st_size / 1_000_000:.1f} MB)"
    )

    return dem_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and decompress a Dota 2 replay from OpenDota.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Notes")[0].strip(),
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

    replay_url = fetch_replay_url(args.match_id)
    download_and_decompress(args.match_id, replay_url, args.out)


if __name__ == "__main__":
    main()
