"""Combat report sections (kill feed, teamfights, combat time-series).

Split out of the former monolithic ``_sections.py`` (see that module's
shim for backward-compatible re-exports).
"""

from __future__ import annotations

import json

from gem.analysis import (
    estimate_vision,
    group_ability_hits,
    is_active_teamfight_participant,
    position_at_tick,
)
from gem.catalog import (
    ability_display,
    item_display,
)
from gem.reports._formatting import (
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    TEAM_COLOR_CSS,
    TICKS_PER_SEC,
    e,
    fmt_tick,
    hero,
    hero_cell,
)
from gem.reports.assets import (
    has_hero_icon,
    hero_icon_src,
    item_icon_tag,
    load_hero_icons,
    load_item_icons,
)
from gem.reports.player_names import display_player_name
from gem.reports.sections._shared import (
    _DIRE_COLORS,
    _RADIANT_COLORS,
)
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
    VisionModifierEvent,
)


def build_combat_timeseries_chart(match: ParsedMatch) -> str:
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


def build_kill_feed(match: ParsedMatch) -> str:
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

        npc_to_player: dict[str, ParsedPlayer] = {
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
                    pos = position_at_tick(victim_player, entry.tick)
                    if pos:
                        sources = estimate_vision(match, attacker_team, entry.tick, pos[0], pos[1])
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
    casts = group_ability_hits(groupable)
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
    slot_to_player: dict[int, ParsedPlayer],
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
    match: ParsedMatch,
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
    active: list[VisionModifierEvent] = []
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
            target_img = (
                f'<img src="{hero_icon_src(ev.target_name)}" width="16" height="10" '
                f'style="object-fit:cover;border-radius:2px;vertical-align:middle">'
                if has_hero_icon(ev.target_name)
                else ""
            )
            badge = (
                f'<span style="display:inline-flex;align-items:center;gap:4px;'
                f"background:#21262d;border:1px solid #30363d;border-radius:4px;"
                f'padding:2px 6px;font-size:11px;white-space:nowrap">'
                f'<span style="color:#8b949e">{e(mod_label)}</span>'
                f'<span style="color:#8b949e">→</span>'
                f"{target_img}"
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


def build_teamfights(match: ParsedMatch, map_b64: str | None) -> str:
    """Build the Teamfights tab content (filters + fight cards)."""
    fights = match.teamfights or []
    if not fights:
        return (
            '<div class="card"><details open><summary>Fights</summary>'
            '<div class="card-body"><p class="dim">(no fights detected)</p></div>'
            "</details></div>"
        )

    slot_to_player: dict[int, ParsedPlayer] = {pp.player_id: pp for pp in match.players}
    h2s: dict[str, int] = {pp.hero_name: pp.player_id for pp in match.players if pp.hero_name}
    load_hero_icons([pp.hero_name for pp in match.players if pp.hero_name])

    max_deaths = max((tf.deaths for tf in fights), default=1)
    max_participants = max(
        (sum(1 for p in tf.players if is_active_teamfight_participant(p)) for tf in fights),
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
        active_slots = [p.player_id for p in tf.players if is_active_teamfight_participant(p)]
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
                pp = slot_to_player.get(slot, ParsedPlayer(player_id=slot))
                team_cls = "radiant" if pp.team == 2 else "dire"
                died_cls = " died" if slot in died_slots else ""
                pname = e(display_player_name(pp))
                hname = e(hero(pp.hero_name))
                if has_hero_icon(pp.hero_name):
                    portrait = f'<img src="{hero_icon_src(pp.hero_name)}" alt="{hname}">'
                else:
                    # No icon cache: keep the card's footprint and team-color cue
                    # with a blank portrait; the hero name below carries identity.
                    portrait = '<div class="tf-participant-noicon"></div>'
                parts.append(
                    f'<div class="tf-participant {team_cls}{died_cls}">'
                    f"{portrait}"
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
                pp = slot_to_player.get(slot, ParsedPlayer(player_id=slot))
                tfp = tf_by_slot.get(slot)
                if tfp is None:
                    continue
                row_cls = "row-radiant" if pp.team == 2 else "row-dire"
                parts.append(
                    f'<tr class="{row_cls}">'
                    f"<td>{hero_cell(pp.hero_name, pp.team)}"
                    f'<div style="color:#8b949e;font-size:11px">{e(display_player_name(pp))}</div></td>'
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
