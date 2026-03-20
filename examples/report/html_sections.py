"""HTML section builders for the example match report."""

from __future__ import annotations

import json
from collections.abc import Callable

import gem
from gem.constants import ability_display, hero_display, item_display
from report.assets import (
    HERO_PLACEHOLDER_B64,
    ITEM_ICON_B64,
    hero_icon_src,
    item_icon_tag,
    load_hero_icons,
    load_item_icons,
)
from report.helpers import (
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    RUNE_ICON_SHORT,
    RUNE_NAMES,
    TEAM_COLOR_CSS,
    TICKS_PER_SEC,
    e,
    fmt_tick,
    hero,
    team_name,
)


def build_header(
    match: gem.ParsedMatch, fmt_tick: Callable[[int], str], game_modes: dict[int, str]
) -> str:
    """Build the report header section."""
    last_tick = match.game_end_tick or max(
        (max(p.times) for p in match.players if p.times), default=0
    )
    duration = fmt_tick(last_tick)
    if match.radiant_win is True:
        winner_color = "#4caf50"
        winner_text = "Radiant"
    elif match.radiant_win is False:
        winner_color = "#f44336"
        winner_text = "Dire"
    else:
        winner_color = "#8b949e"
        winner_text = "Unknown"
    mode = game_modes.get(match.game_mode, f"Mode {match.game_mode}")

    parts = [
        '<div class="match-header">',
        "  <h1>Match Report</h1>",
    ]
    if match.match_id:
        parts.append(
            f'  <div class="match-stat">'
            f'    <span class="label">Match ID</span>'
            f'    <span class="value">{e(str(match.match_id))}</span>'
            f"  </div>"
        )
    parts += [
        f'  <div class="match-stat">'
        f'    <span class="label">Duration</span>'
        f'    <span class="value">{e(duration)}</span>'
        f"  </div>",
        f'  <div class="match-stat">'
        f'    <span class="label">Winner</span>'
        f'    <span class="value" style="color:{winner_color}">{e(winner_text)}</span>'
        f"  </div>",
        f'  <div class="match-stat">'
        f'    <span class="label">Game Mode</span>'
        f'    <span class="value">{e(mode)}</span>'
        f"  </div>",
        "</div>",
    ]
    return "\n".join(parts)


def build_scoreboard(match: gem.ParsedMatch, hero_cell: Callable[[str, int], str]) -> str:
    """Build the scoreboard section."""
    load_hero_icons([p.hero_name for p in match.players if p.hero_name])

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
            f'<h3 style="color:{color};margin-bottom:8px;margin-top:12px">{e(team_name(team))}</h3>'
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
            dust_count = sum(1 for ent in pp.purchase_log if ent.value_name == "item_dust")
            tp_count = sum(1 for ent in pp.purchase_log if ent.value_name == "item_tpscroll")
            smoke_count = sum(
                1 for ent in pp.purchase_log if ent.value_name == "item_smoke_of_deceit"
            )
            parts.append(
                f'<tr class="{row_cls}">'
                f'<td style="white-space:nowrap">{hero_cell(pp.hero_name, team)}</td>'
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


def build_hero_timeseries_chart(match: gem.ParsedMatch) -> str:
    """Two side-by-side line charts: Net Worth and XP per hero over time."""
    players = [p for p in match.players if p.hero_name]
    if not any(p.net_worth_t_min or p.total_earned_xp_t_min for p in players):
        return ""

    times_min: list[int] = []
    for p in players:
        if len(p.times_min) > len(times_min):
            times_min = p.times_min

    n = max((len(p.net_worth_t_min) for p in players), default=0)
    n = max(n, max((len(p.xp_t_min) for p in players), default=0))
    labels: list[str] = []
    for i in range(n):
        if i < len(times_min):
            secs = times_min[i] // TICKS_PER_SEC
            labels.append(f"{secs // 60}")
        else:
            labels.append(str(i))

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
        label = hero(p.hero_name)
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
                "data": list(p.total_earned_xp_t_min),
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


def build_gold_xp_chart(match: gem.ParsedMatch) -> str:
    """Build gold/xp charts section."""
    adv_gold = match.radiant_gold_adv
    adv_xp = match.radiant_xp_adv

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

  var advGold = {adv_gold_js};
  var advXp   = {adv_xp_js};
  var goldPos = advGold.map(function(v) {{ return v > 0 ? v : 0; }});
  var goldNeg = advGold.map(function(v) {{ return v < 0 ? v : 0; }});

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


def _clean_npc(name: str) -> str:
    """Clean an NPC name into a human-readable label."""
    return gem.format_npc_name(name)


def _killer_label(killer: str) -> str:
    """Return display name for a killer NPC (hero or structure/neutral)."""
    if killer.startswith("npc_dota_hero_"):
        return hero(killer)
    return _clean_npc(killer) if killer else "unknown"


def build_objectives(match: gem.ParsedMatch, fmt_tick_fn: Callable[[int], str]) -> str:
    """Build the objectives timeline section."""
    # Build hero_name lookup: player_id → hero display name
    pid_to_hero: dict[int, str] = {
        pp.player_id: hero(pp.hero_name) for pp in match.players if pp.hero_name
    }

    events: list[tuple[int, str, str, str]] = []

    for t in match.towers:
        name = _clean_npc(t.tower_name)
        killer = _killer_label(t.killer)
        desc = (
            f'<span style="color:{TEAM_COLOR_CSS.get(t.team, "#888")};font-weight:bold">'
            f"{e(team_name(t.team))}</span> "
            f"{e(name)} — killed by {e(killer)}"
        )
        events.append((t.tick, "Tower", TEAM_COLOR_CSS.get(t.team, "#888"), desc))

    for b in match.barracks:
        name = _clean_npc(b.barracks_name)
        killer = _killer_label(b.killer)
        desc = (
            f'<span style="color:{TEAM_COLOR_CSS.get(b.team, "#888")};font-weight:bold">'
            f"{e(team_name(b.team))}</span> "
            f"{e(name)} — killed by {e(killer)}"
        )
        events.append((b.tick, "Barracks", TEAM_COLOR_CSS.get(b.team, "#888"), desc))

    for n, r in enumerate(match.roshans, 1):
        killer = _killer_label(r.killer)
        respawn_min = fmt_tick_fn(r.tick + 8 * 30 * 60)
        respawn_max = fmt_tick_fn(r.tick + 11 * 30 * 60)
        drops_str = (", ".join(r.drops).replace("_", " ")) if r.drops else "none"
        desc = (
            f'<span style="color:#ffb74d">Roshan #{n}</span> killed by {e(killer)} '
            f"— drops: {e(drops_str)} "
            f"— respawns {e(respawn_min)}–{e(respawn_max)}"
        )
        events.append((r.tick, f"Roshan #{n}", "#ffb74d", desc))

    for n, tm in enumerate(match.tormentors, 1):
        killer = _killer_label(tm.killer)
        if tm.killer_player_id >= 0:
            hero_name = pid_to_hero.get(tm.killer_player_id, killer)
            killer = hero_name
        desc = f'<span style="color:#ce93d8">Tormentor #{n}</span> killed by {e(killer)}'
        events.append((tm.tick, f"Tormentor #{n}", "#ce93d8", desc))

    for s in match.shrines:
        team_color = TEAM_COLOR_CSS.get(s.team, "#888")
        desc = (
            f'<span style="color:{team_color};font-weight:bold">{e(team_name(s.team))}</span> '
            f"Shrine of Wisdom destroyed"
        )
        events.append((s.tick, "Shrine", team_color, desc))

    # Wisdom rune pickups — rune_type 8 in runes_log
    for pp in match.players:
        team_color = TEAM_COLOR_CSS.get(pp.team, "#888")
        h = hero(pp.hero_name) if pp.hero_name else f"Player {pp.player_id}"
        for entry in pp.runes_log:
            if entry.gold_reason == 8:  # Wisdom rune
                desc = f'<span style="color:{team_color}">{e(h)}</span> picked up Wisdom Rune'
                events.append((entry.tick, "Wisdom Rune", "#80cbc4", desc))

    events.sort(key=lambda ent: ent[0])

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
                f"<td>{e(fmt_tick_fn(tick))}</td>"
                f'<td><span style="color:{color};font-weight:bold">{e(etype)}</span></td>'
                f"<td>{desc}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def build_combat_timeseries_chart(match: gem.ParsedMatch) -> str:
    """Four per-minute line charts: hero damage, healing, deaths, and stuns over time."""
    players = [p for p in match.players if p.hero_name]
    if not any(p.total_hero_damage_t_min for p in players):
        return ""

    times_min: list[int] = []
    for p in players:
        if len(p.times_min) > len(times_min):
            times_min = p.times_min

    n = max((len(p.total_hero_damage_t_min) for p in players), default=0)
    labels: list[str] = []
    for i in range(n):
        if i < len(times_min):
            secs = times_min[i] // TICKS_PER_SEC
            labels.append(f"{secs // 60}")
        else:
            labels.append(str(i))

    radiant_idx = dire_idx = 0
    dmg_datasets: list[dict] = []
    heal_datasets: list[dict] = []
    deaths_datasets: list[dict] = []
    stuns_datasets: list[dict] = []
    for p in players:
        if p.team == 2:
            color = _RADIANT_COLORS[radiant_idx % len(_RADIANT_COLORS)]
            radiant_idx += 1
        else:
            color = _DIRE_COLORS[dire_idx % len(_DIRE_COLORS)]
            dire_idx += 1
        label = hero(p.hero_name)
        base = {
            "label": label,
            "borderColor": color,
            "backgroundColor": "transparent",
            "borderWidth": 2,
            "pointRadius": 0,
            "tension": 0.3,
            "fill": False,
        }

        # Diff the cumulative totals to get per-minute values
        def _per_min(totals: list) -> list:
            if not totals:
                return []
            result = [totals[0]]
            for i in range(1, len(totals)):
                result.append(totals[i] - totals[i - 1])
            return result

        dmg_datasets.append({**base, "data": _per_min(list(p.total_hero_damage_t_min))})
        heal_datasets.append({**base, "data": _per_min(list(p.total_hero_healing_t_min))})
        deaths_datasets.append({**base, "data": _per_min(list(p.total_deaths_t_min))})
        stuns_datasets.append(
            {**base, "data": _per_min([round(v, 2) for v in p.total_stuns_t_min])}
        )

    labels_js = json.dumps(labels)
    dmg_ds_js = json.dumps(dmg_datasets)
    heal_ds_js = json.dumps(heal_datasets)
    deaths_ds_js = json.dumps(deaths_datasets)
    stuns_ds_js = json.dumps(stuns_datasets)

    return f"""
<div class="card">
<details open>
<summary>Combat Timeline (per minute)</summary>
<div class="card-body">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Hero Damage / Minute</div>
    <div class="chart-wrap"><canvas id="combatDmgChart"></canvas></div>
  </div>
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Healing / Minute</div>
    <div class="chart-wrap"><canvas id="combatHealChart"></canvas></div>
  </div>
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Deaths / Minute</div>
    <div class="chart-wrap"><canvas id="combatDeathsChart"></canvas></div>
  </div>
  <div>
    <div style="font-size:0.7rem;color:#8b949e;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em">Stun Duration / Minute (s)</div>
    <div class="chart-wrap"><canvas id="combatStunsChart"></canvas></div>
  </div>
</div>
<script>
(function() {{
  var labels = {labels_js};
  function makeOpts(yTitle, isInt) {{
    return {{
      responsive: true,
      maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ labels: {{ color: '#e6edf3', boxWidth: 12, font: {{ size: 11 }} }} }},
        tooltip: {{
          callbacks: {{
            label: function(c) {{
              var v = isInt ? Math.round(c.parsed.y).toLocaleString() : c.parsed.y.toFixed(1);
              return c.dataset.label + ': ' + v;
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
          beginAtZero: true,
          ticks: {{ color: '#8b949e' }},
          grid: {{ color: '#21262d' }},
          border: {{ color: '#30363d' }},
        }},
      }},
    }};
  }}
  new Chart(document.getElementById('combatDmgChart').getContext('2d'), {{
    type: 'line', data: {{ labels: labels, datasets: {dmg_ds_js} }}, options: makeOpts('Damage', true),
  }});
  new Chart(document.getElementById('combatHealChart').getContext('2d'), {{
    type: 'line', data: {{ labels: labels, datasets: {heal_ds_js} }}, options: makeOpts('Healing', true),
  }});
  new Chart(document.getElementById('combatDeathsChart').getContext('2d'), {{
    type: 'line', data: {{ labels: labels, datasets: {deaths_ds_js} }}, options: makeOpts('Deaths', true),
  }});
  new Chart(document.getElementById('combatStunsChart').getContext('2d'), {{
    type: 'line', data: {{ labels: labels, datasets: {stuns_ds_js} }}, options: makeOpts('Stun (s)', false),
  }});
}})();
</script>
</div>
</details>
</div>"""


def build_damage(match: gem.ParsedMatch, hero_cell: Callable[[str, int], str]) -> str:
    """Build the damage breakdown section."""
    all_dmg = [(p, sum(p.damage.values())) for p in match.players if p.hero_name]
    max_dmg = max((d for _, d in all_dmg), default=1) or 1
    load_hero_icons([p.hero_name for p in match.players if p.hero_name])

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

    for pp, total_dmg in sorted(all_dmg, key=lambda x: -x[1]):
        total_heal = sum(pp.healing.values())
        top_ability = ""
        if pp.ability_uses:
            top_ab = max(pp.ability_uses, key=pp.ability_uses.get)  # type: ignore[arg-type]
            top_ability = f"{e(ability_display(top_ab))} ({pp.ability_uses[top_ab]}x)"

        top3_parts: list[str] = []
        if pp.ability_uses:
            filtered = [
                (k, v)
                for k, v in pp.ability_uses.items()
                if "_passive" not in k and not k.startswith("special_")
            ]
            filtered.sort(key=lambda x: -x[1])
            for ab_key, ab_count in filtered[:3]:
                top3_parts.append(f"{e(ability_display(ab_key))} ({ab_count}x)")
        top3_str = ", ".join(top3_parts)

        total_dmg_taken = sum(pp.damage_taken.values()) if pp.damage_taken else 0
        top_attacker = ""
        if pp.damage_taken:
            top_att_key = max(pp.damage_taken, key=pp.damage_taken.get)  # type: ignore[arg-type]
            top_attacker = f"Most from: {hero(top_att_key)} ({pp.damage_taken[top_att_key]:,})"

        dmg_physical = pp.damage_by_type.get("physical", 0)
        dmg_magical = pp.damage_by_type.get("magical", 0)
        dmg_pure = pp.damage_by_type.get("pure", 0)
        dmg_other = pp.damage_by_type.get("others", 0)
        dmg_known_total = dmg_physical + dmg_magical + dmg_pure

        dmg_type_parts = [
            f"Physical: {dmg_physical:,}",
            f"Magical: {dmg_magical:,}",
            f"Pure: {dmg_pure:,}",
            f"Others: {dmg_other:,}",
        ]
        dmg_type_title = "Damage type split — " + " | ".join(dmg_type_parts)

        dmg_taken_physical = pp.damage_taken_by_type.get("physical", 0)
        dmg_taken_magical = pp.damage_taken_by_type.get("magical", 0)
        dmg_taken_pure = pp.damage_taken_by_type.get("pure", 0)
        dmg_taken_known_total = dmg_taken_physical + dmg_taken_magical + dmg_taken_pure
        dmg_taken_other = max(total_dmg_taken - dmg_taken_known_total, 0)
        dmg_taken_type_parts = [
            f"Physical: {dmg_taken_physical:,}",
            f"Magical: {dmg_taken_magical:,}",
            f"Pure: {dmg_taken_pure:,}",
            f"Others: {dmg_taken_other:,}",
        ]
        dmg_taken_title = (
            f"{top_attacker} | Incoming type split — {' | '.join(dmg_taken_type_parts)}"
        )

        dmg_others = pp.damage_by_type.get("others", 0)
        dmg_bar_total = dmg_known_total + dmg_others or 1

        type_bar_html = ""
        if dmg_bar_total > 0:
            p_pct = 100.0 * dmg_physical / dmg_bar_total
            m_pct = 100.0 * dmg_magical / dmg_bar_total
            u_pct = 100.0 * dmg_pure / dmg_bar_total
            o_pct = max(0.0, 100.0 - p_pct - m_pct - u_pct)
            type_bar_html = (
                '<div class="dmg-type-mini">'
                f'<span class="dmg-type-seg dmg-type-physical" style="width:{p_pct:.2f}%"></span>'
                f'<span class="dmg-type-seg dmg-type-magical" style="width:{m_pct:.2f}%"></span>'
                f'<span class="dmg-type-seg dmg-type-pure" style="width:{u_pct:.2f}%"></span>'
                f'<span class="dmg-type-seg dmg-type-others" style="width:{o_pct:.2f}%"></span>'
                "</div>"
            )

        bar_pct = int(total_dmg / max_dmg * 100)
        team_color = TEAM_COLOR_CSS.get(pp.team, "#888")
        bar_html = (
            f'<div class="dmg-bar-wrap">'
            f'<div class="dmg-bar-fill" style="width:{bar_pct}%;background:{team_color}"></div>'
            f"</div>"
        )
        row_cls = "row-radiant" if pp.team == 2 else "row-dire"
        dmg_taken_cell = f'<td class="r" title="{e(dmg_taken_title)}">{total_dmg_taken:,}</td>'
        hero_dmg_cell = (
            f'<td class="r" title="{e(dmg_type_title)}">'
            f"<div>{total_dmg:,}</div>"
            f"{type_bar_html}"
            "</td>"
        )
        parts.append(
            f'<tr class="{row_cls}">'
            f'<td style="white-space:nowrap">{hero_cell(pp.hero_name, pp.team)}</td>'
            f'<td><span style="color:{team_color}">{e(team_name(pp.team))}</span></td>'
            f"{hero_dmg_cell}"
            f"<td>{top_ability}</td>"
            f"<td>{top3_str}</td>"
            f"{dmg_taken_cell}"
            f'<td class="r">{total_heal:,}</td>'
            f'<td class="r">{pp.stuns_dealt:.1f}</td>'
            f"<td>{bar_html}</td>"
            f"</tr>"
        )
    parts.append("</tbody></table>")
    parts.append(
        '<p class="dmg-legend">'
        '<span class="dmg-legend-swatch dmg-type-physical"></span> Physical &nbsp;'
        '<span class="dmg-legend-swatch dmg-type-magical"></span> Magical &nbsp;'
        '<span class="dmg-legend-swatch dmg-type-pure"></span> Pure &nbsp;'
        '<span class="dmg-legend-swatch dmg-type-others"></span> Others'
        ' <span class="dmg-legend-note">'
        "(Others = damage to non-hero units where type is untracked, e.g. wards, creeps, zombies)"
        "</span>"
        "</p>"
    )
    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def build_kill_feed(match: gem.ParsedMatch, hero_cell: Callable[[str, int], str]) -> str:
    """Build the hero-vs-hero kill feed section."""
    hvh = [
        entry
        for entry in match.combat_log
        if entry.log_type == "DEATH" and entry.attacker_is_hero and entry.target_is_hero
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
        npc_to_team: dict[str, int] = {
            pp.hero_name: pp.team for pp in match.players if pp.hero_name
        }

        all_npcs = {entry.attacker_name for entry in hvh} | {entry.target_name for entry in hvh}
        load_hero_icons([npc for npc in all_npcs if npc.startswith("npc_dota_hero_")])

        load_item_icons(
            [
                entry.inflictor_name.removeprefix("item_")
                for entry in hvh
                if entry.inflictor_name and entry.inflictor_name.startswith("item_")
            ]
        )

        npc_to_player: dict[str, gem.ParsedPlayer] = {
            pp.hero_name: pp for pp in match.players if pp.hero_name
        }

        parts.append(
            f'<p style="margin-bottom:8px;color:#8b949e">Total hero kills: <strong style="color:#e6edf3">{len(hvh)}</strong></p>'
        )
        parts.append("<table>")
        parts.append(
            "<thead><tr><th>Time</th><th>Killer</th><th>Victim</th><th>Via</th><th>Vision</th></tr></thead>"
        )
        parts.append("<tbody>")
        for entry in hvh:
            attacker_team = npc_to_team.get(entry.attacker_name, 0)
            target_team = npc_to_team.get(entry.target_name, 0)
            killer_cell = hero_cell(entry.attacker_name, attacker_team)
            victim_cell = hero_cell(entry.target_name, target_team)

            if entry.inflictor_name:
                if entry.inflictor_name.startswith("item_"):
                    via = item_icon_tag(entry.inflictor_name, 16) + e(
                        ability_display(entry.inflictor_name)
                    )
                else:
                    via = e(ability_display(entry.inflictor_name))
            else:
                via = '<span style="color:#6e7681">auto-attack</span>'

            # Vision badge: was the victim visible to the killer's team at death?
            vision_badge = ""
            if attacker_team in (2, 3):
                victim_player = npc_to_player.get(entry.target_name)
                if victim_player:
                    pos = gem.position_at_tick(victim_player, entry.tick)
                    if pos:
                        sources = gem.estimate_vision(
                            match, attacker_team, entry.tick, pos[0], pos[1]
                        )
                        if not sources:
                            vision_badge = (
                                '<span style="background:#21262d;border:1px solid #30363d;'
                                "border-radius:10px;padding:1px 7px;font-size:11px;"
                                'color:#6e7681;white-space:nowrap">🌫 blind</span>'
                            )

            parts.append(
                f"<tr>"
                f'<td style="color:#8b949e">{e(fmt_tick(entry.tick))}</td>'
                f"<td>{killer_cell}</td>"
                f"<td>{victim_cell}</td>"
                f"<td>{via}</td>"
                f"<td>{vision_badge}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def build_purchases(match: gem.ParsedMatch) -> str:
    """Build the purchase timeline section."""
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
            hero_display = e(hero(pp.hero_name))
            team_display = e(team_name(pp.team))
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
            for entry in sorted(pp.purchase_log, key=lambda ent: ent.tick):
                display_name = (
                    e(item_display(entry.value_name))
                    if entry.value_name
                    else e(entry.value_name or "")
                )
                icon = item_icon_tag(entry.value_name or "", 20) if entry.value_name else ""
                parts.append(
                    f"<tr><td>{e(fmt_tick(entry.tick))}</td><td>{icon}{display_name}</td></tr>"
                )
            parts.append("</tbody></table>")
            parts.append("</details>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _net_worth_at(pp: gem.ParsedPlayer, tick: int) -> int:
    """Return the closest sampled net worth for a player at the given tick."""
    return gem.net_worth_at(pp, tick)


def build_buybacks(match: gem.ParsedMatch) -> str:
    """Build the buybacks section."""
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
        parts.append(
            "<thead><tr><th>Time</th><th>Hero</th><th>Team</th><th>Gold Spent</th></tr></thead>"
        )
        parts.append("<tbody>")
        entries: list[tuple[int, str, int, int]] = []
        for pp in match.players:
            for entry in pp.buyback_log:
                nw = _net_worth_at(pp, entry.tick)
                cost = 200 + nw // 13
                entries.append((entry.tick, pp.hero_name, pp.team, cost))
        entries.sort(key=lambda x: x[0])
        for tick, hero_name, team, cost in entries:
            team_color = TEAM_COLOR_CSS.get(team, "#888")
            parts.append(
                f"<tr>"
                f"<td>{e(fmt_tick(tick))}</td>"
                f"<td>{e(hero(hero_name))}</td>"
                f'<td><span style="color:{team_color}">{e(team_name(team))}</span></td>'
                f'<td class="r">{cost:,}g</td>'
                f"</tr>"
            )
        parts.append("</tbody></table>")
        parts.append(f'<p class="section-note">Total buybacks: {total}</p>')

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def build_runes(match: gem.ParsedMatch, hero_cell: Callable[[str, int], str]) -> str:
    """Build the rune pickups section."""
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
        load_item_icons(list(RUNE_ICON_SHORT.values()))
        all_hero_npcs = [pp.hero_name for pp in match.players if pp.hero_name]
        load_hero_icons(all_hero_npcs)

        parts.append("<table>")
        parts.append("<thead><tr><th>Time</th><th>Hero</th><th>Team</th><th>Rune</th></tr></thead>")
        parts.append("<tbody>")
        entries: list[tuple[int, str, int, int]] = []
        for pp in match.players:
            for entry in pp.runes_log:
                entries.append((entry.tick, pp.hero_name, pp.team, entry.gold_reason))
        entries.sort(key=lambda x: x[0])
        for tick, hero_name, team, rune_type in entries:
            rune_name = RUNE_NAMES.get(rune_type, f"Rune {rune_type}")
            icon_short = RUNE_ICON_SHORT.get(rune_type, "")
            rune_icon = item_icon_tag(icon_short, 18) if icon_short else ""
            team_color = TEAM_COLOR_CSS.get(team, "#888")
            parts.append(
                f"<tr>"
                f'<td style="color:#8b949e">{e(fmt_tick(tick))}</td>'
                f"<td>{hero_cell(hero_name, team)}</td>"
                f'<td><span style="color:{team_color}">{e(team_name(team))}</span></td>'
                f"<td>{rune_icon}{e(rune_name)}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def build_wards(match: gem.ParsedMatch, map_b64: str | None) -> str:
    """Build the ward map section (playback + hover + vision radius)."""
    _e = e
    _fmt_tick = fmt_tick
    _hero = hero
    _team_name = team_name
    _item_icon_tag = item_icon_tag

    _XMIN, _XMAX = MAP_XMIN, MAP_XMAX
    _YMIN, _YMAX = MAP_YMIN, MAP_YMAX

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

    max_tick = max(
        (w.killed_tick or w.expires_tick or w.tick for w in match.wards),
        default=0,
    )
    slider_max = max(max_tick, match.game_end_tick or max_tick)
    _PREGAME_TICKS = 90 * TICKS_PER_SEC
    slider_min = (match.game_start_tick or 0) - _PREGAME_TICKS

    ward_data = []
    for w in match.wards:
        if w.x is None or w.y is None:
            continue
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
                "type": w.ward_type,
                "team": w.team,
                "placed": w.tick,
                "removed": w.killed_tick or w.expires_tick,
                "placer": _hero(w.placer),
                "fate": fate,
                "fate_time": fate_time,
                "placed_fmt": _fmt_tick(w.tick),
            }
        )

    wards_js = json.dumps(ward_data)

    _SMOKE_SHOW_TICKS = 300
    smoke_data = []
    for s in match.smoke_events:
        if s.x is None or s.y is None:
            continue
        fx = (s.x - _XMIN) / (_XMAX - _XMIN)
        fy = 1.0 - (s.y - _YMIN) / (_YMAX - _YMIN)
        enemy_team = 3 if s.team == 2 else 2
        seen_by_enemy = bool(gem.estimate_vision(match, enemy_team, s.tick, s.x, s.y))
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
                "seen": seen_by_enemy,
            }
        )
    smokes_js = json.dumps(smoke_data)

    img_src_js = "window._GEM_MAP_SRC||''" if map_b64 else "''"

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
var imgSrc = {img_src_js};
  var iconObsSrc = {json.dumps(ITEM_ICON_B64.get("ward_observer", ""))};
  var iconSenSrc = {json.dumps(ITEM_ICON_B64.get("ward_sentry", ""))};
  var iconSmokeSrc = {json.dumps(ITEM_ICON_B64.get("smoke_of_deceit", ""))};
  var gameStartTick = {match.game_start_tick or 0};
  var sliderMin = {slider_min};
  var sliderMax = {slider_max};
  var WORLD_WIDTH = {_XMAX - _XMIN};
  var OBS_VISION_RADIUS = 1600;
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

  var mapImg = new Image();
  mapImg.onload = function() {{ draw(currentTick); }};
  if (imgSrc) {{ mapImg.src = imgSrc; }}

  function _makeIcon(src) {{
    var img = new Image();
    if (src) img.src = src;
    return img;
  }}
  var iconObs = _makeIcon(iconObsSrc);
  var iconSen = _makeIcon(iconSenSrc);
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

    if (mapImg.complete && mapImg.naturalWidth > 0) {{
      ctx.drawImage(mapImg, 0, 0, W, H);
    }} else {{
      ctx.fillStyle = '#1a2a1a';
      ctx.fillRect(0, 0, W, H);
    }}


    function drawIcon(img, cx, cy, size, borderColor, alpha) {{
      var half = size / 2;
      ctx.save();
      ctx.globalAlpha = alpha !== undefined ? alpha : 1.0;
      if (img && img.complete && img.naturalWidth > 0) {{
        ctx.beginPath();
        ctx.roundRect(cx - half, cy - half, size, size, 3);
        ctx.clip();
        ctx.drawImage(img, cx - half, cy - half, size, size);
        ctx.restore();
        ctx.save();
        ctx.globalAlpha = alpha !== undefined ? alpha : 1.0;
        ctx.beginPath();
        ctx.roundRect(cx - half, cy - half, size, size, 3);
        ctx.lineWidth = 2;
        ctx.strokeStyle = borderColor;
        ctx.stroke();
      }} else {{
        ctx.beginPath();
        ctx.arc(cx, cy, half, 0, 2 * Math.PI);
        ctx.fillStyle = borderColor;
        ctx.fill();
      }}
      ctx.restore();
    }}

    for (var i = 0; i < wards.length; i++) {{
      var w = wards[i];
      if (tick < w.placed) continue;
      if (w.removed !== null && tick > w.removed) continue;

      var cx = w.fx * W;
      var cy = w.fy * H;
      var isObs = w.type === 'observer';
      var icon = isObs ? iconObs : iconSen;
      var borderColor = isObs ? '#ff9800' : '#2196f3';

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

    for (var i = 0; i < smokes.length; i++) {{
      var s = smokes[i];
      if (tick < s.tick || tick > s.end_tick) continue;

      var cx = s.fx * W;
      var cy = s.fy * H;
      var borderColor = s.team === 2 ? '#4caf50' : '#f44336';
      var age = (tick - s.tick) / (s.end_tick - s.tick);
      var alpha = 1.0 - age * 0.6;
      drawIcon(iconSmoke, cx, cy, 20, borderColor, alpha);

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
      var dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < bestDist) {{ bestDist = dist; hit = w; hitType = 'ward'; }}
    }}
    for (var i = 0; i < smokes.length; i++) {{
      var s = smokes[i];
      if (currentTick < s.tick || currentTick > s.end_tick) continue;
      var dx = s.fx * W - mx, dy = s.fy * H - my;
      var dist = Math.sqrt(dx * dx + dy * dy);
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
      var seenStr = hit.seen
        ? '<span style="color:#f44336">&#128065; Enemy had vision &#10003;</span>'
        : '<span style="color:#4caf50">&#10008; Undetected</span>';
      tooltip.innerHTML =
        '<strong style="color:#9c27b0">Smoke of Deceit</strong> &mdash; ' +
        '<span style="color:' + teamColor + '">' + teamName + '</span><br>' +
        'Activated: ' + hit.tick_fmt + ' by ' + hit.activator + '<br>' +
        hit.count + ' hero' + (hit.count !== 1 ? 'es' : '') + ' smoked<br>' +
        seenStr;
      canvas.style.cursor = 'pointer';
    }} else {{
      tooltip.innerHTML = '';
      canvas.style.cursor = 'crosshair';
    }}
  }});
}})();
</script>"""

    parts.append(canvas_html)

    parts.append(
        '<details style="margin-top:8px"><summary style="color:#8b949e;font-size:12px;cursor:pointer">Show full ward table</summary>'
    )
    parts.append('<table style="margin-top:8px">')
    parts.append(
        "<thead><tr>"
        "<th>Time</th><th>Type</th><th>Hero</th><th>Team</th>"
        '<th>Coords</th><th>Fate</th><th class="r">Enemies seen</th>'
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
            killer = _hero(getattr(w, "killer", "")) if getattr(w, "killer", None) else "?"
            fate = f'<span style="color:#f44336">Killed {_e(_fmt_tick(w.killed_tick))} by {_e(killer)}</span>'
        elif w.expires_tick is not None:
            fate = f'<span style="color:#8b949e">Expired {_e(_fmt_tick(w.expires_tick))}</span>'
        else:
            fate = '<span style="color:#ffb74d">Active / unknown</span>'
        team_color = TEAM_COLOR_CSS.get(w.team, "#888")
        if w.ward_type == "observer":
            enemies_seen = _ward_enemies_seen(w, match)
            seen_cell = f'<td class="r">{enemies_seen}</td>'
        else:
            seen_cell = '<td class="r" style="color:#6e7681">—</td>'
        parts.append(
            f"<tr>"
            f"<td>{_e(_fmt_tick(w.tick))}</td>"
            f"<td>{type_label}</td>"
            f"<td>{_e(_hero(w.placer))}</td>"
            f'<td><span style="color:{team_color}">{_e(_team_name(w.team))}</span></td>'
            f'<td style="font-variant-numeric:tabular-nums">{_e(coords)}</td>'
            f"<td>{fate}</td>"
            f"{seen_cell}"
            f"</tr>"
        )
    parts.append("</tbody></table></details>")

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


def _hero_cell(npc_name: str, team: int = 0) -> str:
    """Return an icon + name cell fragment for a hero NPC name."""
    src = hero_icon_src(npc_name)
    name = e(hero(npc_name))
    color = TEAM_COLOR_CSS.get(team, "#e6edf3")
    return (
        f'<img src="{src}" width="20" height="12" '
        f'style="object-fit:cover;border-radius:2px;vertical-align:middle;margin-right:5px">'
        f'<span style="color:{color}">{name}</span>'
    )


def _is_active_teamfight_player(p: object) -> bool:
    """Return True for active teamfight participants only."""
    return gem.is_active_teamfight_participant(p)


def _top_abilities_teamfight(ability_uses: dict[str, int], n: int = 3) -> str:
    """Format top abilities used in one teamfight row."""
    if not ability_uses:
        return '<span class="dim">—</span>'
    top = sorted(ability_uses.items(), key=lambda x: x[1], reverse=True)[:n]
    return " · ".join(f"{e(ability_display(a))} ×{c}" for a, c in top)


def _fight_combat_log_html(
    fight_start: int,
    fight_end: int,
    combat_log: list,
    slot_to_player: dict,
    h2s: dict[str, int],
    active_slots: list[int],
) -> str:
    """Build a chronological combat log for one teamfight window.

    Only includes events where at least one of the attacker or target is an
    active participant in this fight (as determined by ``active_slots``).
    Creep/neutral-only events and heroes not involved in this fight are skipped.

    Args:
        fight_start: Window start tick.
        fight_end: Window end tick.
        combat_log: Full match combat log (all CombatLogEntry objects).
        slot_to_player: Mapping of player slot → ParsedPlayer.
        h2s: Mapping of hero NPC name → player slot.
        active_slots: Player slots of active participants in this fight.

    Returns:
        HTML string for the combat log expander, or empty string if no events.
    """
    active_set = set(active_slots)
    _RADIANT = "#4caf50"
    _DIRE = "#f44336"
    _NEUTRAL = "#8b949e"
    _ABILITY_COLOR = "#58a6ff"
    _ITEM_COLOR = "#e3b341"
    _HEAL_COLOR = "#4caf50"
    _DEATH_COLOR = "#f44336"

    def _hero_span(npc_name: str) -> str:
        pp = slot_to_player.get(h2s.get(npc_name, -1))
        color = _RADIANT if pp and pp.team == 2 else _DIRE if pp and pp.team == 3 else _NEUTRAL
        short = e(hero(npc_name)) if npc_name else "?"
        return f'<span style="color:{color};font-weight:600">{short}</span>'

    # Split window entries into two streams:
    # 1. Hero-vs-hero DAMAGE with a named inflictor → group into AbilityCast records
    # 2. Everything else → render individually as before
    window_entries = sorted(
        (en for en in combat_log if fight_start <= en.tick <= fight_end),
        key=lambda en: en.tick,
    )

    groupable = [
        en
        for en in window_entries
        if (
            en.log_type == "DAMAGE"
            and en.attacker_is_hero
            and en.target_is_hero
            and en.inflictor_name
            and not en.attacker_is_illusion
            and not en.target_is_illusion
            and (h2s.get(en.attacker_name) in active_set or h2s.get(en.target_name) in active_set)
        )
    ]
    casts = gem.group_ability_hits(groupable)
    # Build a set of entry ids that were absorbed into grouped casts (to skip in the loop)
    grouped_entry_ids: set[int] = {id(en) for cast in casts for en in cast.entries}

    # Produce (tick, html_line) pairs for cast records
    cast_lines: list[tuple[int, str]] = []
    for cast in casts:
        atk = cast.caster
        inf = cast.ability
        n_targets = len(cast.targets)
        total = cast.total_damage
        dmg_type = cast.damage_type
        dmg_type_str = f" ({e(dmg_type)})" if dmg_type and dmg_type != "others" else ""
        if n_targets == 1:
            tgt_str = f"→ {_hero_span(cast.targets[0])}"
        else:
            hero_names = ", ".join(_hero_span(t) for t in cast.targets)
            tgt_str = f"→ {hero_names} ({n_targets} heroes)"
        line = (
            f"{_hero_span(atk)} casts "
            f'<span style="color:#58a6ff;font-weight:600">{e(ability_display(inf))}</span> '
            f"{tgt_str} for "
            f'<span style="color:#e6edf3;font-weight:600">{total:,}</span>'
            f"{dmg_type_str} dmg"
        )
        tick_str = e(fmt_tick(cast.tick))
        cast_lines.append(
            (
                cast.tick,
                f'<div class="tf-log-line"><span class="tf-log-time">{tick_str}</span>'
                f'<span class="tf-log-text">{line}</span></div>',
            )
        )

    lines = []
    entries = window_entries

    for en in entries:
        log_type = en.log_type
        atk = en.attacker_name
        tgt = en.target_name
        inf = en.inflictor_name
        val = en.value

        # Skip non-hero attacker AND non-hero target events (pure creep/neutral noise)
        if not en.attacker_is_hero and not en.target_is_hero:
            continue
        # Skip illusions as attacker or target for clarity
        if en.attacker_is_illusion or en.target_is_illusion:
            continue
        # Skip events where neither attacker nor target is an active participant
        atk_slot = h2s.get(en.attacker_name)
        tgt_slot = h2s.get(en.target_name)
        if atk_slot not in active_set and tgt_slot not in active_set:
            continue
        # Skip hero-vs-hero DAMAGE with inflictor — these are rendered as grouped cast rows
        if id(en) in grouped_entry_ids:
            continue

        tick_str = e(fmt_tick(en.tick))

        if log_type == "DAMAGE" and en.attacker_is_hero and en.target_is_hero:
            # Hero-vs-hero DAMAGE without an inflictor (right-click auto-attacks)
            dmg_type = (
                f" ({e(en.damage_type)})" if en.damage_type and en.damage_type != "others" else ""
            )
            line = (
                f"{_hero_span(atk)} attacks "
                f"{_hero_span(tgt)} for "
                f'<span style="color:#e6edf3;font-weight:600">{val:,}</span>'
                f"{dmg_type} dmg"
            )
            css = ""

        elif log_type == "DAMAGE" and en.target_is_hero and not en.attacker_is_hero:
            # Non-hero source hitting a hero (tower, creep, neutral)
            src_label = e(atk.replace("npc_dota_", "").replace("_", " ")) if atk else "unknown"
            line = (
                f"{_hero_span(tgt)} takes "
                f'<span style="color:#e6edf3">{val:,}</span> dmg '
                f'from <span style="color:{_NEUTRAL}">{src_label}</span>'
            )
            css = f"color:{_NEUTRAL}"

        elif log_type == "DEATH" and en.target_is_hero:
            killer = (
                _hero_span(atk)
                if en.attacker_is_hero and atk
                else (
                    f'<span style="color:{_NEUTRAL}">'
                    f"{e(atk.replace('npc_dota_', '').replace('_', ' ')) if atk else 'unknown'}"
                    f"</span>"
                )
            )
            line = f"☠ {_hero_span(tgt)} dies — killed by {killer}"
            css = f"color:{_DEATH_COLOR}"

        elif log_type == "ABILITY" and en.attacker_is_hero and inf:
            tgt_part = f" on {_hero_span(tgt)}" if tgt and en.target_is_hero else ""
            line = (
                f"{_hero_span(atk)} uses "
                f'<span style="color:{_ABILITY_COLOR};font-weight:600">'
                f"{e(ability_display(inf))}</span>{tgt_part}"
            )
            css = ""

        elif log_type == "ITEM" and en.attacker_is_hero and inf:
            tgt_part = f" on {_hero_span(tgt)}" if tgt and en.target_is_hero else ""
            line = (
                f"{_hero_span(atk)} uses "
                f'<span style="color:{_ITEM_COLOR};font-weight:600">'
                f"{e(item_display(inf))}</span>{tgt_part}"
            )
            css = ""

        elif log_type == "HEAL" and en.attacker_is_hero and en.target_is_hero and atk != tgt:
            via = f" via <em>{e(ability_display(inf))}</em>" if inf else ""
            line = (
                f"{_hero_span(atk)} heals {_hero_span(tgt)} for "
                f'<span style="color:{_HEAL_COLOR};font-weight:600">{val:,}</span>{via}'
            )
            css = f"color:{_HEAL_COLOR}"

        else:
            continue

        style = f' style="{css}"' if css else ""
        lines.append(
            (
                en.tick,
                f'<div class="tf-log-line"{style}>'
                f'<span class="tf-log-time">{tick_str}</span>'
                f'<span class="tf-log-text">{line}</span>'
                f"</div>",
            )
        )

    # Merge cast lines and individual lines, sorted by tick
    all_lines = sorted(cast_lines + lines, key=lambda t: t[0])
    if not all_lines:
        return ""

    return (
        '<details class="tf-log-expander">'
        "<summary>Combat log</summary>"
        '<div class="tf-log-body">' + "\n".join(html for _, html in all_lines) + "</div></details>"
    )


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
    _XMIN, _XMAX = MAP_XMIN, MAP_XMAX
    _YMIN, _YMAX = MAP_YMIN, MAP_YMAX

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
        src = hero_icon_src(pp.hero_name)

        hero_elements.append(
            f'<defs><clipPath id="{clip_id}"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}"/></clipPath></defs>'
            f'<image href="{src}" x="{cx - icon_r:.1f}" y="{cy - icon_r:.1f}" '
            f'width="{icon_r * 2}" height="{icon_r * 2}" clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}" fill="none" stroke="{stroke}" stroke-width="{stroke_w}"/>'
        )

    bg_img = (
        f'<image class="gem-map-bg" href="" x="0" y="0" width="{size}" height="{size}" '
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


def _ward_enemies_seen(ward: object, match: gem.ParsedMatch) -> int:
    """Count distinct enemy heroes that passed within observer ward vision radius."""
    return gem.ward_vision_impact(ward, match)


# Friendly labels for tracked vision modifier names
_MODIFIER_DISPLAY: dict[str, str] = {
    "modifier_slardar_amplify_damage": "Corrosive Haze",
    "modifier_bounty_hunter_track": "Track",
    "modifier_item_dustofappearance": "Dust of Appearance",
    "modifier_item_gem_of_true_sight": "Gem of True Sight",
    "modifier_gem_active_truesight": "Gem of True Sight",
}


def _fight_reveals_html(
    start_tick: int,
    end_tick: int,
    match: gem.ParsedMatch,
) -> str:
    """Return HTML for active vision-modifier reveals during a fight window.

    Collects all VisionModifierEvents whose window overlaps [start_tick, end_tick],
    de-duplicates by (modifier_name, target_name), and renders a compact badge row.
    Returns empty string if no modifiers were active.
    """
    if not match.vision_modifiers:
        return ""

    # Collect modifiers that overlap the fight window
    # Only show hero targets (skip neutrals/creep-heroes)
    active: list[gem.VisionModifierEvent] = []
    seen: set[tuple[str, str]] = set()
    for ev in match.vision_modifiers:
        if ev.tick > end_tick:
            continue
        if ev.end_tick is not None and ev.end_tick < start_tick:
            continue
        if not ev.target_name.startswith("npc_dota_hero_"):
            continue
        key = (ev.modifier_name, ev.target_name)
        if key in seen:
            continue
        seen.add(key)
        active.append(ev)

    if not active:
        return ""

    # Group by caster team so Radiant reveals and Dire reveals are separate
    rows: list[str] = []
    for team_num, team_label, team_color in (
        (2, "Radiant", "#4caf50"),
        (3, "Dire", "#f44336"),
    ):
        team_evs = [ev for ev in active if ev.caster_team == team_num]
        if not team_evs:
            continue
        badges: list[str] = []
        for ev in team_evs:
            mod_label = _MODIFIER_DISPLAY.get(ev.modifier_name, ev.modifier_name)
            target_display = e(hero(ev.target_name))
            target_color = "#f44336" if team_num == 2 else "#4caf50"  # target is enemy
            src = hero_icon_src(ev.target_name)
            badge = (
                f'<span style="display:inline-flex;align-items:center;gap:4px;'
                f"background:#21262d;border:1px solid #30363d;border-radius:4px;"
                f'padding:2px 6px;font-size:11px;white-space:nowrap">'
                f'<span style="color:#8b949e">{e(mod_label)}</span>'
                f'<span style="color:#8b949e">→</span>'
                f'<img src="{src}" width="16" height="10" '
                f'style="object-fit:cover;border-radius:2px;vertical-align:middle">'
                f'<span style="color:{target_color}">{target_display}</span>'
                f"</span>"
            )
            badges.append(badge)
        row = (
            f'<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:4px">'
            f'<span style="color:{team_color};font-size:11px;font-weight:600;'
            f'min-width:52px">{e(team_label)}</span>' + "".join(badges) + "</div>"
        )
        rows.append(row)

    return (
        '<details style="margin-top:8px">'
        '<summary style="color:#8b949e;font-size:12px;cursor:pointer">'
        f"&#128065; Active reveals during fight ({len(active)})"
        "</summary>"
        '<div style="margin-top:6px;padding:6px 8px;background:#161b22;'
        'border:1px solid #30363d;border-radius:6px">' + "\n".join(rows) + "</div></details>"
    )


def build_teamfights(match: gem.ParsedMatch, map_b64: str | None) -> str:
    """Build the Teamfights tab content (filters + fight cards)."""
    fights = match.teamfights or []
    if not fights:
        return (
            '<div class="card"><details open><summary>Fights</summary>'
            '<div class="card-body"><p class="dim">(no fights detected)</p></div>'
            "</details></div>"
        )

    slot_to_player: dict[int, gem.ParsedPlayer] = {pp.player_id: pp for pp in match.players}
    h2s: dict[str, int] = {pp.hero_name: pp.player_id for pp in match.players if pp.hero_name}
    load_hero_icons([pp.hero_name for pp in match.players if pp.hero_name])

    max_deaths = max((tf.deaths for tf in fights), default=1)
    max_participants = max(
        (sum(1 for p in tf.players if _is_active_teamfight_player(p)) for tf in fights),
        default=1,
    )

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Fights</summary>",
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
            f'<span class="tf-fight-time">{e(fmt_tick(tf.start_tick))} → {e(fmt_tick(tf.end_tick))}</span>'
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
                pname = e(pp.player_name or "")
                hname = e(hero(pp.hero_name))
                src = hero_icon_src(pp.hero_name)
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
                    f'<div style="color:#8b949e;font-size:11px">{e(pp.player_name or "")}</div></td>'
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

        log_html = _fight_combat_log_html(
            tf.start_tick,
            tf.end_tick,
            match.combat_log or [],
            slot_to_player,
            h2s,
            active_slots,
        )
        if log_html:
            parts.append(log_html)

        reveals_html = _fight_reveals_html(tf.start_tick, tf.end_tick, match)
        if reveals_html:
            parts.append(reveals_html)

        parts.append("</div></div></div>")

    parts.append(
        '<div id="tf-no-results" class="dim" style="display:none;padding:12px 0">(no fights match current filters)</div>'
    )
    parts.append("</div></details></div>")
    return "\n".join(parts)


def build_draft(match: gem.ParsedMatch) -> str:
    """Build the draft section."""
    if not match.draft:
        return ""

    sorted_draft = sorted(match.draft, key=lambda d: d.tick)

    hero_to_player: dict[str, gem.ParsedPlayer] = {
        pp.hero_name: pp for pp in match.players if pp.hero_name
    }

    def _pick_team(event: object) -> int:
        from gem.extractors.draft import DraftEvent, resolve_pick_team

        if isinstance(event, DraftEvent):
            return resolve_pick_team(event, match.players)
        return 2

    load_hero_icons([ev.hero_name for ev in sorted_draft if ev.hero_name])

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Draft</summary>",
        '<div class="card-body">',
    ]

    parts.append(
        '<div style="font-size:0.75rem;font-weight:700;letter-spacing:0.08em;'
        'text-transform:uppercase;color:#8b949e;margin-bottom:10px">Pick / Ban sequence</div>'
    )
    parts.append('<div class="draft-sequence">')
    for i, ev in enumerate(sorted_draft, 1):
        name = hero_display(ev.hero_name) if ev.hero_name else f"ID {ev.hero_id}"
        src = hero_icon_src(ev.hero_name) if ev.hero_name else HERO_PLACEHOLDER_B64
        time_str = fmt_tick(ev.tick) if ev.tick else ""
        team = _pick_team(ev)
        if not ev.is_pick:
            css_cls = "dc-ban-radiant" if team == 2 else "dc-ban-dire"
        else:
            css_cls = "dc-pick-radiant" if team == 2 else "dc-pick-dire"
        type_label = "PICK" if ev.is_pick else "BAN"
        parts.append(
            f'<div class="draft-cell {css_cls}" title="#{i} {type_label}: {e(name)}">'
            f'<span class="dc-seq">#{i}</span>'
            f'<span class="dc-type-badge">{type_label}</span>'
            f'<img src="{src}" alt="{e(name)}">'
            f'<div class="dc-name">{e(name)}</div>'
            f'<div class="dc-time">{e(time_str)}</div>'
            f"</div>"
        )
    parts.append("</div>")

    picks = [ev for ev in sorted_draft if ev.is_pick]
    radiant_picks = [ev for ev in picks if _pick_team(ev) == 2]
    dire_picks = [ev for ev in picks if _pick_team(ev) == 3]

    def _picks_row(events: list, team_num: int) -> str:
        if not events:
            return ""
        label_cls = "radiant" if team_num == 2 else "dire"
        label_txt = "Radiant" if team_num == 2 else "Dire"
        cards = []
        for ev in events:
            name = hero_display(ev.hero_name) if ev.hero_name else f"ID {ev.hero_id}"
            src = hero_icon_src(ev.hero_name) if ev.hero_name else HERO_PLACEHOLDER_B64
            pp = hero_to_player.get(ev.hero_name)
            player_name = pp.player_name if pp and pp.player_name else ""
            time_str = fmt_tick(ev.tick) if ev.tick else ""
            player_html = f'<div class="dp-player">{e(player_name)}</div>' if player_name else ""
            cards.append(
                f'<div class="draft-pick-card {label_cls}">'
                f'<img src="{src}" alt="{e(name)}">'
                f'<div class="dp-name">{e(name)}</div>'
                f"{player_html}"
                f'<div class="dp-time">{e(time_str)}</div>'
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


def build_chat(match: gem.ParsedMatch) -> str:
    """Build the chat log section."""
    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Chat Log</summary>",
        '<div class="card-body">',
    ]

    if not match.chat:
        parts.append('<p class="dim">(no chat messages recorded)</p>')
    else:
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
                f"<td>{e(fmt_tick(msg.tick))}</td>"
                f'<td><span style="color:{team_color}">{e(hero(hero_name))}</span></td>'
                f'<td><span style="color:{channel_color};font-weight:bold">{e(channel_label)}</span></td>'
                f"<td>{e(msg.text)}</td>"
                f"</tr>"
            )
        parts.append("</tbody></table>")
        parts.append(f'<p class="section-note">Total messages: {len(match.chat)}</p>')

    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Lane role constants (mirroring gem.extractors.lane)
# ---------------------------------------------------------------------------

_LANE_ROLE_NAMES: dict[int, str] = {
    1: "Safe",
    2: "Mid",
    3: "Off",
    4: "Jungle",
    5: "Roaming",
    0: "—",
}

# Colours for lane zone rings on the minimap SVG
_LANE_COLORS: dict[int, str] = {
    1: "#4caf50",
    2: "#58a6ff",
    3: "#f44336",
    4: "#ff9800",
    5: "#ab47bc",
}

# Per-slot dot colours matching movement.py _SLOT_COLORS
_SLOT_COLORS_LANE: list[str] = [
    "#29b6f6",
    "#0288d1",
    "#26c6da",
    "#66bb6a",
    "#9ccc65",
    "#ef5350",
    "#ff7043",
    "#ffca28",
    "#ab47bc",
    "#ec407a",
]


def _laning_minimap_svg(
    match: gem.ParsedMatch,
    map_b64: str | None,
    size: int = 320,
) -> str:
    """Render a minimap SVG with each hero's dwell-weighted 10-min centroid."""
    _XMIN, _XMAX = MAP_XMIN, MAP_XMAX
    _YMIN, _YMAX = MAP_YMIN, MAP_YMAX
    _GRID = 64

    def _world_to_px(wx: float, wy: float) -> tuple[float, float]:
        px = (wx - _XMIN) / (_XMAX - _XMIN) * size
        py = (1.0 - (wy - _YMIN) / (_YMAX - _YMIN)) * size
        return px, py

    bg_img = (
        f'<image class="gem-map-bg" href="" x="0" y="0" '
        f'width="{size}" height="{size}" preserveAspectRatio="xMidYMid slice"/>'
        if map_b64
        else f'<rect width="{size}" height="{size}" fill="#0d1117"/>'
    )

    elements: list[str] = [bg_img]
    icon_r = 13

    for pp in match.players:
        if not pp.lane_pos or not pp.hero_name:
            continue
        total = sum(pp.lane_pos.values())
        if not total:
            continue
        wx_sum = wy_sum = 0.0
        for key, cnt in pp.lane_pos.items():
            gx_s, gy_s = key.split("_", 1)
            wx_sum += (int(gx_s) * _GRID + _GRID // 2) * cnt
            wy_sum += (int(gy_s) * _GRID + _GRID // 2) * cnt
        cx, cy = _world_to_px(wx_sum / total, wy_sum / total)

        slot = pp.player_id
        ring_color = _LANE_COLORS.get(pp.lane_role, "#8b949e")
        clip_id = f"lane_clip_{slot}"
        src = hero_icon_src(pp.hero_name)
        role_label = _LANE_ROLE_NAMES.get(pp.lane_role, "—")

        elements.append(
            f'<defs><clipPath id="{clip_id}">'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}"/>'
            f"</clipPath></defs>"
            f'<image href="{src}" x="{cx - icon_r:.1f}" y="{cy - icon_r:.1f}" '
            f'width="{icon_r * 2}" height="{icon_r * 2}" '
            f'clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}" fill="none" '
            f'stroke="{ring_color}" stroke-width="2.5"/>'
            f"<title>{e(hero(pp.hero_name))} ({role_label})</title>"
        )

    return (
        f'<svg class="lane-map-svg" width="{size}" height="{size}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'style="border-radius:8px;overflow:hidden;border:1px solid #30363d">'
        + "".join(elements)
        + "</svg>"
    )


def build_laning(match: gem.ParsedMatch, map_b64: str | None = None) -> str:
    """Build the Laning tab: minimap + per-player 10-minute metrics table.

    Shows inferred lane role, last hits / denies / gold / XP at 10 minutes,
    Tier-1 lane efficiency % (OpenDota formula: gold@10 ÷ 4948), and
    Tier-2 gold/XP advantage versus opposing lane opponents.

    Args:
        match: Parsed match data from ``gem.parse()``.
        map_b64: Optional base64-encoded map JPEG for the minimap background.

    Returns:
        HTML string for the Laning tab content.
    """
    load_hero_icons([pp.hero_name for pp in match.players if pp.hero_name])

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Laning Phase</summary>",
        '<div class="card-body">',
    ]

    # Minimap + legend
    svg = _laning_minimap_svg(match, map_b64)
    legend_items = "".join(
        f'<div class="lane-legend-item">'
        f'<span class="lane-dot" style="background:{_LANE_COLORS[role]}"></span>'
        f"<span>{name}</span>"
        f"</div>"
        for role, name in _LANE_ROLE_NAMES.items()
        if role != 0
    )
    parts.append(
        f'<div class="lane-map-wrap">'
        f"{svg}"
        f"<div>"
        f'<p style="font-size:12px;color:#8b949e;margin-bottom:8px">'
        f"Ring colour = inferred lane role (centroid of first-10-min heatmap)"
        f"</p>"
        f'<div class="lane-legend">{legend_items}</div>'
        f"</div>"
        f"</div>"
    )

    # Stats table — Radiant first, then Dire, each sorted by lane_role
    players = sorted(
        [pp for pp in match.players if pp.hero_name],
        key=lambda p: (0 if p.team == 2 else 1, p.lane_role, p.player_id),
    )

    parts.append("<table>")
    parts.append(
        "<thead><tr>"
        "<th>Hero</th>"
        "<th>Team</th>"
        "<th>Lane</th>"
        '<th class="r" title="Last hits at 10 minutes">LH@10</th>'
        '<th class="r" title="Denies at 10 minutes">DN@10</th>'
        '<th class="r" title="Total earned gold at 10 minutes">Gold@10</th>'
        '<th class="r" title="Total earned XP at 10 minutes">XP@10</th>'
        '<th class="r" title="Lane Efficiency % — gold@10 ÷ 4948 baseline (OpenDota). '
        'Values above 100 occur when the hero has kills.">Eff%</th>'
        '<th class="r" title="Gold advantage vs lane opponents at 10 min. '
        'N/A for jungle/roaming.">Gold Adv</th>'
        '<th class="r" title="XP advantage vs lane opponents at 10 min. '
        'N/A for jungle/roaming.">XP Adv</th>'
        "<th>Eff Bar</th>"
        "</tr></thead>"
    )
    parts.append("<tbody>")

    for pp in players:
        team_color = TEAM_COLOR_CSS.get(pp.team, "#888")
        row_cls = "row-radiant" if pp.team == 2 else "row-dire"
        role_name = _LANE_ROLE_NAMES.get(pp.lane_role, "—")
        role_color = _LANE_COLORS.get(pp.lane_role, "#8b949e")

        def _adv_cell(val: int | None) -> str:
            if val is None:
                return '<td class="r lane-adv-neu">N/A</td>'
            cls = "lane-adv-pos" if val > 0 else ("lane-adv-neg" if val < 0 else "lane-adv-neu")
            sign = "+" if val > 0 else ""
            return f'<td class="r {cls}">{sign}{val:,}</td>'

        # Efficiency bar — capped at 120% visually so >100% values still fit
        eff_bar_width = min(pp.lane_efficiency_pct / 120 * 100, 100)
        eff_bar = (
            f'<div class="lane-eff-bar-wrap">'
            f'<div class="lane-eff-bar-fill" '
            f'style="width:{eff_bar_width:.1f}%;background:{team_color}"></div>'
            f"</div>"
        )

        hero_cell_html = (
            f'<img src="{hero_icon_src(pp.hero_name)}" width="20" height="12" '
            f'style="object-fit:cover;border-radius:2px;vertical-align:middle;margin-right:5px">'
            f'<span style="color:{team_color}">{e(hero(pp.hero_name))}</span>'
        )

        parts.append(
            f'<tr class="{row_cls}">'
            f'<td style="white-space:nowrap">{hero_cell_html}</td>'
            f'<td><span style="color:{team_color}">{e(team_name(pp.team))}</span></td>'
            f'<td><span style="color:{role_color};font-weight:600">{role_name}</span></td>'
            f'<td class="r">{pp.lane_last_hits}</td>'
            f'<td class="r">{pp.lane_denies}</td>'
            f'<td class="r">{pp.lane_total_gold:,}</td>'
            f'<td class="r">{pp.lane_total_xp:,}</td>'
            f'<td class="r"><b>{pp.lane_efficiency_pct}%</b></td>'
            f"{_adv_cell(pp.lane_gold_adv)}"
            f"{_adv_cell(pp.lane_xp_adv)}"
            f"<td>{eff_bar}</td>"
            f"</tr>"
        )

    parts.append("</tbody></table>")
    parts.append(
        '<p class="section-note">'
        "Eff% = total earned gold@10 ÷ 4948 (OpenDota baseline: lane creeps + passive income + starting gold). "
        "Gold/XP Adv = vs opposing hero(es) in same lane. N/A = no opponent with matching lane role."
        "</p>"
    )
    parts += ["</div>", "</details>", "</div>"]
    return "\n".join(parts)
