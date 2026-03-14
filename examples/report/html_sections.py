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
    if not any(p.net_worth_t_min or p.xp_t_min for p in players):
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


def build_objectives(match: gem.ParsedMatch, fmt_tick_fn: Callable[[int], str]) -> str:
    """Build the objectives timeline section."""
    events: list[tuple[int, str, str, str]] = []

    for t in match.towers:
        team_color = TEAM_COLOR_CSS.get(t.team, "#888")
        name = t.tower_name.replace("npc_dota_", "").replace("_", " ")
        killer = hero(t.killer) if t.killer.startswith("npc_dota_hero_") else t.killer
        desc = (
            f'<span style="color:{TEAM_COLOR_CSS.get(t.team, "#888")};font-weight:bold">'
            f"{e(team_name(t.team))}</span> "
            f"{e(name)} — killed by {e(killer)}"
        )
        events.append((t.tick, "Tower", team_color, desc))

    for b in match.barracks:
        team_color = TEAM_COLOR_CSS.get(b.team, "#888")
        name = b.barracks_name.replace("npc_dota_", "").replace("_", " ")
        killer = hero(b.killer) if b.killer.startswith("npc_dota_hero_") else b.killer
        desc = (
            f'<span style="color:{TEAM_COLOR_CSS.get(b.team, "#888")};font-weight:bold">'
            f"{e(team_name(b.team))}</span> "
            f"{e(name)} — killed by {e(killer)}"
        )
        events.append((b.tick, "Barracks", team_color, desc))

    for n, r in enumerate(match.roshans, 1):
        killer = hero(r.killer) if r.killer else "?"
        respawn_min = fmt_tick_fn(r.tick + 8 * 30 * 60)
        respawn_max = fmt_tick_fn(r.tick + 11 * 30 * 60)
        desc = (
            f'<span style="color:#ffb74d">Roshan #{n}</span> killed by {e(killer)} '
            f"— respawns {e(respawn_min)}–{e(respawn_max)}"
        )
        events.append((r.tick, f"Roshan #{n}", "#ffb74d", desc))

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

        bar_pct = int(total_dmg / max_dmg * 100)
        team_color = TEAM_COLOR_CSS.get(pp.team, "#888")
        bar_html = (
            f'<div class="dmg-bar-wrap">'
            f'<div class="dmg-bar-fill" style="width:{bar_pct}%;background:{team_color}"></div>'
            f"</div>"
        )
        row_cls = "row-radiant" if pp.team == 2 else "row-dire"
        dmg_taken_cell = f'<td class="r" title="{e(top_attacker)}">{total_dmg_taken:,}</td>'
        parts.append(
            f'<tr class="{row_cls}">'
            f'<td style="white-space:nowrap">{hero_cell(pp.hero_name, pp.team)}</td>'
            f'<td><span style="color:{team_color}">{e(team_name(pp.team))}</span></td>'
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

            parts.append(
                f"<tr>"
                f'<td style="color:#8b949e">{e(fmt_tick(entry.tick))}</td>'
                f"<td>{killer_cell}</td>"
                f"<td>{victim_cell}</td>"
                f"<td>{via}</td>"
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
                f"<td>{e(fmt_tick(tick))}</td>"
                f"<td>{e(hero(hero_name))}</td>"
                f'<td><span style="color:{team_color}">{e(team_name(team))}</span></td>'
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
            killer = _hero(getattr(w, "killer", "")) if getattr(w, "killer", None) else "?"
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
    return " · ".join(f"{e(ability_display(a))} ×{c}" for a, c in top)


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


def build_teamfights(match: gem.ParsedMatch, map_b64: str | None) -> str:
    """Build the Teamfights tab content (filters + fight cards)."""
    fights = match.teamfights or []
    if not fights:
        return (
            '<div class="card"><details open><summary>Teamfights</summary>'
            '<div class="card-body"><p class="dim">(no teamfights detected)</p></div>'
            "</details></div>"
        )

    slot_to_player: dict[int, gem.ParsedPlayer] = {pp.player_id: pp for pp in match.players}
    load_hero_icons([pp.hero_name for pp in match.players if pp.hero_name])

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
        is_pick = bool(getattr(event, "is_pick", False))
        hero_name = getattr(event, "hero_name", "")
        team = getattr(event, "team", None)
        slot_index = int(getattr(event, "slot_index", 0))

        if is_pick and hero_name and hero_name in hero_to_player:
            return hero_to_player[hero_name].team
        if team in (2, 3):
            return int(team)
        if is_pick:
            return 2 if slot_index < 5 else 3
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
