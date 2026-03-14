"""Shared helper utilities for the example match report."""

from __future__ import annotations

import html

from gem.constants import hero_short

TICKS_PER_SEC = 30
TICKS_PER_MIN = TICKS_PER_SEC * 60

TEAM_COLOR_CSS: dict[int, str] = {2: "#4caf50", 3: "#f44336"}
TEAM_NAMES: dict[int, str] = {2: "Radiant", 3: "Dire"}

# World-coordinate bounds calibrated against Game_map_7.40.jpg.
MAP_XMIN, MAP_XMAX = 7563, 25900
MAP_YMIN, MAP_YMAX = 7800, 25600

# Rune type → display name.
# Reference: DOTA_RUNE_TYPE enum in dota_shared_enums.proto
RUNE_NAMES: dict[int, str] = {
    0: "Double Damage",
    1: "Haste",
    2: "Illusion",
    3: "Invisibility",
    4: "Regeneration",
    5: "Bounty",
    6: "Arcane",
    7: "Water",
    8: "Wisdom",
    9: "Shield",
}

# Rune type → short icon name (under item_icons/rune_<name>.png).
RUNE_ICON_SHORT: dict[int, str] = {
    0: "rune_doubledamage",
    1: "rune_haste",
    2: "rune_illusion",
    3: "rune_invisibility",
    4: "rune_regen",
    5: "rune_bounty",
    6: "rune_arcane",
    7: "rune_water",
    8: "rune_wisdom",
    9: "rune_shield",
}

GAME_MODES: dict[int, str] = {
    1: "All Pick",
    2: "Captain's Mode",
    3: "Random Draft",
    4: "Single Draft",
    5: "All Random",
    12: "Least Played",
    13: "New Player Pool",
    14: "Compendium",
    15: "Custom",
    16: "Captain's Draft",
    18: "Ability Draft",
    20: "All Random Death Match",
    21: "1v1 Solo Mid",
    22: "All Pick Ranked",
    23: "Turbo",
    24: "Mutation",
}

# Set at report-build time so fmt_tick() produces game-relative times
_GAME_START_TICK: int = 0


def set_game_start_tick(tick: int) -> None:
    """Set the game start tick used by fmt_tick()."""
    global _GAME_START_TICK
    _GAME_START_TICK = tick


def fmt_tick(tick: int) -> str:
    """Format a game tick as MM:SS relative to game start."""
    rel = tick - _GAME_START_TICK
    neg = rel < 0
    secs = abs(rel) // TICKS_PER_SEC
    s = f"{secs // 60:02d}:{secs % 60:02d}"
    return f"-{s}" if neg else s


def hero(npc_name: str) -> str:
    """Shorten an NPC hero name to a display name."""
    return hero_short(npc_name) if npc_name else "?"


def team_name(team: int) -> str:
    """Return team display name."""
    return TEAM_NAMES.get(team, f"Team{team}")


def e(s: str) -> str:
    """HTML-escape a string."""
    return html.escape(str(s))


def team_badge(team: int) -> str:
    """Build a colored team badge span."""
    color = TEAM_COLOR_CSS.get(team, "#888")
    return f'<span style="color:{color};font-weight:bold">{e(team_name(team))}</span>'
