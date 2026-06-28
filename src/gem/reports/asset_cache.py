"""Report asset cache discovery, status, and download helpers."""

from __future__ import annotations

import json
import os
import platform
import shutil
import ssl
import time
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from gem.reports.assets import ReportAssets

REPORT_ASSET_ENV = "GEM_REPORT_ASSET_DIR"
DEFAULT_MAP_NAME = "Game_map_7.40.jpg"

HERO_ICON_SUBDIR = "hero_icons"
ITEM_ICON_SUBDIR = "item_icons"
MAP_SUBDIR = "maps"

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
HEROES_JSON = DATA_DIR / "heroes.json"
ITEMS_JSON = DATA_DIR / "items.json"
SOURCE_HERO_ICON_DIR = DATA_DIR / HERO_ICON_SUBDIR
SOURCE_ITEM_ICON_DIR = DATA_DIR / ITEM_ICON_SUBDIR

_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
_HERO_CDN_URLS = (
    "https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{short}_icon.png",
    "https://cdn.dota2.com/apps/dota2/images/heroes/{short}_icon.png",
    "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/icons/{short}.png",
    "https://cdn.stratz.com/images/dota2/heroes/{short}_icon.png",
)
_ITEM_CDN_URLS = (
    "https://cdn.dota2.com/apps/dota2/images/dota_react/items/{short}.png",
    "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/items/{short}_lg.png",
)
_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# Some heroes use a different short name on the CDN.
_HERO_CDN_OVERRIDES: dict[str, str] = {
    "dawnbreaker": "dawnbreaker",
    "kez": "kez",
    "marci": "marci",
    "muerta": "muerta",
    "primal_beast": "primal_beast",
    "ringmaster": "ringmaster",
    "void_spirit": "void_spirit",
}


@dataclass(frozen=True)
class ReportAssetPaths:
    """Filesystem locations used for local report assets."""

    root: Path
    hero_icon_dir: Path
    item_icon_dir: Path
    map_dir: Path


@dataclass(frozen=True)
class AssetKindStatus:
    """Status for one asset kind in a report asset cache."""

    label: str
    path: Path
    expected: int
    present: int
    missing: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return not self.missing


@dataclass(frozen=True)
class ReportAssetStatus:
    """Status snapshot for a complete report asset cache."""

    root: Path
    hero_icons: AssetKindStatus
    item_icons: AssetKindStatus
    maps: AssetKindStatus

    @property
    def complete(self) -> bool:
        return self.hero_icons.complete and self.item_icons.complete and self.maps.complete


@dataclass(frozen=True)
class IconDownloadResult:
    """Summary of one icon download run."""

    label: str
    out_dir: Path
    downloaded: int
    skipped: int
    failed: int


def default_report_asset_dir() -> Path:
    """Return the default user cache directory for report assets.

    Set ``GEM_REPORT_ASSET_DIR`` to override this location.
    """

    configured = os.environ.get(REPORT_ASSET_ENV)
    if configured:
        return Path(configured).expanduser()

    system = platform.system()
    if system == "Darwin":
        base = Path("~/Library/Caches").expanduser()
    elif system == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", "~/AppData/Local")).expanduser()
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", "~/.cache")).expanduser()

    return base / "gem-dota" / "reports"


def report_asset_paths(root: str | Path | None = None) -> ReportAssetPaths:
    """Resolve the cache subdirectories used by reports."""

    root_path = Path(root).expanduser() if root is not None else default_report_asset_dir()
    return ReportAssetPaths(
        root=root_path,
        hero_icon_dir=root_path / HERO_ICON_SUBDIR,
        item_icon_dir=root_path / ITEM_ICON_SUBDIR,
        map_dir=root_path / MAP_SUBDIR,
    )


def ensure_report_asset_dirs(root: str | Path | None = None) -> ReportAssetPaths:
    """Create and return the report asset cache directories."""

    paths = report_asset_paths(root)
    paths.hero_icon_dir.mkdir(parents=True, exist_ok=True)
    paths.item_icon_dir.mkdir(parents=True, exist_ok=True)
    paths.map_dir.mkdir(parents=True, exist_ok=True)
    return paths


def auto_report_assets(
    *,
    root: str | Path | None = None,
    fallback_map: str | Path | None = None,
    map_name: str = DEFAULT_MAP_NAME,
) -> ReportAssets:
    """Build a ``ReportAssets`` value from the configured cache.

    The user cache is checked first. In source checkouts, the local
    ``src/gem/data/*_icons`` directories are used as a development fallback
    when no explicit cache root is supplied. ``fallback_map`` is useful for
    examples that keep a map image in the repository instead of the user cache.
    """

    paths = report_asset_paths(root)
    use_source_fallback = root is None

    map_image = _choose_map(paths.map_dir, map_name)
    if map_image is None:
        map_image = _existing_file(fallback_map)

    hero_icon_dir = _populated_icon_dir(paths.hero_icon_dir)
    item_icon_dir = _populated_icon_dir(paths.item_icon_dir)
    if use_source_fallback:
        hero_icon_dir = hero_icon_dir or _populated_icon_dir(SOURCE_HERO_ICON_DIR)
        item_icon_dir = item_icon_dir or _populated_icon_dir(SOURCE_ITEM_ICON_DIR)

    return ReportAssets(
        map_image=map_image,
        hero_icon_dir=hero_icon_dir,
        item_icon_dir=item_icon_dir,
    )


def report_asset_status(
    *,
    root: str | Path | None = None,
    include_recipes: bool = False,
    map_name: str = DEFAULT_MAP_NAME,
) -> ReportAssetStatus:
    """Return cache completeness for maps and hero/item icons."""

    paths = report_asset_paths(root)
    hero_expected = hero_icon_shorts()
    item_expected = item_icon_shorts(include_recipes=include_recipes)
    hero_missing = missing_hero_icons(out_dir=paths.hero_icon_dir)
    item_missing = missing_item_icons(out_dir=paths.item_icon_dir, include_recipes=include_recipes)
    map_files = _map_files(paths.map_dir)
    map_missing = () if map_files else (map_name,)

    return ReportAssetStatus(
        root=paths.root,
        hero_icons=AssetKindStatus(
            label="Hero icons",
            path=paths.hero_icon_dir,
            expected=len(hero_expected),
            present=len(hero_expected) - len(hero_missing),
            missing=hero_missing,
        ),
        item_icons=AssetKindStatus(
            label="Item icons",
            path=paths.item_icon_dir,
            expected=len(item_expected),
            present=len(item_expected) - len(item_missing),
            missing=item_missing,
        ),
        maps=AssetKindStatus(
            label="Map images",
            path=paths.map_dir,
            expected=1,
            present=1 if map_files else 0,
            missing=map_missing,
        ),
    )


def add_map_image(
    source: str | Path,
    *,
    root: str | Path | None = None,
    name: str | None = None,
) -> Path:
    """Copy a map image into the report asset cache and return its new path."""

    source_path = Path(source).expanduser()
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    paths = ensure_report_asset_dirs(root)
    dest = paths.map_dir / (name or source_path.name)
    shutil.copy2(source_path, dest)
    return dest


def hero_icon_shorts(heroes_path: str | Path = HEROES_JSON) -> tuple[str, ...]:
    """Return expected hero icon short names from ``heroes.json``."""

    heroes: dict[str, object] = json.loads(Path(heroes_path).read_text(encoding="utf-8"))
    return tuple(_hero_short(npc_name) for npc_name in sorted(heroes))


def item_icon_shorts(
    items_path: str | Path = ITEMS_JSON,
    *,
    include_recipes: bool = False,
) -> tuple[str, ...]:
    """Return expected item icon short names from ``items.json``."""

    items: dict[str, object] = json.loads(Path(items_path).read_text(encoding="utf-8"))
    shorts: list[str] = []
    for item_key in sorted(items):
        short = _item_short(item_key)
        if short.startswith("recipe_") and not include_recipes:
            continue
        shorts.append(short)
    return tuple(shorts)


def missing_hero_icons(
    heroes_path: str | Path = HEROES_JSON,
    out_dir: str | Path | None = None,
) -> tuple[str, ...]:
    """Return hero short names missing from an icon directory."""

    icon_dir = (
        Path(out_dir).expanduser() if out_dir is not None else report_asset_paths().hero_icon_dir
    )
    return tuple(
        short
        for short in hero_icon_shorts(heroes_path)
        if not _is_png_file(icon_dir / f"{short}.png")
    )


def missing_item_icons(
    items_path: str | Path = ITEMS_JSON,
    out_dir: str | Path | None = None,
    *,
    include_recipes: bool = False,
) -> tuple[str, ...]:
    """Return item short names missing from an icon directory."""

    icon_dir = (
        Path(out_dir).expanduser() if out_dir is not None else report_asset_paths().item_icon_dir
    )
    return tuple(
        short
        for short in item_icon_shorts(items_path, include_recipes=include_recipes)
        if not _is_png_file(icon_dir / f"{short}.png")
    )


def download_hero_icons(
    *,
    force: bool = False,
    heroes_path: str | Path = HEROES_JSON,
    out_dir: str | Path | None = None,
    reporter: Callable[[str], None] | None = None,
    error_reporter: Callable[[str], None] | None = None,
) -> IconDownloadResult:
    """Download missing hero icons into the report asset cache."""

    icon_dir = _download_dir(out_dir, HERO_ICON_SUBDIR)
    ctx = _cdn_ssl_context()
    downloaded = failed = skipped = 0

    for short in hero_icon_shorts(heroes_path):
        out_path = icon_dir / f"{short}.png"
        if _is_png_file(out_path) and not force:
            skipped += 1
            continue

        cdn_short = _HERO_CDN_OVERRIDES.get(short, short)
        urls = [url.format(short=cdn_short) for url in _HERO_CDN_URLS]
        if _download_first(urls, out_path, ctx):
            downloaded += 1
            _emit(reporter, f"  OK  {short}")
            time.sleep(0.05)
        else:
            failed += 1
            _emit(error_reporter, f"  FAIL {short}")

    return IconDownloadResult(
        label="hero icons",
        out_dir=icon_dir,
        downloaded=downloaded,
        skipped=skipped,
        failed=failed,
    )


def download_item_icons(
    *,
    force: bool = False,
    items_path: str | Path = ITEMS_JSON,
    out_dir: str | Path | None = None,
    include_recipes: bool = False,
    reporter: Callable[[str], None] | None = None,
    error_reporter: Callable[[str], None] | None = None,
) -> IconDownloadResult:
    """Download missing item icons into the report asset cache."""

    icon_dir = _download_dir(out_dir, ITEM_ICON_SUBDIR)
    ctx = _cdn_ssl_context()
    downloaded = failed = skipped = 0

    for short in item_icon_shorts(items_path, include_recipes=include_recipes):
        out_path = icon_dir / f"{short}.png"
        if _is_png_file(out_path) and not force:
            skipped += 1
            continue

        urls = [url.format(short=short) for url in _ITEM_CDN_URLS]
        if _download_first(urls, out_path, ctx):
            downloaded += 1
            _emit(reporter, f"  OK  {short}")
            time.sleep(0.05)
        else:
            failed += 1
            _emit(error_reporter, f"  FAIL {short}")

    return IconDownloadResult(
        label="item icons",
        out_dir=icon_dir,
        downloaded=downloaded,
        skipped=skipped,
        failed=failed,
    )


def _hero_short(npc_name: str) -> str:
    return npc_name.removeprefix("npc_dota_hero_")


def _item_short(item_key: str) -> str:
    return item_key.removeprefix("item_")


def _download_dir(out_dir: str | Path | None, subdir: str) -> Path:
    if out_dir is not None:
        icon_dir = Path(out_dir).expanduser()
        icon_dir.mkdir(parents=True, exist_ok=True)
        return icon_dir

    paths = ensure_report_asset_dirs()
    return paths.hero_icon_dir if subdir == HERO_ICON_SUBDIR else paths.item_icon_dir


def _cdn_ssl_context() -> ssl.SSLContext:
    """Return the verified TLS context used for report asset downloads."""
    return ssl.create_default_context()


def _download_first(urls: list[str], out_path: Path, ctx: ssl.SSLContext) -> bool:
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                data = resp.read()
            if not _is_png_bytes(data):
                continue
            out_path.write_bytes(data)
            return True
        except Exception:
            continue
    return False


def _emit(reporter: Callable[[str], None] | None, message: str) -> None:
    if reporter is not None:
        reporter(message)


def _existing_file(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    candidate = Path(path).expanduser()
    return candidate if candidate.exists() else None


def _populated_icon_dir(path: Path) -> Path | None:
    if not path.is_dir():
        return None
    return path if any(_is_png_file(icon) for icon in path.glob("*.png")) else None


def _is_png_file(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("rb") as fh:
            return _is_png_bytes(fh.read(len(_PNG_MAGIC)))
    except OSError:
        return False


def _is_png_bytes(data: bytes) -> bool:
    return data.startswith(_PNG_MAGIC)


def _map_files(path: Path) -> tuple[Path, ...]:
    if not path.is_dir():
        return ()
    return tuple(
        sorted(p for p in path.iterdir() if p.is_file() and p.suffix.lower() in _IMAGE_SUFFIXES)
    )


def _choose_map(path: Path, map_name: str) -> Path | None:
    preferred = path / map_name
    if preferred.exists():
        return preferred
    files = _map_files(path)
    return files[0] if files else None
