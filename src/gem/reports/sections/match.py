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
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    TEAM_COLOR_CSS,
    e,
    fmt_tick,
    hero,
    hero_cell,
    team_name,
    tick_after_game_seconds,
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
    from gem.analysis.roshan import RoshConversion, RoshTerritoryWindow


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
    if match.duration > 0:
        duration = f"{match.duration // 60:02d}:{match.duration % 60:02d}"
    else:
        last_tick = (
            match.post_game_tick
            or match.game_end_tick
            or max((max(p.times) for p in match.players if p.times), default=0)
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
        respawn_min = fmt_tick_fn(tick_after_game_seconds(r.tick, 8 * 60))
        respawn_max = fmt_tick_fn(tick_after_game_seconds(r.tick, 11 * 60))
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


_ROSH_AEGIS_OUTCOME_DISPLAY: dict[str, str] = {
    "consumed_in_fight": "Consumed In Fight",
    "expired_after_use": "Expired After Use",
    "expired_unused": "Expired Unused",
    "denied": "Denied",
    "window_lost": "Window Lost",
    "game_ended": "Game Ended",
    "unknown": "Unknown",
}


_ROSH_TAG_DISPLAY: dict[str, str] = {
    "fight_advantage": "Fight advantage",
    "objective_gain": "Objective gain",
    "resource_gain": "Resource gain",
    "territorial_expansion": "Territorial expansion",
    "vision_expansion": "Vision expansion",
    "tormentor_secured": "Tormentor secured",
    "game_closing": "Game closing",
    "counter_conversion": "Counter-conversion",
}

_ROSH_BALANCE_SCALE: dict[str, float] = {
    "fight": 3.0,
    "structure": 12.0,
    "net_worth": 10_000.0,
    "xp": 8_000.0,
    "coverage": 25.0,
    "depth": 0.5,
    "ward": 5.0,
    "tormentor": 2.0,
}


def _display_token(value: str) -> str:
    words: list[str] = []
    for token in value.replace("_", " ").split():
        lowered = token.lower()
        if lowered == "xp":
            words.append("XP")
        elif lowered.endswith("pct") and lowered[:-3].replace(".", "", 1).isdigit():
            words.append(f"{token[:-3]}%")
        else:
            words.append(token.title())
    return " ".join(words)


def _format_signed(
    value: int | float | None,
    *,
    decimals: int = 0,
    suffix: str = "",
) -> str:
    if value is None:
        return "Unavailable"
    if decimals:
        rendered = f"{value:+,.{decimals}f}" if value else f"{value:,.{decimals}f}"
    else:
        rendered = f"{value:+,.0f}" if value else "0"
    return f"{rendered}{suffix}"


def _analysis_status_html(conversion: RoshConversion) -> str:
    status = conversion.analysis_status
    reasons = conversion.analysis_status_reasons
    status_text = _display_token(status)
    reason_text = "; ".join(_display_token(reason) for reason in reasons)
    title = f' title="{e(reason_text)}"' if reason_text else ""
    reason_html = (
        '<ul class="rosh-status-reasons">'
        + "".join(f"<li>{e(_display_token(reason))}</li>" for reason in reasons)
        + "</ul>"
        if reasons
        else ""
    )
    return (
        '<div class="rosh-status-block">'
        f'<span class="rosh-status rosh-status-{e(status)}"{title}>'
        f"Evidence: {e(status_text)}</span>{reason_html}</div>"
    )


def _tag_chips(tags: list[str]) -> str:
    if not tags:
        return '<span class="rosh-tag rosh-tag-none">No evidence tags</span>'
    return "".join(
        f'<span class="rosh-tag rosh-tag-{e(tag)}">'
        f"{e(_ROSH_TAG_DISPLAY.get(tag, _display_token(tag)))}</span>"
        for tag in tags
    )


def _balance_row(
    label: str,
    value: int | float | None,
    scale_key: str,
    *,
    decimals: int = 0,
    suffix: str = "",
) -> str:
    rendered = _format_signed(value, decimals=decimals, suffix=suffix)
    if value is None:
        bar = '<span class="rosh-balance-unavailable">No evidence</span>'
        value_class = " unavailable"
    else:
        width = min(abs(float(value)) / _ROSH_BALANCE_SCALE[scale_key], 1.0) * 50.0
        direction = "positive" if value > 0 else "negative" if value < 0 else "neutral"
        bar = (
            '<span class="rosh-balance-track" aria-hidden="true">'
            f'<span class="rosh-balance-fill {direction}" style="--rosh-bar:{width:.1f}%"></span>'
            "</span>"
        )
        value_class = f" {direction}"
    return (
        f'<div class="rosh-balance-row" role="img" aria-label="{e(label)}: {e(rendered)}">'
        f'<span class="rosh-balance-label">{e(label)}</span>{bar}'
        f'<span class="rosh-balance-value{value_class}">{e(rendered)}</span></div>'
    )


def _balance_panel(conversion: RoshConversion) -> str:
    profile = conversion.differential_profile
    rows = [
        _balance_row("Fight differential", profile.fight_differential, "fight"),
        _balance_row("Weighted structure differential", profile.structure_delta, "structure"),
        _balance_row("Net worth swing", profile.net_worth_swing, "net_worth"),
        _balance_row("XP swing", profile.xp_swing, "xp"),
        _balance_row(
            "Coverage swing", profile.coverage_swing_pct, "coverage", decimals=1, suffix=" pp"
        ),
        _balance_row("Depth swing", profile.depth_swing, "depth", decimals=3),
        _balance_row("Forward-ward differential", profile.forward_ward_delta, "ward"),
        _balance_row("Tormentor differential", profile.tormentor_delta, "tormentor"),
    ]
    unknown_parts: list[str] = []
    if profile.unattributed_towers:
        unknown_parts.append(f"{profile.unattributed_towers} tower(s)")
    if profile.unattributed_barracks:
        unknown_parts.append(f"{profile.unattributed_barracks} barracks")
    if profile.unattributed_tormentors:
        unknown_parts.append(f"{profile.unattributed_tormentors} Tormentor(s)")
    unknown_note = (
        '<p class="rosh-panel-note rosh-unattributed">Not credited to either side: '
        + e(", ".join(unknown_parts))
        + ".</p>"
        if unknown_parts
        else ""
    )
    return (
        '<section class="rosh-panel rosh-balance-panel" '
        'aria-label="Signed conversion balance">'
        "<h4>Signed conversion balance</h4>"
        '<p class="rosh-panel-note">Positive values favor the conversion team; each row uses '
        "its own visual scale.</p>" + "".join(rows) + unknown_note + "</section>"
    )


def _resource_card(
    label: str,
    start: int | None,
    end: int | None,
    swing: int | None,
    rate: float | None,
) -> str:
    complete = all(value is not None for value in (start, end, swing, rate))
    note = "" if complete else '<p class="rosh-resource-note">Insufficient samples</p>'
    return (
        '<div class="rosh-resource-card">'
        f"<h5>{e(label)}</h5>"
        f'<div class="rosh-resource-flow"><span>{e(_format_signed(start))}</span>'
        '<span aria-hidden="true">→</span>'
        f"<span>{e(_format_signed(end))}</span></div>"
        f'<div class="rosh-resource-detail"><span>Raw swing</span>'
        f"<strong>{e(_format_signed(swing))}</strong></div>"
        f'<div class="rosh-resource-detail"><span>Rate / minute</span>'
        f"<strong>{e(_format_signed(rate, decimals=1))}</strong></div>{note}</div>"
    )


def _resource_panel(conversion: RoshConversion) -> str:
    profile = conversion.differential_profile
    return (
        '<section class="rosh-panel" aria-label="Resource advantage movement">'
        "<h4>Resource movement</h4>"
        '<p class="rosh-panel-note">Conversion-team advantage at the first and last valid '
        "samples in the analysis window.</p>"
        '<div class="rosh-resource-grid">'
        + _resource_card(
            "Net worth advantage",
            profile.net_worth_advantage_start,
            profile.net_worth_advantage_end,
            profile.net_worth_swing,
            profile.net_worth_swing_per_minute,
        )
        + _resource_card(
            "XP advantage",
            profile.xp_advantage_start,
            profile.xp_advantage_end,
            profile.xp_swing,
            profile.xp_swing_per_minute,
        )
        + "</div></section>"
    )


def _rosh_world_to_px(x: float, y: float, size: int) -> tuple[float, float]:
    px = (x - MAP_XMIN) / (MAP_XMAX - MAP_XMIN) * size
    py = (1.0 - (y - MAP_YMIN) / (MAP_YMAX - MAP_YMIN)) * size
    return px, py


def _territory_metric(value: float | None, *, suffix: str = "") -> str:
    return "Unavailable" if value is None else f"{value:.1f}{suffix}"


def _coverage_map_svg(
    match: ParsedMatch,
    window: RoshTerritoryWindow,
    *,
    conversion_number: int,
    phase: str,
    map_b64: str | None,
    conversion_team: int | None,
    size: int = 360,
) -> str:
    phase_label = "Before" if phase == "before" else "During"
    reasons = ", ".join(_display_token(reason) for reason in window.status_reasons)
    if window.status == "unavailable":
        detail = f": {reasons}" if reasons else ""
        return (
            f'<figure class="rosh-map-card" aria-label="{phase_label} territory coverage unavailable">'
            f"<h5>{phase_label}</h5>"
            f'<div class="rosh-map-empty" role="status">Coverage unavailable{e(detail)}</div>'
            "<figcaption>Sampled/sustained occupancy is unavailable; no true control is "
            "inferred.</figcaption></figure>"
        )

    svg_id = f"rosh-{conversion_number}-{phase}"
    conversion_cells = {(cell.grid_x, cell.grid_y): cell for cell in window.conversion_cells}
    opponent_cells = {(cell.grid_x, cell.grid_y): cell for cell in window.opponent_cells}
    cell_fragments: list[str] = []
    for key in sorted(conversion_cells.keys() | opponent_cells.keys()):
        own_cell = conversion_cells.get(key)
        opponent_cell = opponent_cells.get(key)
        cell = own_cell or opponent_cell
        if cell is None:
            continue
        left, bottom = _rosh_world_to_px(cell.x_min, cell.y_min, size)
        right, top = _rosh_world_to_px(cell.x_max, cell.y_max, size)
        opacity = 0.24 + 0.66 * max(
            own_cell.occupancy_share if own_cell else 0.0,
            opponent_cell.occupancy_share if opponent_cell else 0.0,
        )
        cell_class = (
            "contested"
            if own_cell is not None and opponent_cell is not None
            else "conversion"
            if own_cell is not None
            else "opponent"
        )
        cell_fragments.append(
            f'<rect class="rosh-coverage-cell {cell_class}" x="{left:.2f}" y="{top:.2f}" '
            f'width="{right - left:.2f}" height="{bottom - top:.2f}" '
            f'fill="url(#{svg_id}-{cell_class})" fill-opacity="{opacity:.2f}">'
            f"<title>{e(_display_token(cell_class))} sampled occupancy; "
            f"{cell.occupancy_share * 100:.1f}% of time buckets</title></rect>"
        )

    ward_fragments: list[str] = []
    for ward in match.wards:
        if (
            ward.x is None
            or ward.y is None
            or ward.tick < window.start_tick
            or ward.tick > window.end_tick
        ):
            continue
        cx, cy = _rosh_world_to_px(ward.x, ward.y, size)
        relation = (
            "conversion"
            if ward.team == conversion_team
            else "opponent"
            if ward.team in (2, 3)
            else "unknown"
        )
        ward_label = f"{team_name(ward.team) if ward.team in (2, 3) else 'Unknown'} "
        ward_label += f"{ward.ward_type} ward at {fmt_tick(ward.tick)}"
        ward_fragments.append(
            f'<circle class="rosh-ward-marker {relation} {e(ward.ward_type)}" '
            f'cx="{cx:.2f}" cy="{cy:.2f}" r="4.2"><title>{e(ward_label)}</title></circle>'
        )

    background = (
        f'<image class="gem-map-bg" href="" x="0" y="0" width="{size}" height="{size}" '
        'preserveAspectRatio="xMidYMid slice"/>'
        if map_b64
        else f'<rect class="rosh-map-fallback" width="{size}" height="{size}"/>'
    )
    title_id = f"{svg_id}-title"
    description_id = f"{svg_id}-description"
    svg = (
        f'<svg class="rosh-coverage-map" viewBox="0 0 {size} {size}" role="img" '
        f'aria-labelledby="{title_id} {description_id}" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{title_id}">{phase_label} sampled territory occupancy</title>'
        f'<desc id="{description_id}">Conversion team, opponent, and contested sustained '
        "occupancy cells with ward placement markers.</desc>"
        "<defs>"
        f'<pattern id="{svg_id}-conversion" width="8" height="8" patternUnits="userSpaceOnUse">'
        '<rect width="8" height="8" fill="#238636"/></pattern>'
        f'<pattern id="{svg_id}-opponent" width="8" height="8" patternUnits="userSpaceOnUse">'
        '<rect width="8" height="8" fill="#da3633"/></pattern>'
        f'<pattern id="{svg_id}-contested" width="8" height="8" '
        'patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#238636"/>'
        '<path d="M-2,2 L2,-2 M0,8 L8,0 M6,10 L10,6" stroke="#ff7b72" '
        'stroke-width="3"/></pattern></defs>'
        f"{background}{''.join(cell_fragments)}{''.join(ward_fragments)}</svg>"
    )
    metrics = (
        '<div class="rosh-map-metrics">'
        f"<span>Conversion coverage <strong>{e(_territory_metric(window.conversion_coverage_pct, suffix='%'))}</strong></span>"
        f"<span>Opponent coverage <strong>{e(_territory_metric(window.opponent_coverage_pct, suffix='%'))}</strong></span>"
        f"<span>Coverage differential <strong>{e(_format_signed(window.coverage_differential_pct, decimals=1, suffix=' pp'))}</strong></span>"
        f"<span>Depth differential <strong>{e(_format_signed(window.depth_differential, decimals=3))}</strong></span>"
        "</div>"
    )
    status_note = f'<p class="rosh-map-status">{e(_display_token(window.status))}'
    if reasons:
        status_note += f": {e(reasons)}"
    status_note += "</p>"
    return (
        f'<figure class="rosh-map-card"><h5>{phase_label}</h5>{svg}{metrics}{status_note}'
        '<div class="rosh-map-legend" aria-label="Coverage map legend">'
        '<span><i class="conversion"></i>Conversion team occupancy</span>'
        '<span><i class="opponent"></i>Opponent occupancy</span>'
        '<span><i class="contested"></i>Contested cell</span>'
        '<span><i class="ward"></i>Ward placement</span></div>'
        "<figcaption>Cells show sampled/sustained occupancy, not true control. Ward markers "
        "show recorded placements in the same window.</figcaption></figure>"
    )


def _territory_panel(
    match: ParsedMatch,
    conversion: RoshConversion,
    map_b64: str | None,
) -> str:
    profile = conversion.differential_profile
    return (
        '<section class="rosh-panel" aria-label="Paired territory coverage maps">'
        "<h4>Before vs during territory evidence</h4>"
        '<div class="rosh-map-pair">'
        + _coverage_map_svg(
            match,
            profile.before_territory,
            conversion_number=conversion.rosh_number,
            phase="before",
            map_b64=map_b64,
            conversion_team=conversion.conversion_team,
        )
        + _coverage_map_svg(
            match,
            profile.during_territory,
            conversion_number=conversion.rosh_number,
            phase="during",
            map_b64=map_b64,
            conversion_team=conversion.conversion_team,
        )
        + "</div></section>"
    )


_ROSH_TIMELINE_POSITIVE = {
    "fight_win",
    "tower",
    "barracks",
    "buyback",
    "tormentor",
    "banner",
}
_ROSH_TIMELINE_ADVERSE = {
    "fight_loss",
    "tower_lost",
    "barracks_lost",
    "own_buyback",
    "opponent_tormentor",
    "opponent_banner",
    "aegis_denied",
}


def _timeline_side(kind: str) -> str:
    if kind in _ROSH_TIMELINE_POSITIVE:
        return "positive"
    if kind in _ROSH_TIMELINE_ADVERSE:
        return "adverse"
    return "anchor"


def _timeline_html(conversion: RoshConversion) -> str:
    events = sorted(conversion.timeline_events, key=lambda event: (event.tick, event.kind))
    if not events:
        event_html = '<li class="rosh-timeline-empty">No timeline evidence available.</li>'
    else:
        rendered: list[str] = []
        for event in events:
            side = _timeline_side(event.kind)
            kind_class = "".join(
                character if character.isalnum() or character in "-_" else "-"
                for character in event.kind
            )
            link_attributes = (
                f' href="#fight-{event.fight_index + 1}" '
                f'data-report-target="fight-{event.fight_index + 1}"'
                if event.fight_index is not None
                else ""
            )
            content_tag = "a" if event.fight_index is not None else "div"
            rendered.append(
                f'<li class="rosh-timeline-event {side} rosh-event-{e(kind_class)}" '
                f'data-tick="{event.tick}"><{content_tag} class="rosh-timeline-content"'
                f"{link_attributes}>"
                f"<time>{e(fmt_tick(event.tick))}</time><span>{e(event.label)}</span>"
                f"</{content_tag}></li>"
            )
        event_html = "".join(rendered)
    return (
        '<section class="rosh-panel rosh-timeline-panel" aria-label="Chronological conversion evidence">'
        "<h4>Chronological evidence</h4>"
        '<p class="rosh-panel-note">Events are aligned by conversion-positive, neutral anchor, '
        "or adverse kind. Timing proximity does not establish causation.</p>"
        f'<ol class="rosh-timeline-list">{event_html}</ol></section>'
    )


def _summary_metric(value: int | float | None, *, decimals: int = 0, suffix: str = "") -> str:
    return e(_format_signed(value, decimals=decimals, suffix=suffix))


def build_rosh_conversion(
    match: ParsedMatch,
    map_b64: str | None = None,
    conversions: list[RoshConversion] | None = None,
) -> str:
    """Build the evidence-first Roshan conversion section.

    Args:
        match: Parsed match carrying Roshan and downstream replay evidence.
        map_b64: Optional pre-encoded map background. The full report patches the
            shared source into ``image.gem-map-bg`` elements after load.
        conversions: Optional precomputed records shared with the Fights tab.

    Returns:
        Self-contained HTML for the Roshan conversion tab, or an empty string
        when the match has no Roshan kills.
    """
    if conversions is None:
        conversions = build_rosh_conversions(match)
    if not conversions:
        return ""

    parts = [
        '<div class="card rosh-section">',
        "<details open>",
        "<summary>Roshan Conversion</summary>",
        '<div class="card-body">',
        '<p class="section-note">Each card compares the conversion team with its opponent using '
        "raw, signed evidence. Tags are non-exclusive and status explains missing telemetry. "
        "Aegis use can be inferred from replay events.</p>"
        '<details class="rosh-definitions"><summary>Definitions &amp; evidence limits</summary>'
        '<div class="rosh-definitions-body"><p><strong>Balance:</strong> conversion team minus '
        "opponent. Structure value weights towers by tier and barracks separately.</p>"
        "<p><strong>Territory:</strong> a three-minute baseline and the hardened analysis window "
        "use sampled hero-seconds and sustained occupancy. This is not true map control or a causal claim.</p>"
        "<p><strong>Resources:</strong> first-to-last valid team-advantage samples; unavailable "
        "samples remain unavailable rather than becoming zero.</p></div></details>"
        '<div class="rosh-card-grid">',
    ]

    for conversion in conversions:
        team = (
            conversion.conversion_team
            if conversion.conversion_team in (2, 3)
            else conversion.holder_team
        )
        team_color = TEAM_COLOR_CSS.get(team or 0, "#8b949e")
        team_label = team_name(team) if team in (2, 3) else "Unknown"
        roshan_team_label = (
            team_name(conversion.roshan_team) if conversion.roshan_team in (2, 3) else "Unknown"
        )
        holder_label = hero(conversion.holder_name) if conversion.holder_name else "Unknown"
        fate_display = _ROSH_FATE_DISPLAY.get(
            conversion.aegis_fate, _display_token(conversion.aegis_fate)
        )
        outcome_display = _ROSH_AEGIS_OUTCOME_DISPLAY.get(
            conversion.aegis_outcome,
            _display_token(conversion.aegis_outcome),
        )
        inferred_badge = (
            '<span class="rosh-inferred-badge">Inferred</span>'
            if conversion.aegis_fate_inferred
            else ""
        )
        fate_source_display = _display_token(conversion.aegis_fate_source.value)
        roshan_source_display = _display_token(conversion.roshan_team_source.value).replace(
            " Id", " ID"
        )
        conversion_source_display = _display_token(conversion.conversion_team_source.value).replace(
            " Id", " ID"
        )
        drops_display = _rosh_drops_display(conversion.drops)
        hv_badge = (
            '<span class="rosh-hv-badge">High value</span>'
            if conversion.had_high_value_drop
            else ""
        )
        parts.append(
            f'<article class="rosh-card" id="roshan-conversion-{conversion.rosh_number}">'
            '<header class="rosh-card-head">'
            '<div class="rosh-head-evidence">'
            f'<div class="rosh-kicker">Roshan #{conversion.rosh_number} · '
            f"{e(fmt_tick(conversion.rosh_tick))}</div>"
            f'<h3 class="rosh-title"><span style="color:{team_color}">{e(team_label)}</span>'
            f" conversion · {e(holder_label)}</h3>"
            f'<p class="rosh-meta">Roshan secured by {e(roshan_team_label)} · '
            f"Analysis window ends {e(fmt_tick(conversion.differential_profile.window_end_tick)) if conversion.differential_profile.window_end_tick is not None else 'Unavailable'} · "
            f"team evidence {e(roshan_source_display)} / {e(conversion_source_display)}</p>"
            f'<div class="rosh-drops">Drops: {e(drops_display)}{hv_badge}</div>'
            f"{_rosh_banner_line(conversion)}</div>"
            '<div class="rosh-head-right">'
            f'<span class="rosh-outcome-badge rosh-outcome-{e(conversion.aegis_outcome)}">'
            f"Aegis: {e(outcome_display)} {inferred_badge}</span>"
            f'<span class="rosh-fate">Lifecycle: {e(fate_display)} · '
            f"{e(fate_source_display)}</span>"
            f"{_analysis_status_html(conversion)}"
            "</div></header>"
            '<div class="rosh-tags" aria-label="Non-exclusive conversion tags">'
            f"{_tag_chips(conversion.conversion_tags)}</div>"
            '<div class="rosh-core-grid">'
            f"{_balance_panel(conversion)}{_resource_panel(conversion)}</div>"
            f"{_territory_panel(match, conversion, map_b64)}"
            f"{_timeline_html(conversion)}"
            "</article>"
        )

    parts.append("</div>")
    parts.append('<div class="rosh-table-wrap"><table class="rosh-summary-table">')
    parts.append(
        "<thead><tr><th>Rosh</th><th>Conversion / Holder</th><th>Aegis</th><th>Drops</th>"
        "<th>Tags</th>"
        '<th class="r">Fight Δ</th><th class="r">Structure Δ</th>'
        '<th class="r">NW swing</th><th class="r">XP swing</th>'
        '<th class="r">Coverage Δ</th><th class="r">Depth Δ</th>'
        '<th class="r">Ward Δ</th><th class="r">Tormentor Δ</th>'
        "<th>Banner</th><th>Status</th></tr></thead><tbody>"
    )
    for conversion in conversions:
        profile = conversion.differential_profile
        team = (
            conversion.conversion_team
            if conversion.conversion_team in (2, 3)
            else conversion.holder_team
        )
        team_color = TEAM_COLOR_CSS.get(team or 0, "#8b949e")
        team_label = team_name(team) if team in (2, 3) else "Unknown"
        holder_label = hero(conversion.holder_name) if conversion.holder_name else "Unknown"
        outcome_display = _ROSH_AEGIS_OUTCOME_DISPLAY.get(
            conversion.aegis_outcome,
            _display_token(conversion.aegis_outcome),
        )
        drops_cell = _rosh_drops_display(conversion.drops)
        if conversion.had_high_value_drop:
            drops_cell += " ★"
        tags_cell = (
            ", ".join(
                _ROSH_TAG_DISPLAY.get(tag, _display_token(tag))
                for tag in conversion.conversion_tags
            )
            or "None"
        )
        banner_cell = "—"
        if conversion.banner_planted:
            banner_cell = "Planted"
        if conversion.banner_rax_conversion:
            lane = f" {conversion.banner_rax_lane.title()}" if conversion.banner_rax_lane else ""
            banner_cell = f"⚑ Rax{lane}"
        reasons = "; ".join(_display_token(reason) for reason in conversion.analysis_status_reasons)
        status_cell = _display_token(conversion.analysis_status)
        if reasons:
            status_cell += f": {reasons}"
        parts.append(
            "<tr>"
            f"<td>#{conversion.rosh_number}</td>"
            f'<td><span style="color:{team_color}">{e(team_label)}</span> / {e(holder_label)}</td>'
            f"<td>{e(outcome_display)}</td><td>{e(drops_cell)}</td><td>{e(tags_cell)}</td>"
            f'<td class="r">{_summary_metric(profile.fight_differential)}</td>'
            f'<td class="r">{_summary_metric(profile.structure_delta)}</td>'
            f'<td class="r">{_summary_metric(profile.net_worth_swing)}</td>'
            f'<td class="r">{_summary_metric(profile.xp_swing)}</td>'
            f'<td class="r">{_summary_metric(profile.coverage_swing_pct, decimals=1, suffix=" pp")}</td>'
            f'<td class="r">{_summary_metric(profile.depth_swing, decimals=3)}</td>'
            f'<td class="r">{_summary_metric(profile.forward_ward_delta)}</td>'
            f'<td class="r">{_summary_metric(profile.tormentor_delta)}</td>'
            f"<td>{e(banner_cell)}</td><td>{e(status_cell)}</td></tr>"
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
            channel_label = {"all": "ALL", "team": "TEAM"}.get(msg.channel, f"CH {msg.channel}")
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
