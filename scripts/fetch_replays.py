"""
Fetch Dota 2 replay (.dem) files for use as test fixtures.

Replays are downloaded from the Steam CDN using match metadata from the
OpenDota API. The .dem.bz2 file is decompressed automatically on download.

Replay files are saved to tests/fixtures/ and are gitignored (too large to commit).
A small truncated fixture (~5MB) is also created for fast unit tests.

Usage:
    uv run python scripts/fetch_replays.py                  # download all configured replays
    uv run python scripts/fetch_replays.py --match 8461735141  # download a specific match
    uv run python scripts/fetch_replays.py --list           # list configured replays

Replay CDN URL format:
    http://replay{cluster}.valve.net/570/{match_id}_{replay_salt}.dem.bz2
"""

import argparse
import bz2
import sys
import urllib.request as urlreq
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
OPENDOTA_API = "https://api.opendota.com/api/matches"
STEAM_CDN = "http://replay{cluster}.valve.net/570/{match_id}_{salt}.dem.bz2"

# Truncated fixture size — enough to cover the file header + first packet frames.
# Used for fast unit tests that don't need a full replay.
TRUNCATE_BYTES = 5 * 1024 * 1024  # 5 MB


@dataclass
class Replay:
    match_id: int
    label: str  # human-readable name for the fixture file
    cluster: int | None = None
    salt: int | None = None


# ---------------------------------------------------------------------------
# Curated replays used as test fixtures
# ---------------------------------------------------------------------------

REPLAYS: list[Replay] = [
    Replay(
        match_id=8461735141,
        label="ti14_finals_g1_xg_vs_falcons",
        # cluster and salt pre-filled to avoid an extra API call
        cluster=274,
        salt=494961331,
    ),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fetch_json(url: str) -> dict:
    with urlreq.urlopen(url, timeout=15) as resp:
        import json

        return json.loads(resp.read())


def resolve_metadata(replay: Replay) -> Replay:
    """Fill in cluster + salt from OpenDota if not already set."""
    if replay.cluster and replay.salt:
        return replay
    print(f"  Fetching metadata for match {replay.match_id} from OpenDota...")
    data = fetch_json(f"{OPENDOTA_API}/{replay.match_id}")
    cluster = data.get("cluster")
    salt = data.get("replay_salt")
    if not cluster or not salt:
        print(
            f"  ERROR: OpenDota has no replay metadata for match {replay.match_id}", file=sys.stderr
        )
        sys.exit(1)
    return Replay(match_id=replay.match_id, label=replay.label, cluster=cluster, salt=salt)


def cdn_url(replay: Replay) -> str:
    return STEAM_CDN.format(cluster=replay.cluster, match_id=replay.match_id, salt=replay.salt)


def download_replay(replay: Replay, dest: Path) -> None:
    url = cdn_url(replay)
    print(f"  URL: {url}")

    bz2_path = dest.with_suffix(".dem.bz2")

    def progress_hook(count: int, block_size: int, total_size: int) -> None:
        if total_size > 0:
            pct = min(count * block_size * 100 // total_size, 100)
            mb = count * block_size / 1024 / 1024
            print(f"\r  Downloading... {pct}% ({mb:.1f} MB)", end="", flush=True)

    print(f"  Saving to: {bz2_path.name}")
    urlreq.urlretrieve(url, bz2_path, reporthook=progress_hook)
    print()  # newline after progress

    print("  Decompressing...")
    with bz2.open(bz2_path, "rb") as f_in, open(dest, "wb") as f_out:
        while chunk := f_in.read(1024 * 1024):
            f_out.write(chunk)

    bz2_path.unlink()
    size_mb = dest.stat().st_size / 1024 / 1024
    print(f"  Done: {dest.name} ({size_mb:.1f} MB)")


def create_truncated_fixture(full: Path, truncated: Path) -> None:
    """Write the first TRUNCATE_BYTES of a replay as a small fixture for unit tests."""
    if truncated.exists():
        print(f"  Truncated fixture already exists: {truncated.name}, skipping.")
        return
    with open(full, "rb") as f_in, open(truncated, "wb") as f_out:
        f_out.write(f_in.read(TRUNCATE_BYTES))
    size_mb = truncated.stat().st_size / 1024 / 1024
    print(f"  Created truncated fixture: {truncated.name} ({size_mb:.1f} MB)")


def process_replay(replay: Replay) -> None:
    replay = resolve_metadata(replay)
    full_dest = FIXTURES_DIR / f"{replay.label}.dem"
    truncated_dest = FIXTURES_DIR / f"{replay.label}_truncated.dem"

    if full_dest.exists():
        size_mb = full_dest.stat().st_size / 1024 / 1024
        print(f"  Already downloaded: {full_dest.name} ({size_mb:.1f} MB)")
    else:
        download_replay(replay, full_dest)

    create_truncated_fixture(full_dest, truncated_dest)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Download Dota 2 replays for test fixtures.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--match", type=int, help="Download a single match by ID.")
    group.add_argument("--list", action="store_true", help="List configured replays.")
    args = parser.parse_args()

    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

    if args.list:
        print("Configured replays:")
        for r in REPLAYS:
            dest = FIXTURES_DIR / f"{r.label}.dem"
            status = (
                f"{dest.stat().st_size / 1024 / 1024:.1f} MB" if dest.exists() else "not downloaded"
            )
            print(f"  {r.match_id}  {r.label}  [{status}]")
        return

    if args.match:
        replay = Replay(match_id=args.match, label=str(args.match))
        print(f"Fetching match {args.match}...")
        process_replay(replay)
        return

    # Default: download all configured replays
    print(f"Downloading {len(REPLAYS)} configured replay(s) to {FIXTURES_DIR}\n")
    for replay in REPLAYS:
        print(f"[{replay.label}]")
        process_replay(replay)
        print()

    print("All done.")
    print("Note: .dem files are gitignored. Truncated fixtures are committed for unit tests.")


if __name__ == "__main__":
    main()
