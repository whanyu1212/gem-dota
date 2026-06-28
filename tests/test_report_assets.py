from __future__ import annotations

import ssl
from pathlib import Path
from typing import Any

import gem.reports.asset_cache as asset_cache
from gem.reports import ReportAssets, add_map_image, report_asset_status

_PNG_BYTES = b"\x89PNG\r\n\x1a\nfake-png"


def test_report_asset_download_tls_context_verifies_certificates() -> None:
    ctx = asset_cache._cdn_ssl_context()

    assert ctx.verify_mode == ssl.CERT_REQUIRED
    assert ctx.check_hostname is True


def test_report_assets_auto_uses_cache_icons_and_fallback_map(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    hero_dir = root / "hero_icons"
    item_dir = root / "item_icons"
    hero_dir.mkdir(parents=True)
    item_dir.mkdir(parents=True)
    (hero_dir / "axe.png").write_bytes(_PNG_BYTES)
    (item_dir / "blink.png").write_bytes(_PNG_BYTES)
    fallback_map = tmp_path / "Game_map_7.40.jpg"
    fallback_map.write_bytes(b"map")

    assets = ReportAssets.auto(root=root, fallback_map=fallback_map)

    assert assets.hero_icon_dir == hero_dir
    assert assets.item_icon_dir == item_dir
    assert assets.map_image == fallback_map


def test_report_assets_auto_prefers_cached_map(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    map_dir = root / "maps"
    map_dir.mkdir(parents=True)
    cached_map = map_dir / "Game_map_7.40.jpg"
    cached_map.write_bytes(b"map")
    fallback_map = tmp_path / "fallback.jpg"
    fallback_map.write_bytes(b"fallback")

    assets = ReportAssets.auto(root=root, fallback_map=fallback_map)

    assert assets.map_image == cached_map


def test_report_asset_status_reports_missing_assets(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    hero_dir = root / "hero_icons"
    hero_dir.mkdir(parents=True)
    (hero_dir / "axe.png").write_bytes(_PNG_BYTES)

    status = report_asset_status(root=root)

    assert status.root == root
    assert status.hero_icons.expected > 0
    assert status.hero_icons.present >= 1
    assert "axe" not in status.hero_icons.missing
    assert status.item_icons.missing
    assert status.maps.missing == ("Game_map_7.40.jpg",)


def test_add_map_image_copies_into_cache(tmp_path: Path) -> None:
    source = tmp_path / "source-map.jpg"
    source.write_bytes(b"map")

    dest = add_map_image(source, root=tmp_path / "cache", name="Game_map_7.40.jpg")

    assert dest == tmp_path / "cache" / "maps" / "Game_map_7.40.jpg"
    assert dest.read_bytes() == b"map"


def test_item_download_uses_legacy_lg_fallback_for_missing_react_icon(
    tmp_path: Path,
    monkeypatch,
) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text('{"eternal_shroud": {"id": 1}}', encoding="utf-8")
    out_dir = tmp_path / "item_icons"
    calls: list[str] = []

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return _PNG_BYTES

    def fake_urlopen(request: Any, *, timeout: int, context: object) -> Response:
        url = request.full_url
        calls.append(url)
        if "dota_react/items" in url:
            raise OSError("missing react icon")
        assert timeout == 10
        assert context is not None
        return Response()

    monkeypatch.setattr(asset_cache.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(asset_cache.time, "sleep", lambda _seconds: None)

    result = asset_cache.download_item_icons(items_path=items_path, out_dir=out_dir)

    assert result.downloaded == 1
    assert result.failed == 0
    assert calls == [
        "https://cdn.dota2.com/apps/dota2/images/dota_react/items/eternal_shroud.png",
        "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/items/eternal_shroud_lg.png",
    ]
    assert (out_dir / "eternal_shroud.png").read_bytes() == _PNG_BYTES


def test_download_skips_non_png_responses_before_fallback(
    tmp_path: Path,
    monkeypatch,
) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text('{"wind_lace": {"id": 1}}', encoding="utf-8")
    out_dir = tmp_path / "item_icons"
    responses = [b"not-a-png", _PNG_BYTES]

    class Response:
        def __init__(self, data: bytes) -> None:
            self._data = data

        def __enter__(self) -> Response:
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return self._data

    def fake_urlopen(request: Any, *, timeout: int, context: object) -> Response:
        assert request.full_url
        assert timeout == 10
        assert context is not None
        return Response(responses.pop(0))

    monkeypatch.setattr(asset_cache.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(asset_cache.time, "sleep", lambda _seconds: None)

    result = asset_cache.download_item_icons(items_path=items_path, out_dir=out_dir)

    assert result.downloaded == 1
    assert result.failed == 0
    assert (out_dir / "wind_lace.png").read_bytes() == _PNG_BYTES


def test_invalid_existing_item_icon_is_redownloaded_without_force(
    tmp_path: Path,
    monkeypatch,
) -> None:
    items_path = tmp_path / "items.json"
    items_path.write_text('{"eternal_shroud": {"id": 1}}', encoding="utf-8")
    out_dir = tmp_path / "item_icons"
    out_dir.mkdir()
    out_path = out_dir / "eternal_shroud.png"
    out_path.write_bytes(b"<html>cdn error</html>")

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return _PNG_BYTES

    def fake_urlopen(request: Any, *, timeout: int, context: object) -> Response:
        url = request.full_url
        if "dota_react/items" in url:
            raise OSError("missing react icon")
        assert timeout == 10
        assert context is not None
        return Response()

    monkeypatch.setattr(asset_cache.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(asset_cache.time, "sleep", lambda _seconds: None)

    result = asset_cache.download_item_icons(items_path=items_path, out_dir=out_dir)

    assert result.downloaded == 1
    assert result.skipped == 0
    assert result.failed == 0
    assert out_path.read_bytes() == _PNG_BYTES


def test_invalid_existing_icon_is_redownloaded_without_force(
    tmp_path: Path,
    monkeypatch,
) -> None:
    heroes_path = tmp_path / "heroes.json"
    heroes_path.write_text('{"npc_dota_hero_ringmaster": {"id": 1}}', encoding="utf-8")
    out_dir = tmp_path / "hero_icons"
    out_dir.mkdir()
    out_path = out_dir / "ringmaster.png"
    out_path.write_bytes(b"RIFF-webp")

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return _PNG_BYTES

    def fake_urlopen(request: Any, *, timeout: int, context: object) -> Response:
        url = request.full_url
        if "dota_react/heroes/icons" not in url:
            raise OSError("try next fallback")
        assert timeout == 10
        assert context is not None
        return Response()

    monkeypatch.setattr(asset_cache.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(asset_cache.time, "sleep", lambda _seconds: None)

    result = asset_cache.download_hero_icons(heroes_path=heroes_path, out_dir=out_dir)

    assert result.downloaded == 1
    assert result.skipped == 0
    assert result.failed == 0
    assert out_path.read_bytes() == _PNG_BYTES
