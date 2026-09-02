from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.sync_opendota_fixtures import (
    DEFAULT_MANIFEST,
    FixtureIntegrityError,
    FixtureManifestError,
    FixtureSpec,
    file_sha256,
    load_fixture_manifest,
    select_fixture_specs,
    sync_fixture,
    verify_fixture,
)


def _entry(
    match_id: int,
    *,
    name: str,
    tier: str,
    status: str = "active",
    replaced_by: int | None = None,
) -> dict[str, object]:
    return {
        "match_id": match_id,
        "name": name,
        "dem": f"{match_id}.dem",
        "tier": tier,
        "status": status,
        "capabilities": [tier],
        "replay_url": f"https://replay.example/{match_id}.dem.bz2",
        "artifact_url": None,
        "dem_size_bytes": None,
        "dem_sha256": None,
        "replaced_by": replaced_by,
    }


def _write_manifest(path: Path, entries: list[dict[str, object]]) -> None:
    path.write_text(
        json.dumps({"schema_version": 2, "matches": entries}),
        encoding="utf-8",
    )


def test_load_fixture_manifest_validates_deprecated_replacement(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    _write_manifest(
        path,
        [
            _entry(1, name="old", tier="archive", status="deprecated", replaced_by=2),
            _entry(2, name="current", tier="canonical"),
        ],
    )

    specs = load_fixture_manifest(path)

    assert [spec.match_id for spec in specs] == [1, 2]
    assert specs[0].replaced_by == 2


def test_committed_manifest_defines_ti2026_tiers_and_integrity() -> None:
    specs = load_fixture_manifest(DEFAULT_MANIFEST)
    by_tier = {spec.tier: spec for spec in specs if "ti2026" in spec.capabilities}

    assert by_tier["canonical"].match_id == 8868259993
    assert by_tier["extended"].match_id == 8860187335
    assert by_tier["stress"].match_id == 8856501050
    for spec in specs:
        assert spec.dem_size_bytes is not None
        assert spec.dem_sha256 is not None


def test_load_fixture_manifest_rejects_duplicate_names(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    _write_manifest(
        path,
        [
            _entry(1, name="duplicate", tier="canonical"),
            _entry(2, name="duplicate", tier="extended"),
        ],
    )

    with pytest.raises(FixtureManifestError, match="duplicate names"):
        load_fixture_manifest(path)


def test_load_fixture_manifest_rejects_duplicate_dem_filenames(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    first = _entry(1, name="first", tier="canonical")
    second = _entry(2, name="second", tier="extended")
    second["dem"] = first["dem"]
    _write_manifest(path, [first, second])

    with pytest.raises(FixtureManifestError, match="duplicate dem filenames"):
        load_fixture_manifest(path)


@pytest.mark.parametrize(("field", "value"), [("tier", []), ("status", {})])
def test_load_fixture_manifest_rejects_non_string_enum_fields(
    tmp_path: Path, field: str, value: object
) -> None:
    path = tmp_path / "manifest.json"
    entry = _entry(1, name="invalid", tier="canonical")
    entry[field] = value
    _write_manifest(path, [entry])

    with pytest.raises(FixtureManifestError, match=rf"invalid {field}"):
        load_fixture_manifest(path)


def test_load_fixture_manifest_rejects_inactive_replacement(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    _write_manifest(
        path,
        [
            _entry(1, name="old", tier="archive", status="deprecated", replaced_by=2),
            _entry(2, name="also-old", tier="archive", status="deprecated", replaced_by=1),
        ],
    )

    with pytest.raises(FixtureManifestError, match="active replacement"):
        load_fixture_manifest(path)


def test_selection_defaults_to_active_canonical() -> None:
    specs = [
        _spec(1, "canonical", "active"),
        _spec(2, "extended", "active"),
        _spec(3, "canonical", "deprecated", replaced_by=1),
    ]

    selected = select_fixture_specs(specs)

    assert [spec.match_id for spec in selected] == [1]


def test_explicit_deprecated_selection_requires_opt_in() -> None:
    specs = [
        _spec(1, "canonical", "active"),
        _spec(2, "archive", "deprecated", replaced_by=1),
    ]

    with pytest.raises(FixtureManifestError, match="include-deprecated"):
        select_fixture_specs(specs, match_ids=[2])

    selected = select_fixture_specs(specs, match_ids=[2], include_deprecated=True)
    assert [spec.match_id for spec in selected] == [2]


def test_verify_fixture_checks_size_and_sha256(tmp_path: Path) -> None:
    replay = tmp_path / "1.dem"
    replay.write_bytes(b"demo replay")
    spec = _spec(
        1,
        "canonical",
        "active",
        size=replay.stat().st_size,
        sha256=hashlib.sha256(b"demo replay").hexdigest(),
    )

    verify_fixture(spec, replay)
    assert file_sha256(replay) == spec.dem_sha256


def test_verify_fixture_rejects_integrity_mismatch(tmp_path: Path) -> None:
    replay = tmp_path / "1.dem"
    replay.write_bytes(b"wrong")
    spec = _spec(1, "canonical", "active", size=99)

    with pytest.raises(FixtureIntegrityError, match="size mismatch"):
        verify_fixture(spec, replay)


def test_sync_fixture_downloads_to_temporary_path_before_install(tmp_path: Path) -> None:
    payload = b"verified replay"
    spec = _spec(
        1,
        "canonical",
        "active",
        size=len(payload),
        sha256=hashlib.sha256(payload).hexdigest(),
    )
    download_dirs: list[Path] = []

    def downloader(match_id: int, replay_url: str, out_dir: Path) -> Path:
        assert match_id == 1
        assert replay_url.endswith("1.dem.bz2")
        download_dirs.append(out_dir)
        path = out_dir / "1.dem"
        path.write_bytes(payload)
        return path

    path, downloaded = sync_fixture(spec, tmp_path, downloader=downloader)

    assert downloaded is True
    assert path == tmp_path / "1.dem"
    assert path.read_bytes() == payload
    assert download_dirs and download_dirs[0] != tmp_path
    assert not download_dirs[0].exists()


def test_sync_fixture_reuses_verified_local_file(tmp_path: Path) -> None:
    replay = tmp_path / "1.dem"
    replay.write_bytes(b"local")
    spec = _spec(1, "canonical", "active", size=5)

    path, downloaded = sync_fixture(spec, tmp_path)

    assert path == replay
    assert downloaded is False


def test_failed_forced_download_does_not_replace_existing_fixture(tmp_path: Path) -> None:
    replay = tmp_path / "1.dem"
    replay.write_bytes(b"known good")
    expected = b"replacement"
    spec = _spec(
        1,
        "canonical",
        "active",
        size=len(expected),
        sha256=hashlib.sha256(expected).hexdigest(),
    )

    def bad_downloader(match_id: int, replay_url: str, out_dir: Path) -> Path:
        path = out_dir / f"{match_id}.dem"
        path.write_bytes(b"corrupt")
        return path

    with pytest.raises(FixtureIntegrityError, match="size mismatch"):
        sync_fixture(spec, tmp_path, force=True, downloader=bad_downloader)

    assert replay.read_bytes() == b"known good"


def _spec(
    match_id: int,
    tier: str,
    status: str,
    *,
    replaced_by: int | None = None,
    size: int | None = None,
    sha256: str | None = None,
) -> FixtureSpec:
    return FixtureSpec(
        match_id=match_id,
        name=f"fixture-{match_id}",
        dem=f"{match_id}.dem",
        tier=tier,
        status=status,
        capabilities=(tier,),
        replay_url=f"https://replay.example/{match_id}.dem.bz2",
        artifact_url=None,
        dem_size_bytes=size,
        dem_sha256=sha256,
        replaced_by=replaced_by,
    )
