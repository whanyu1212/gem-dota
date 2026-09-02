"""Synchronize and verify curated OpenDota replay fixtures.

Full ``.dem`` files remain ignored by Git. This command reads the committed
fixture manifest, downloads selected replay tiers into the local fixture cache,
and verifies recorded size and SHA-256 metadata before installing each file.

Examples:
    uv run python scripts/sync_opendota_fixtures.py
    uv run python scripts/sync_opendota_fixtures.py --tier extended --tier stress
    uv run python scripts/sync_opendota_fixtures.py --match 8822520406
    uv run python scripts/sync_opendota_fixtures.py --all-active --verify-only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "tests" / "fixtures" / "opendota" / "manifest.json"
DEFAULT_OUT_DIR = DEFAULT_MANIFEST.parent

VALID_STATUSES = frozenset({"active", "deprecated"})
VALID_TIERS = frozenset(
    {"performance-baseline", "canonical", "extended", "stress", "regression", "archive"}
)
_TIER_ORDER = {
    "canonical": 0,
    "extended": 1,
    "stress": 2,
    "performance-baseline": 3,
    "regression": 4,
    "archive": 5,
}

Downloader = Callable[[int, str, Path], Path]


class FixtureManifestError(ValueError):
    """Raised when fixture metadata or selection is invalid."""


class FixtureIntegrityError(RuntimeError):
    """Raised when a replay does not match its recorded integrity metadata."""


@dataclass(frozen=True, slots=True)
class FixtureSpec:
    """Normalized manifest metadata for one replay fixture."""

    match_id: int
    name: str
    dem: str
    tier: str
    status: str
    capabilities: tuple[str, ...]
    replay_url: str | None
    artifact_url: str | None
    dem_size_bytes: int | None
    dem_sha256: str | None
    replaced_by: int | None

    @property
    def source_url(self) -> str | None:
        """Prefer a durable artifact URL over the original replay host."""
        return self.artifact_url or self.replay_url


def _optional_str(raw: dict[str, Any], key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise FixtureManifestError(f"{key} must be a non-empty string or null")
    return value


def _parse_spec(raw: object) -> FixtureSpec:
    if not isinstance(raw, dict):
        raise FixtureManifestError("each manifest match must be an object")

    match_id = raw.get("match_id")
    if not isinstance(match_id, int) or isinstance(match_id, bool) or match_id <= 0:
        raise FixtureManifestError("match_id must be a positive integer")

    name = raw.get("name", f"match-{match_id}")
    dem = raw.get("dem", f"{match_id}.dem")
    tier = raw.get("tier", "regression")
    status = raw.get("status", "active")
    if not isinstance(name, str) or not name:
        raise FixtureManifestError(f"fixture {match_id}: name must be a non-empty string")
    if not isinstance(dem, str) or not dem or Path(dem).name != dem:
        raise FixtureManifestError(f"fixture {match_id}: dem must be a plain filename")
    if not isinstance(tier, str) or tier not in VALID_TIERS:
        raise FixtureManifestError(f"fixture {match_id}: invalid tier {tier!r}")
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise FixtureManifestError(f"fixture {match_id}: invalid status {status!r}")

    raw_capabilities = raw.get("capabilities", [])
    if not isinstance(raw_capabilities, list) or not all(
        isinstance(value, str) and value for value in raw_capabilities
    ):
        raise FixtureManifestError(f"fixture {match_id}: capabilities must be strings")
    capabilities = tuple(raw_capabilities)
    if len(set(capabilities)) != len(capabilities):
        raise FixtureManifestError(f"fixture {match_id}: capabilities must be unique")

    size = raw.get("dem_size_bytes")
    if size is not None and (not isinstance(size, int) or isinstance(size, bool) or size <= 0):
        raise FixtureManifestError(f"fixture {match_id}: dem_size_bytes must be positive")

    sha256 = _optional_str(raw, "dem_sha256")
    if sha256 is not None:
        sha256 = sha256.lower()
        if len(sha256) != 64 or any(ch not in "0123456789abcdef" for ch in sha256):
            raise FixtureManifestError(f"fixture {match_id}: dem_sha256 must be 64 hex digits")

    replaced_by = raw.get("replaced_by")
    if replaced_by is not None and (
        not isinstance(replaced_by, int) or isinstance(replaced_by, bool) or replaced_by <= 0
    ):
        raise FixtureManifestError(f"fixture {match_id}: replaced_by must be a match ID or null")

    return FixtureSpec(
        match_id=match_id,
        name=name,
        dem=dem,
        tier=tier,
        status=status,
        capabilities=capabilities,
        replay_url=_optional_str(raw, "replay_url"),
        artifact_url=_optional_str(raw, "artifact_url"),
        dem_size_bytes=size,
        dem_sha256=sha256,
        replaced_by=replaced_by,
    )


def load_fixture_manifest(path: Path = DEFAULT_MANIFEST) -> list[FixtureSpec]:
    """Load and validate the fixture manifest."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FixtureManifestError(f"unable to read fixture manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise FixtureManifestError("fixture manifest root must be an object")
    if payload.get("schema_version") != 2:
        raise FixtureManifestError("fixture manifest schema_version must be 2")
    raw_matches = payload.get("matches")
    if not isinstance(raw_matches, list):
        raise FixtureManifestError("fixture manifest matches must be a list")

    specs = [_parse_spec(raw) for raw in raw_matches]
    ids = [spec.match_id for spec in specs]
    names = [spec.name for spec in specs]
    dem_filenames = [spec.dem for spec in specs]
    if len(ids) != len(set(ids)):
        raise FixtureManifestError("fixture manifest contains duplicate match IDs")
    if len(names) != len(set(names)):
        raise FixtureManifestError("fixture manifest contains duplicate names")
    if len(dem_filenames) != len(set(dem_filenames)):
        raise FixtureManifestError("fixture manifest contains duplicate dem filenames")

    by_id = {spec.match_id: spec for spec in specs}
    for spec in specs:
        if spec.dem_size_bytes is None or spec.dem_sha256 is None:
            raise FixtureManifestError(
                f"fixture {spec.match_id} must define dem_size_bytes and dem_sha256"
            )
        if spec.status == "active" and spec.source_url is None:
            raise FixtureManifestError(f"active fixture {spec.match_id} has no download URL")
        if spec.status == "deprecated":
            replacement = by_id.get(spec.replaced_by) if spec.replaced_by is not None else None
            if replacement is None or replacement.status != "active":
                raise FixtureManifestError(
                    f"deprecated fixture {spec.match_id} must reference an active replacement"
                )
    return specs


def select_fixture_specs(
    specs: Iterable[FixtureSpec],
    *,
    tiers: Iterable[str] = (),
    match_ids: Iterable[int] = (),
    all_active: bool = False,
    include_deprecated: bool = False,
) -> list[FixtureSpec]:
    """Select fixtures deterministically from manifest metadata."""
    spec_list = list(specs)
    tier_set = set(tiers)
    id_set = set(match_ids)
    unknown_tiers = tier_set - VALID_TIERS
    if unknown_tiers:
        raise FixtureManifestError(f"unknown fixture tier(s): {sorted(unknown_tiers)}")
    known_ids = {spec.match_id for spec in spec_list}
    missing_ids = id_set - known_ids
    if missing_ids:
        raise FixtureManifestError(f"unknown fixture match ID(s): {sorted(missing_ids)}")
    if not tier_set and not id_set and not all_active:
        tier_set.add("canonical")

    selected: list[FixtureSpec] = []
    for spec in spec_list:
        matches = all_active or spec.tier in tier_set or spec.match_id in id_set
        if not matches:
            continue
        if spec.status == "deprecated" and not include_deprecated:
            if spec.match_id in id_set:
                raise FixtureManifestError(
                    f"fixture {spec.match_id} is deprecated; pass --include-deprecated"
                )
            continue
        selected.append(spec)

    if not selected:
        raise FixtureManifestError("fixture selection is empty")
    return sorted(selected, key=lambda spec: (_TIER_ORDER[spec.tier], spec.match_id))


def file_sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file without loading it all into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_fixture(spec: FixtureSpec, path: Path) -> None:
    """Raise when a local replay differs from recorded manifest integrity data."""
    if not path.is_file():
        raise FixtureIntegrityError(f"fixture is missing: {path}")
    actual_size = path.stat().st_size
    if spec.dem_size_bytes is not None and actual_size != spec.dem_size_bytes:
        raise FixtureIntegrityError(
            f"fixture {spec.match_id} size mismatch: "
            f"expected {spec.dem_size_bytes}, got {actual_size}"
        )
    if spec.dem_sha256 is not None:
        actual_sha256 = file_sha256(path)
        if actual_sha256 != spec.dem_sha256:
            raise FixtureIntegrityError(
                f"fixture {spec.match_id} SHA-256 mismatch: "
                f"expected {spec.dem_sha256}, got {actual_sha256}"
            )


def _download_replay(match_id: int, replay_url: str, out_dir: Path) -> Path:
    from gem.replays.fetch import download_and_decompress

    return download_and_decompress(match_id, replay_url, out_dir)


def sync_fixture(
    spec: FixtureSpec,
    out_dir: Path,
    *,
    force: bool = False,
    verify_only: bool = False,
    downloader: Downloader = _download_replay,
) -> tuple[Path, bool]:
    """Verify or atomically download one replay fixture."""
    target = out_dir / spec.dem
    if target.exists() and not force:
        verify_fixture(spec, target)
        return target, False
    if verify_only:
        verify_fixture(spec, target)
        return target, False
    if spec.source_url is None:
        raise FixtureManifestError(f"fixture {spec.match_id} has no download URL")

    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="gem-fixture-", dir=out_dir) as temp_name:
        downloaded = downloader(spec.match_id, spec.source_url, Path(temp_name))
        verify_fixture(spec, downloaded)
        downloaded.replace(target)
    return target, True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--tier", action="append", choices=sorted(VALID_TIERS), default=[])
    parser.add_argument("--match", dest="match_ids", action="append", type=int, default=[])
    parser.add_argument("--all-active", action="store_true")
    parser.add_argument("--include-deprecated", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        specs = load_fixture_manifest(args.manifest)
        selected = select_fixture_specs(
            specs,
            tiers=args.tier,
            match_ids=args.match_ids,
            all_active=args.all_active,
            include_deprecated=args.include_deprecated,
        )
        for spec in selected:
            path, downloaded = sync_fixture(
                spec,
                args.out,
                force=args.force,
                verify_only=args.verify_only,
            )
            action = "DOWNLOADED" if downloaded else "VERIFIED"
            print(f"{action} {spec.name} ({spec.match_id}): {path}")
    except (FixtureManifestError, FixtureIntegrityError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
