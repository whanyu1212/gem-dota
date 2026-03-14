"""Movement heatmap figure builder used by match_report."""

from __future__ import annotations

import base64
from collections import defaultdict
from pathlib import Path

import plotly.graph_objects as go

import gem
from gem.constants import ability_display, hero_display, item_display, league_name
from report.helpers import MAP_XMAX, MAP_XMIN, MAP_YMAX, MAP_YMIN

# ---------------------------------------------------------------------------
# Dota 2 map coordinate system
# Calibrated against Game_map_7.40.jpg using fountain positions as anchors.
# Radiant fountain: (9684, 9684)  Dire fountain: (23120, 22350)
# ---------------------------------------------------------------------------

_TICKS_PER_SEC = 30
_TRAIL = 12  # number of past samples to show in the moving window

# Per-player-slot colors: Radiant blues/greens, Dire reds/purples
_SLOT_COLORS = [
    "#29b6f6",
    "#0288d1",
    "#26c6da",
    "#66bb6a",
    "#9ccc65",  # Radiant
    "#ef5350",
    "#ff7043",
    "#ffca28",
    "#ab47bc",
    "#ec407a",  # Dire
]

# Game mode labels (from DOTA_GameMode proto enum)
_GAME_MODE = {
    0: "Unknown",
    1: "All Pick",
    2: "Captains Mode",
    3: "Random Draft",
    4: "Single Draft",
    5: "All Random",
    11: "Least Played",
    16: "Captains Draft",
    18: "Ability Draft",
    20: "All Random DM",
    21: "1v1 Mid",
    22: "All Draft",
    23: "Turbo",
    24: "Mutation",
}


def _world_to_frac(wx: float, wy: float) -> tuple[float, float]:
    """Convert world (x, y) to [0, 1] fractions for Plotly axis coordinates."""
    fx = (wx - MAP_XMIN) / (MAP_XMAX - MAP_XMIN)
    fy = (wy - MAP_YMIN) / (MAP_YMAX - MAP_YMIN)
    return fx, fy


def _fmt_tick(tick: int) -> str:
    secs = tick // _TICKS_PER_SEC
    return f"{secs // 60:02d}:{secs % 60:02d}"


def _match_title(match: gem.ParsedMatch, dem_stem: str) -> str:
    mid = str(match.match_id) if match.match_id else dem_stem
    mode = _GAME_MODE.get(match.game_mode, f"Mode {match.game_mode}")
    parts = [f"Match {mid}", mode]
    if match.leagueid:
        name = league_name(match.leagueid)
        parts.append(name if name else f"League {match.leagueid}")
    return "  ·  ".join(parts)


_ACTIVITY_WINDOW = 150  # ticks (~5 seconds) to look back for recent activity
_MAX_ACTIVITY = 5  # max recent events to show in hover


def _build_hover_cache(
    match: gem.ParsedMatch, player_snapshots: dict[int, list]
) -> dict[int, dict]:
    """Pre-build per-player lookup structures for enriched hover text."""
    combat_by_hero: dict[str, list] = defaultdict(list)
    for e in match.combat_log:
        if e.attacker_name:
            combat_by_hero[e.attacker_name.lower()].append(e)

    cache: dict[int, dict] = {}
    for pp in match.players:
        if not pp.position_log:
            continue

        times = pp.times
        gold_t = pp.gold_t
        lh_t = pp.lh_t
        xp_t = pp.xp_t

        purchase_by_tick: list[tuple[int, str]] = sorted(
            (e.tick, e.value_name) for e in pp.purchase_log if e.value_name
        )

        # Combat events: kills, abilities, damage
        combat: list[tuple[int, str]] = []
        for e in pp.kills_log:
            target = e.target_name.removeprefix("npc_dota_hero_").replace("_", " ").title()
            combat.append((e.tick, f"Kill: {target}"))
        for e in combat_by_hero.get(pp.hero_name.lower(), []):
            if e.log_type == "ABILITY" and e.inflictor_name:
                aname = ability_display(e.inflictor_name)
                combat.append((e.tick, f"Ability: {aname}"))
            elif e.log_type == "DAMAGE" and e.value > 0:
                target = e.target_name.removeprefix("npc_dota_hero_").replace("_", " ").title()
                combat.append((e.tick, f"Damage: {target} -{e.value}"))
        combat.sort(key=lambda x: x[0])

        ability_levels_by_tick: list[tuple[int, dict[str, int]]] = [
            (snap.tick, snap.ability_levels)
            for snap in player_snapshots.get(pp.player_id, [])
            if snap.ability_levels
        ]

        cache[pp.player_id] = {
            "times": times,
            "gold_t": gold_t,
            "lh_t": lh_t,
            "xp_t": xp_t,
            "purchase_by_tick": purchase_by_tick,
            "combat": combat,
            "ability_levels_by_tick": ability_levels_by_tick,
            "stuns_dealt": pp.stuns_dealt,
        }
    return cache


def _hover_text(pp: gem.ParsedPlayer, tick: int, cache: dict, label: str, team: str) -> str:
    """Build enriched hover HTML for a hero at a given tick."""
    d = cache.get(pp.player_id)
    if not d:
        return f"<b>{label}</b><br>{team}<br>⏱ {_fmt_tick(tick)}"

    times = d["times"]
    idx = 0
    for i, t in enumerate(times):
        if t <= tick:
            idx = i
        else:
            break

    gold = d["gold_t"][idx] if idx < len(d["gold_t"]) else 0
    lh = d["lh_t"][idx] if idx < len(d["lh_t"]) else 0
    xp = d["xp_t"][idx] if idx < len(d["xp_t"]) else 0

    items = [
        item_display(name)
        for t, name in d["purchase_by_tick"]
        if t <= tick and not name.startswith("item_recipe")
    ]
    items_str = "  ".join(items[-6:]) if items else "—"

    ability_snap: dict[str, int] = {}
    for t, levels in d["ability_levels_by_tick"]:
        if t <= tick:
            ability_snap = levels
        else:
            break
    abilities_str = (
        "  ".join(f"{ability_display(n)} Lv{lv}" for n, lv in sorted(ability_snap.items()))
        if ability_snap
        else "—"
    )

    stuns = d["stuns_dealt"]
    stuns_str = f"{stuns:.1f}s" if stuns > 0 else "—"

    window_start = tick - _ACTIVITY_WINDOW
    recent = [text for t, text in d["combat"] if window_start <= t <= tick]
    seen: list[str] = []
    for r in reversed(recent):
        if not seen or seen[-1] != r:
            seen.append(r)
        if len(seen) >= _MAX_ACTIVITY:
            break
    recent_str = "<br>".join(reversed(seen)) if seen else "—"

    return (
        f"<b>{label}</b>  [{team[0]}]<br>"
        f"⏱ {_fmt_tick(tick)}<br>"
        f"<br>"
        f"Gold: {gold:,}  LH: {lh}  XP: {xp:,}<br>"
        f"Items: {items_str}<br>"
        f"Abilities: {abilities_str}<br>"
        f"Stuns dealt: {stuns_str}<br>"
        f"<br>"
        f"<i>Recent (±5s):</i><br>"
        f"{recent_str}"
    )


def build_figure(
    match: gem.ParsedMatch,
    map_path: Path,
    dem_stem: str,
    player_snapshots: dict[int, list] | None = None,
) -> go.Figure:
    """Build the Plotly figure with map background and animated hero traces."""
    with open(map_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    suffix = map_path.suffix.lstrip(".").lower()
    mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
    img_src = f"data:image/{mime};base64,{img_b64}"

    active_players = [pp for pp in match.players if pp.position_log]
    hover_cache = _build_hover_cache(match, player_snapshots or {})

    fig = go.Figure()

    fig.add_layout_image(
        {
            "source": img_src,
            "xref": "x",
            "yref": "y",
            "x": 0,
            "y": 1,
            "sizex": 1,
            "sizey": 1,
            "sizing": "stretch",
            "layer": "below",
        }
    )

    all_ticks: list[int] = sorted({tick for pp in match.players for tick, _, _ in pp.position_log})

    for pp in active_players:
        color = _SLOT_COLORS[pp.player_id]
        team = "Radiant" if pp.team == 2 else "Dire"
        name = hero_display(pp.hero_name)
        label = (
            f"{pp.player_name} · {name}"
            if pp.player_name
            else f"[{team[0]}{pp.player_id % 5 + 1}] {name}"
        )
        xs = [_world_to_frac(wx, wy)[0] for _, wx, wy in pp.position_log]
        ys = [_world_to_frac(wx, wy)[1] for _, wx, wy in pp.position_log]
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                name=label,
                line={"color": color, "width": 1, "dash": "dot"},
                opacity=0.25,
                legendgroup=f"hero_{pp.player_id}",
                legendgrouptitle_text=team if pp.player_id in (0, 5) else None,
                showlegend=True,
                hoverinfo="skip",
            )
        )

    for pp in active_players:
        color = _SLOT_COLORS[pp.player_id]
        team = "Radiant" if pp.team == 2 else "Dire"
        name = hero_display(pp.hero_name)
        label = (
            f"{pp.player_name} · {name}"
            if pp.player_name
            else f"[{team[0]}{pp.player_id % 5 + 1}] {name}"
        )
        first_tick, first_wx, first_wy = pp.position_log[0]
        fx0, fy0 = _world_to_frac(first_wx, first_wy)
        fig.add_trace(
            go.Scatter(
                x=[fx0],
                y=[fy0],
                mode="lines+markers",
                name=label,
                line={"color": color, "width": 2},
                marker={"color": color, "size": 10, "line": {"color": "white", "width": 0.5}},
                legendgroup=f"hero_{pp.player_id}",
                showlegend=False,
                hovertemplate="%{customdata}<extra></extra>",
                customdata=[_hover_text(pp, first_tick, hover_cache, label, team)],
            )
        )

    frames = []
    for tick in all_ticks:
        frame_data = []
        annotations = []

        for _ in active_players:
            frame_data.append(go.Scatter())

        for pp in active_players:
            color = _SLOT_COLORS[pp.player_id]
            name = hero_display(pp.hero_name)
            team = "Radiant" if pp.team == 2 else "Dire"
            ann_text = f"{pp.player_name} · {name}" if pp.player_name else name
            label = (
                f"{pp.player_name} · {name}"
                if pp.player_name
                else f"[{team[0]}{pp.player_id % 5 + 1}] {name}"
            )
            window = [(t, wx, wy) for t, wx, wy in pp.position_log if t <= tick][-_TRAIL:]
            if not window:
                t0, wx0, wy0 = pp.position_log[0]
                fx0, fy0 = _world_to_frac(wx0, wy0)
                frame_data.append(
                    go.Scatter(
                        x=[fx0],
                        y=[fy0],
                        customdata=[_hover_text(pp, t0, hover_cache, label, team)],
                    )
                )
                annotations.append(
                    {
                        "x": fx0,
                        "y": fy0,
                        "text": ann_text,
                        "xref": "x",
                        "yref": "y",
                        "showarrow": False,
                        "yshift": 14,
                        "font": {"size": 9, "color": color},
                        "bgcolor": "rgba(13,17,23,0.6)",
                        "borderpad": 2,
                    }
                )
                continue

            xs, ys, hovers = [], [], []
            for t, wx, wy in window:
                fx, fy = _world_to_frac(wx, wy)
                xs.append(fx)
                ys.append(fy)
                hovers.append(_hover_text(pp, t, hover_cache, label, team))
            sizes = [4] * (len(window) - 1) + [10]
            frame_data.append(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="lines+markers",
                    line={"color": color, "width": 2},
                    marker={
                        "color": color,
                        "size": sizes,
                        "line": {"color": "white", "width": 0.5},
                    },
                    customdata=hovers,
                    hovertemplate="%{customdata}<extra></extra>",
                )
            )
            annotations.append(
                {
                    "x": xs[-1],
                    "y": ys[-1],
                    "text": ann_text,
                    "xref": "x",
                    "yref": "y",
                    "showarrow": False,
                    "yshift": 14,
                    "font": {"size": 9, "color": color},
                    "bgcolor": "rgba(13,17,23,0.6)",
                    "borderpad": 2,
                }
            )

        frames.append(
            go.Frame(
                data=frame_data,
                layout=go.Layout(annotations=annotations),
                name=_fmt_tick(tick),
            )
        )

    fig.frames = frames

    if frames and frames[0].layout and frames[0].layout.annotations:
        fig.update_layout(annotations=list(frames[0].layout.annotations))

    steps = [
        {
            "method": "animate",
            "args": [
                [f.name],
                {
                    "mode": "immediate",
                    "frame": {"duration": 0, "redraw": True},
                    "transition": {"duration": 0},
                },
            ],
            "label": f.name,
        }
        for f in fig.frames
    ]

    title = _match_title(match, dem_stem)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 16, "color": "#e6edf3", "family": "monospace"},
        },
        xaxis={
            "range": [0, 1],
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "scaleanchor": "y",
        },
        yaxis={"range": [0, 1], "showgrid": False, "zeroline": False, "showticklabels": False},
        width=960,
        height=1000,
        margin={"l": 10, "r": 180, "t": 60, "b": 60},
        legend={
            "x": 1.01,
            "y": 0.98,
            "xanchor": "left",
            "bgcolor": "rgba(13,17,23,0.8)",
            "bordercolor": "#30363d",
            "borderwidth": 1,
            "font": {"size": 11, "color": "#e6edf3"},
        },
        sliders=[
            {
                "active": 0,
                "currentvalue": {
                    "prefix": "⏱  ",
                    "font": {"size": 14, "color": "#e6edf3"},
                    "xanchor": "center",
                },
                "pad": {"t": 15, "b": 10},
                "bgcolor": "#161b22",
                "bordercolor": "#30363d",
                "tickcolor": "#8b949e",
                "font": {"color": "#8b949e", "size": 10},
                "steps": steps,
            }
        ],
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 1.01,
                "xanchor": "left",
                "y": 0.55,
                "yanchor": "top",
                "bgcolor": "#161b22",
                "bordercolor": "#30363d",
                "font": {"color": "#e6edf3"},
                "buttons": [
                    {
                        "label": "▶  Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 150, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "⏸  Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                ],
            },
            {
                "type": "buttons",
                "showactive": True,
                "x": 1.01,
                "xanchor": "left",
                "y": 0.45,
                "yanchor": "top",
                "bgcolor": "#161b22",
                "bordercolor": "#30363d",
                "font": {"color": "#e6edf3", "size": 11},
                "buttons": [
                    {
                        "label": "0.5×",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 300, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "1×",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 150, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "2×",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 75, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "4×",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 37, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                ],
            },
        ],
    )

    return fig
