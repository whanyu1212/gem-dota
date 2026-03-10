"""Draft extraction example — generate an HTML draft summary from a replay.

Parses a .dem replay file and produces a self-contained HTML page showing
hero picks and bans with portrait icons, player nicknames, and timestamps.

Hero icons must be downloaded first::

    python scripts/fetch_hero_icons.py

Usage::

    python examples/draft_summary.py <replay.dem> [--out <output.html>]

Example::

    python examples/draft_summary.py tests/fixtures/ti14_finals_g1_xg_vs_falcons.dem
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import gem
from gem.constants import hero_display, league_name

_ICON_DIR = Path(__file__).parent.parent / "src" / "gem" / "data" / "hero_icons"
_GAME_MODE = {
    2: "Captains Mode",
    22: "All Draft",
    23: "Turbo",
}

# Placeholder icon (1×1 grey PNG) used when icon file is missing
_PLACEHOLDER_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


def _icon_b64(short: str) -> str:
    path = _ICON_DIR / f"{short}.png"
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return _PLACEHOLDER_B64


def _short(npc_name: str) -> str:
    return npc_name.removeprefix("npc_dota_hero_")


def _fmt_tick(tick: int) -> str:
    secs = tick // 30
    return f"{secs // 60:02d}:{secs % 60:02d}"


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #0d1117;
    color: #e6edf3;
    font-family: 'Segoe UI', system-ui, sans-serif;
    padding: 24px;
}
h1 { font-size: 1.4rem; color: #58a6ff; margin-bottom: 4px; }
.subtitle { color: #8b949e; font-size: 0.9rem; margin-bottom: 32px; }
.section-title {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8b949e;
    margin: 28px 0 12px;
    border-bottom: 1px solid #21262d;
    padding-bottom: 6px;
}
/* Hero card */
.card {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    width: 90px;
    margin: 6px;
    border-radius: 8px;
    overflow: hidden;
    border: 2px solid transparent;
    transition: border-color 0.15s;
}
.card:hover { border-color: #58a6ff; }
.card img {
    width: 90px;
    height: 52px;
    object-fit: cover;
    display: block;
}
.card .hero-name {
    font-size: 0.65rem;
    font-weight: 600;
    text-align: center;
    padding: 3px 4px 2px;
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card .player-name {
    font-size: 0.6rem;
    color: #8b949e;
    text-align: center;
    padding-bottom: 4px;
}
.card .timestamp {
    font-size: 0.55rem;
    color: #484f58;
    padding-bottom: 4px;
    font-family: monospace;
}
/* Ban cards — greyed out with red tint */
.ban .card { filter: grayscale(60%); }
.ban .card { background: #1c1217; border-color: #3d1f1f; }
.ban .card .hero-name { color: #f87171; }
/* Pick cards */
.radiant .card { background: #111c18; border-color: #1a3a2a; }
.radiant .card .hero-name { color: #4ade80; }
.dire .card { background: #1c1117; border-color: #3a1a1a; }
.dire .card .hero-name { color: #f87171; }
/* Row labels */
.team-row { margin-bottom: 8px; }
.team-label {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.radiant .team-label { color: #4ade80; }
.dire .team-label { color: #f87171; }
.no-draft {
    color: #8b949e;
    font-style: italic;
    padding: 12px 0;
}
"""


def _card_html(
    npc_name: str,
    player_name: str = "",
    tick: int = 0,
    is_pick: bool = True,
) -> str:
    short = _short(npc_name) if npc_name.startswith("npc_") else npc_name
    icon = _icon_b64(short)
    name = hero_display(npc_name) if npc_name.startswith("npc_") else npc_name
    ts = _fmt_tick(tick) if tick else ""
    player_html = f'<div class="player-name">{player_name}</div>' if player_name else ""
    ts_html = f'<div class="timestamp">{ts}</div>' if ts else ""
    return (
        f'<div class="card">'
        f'<img src="data:image/png;base64,{icon}" alt="{name}" title="{name}" />'
        f'<div class="hero-name">{name}</div>'
        f"{player_html}"
        f"{ts_html}"
        f"</div>"
    )


def build_html(match: gem.ParsedMatch, dem_stem: str) -> str:
    mid = str(match.match_id) if match.match_id else dem_stem
    mode = _GAME_MODE.get(match.game_mode, f"Mode {match.game_mode}")
    league_str = ""
    if match.leagueid:
        lname = league_name(match.leagueid)
        league_str = f"  ·  {lname or f'League {match.leagueid}'}"

    hero_to_player: dict[str, gem.ParsedPlayer] = {
        pp.hero_name: pp for pp in match.players if pp.hero_name
    }

    bans = [e for e in match.draft if not e.is_pick]
    picks = [e for e in match.draft if e.is_pick]
    radiant_picks = [
        e for e in picks if hero_to_player.get(e.hero_name, gem.ParsedPlayer(0)).team == 2
    ]
    dire_picks = [
        e for e in picks if hero_to_player.get(e.hero_name, gem.ParsedPlayer(0)).team == 3
    ]

    # Bans section
    if bans:
        bans_html = (
            '<div class="ban">'
            + "".join(_card_html(e.hero_name, tick=e.tick, is_pick=False) for e in bans)
            + "</div>"
        )
    else:
        bans_html = '<p class="no-draft">No bans detected (All Pick / Turbo mode).</p>'

    # Picks section — Radiant
    def _picks_row(events: list, team_cls: str, team_label: str) -> str:
        if not events:
            return ""
        cards = "".join(
            _card_html(
                e.hero_name,
                player_name=hero_to_player[e.hero_name].player_name
                if e.hero_name in hero_to_player and hero_to_player[e.hero_name].player_name
                else "",
                tick=e.tick,
                is_pick=True,
            )
            for e in events
        )
        return (
            f'<div class="team-row {team_cls}">'
            f'<div class="team-label">{team_label}</div>'
            f"{cards}"
            f"</div>"
        )

    radiant_html = _picks_row(radiant_picks, "radiant", "Radiant")
    dire_html = _picks_row(dire_picks, "dire", "Dire")

    # No-picks fallback
    if not picks:
        picks_html = '<p class="no-draft">No picks detected.</p>'
    else:
        picks_html = radiant_html + dire_html

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Draft — Match {mid}</title>
<style>{_CSS}</style>
</head>
<body>
<h1>Match {mid}  ·  {mode}</h1>
<div class="subtitle">{league_str.lstrip(" ·") if league_str else "Public match"}</div>

<div class="section-title">Bans ({len(bans)})</div>
{bans_html}

<div class="section-title">Picks ({len(picks)})</div>
{picks_html}
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="HTML draft summary from a Dota 2 replay.")
    parser.add_argument("replay", help="Path to .dem replay file")
    parser.add_argument(
        "--out", default=None, help="Output HTML file (default: <match_id>_draft.html)"
    )
    args = parser.parse_args()

    if not _ICON_DIR.exists() or not any(_ICON_DIR.glob("*.png")):
        print(
            "Warning: hero icons not found. Run 'python scripts/fetch_hero_icons.py' first.\n"
            "         Placeholder icons will be used.",
            file=sys.stderr,
        )

    print(f"Parsing {args.replay} ...")
    match = gem.parse(args.replay)
    dem_stem = Path(args.replay).stem

    print("Building draft summary ...")
    html = build_html(match, dem_stem)

    if args.out:
        out_path = Path(args.out)
    else:
        stem = str(match.match_id) if match.match_id else dem_stem
        project_root = Path(__file__).parent.parent
        out_path = project_root / f"{stem}_draft.html"

    out_path.write_text(html, encoding="utf-8")
    print(f"Saved → {out_path}  ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
