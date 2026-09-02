"""Fetch an OpenDota replay fixture and save its metadata snapshot.

Usage:
    uv run python scripts/fetch_opendota_fixture.py 1234567890
    uv run python scripts/fetch_opendota_fixture.py 1234567890 --note "7.41 regression"
    uv run python scripts/fetch_opendota_fixture.py 1234567890 --force
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT_DIR = REPO_ROOT / "tests" / "fixtures" / "opendota"
OPENDOTA_MATCHES = "https://api.opendota.com/api/matches"

sys.path.insert(0, str(REPO_ROOT / "src"))


class FixtureExistsError(RuntimeError):
    """Raised when fixture outputs already exist and --force was not passed."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_opendota_match(match_id: int) -> dict[str, Any]:
    url = f"{OPENDOTA_MATCHES}/{match_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "gem-fixture-fetcher/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"OpenDota request failed for match {match_id}: {url}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"OpenDota returned non-object payload for match {match_id}: {url}")
    return data


def build_manifest_entry(
    match_id: int,
    opendota_payload: dict[str, Any],
    *,
    fetched_at: str,
    note: str | None,
    dem_size_bytes: int | None = None,
    dem_sha256: str | None = None,
) -> dict[str, Any]:
    return {
        "match_id": match_id,
        "dem": f"{match_id}.dem",
        "opendota_json": f"{match_id}.opendota.json",
        "fetched_at": fetched_at,
        "duration": opendota_payload.get("duration"),
        "game_mode": opendota_payload.get("game_mode"),
        "lobby_type": opendota_payload.get("lobby_type"),
        "patch": opendota_payload.get("patch"),
        "replay_url": opendota_payload.get("replay_url"),
        "dem_size_bytes": dem_size_bytes,
        "dem_sha256": dem_sha256,
        "note": note,
    }


def update_manifest(manifest_path: Path, entry: dict[str, Any]) -> None:
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError(f"Fixture manifest root must be an object: {manifest_path}")
        schema_version = manifest.get("schema_version")
        if schema_version != 2:
            raise ValueError(
                f"Fixture manifest uses schema_version {schema_version!r}; "
                "migrate it to schema_version 2 before updating"
            )
    else:
        manifest = {"schema_version": 2, "matches": []}

    matches = list(manifest.get("matches", []))
    existing = next((m for m in matches if m.get("match_id") == entry["match_id"]), None)
    merged = dict(existing) if isinstance(existing, dict) else {}
    updates = entry
    if isinstance(existing, dict) and entry.get("note") is None:
        updates = {key: value for key, value in entry.items() if key != "note"}
    merged.update(updates)
    matches = [m for m in matches if m.get("match_id") != entry["match_id"]]
    matches.append(merged)
    matches.sort(key=lambda m: int(m["match_id"]))

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest["schema_version"] = 2
    manifest["matches"] = matches
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    """Return the SHA-256 digest for a replay without loading it all into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_can_write_fixture(dem_path: Path, json_path: Path, *, force: bool) -> None:
    existing = [path for path in (dem_path, json_path) if path.exists()]
    if existing and not force:
        existing_names = ", ".join(str(path) for path in existing)
        raise FixtureExistsError(f"Fixture output already exists: {existing_names}. Use --force.")


def write_opendota_snapshot(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fetch_fixture(match_id: int, *, out_dir: Path, force: bool, note: str | None) -> Path:
    from gem.replays.fetch import download_and_decompress

    out_dir.mkdir(parents=True, exist_ok=True)
    dem_path = out_dir / f"{match_id}.dem"
    json_path = out_dir / f"{match_id}.opendota.json"
    ensure_can_write_fixture(dem_path, json_path, force=force)

    payload = fetch_opendota_match(match_id)
    replay_url = payload.get("replay_url")
    if not replay_url:
        raise ValueError(
            f"OpenDota returned no replay_url for match {match_id}. "
            f"Request parsing with: curl -X POST https://api.opendota.com/api/request/{match_id}"
        )

    try:
        download_and_decompress(match_id, str(replay_url), out_dir)
    except Exception as exc:
        raise RuntimeError(
            f"Replay download failed for match {match_id}: {replay_url}: {exc}"
        ) from exc

    write_opendota_snapshot(json_path, payload)
    entry = build_manifest_entry(
        match_id,
        payload,
        fetched_at=utc_now_iso(),
        note=note,
        dem_size_bytes=dem_path.stat().st_size,
        dem_sha256=file_sha256(dem_path),
    )
    update_manifest(out_dir / "manifest.json", entry)
    return dem_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch an OpenDota replay into the curated test fixture corpus."
    )
    parser.add_argument("match_id", type=int, help="Steam match ID.")
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUT_DIR}).",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing fixture files.")
    parser.add_argument("--note", help="Reason this fixture was added.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        dem_path = fetch_fixture(
            args.match_id,
            out_dir=args.out,
            force=args.force,
            note=args.note,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Saved replay fixture: {dem_path}")
    print(f"Saved OpenDota snapshot: {args.out / f'{args.match_id}.opendota.json'}")
    print(f"Updated manifest: {args.out / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
