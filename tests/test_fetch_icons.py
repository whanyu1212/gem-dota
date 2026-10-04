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


class _Response:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self._data


def test_item_download_falls_back_to_the_legacy_icon_url(tmp_path: Path, monkeypatch) -> None:
    from scripts import _icons

    items_path = tmp_path / "items.json"
    items_path.write_text('{"eternal_shroud": {"id": 1}}', encoding="utf-8")
    out_dir = tmp_path / "item_icons"
    calls: list[str] = []

    def fake_urlopen(request, *, timeout: int, context: object) -> _Response:
        calls.append(request.full_url)
        if "dota_react/items" in request.full_url:
            raise OSError("missing react icon")
        return _Response(_PNG_BYTES)

    monkeypatch.setattr(_icons.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(_icons.time, "sleep", lambda _seconds: None)

    result = _icons.download_item_icons(items_path=items_path, out_dir=out_dir)

    assert (result.downloaded, result.failed) == (1, 0)
    assert calls == [
        "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/eternal_shroud.png",
        "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/items/eternal_shroud_lg.png",
    ]
    assert (out_dir / "eternal_shroud.png").read_bytes() == _PNG_BYTES


def test_download_skips_non_png_responses_and_replaces_bad_files(
    tmp_path: Path, monkeypatch
) -> None:
    from scripts import _icons

    heroes_path = tmp_path / "heroes.json"
    heroes_path.write_text('{"npc_dota_hero_axe": {"id": 2}}', encoding="utf-8")
    out_dir = tmp_path / "hero_icons"
    out_dir.mkdir()
    (out_dir / "axe.png").write_bytes(b"<html>cdn error</html>")
    responses = [b"not-a-png", _PNG_BYTES]

    monkeypatch.setattr(
        _icons.urllib.request, "urlopen", lambda *a, **k: _Response(responses.pop(0))
    )
    monkeypatch.setattr(_icons.time, "sleep", lambda _seconds: None)

    result = _icons.download_hero_icons(heroes_path=heroes_path, out_dir=out_dir)

    assert (result.downloaded, result.skipped, result.failed) == (1, 0, 0)
    assert (out_dir / "axe.png").read_bytes() == _PNG_BYTES


def test_fetch_scripts_do_not_import_the_report() -> None:
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    for script in ("fetch_hero_icons.py", "fetch_item_icons.py"):
        code = (
            f"import runpy, sys; sys.argv = ['{script}', '--check']\n"
            f"try:\n    runpy.run_path(r'{root / 'scripts' / script}', run_name='__main__')\n"
            "except SystemExit:\n    pass\n"
            "assert 'gem.reports' not in sys.modules"
        )
        subprocess.run([sys.executable, "-c", code], check=True, capture_output=True)
