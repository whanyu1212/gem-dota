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
    tick_after_game_seconds,
)
from gem.reports.assets import (
    has_hero_icon,
    hero_icon_src,
    load_hero_icons,
)
from gem.reports.player_names import display_player_name
from gem.reports.sections._shared import fight_numbers, fight_outcome
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
)

if TYPE_CHECKING:
    from gem.analysis.roshan import RoshConversion
    from gem.combat.log import CombatLogEntry


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


def _rune_type(entry: CombatLogEntry) -> int:
    """Return a PICKUP_RUNE entry's rune code.

    Matches loaded from JSON written before ``rune_type`` existed keep the code
    only in ``gold_reason``.
    """
    return entry.rune_type if entry.rune_type is not None else entry.gold_reason


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
            if _rune_type(entry) == 8:  # Wisdom rune
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
    "game_end": "Held to game end",
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


def _team_span(team: int | None, text: str) -> str:
    color = TEAM_COLOR_CSS.get(team or 0, "#8b949e")
    return f'<span style="color:{color}">{e(text)}</span>'


def _aegis_cells(match: ParsedMatch, conversion: RoshConversion, numbers: dict[int, int]) -> str:
    """Render the Aegis holder, its end, and the fights and buildings while it was held."""
    if conversion.aegis_pickup_tick is None or conversion.aegis_fate == "denied":
        # A denied Aegis is never held, whatever tick the denial was recorded at.
        if conversion.aegis_fate == "denied":
            label = "Denied"
            ended = f'Denied<br><span class="dim">{e(fmt_tick(conversion.aegis_end_tick))}</span>'
        else:
            label = "Not picked up"
            ended = e(_ROSH_FATE_DISPLAY.get(conversion.aegis_fate, conversion.aegis_fate))
        return f'<td class="dim">{label}</td><td>{ended}</td><td>—</td><td>—</td>'
    holder = hero(conversion.holder_name) if conversion.holder_name else "Unknown"
    holder_html = (
        f"{_team_span(conversion.holder_team, holder)}"
        f'<br><span class="dim">picked up {e(fmt_tick(conversion.aegis_pickup_tick))}</span>'
    )
    fate = _ROSH_FATE_DISPLAY.get(conversion.aegis_fate, conversion.aegis_fate)
    if conversion.aegis_fate_inferred:
        fate += "*"
    ended_html = f'{e(fate)}<br><span class="dim">{e(fmt_tick(conversion.aegis_end_tick))}</span>'

    start, end = conversion.aegis_pickup_tick, conversion.aegis_end_tick
    fights = [
        fight for fight in match.fights or [] if fight.start_tick <= end and start <= fight.end_tick
    ]
    fight_links = []
    for fight in fights:
        number = numbers[id(fight)]
        outcome = fight_outcome(fight.winner)
        fight_links.append(
            f'<a class="smoke-fight-link" href="#fight-{number}" '
            f'data-report-target="fight-{number}" data-report-snapshot="engagement_start">'
            f'Fight #{number}</a> <span class="dim">{e(outcome)}</span>'
        )
    fights_html = "<br>".join(fight_links) or '<span class="dim">None</span>'

    enemy = {2: 3, 3: 2}.get(conversion.holder_team or 0)
    towers = sum(start <= tower.tick <= end and tower.team == enemy for tower in match.towers)
    barracks = sum(start <= rax.tick <= end and rax.team == enemy for rax in match.barracks)
    buildings = [
        f"{count} {singular if count == 1 else plural}"
        for count, singular, plural in (
            (towers, "tower", "towers"),
            (barracks, "barracks", "barracks"),
        )
        if count
    ]
    buildings_html = e(", ".join(buildings)) or '<span class="dim">None</span>'
    return (
        f"<td>{holder_html}</td><td>{ended_html}</td>"
        f"<td>{fights_html}</td><td>{buildings_html}</td>"
    )


def build_rosh_conversion(
    match: ParsedMatch,
    conversions: list[RoshConversion] | None = None,
) -> str:
    """Build the Roshan tab: each kill, its drops, and what happened while the Aegis was held.

    Args:
        match: Parsed match carrying Roshan kills, Aegis events, fights and buildings.
        conversions: Optional precomputed :func:`gem.build_rosh_conversions`
            records, shared with the Fights tab. Only their kill and Aegis
            lifecycle facts are shown.

    Returns:
        Self-contained HTML for the Roshan tab, or an empty string when the
        match has no Roshan kills.
    """
    if conversions is None:
        conversions = build_rosh_conversions(match)
    if not conversions:
        return ""
    numbers = fight_numbers(match)

    rows = []
    for conversion in conversions:
        killer_team = conversion.roshan_team
        killed_by = team_name(killer_team) if killer_team in (2, 3) else "Unknown"
        killer = _killer_label(conversion.killer_name) if conversion.killer_name else ""
        killer_html = f'<br><span class="dim">{e(killer)}</span>' if killer else ""
        rows.append(
            f'<tr id="roshan-{conversion.rosh_number}">'
            f'<td class="r"><strong>#{conversion.rosh_number}</strong></td>'
            f"<td>{e(fmt_tick(conversion.rosh_tick))}</td>"
            f"<td>{_team_span(killer_team, killed_by)}{killer_html}</td>"
            f"<td>{e(_rosh_drops_display(conversion.drops))}</td>"
            f"{_aegis_cells(match, conversion, numbers)}"
            "</tr>"
        )

    return "\n".join(
        [
            '<div class="card rosh-section">',
            "<details open>",
            "<summary>Roshan</summary>",
            '<div class="card-body">',
            '<p class="section-note">While held = from the Aegis pickup until it was '
            "consumed, expired or the game ended, or, when its end was not observed "
            "(Unknown), the next Roshan kill. Fights are those overlapping that time; "
            "buildings are the enemy's towers and barracks destroyed in it. "
            "* Consumed is inferred from the holder dying while holding the Aegis.</p>",
            '<div class="rosh-table-wrap"><table class="rosh-summary-table">',
            '<thead><tr><th class="r">#</th><th>Time</th><th>Killed by</th><th>Drops</th>'
            "<th>Aegis</th><th>Aegis ended</th><th>Fights while held</th>"
            "<th>Buildings taken while held</th></tr></thead><tbody>",
            *rows,
            "</tbody></table></div>",
            "</div>",
            "</details>",
            "</div>",
        ]
    )


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
