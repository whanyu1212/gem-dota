"""Economy report sections (gold/XP charts, damage, purchases, buybacks, runes).

Split out of the former monolithic ``_sections.py`` (see that module's
shim for backward-compatible re-exports).
"""

from __future__ import annotations

import json

from gem.analysis import net_worth_at
from gem.catalog import (
    ability_display,
    item_display,
)
from gem.reports._formatting import (
    RUNE_ICON_SHORT,
    RUNE_NAMES,
    TEAM_COLOR_CSS,
    TICKS_PER_SEC,
    e,
    fmt_tick,
    hero,
    hero_cell,
    team_name,
)
from gem.reports.assets import (
    item_icon_tag,
    load_hero_icons,
    load_item_icons,
)
from gem.reports.sections._shared import (
    _DIRE_COLORS,
    _RADIANT_COLORS,
)
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
)


def build_hero_timeseries_chart(match: ParsedMatch) -> str:
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


def build_gold_xp_chart(match: ParsedMatch) -> str:
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


def build_damage(match: ParsedMatch) -> str:
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


def build_purchases(match: ParsedMatch) -> str:
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


def _net_worth_at(pp: ParsedPlayer, tick: int) -> int:
    """Return the closest sampled net worth for a player at the given tick."""
    return net_worth_at(pp, tick)


def build_buybacks(match: ParsedMatch) -> str:
    """Build the buybacks section."""
    total = sum(len(p.buybacks) for p in match.players)

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
        # Cost comes from the model's BuybackEvent (gem.results.derived.buyback_cost),
        # not recomputed here, so the table matches ParsedPlayer.buybacks exactly.
        entries: list[tuple[int, str, int, int]] = []
        for pp in match.players:
            for bb in pp.buybacks:
                entries.append((bb.tick, pp.hero_name, pp.team, bb.cost))
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


def build_runes(match: ParsedMatch) -> str:
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
