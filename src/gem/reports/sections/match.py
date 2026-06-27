"""Match-level report sections (header, scoreboard, objectives, draft, chat, Roshan).

Split out of the former monolithic ``_sections.py`` (see that module's
shim for backward-compatible re-exports).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from gem.analysis import (
    build_rosh_conversions,
    format_npc_name,
)
from gem.catalog import hero_display
from gem.reports._formatting import (
    TEAM_COLOR_CSS,
    e,
    fmt_tick,
    hero,
    hero_cell,
    team_name,
)
from gem.reports.assets import (
    has_hero_icon,
    hero_icon_src,
    load_hero_icons,
)
from gem.reports.player_names import display_player_name
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
)

if TYPE_CHECKING:
    from gem.analysis.roshan import RoshConversion


def _draft_portrait(npc_name: str, alt: str, noicon_cls: str) -> str:
    """Draft-card portrait: hero icon when loaded, else a blank placeholder.

    Draft cards already render the hero name beneath the portrait, so when no
    icon cache is present we emit a sized placeholder (keeping the card's
    footprint and team-color cue) rather than a redundant name chip.

    Args:
        npc_name: Hero NPC name, possibly empty for an unresolved pick/ban.
        alt: Pre-escaped alt/title text for the image.
        noicon_cls: CSS class sizing the placeholder to the card's image box.

    Returns:
        An ``<img>`` fragment, or a placeholder ``<div>`` fragment.
    """
    if npc_name and has_hero_icon(npc_name):
        return f'<img src="{hero_icon_src(npc_name)}" alt="{alt}">'
    return f'<div class="{noicon_cls}" title="{alt}"></div>'


def build_header(
    match: ParsedMatch, fmt_tick: Callable[[int], str], game_modes: dict[int, str]
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

    # ── Team & roster panel ──────────────────────────────────────────────────
    # Only render if at least one team name is known (league/tournament games).
    load_hero_icons([p.hero_name for p in match.players if p.hero_name])
    team_rows: dict[int, list[str]] = {2: [], 3: []}
    for pp in match.players:
        if pp.team not in (2, 3):
            continue
        player_name = display_player_name(pp)
        player_label = e(player_name) if player_name else "—"
        if pp.account_id:
            player_label = (
                f'<a href="https://www.opendota.com/players/{pp.account_id}" '
                f'target="_blank" rel="noopener" '
                f'style="color:inherit;text-decoration:underline dotted">'
                f"{player_label}</a>"
            )
        hero_cell_html = hero_cell(pp.hero_name, pp.team) if pp.hero_name else "—"
        team_rows[pp.team].append(
            f"<tr>"
            f'<td style="padding:3px 12px 3px 0">{player_label}</td>'
            f'<td style="padding:3px 0;white-space:nowrap">{hero_cell_html}</td>'
            f"</tr>"
        )

    def _team_block(team: int, color: str) -> str:
        name = match.radiant_team_name if team == 2 else match.dire_team_name
        tag = match.radiant_team_tag if team == 2 else match.dire_team_tag
        team_id = match.radiant_team_id if team == 2 else match.dire_team_id
        side = "Radiant" if team == 2 else "Dire"
        if name:
            heading = f"{e(name)}"
            if tag:
                heading += f' <span style="opacity:.6;font-size:.85em">[{e(tag)}]</span>'
            if team_id:
                heading += (
                    f' <a href="https://www.opendota.com/teams/{team_id}" '
                    f'target="_blank" rel="noopener" '
                    f'style="opacity:.5;font-size:.75em;color:inherit;'
                    f'text-decoration:underline dotted">#{team_id}</a>'
                )
        else:
            heading = side
        rows_html = "\n".join(team_rows[team])
        return (
            f'<div style="flex:1;min-width:220px">'
            f'<div style="font-weight:600;color:{color};margin-bottom:6px">{heading}</div>'
            f'<table style="border:none;font-size:.85em">{rows_html}</table>'
            f"</div>"
        )

    radiant_block = _team_block(2, "#4caf50")
    dire_block = _team_block(3, "#f44336")

    parts.append(
        '<div class="card" style="margin-top:12px">'
        "<details open>"
        "<summary>Rosters</summary>"
        '<div class="card-body">'
        '<div style="display:flex;gap:32px;flex-wrap:wrap">'
        f"{radiant_block}{dire_block}"
        "</div>"
        "</div>"
        "</details>"
        "</div>"
    )

    return "\n".join(parts)


def build_scoreboard(match: ParsedMatch) -> str:
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
            acct = (
                f'<br><span style="font-size:0.75em;color:#8b949e">{pp.account_id}</span>'
                if pp.account_id
                else ""
            )
            parts.append(
                f'<tr class="{row_cls}">'
                f'<td style="white-space:nowrap">{hero_cell(pp.hero_name, team)}{acct}</td>'
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


def _clean_npc(name: str) -> str:
    """Clean an NPC name into a human-readable label."""
    return format_npc_name(name)


def _killer_label(killer: str) -> str:
    """Return display name for a killer NPC (hero or structure/neutral)."""
    if killer.startswith("npc_dota_hero_"):
        return hero(killer)
    return _clean_npc(killer) if killer else "unknown"


def build_objectives(match: ParsedMatch, fmt_tick_fn: Callable[[int], str]) -> str:
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


_ROSH_LABEL_DISPLAY: dict[str, str] = {
    "low_conversion": "Low Conversion",
    "fight_conversion": "Fight Conversion",
    "objective_conversion": "Objective Conversion",
    "map_squeeze": "Map Squeeze",
    "game_closing_rosh": "Game-Closing Rosh",
}


_ROSH_FATE_DISPLAY: dict[str, str] = {
    "consumed": "Consumed",
    "expired": "Expired",
    "denied": "Denied",
    "game_end": "Game End",
    "unknown": "Unknown",
}


_ROSH_DROP_DISPLAY: dict[str, str] = {
    "aegis": "Aegis",
    "cheese": "Cheese",
    "refresher_shard": "Refresher Shard",
    "banner": "Banner",
}


def _rosh_drops_display(drops: list[str]) -> str:
    """Render Roshan drop tokens as a human-readable comma list.

    Args:
        drops: Short drop tokens (e.g. ``["aegis", "cheese", "banner"]``).

    Returns:
        A comma-joined display string (e.g. ``"Aegis, Cheese, Banner"``), or
        ``"none"`` when no drops were captured.
    """
    if not drops:
        return "none"
    return ", ".join(_ROSH_DROP_DISPLAY.get(drop, drop.replace("_", " ").title()) for drop in drops)


def _rosh_banner_line(conversion: RoshConversion) -> str:
    """Render the Roshan's Banner plant/push line for a conversion card.

    A banner planted by the holder team is shown only when it was actually used;
    when that plant was followed by an enemy barracks falling, a "→ Rax" badge
    (with the lane, if known) flags the associative siege conversion.

    Args:
        conversion: The Roshan conversion record.

    Returns:
        An HTML ``<div>`` describing the banner plant, or ``""`` when no banner
        was planted in the window.
    """
    if not conversion.banner_planted:
        return ""
    if conversion.banner_rax_conversion:
        lane = f" ({conversion.banner_rax_lane})" if conversion.banner_rax_lane else ""
        badge = f'<span class="rosh-banner-badge">&rarr; Rax{e(lane)}</span>'
    else:
        badge = ""
    return f'<div class="rosh-banner">Banner planted{badge}</div>'


_ROSH_LABEL_EXPLANATION: dict[str, tuple[str, str]] = {
    "low_conversion": (
        "Roshan was secured, but the window did not clearly translate into fights, structures, or territorial squeeze.",
        "Fallback when no stronger fight/objective/map-control signal fired.",
    ),
    "fight_conversion": (
        "The team used Roshan mainly to win fights, but did not turn that advantage into major structural damage yet.",
        "Assigned when post-Rosh fight results are favorable without large objective conversion.",
    ),
    "objective_conversion": (
        "Roshan was translated into towers, barracks, or a clearly destructive push sequence.",
        "Assigned when the Aegis team takes at least 2 towers or any barracks during the conversion window.",
    ),
    "map_squeeze": (
        "The main gain was territorial: deeper warding or noticeably more farming presence in enemy territory.",
        "Assigned when enemy-half warding or enemy-half presence expands without a stronger fight/objective label.",
    ),
    "game_closing_rosh": (
        "This Roshan directly fed into the final closing sequence before the game ended.",
        "Assigned when the Roshan-holding team ends the game before the next Roshan window.",
    ),
}


_ROSH_AEGIS_OUTCOME_DISPLAY: dict[str, str] = {
    "consumed_in_fight": "Consumed In Fight",
    "expired_after_use": "Expired After Use",
    "expired_unused": "Expired Unused",
    "denied": "Denied",
    "window_lost": "Window Lost",
    "game_ended": "Game Ended",
    "unknown": "Unknown",
}


_ROSH_AEGIS_OUTCOME_EXPLANATION: dict[str, tuple[str, str]] = {
    "consumed_in_fight": (
        "The holder died once and Aegis actually triggered during the evaluated window.",
        "Inferred from the Aegis holder's first hero death before expiry.",
    ),
    "expired_after_use": (
        "Aegis timed out, but the team still got meaningful use from the Roshan window first.",
        "Used when Aegis expires after fights, structures, or map-control conversion.",
    ),
    "expired_unused": (
        "Aegis expired without a second life and without meaningful downstream conversion.",
        "Used when expiry happens with no fight wins and no structures.",
    ),
    "denied": (
        "The Aegis was denied, so the team never got the immortality window.",
        "Comes directly from the replay Aegis-denied event.",
    ),
    "window_lost": (
        "The Aegis team lost momentum in the key window and did not offset that with structures.",
        "Used when the Aegis side loses more fights than it wins and takes no towers or barracks.",
    ),
    "game_ended": (
        "The game ended before Aegis could be consumed or expire normally.",
        "Used when the replay ends during the Aegis ownership window.",
    ),
    "unknown": (
        "The replay does not let us classify the Aegis lifecycle confidently.",
        "Fallback when attribution is incomplete.",
    ),
}


def build_rosh_conversion(match: ParsedMatch) -> str:
    """Build the Roshan conversion section."""
    conversions = build_rosh_conversions(match)
    if not conversions:
        return ""

    label_rows = "".join(
        (
            "<tr>"
            f'<td><span class="rosh-badge rosh-badge-{label_key}">{e(_ROSH_LABEL_DISPLAY[label_key])}</span></td>'
            f"<td>{e(explanation)}</td>"
            f'<td style="color:#8b949e">{e(rule)}</td>'
            "</tr>"
        )
        for label_key, (explanation, rule) in _ROSH_LABEL_EXPLANATION.items()
    )
    aegis_outcome_rows = "".join(
        (
            "<tr>"
            f'<td><span class="rosh-outcome-badge rosh-outcome-{outcome_key}">{e(_ROSH_AEGIS_OUTCOME_DISPLAY[outcome_key])}</span></td>'
            f"<td>{e(explanation)}</td>"
            f'<td style="color:#8b949e">{e(rule)}</td>'
            "</tr>"
        )
        for outcome_key, (explanation, rule) in _ROSH_AEGIS_OUTCOME_EXPLANATION.items()
    )
    metric_rows = "".join(
        (
            "<tr>"
            f"<td>{e(name)}</td>"
            f"<td>{e(formula)}</td>"
            f'<td style="color:#8b949e">{e(description)}</td>'
            "</tr>"
        )
        for name, formula, description in [
            (
                "Immediate Window",
                "Roshan kill -> +180s",
                "Quick-read lens for whether the team acted on the spike immediately.",
            ),
            (
                "Aegis Window",
                "Aegis pickup -> inferred consume / expire / deny",
                "Primary evaluation window. If Aegis is consumed mid-fight, the overlapping fight is still counted.",
            ),
            (
                "Extended Window",
                "Roshan kill -> next Roshan or game end",
                "Used for broader context like game-closing sequences.",
            ),
            (
                "Ward Delta",
                "Aegis-side observer wards in enemy half - enemy observer wards in their own forward half",
                "Positive means the Roshan team pushed vision deeper than the opponent did during the same Aegis window.",
            ),
            (
                "Presence Delta",
                "enemy_half_farm_share_during - enemy_half_farm_share_before",
                "Before = % of holder-team position samples in enemy half during the 3 minutes before Roshan. During = % in enemy half during the first 3 minutes after Roshan. Reported in percentage points.",
            ),
        ]
    )

    parts = [
        '<div class="card">',
        "<details open>",
        "<summary>Roshan Conversion</summary>",
        '<div class="card-body">',
        '<p class="section-note">'
        "Each card asks whether a Roshan translated into fights, objectives, map expansion, "
        "or a game-closing sequence. Aegis consume is inferred from the holder's first death, "
        "so treat the timing as analytical rather than authoritative. No single score is shown "
        "because late-game Roshan windows naturally have more game-ending leverage than early ones."
        "</p>",
        '<div class="rosh-guide-grid">'
        '<div class="rosh-guide-block">'
        '<div class="rosh-guide-title">Labels</div>'
        f'<div class="rosh-table-wrap"><table class="rosh-guide-table"><thead><tr><th>Label</th><th>Meaning</th><th>Rule</th></tr></thead><tbody>{label_rows}</tbody></table></div>'
        "</div>"
        '<div class="rosh-guide-block">'
        '<div class="rosh-guide-title">Aegis Outcomes</div>'
        f'<div class="rosh-table-wrap"><table class="rosh-guide-table"><thead><tr><th>Outcome</th><th>Meaning</th><th>Rule</th></tr></thead><tbody>{aegis_outcome_rows}</tbody></table></div>'
        "</div>"
        '<div class="rosh-guide-block">'
        '<div class="rosh-guide-title">Definitions</div>'
        f'<div class="rosh-table-wrap"><table class="rosh-guide-table"><thead><tr><th>Metric</th><th>Formula</th><th>Interpretation</th></tr></thead><tbody>{metric_rows}</tbody></table></div>'
        "</div>"
        "</div>",
        '<div class="rosh-card-grid">',
    ]

    for conversion in conversions:
        team = conversion.holder_team
        team_color = TEAM_COLOR_CSS.get(team or 0, "#8b949e")
        team_label = team_name(team) if team in (2, 3) else "Unknown"
        holder_label = hero(conversion.holder_name) if conversion.holder_name else "Unknown"
        label_key = conversion.conversion_label
        label_display = _ROSH_LABEL_DISPLAY.get(label_key, label_key.replace("_", " ").title())
        fate_display = _ROSH_FATE_DISPLAY.get(conversion.aegis_fate, conversion.aegis_fate.title())
        outcome_display = _ROSH_AEGIS_OUTCOME_DISPLAY.get(
            conversion.aegis_outcome,
            conversion.aegis_outcome.replace("_", " ").title(),
        )
        presence_delta_pct = round(conversion.enemy_half_farm_share_delta * 100)
        first_fight = fmt_tick(conversion.first_fight_tick) if conversion.first_fight_tick else "—"
        first_objective = (
            fmt_tick(conversion.first_objective_tick) if conversion.first_objective_tick else "—"
        )
        drops_display = _rosh_drops_display(conversion.drops)
        hv_badge = (
            '<span class="rosh-hv-badge">High value</span>'
            if conversion.had_high_value_drop
            else ""
        )
        banner_html = _rosh_banner_line(conversion)
        chips = "".join(
            f'<span class="rosh-chip rosh-chip-{event.kind}">'
            f'<span class="rosh-chip-time">{e(fmt_tick(event.tick))}</span>'
            f"{e(event.label)}</span>"
            for event in conversion.timeline_events
        )
        drivers_html = (
            '<ul class="rosh-driver-list">'
            + "".join(f"<li>{e(driver)}</li>" for driver in conversion.drivers)
            + "</ul>"
            if conversion.drivers
            else '<p class="dim">No strong downstream conversion signals were detected.</p>'
        )
        parts.append(
            '<div class="rosh-card">'
            '<div class="rosh-card-head">'
            f'<div><div class="rosh-kicker">Roshan #{conversion.rosh_number}</div>'
            f'<div class="rosh-title"><span style="color:{team_color}">{e(team_label)}</span>'
            f" — {e(holder_label)}</div>"
            f'<div class="rosh-meta">Rosh {e(fmt_tick(conversion.rosh_tick))} · '
            f"Aegis {e(fate_display)} at {e(fmt_tick(conversion.aegis_end_tick))} · "
            f"Extended window ends {e(fmt_tick(conversion.extended_end_tick))}</div>"
            f'<div class="rosh-drops">Drops: {e(drops_display)}{hv_badge}</div>'
            f"{banner_html}</div>"
            '<div class="rosh-head-right">'
            f'<span class="rosh-badge rosh-badge-{e(label_key)}">{e(label_display)}</span>'
            f'<span class="rosh-outcome-badge rosh-outcome-{e(conversion.aegis_outcome)}">{e(outcome_display)}</span>'
            "</div>"
            "</div>"
            '<div class="rosh-metric-grid">'
            f'<div class="rosh-metric"><span class="label">Fights</span><span class="value">{conversion.fights_won}-{conversion.fights_lost}-{conversion.fights_drawn}</span></div>'
            f'<div class="rosh-metric"><span class="label">Objectives</span><span class="value">{conversion.towers_taken} T / {conversion.barracks_taken} Rax</span></div>'
            f'<div class="rosh-metric"><span class="label">Enemy Buybacks</span><span class="value">{conversion.enemy_buybacks_forced}</span></div>'
            f'<div class="rosh-metric"><span class="label">Ward Delta</span><span class="value">{conversion.enemy_half_observer_delta:+d}</span></div>'
            f'<div class="rosh-metric"><span class="label">Presence Delta</span><span class="value">{presence_delta_pct:+d} pts</span></div>'
            f'<div class="rosh-metric"><span class="label">First Fight / Obj</span><span class="value">{e(first_fight)} / {e(first_objective)}</span></div>'
            "</div>"
            f'<div class="rosh-timeline">{chips}</div>'
            f"{drivers_html}"
            "</div>"
        )

    parts.append("</div>")
    parts.append('<div class="rosh-table-wrap"><table>')
    parts.append(
        "<thead><tr>"
        "<th>Rosh</th><th>Team</th><th>Holder</th><th>Aegis</th><th>Outcome</th><th>Drops</th>"
        '<th class="r">Fights</th><th class="r">Towers</th><th class="r">Rax</th>'
        '<th class="r">Buybacks</th><th class="r">Ward Δ</th><th class="r">Presence Δ</th>'
        "<th>Label</th>"
        "</tr></thead><tbody>"
    )
    for conversion in conversions:
        team = conversion.holder_team
        team_color = TEAM_COLOR_CSS.get(team or 0, "#8b949e")
        team_label = team_name(team) if team in (2, 3) else "Unknown"
        holder_label = hero(conversion.holder_name) if conversion.holder_name else "Unknown"
        label_key = conversion.conversion_label
        label_display = _ROSH_LABEL_DISPLAY.get(label_key, label_key.replace("_", " ").title())
        fate_display = _ROSH_FATE_DISPLAY.get(conversion.aegis_fate, conversion.aegis_fate.title())
        outcome_display = _ROSH_AEGIS_OUTCOME_DISPLAY.get(
            conversion.aegis_outcome,
            conversion.aegis_outcome.replace("_", " ").title(),
        )
        presence_delta_pct = round(conversion.enemy_half_farm_share_delta * 100)
        drops_cell = _rosh_drops_display(conversion.drops)
        if conversion.had_high_value_drop:
            drops_cell += " ★"
        # Flag a banner→rax push in the Rax column: ⚑ when a planted banner was
        # followed by a barracks falling, with the lane initial when known.
        rax_cell = str(conversion.barracks_taken)
        if conversion.banner_rax_conversion:
            lane_initial = (conversion.banner_rax_lane or "")[:1].upper()
            rax_cell += f" ⚑{lane_initial}" if lane_initial else " ⚑"
        parts.append(
            "<tr>"
            f"<td>#{conversion.rosh_number}</td>"
            f'<td><span style="color:{team_color}">{e(team_label)}</span></td>'
            f"<td>{e(holder_label)}</td>"
            f"<td>{e(fate_display)}</td>"
            f"<td>{e(outcome_display)}</td>"
            f"<td>{e(drops_cell)}</td>"
            f'<td class="r">{conversion.fights_won}-{conversion.fights_lost}-{conversion.fights_drawn}</td>'
            f'<td class="r">{conversion.towers_taken}</td>'
            f'<td class="r">{e(rax_cell)}</td>'
            f'<td class="r">{conversion.enemy_buybacks_forced}</td>'
            f'<td class="r">{conversion.enemy_half_observer_delta:+d}</td>'
            f'<td class="r">{presence_delta_pct:+d} pts</td>'
            f"<td>{e(label_display)}</td>"
            "</tr>"
        )
    parts.append("</tbody></table></div>")
    parts.extend(["</div>", "</details>", "</div>"])
    return "\n".join(parts)


def build_draft(match: ParsedMatch) -> str:
    """Build the draft section."""
    if not match.draft:
        return ""

    sorted_draft = sorted(match.draft, key=lambda d: d.tick)

    hero_to_player: dict[str, ParsedPlayer] = {
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
        portrait = _draft_portrait(ev.hero_name, e(name), "draft-noicon")
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
            f"{portrait}"
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
            portrait = _draft_portrait(ev.hero_name, e(name), "draft-noicon-pick")
            pp = hero_to_player.get(ev.hero_name)
            player_name = display_player_name(pp)
            time_str = fmt_tick(ev.tick) if ev.tick else ""
            player_html = f'<div class="dp-player">{e(player_name)}</div>' if player_name else ""
            cards.append(
                f'<div class="draft-pick-card {label_cls}">'
                f"{portrait}"
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


def build_chat(match: ParsedMatch) -> str:
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
