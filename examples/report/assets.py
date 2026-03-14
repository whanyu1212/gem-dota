"""Asset and icon helpers for the HTML match report."""

from __future__ import annotations

import base64
import html
from pathlib import Path

_ITEM_ICONS_DIR = Path(__file__).parent.parent.parent / "src" / "gem" / "data" / "item_icons"
_HERO_ICONS_DIR = Path(__file__).parent.parent.parent / "src" / "gem" / "data" / "hero_icons"

# Global caches: short_name → "data:image/png;base64,..." (populated at build time)
ITEM_ICON_B64: dict[str, str] = {}
HERO_ICON_B64: dict[str, str] = {}

# Placeholder icon (1×1 grey PNG) used when a hero icon file is missing
HERO_PLACEHOLDER_B64 = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)


def load_item_icons(short_names: list[str]) -> None:
    """Load item icons from disk into ``ITEM_ICON_B64``."""
    for short in short_names:
        if short in ITEM_ICON_B64:
            continue
        path = _ITEM_ICONS_DIR / f"{short}.png"
        if path.exists():
            ITEM_ICON_B64[short] = (
                "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            )


def item_icon_tag(item_key: str, size: int = 24) -> str:
    """Return an ``<img>`` tag for an item icon, or empty string if unavailable."""
    short = item_key.removeprefix("item_")
    src = ITEM_ICON_B64.get(short, "")
    if not src:
        return ""
    return (
        f'<img src="{src}" width="{size}" height="{size}" '
        f'style="vertical-align:middle;border-radius:3px;margin-right:4px" '
        f'title="{html.escape(short)}">'
    )


def load_hero_icons(npc_names: list[str]) -> None:
    """Load hero portrait icons from disk into ``HERO_ICON_B64``."""
    for npc in npc_names:
        short = npc.removeprefix("npc_dota_hero_")
        if short in HERO_ICON_B64:
            continue
        path = _HERO_ICONS_DIR / f"{short}.png"
        if path.exists():
            HERO_ICON_B64[short] = (
                "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            )


def hero_icon_src(npc_name: str) -> str:
    """Return a base64 data URI for a hero portrait, or the placeholder."""
    short = npc_name.removeprefix("npc_dota_hero_")
    return HERO_ICON_B64.get(short, HERO_PLACEHOLDER_B64)
