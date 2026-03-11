"""Teamfight report — generate an HTML teamfight breakdown from a replay.

Parses a .dem replay file and produces a self-contained HTML page showing
every detected teamfight with:

  - Interactive filter bar (min deaths, min active participants)
  - Minimap with hero icons plotted at their positions at fight midpoint
  - Hero icon strip for active participants only
  - Per-player stat table (damage dealt, damage taken, deaths, buybacks,
    healing, XP gained, top abilities used)

A hero is considered an "active participant" if they dealt or took hero damage,
healed an allied hero, or died during the fight window.  Ability/item use on
non-hero targets (e.g. farming nearby) does NOT count as participation.

Hero icons must be downloaded first::

    python scripts/fetch_hero_icons.py

Usage::

    python examples/teamfight_report.py <replay.dem> [--out <output.html>] [--map <map.jpg>]

Example::

    python examples/teamfight_report.py tests/fixtures/ti14_finals_g1_xg_vs_falcons.dem
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import gem
from gem.constants import ability_display, hero_display
from gem.extractors.teamfights import Teamfight, TeamfightPlayer

_ICON_DIR = Path(__file__).parent.parent / "src" / "gem" / "data" / "hero_icons"
_DEFAULT_MAP = Path(__file__).parent.parent / "tests" / "fixtures" / "Game_map_7.40.jpg"

_PLACEHOLDER_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

# Map coordinate bounds — calibrated from movement_heatmap.py using fountain anchors
_XMIN, _XMAX = 7563, 25900
_YMIN, _YMAX = 7800, 25600

TICKS_PER_SEC = 30
_MAP_SIZE = 300
_TEAM_COLOR = {2: "#4ade80", 3: "#f87171"}
_DEATH_STROKE = "#ffffff"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _icon_b64(npc_name: str) -> str:
    short = npc_name.removeprefix("npc_dota_hero_")
    path = _ICON_DIR / f"{short}.png"
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return _PLACEHOLDER_B64


def _map_b64(map_path: Path) -> str:
    suffix = map_path.suffix.lstrip(".").lower()
    mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
    data = base64.b64encode(map_path.read_bytes()).decode()
    return f"data:image/{mime};base64,{data}"


def _world_to_px(wx: float, wy: float, size: int = _MAP_SIZE) -> tuple[float, float]:
    px = (wx - _XMIN) / (_XMAX - _XMIN) * size
    py = (1.0 - (wy - _YMIN) / (_YMAX - _YMIN)) * size
    return px, py


def _fmt_tick(tick: int) -> str:
    secs = tick // TICKS_PER_SEC
    return f"{secs // 60:02d}:{secs % 60:02d}"


def _fmt_duration(start: int, end: int) -> str:
    secs = (end - start) // TICKS_PER_SEC
    return f"{secs}s"


def _is_active(p: TeamfightPlayer) -> bool:
    """A hero is an active participant only if they had direct hero-vs-hero combat involvement.

    Ability/item uses on non-hero targets (farming, stacking) are excluded intentionally
    to avoid counting heroes that were simply nearby but not fighting.
    """
    return p.deaths > 0 or p.damage_dealt > 0 or p.damage_taken > 0 or p.healing > 0


# ---------------------------------------------------------------------------
# Minimap SVG
# ---------------------------------------------------------------------------


def _minimap_svg(
    fight_idx: int,
    mid_tick: int,
    slot_to_player: dict[int, gem.ParsedPlayer],
    active_slots: list[int],
    died_slots: set[int],
    size: int = _MAP_SIZE,
) -> str:
    icon_r = 14
    icon_size = icon_r * 2
    hero_elements: list[str] = []

    for slot in active_slots:
        pp = slot_to_player.get(slot)
        if pp is None or not pp.position_log:
            continue
        closest = min(pp.position_log, key=lambda t: abs(t[0] - mid_tick))
        _, wx, wy = closest
        cx, cy = _world_to_px(wx, wy, size)

        stroke = _DEATH_STROKE if slot in died_slots else _TEAM_COLOR.get(pp.team, "#8b949e")
        stroke_width = 2.5 if slot in died_slots else 2
        icon_b64 = _icon_b64(pp.hero_name)
        display = hero_display(pp.hero_name) if pp.hero_name.startswith("npc_") else pp.hero_name
        clip_id = f"clip_f{fight_idx}_s{slot}"

        hero_elements.append(
            f'<defs><clipPath id="{clip_id}">'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}"/>'
            f"</clipPath></defs>"
            f'<image href="data:image/png;base64,{icon_b64}" '
            f'x="{cx - icon_r:.1f}" y="{cy - icon_r:.1f}" '
            f'width="{icon_size}" height="{icon_size}" '
            f'clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice">'
            f"<title>{display}</title></image>"
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}" '
            f'fill="none" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )

    return (
        f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg" '
        f'style="border-radius:6px;overflow:hidden;flex-shrink:0">'
        f'<image href="" id="map-ref-f{fight_idx}" x="0" y="0" '
        f'width="{size}" height="{size}" preserveAspectRatio="xMidYMid slice"/>'
        f"{''.join(hero_elements)}"
        f"</svg>"
        f'<script>document.getElementById("map-ref-f{fight_idx}").setAttribute("href",_MAP_URI);</script>'
    )


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #0d1117;
    color: #e6edf3;
    font-family: 'Segoe UI', system-ui, sans-serif;
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
}
h1 { font-size: 1.4rem; color: #58a6ff; margin-bottom: 4px; }
.subtitle { color: #8b949e; font-size: 0.9rem; margin-bottom: 16px; }

/* Summary bar */
.summary-bar {
    display: flex;
    gap: 24px;
    margin-bottom: 20px;
    padding: 12px 16px;
    background: #161b22;
    border-radius: 8px;
    border: 1px solid #21262d;
    font-size: 0.85rem;
    align-items: center;
}
.summary-bar span { color: #8b949e; }
.summary-bar strong { color: #e6edf3; }

/* Filter bar */
.filter-bar {
    display: flex;
    gap: 32px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 28px;
    padding: 14px 16px;
    background: #161b22;
    border-radius: 8px;
    border: 1px solid #21262d;
}
.filter-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-width: 180px;
}
.filter-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #8b949e;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    display: flex;
    justify-content: space-between;
}
.filter-label span { color: #e6edf3; font-weight: 700; }
input[type=range] {
    width: 100%;
    accent-color: #58a6ff;
    cursor: pointer;
}
.filter-hint {
    font-size: 0.7rem;
    color: #484f58;
}

/* Fight card */
.fight-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    margin-bottom: 24px;
    overflow: hidden;
    transition: opacity 0.15s;
}
.fight-card.hidden { display: none; }
.fight-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 16px;
    background: #1c2128;
    border-bottom: 1px solid #21262d;
    flex-wrap: wrap;
}
.fight-index { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; color: #58a6ff; text-transform: uppercase; }
.fight-time { font-family: monospace; font-size: 0.9rem; color: #e6edf3; }
.fight-duration { color: #8b949e; font-size: 0.8rem; }
.fight-meta { margin-left: auto; display: flex; gap: 8px; align-items: center; }
.badge {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 12px;
}
.badge-deaths { background: #3d1f1f; color: #f87171; }
.badge-participants { background: #1a2744; color: #58a6ff; }

/* Body layout */
.fight-body { display: flex; gap: 0; }
.fight-map { padding: 12px; flex-shrink: 0; border-right: 1px solid #21262d; }
.fight-right { flex: 1; min-width: 0; display: flex; flex-direction: column; }

/* Participant strip */
.participants {
    display: flex;
    gap: 6px;
    padding: 12px 16px;
    border-bottom: 1px solid #21262d;
    flex-wrap: wrap;
    align-items: flex-end;
}
.participant { display: flex; flex-direction: column; align-items: center; gap: 3px; width: 64px; }
.participant img { width: 64px; height: 36px; object-fit: cover; border-radius: 4px; border: 2px solid transparent; }
.participant.radiant img { border-color: #4ade80; }
.participant.dire img { border-color: #f87171; }
.participant.died img { box-shadow: 0 0 0 2px #ffffff; }
.participant .p-name { font-size: 0.55rem; color: #8b949e; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 64px; }
.participant .p-hero { font-size: 0.6rem; font-weight: 600; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 64px; }
.participant.radiant .p-hero { color: #4ade80; }
.participant.dire .p-hero { color: #f87171; }

/* Stat table */
.stat-table-wrap { padding: 12px 16px 16px; overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
th { text-align: left; color: #8b949e; font-weight: 600; padding: 6px 10px; border-bottom: 1px solid #21262d; white-space: nowrap; }
td { padding: 5px 10px; border-bottom: 1px solid #161b22; white-space: nowrap; }
tr:last-child td { border-bottom: none; }
tr.radiant td { background: #0d1a14; }
tr.dire td { background: #1a0d0d; }
tr.radiant td:first-child { border-left: 3px solid #4ade80; }
tr.dire td:first-child { border-left: 3px solid #f87171; }
.num { text-align: right; font-variant-numeric: tabular-nums; }
.zero { color: #484f58; }
.abilities { color: #a5b4fc; font-size: 0.7rem; }

.no-fights { color: #8b949e; font-style: italic; text-align: center; padding: 48px; }
#no-results { display: none; color: #8b949e; font-style: italic; text-align: center; padding: 48px; }
"""

# ---------------------------------------------------------------------------
# JavaScript for live filtering
# ---------------------------------------------------------------------------

_JS = """
const cards = Array.from(document.querySelectorAll('.fight-card'));
const visCount = document.getElementById('vis-count');
const noResults = document.getElementById('no-results');

function applyFilters() {
    const minDeaths = parseInt(document.getElementById('f-deaths').value);
    const minPart   = parseInt(document.getElementById('f-participants').value);
    document.getElementById('f-deaths-val').textContent = minDeaths;
    document.getElementById('f-part-val').textContent   = minPart;

    let shown = 0;
    cards.forEach(card => {
        const deaths = parseInt(card.dataset.deaths);
        const parts  = parseInt(card.dataset.participants);
        const visible = deaths >= minDeaths && parts >= minPart;
        card.classList.toggle('hidden', !visible);
        if (visible) shown++;
    });
    visCount.textContent = shown;
    noResults.style.display = shown === 0 ? 'block' : 'none';
}

document.getElementById('f-deaths').addEventListener('input', applyFilters);
document.getElementById('f-participants').addEventListener('input', applyFilters);
applyFilters();
"""


# ---------------------------------------------------------------------------
# HTML builders
# ---------------------------------------------------------------------------


def _num(val: int) -> str:
    return '<span class="zero">—</span>' if val == 0 else f"{val:,}"


def _top_abilities(ability_uses: dict[str, int], n: int = 3) -> str:
    if not ability_uses:
        return '<span class="zero">—</span>'
    top = sorted(ability_uses.items(), key=lambda x: x[1], reverse=True)[:n]
    parts = [f"{ability_display(a)} ×{c}" for a, c in top]
    return f'<span class="abilities">{" · ".join(parts)}</span>'


def _participant_html(npc_name: str, player_name: str, team: int, died: bool) -> str:
    icon = _icon_b64(npc_name)
    display = hero_display(npc_name) if npc_name.startswith("npc_") else npc_name
    team_cls = "radiant" if team == 2 else "dire"
    died_cls = " died" if died else ""
    pname_html = (
        f'<div class="p-name">{player_name}</div>' if player_name else '<div class="p-name"></div>'
    )
    return (
        f'<div class="participant {team_cls}{died_cls}">'
        f'<img src="data:image/png;base64,{icon}" alt="{display}" title="{display}" />'
        f'<div class="p-hero">{display}</div>'
        f"{pname_html}"
        f"</div>"
    )


def _fight_html(fight_idx: int, tf: Teamfight, slot_to_player: dict[int, gem.ParsedPlayer]) -> str:
    active_slots = [p.player_id for p in tf.players if _is_active(p)]
    died_slots = {p.player_id for p in tf.players if p.deaths > 0}

    radiant_slots = sorted(
        s for s in active_slots if slot_to_player.get(s, gem.ParsedPlayer(s)).team == 2
    )
    dire_slots = sorted(
        s for s in active_slots if slot_to_player.get(s, gem.ParsedPlayer(s)).team == 3
    )
    ordered_slots = radiant_slots + dire_slots
    n_participants = len(ordered_slots)

    # Header
    header = (
        f'<div class="fight-header">'
        f'<span class="fight-index">Fight #{fight_idx}</span>'
        f'<span class="fight-time">{_fmt_tick(tf.start_tick)} → {_fmt_tick(tf.end_tick)}</span>'
        f'<span class="fight-duration">({_fmt_duration(tf.start_tick, tf.end_tick)})</span>'
        f'<span class="fight-meta">'
        f'<span class="badge badge-deaths">☠ {tf.deaths} {"death" if tf.deaths == 1 else "deaths"}</span>'
        f'<span class="badge badge-participants">👤 {n_participants} active</span>'
        f"</span>"
        f"</div>"
    )

    # Minimap
    mid_tick = (tf.start_tick + tf.end_tick) // 2
    minimap = _minimap_svg(fight_idx, mid_tick, slot_to_player, active_slots, died_slots)

    # Participant strip
    cards = "".join(
        _participant_html(
            slot_to_player.get(s, gem.ParsedPlayer(s)).hero_name,
            slot_to_player.get(s, gem.ParsedPlayer(s)).player_name,
            slot_to_player.get(s, gem.ParsedPlayer(s)).team,
            died=s in died_slots,
        )
        for s in ordered_slots
    )
    participants_html = f'<div class="participants">{cards}</div>' if cards else ""

    # Stat table
    rows: list[str] = []
    for slot in ordered_slots:
        pp = slot_to_player.get(slot, gem.ParsedPlayer(slot))
        tfp = tf.players[slot]
        team_cls = "radiant" if pp.team == 2 else "dire"
        hero = (
            hero_display(pp.hero_name)
            if pp.hero_name.startswith("npc_")
            else pp.hero_name or f"Slot {slot}"
        )
        rows.append(
            f'<tr class="{team_cls}">'
            f"<td>{hero}<br><small style='color:#8b949e'>{pp.player_name or ''}</small></td>"
            f'<td class="num">{_num(tfp.damage_dealt)}</td>'
            f'<td class="num">{_num(tfp.damage_taken)}</td>'
            f'<td class="num">{_num(tfp.deaths)}</td>'
            f'<td class="num">{_num(tfp.buybacks)}</td>'
            f'<td class="num">{_num(tfp.healing)}</td>'
            f'<td class="num">{_num(tfp.xp_delta)}</td>'
            f"<td>{_top_abilities(tfp.ability_uses)}</td>"
            f"</tr>"
        )
    table_html = (
        (
            '<div class="stat-table-wrap"><table><thead><tr>'
            "<th>Hero</th><th>DMG dealt</th><th>DMG taken</th>"
            "<th>Deaths</th><th>BKs</th><th>Healing</th>"
            f"<th>XP gained</th><th>Top abilities</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table></div>"
        )
        if rows
        else ""
    )

    return (
        f'<div class="fight-card" data-deaths="{tf.deaths}" data-participants="{n_participants}">'
        f"{header}"
        f'<div class="fight-body">'
        f'<div class="fight-map">{minimap}</div>'
        f'<div class="fight-right">{participants_html}{table_html}</div>'
        f"</div></div>"
    )


def build_html(match: gem.ParsedMatch, dem_stem: str, map_path: Path) -> str:
    mid = str(match.match_id) if match.match_id else dem_stem
    slot_to_player: dict[int, gem.ParsedPlayer] = {pp.player_id: pp for pp in match.players}
    map_data_uri = _map_b64(map_path)
    map_js = f"<script>const _MAP_URI = '{map_data_uri}';</script>"

    fights = match.teamfights
    total = len(fights)
    max_deaths = max((tf.deaths for tf in fights), default=0)
    max_participants = max(
        (sum(1 for p in tf.players if _is_active(p)) for tf in fights), default=0
    )

    fights_html = (
        "".join(_fight_html(i + 1, tf, slot_to_player) for i, tf in enumerate(fights))
        if fights
        else '<p class="no-fights">No teamfights detected.</p>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Teamfights — Match {mid}</title>
<style>{_CSS}</style>
{map_js}
</head>
<body>
<h1>Teamfight Report — Match {mid}</h1>
<div class="subtitle">Detected from combat log · 15 s merge window · positions sampled at 1 s intervals · active = hero-vs-hero combat only</div>

<div class="summary-bar">
  <div><span>Showing</span><br /><strong id="vis-count">{total}</strong> / {total} fights</div>
  <div><span>Max deaths in one fight</span><br /><strong>{max_deaths}</strong></div>
  <div><span>Max active in one fight</span><br /><strong>{max_participants}</strong></div>
</div>

<div class="filter-bar">
  <div class="filter-group">
    <div class="filter-label">Min deaths &nbsp;<span id="f-deaths-val">1</span></div>
    <input type="range" id="f-deaths" min="1" max="{max(max_deaths, 1)}" value="1" step="1" />
    <div class="filter-hint">Reference threshold for a teamfight: 3</div>
  </div>
  <div class="filter-group">
    <div class="filter-label">Min active participants &nbsp;<span id="f-part-val">1</span></div>
    <input type="range" id="f-participants" min="1" max="{max(max_participants, 1)}" value="1" step="1" />
    <div class="filter-hint">Deals/takes hero dmg, heals, or dies</div>
  </div>
</div>

{fights_html}
<div id="no-results">No fights match the current filters.</div>
<script>{_JS}</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="HTML teamfight report from a Dota 2 replay.")
    parser.add_argument("replay", nargs="?", help="Path to .dem replay file")
    parser.add_argument("--out", default=None, help="Output HTML file")
    parser.add_argument(
        "--map", default=None, help="Path to map image (default: tests/fixtures/Game_map_7.40.jpg)"
    )
    args = parser.parse_args()

    if args.replay is None:
        fixture = (
            Path(__file__).parent.parent / "tests" / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"
        )
        if not fixture.exists():
            print("No replay specified and default fixture not found.", file=sys.stderr)
            sys.exit(1)
        args.replay = str(fixture)
        print(f"No replay specified — using fixture: {fixture.name}")

    map_path = Path(args.map) if args.map else _DEFAULT_MAP
    if not map_path.exists():
        print(f"Map image not found: {map_path}", file=sys.stderr)
        sys.exit(1)

    if not _ICON_DIR.exists() or not any(_ICON_DIR.glob("*.png")):
        print(
            "Warning: hero icons not found. Run 'python scripts/fetch_hero_icons.py' first.\n"
            "         Placeholder icons will be used.",
            file=sys.stderr,
        )

    print(f"Parsing {args.replay} ...")
    match = gem.parse(args.replay)
    dem_stem = Path(args.replay).stem
    print(f"Detected {len(match.teamfights)} fights total.")

    print("Building teamfight report ...")
    html = build_html(match, dem_stem, map_path)

    if args.out:
        out_path = Path(args.out)
    else:
        stem = str(match.match_id) if match.match_id else dem_stem
        out_path = Path(__file__).parent.parent / f"{stem}_teamfights.html"

    out_path.write_text(html, encoding="utf-8")
    print(f"Saved → {out_path}  ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
