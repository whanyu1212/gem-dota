from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.fetch_opendota_fixture import (
    DEFAULT_OUT_DIR,
    FixtureExistsError,
    build_manifest_entry,
    ensure_can_write_fixture,
    main,
    parse_args,
    update_manifest,
)


def test_build_manifest_entry_uses_stable_shape() -> None:
    payload = {
        "match_id": 1234567890,
        "duration": 2400,
        "game_mode": 2,
        "lobby_type": 1,
        "patch": 7.41,
        "replay_url": "https://replay.example/123.dem.bz2",
    }

    entry = build_manifest_entry(
        1234567890,
        payload,
        fetched_at="2026-05-24T01:00:00Z",
        note="7.41 facets regression",
    )

    assert entry == {
        "match_id": 1234567890,
        "dem": "1234567890.dem",
        "opendota_json": "1234567890.opendota.json",
        "fetched_at": "2026-05-24T01:00:00Z",
        "duration": 2400,
        "game_mode": 2,
        "lobby_type": 1,
        "patch": 7.41,
        "replay_url": "https://replay.example/123.dem.bz2",
        "dem_size_bytes": None,
        "dem_sha256": None,
        "note": "7.41 facets regression",
    }


def test_build_manifest_entry_sets_missing_optional_fields_to_none() -> None:
    payload = {"match_id": 1234567890, "replay_url": "https://replay.example/123.dem.bz2"}

    entry = build_manifest_entry(
        1234567890,
        payload,
        fetched_at="2026-05-24T01:00:00Z",
        note=None,
    )

    assert entry["duration"] is None
    assert entry["game_mode"] is None
    assert entry["lobby_type"] is None
    assert entry["patch"] is None
    assert entry["note"] is None


def test_update_manifest_creates_sorted_manifest(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    update_manifest(manifest_path, {"match_id": 22, "dem": "22.dem"})
    update_manifest(manifest_path, {"match_id": 11, "dem": "11.dem"})

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest == {
        "schema_version": 2,
        "matches": [
            {"match_id": 11, "dem": "11.dem"},
            {"match_id": 22, "dem": "22.dem"},
        ],
    }


def test_update_manifest_replaces_existing_entry(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    update_manifest(manifest_path, {"match_id": 11, "dem": "old.dem"})
    update_manifest(manifest_path, {"match_id": 11, "dem": "new.dem"})

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest == {
        "schema_version": 2,
        "matches": [{"match_id": 11, "dem": "new.dem"}],
    }


def test_update_manifest_refuses_legacy_schema_without_rewriting(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    legacy_manifest = {
        "schema_version": 1,
        "matches": [{"match_id": 11, "dem": "11.dem"}],
    }
    original = json.dumps(legacy_manifest, indent=2) + "\n"
    manifest_path.write_text(original, encoding="utf-8")

    with pytest.raises(ValueError, match="migrate it to schema_version 2"):
        update_manifest(manifest_path, {"match_id": 22, "dem": "22.dem"})

    assert manifest_path.read_text(encoding="utf-8") == original


def test_update_manifest_preserves_curated_metadata(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "matches": [
                    {
                        "match_id": 11,
                        "name": "canonical-replay",
                        "tier": "canonical",
                        "dem": "old.dem",
                        "note": "keep this curated explanation",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    update_manifest(manifest_path, {"match_id": 11, "dem": "new.dem"})

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["matches"] == [
        {
            "match_id": 11,
            "name": "canonical-replay",
            "tier": "canonical",
            "dem": "new.dem",
            "note": "keep this curated explanation",
        }
    ]


def test_ensure_can_write_fixture_rejects_existing_outputs_without_force(tmp_path: Path) -> None:
    dem_path = tmp_path / "1234567890.dem"
    json_path = tmp_path / "1234567890.opendota.json"
    dem_path.write_bytes(b"demo")

    with pytest.raises(FixtureExistsError, match="already exists"):
        ensure_can_write_fixture(dem_path, json_path, force=False)


def test_ensure_can_write_fixture_allows_existing_outputs_with_force(tmp_path: Path) -> None:
    dem_path = tmp_path / "1234567890.dem"
    json_path = tmp_path / "1234567890.opendota.json"
    dem_path.write_bytes(b"demo")
    json_path.write_text("{}", encoding="utf-8")

    ensure_can_write_fixture(dem_path, json_path, force=True)


def test_parse_args_defaults_to_opendota_fixture_dir() -> None:
    args = parse_args(["1234567890"])

    assert args.match_id == 1234567890
    assert args.out == DEFAULT_OUT_DIR
    assert args.force is False
    assert args.note is None


def test_main_returns_nonzero_on_fetch_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_fetch_fixture(*args: object, **kwargs: object) -> Path:
        raise ValueError("OpenDota returned no replay_url for match 1234567890")

    monkeypatch.setattr("scripts.fetch_opendota_fixture.fetch_fixture", fail_fetch_fixture)

    assert main(["1234567890"]) == 1
