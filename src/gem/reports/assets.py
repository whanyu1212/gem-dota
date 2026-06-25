"""Asset and icon helpers for HTML match reports."""

from __future__ import annotations

import base64
import html
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReportAssets:
    """Optional local assets used to enrich generated HTML reports.

    ``gem`` does not ship map images or downloaded hero/item icon caches in the
    wheel. Pass paths here when those assets are available locally.

    Attributes:
        map_image: Local map image to use as minimap/report background.
        hero_icon_dir: Directory containing ``<hero_short>.png`` hero icons.
        item_icon_dir: Directory containing ``<item_short>.png`` item icons.
    """

    map_image: str | Path | None = None
    hero_icon_dir: str | Path | None = None
    item_icon_dir: str | Path | None = None

    @classmethod
    def auto(
        cls,
        *,
        root: str | Path | None = None,
        fallback_map: str | Path | None = None,
        map_name: str = "Game_map_7.40.jpg",
    ) -> ReportAssets:
        """Discover local report assets from the configured asset cache."""

        from gem.reports.asset_cache import auto_report_assets

        return auto_report_assets(root=root, fallback_map=fallback_map, map_name=map_name)


# Global caches: short_name → "data:image/png;base64,..." (populated at build time)
ITEM_ICON_B64: dict[str, str] = {}
HERO_ICON_B64: dict[str, str] = {}
_CURRENT_ASSETS = ReportAssets()

# Placeholder icon (1×1 grey PNG) used when a hero icon file is missing
HERO_PLACEHOLDER_B64 = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)
_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def configure_assets(assets: ReportAssets | None = None) -> None:
    """Set the asset source used by subsequent section renderers.

    Existing icon caches are cleared so repeated report builds with different
    asset directories cannot leak stale icons into later reports.
    """

    global _CURRENT_ASSETS
    _CURRENT_ASSETS = assets or ReportAssets()
    ITEM_ICON_B64.clear()
    HERO_ICON_B64.clear()


def _path(value: str | Path | None) -> Path | None:
    if value is None:
        return None
    return Path(value).expanduser()


def load_map_base64(map_image: str | Path | None) -> str | None:
    """Load a local map image as a base64 string.

    Returns ``None`` when no image is configured or the path does not exist.
    """

    path = _path(map_image)
    if path is None or not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode()


def load_item_icons(short_names: list[str], assets: ReportAssets | None = None) -> None:
    """Load item icons from disk into ``ITEM_ICON_B64``."""
    icon_dir = _path((assets or _CURRENT_ASSETS).item_icon_dir)
    if icon_dir is None:
        return
    for short in short_names:
        if short in ITEM_ICON_B64:
            continue
        path = icon_dir / f"{short}.png"
        if _is_png_file(path):
            ITEM_ICON_B64[short] = (
                "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            )


def _text_chip(label: str, *, size: int = 24, title: str | None = None) -> str:
    """Return a compact rounded name pill used when an icon is unavailable.

    The font size and padding scale loosely with ``size`` so a chip used in
    place of a ``size``-px icon stays visually proportionate in dense tables.

    Args:
        label: Human-readable text shown inside the chip.
        size: Pixel size of the icon this chip replaces; scales the chip.
        title: Optional tooltip text (defaults to ``label``).

    Returns:
        An HTML ``<span>`` fragment.
    """
    font_px = max(9, min(13, round(size * 0.5)))
    pad_y = max(1, round(size * 0.08))
    pad_x = max(3, round(size * 0.22))
    return (
        f'<span class="gem-name-chip" title="{html.escape(title or label)}" '
        f'style="display:inline-block;padding:{pad_y}px {pad_x}px;margin-right:4px;'
        f"border-radius:4px;background:#21262d;color:#c9d1d9;"
        f"font-size:{font_px}px;line-height:1.2;vertical-align:middle;"
        f'white-space:nowrap">{html.escape(label)}</span>'
    )


def _item_label(item_key: str) -> str:
    """Best-effort readable label for an item, for icon-less fallback chips."""
    from gem.constants import item_display

    short = item_key.removeprefix("item_")
    display = item_display(item_key) or item_display(short)
    return display or short.replace("_", " ")


def item_icon_tag(item_key: str, size: int = 24) -> str:
    """Return an item icon ``<img>``, or a readable name chip if unavailable.

    When the item's icon is not in the loaded cache (no icon cache, or the
    individual file is missing), a compact text chip with the item's display
    name is returned instead of an empty string, so reports stay readable
    without downloaded assets.
    """
    short = item_key.removeprefix("item_")
    src = ITEM_ICON_B64.get(short, "")
    if not src:
        if not short:
            return ""
        return _text_chip(_item_label(item_key), size=size)
    return (
        f'<img src="{src}" width="{size}" height="{size}" '
        f'style="vertical-align:middle;border-radius:3px;margin-right:4px" '
        f'title="{html.escape(short)}">'
    )


def load_hero_icons(npc_names: list[str], assets: ReportAssets | None = None) -> None:
    """Load hero portrait icons from disk into ``HERO_ICON_B64``."""
    icon_dir = _path((assets or _CURRENT_ASSETS).hero_icon_dir)
    if icon_dir is None:
        return
    for npc in npc_names:
        short = npc.removeprefix("npc_dota_hero_")
        if short in HERO_ICON_B64:
            continue
        path = icon_dir / f"{short}.png"
        if _is_png_file(path):
            HERO_ICON_B64[short] = (
                "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            )


def hero_icon_src(npc_name: str) -> str:
    """Return a base64 data URI for a hero portrait, or the placeholder."""
    short = npc_name.removeprefix("npc_dota_hero_")
    return HERO_ICON_B64.get(short, HERO_PLACEHOLDER_B64)


def has_hero_icon(npc_name: str) -> bool:
    """Return whether a real hero portrait is loaded for ``npc_name``.

    Used by section renderers to decide between a portrait ``<img>`` and a
    name-only fallback when no icon cache is configured.
    """
    return npc_name.removeprefix("npc_dota_hero_") in HERO_ICON_B64


def _is_png_file(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("rb") as fh:
            return fh.read(len(_PNG_MAGIC)).startswith(_PNG_MAGIC)
    except OSError:
        return False
