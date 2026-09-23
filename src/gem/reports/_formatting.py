"""Shared formatting helpers for HTML match reports."""

from __future__ import annotations

import html

from gem.catalog import hero_short
from gem.reports.assets import has_hero_icon, hero_icon_src
from gem.state.game_clock import GameClock

TICKS_PER_SEC = 30
TICKS_PER_MIN = TICKS_PER_SEC * 60

TEAM_COLOR_CSS: dict[int, str] = {2: "#4caf50", 3: "#f44336"}
TEAM_NAMES: dict[int, str] = {2: "Radiant", 3: "Dire"}

# World-coordinate bounds used with assets/maps/Game_map_7.41.jpg. The 7.41
# image is normalized to the legacy canvas so the established projection stays stable.
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

# Set at report-build time so fmt_tick() produces pause-aware in-game times
_GAME_CLOCK: GameClock = GameClock(game_start_tick=0)


def set_game_clock(clock: GameClock) -> None:
    """Set the pause-aware game clock used by fmt_tick()."""
    global _GAME_CLOCK
    _GAME_CLOCK = clock


def set_game_start_tick(tick: int) -> None:
    """Set a pause-free clock anchored at ``tick`` (legacy; prefer set_game_clock)."""
    set_game_clock(GameClock(game_start_tick=tick))


def game_clock() -> GameClock:
    """Return the game clock configured for the report being built."""
    return _GAME_CLOCK


def fmt_tick(tick: int) -> str:
    """Format a replay tick as the in-game clock (MM:SS, pause-aware)."""
    return _GAME_CLOCK.format_tick(tick)


def tick_after_game_seconds(tick: int, seconds: float) -> int:
    """Return the replay tick ``seconds`` of in-game time after ``tick``.

    In-game timers such as Roshan's respawn stop during pauses, so the offset is
    applied on the pause-aware clock rather than on raw replay ticks.
    """
    start = _GAME_CLOCK.game_time_at(tick)
    later = _GAME_CLOCK.tick_at(start + seconds) if start is not None else None
    return later if later is not None else tick + round(seconds * TICKS_PER_SEC)


def game_clock_js_config(clock: GameClock) -> dict[str, object]:
    """Serialize a game clock for the report's client-side ``gemGameSeconds``."""
    return {
        "gameStartTick": clock.game_start_tick,
        "gameStartTimeS": clock.game_start_time_s,
        "netTickOffset": clock.net_tick_offset,
        "pauses": [[pause.start_tick, pause.end_tick] for pause in clock.pauses],
    }


# Client-side mirror of ``GameClock.game_seconds_at`` for playback labels.
GAME_CLOCK_JS = """
function gemGameSeconds(clock, tick) {
  var paused = 0;
  for (var i = 0; i < clock.pauses.length; i++) {
    var start = clock.pauses[i][0], end = clock.pauses[i][1];
    if (tick <= start) break;
    paused += (end === null ? tick : Math.min(tick, end)) - start;
  }
  if (clock.gameStartTimeS !== null && clock.gameStartTimeS !== undefined) {
    var unpaused = tick + clock.netTickOffset - paused;
    return Math.floor(unpaused / 30 + 0.5) - Math.floor(clock.gameStartTimeS + 0.5);
  }
  if (clock.gameStartTick === null || clock.gameStartTick === undefined) return null;
  var base = clock.gameStartTick;
  for (var j = 0; j < clock.pauses.length; j++) {
    var ps = clock.pauses[j][0], pe = clock.pauses[j][1];
    if (clock.gameStartTick <= ps) break;
    base -= (pe === null ? clock.gameStartTick : Math.min(clock.gameStartTick, pe)) - ps;
  }
  return Math.floor((tick - paused - base) / 30);
}
function gemFormatClock(clock, tick) {
  var secs = gemGameSeconds(clock, tick);
  if (secs === null) return '--:--';
  var neg = secs < 0;
  secs = Math.abs(secs);
  var m = Math.floor(secs / 60), s = secs % 60;
  var t = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  return neg ? '-' + t : t;
}
"""


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


def hero_cell(npc_name: str, team: int = 0) -> str:
    """Return an icon + name cell fragment for a hero NPC name.

    Args:
        npc_name: Hero NPC name e.g. ``"npc_dota_hero_axe"``.
        team: Team number for name colouring (2=Radiant, 3=Dire, 0=neutral).

    Returns:
        HTML fragment with a 20px portrait thumbnail followed by the display name.
    """
    name = e(hero(npc_name))
    color = TEAM_COLOR_CSS.get(team, "#e6edf3")
    # The cell already shows the name, so when no real icon is loaded we omit
    # the portrait (and its grey placeholder) rather than render a chip too.
    img = ""
    if has_hero_icon(npc_name):
        img = (
            f'<img src="{hero_icon_src(npc_name)}" width="20" height="12" '
            f'style="object-fit:cover;border-radius:2px;vertical-align:middle;margin-right:5px">'
        )
    return f'{img}<span style="color:{color}">{name}</span>'
