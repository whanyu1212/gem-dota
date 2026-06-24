from __future__ import annotations

import json
from pathlib import Path

from scripts import fetch_hero_icons, fetch_item_icons

_PNG_BYTES = b"\x89PNG\r\n\x1a\nfake-png"


def test_item_icon_check_ignores_recipe_items_by_default(tmp_path: Path) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text(
        json.dumps(
            {
                "blink": {"id": 1, "dname": "Blink Dagger"},
                "conjurers_catalyst": {"id": 1864, "dname": "Conjurer's Catalyst"},
                "recipe_blink": {"id": 2, "dname": "Recipe: Blink Dagger"},
            }
        ),
        encoding="utf-8",
    )
    icon_dir = tmp_path / "item_icons"
    icon_dir.mkdir()
    (icon_dir / "blink.png").write_bytes(_PNG_BYTES)

    assert fetch_item_icons.missing_icon_shorts(items_path, icon_dir) == ("conjurers_catalyst",)
    assert fetch_item_icons.missing_icon_shorts(
        items_path,
        icon_dir,
        include_recipes=True,
    ) == (
        "conjurers_catalyst",
        "recipe_blink",
    )


def test_item_icon_check_returns_nonzero_for_missing_non_recipe_icons(
    tmp_path: Path,
    capsys,
) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text(
        json.dumps(
            {
                "blink": {"id": 1, "dname": "Blink Dagger"},
                "conjurers_catalyst": {"id": 1864, "dname": "Conjurer's Catalyst"},
                "recipe_blink": {"id": 2, "dname": "Recipe: Blink Dagger"},
            }
        ),
        encoding="utf-8",
    )
    icon_dir = tmp_path / "item_icons"
    icon_dir.mkdir()
    (icon_dir / "blink.png").write_bytes(_PNG_BYTES)

    status = fetch_item_icons.main(
        ["--check", "--items", str(items_path), "--out-dir", str(icon_dir)]
    )

    captured = capsys.readouterr()
    assert status == 1
    assert "Missing 1 item icon" in captured.out
    assert "conjurers_catalyst" in captured.out
    assert "recipe_blink" not in captured.out


def test_hero_icon_check_returns_zero_when_icons_are_complete(tmp_path: Path, capsys) -> None:
    heroes_path = tmp_path / "heroes.json"
    heroes_path.write_text(
        json.dumps({"npc_dota_hero_axe": {"id": 2, "localized_name": "Axe"}}),
        encoding="utf-8",
    )
    icon_dir = tmp_path / "hero_icons"
    icon_dir.mkdir()
    (icon_dir / "axe.png").write_bytes(_PNG_BYTES)

    status = fetch_hero_icons.main(
        ["--check", "--heroes", str(heroes_path), "--out-dir", str(icon_dir)]
    )

    captured = capsys.readouterr()
    assert status == 0
    assert "All hero icons present" in captured.out


def test_hero_icon_check_reports_missing_icons(tmp_path: Path, capsys) -> None:
    heroes_path = tmp_path / "heroes.json"
    heroes_path.write_text(
        json.dumps(
            {
                "npc_dota_hero_axe": {"id": 2, "localized_name": "Axe"},
                "npc_dota_hero_largo": {"id": 155, "localized_name": "Largo"},
            }
        ),
        encoding="utf-8",
    )
    icon_dir = tmp_path / "hero_icons"
    icon_dir.mkdir()
    (icon_dir / "axe.png").write_bytes(_PNG_BYTES)

    status = fetch_hero_icons.main(
        ["--check", "--heroes", str(heroes_path), "--out-dir", str(icon_dir)]
    )

    captured = capsys.readouterr()
    assert status == 1
    assert "Missing 1 hero icon" in captured.out
    assert "largo" in captured.out
