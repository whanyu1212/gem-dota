"""Download hero and item icons from the Dota 2 CDN into the source tree.

Shared by ``fetch_hero_icons.py`` and ``fetch_item_icons.py``. The icons land in
``src/gem/data/hero_icons`` and ``item_icons``, which the docs site export copies
from; they are not committed and not shipped in the wheel.

This is the CDN download from ``gem.reports.asset_cache``, kept here so the
tooling no longer depends on the HTML report, which is deprecated (HY-136).
"""

from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "src" / "gem" / "data"
HEROES_JSON = DATA_DIR / "heroes.json"
ITEMS_JSON = DATA_DIR / "items.json"
HERO_ICON_DIR = DATA_DIR / "hero_icons"
ITEM_ICON_DIR = DATA_DIR / "item_icons"

_HERO_CDN_URLS = (
    "https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{short}_icon.png",
    "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/heroes/{short}_icon.png",
    "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/icons/{short}.png",
    "https://cdn.stratz.com/images/dota2/heroes/{short}_icon.png",
)
_ITEM_CDN_URLS = (
    "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/{short}.png",
    "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/items/{short}_lg.png",
)
_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


@dataclass(frozen=True)
class IconDownloadResult:
    """Summary of one icon download run."""

    label: str
    out_dir: Path
    downloaded: int
    skipped: int
    failed: int


def hero_icon_shorts(heroes_path: str | Path = HEROES_JSON) -> tuple[str, ...]:
    """Return the expected hero icon names (``axe``, ...) from ``heroes.json``."""
    heroes: dict[str, object] = json.loads(Path(heroes_path).read_text(encoding="utf-8"))
    return tuple(npc_name.removeprefix("npc_dota_hero_") for npc_name in sorted(heroes))


def item_icon_shorts(
    items_path: str | Path = ITEMS_JSON, *, include_recipes: bool = False
) -> tuple[str, ...]:
    """Return the expected item icon names (``blink``, ...) from ``items.json``."""
    items: dict[str, object] = json.loads(Path(items_path).read_text(encoding="utf-8"))
    shorts = (key.removeprefix("item_") for key in sorted(items))
    return tuple(s for s in shorts if include_recipes or not s.startswith("recipe_"))


def missing_hero_icons(
    heroes_path: str | Path = HEROES_JSON, out_dir: str | Path = HERO_ICON_DIR
) -> tuple[str, ...]:
    """Return the hero icon names missing from ``out_dir``."""
    icon_dir = Path(out_dir).expanduser()
    return tuple(
        s for s in hero_icon_shorts(heroes_path) if not _is_png_file(icon_dir / f"{s}.png")
    )


def missing_item_icons(
    items_path: str | Path = ITEMS_JSON,
    out_dir: str | Path = ITEM_ICON_DIR,
    *,
    include_recipes: bool = False,
) -> tuple[str, ...]:
    """Return the item icon names missing from ``out_dir``."""
    icon_dir = Path(out_dir).expanduser()
    return tuple(
        s
        for s in item_icon_shorts(items_path, include_recipes=include_recipes)
        if not _is_png_file(icon_dir / f"{s}.png")
    )


def download_hero_icons(
    *,
    force: bool = False,
    heroes_path: str | Path = HEROES_JSON,
    out_dir: str | Path = HERO_ICON_DIR,
    only: Iterable[str] | None = None,
    reporter: Callable[[str], None] | None = None,
    error_reporter: Callable[[str], None] | None = None,
) -> IconDownloadResult:
    """Download missing hero icons (all, or ``only`` these names) into ``out_dir``."""
    shorts = hero_icon_shorts(heroes_path) if only is None else tuple(only)
    return _download("hero icons", _HERO_CDN_URLS, shorts, out_dir, force, reporter, error_reporter)


def download_item_icons(
    *,
    force: bool = False,
    items_path: str | Path = ITEMS_JSON,
    out_dir: str | Path = ITEM_ICON_DIR,
    include_recipes: bool = False,
    only: Iterable[str] | None = None,
    reporter: Callable[[str], None] | None = None,
    error_reporter: Callable[[str], None] | None = None,
) -> IconDownloadResult:
    """Download missing item icons (all, or ``only`` these names) into ``out_dir``."""
    shorts = (
        item_icon_shorts(items_path, include_recipes=include_recipes)
        if only is None
        else tuple(only)
    )
    return _download("item icons", _ITEM_CDN_URLS, shorts, out_dir, force, reporter, error_reporter)


def _download(
    label: str,
    url_patterns: tuple[str, ...],
    shorts: Iterable[str],
    out_dir: str | Path,
    force: bool,
    reporter: Callable[[str], None] | None,
    error_reporter: Callable[[str], None] | None,
) -> IconDownloadResult:
    icon_dir = Path(out_dir).expanduser()
    icon_dir.mkdir(parents=True, exist_ok=True)
    ctx = _cdn_ssl_context()
    cert_failures: list[str] = []
    downloaded = failed = skipped = 0
    for short in shorts:
        out_path = icon_dir / f"{short}.png"
        if _is_png_file(out_path) and not force:
            skipped += 1
            continue
        if _download_first(
            [url.format(short=short) for url in url_patterns], out_path, ctx, cert_failures
        ):
            downloaded += 1
            _emit(reporter, f"  OK  {short}")
            time.sleep(0.05)
        else:
            failed += 1
            _emit(error_reporter, f"  FAIL {short}")
    if failed and cert_failures:
        _emit(
            error_reporter,
            f"  {len(cert_failures)} CDN request(s) failed TLS certificate verification. "
            "If this Python has no CA bundle (common with python.org macOS installs), "
            "run its 'Install Certificates.command' or `pip install certifi`.",
        )
    return IconDownloadResult(label, icon_dir, downloaded, skipped, failed)


def _cdn_ssl_context() -> ssl.SSLContext:
    # Verify certificates and hostnames. python.org macOS builds ship without a
    # CA bundle, so certifi's roots are added on top of the system store when
    # certifi is installed; without either, downloads fail with a hint.
    ctx = ssl.create_default_context()
    try:
        import certifi
    except ImportError:
        return ctx
    ctx.load_verify_locations(cafile=certifi.where())
    return ctx


def _download_first(
    urls: list[str], out_path: Path, ctx: ssl.SSLContext, cert_failures: list[str]
) -> bool:
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                data = resp.read()
            if not data.startswith(_PNG_MAGIC):
                continue
            out_path.write_bytes(data)
            return True
        except Exception as exc:
            # urlopen wraps TLS handshake failures in URLError(reason=...).
            reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
            if isinstance(reason, ssl.SSLCertVerificationError):
                cert_failures.append(url)
    return False


def _emit(reporter: Callable[[str], None] | None, message: str) -> None:
    if reporter is not None:
        reporter(message)


def _is_png_file(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            return fh.read(len(_PNG_MAGIC)) == _PNG_MAGIC
    except OSError:
        return False
