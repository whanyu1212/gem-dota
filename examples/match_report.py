"""Full match report — outputs a self-contained multi-tab HTML file.

Tabs and their sections:

  Overview   — Match header (always visible), Scoreboard, Gold & XP chart
  Combat     — Damage breakdown, Kill feed
  Vision     — Ward map (interactive canvas with playback)
  Economy    — Purchase timeline, Buybacks, Runes
  Draft      — Pick/ban sequence + team picks with hero portraits
  Movement   — Interactive Plotly movement heatmap (requires plotly + map image)
  Misc       — Objectives timeline, Chat log

Built entirely on top of ``gem.parse()``. Plotly is optional — the Movement
tab is omitted if plotly is not installed or no map image is provided.

Usage:
    python examples/match_report.py path/to/replay.dem [--output report.html]
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import gem
from gem.constants import ability_display, hero_short, item_display

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TICKS_PER_SEC = 30
TICKS_PER_MIN = TICKS_PER_SEC * 60

# Set at report-build time so _fmt_tick() produces game-relative times
_GAME_START_TICK: int = 0

TEAM_COLOR_CSS: dict[int, str] = {2: "#4caf50", 3: "#f44336"}
TEAM_NAMES: dict[int, str] = {2: "Radiant", 3: "Dire"}

# Rune type → display name.
# Reference: DOTA_RUNE_TYPE enum in dota_shared_enums.proto
_RUNE_NAMES: dict[int, str] = {
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
# Icons sourced from opendota.com/assets/images/dota2/runes/{type_id}.png
# and saved as rune_<name>.png via scripts/fetch_item_icons.py.
_RUNE_ICON_SHORT: dict[int, str] = {
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

_GAME_MODES: dict[int, str] = {
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

# ---------------------------------------------------------------------------
# Item icon support
# ---------------------------------------------------------------------------

_ITEM_ICONS_DIR = Path(__file__).parent.parent / "src" / "gem" / "data" / "item_icons"
_HERO_ICONS_DIR = Path(__file__).parent.parent / "src" / "gem" / "data" / "hero_icons"

# Global caches: short_name → "data:image/png;base64,..." (populated at build time)
_ITEM_ICON_B64: dict[str, str] = {}
_HERO_ICON_B64: dict[str, str] = {}

# Placeholder icon (1×1 grey PNG) used when a hero icon file is missing
_HERO_PLACEHOLDER_B64 = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)


def _load_item_icons(short_names: list[str]) -> None:
    """Load item icons from disk into ``_ITEM_ICON_B64``."""
    for short in short_names:
        if short in _ITEM_ICON_B64:
            continue
        path = _ITEM_ICONS_DIR / f"{short}.png"
        if path.exists():
            _ITEM_ICON_B64[short] = (
                "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            )


def _item_icon_tag(item_key: str, size: int = 24) -> str:
    """Return an ``<img>`` tag for an item icon, or empty string if not available.

    Args:
        item_key: Full item key e.g. ``"item_blink"`` or short name ``"blink"``.
        size: Icon display size in pixels.

    Returns:
        HTML ``<img>`` tag, or ``""`` if icon not loaded.
    """
    short = item_key.removeprefix("item_")
    src = _ITEM_ICON_B64.get(short, "")
    if not src:
        return ""
    return (
        f'<img src="{src}" width="{size}" height="{size}" '
        f'style="vertical-align:middle;border-radius:3px;margin-right:4px" '
        f'title="{html.escape(short)}">'
    )


def _load_hero_icons(npc_names: list[str]) -> None:
    """Load hero portrait icons from disk into ``_HERO_ICON_B64``."""
    for npc in npc_names:
        short = npc.removeprefix("npc_dota_hero_")
        if short in _HERO_ICON_B64:
            continue
        path = _HERO_ICONS_DIR / f"{short}.png"
        if path.exists():
            _HERO_ICON_B64[short] = (
                "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
            )


def _hero_icon_src(npc_name: str) -> str:
    """Return a base64 data URI for a hero portrait, or the placeholder."""
    short = npc_name.removeprefix("npc_dota_hero_")
    return _HERO_ICON_B64.get(short, _HERO_PLACEHOLDER_B64)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fmt_tick(tick: int) -> str:
    """Format a game tick as MM:SS relative to game start.

    Negative values (pre-game) are shown as ``-MM:SS``.

    Args:
        tick: Absolute game tick number.

    Returns:
        Time string in [±]MM:SS format.
    """
    rel = tick - _GAME_START_TICK
    neg = rel < 0
    secs = abs(rel) // TICKS_PER_SEC
    s = f"{secs // 60:02d}:{secs % 60:02d}"
    return f"-{s}" if neg else s


def _hero(npc_name: str) -> str:
    """Shorten an NPC hero name to a display name.

    Args:
        npc_name: Full NPC hero name, e.g. ``"npc_dota_hero_axe"``.

    Returns:
        Short display name, e.g. ``"Axe"``.
    """
    return hero_short(npc_name) if npc_name else "?"


def _team_name(team: int) -> str:
    """Return team display name.

    Args:
        team: Team number (2=Radiant, 3=Dire).

    Returns:
        Team display name string.
    """
    return TEAM_NAMES.get(team, f"Team{team}")


def _e(s: str) -> str:
    """HTML-escape a string.

    Args:
        s: Input string.

    Returns:
        HTML-escaped string.
    """
    return html.escape(str(s))


def _team_badge(team: int) -> str:
    color = TEAM_COLOR_CSS.get(team, "#888")
    return f'<span style="color:{color};font-weight:bold">{_e(_team_name(team))}</span>'


# ---------------------------------------------------------------------------
# CSS — GitHub dark palette
# ---------------------------------------------------------------------------

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background: #0d1117;
    color: #e6edf3;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 14px;
    padding: 16px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

/* ---- Match header ---- */
.match-header {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    align-items: center;
}
.match-header h1 {
    font-size: 20px;
    font-weight: 700;
    flex: 1 1 100%;
}
.match-stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.match-stat .label {
    font-size: 11px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: .05em;
}
.match-stat .value {
    font-size: 16px;
    font-weight: 600;
}

/* ---- Section cards ---- */
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-bottom: 16px;
    overflow: hidden;
}

details > summary {
    list-style: none;
    cursor: pointer;
    padding: 14px 20px;
    font-weight: 600;
    font-size: 15px;
    border-bottom: 1px solid #30363d;
    user-select: none;
    display: flex;
    align-items: center;
    gap: 8px;
}
details > summary::before {
    content: "\\25B6";
    font-size: 10px;
    transition: transform .15s;
    display: inline-block;
}
details[open] > summary::before {
    transform: rotate(90deg);
}
details > summary::-webkit-details-marker { display: none; }

.card-body {
    padding: 16px 20px;
    overflow-x: auto;
}

/* ---- Tables ---- */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
thead th {
    position: sticky;
    top: 0;
    background: #1c2128;
    color: #8b949e;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: .04em;
    padding: 8px 10px;
    text-align: left;
    white-space: nowrap;
}
thead th.r { text-align: right; }
tbody tr { border-top: 1px solid #21262d; }
tbody tr:hover { background: #1c2128; }
tbody td { padding: 7px 10px; white-space: nowrap; }
tbody td.r { text-align: right; font-variant-numeric: tabular-nums; }

.row-radiant { background: rgba(76,175,80,.07); }
.row-dire    { background: rgba(244,67,54,.07); }
.row-radiant:hover { background: rgba(76,175,80,.14) !important; }
.row-dire:hover    { background: rgba(244,67,54,.14) !important; }

/* ---- Dots / badges ---- */
.dot-obs { color: #ff9800; font-size: 16px; }
.dot-sen { color: #2196f3; font-size: 16px; }

/* ---- Draft section ---- */
.draft-sequence {
    display: flex; flex-wrap: wrap; gap: 6px;
    margin-bottom: 20px;
}
.draft-cell {
    display: flex; flex-direction: column; align-items: center;
    width: 72px; border-radius: 6px; overflow: hidden;
    border: 2px solid transparent; position: relative;
}
.draft-cell img { width: 72px; height: 42px; object-fit: cover; display: block; }
.draft-cell .dc-name {
    font-size: 0.6rem; font-weight: 600; text-align: center;
    padding: 2px 3px; width: 100%; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
.draft-cell .dc-seq {
    position: absolute; top: 2px; left: 4px;
    font-size: 0.55rem; font-weight: 700; color: #fff;
    text-shadow: 0 0 3px #000;
}
.draft-cell .dc-type-badge {
    position: absolute; top: 2px; right: 4px;
    font-size: 0.48rem; font-weight: 800; letter-spacing: 0.04em;
    text-transform: uppercase; text-shadow: 0 0 3px #000;
}
.draft-cell.dc-ban-radiant .dc-type-badge { color: #4ade80; }
.draft-cell.dc-ban-dire    .dc-type-badge { color: #fb923c; }
.draft-cell.dc-pick-radiant .dc-type-badge { color: #4ade80; }
.draft-cell.dc-pick-dire    .dc-type-badge { color: #fb923c; }
.draft-cell .dc-time {
    font-size: 0.55rem; color: #484f58; font-family: monospace; padding-bottom: 3px;
}
/* Bans: greyscale + team-coloured border so you can still tell which side */
.draft-cell.dc-ban-radiant {
    background: #0e1610; border-color: #1e5c28;
    filter: grayscale(100%) brightness(0.55);
}
.draft-cell.dc-ban-radiant .dc-name { color: #4ade80; }
.draft-cell.dc-ban-dire {
    background: #160e0e; border-color: #6b2a10;
    filter: grayscale(100%) brightness(0.55);
}
.draft-cell.dc-ban-dire .dc-name { color: #fb923c; }
/* ✕ overlay shared by both ban variants */
.draft-cell.dc-ban-radiant::after,
.draft-cell.dc-ban-dire::after {
    content: "✕";
    position: absolute; top: 0; left: 0; right: 0; bottom: 22px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 900; color: rgba(255,255,255,0.55);
    pointer-events: none;
}
.draft-cell.dc-pick-radiant {
    background: #111c18; border-color: #1a3a2a;
}
.draft-cell.dc-pick-radiant .dc-name { color: #4ade80; }
.draft-cell.dc-pick-dire {
    background: #1c1117; border-color: #3a1a1a;
}
.draft-cell.dc-pick-dire .dc-name { color: #f87171; }
.draft-team-row { margin-bottom: 14px; }
.draft-team-label {
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;
    margin-bottom: 6px; text-transform: uppercase;
}
.draft-team-label.radiant { color: #4caf50; }
.draft-team-label.dire    { color: #f44336; }
.draft-picks-row { display: flex; flex-wrap: wrap; gap: 8px; }
.draft-pick-card {
    display: flex; flex-direction: column; align-items: center;
    width: 88px; border-radius: 7px; overflow: hidden;
    border: 2px solid transparent;
}
.draft-pick-card img { width: 88px; height: 52px; object-fit: cover; display: block; }
.draft-pick-card .dp-name {
    font-size: 0.65rem; font-weight: 600; text-align: center;
    padding: 3px 4px 1px; width: 100%; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
.draft-pick-card .dp-player {
    font-size: 0.6rem; color: #8b949e; text-align: center; padding-bottom: 2px;
}
.draft-pick-card .dp-time {
    font-size: 0.55rem; color: #484f58; font-family: monospace; padding-bottom: 4px;
}
.draft-pick-card.radiant { background: #111c18; border-color: #1a3a2a; }
.draft-pick-card.radiant .dp-name { color: #4ade80; }
.draft-pick-card.dire    { background: #1c1117; border-color: #3a1a1a; }
.draft-pick-card.dire    .dp-name { color: #f87171; }

/* ---- Inline damage bar ---- */
.dmg-bar-wrap { display: inline-block; width: 120px; height: 8px;
    background: #21262d; border-radius: 4px; vertical-align: middle; }
.dmg-bar-fill { height: 100%; border-radius: 4px; }

/* ---- Chart container ---- */
.chart-wrap {
    position: relative;
    height: 300px;
    padding: 8px 0;
}

/* ---- Sub-accordion (purchase per player) ---- */
.sub-accordion {
    border: 1px solid #30363d;
    border-radius: 6px;
    margin-bottom: 8px;
    overflow: hidden;
}
.sub-accordion > summary {
    padding: 8px 14px;
    font-size: 13px;
    border-bottom: 1px solid #30363d;
}
.sub-accordion > summary::before {
    content: "\\25B6";
    font-size: 9px;
    display: inline-block;
    transition: transform .15s;
    margin-right: 6px;
}
details[open].sub-accordion > summary::before {
    transform: rotate(90deg);
}

/* ---- Misc ---- */
.dim { color: #6e7681; font-style: italic; }
.radiant { color: #4caf50; }
.dire    { color: #f44336; }
.section-note { color: #8b949e; font-size: 12px; margin-top: 8px; }

/* ---- Teamfights ---- */
.tf-summary {
    margin-bottom: 10px;
    color: #8b949e;
    font-size: 12px;
}
.tf-filter-bar {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
    margin-bottom: 14px;
    padding: 10px 12px;
    border: 1px solid #30363d;
    border-radius: 6px;
    background: #11161d;
}
.tf-filter-group { min-width: 220px; }
.tf-filter-label {
    font-size: 12px;
    color: #8b949e;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    font-weight: 600;
}
.tf-filter-group input[type="range"] { width: 100%; accent-color: #58a6ff; }

.tf-fight-card {
    background: #11161d;
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-bottom: 14px;
    overflow: hidden;
}
.tf-fight-card.hidden { display: none; }
.tf-fight-header {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    padding: 10px 12px;
    border-bottom: 1px solid #30363d;
    background: #161b22;
}
.tf-fight-index {
    color: #58a6ff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .05em;
    text-transform: uppercase;
}
.tf-fight-time {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 12px;
    color: #e6edf3;
}
.tf-fight-meta {
    margin-left: auto;
    color: #8b949e;
    font-size: 12px;
}
.tf-fight-body { display: flex; gap: 0; }
.tf-fight-map {
    padding: 10px;
    border-right: 1px solid #30363d;
    flex-shrink: 0;
}
.tf-fight-right { flex: 1; min-width: 0; }

.tf-participants {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    padding: 10px 12px;
    border-bottom: 1px solid #30363d;
}
.tf-participant {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 62px;
    gap: 3px;
}
.tf-participant img {
    width: 62px;
    height: 36px;
    object-fit: cover;
    border-radius: 4px;
    border: 2px solid transparent;
}
.tf-participant.radiant img { border-color: #4caf50; }
.tf-participant.dire img { border-color: #f44336; }
.tf-participant.died img { box-shadow: 0 0 0 2px #ffffff; }
.tf-participant-hero {
    font-size: 10px;
    font-weight: 600;
    text-align: center;
    width: 62px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.tf-participant-player {
    font-size: 10px;
    color: #8b949e;
    text-align: center;
    width: 62px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.tf-table-wrap { padding: 10px 12px 12px; overflow-x: auto; }
.tf-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.tf-table th, .tf-table td { padding: 6px 8px; white-space: nowrap; }
.tf-table thead th {
    color: #8b949e;
    text-transform: uppercase;
    font-size: 10px;
    letter-spacing: .04em;
    border-bottom: 1px solid #30363d;
}
.tf-table tbody td { border-top: 1px solid #21262d; }
.tf-table .r { text-align: right; font-variant-numeric: tabular-nums; }

/* ---- Tab navigation ---- */
.tab-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 2px;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 6px 8px;
    margin-bottom: 16px;
}
.tab-bar input[type="radio"] { display: none; }
.tab-bar label {
    padding: 7px 16px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    color: #8b949e;
    cursor: pointer;
    user-select: none;
    transition: background .15s, color .15s;
    white-space: nowrap;
}
.tab-bar label:hover { color: #e6edf3; background: #21262d; }
.tab-bar input[type="radio"]:checked + label {
    background: #21262d;
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
}
.tab-page { display: none; }
.tab-page.active { display: block; }
"""

# ---------------------------------------------------------------------------
# Section builders — return HTML strings
# ---------------------------------------------------------------------------


def _build_header(match: gem.ParsedMatch) -> str:
    last_tick = match.game_end_tick or max(
        (max(p.times) for p in match.players if p.times), default=0
    )
    duration = _fmt_tick(last_tick)
    if match.radiant_win is True:
        winner_color = "#4caf50"
        winner_text = "Radiant"
    elif match.radiant_win is False:
        winner_color = "#f44336"
        winner_text = "Dire"
    else:
        winner_color = "#8b949e"
        winner_text = "Unknown"
    mode = _GAME_MODES.get(match.game_mode, f"Mode {match.game_mode}")

    parts = [
        '<div class="match-header">',
        "  <h1>Match Report</h1>",
    ]
    if match.match_id:
        parts.append(
            f'  <div class="match-stat">'
            f'    <span class="label">Match ID</span>'
            f'    <span class="value">{_e(str(match.match_id))}</span>'
            f"  </div>"
        )
    parts += [
        f'  <div class="match-stat">'
        f'    <span class="label">Duration</span>'
        f'    <span class="value">{_e(duration)}</span>'
        f"  </div>",
        f'  <div class="match-stat">'
        f'    <span class="label">Winner</span>'
        f'    <span class="value" style="color:{winner_color}">{_e(winner_text)}</span>'
        f"  </div>",
        f'  <div class="match-stat">'
        f'    <span class="label">Game Mode</span>'
        f'    <span class="value">{_e(mode)}</span>'
        f"  </div>",
        "</div>",
    ]
    return "\n".join(parts)


def _build_scoreboard(match: gem.ParsedMatch) -> str:
    _load_hero_icons([p.hero_name for p in match.players if p.hero_name])

    parts = ['<div class="card">']
    parts.append("<details open>")
    parts.append("<summary>Scoreboard</summary>")
    parts.append('<div class="card-body">')

    for team in (2, 3):
        color = TEAM_COLOR_CSS[team]
        team_players = [p for p in match.players if p.team == team and p.hero_name]
        if not team_players:
            continue

        total_team_kills = sum(pp.kills for pp in team_players)
        parts.append(
            f'<h3 style="color:{color};margin-bottom:8px;margin-top:12px">{_e(_team_name(team))}</h3>'
        )
        parts.append("<table>")
        parts.append(
            "<thead><tr>"
            "<th>Hero</th>"
            '<th class="r">K</th><th class="r">D</th><th class="r">A</th>'
            '<th class="r">KP%</th>'
            '<th class="r">LH</th><th class="r">DN</th>'
            '<th class="r">Net Worth</th>'
            '<th class="r">Damage</th>'
            '<th class="r">Healing</th>'
            '<th class="r">Obs</th>'
            '<th class="r">Sen</th>'
            '<th class="r">Dust</th><th class="r">TP</th><th class="r">Smoke</th>'
            '<th class="r">Stuns(s)</th>'
            "</tr></thead>"
        )
        parts.append("<tbody>")
        row_cls = "row-radiant" if team == 2 else "row-dire"
        for pp in team_players:
            final_nw = pp.net_worth_t[-1] if pp.net_worth_t else 0
            final_lh = pp.lh_t[-1] if pp.lh_t else 0
            final_dn = pp.dn_t[-1] if pp.dn_t else 0
            total_dmg = sum(pp.damage.values())
            total_heal = sum(pp.healing.values())
            stuns = f"{pp.stuns_dealt:.1f}"
            kp = (pp.kills + pp.assists) / total_team_kills * 100 if total_team_kills > 0 else 0
            dust_count = sum(1 for e in pp.purchase_log if e.value_name == "item_dust")
            tp_count = sum(1 for e in pp.purchase_log if e.value_name == "item_tpscroll")
            smoke_count = sum(1 for e in pp.purchase_log if e.value_name == "item_smoke_of_deceit")
            parts.append(
                f'<tr class="{row_cls}">'
                f'<td style="white-space:nowrap">{_hero_cell(pp.hero_name, team)}</td>'
                f'<td class="r">{pp.kills}</td>'
                f'<td class="r">{pp.deaths}</td>'
                f'<td class="r">{pp.assists}</td>'
                f'<td class="r">{kp:.0f}%</td>'
                f'<td class="r">{final_lh:,}</td>'
                f'<td class="r">{final_dn:,}</td>'
                f'<td class="r">{final_nw:,}</td>'
                f'<td class="r">{total_dmg:,}</td>'
                f'<td class="r">{total_heal:,}</td>'
                f'<td class="r">{len(pp.obs_log)}</td>'
                f'<td class="r">{len(pp.sen_log)}</td>'
                f'<td class="r">{dust_count}</td>'
                f'<td class="r">{tp_count}</td>'
                f'<td class="r">{smoke_count}</td>'
                f'<td class="r">{stuns}</td>'
                f"</tr>"
            )
        parts.append("</tbody></table>")

    parts.append("</div>")
    parts.append("</details>")
    parts.append("</div>")
    return "\n".join(parts)


# 5 distinct shades per team — Radiant (greens), Dire (reds/oranges)
_RADIANT_COLORS = ["#4caf50", "#81c784", "#a5d6a7", "#2e7d32", "#66bb6a"]
_DIRE_COLORS = ["#f44336", "#ff7043", "#ef9a9a", "#b71c1c", "#ff8a65"]


def _build_hero_timeseries_chart(match: gem.ParsedMatch) -> str:
    """Two side-by-side line charts: Net Worth and XP per hero over time."""
    players = [p for p in match.players if p.hero_name]
    if not any(p.net_worth_t_min or p.xp_t_min for p in players):
        return ""

    # Build minute labels from the longest times_min series
    times_min: list[int] = []
    for p in players:
        if len(p.times_min) > len(times_min):
            times_min = p.times_min

    n = max((len(p.net_worth_t_min) for p in players), default=0)
    n = max(n, max((len(p.xp_t_min) for p in players), default=0))
    labels = []
    for i in range(n):
        if i < len(times_min):
            secs = times_min[i] // TICKS_PER_SEC
            labels.append(f"{secs // 60}")
        else:
            labels.append(str(i))

    # Build dataset list for each chart
    radiant_idx = dire_idx = 0
    nw_datasets: list[dict] = []
    xp_datasets: list[dict] = []
    for p in players:
        if p.team == 2:
            color = _RADIANT_COLORS[radiant_idx % len(_RADIANT_COLORS)]
            radiant_idx += 1
        else:
            color = _DIRE_COLORS[dire_idx % len(_DIRE_COLORS)]
            dire_idx += 1
        label = _hero(p.hero_name)
        nw_datasets.append(
            {
                "label": label,
                "data": list(p.net_worth_t_min),
                "borderColor": color,
                "backgroundColor": "transparent",
                "borderWidth": 2,
                "pointRadius": 0,
                "tension": 0.3,
                "fill": False,
            }
        )
        xp_datasets.append(
            {
                "label": label,
                "data": list(p.xp_t_min),
                "borderColor": color,
                "backgroundColor": "transparent",
                "borderWidth": 2,
                "pointRadius": 0,
                "tension": 0.3,
                "fill": False,
            }
        )

    labels_js = json.dumps(labels)
    nw_ds_js = json.dumps(nw_datasets)
    xp_ds_js = json.dumps(xp_datasets)

    return f"""
<div class="card">
<details open>
<summary>Hero Net Worth &amp; XP</summary>
<div class="card-body">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Net Worth per Hero</div>
    <div class="chart-wrap"><canvas id="heroNwChart"></canvas></div>
  </div>
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">XP per Hero</div>
    <div class="chart-wrap"><canvas id="heroXpChart"></canvas></div>
  </div>
</div>
<script>
(function() {{
  var labels = {labels_js};
  function makeOpts(yTitle) {{
    return {{
      responsive: true,
      maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ labels: {{ color: '#e6edf3', boxWidth: 12, font: {{ size: 11 }} }} }},
        tooltip: {{
          callbacks: {{
            label: function(c) {{
              return c.dataset.label + ': ' + Math.round(c.parsed.y).toLocaleString();
            }}
          }}
        }},
      }},
      scales: {{
        x: {{
          title: {{ display: true, text: 'Game Minute', color: '#8b949e' }},
          ticks: {{ color: '#8b949e' }},
          grid: {{ color: '#21262d' }},
        }},
        y: {{
          title: {{ display: true, text: yTitle, color: '#8b949e' }},
          ticks: {{
            color: '#8b949e',
            callback: function(v) {{ return (v/1000).toFixed(0) + 'k'; }},
          }},
          grid: {{ color: '#21262d' }},
          border: {{ color: '#30363d' }},
        }},
      }},
    }};
  }}
  new Chart(document.getElementById('heroNwChart').getContext('2d'), {{
    type: 'line',
    data: {{ labels: labels, datasets: {nw_ds_js} }},
    options: makeOpts('Net Worth'),
  }});
  new Chart(document.getElementById('heroXpChart').getContext('2d'), {{
    type: 'line',
    data: {{ labels: labels, datasets: {xp_ds_js} }},
    options: makeOpts('XP'),
  }});
}})();
</script>
</div>
</details>
</div>"""


def _build_gold_xp_chart(match: gem.ParsedMatch) -> str:
    adv_gold = match.radiant_gold_adv
    adv_xp = match.radiant_xp_adv

    # Sum per-player total-earned values by team to get raw Radiant / Dire series
    radiant_gold_raw: list[int] = []
    dire_gold_raw: list[int] = []
    radiant_xp_raw: list[int] = []
    dire_xp_raw: list[int] = []

    for p in match.players:
        if p.team == 2:  # Radiant
            g = p.total_earned_gold_t_min
            x = p.total_earned_xp_t_min
            if not radiant_gold_raw:
                radiant_gold_raw = list(g)
                radiant_xp_raw = list(x)
            else:
                for i, v in enumerate(g):
                    if i < len(radiant_gold_raw):
                        radiant_gold_raw[i] += v
                    else:
                        radiant_gold_raw.append(v)
                for i, v in enumerate(x):
                    if i < len(radiant_xp_raw):
                        radiant_xp_raw[i] += v
                    else:
                        radiant_xp_raw.append(v)
        elif p.team == 3:  # Dire
            g = p.total_earned_gold_t_min
            x = p.total_earned_xp_t_min
            if not dire_gold_raw:
                dire_gold_raw = list(g)
                dire_xp_raw = list(x)
            else:
                for i, v in enumerate(g):
                    if i < len(dire_gold_raw):
                        dire_gold_raw[i] += v
                    else:
                        dire_gold_raw.append(v)
                for i, v in enumerate(x):
                    if i < len(dire_xp_raw):
                        dire_xp_raw[i] += v
                    else:
                        dire_xp_raw.append(v)

    # Build labels from the longest available series
    times_min: list[int] = []
    for p in match.players:
        if p.times_min:
            times_min = p.times_min
            break

    n = max(len(adv_gold), len(adv_xp), len(radiant_gold_raw), len(dire_gold_raw), 0)
    labels: list[str] = []
    for i in range(n):
        if i < len(times_min):
            secs = times_min[i] // TICKS_PER_SEC
            labels.append(f"{secs // 60}")
        else:
            labels.append(str(i))

    # Pad all series to the same length
    def _pad(lst: list[int], length: int) -> list[int]:
        return lst + [lst[-1] if lst else 0] * (length - len(lst))

    radiant_gold_raw = _pad(radiant_gold_raw, n)
    dire_gold_raw = _pad(dire_gold_raw, n)
    radiant_xp_raw = _pad(radiant_xp_raw, n)
    dire_xp_raw = _pad(dire_xp_raw, n)
    adv_gold_padded = _pad(list(adv_gold), n)
    adv_xp_padded = _pad(list(adv_xp), n)

    labels_js = json.dumps(labels)
    rad_gold_js = json.dumps(radiant_gold_raw)
    dire_gold_js = json.dumps(dire_gold_raw)
    rad_xp_js = json.dumps(radiant_xp_raw)
    dire_xp_js = json.dumps(dire_xp_raw)
    adv_gold_js = json.dumps(adv_gold_padded)
    adv_xp_js = json.dumps(adv_xp_padded)

    no_data_msg = ""
    has_raw = bool(radiant_gold_raw and dire_gold_raw)
    if not adv_gold and not adv_xp and not has_raw:
        no_data_msg = '<p class="dim">(no advantage data available)</p>'

    # Shared chart options factory (injected as JS)
    chart_html = f"""
<div class="card">
<details open>
<summary>Gold &amp; XP</summary>
<div class="card-body">
{no_data_msg}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Total Gold Earned</div>
    <div class="chart-wrap"><canvas id="goldRawChart"></canvas></div>
  </div>
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Total XP Earned</div>
    <div class="chart-wrap"><canvas id="xpRawChart"></canvas></div>
  </div>
</div>
<div style="margin-top:16px">
  <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Net Advantage (Radiant − Dire)</div>
  <div class="chart-wrap"><canvas id="advChart"></canvas></div>
</div>
<script>
(function() {{
  var labels = {labels_js};

  function sharedScales(yTitle) {{
    return {{
      x: {{
        title: {{ display: true, text: 'Game Minute', color: '#8b949e' }},
        ticks: {{ color: '#8b949e' }},
        grid: {{ color: '#21262d' }},
      }},
      y: {{
        title: {{ display: true, text: yTitle, color: '#8b949e' }},
        ticks: {{
          color: '#8b949e',
          callback: function(v) {{ return (v/1000).toFixed(0) + 'k'; }},
        }},
        grid: {{ color: '#21262d' }},
        border: {{ color: '#30363d' }},
      }},
    }};
  }}

  function sharedOpts(yTitle) {{
    return {{
      responsive: true,
      maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ labels: {{ color: '#e6edf3', boxWidth: 14 }} }},
        tooltip: {{
          callbacks: {{
            label: function(c) {{
              return c.dataset.label + ': ' + Math.round(c.parsed.y).toLocaleString();
            }}
          }}
        }},
      }},
      scales: sharedScales(yTitle),
    }};
  }}

  // ---- Raw Gold chart ----
  new Chart(document.getElementById('goldRawChart').getContext('2d'), {{
    type: 'line',
    data: {{
      labels: labels,
      datasets: [
        {{
          label: 'Radiant',
          data: {rad_gold_js},
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76,175,80,0.06)',
          borderWidth: 2, pointRadius: 0, tension: 0.3, fill: false,
        }},
        {{
          label: 'Dire',
          data: {dire_gold_js},
          borderColor: '#f44336',
          backgroundColor: 'rgba(244,67,54,0.06)',
          borderWidth: 2, pointRadius: 0, tension: 0.3, fill: false,
        }},
      ],
    }},
    options: sharedOpts('Gold'),
  }});

  // ---- Raw XP chart ----
  new Chart(document.getElementById('xpRawChart').getContext('2d'), {{
    type: 'line',
    data: {{
      labels: labels,
      datasets: [
        {{
          label: 'Radiant',
          data: {rad_xp_js},
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76,175,80,0.06)',
          borderWidth: 2, pointRadius: 0, tension: 0.3, fill: false,
        }},
        {{
          label: 'Dire',
          data: {dire_xp_js},
          borderColor: '#f44336',
          backgroundColor: 'rgba(244,67,54,0.06)',
          borderWidth: 2, pointRadius: 0, tension: 0.3, fill: false,
        }},
      ],
    }},
    options: sharedOpts('XP'),
  }});

  // ---- Net advantage chart ----
  // Split each series into positive (Radiant-ahead) and negative (Dire-ahead) segments
  // by using two filled datasets against a zero baseline
  var advGold = {adv_gold_js};
  var advXp   = {adv_xp_js};
  var goldPos = advGold.map(function(v) {{ return v > 0 ? v : 0; }});
  var goldNeg = advGold.map(function(v) {{ return v < 0 ? v : 0; }});
  var xpPos   = advXp.map(function(v)   {{ return v > 0 ? v : 0; }});
  var xpNeg   = advXp.map(function(v)   {{ return v < 0 ? v : 0; }});

  var advOpts = sharedOpts('Gold / XP');
  advOpts.scales.y.ticks.callback = function(v) {{
    return (v >= 0 ? '+' : '') + (v/1000).toFixed(1) + 'k';
  }};
  advOpts.scales.y.afterDataLimits = function(axis) {{
    axis.min = Math.min(axis.min, 0);
    axis.max = Math.max(axis.max, 0);
  }};
  advOpts.plugins.tooltip.callbacks.label = function(c) {{
    var v = c.parsed.y;
    return c.dataset.label + ': ' + (v >= 0 ? '+' : '') + Math.round(v).toLocaleString();
  }};

  new Chart(document.getElementById('advChart').getContext('2d'), {{
    type: 'line',
    data: {{
      labels: labels,
      datasets: [
        {{
          label: 'Gold adv (Radiant)',
          data: advGold,
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76,175,80,0.0)',
          borderWidth: 2, pointRadius: 0, tension: 0.3, fill: false,
        }},
        {{
          label: 'XP adv (Radiant)',
          data: advXp,
          borderColor: '#2196f3',
          backgroundColor: 'rgba(33,150,243,0.0)',
          borderWidth: 2, borderDash: [5,3], pointRadius: 0, tension: 0.3, fill: false,
        }},
        {{
          label: 'Gold lead',
          data: goldPos,
          borderColor: 'transparent',
          backgroundColor: 'rgba(76,175,80,0.20)',
          borderWidth: 0, pointRadius: 0, tension: 0.3, fill: 'origin',
        }},
        {{
          label: 'Dire gold lead',
          data: goldNeg,
          borderColor: 'transparent',
          backgroundColor: 'rgba(244,67,54,0.20)',
          borderWidth: 0, pointRadius: 0, tension: 0.3, fill: 'origin',
        }},
      ],
    }},
    options: advOpts,
  }});
}})();
</script>
</div>
</details>
</div>"""
    return chart_html


def _build_objectives(match: gem.ParsedMatch) -> str:
    events: list[tuple[int, str, str, str]] = []

    for t in match.towers:
        team_color = TEAM_COLOR_CSS.get(t.team, "#888")
        name = t.tower_name.replace("npc_dota_", "").replace("_", " ")
        killer = _hero(t.killer) if t.killer.startswith("npc_dota_hero_") else t.killer
        desc = f"{_team_badge(t.team)} {_e(name)} — killed by {_e(killer)}"
        events.append((t.tick, "Tower", team_color, desc))

    for b in match.barracks:
        team_color = TEAM_COLOR_CSS.get(b.team, "#888")
        name = b.barracks_name.replace("npc_dota_", "").replace("_", " ")
        killer = _hero(b.killer) if b.killer.startswith("npc_dota_hero_") else b.killer
        desc = f"{_team_badge(b.team)} {_e(name)} — killed by {_e(killer)}"
        events.append((b.tick, "Barracks", team_color, desc))

    for n, r in enumerate(match.roshans, 1):
        killer = _hero(r.killer) if r.killer else "?"
        respawn_min = _fmt_tick(r.tick + 8 * TICKS_PER_MIN)
        respawn_max = _fmt_tick(r.tick + 11 * TICKS_PER_MIN)
        desc = f'<span style="color:#ffb74d">Roshan #{n}</span> killed by {_e(killer)} — respawns {_e(respawn_min)}–{_e(respawn_max)}'
        events.append((r.tick, f"Roshan #{n}", "#ffb74d", desc))

    events.sort(key=lambda e: e[0])

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Objectives Timeline</summary>",
        '<div class="card-body">',
    ]

    if not events:
        parts.append('<p class="dim">(no objective events recorded)</p>')
    else:
        parts.append("<table>")
        parts.append("<thead><tr><th>Time</th><th>Type</th><th>Detail</th></tr></thead>")
        parts.append("<tbody>")
        for tick, etype, color, desc in events:
            parts.append(
                f"<tr>"
                f"<td>{_e(_fmt_tick(tick))}</td>"
                f'<td><span style="color:{color};font-weight:bold">{_e(etype)}</span></td>'
                f"<td>{desc}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _build_wards(match: gem.ParsedMatch, map_b64: str | None) -> str:
    # Coordinate system from movement_heatmap.py — calibrated against Game_map_7.40.jpg
    _XMIN, _XMAX = 7563, 25900
    _YMIN, _YMAX = 7800, 25600

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Ward Map</summary>",
        '<div class="card-body">',
    ]

    if not match.wards:
        parts.append('<p class="dim">(no ward placement data)</p>')
        parts += ["</div>", "</details>", "</div>"]
        return "\n".join(parts)

    # Determine tick range for the slider (use game_end_tick if available)
    max_tick = max(
        (w.killed_tick or w.expires_tick or w.tick for w in match.wards),
        default=0,
    )
    slider_max = max(max_tick, match.game_end_tick or max_tick)
    # Slider lower bound = game clock -1:30 (-90s before creep spawn).
    # Per Liquipedia: heroes enter the map at the following game-clock values:
    #   -90s  normal / ranked / Captain's Mode / New Player Mode
    #   -75s  Play vs Bots
    #   -60s  Turbo
    #    0s   Demo Hero
    # We use -90s universally as the safe lower bound (harmless for turbo — the
    # first 30s of the slider will just be an empty map).
    # Reference: https://liquipedia.net/dota2/Clock
    _PREGAME_TICKS = 90 * TICKS_PER_SEC  # 2700 ticks
    slider_min = (match.game_start_tick or 0) - _PREGAME_TICKS

    # Serialise wards as JSON for the canvas JS
    ward_data = []
    for w in match.wards:
        if w.x is None or w.y is None:
            continue
        # Convert world coords to [0,1] fractions (y-axis flipped: world y+ = up, canvas y+ = down)
        fx = (w.x - _XMIN) / (_XMAX - _XMIN)
        fy = 1.0 - (w.y - _YMIN) / (_YMAX - _YMIN)
        fate = "active"
        fate_time = ""
        if w.killed_tick is not None:
            fate = "killed"
            fate_time = _fmt_tick(w.killed_tick)
        elif w.expires_tick is not None:
            fate = "expired"
            fate_time = _fmt_tick(w.expires_tick)
        ward_data.append(
            {
                "fx": round(fx, 5),
                "fy": round(fy, 5),
                "type": w.ward_type,  # "observer" | "sentry"
                "team": w.team,  # 2 | 3
                "placed": w.tick,
                "removed": w.killed_tick or w.expires_tick,  # None = still active
                "placer": _hero(w.placer),
                "fate": fate,
                "fate_time": fate_time,
                "placed_fmt": _fmt_tick(w.tick),
            }
        )

    wards_js = json.dumps(ward_data)

    # Serialise smoke events — show for _SMOKE_SHOW_TICKS after activation
    _SMOKE_SHOW_TICKS = 300  # ~10 seconds game time
    smoke_data = []
    for s in match.smoke_events:
        if s.x is None or s.y is None:
            continue
        fx = (s.x - _XMIN) / (_XMAX - _XMIN)
        fy = 1.0 - (s.y - _YMIN) / (_YMAX - _YMIN)
        smoke_data.append(
            {
                "fx": round(fx, 5),
                "fy": round(fy, 5),
                "tick": s.tick,
                "end_tick": s.tick + _SMOKE_SHOW_TICKS,
                "team": s.team,
                "activator": _hero(s.activator),
                "count": len(s.smoked),
                "tick_fmt": _fmt_tick(s.tick),
            }
        )
    smokes_js = json.dumps(smoke_data)

    img_src = f"data:image/jpeg;base64,{map_b64}" if map_b64 else ""

    # Canvas + slider HTML
    canvas_html = f"""
<div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;margin-bottom:16px">
  <div style="flex:0 0 auto">
    <canvas id="wardCanvas" width="700" height="700"
      style="border:1px solid #30363d;border-radius:6px;cursor:crosshair;display:block"></canvas>
    <div style="margin-top:8px;display:flex;align-items:center;gap:8px">
      <button id="wardPlayBtn"
        style="background:#21262d;border:1px solid #30363d;border-radius:4px;
               color:#e6edf3;cursor:pointer;font-size:14px;padding:2px 10px;
               line-height:1.6;flex:0 0 auto"
        title="Play / Pause">&#9654;</button>
      <select id="wardSpeed"
        style="background:#21262d;border:1px solid #30363d;border-radius:4px;
               color:#8b949e;font-size:12px;padding:2px 4px;flex:0 0 auto">
        <option value="1">1×</option>
        <option value="2">2×</option>
        <option value="5" selected>5×</option>
        <option value="10">10×</option>
        <option value="30">30×</option>
      </select>
      <input id="wardSlider" type="range" min="{slider_min}" max="{slider_max}" value="{slider_min}"
        style="flex:1;accent-color:#58a6ff">
      <span id="wardTime" style="color:#e6edf3;font-size:13px;min-width:55px;text-align:right">-01:30</span>
    </div>
    <div style="margin-top:6px;display:flex;gap:14px;font-size:12px;color:#8b949e;align-items:center">
      <span>{_item_icon_tag("ward_observer", 16)} Observer <span style="color:#8b949e">(vision 1600)</span></span>
      <span>{_item_icon_tag("ward_sentry", 16)} Sentry <span style="color:#8b949e">(truesight 1050)</span></span>
      <span>{_item_icon_tag("smoke_of_deceit", 16)} Smoke</span>
    </div>
    <div id="wardTooltip" style="margin-top:8px;min-height:40px;font-size:12px;color:#8b949e"></div>
  </div>
  <div style="flex:1;min-width:200px">
    <p style="color:#8b949e;font-size:12px;margin-bottom:8px">
      Press &#9654; to play or drag the slider to scrub.<br>
      Wards shown are active at the selected time.<br>
      Hover over a dot to see details.
    </p>
    <p style="color:#8b949e;font-size:12px">
      Total wards: <strong style="color:#e6edf3">{len(ward_data)}</strong>
      ({sum(1 for w in ward_data if w["type"] == "observer")} obs /
       {sum(1 for w in ward_data if w["type"] == "sentry")} sen)
    </p>
  </div>
</div>
<script>
(function() {{
  var wards = {wards_js};
  var smokes = {smokes_js};
  var imgSrc = {json.dumps(img_src)};
  var iconObsSrc = {json.dumps(_ITEM_ICON_B64.get("ward_observer", ""))};
  var iconSenSrc = {json.dumps(_ITEM_ICON_B64.get("ward_sentry", ""))};
  var iconSmokeSrc = {json.dumps(_ITEM_ICON_B64.get("smoke_of_deceit", ""))};
  var gameStartTick = {match.game_start_tick or 0};
  var sliderMin = {slider_min};
  var sliderMax = {slider_max};
  // Vision radii in world units (Dota 2 wiki / Liquipedia):
  //   Observer Ward: 1600 (uniform day/night vision)
  //   Sentry Ward:   1050 (true sight / detection radius)
  // Converted to canvas pixels at runtime using: radius_px = radius_world * (W / worldWidth)
  var WORLD_WIDTH = {_XMAX - _XMIN};   // world units across the full map canvas
  var OBS_VISION_RADIUS   = 1600;
  var SEN_TRUESIGHT_RADIUS = 1050;
  var canvas = document.getElementById('wardCanvas');
  var ctx = canvas.getContext('2d');
  var slider = document.getElementById('wardSlider');
  var timeLabel = document.getElementById('wardTime');
  var tooltip = document.getElementById('wardTooltip');
  var playBtn = document.getElementById('wardPlayBtn');
  var speedSel = document.getElementById('wardSpeed');
  var W = canvas.width, H = canvas.height;
  var currentTick = sliderMin;
  var playing = false;
  var lastTs = null;

  // Load map image and item icons
  var mapImg = new Image();
  mapImg.onload = function() {{ draw(currentTick); }};
  if (imgSrc) {{ mapImg.src = imgSrc; }}

  function _makeIcon(src) {{
    var img = new Image();
    if (src) img.src = src;
    return img;
  }}
  var iconObs   = _makeIcon(iconObsSrc);
  var iconSen   = _makeIcon(iconSenSrc);
  var iconSmoke = _makeIcon(iconSmokeSrc);

  function fmtTick(tick) {{
    var rel = tick - gameStartTick;
    var neg = rel < 0;
    var secs = Math.floor(Math.abs(rel) / 30);
    var m = Math.floor(secs / 60), s = secs % 60;
    var t = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    return neg ? '-' + t : t;
  }}

  function draw(tick) {{
    ctx.clearRect(0, 0, W, H);

    // Map background
    if (mapImg.complete && mapImg.naturalWidth > 0) {{
      ctx.drawImage(mapImg, 0, 0, W, H);
    }} else {{
      ctx.fillStyle = '#1a2a1a';
      ctx.fillRect(0, 0, W, H);
    }}

    // Helper: draw icon (or coloured circle fallback) centred at (cx,cy)
    function drawIcon(img, cx, cy, size, borderColor, alpha) {{
      var half = size / 2;
      ctx.save();
      ctx.globalAlpha = alpha !== undefined ? alpha : 1.0;
      if (img && img.complete && img.naturalWidth > 0) {{
        // Rounded clip
        ctx.beginPath();
        ctx.roundRect(cx - half, cy - half, size, size, 3);
        ctx.clip();
        ctx.drawImage(img, cx - half, cy - half, size, size);
        ctx.restore();
        // Border on top
        ctx.save();
        ctx.globalAlpha = alpha !== undefined ? alpha : 1.0;
        ctx.beginPath();
        ctx.roundRect(cx - half, cy - half, size, size, 3);
        ctx.lineWidth = 2;
        ctx.strokeStyle = borderColor;
        ctx.stroke();
      }} else {{
        // Fallback circle
        ctx.beginPath();
        ctx.arc(cx, cy, half, 0, 2 * Math.PI);
        ctx.fillStyle = borderColor;
        ctx.fill();
      }}
      ctx.restore();
    }}

    // Draw active wards at this tick
    for (var i = 0; i < wards.length; i++) {{
      var w = wards[i];
      if (tick < w.placed) continue;
      if (w.removed !== null && tick > w.removed) continue;

      var cx = w.fx * W;
      var cy = w.fy * H;
      var isObs = w.type === 'observer';
      var icon = isObs ? iconObs : iconSen;
      var borderColor = isObs ? '#ff9800' : '#2196f3';

      // Draw vision radius circle behind the icon
      var visionRadius = (isObs ? OBS_VISION_RADIUS : SEN_TRUESIGHT_RADIUS) * W / WORLD_WIDTH;
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, visionRadius, 0, 2 * Math.PI);
      ctx.fillStyle = isObs ? 'rgba(255,152,0,0.07)' : 'rgba(33,150,243,0.10)';
      ctx.fill();
      ctx.strokeStyle = isObs ? 'rgba(255,152,0,0.35)' : 'rgba(33,150,243,0.40)';
      ctx.lineWidth = 1;
      ctx.setLineDash([3, 3]);
      ctx.stroke();
      ctx.restore();

      drawIcon(icon, cx, cy, isObs ? 18 : 16, borderColor);
    }}

    // Draw active smokes at this tick
    for (var i = 0; i < smokes.length; i++) {{
      var s = smokes[i];
      if (tick < s.tick || tick > s.end_tick) continue;

      var cx = s.fx * W;
      var cy = s.fy * H;
      var borderColor = s.team === 2 ? '#4caf50' : '#f44336';
      var age = (tick - s.tick) / (s.end_tick - s.tick);
      var alpha = 1.0 - age * 0.6;
      drawIcon(iconSmoke, cx, cy, 20, borderColor, alpha);

      // Hero count badge
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.fillStyle = 'rgba(0,0,0,0.75)';
      ctx.beginPath();
      ctx.arc(cx + 8, cy - 8, 7, 0, 2 * Math.PI);
      ctx.fill();
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 9px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(s.count, cx + 8, cy - 8);
      ctx.restore();
    }}
  }}

  function setTick(tick) {{
    currentTick = Math.max(sliderMin, Math.min(sliderMax, tick));
    slider.value = currentTick;
    timeLabel.textContent = fmtTick(currentTick);
    draw(currentTick);
  }}

  function animFrame(ts) {{
    if (!playing) return;
    if (lastTs !== null) {{
      var speed = parseInt(speedSel.value) || 5;
      // advance at `speed` ticks per real millisecond (30 ticks/sec game = 1x)
      var delta = (ts - lastTs) * speed * 30 / 1000;
      currentTick = Math.min(sliderMax, currentTick + delta);
      slider.value = currentTick;
      timeLabel.textContent = fmtTick(Math.floor(currentTick));
      draw(Math.floor(currentTick));
      if (currentTick >= sliderMax) {{
        playing = false;
        playBtn.textContent = '\u25b6';
        lastTs = null;
        return;
      }}
    }}
    lastTs = ts;
    requestAnimationFrame(animFrame);
  }}

  playBtn.addEventListener('click', function() {{
    if (playing) {{
      playing = false;
      lastTs = null;
      playBtn.textContent = '\u25b6';
    }} else {{
      if (currentTick >= sliderMax) setTick(sliderMin);
      playing = true;
      playBtn.textContent = '\u23f8';
      lastTs = null;
      requestAnimationFrame(animFrame);
    }}
  }});

  slider.addEventListener('input', function() {{
    playing = false;
    lastTs = null;
    playBtn.textContent = '\u25b6';
    currentTick = parseInt(this.value);
    timeLabel.textContent = fmtTick(currentTick);
    draw(currentTick);
    tooltip.innerHTML = '';
  }});

  // Hover tooltip — checks wards first, then smokes
  canvas.addEventListener('mousemove', function(e) {{
    var rect = canvas.getBoundingClientRect();
    var mx = (e.clientX - rect.left) * (W / rect.width);
    var my = (e.clientY - rect.top) * (H / rect.height);
    var hit = null, hitType = null, bestDist = 12;

    for (var i = 0; i < wards.length; i++) {{
      var w = wards[i];
      if (currentTick < w.placed) continue;
      if (w.removed !== null && currentTick > w.removed) continue;
      var dx = w.fx * W - mx, dy = w.fy * H - my;
      var dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < bestDist) {{ bestDist = dist; hit = w; hitType = 'ward'; }}
    }}
    for (var i = 0; i < smokes.length; i++) {{
      var s = smokes[i];
      if (currentTick < s.tick || currentTick > s.end_tick) continue;
      var dx = s.fx * W - mx, dy = s.fy * H - my;
      var dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < bestDist) {{ bestDist = dist; hit = s; hitType = 'smoke'; }}
    }}

    if (hit && hitType === 'ward') {{
      var teamName = hit.team === 2 ? 'Radiant' : 'Dire';
      var teamColor = hit.team === 2 ? '#4caf50' : '#f44336';
      var fateStr = hit.fate === 'killed' ? '&#128308; Killed ' + hit.fate_time
                  : hit.fate === 'expired' ? '&#9898; Expired ' + hit.fate_time
                  : '&#128994; Still active';
      tooltip.innerHTML =
        '<strong style="color:#e6edf3">' + hit.type.charAt(0).toUpperCase() + hit.type.slice(1) + '</strong> &mdash; ' +
        '<span style="color:' + teamColor + '">' + teamName + '</span><br>' +
        'Placed: ' + hit.placed_fmt + ' by ' + hit.placer + '<br>' +
        fateStr;
      canvas.style.cursor = 'pointer';
    }} else if (hit && hitType === 'smoke') {{
      var teamName = hit.team === 2 ? 'Radiant' : 'Dire';
      var teamColor = hit.team === 2 ? '#4caf50' : '#f44336';
      tooltip.innerHTML =
        '<strong style="color:#9c27b0">Smoke of Deceit</strong> &mdash; ' +
        '<span style="color:' + teamColor + '">' + teamName + '</span><br>' +
        'Activated: ' + hit.tick_fmt + ' by ' + hit.activator + '<br>' +
        hit.count + ' hero' + (hit.count !== 1 ? 'es' : '') + ' smoked';
      canvas.style.cursor = 'pointer';
    }} else {{
      tooltip.innerHTML = '';
      canvas.style.cursor = 'crosshair';
    }}
  }});
}})();
</script>"""

    parts.append(canvas_html)

    # Keep the full table below for reference
    parts.append(
        '<details style="margin-top:8px"><summary style="color:#8b949e;font-size:12px;cursor:pointer">Show full ward table</summary>'
    )
    parts.append('<table style="margin-top:8px">')
    parts.append(
        "<thead><tr>"
        "<th>Time</th><th>Type</th><th>Hero</th><th>Team</th>"
        "<th>Coords</th><th>Fate</th>"
        "</tr></thead>"
    )
    parts.append("<tbody>")
    for w in sorted(match.wards, key=lambda x: x.tick):
        type_dot = (
            '<span class="dot-obs">&#9679;</span>'
            if w.ward_type == "observer"
            else '<span class="dot-sen">&#9679;</span>'
        )
        type_label = f"{type_dot} {_e(w.ward_type.capitalize())}"
        coords = f"({w.x:.0f}, {w.y:.0f})" if w.x is not None else "—"
        if w.killed_tick is not None:
            killer = _hero(w.killer) if w.killer else "?"
            fate = f'<span style="color:#f44336">Killed {_e(_fmt_tick(w.killed_tick))} by {_e(killer)}</span>'
        elif w.expires_tick is not None:
            fate = f'<span style="color:#8b949e">Expired {_e(_fmt_tick(w.expires_tick))}</span>'
        else:
            fate = '<span style="color:#ffb74d">Active / unknown</span>'
        team_color = TEAM_COLOR_CSS.get(w.team, "#888")
        parts.append(
            f"<tr>"
            f"<td>{_e(_fmt_tick(w.tick))}</td>"
            f"<td>{type_label}</td>"
            f"<td>{_e(_hero(w.placer))}</td>"
            f'<td><span style="color:{team_color}">{_e(_team_name(w.team))}</span></td>'
            f'<td style="font-variant-numeric:tabular-nums">{_e(coords)}</td>'
            f"<td>{fate}</td>"
            f"</tr>"
        )
    parts.append("</tbody></table></details>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _build_damage(match: gem.ParsedMatch) -> str:
    all_dmg = [(p, sum(p.damage.values())) for p in match.players if p.hero_name]
    max_dmg = max((d for _, d in all_dmg), default=1) or 1
    _load_hero_icons([p.hero_name for p in match.players if p.hero_name])

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Damage Breakdown</summary>",
        '<div class="card-body">',
    ]
    parts.append("<table>")
    parts.append(
        "<thead><tr>"
        "<th>Hero</th><th>Team</th>"
        '<th class="r">Hero Dmg</th>'
        "<th>Top Ability</th>"
        "<th>Abilities (top 3)</th>"
        '<th class="r">Dmg Taken</th>'
        '<th class="r">Healing</th>'
        '<th class="r">Stuns(s)</th>'
        "<th>Bar</th>"
        "</tr></thead>"
    )
    parts.append("<tbody>")

    # Sort by damage descending
    for pp, total_dmg in sorted(all_dmg, key=lambda x: -x[1]):
        total_heal = sum(pp.healing.values())
        top_ability = ""
        if pp.ability_uses:
            top_ab = max(pp.ability_uses, key=pp.ability_uses.get)  # type: ignore[arg-type]
            top_ability = f"{_e(ability_display(top_ab))} ({pp.ability_uses[top_ab]}x)"

        # Top-3 abilities column — filter passives/specials, sort by cast count descending
        top3_parts: list[str] = []
        if pp.ability_uses:
            filtered = [
                (k, v)
                for k, v in pp.ability_uses.items()
                if "_passive" not in k and not k.startswith("special_")
            ]
            filtered.sort(key=lambda x: -x[1])
            for ab_key, ab_count in filtered[:3]:
                top3_parts.append(f"{_e(ability_display(ab_key))} ({ab_count}x)")
        top3_str = ", ".join(top3_parts)

        # Damage taken column
        total_dmg_taken = sum(pp.damage_taken.values()) if pp.damage_taken else 0
        top_attacker = ""
        if pp.damage_taken:
            top_att_key = max(pp.damage_taken, key=pp.damage_taken.get)  # type: ignore[arg-type]
            top_attacker = f"Most from: {_hero(top_att_key)} ({pp.damage_taken[top_att_key]:,})"

        bar_pct = int(total_dmg / max_dmg * 100)
        team_color = TEAM_COLOR_CSS.get(pp.team, "#888")
        bar_html = (
            f'<div class="dmg-bar-wrap">'
            f'<div class="dmg-bar-fill" style="width:{bar_pct}%;background:{team_color}"></div>'
            f"</div>"
        )
        row_cls = "row-radiant" if pp.team == 2 else "row-dire"
        dmg_taken_cell = f'<td class="r" title="{_e(top_attacker)}">{total_dmg_taken:,}</td>'
        parts.append(
            f'<tr class="{row_cls}">'
            f'<td style="white-space:nowrap">{_hero_cell(pp.hero_name, pp.team)}</td>'
            f'<td><span style="color:{team_color}">{_e(_team_name(pp.team))}</span></td>'
            f'<td class="r">{total_dmg:,}</td>'
            f"<td>{top_ability}</td>"
            f"<td>{top3_str}</td>"
            f"{dmg_taken_cell}"
            f'<td class="r">{total_heal:,}</td>'
            f'<td class="r">{pp.stuns_dealt:.1f}</td>'
            f"<td>{bar_html}</td>"
            f"</tr>"
        )
    parts.append("</tbody></table>")
    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _hero_cell(npc_name: str, team: int = 0) -> str:
    """Return an icon + name cell fragment for a hero NPC name.

    Args:
        npc_name: Hero NPC name e.g. ``"npc_dota_hero_axe"``.
        team: Team number for name colouring (2=Radiant, 3=Dire, 0=neutral).

    Returns:
        HTML fragment with a 20px portrait thumbnail followed by the display name.
    """
    src = _hero_icon_src(npc_name)
    name = _e(_hero(npc_name))
    color = TEAM_COLOR_CSS.get(team, "#e6edf3")
    return (
        f'<img src="{src}" width="20" height="12" '
        f'style="object-fit:cover;border-radius:2px;vertical-align:middle;margin-right:5px">'
        f'<span style="color:{color}">{name}</span>'
    )


def _is_active_teamfight_player(p: object) -> bool:
    """Return True for active teamfight participants only."""
    return (
        getattr(p, "deaths", 0) > 0
        or getattr(p, "damage_dealt", 0) > 0
        or getattr(p, "damage_taken", 0) > 0
        or getattr(p, "healing", 0) > 0
    )


def _top_abilities_teamfight(ability_uses: dict[str, int], n: int = 3) -> str:
    """Format top abilities used in one teamfight row."""
    if not ability_uses:
        return '<span class="dim">—</span>'
    top = sorted(ability_uses.items(), key=lambda x: x[1], reverse=True)[:n]
    return " · ".join(f"{_e(ability_display(a))} ×{c}" for a, c in top)


def _teamfight_minimap_svg(
    fight_idx: int,
    mid_tick: int,
    slot_to_player: dict[int, gem.ParsedPlayer],
    active_slots: list[int],
    died_slots: set[int],
    map_b64: str | None,
    size: int = 260,
) -> str:
    """Render one fight minimap SVG with hero portrait markers."""
    # Coordinate system aligned with movement_heatmap.py and ward map.
    _XMIN, _XMAX = 7563, 25900
    _YMIN, _YMAX = 7800, 25600

    def _world_to_px(wx: float, wy: float) -> tuple[float, float]:
        px = (wx - _XMIN) / (_XMAX - _XMIN) * size
        py = (1.0 - (wy - _YMIN) / (_YMAX - _YMIN)) * size
        return px, py

    icon_r = 12
    hero_elements: list[str] = []
    for slot in active_slots:
        pp = slot_to_player.get(slot)
        if pp is None or not pp.position_log or not pp.hero_name:
            continue
        closest = min(pp.position_log, key=lambda t: abs(t[0] - mid_tick))
        _, wx, wy = closest
        cx, cy = _world_to_px(wx, wy)

        stroke = "#ffffff" if slot in died_slots else TEAM_COLOR_CSS.get(pp.team, "#8b949e")
        stroke_w = 2.4 if slot in died_slots else 1.8
        clip_id = f"tf_clip_{fight_idx}_{slot}"
        src = _hero_icon_src(pp.hero_name)

        hero_elements.append(
            f'<defs><clipPath id="{clip_id}"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}"/></clipPath></defs>'
            f'<image href="{src}" x="{cx - icon_r:.1f}" y="{cy - icon_r:.1f}" '
            f'width="{icon_r * 2}" height="{icon_r * 2}" clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}" fill="none" stroke="{stroke}" stroke-width="{stroke_w}"/>'
        )

    bg_img = (
        f'<image href="data:image/jpeg;base64,{map_b64}" x="0" y="0" width="{size}" height="{size}" '
        f'preserveAspectRatio="xMidYMid slice"/>'
        if map_b64
        else ""
    )

    return (
        f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg" '
        f'style="border-radius:6px;overflow:hidden;flex-shrink:0">'
        f'<rect x="0" y="0" width="{size}" height="{size}" fill="#1a2a1a"/>'
        f"{bg_img}"
        f"{''.join(hero_elements)}"
        f"</svg>"
    )


def _build_teamfights(match: gem.ParsedMatch, map_b64: str | None) -> str:
    """Build the Teamfights tab content (filters + fight cards)."""
    fights = match.teamfights or []
    if not fights:
        return (
            '<div class="card"><details open><summary>Teamfights</summary>'
            '<div class="card-body"><p class="dim">(no teamfights detected)</p></div>'
            "</details></div>"
        )

    slot_to_player: dict[int, gem.ParsedPlayer] = {pp.player_id: pp for pp in match.players}
    _load_hero_icons([pp.hero_name for pp in match.players if pp.hero_name])

    max_deaths = max((tf.deaths for tf in fights), default=1)
    max_participants = max(
        (sum(1 for p in tf.players if _is_active_teamfight_player(p)) for tf in fights),
        default=1,
    )

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Teamfights</summary>",
        '<div class="card-body">',
        f'<div class="tf-summary">Showing <strong id="tf-vis-count">{len(fights)}</strong> / {len(fights)} fights</div>',
        '<div class="tf-filter-bar">',
        '<div class="tf-filter-group">',
        '<div class="tf-filter-label">Min deaths <span id="tf-deaths-val">1</span></div>',
        f'<input type="range" id="tf-deaths" min="1" max="{max(max_deaths, 1)}" value="1" step="1">',
        "</div>",
        '<div class="tf-filter-group">',
        '<div class="tf-filter-label">Min active participants <span id="tf-participants-val">1</span></div>',
        f'<input type="range" id="tf-participants" min="1" max="{max(max_participants, 1)}" value="1" step="1">',
        "</div>",
        "</div>",
    ]

    for i, tf in enumerate(fights, start=1):
        tf_by_slot = {p.player_id: p for p in tf.players}
        active_slots = [p.player_id for p in tf.players if _is_active_teamfight_player(p)]
        died_slots = {p.player_id for p in tf.players if p.deaths > 0}

        radiant_slots = sorted(
            s
            for s in active_slots
            if slot_to_player.get(s) is not None and slot_to_player[s].team == 2
        )
        dire_slots = sorted(
            s
            for s in active_slots
            if slot_to_player.get(s) is not None and slot_to_player[s].team == 3
        )
        # Keep unknown-team slots at the end (should be rare, but avoids silent drops).
        unknown_slots = sorted(
            s
            for s in active_slots
            if slot_to_player.get(s) is None or slot_to_player[s].team not in (2, 3)
        )
        ordered_slots = radiant_slots + dire_slots + unknown_slots
        n_participants = len(ordered_slots)

        parts.append(
            f'<div class="tf-fight-card" data-deaths="{tf.deaths}" data-participants="{n_participants}">'
            f'<div class="tf-fight-header">'
            f'<span class="tf-fight-index">Fight #{i}</span>'
            f'<span class="tf-fight-time">{_e(_fmt_tick(tf.start_tick))} → {_e(_fmt_tick(tf.end_tick))}</span>'
            f'<span class="tf-fight-meta">☠ {tf.deaths} · 👤 {n_participants}</span>'
            f"</div>"
            f'<div class="tf-fight-body">'
            f'<div class="tf-fight-map">{_teamfight_minimap_svg(i, (tf.start_tick + tf.end_tick) // 2, slot_to_player, active_slots, died_slots, map_b64)}</div>'
            f'<div class="tf-fight-right">'
        )

        if ordered_slots:
            parts.append('<div class="tf-participants">')
            for slot in ordered_slots:
                pp = slot_to_player.get(slot, gem.ParsedPlayer(player_id=slot))
                team_cls = "radiant" if pp.team == 2 else "dire"
                died_cls = " died" if slot in died_slots else ""
                pname = _e(pp.player_name or "")
                hname = _e(_hero(pp.hero_name))
                src = _hero_icon_src(pp.hero_name)
                parts.append(
                    f'<div class="tf-participant {team_cls}{died_cls}">'
                    f'<img src="{src}" alt="{hname}">'
                    f'<div class="tf-participant-hero">{hname}</div>'
                    f'<div class="tf-participant-player">{pname}</div>'
                    f"</div>"
                )
            parts.append("</div>")

            parts.append(
                '<div class="tf-table-wrap"><table class="tf-table"><thead><tr>'
                '<th>Hero</th><th class="r">DMG dealt</th><th class="r">DMG taken</th>'
                '<th class="r">Deaths</th><th class="r">BKs</th><th class="r">Healing</th>'
                '<th class="r">XP gained</th><th>Top abilities</th>'
                "</tr></thead><tbody>"
            )
            for slot in ordered_slots:
                pp = slot_to_player.get(slot, gem.ParsedPlayer(player_id=slot))
                tfp = tf_by_slot.get(slot)
                if tfp is None:
                    continue
                row_cls = "row-radiant" if pp.team == 2 else "row-dire"
                parts.append(
                    f'<tr class="{row_cls}">'
                    f"<td>{_hero_cell(pp.hero_name, pp.team)}"
                    f'<div style="color:#8b949e;font-size:11px">{_e(pp.player_name or "")}</div></td>'
                    f'<td class="r">{getattr(tfp, "damage_dealt", 0):,}</td>'
                    f'<td class="r">{getattr(tfp, "damage_taken", 0):,}</td>'
                    f'<td class="r">{getattr(tfp, "deaths", 0):,}</td>'
                    f'<td class="r">{getattr(tfp, "buybacks", 0):,}</td>'
                    f'<td class="r">{getattr(tfp, "healing", 0):,}</td>'
                    f'<td class="r">{getattr(tfp, "xp_delta", 0):,}</td>'
                    f"<td>{_top_abilities_teamfight(getattr(tfp, 'ability_uses', {}))}</td>"
                    f"</tr>"
                )
            parts.append("</tbody></table></div>")

        parts.append("</div></div></div>")

    parts.append(
        '<div id="tf-no-results" class="dim" style="display:none;padding:12px 0">(no fights match current filters)</div>'
    )
    parts.append("</div></details></div>")
    return "\n".join(parts)


def _build_kill_feed(match: gem.ParsedMatch) -> str:
    hvh = [
        e
        for e in match.combat_log
        if e.log_type == "DEATH" and e.attacker_is_hero and e.target_is_hero
    ]

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Kill Feed</summary>",
        '<div class="card-body">',
    ]

    if not hvh:
        parts.append('<p class="dim">(no hero-vs-hero kills recorded)</p>')
    else:
        # Build NPC → team map for colour coding
        npc_to_team: dict[str, int] = {
            pp.hero_name: pp.team for pp in match.players if pp.hero_name
        }
        # Pre-load icons for all heroes that appear in the kill feed
        all_npcs = {e.attacker_name for e in hvh} | {e.target_name for e in hvh}
        _load_hero_icons([n for n in all_npcs if n.startswith("npc_dota_hero_")])
        # Pre-load item icons for inflictors that are items
        _load_item_icons(
            [
                e.inflictor_name.removeprefix("item_")
                for e in hvh
                if e.inflictor_name and e.inflictor_name.startswith("item_")
            ]
        )

        parts.append(
            f'<p style="margin-bottom:8px;color:#8b949e">Total hero kills: <strong style="color:#e6edf3">{len(hvh)}</strong></p>'
        )
        parts.append("<table>")
        parts.append(
            "<thead><tr><th>Time</th><th>Killer</th><th>Victim</th><th>Via</th></tr></thead>"
        )
        parts.append("<tbody>")
        for entry in hvh:
            attacker_team = npc_to_team.get(entry.attacker_name, 0)
            target_team = npc_to_team.get(entry.target_name, 0)
            killer_cell = _hero_cell(entry.attacker_name, attacker_team)
            victim_cell = _hero_cell(entry.target_name, target_team)
            if entry.inflictor_name:
                if entry.inflictor_name.startswith("item_"):
                    via = _item_icon_tag(entry.inflictor_name, 16) + _e(
                        ability_display(entry.inflictor_name)
                    )
                else:
                    via = _e(ability_display(entry.inflictor_name))
            else:
                via = '<span style="color:#6e7681">auto-attack</span>'
            parts.append(
                f"<tr>"
                f'<td style="color:#8b949e">{_e(_fmt_tick(entry.tick))}</td>'
                f"<td>{killer_cell}</td>"
                f"<td>{victim_cell}</td>"
                f"<td>{via}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _build_draft(match: gem.ParsedMatch) -> str:
    if not match.draft:
        return ""

    from gem.constants import hero_display as _hero_display

    sorted_draft = sorted(match.draft, key=lambda d: d.tick)

    # Hero → player mapping for player name + team lookup
    hero_to_player: dict[str, gem.ParsedPlayer] = {
        pp.hero_name: pp for pp in match.players if pp.hero_name
    }

    def _pick_team(event: Any) -> int:
        """Return team for a pick/ban event (2=Radiant, 3=Dire)."""
        # For picks: player roster lookup is most reliable
        if event.is_pick and event.hero_name and event.hero_name in hero_to_player:
            return hero_to_player[event.hero_name].team
        # Use the active_team captured at draft time when available
        if event.team in (2, 3):
            return event.team
        # Fallback: slot_index for picks only (0-4=Radiant, 5-9=Dire)
        if event.is_pick:
            return 2 if event.slot_index < 5 else 3
        return 2  # unknown ban team

    # Pre-load hero icons for all drafted heroes
    _load_hero_icons([e.hero_name for e in sorted_draft if e.hero_name])

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Draft</summary>",
        '<div class="card-body">',
    ]

    # ---- Section 1: chronological sequence strip ----
    parts.append(
        '<div style="font-size:0.75rem;font-weight:700;letter-spacing:0.08em;'
        'text-transform:uppercase;color:#8b949e;margin-bottom:10px">Pick / Ban sequence</div>'
    )
    parts.append('<div class="draft-sequence">')
    for i, ev in enumerate(sorted_draft, 1):
        name = _hero_display(ev.hero_name) if ev.hero_name else f"ID {ev.hero_id}"
        src = _hero_icon_src(ev.hero_name) if ev.hero_name else _HERO_PLACEHOLDER_B64
        time_str = _fmt_tick(ev.tick) if ev.tick else ""
        team = _pick_team(ev)
        if not ev.is_pick:
            css_cls = "dc-ban-radiant" if team == 2 else "dc-ban-dire"
        else:
            css_cls = "dc-pick-radiant" if team == 2 else "dc-pick-dire"
        type_label = "PICK" if ev.is_pick else "BAN"
        parts.append(
            f'<div class="draft-cell {css_cls}" title="#{i} {type_label}: {_e(name)}">'
            f'<span class="dc-seq">#{i}</span>'
            f'<span class="dc-type-badge">{type_label}</span>'
            f'<img src="{src}" alt="{_e(name)}">'
            f'<div class="dc-name">{_e(name)}</div>'
            f'<div class="dc-time">{_e(time_str)}</div>'
            f"</div>"
        )
    parts.append("</div>")  # draft-sequence

    # ---- Section 2: team picks rows ----
    picks = [e for e in sorted_draft if e.is_pick]
    radiant_picks = [e for e in picks if _pick_team(e) == 2]
    dire_picks = [e for e in picks if _pick_team(e) == 3]

    def _picks_row(events: list, team_num: int) -> str:
        if not events:
            return ""
        label_cls = "radiant" if team_num == 2 else "dire"
        label_txt = "Radiant" if team_num == 2 else "Dire"
        cards = []
        for ev in events:
            name = _hero_display(ev.hero_name) if ev.hero_name else f"ID {ev.hero_id}"
            src = _hero_icon_src(ev.hero_name) if ev.hero_name else _HERO_PLACEHOLDER_B64
            pp = hero_to_player.get(ev.hero_name)
            player_name = pp.player_name if pp and pp.player_name else ""
            time_str = _fmt_tick(ev.tick) if ev.tick else ""
            player_html = f'<div class="dp-player">{_e(player_name)}</div>' if player_name else ""
            cards.append(
                f'<div class="draft-pick-card {label_cls}">'
                f'<img src="{src}" alt="{_e(name)}">'
                f'<div class="dp-name">{_e(name)}</div>'
                f"{player_html}"
                f'<div class="dp-time">{_e(time_str)}</div>'
                f"</div>"
            )
        return (
            f'<div class="draft-team-row">'
            f'<div class="draft-team-label {label_cls}">{label_txt}</div>'
            f'<div class="draft-picks-row">{"".join(cards)}</div>'
            f"</div>"
        )

    if picks:
        parts.append(
            '<div style="font-size:0.75rem;font-weight:700;letter-spacing:0.08em;'
            'text-transform:uppercase;color:#8b949e;margin:16px 0 10px">Picks by team</div>'
        )
        parts.append(_picks_row(radiant_picks, 2))
        parts.append(_picks_row(dire_picks, 3))

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _build_purchases(match: gem.ParsedMatch) -> str:
    total_purchases = sum(len(p.purchase_log) for p in match.players)

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Purchase Timeline</summary>",
        '<div class="card-body">',
    ]

    if total_purchases == 0:
        parts.append(
            '<p class="dim">No purchase data available — HLTV/spectator replays may not carry '
            "hero-attributed PURCHASE events in the S2 combat log path.</p>"
        )
    else:
        for pp in sorted(match.players, key=lambda p: p.team):
            if not pp.purchase_log or not pp.hero_name:
                continue
            team_color = TEAM_COLOR_CSS.get(pp.team, "#888")
            hero_display = _e(_hero(pp.hero_name))
            team_display = _e(_team_name(pp.team))
            parts.append('<details class="sub-accordion">')
            parts.append(
                f"<summary>"
                f'<span style="color:{team_color}">{hero_display}</span> '
                f'<span style="color:#8b949e;font-size:12px">({team_display}, {len(pp.purchase_log)} purchases)</span>'
                f"</summary>"
            )
            parts.append("<table>")
            parts.append("<thead><tr><th>Time</th><th>Item</th></tr></thead>")
            parts.append("<tbody>")
            for entry in sorted(pp.purchase_log, key=lambda e: e.tick):
                display_name = (
                    _e(item_display(entry.value_name))
                    if entry.value_name
                    else _e(entry.value_name or "")
                )
                icon = _item_icon_tag(entry.value_name or "", 20) if entry.value_name else ""
                parts.append(
                    f"<tr><td>{_e(_fmt_tick(entry.tick))}</td><td>{icon}{display_name}</td></tr>"
                )
            parts.append("</tbody></table>")
            parts.append("</details>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _build_buybacks(match: gem.ParsedMatch) -> str:
    total = sum(len(p.buyback_log) for p in match.players)

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Buybacks</summary>",
        '<div class="card-body">',
    ]

    if total == 0:
        parts.append('<p class="dim">(no buybacks recorded)</p>')
    else:
        parts.append("<table>")
        parts.append("<thead><tr><th>Time</th><th>Hero</th><th>Team</th></tr></thead>")
        parts.append("<tbody>")
        entries: list[tuple[int, str, int]] = []
        for pp in match.players:
            for entry in pp.buyback_log:
                entries.append((entry.tick, pp.hero_name, pp.team))
        entries.sort(key=lambda x: x[0])
        for tick, hero_name, team in entries:
            team_color = TEAM_COLOR_CSS.get(team, "#888")
            parts.append(
                f"<tr>"
                f"<td>{_e(_fmt_tick(tick))}</td>"
                f"<td>{_e(_hero(hero_name))}</td>"
                f'<td><span style="color:{team_color}">{_e(_team_name(team))}</span></td>'
                f"</tr>"
            )
        parts.append("</tbody></table>")
        parts.append(f'<p class="section-note">Total buybacks: {total}</p>')

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _build_runes(match: gem.ParsedMatch) -> str:
    total = sum(len(p.runes_log) for p in match.players)

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Rune Pickups</summary>",
        '<div class="card-body">',
    ]

    if total == 0:
        parts.append('<p class="dim">(no rune pickups recorded)</p>')
    else:
        # Pre-load rune icons and hero icons
        _load_item_icons(list(_RUNE_ICON_SHORT.values()))
        all_hero_npcs = [pp.hero_name for pp in match.players if pp.hero_name]
        _load_hero_icons(all_hero_npcs)

        parts.append("<table>")
        parts.append("<thead><tr><th>Time</th><th>Hero</th><th>Team</th><th>Rune</th></tr></thead>")
        parts.append("<tbody>")
        entries: list[tuple[int, str, int, int]] = []
        for pp in match.players:
            for entry in pp.runes_log:
                entries.append((entry.tick, pp.hero_name, pp.team, entry.gold_reason))
        entries.sort(key=lambda x: x[0])
        for tick, hero_name, team, rune_type in entries:
            rune_name = _RUNE_NAMES.get(rune_type, f"Rune {rune_type}")
            icon_short = _RUNE_ICON_SHORT.get(rune_type, "")
            rune_icon = _item_icon_tag(icon_short, 18) if icon_short else ""
            team_color = TEAM_COLOR_CSS.get(team, "#888")
            parts.append(
                f"<tr>"
                f'<td style="color:#8b949e">{_e(_fmt_tick(tick))}</td>'
                f"<td>{_hero_cell(hero_name, team)}</td>"
                f'<td><span style="color:{team_color}">{_e(_team_name(team))}</span></td>'
                f"<td>{rune_icon}{_e(rune_name)}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _build_chat(match: gem.ParsedMatch) -> str:
    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Chat Log</summary>",
        '<div class="card-body">',
    ]

    if not match.chat:
        parts.append('<p class="dim">(no chat messages recorded)</p>')
    else:
        # Build player_slot → (hero_name, team) map
        slot_to_hero: dict[int, tuple[str, int]] = {}
        for pp in match.players:
            if pp.hero_name:
                slot_to_hero[pp.player_id] = (pp.hero_name, pp.team)

        parts.append("<table>")
        parts.append(
            "<thead><tr><th>Time</th><th>Hero</th><th>Channel</th><th>Message</th></tr></thead>"
        )
        parts.append("<tbody>")
        for msg in match.chat:
            hero_name, team = slot_to_hero.get(msg.player_slot, ("?", 0))
            team_color = TEAM_COLOR_CSS.get(team, "#8b949e")
            channel_label = "ALL" if msg.channel == "all" else "TEAM"
            channel_color = "#ffb74d" if msg.channel == "all" else team_color
            parts.append(
                f"<tr>"
                f"<td>{_e(_fmt_tick(msg.tick))}</td>"
                f'<td><span style="color:{team_color}">{_e(_hero(hero_name))}</span></td>'
                f'<td><span style="color:{channel_color};font-weight:bold">{_e(channel_label)}</span></td>'
                f"<td>{_e(msg.text)}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")
        parts.append(f'<p class="section-note">Total messages: {len(match.chat)}</p>')

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------


def _build_movement_tab(match: gem.ParsedMatch, map_b64: str | None) -> str:
    """Build the Movement tab content using Plotly.

    Returns an empty string if plotly is not installed or no map image is
    available — the tab is omitted from the report in that case.

    Args:
        match: Parsed match data.
        map_b64: Base64-encoded map image, or ``None``.

    Returns:
        HTML string for the tab content, or ``""`` if unavailable.
    """
    if map_b64 is None:
        return ""
    try:
        import plotly.graph_objects as go  # noqa: F401
        from movement_heatmap import build_figure
    except ImportError:
        try:
            # When run directly from the examples/ directory or project root
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "movement_heatmap",
                Path(__file__).parent / "movement_heatmap.py",
            )
            mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
            spec.loader.exec_module(mod)  # type: ignore[union-attr]
            build_figure = mod.build_figure
        except Exception:
            return ""

    try:
        import tempfile

        import plotly.io as pio

        # Write map image to a temp file so build_figure can read it
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(base64.b64decode(map_b64))
            tmp_path = Path(tmp.name)

        fig = build_figure(match, tmp_path, dem_stem="match")
        tmp_path.unlink(missing_ok=True)

        # Embed as a standalone div (no full HTML wrapper, CDN Plotly).
        plotly_div = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs="cdn",
            config={"responsive": True},
        )

        # Extract the auto-generated div id so we can cancel autoplay via JS.
        # Plotly emits: <div id="..." class="plotly-graph-div" ...>
        import re as _re

        m = _re.search(r'<div id="([^"]+)" class="plotly-graph-div"', plotly_div)
        div_id = m.group(1) if m else ""

        # After Plotly initialises the figure, pause at frame 0 immediately.
        # Plotly.animate(id, null, {mode:'immediate'}) cancels any queued animation.
        pause_js = ""
        if div_id:
            pause_js = (
                f"<script>"
                f"(function waitForPlotly(){{"
                f'  var el = document.getElementById("{div_id}");'
                f"  if (!el || !el._fullLayout) {{ setTimeout(waitForPlotly, 50); return; }}"
                f'  Plotly.animate("{div_id}", null, {{mode:"immediate"}});'
                f"}})();"
                f"</script>"
            )

        return (
            f'<div class="card"><div class="card-body" style="padding:8px">'
            f"{plotly_div}{pause_js}"
            f"</div></div>"
        )
    except Exception:
        return ""


def build_html(match: gem.ParsedMatch, map_b64: str | None = None) -> str:
    """Assemble the complete self-contained multi-tab HTML report.

    Args:
        match: Parsed match data from ``gem.parse()``.
        map_b64: Base64-encoded map image for the ward canvas and movement
            heatmap, or ``None``.

    Returns:
        Complete HTML string.
    """
    global _GAME_START_TICK
    _GAME_START_TICK = match.game_start_tick or 0

    # Pre-load icons for canvas ward/smoke markers and purchase timeline
    _canvas_icons = ["ward_observer", "ward_sentry", "smoke_of_deceit"]
    _purchase_icons = [
        e.value_name.removeprefix("item_")
        for pp in match.players
        for e in pp.purchase_log
        if e.value_name
    ]
    _load_item_icons(_canvas_icons + list(set(_purchase_icons)))

    # Pre-load hero portrait icons for the draft section
    _load_hero_icons([e.hero_name for e in match.draft if e.hero_name])

    # Build each tab's content
    header_html = _build_header(match)

    tabs: list[tuple[str, str]] = [
        (
            "Overview",
            "\n".join(
                filter(
                    None,
                    [
                        _build_scoreboard(match),
                        _build_hero_timeseries_chart(match),
                        _build_gold_xp_chart(match),
                    ],
                )
            ),
        ),
        (
            "Combat",
            "\n".join(
                filter(
                    None,
                    [
                        _build_damage(match),
                        _build_kill_feed(match),
                    ],
                )
            ),
        ),
        ("Teamfights", _build_teamfights(match, map_b64)),
        ("Vision", _build_wards(match, map_b64)),
        (
            "Economy",
            "\n".join(
                filter(
                    None,
                    [
                        _build_purchases(match),
                        _build_buybacks(match),
                        _build_runes(match),
                    ],
                )
            ),
        ),
        ("Draft", _build_draft(match)),
        (
            "Misc",
            "\n".join(
                filter(
                    None,
                    [
                        _build_objectives(match),
                        _build_chat(match),
                    ],
                )
            ),
        ),
    ]

    # Movement tab — optional (requires plotly + map image)
    movement_html = _build_movement_tab(match, map_b64)
    if movement_html:
        tabs.append(("Movement", movement_html))

    # Remove tabs with no content
    tabs = [(label, content) for label, content in tabs if content.strip()]

    # Build tab bar + pages
    tab_inputs = []
    tab_labels = []
    tab_pages = []
    for i, (label, content) in enumerate(tabs):
        tid = f"tab{i}"
        checked = " checked" if i == 0 else ""
        tab_inputs.append(f'<input type="radio" name="gemtab" id="{tid}"{checked}>')
        tab_labels.append(f'<label for="{tid}">{html.escape(label)}</label>')
        tab_pages.append(
            f'<div class="tab-page{" active" if i == 0 else ""}" id="page-{tid}">\n{content}\n</div>'
        )

    tab_bar = (
        '<div class="tab-bar">\n'
        + "\n".join(f"{inp}\n{lbl}" for inp, lbl in zip(tab_inputs, tab_labels, strict=False))
        + "\n</div>"
    )

    pages_html = "\n".join(tab_pages)

    # JS: switch active tab on radio change + resize Chart.js on tab show
    tab_js = """
<script>
(function() {
  function applyTeamfightFilters() {
    var deathsEl = document.getElementById('tf-deaths');
    var partsEl = document.getElementById('tf-participants');
    if (!deathsEl || !partsEl) return;

    var minDeaths = parseInt(deathsEl.value || '1', 10);
    var minParts = parseInt(partsEl.value || '1', 10);

    var dVal = document.getElementById('tf-deaths-val');
    var pVal = document.getElementById('tf-participants-val');
    if (dVal) dVal.textContent = String(minDeaths);
    if (pVal) pVal.textContent = String(minParts);

    var cards = Array.prototype.slice.call(document.querySelectorAll('.tf-fight-card'));
    var shown = 0;
    cards.forEach(function(card) {
      var deaths = parseInt(card.getAttribute('data-deaths') || '0', 10);
      var participants = parseInt(card.getAttribute('data-participants') || '0', 10);
      var visible = deaths >= minDeaths && participants >= minParts;
      card.classList.toggle('hidden', !visible);
      if (visible) shown++;
    });

    var vis = document.getElementById('tf-vis-count');
    if (vis) vis.textContent = String(shown);
    var noRes = document.getElementById('tf-no-results');
    if (noRes) noRes.style.display = shown === 0 ? 'block' : 'none';
  }

  var radios = document.querySelectorAll('input[name="gemtab"]');
  radios.forEach(function(r) {
    r.addEventListener('change', function() {
      document.querySelectorAll('.tab-page').forEach(function(p) {
        p.classList.remove('active');
      });
      var page = document.getElementById('page-' + r.id);
      if (page) page.classList.add('active');
      // Resize any Chart.js charts that just became visible
      if (window.Chart) {
        Object.values(Chart.instances).forEach(function(c) { c.resize(); });
      }
      applyTeamfightFilters();
    });
  });

  var tfDeaths = document.getElementById('tf-deaths');
  var tfParts = document.getElementById('tf-participants');
  if (tfDeaths) tfDeaths.addEventListener('input', applyTeamfightFilters);
  if (tfParts) tfParts.addEventListener('input', applyTeamfightFilters);
  applyTeamfightFilters();
})();
</script>"""

    body_parts = [header_html, tab_bar, pages_html, tab_js]
    body = "\n".join(p for p in body_parts if p)

    return "\n".join(
        [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            "<title>Dota 2 Match Report</title>",
            '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>',
            "<style>",
            _CSS,
            "</style>",
            "</head>",
            "<body>",
            '<div class="container">',
            body,
            "</div>",
            "</body>",
            "</html>",
        ]
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse a .dem replay and write a self-contained HTML match report."""
    parser = argparse.ArgumentParser(
        description="Generate an HTML match report from a Dota 2 .dem replay file."
    )
    parser.add_argument("dem", nargs="?", help="Path to the .dem replay file")
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output HTML file path (default: <dem_name>_report.html in project root)",
    )
    parser.add_argument(
        "--map",
        default=None,
        help="Path to map image for ward overlay (default: tests/fixtures/Game_map_7.40.jpg)",
    )
    args = parser.parse_args()

    if args.dem:
        dem_path = args.dem
    else:
        dem_path = str(
            Path(__file__).parent.parent / "tests" / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"
        )

    print(f"Parsing {dem_path} ...")
    match = gem.parse(dem_path)

    # Load map image for ward canvas
    map_path = (
        Path(args.map)
        if args.map
        else Path(__file__).parent.parent / "tests" / "fixtures" / "Game_map_7.40.jpg"
    )
    map_b64: str | None = None
    if map_path.exists():
        map_b64 = base64.b64encode(map_path.read_bytes()).decode()
        print(f"Map image loaded: {map_path}")
    else:
        print(f"Map image not found at {map_path} — ward map will render without background.")

    if args.output:
        output_path = Path(args.output)
    else:
        dem_file = Path(dem_path)
        project_root = Path(__file__).parent.parent
        output_path = project_root / (dem_file.stem + "_report.html")

    html_content = build_html(match, map_b64)
    output_path.write_text(html_content, encoding="utf-8")
    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
