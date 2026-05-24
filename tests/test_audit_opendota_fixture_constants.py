from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_opendota_fixture_constants import (
    DEFAULT_ALLOWED_MISSING_ITEM_KEYS,
    DEFAULT_FIXTURE_DIR,
    DEFAULT_ITEMS_PATH,
    audit_fixture_constants,
    collect_observed_item_constants,
    find_fixture_paths,
    load_items,
    main,
)


def test_collect_observed_item_constants_reads_keys_and_inventory_ids(tmp_path: Path) -> None:
    payload_path = tmp_path / "123.opendota.json"
    payload_path.write_text(
        json.dumps(
            {
                "players": [
                    {
                        "purchase": {"blink": 1},
                        "item_uses": {"prophets_pendulum": 2},
                        "purchase_log": [{"key": "conjurers_catalyst"}],
                        "neutral_item_history": [
                            {
                                "item_neutral": "enhancement_nimble",
                                "item_neutral_enhancement": "enhancement_vital",
                            }
                        ],
                        "item_0": 1,
                        "backpack_0": 1860,
                        "item_neutral": 1864,
                        "item_neutral2": 1874,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    observed = collect_observed_item_constants([payload_path])

    assert observed.item_keys == {
        "blink",
        "conjurers_catalyst",
        "enhancement_nimble",
        "enhancement_vital",
        "prophets_pendulum",
    }
    assert observed.item_ids == {1, 1860, 1864, 1874}


def test_audit_fixture_constants_reports_unresolved_keys_and_ids(tmp_path: Path) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text(
        json.dumps({"blink": {"id": 1, "dname": "Blink Dagger"}}),
        encoding="utf-8",
    )
    payload_path = tmp_path / "123.opendota.json"
    payload_path.write_text(
        json.dumps(
            {
                "players": [
                    {
                        "purchase": {"blink": 1, "missing_item": 1},
                        "item_0": 1,
                        "item_neutral": 9999,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    report = audit_fixture_constants([payload_path], load_items(items_path))

    assert report.ok is False
    assert report.missing_item_keys == ("missing_item",)
    assert report.missing_item_ids == (9999,)


def test_audit_fixture_constants_allows_known_opendota_key_exceptions(tmp_path: Path) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text(
        json.dumps({"blink": {"id": 1, "dname": "Blink Dagger"}}),
        encoding="utf-8",
    )
    payload_path = tmp_path / "123.opendota.json"
    payload_path.write_text(
        json.dumps({"players": [{"purchase": {"guardian_shell": 1}, "item_0": 1}]}),
        encoding="utf-8",
    )

    report = audit_fixture_constants(
        [payload_path],
        load_items(items_path),
        allowed_missing_item_keys=DEFAULT_ALLOWED_MISSING_ITEM_KEYS,
    )

    assert report.ok is True
    assert report.allowed_missing_item_keys == ("guardian_shell",)


def test_main_returns_nonzero_for_unexpected_missing_constants(tmp_path: Path) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text("{}", encoding="utf-8")
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "123.opendota.json").write_text(
        json.dumps({"players": [{"purchase": {"blink": 1}, "item_0": 1}]}),
        encoding="utf-8",
    )

    assert main(["--fixtures", str(fixture_dir), "--items", str(items_path)]) == 1


def test_saved_opendota_fixtures_resolve_against_bundled_item_constants() -> None:
    report = audit_fixture_constants(
        find_fixture_paths(DEFAULT_FIXTURE_DIR),
        load_items(DEFAULT_ITEMS_PATH),
        allowed_missing_item_keys=DEFAULT_ALLOWED_MISSING_ITEM_KEYS,
    )

    assert report.missing_item_keys == ()
    assert report.missing_item_ids == ()
    assert report.allowed_missing_item_keys == ("guardian_shell",)
