from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from PIL import Image

import gem.reports.asset_cache as asset_cache
import gem.reports.assets as report_assets
import gem.reports.builder as builder
from gem.combat.log import CombatLogEntry
from gem.extractors.draft import DraftEvent
from gem.reports import ReportAssets, add_map_image, report_asset_status
from gem.results.models import ParsedMatch, ParsedPlayer

_PNG_BYTES = b"\x89PNG\r\n\x1a\nfake-png"


def test_checkout_map_uses_patch_741_at_legacy_resolution() -> None:
    map_dir = Path(__file__).resolve().parents[1] / "assets" / "maps"
    map_path = map_dir / "Game_map_7.41.jpg"

    with Image.open(map_path) as image:
        assert image.size == (8878, 8356)
        assert image.format == "JPEG"
    assert not (map_dir / "Game_map_7.40.jpg").exists()


def test_report_assets_auto_uses_cache_icons_and_fallback_map(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    hero_dir = root / "hero_icons"
    item_dir = root / "item_icons"
    hero_dir.mkdir(parents=True)
    item_dir.mkdir(parents=True)
    (hero_dir / "axe.png").write_bytes(_PNG_BYTES)
    (item_dir / "blink.png").write_bytes(_PNG_BYTES)
    fallback_map = tmp_path / "Game_map_7.41.jpg"
    fallback_map.write_bytes(b"map")

    assets = ReportAssets.auto(root=root, fallback_map=fallback_map)

    assert assets.hero_icon_dir == hero_dir
    assert assets.item_icon_dir == item_dir
    assert assets.map_image == fallback_map


def test_report_assets_auto_prefers_cached_map(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    map_dir = root / "maps"
    map_dir.mkdir(parents=True)
    cached_map = map_dir / "Game_map_7.41.jpg"
    cached_map.write_bytes(b"map")
    fallback_map = tmp_path / "fallback.jpg"
    fallback_map.write_bytes(b"fallback")

    assets = ReportAssets.auto(root=root, fallback_map=fallback_map)

    assert assets.map_image == cached_map


def test_report_assets_auto_falls_back_to_checkout_map(tmp_path: Path, monkeypatch: Any) -> None:
    empty_cache = tmp_path / "cache"
    monkeypatch.setattr(asset_cache, "default_report_asset_dir", lambda: empty_cache)
    source_maps = tmp_path / "assets" / "maps"
    source_maps.mkdir(parents=True)
    checkout_map = source_maps / "Game_map_7.41.jpg"
    checkout_map.write_bytes(b"map")
    (source_maps / "camp_annotated.png").write_bytes(_PNG_BYTES)
    monkeypatch.setattr(asset_cache, "SOURCE_MAP_DIR", source_maps)

    assert ReportAssets.auto().map_image == checkout_map

    explicit = tmp_path / "explicit.jpg"
    explicit.write_bytes(b"explicit")
    assert ReportAssets.auto(fallback_map=explicit).map_image == explicit

    # An explicit cache root opts out of checkout fallbacks, as for icons.
    assert ReportAssets.auto(root=empty_cache).map_image is None
    # Only the named patch map is used, never another image in the folder.
    checkout_map.unlink()
    assert ReportAssets.auto().map_image is None


def test_checkout_map_dir_points_at_repository_assets() -> None:
    assert Path(__file__).resolve().parents[1] / "assets" / "maps" == asset_cache.SOURCE_MAP_DIR
    assert (asset_cache.SOURCE_MAP_DIR / asset_cache.DEFAULT_MAP_NAME).exists()


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
    assert status.maps.missing == ("Game_map_7.41.jpg",)


def test_add_map_image_copies_into_cache(tmp_path: Path) -> None:
    source = tmp_path / "source-map.jpg"
    source.write_bytes(b"map")

    dest = add_map_image(source, root=tmp_path / "cache", name="Game_map_7.41.jpg")

    assert dest == tmp_path / "cache" / "maps" / "Game_map_7.41.jpg"
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


# ---------------------------------------------------------------------------
# Missing icons: tracking, warning, and fetching one match's icons (HY-94)
# ---------------------------------------------------------------------------


def _icon_match() -> ParsedMatch:
    return ParsedMatch(
        players=[
            ParsedPlayer(
                player_id=0,
                hero_name="npc_dota_hero_kez",
                purchase_log=[
                    CombatLogEntry(tick=1, log_type="PURCHASE", value_name="item_blink"),
                    CombatLogEntry(tick=2, log_type="PURCHASE", value_name="item_not_an_item"),
                ],
            )
        ],
        draft=[
            DraftEvent(
                tick=0, slot_index=0, hero_id=1, hero_name="npc_dota_hero_axe", is_pick=False
            )
        ],
        combat_log=[
            CombatLogEntry(tick=3, log_type="DAMAGE", inflictor_name="item_dagon_5"),
            CombatLogEntry(tick=4, log_type="DAMAGE", inflictor_name="lina_laguna_blade"),
        ],
    )


def test_match_icon_shorts_lists_the_matchs_downloadable_icons() -> None:
    heroes, items = asset_cache.match_icon_shorts(_icon_match())

    # Draft bans and players; unknown names are dropped.
    assert heroes == ("axe", "kez")
    assert set(items) == {"blink", "dagon_5", "ward_observer", "ward_sentry", "smoke_of_deceit"}


def test_icon_loaders_record_missing_icons(tmp_path: Path) -> None:
    hero_dir = tmp_path / "hero_icons"
    hero_dir.mkdir()
    (hero_dir / "axe.png").write_bytes(_PNG_BYTES)
    assets = ReportAssets(hero_icon_dir=hero_dir, item_icon_dir=None)
    report_assets.configure_assets(assets)

    report_assets.load_hero_icons(["npc_dota_hero_axe", "npc_dota_hero_kez"])
    report_assets.load_item_icons(["blink"])

    missing_heroes = report_assets.MISSING_HERO_ICONS
    missing_items = report_assets.MISSING_ITEM_ICONS
    assert missing_heroes == {"kez"}
    assert missing_items == {"blink"}
    report_assets.configure_assets(assets)
    assert not report_assets.MISSING_HERO_ICONS
    assert not report_assets.MISSING_ITEM_ICONS


def test_report_warns_with_the_missing_downloadable_icons(caplog: Any) -> None:
    report_assets.configure_assets(ReportAssets())
    report_assets.MISSING_HERO_ICONS.update({"kez", "not_a_hero"})
    report_assets.MISSING_ITEM_ICONS.update({"rune_haste"})  # no download source

    with caplog.at_level(logging.WARNING, logger="gem.reports.builder"):
        builder._warn_missing_icons()

    assert len(caplog.records) == 1
    message = caplog.records[0].getMessage()
    assert "1 hero(es): kez" in message
    assert "not_a_hero" not in message
    assert "rune_haste" not in message
    assert "fetch_match_icons" in message
    report_assets.configure_assets(ReportAssets())


def test_report_is_quiet_when_every_icon_is_cached(caplog: Any) -> None:
    report_assets.configure_assets(ReportAssets())
    with caplog.at_level(logging.WARNING, logger="gem.reports.builder"):
        builder._warn_missing_icons()
    assert not caplog.records


def test_fetch_match_icons_downloads_only_the_matchs_missing_icons(
    tmp_path: Path, monkeypatch: Any
) -> None:
    hero_dir = tmp_path / "hero_icons"
    item_dir = tmp_path / "item_icons"
    hero_dir.mkdir()
    item_dir.mkdir()
    (hero_dir / "axe.png").write_bytes(_PNG_BYTES)  # already cached
    requested: list[str] = []

    def fake_download(urls: list[str], out_path: Path, ctx: object) -> bool:
        requested.append(out_path.name)
        out_path.write_bytes(_PNG_BYTES)
        return True

    monkeypatch.setattr(asset_cache, "_download_first", fake_download)
    monkeypatch.setattr(asset_cache.time, "sleep", lambda _seconds: None)
    assets = ReportAssets(
        map_image=tmp_path / "map.jpg", hero_icon_dir=hero_dir, item_icon_dir=item_dir
    )

    fetched = asset_cache.fetch_match_icons(_icon_match(), assets)

    assert sorted(requested) == sorted(
        [
            "kez.png",
            "blink.png",
            "dagon_5.png",
            "ward_observer.png",
            "ward_sentry.png",
            "smoke_of_deceit.png",
        ]
    )
    assert fetched == assets
    assert (hero_dir / "kez.png").exists()


def test_fetch_match_icons_fills_the_cache_when_no_icon_dir_is_set(
    tmp_path: Path, monkeypatch: Any
) -> None:
    def fake_download(urls: list[str], out_path: Path, ctx: object) -> bool:
        out_path.write_bytes(_PNG_BYTES)
        return True

    monkeypatch.setattr(asset_cache, "_download_first", fake_download)
    monkeypatch.setattr(asset_cache.time, "sleep", lambda _seconds: None)
    root = tmp_path / "cache"

    fetched = asset_cache.fetch_match_icons(_icon_match(), ReportAssets(), root=root)

    assert fetched.hero_icon_dir == root / "hero_icons"
    assert fetched.item_icon_dir == root / "item_icons"
    assert (root / "hero_icons" / "kez.png").exists()
