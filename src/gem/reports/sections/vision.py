"""Vision report sections (wards, laning, farming maps).

Split out of the former monolithic ``_sections.py`` (see that module's
shim for backward-compatible re-exports).
"""

from __future__ import annotations

import json
import math

from gem.analysis import (
    ExactEventKind,
    FarmingBoundaryReason,
    FarmingRoute,
    FarmingRoutePoint,
    SmokeFightInsight,
    SmokeFightStatus,
    SmokeLifecycleStatus,
    build_farming_routes,
    build_smoke_analysis,
    build_smoke_fight_insights,
)
from gem.catalog.map import load_camp_zones
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
    team_name,
)
from gem.reports.assets import (
    ITEM_ICON_B64,
    has_hero_icon,
    hero_icon_src,
    item_icon_tag,
    load_hero_icons,
)
from gem.reports.sections._shared import _ward_enemies_seen
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
    VisibilityState,
)


def _smoke_route(match: ParsedMatch, smoke: object) -> list[dict[str, float | int]]:
    """Build a sampled member-centroid route from recorded position samples."""
    participants = getattr(smoke, "participants", [])
    if not participants:
        return []

    start_tick = getattr(smoke, "tick", 0)
    players_by_id = {player.player_id: player for player in match.players}
    players_by_name = {player.hero_name: player for player in match.players}
    buckets: dict[int, dict[int, tuple[int, float, float]]] = {}

    for participant in participants:
        player = players_by_id.get(participant.player_id)
        if player is None:
            player = players_by_name.get(participant.hero_name)
        if player is None:
            continue
        participant_end_tick = participant.removed_tick or participant.applied_tick
        for sample_tick, x, y in player.position_log:
            if not participant.applied_tick <= sample_tick <= participant_end_tick:
                continue
            bucket = (sample_tick - start_tick) // TICKS_PER_SEC
            buckets.setdefault(bucket, {})[player.player_id] = (sample_tick, x, y)

    route: list[dict[str, float | int]] = []
    for samples in buckets.values():
        if not samples:
            continue
        ticks = [sample[0] for sample in samples.values()]
        xs = [sample[1] for sample in samples.values()]
        ys = [sample[2] for sample in samples.values()]
        route.append(
            {
                "tick": round(sum(ticks) / len(ticks)),
                "fx": round((sum(xs) / len(xs) - MAP_XMIN) / (MAP_XMAX - MAP_XMIN), 5),
                "fy": round(1.0 - (sum(ys) / len(ys) - MAP_YMIN) / (MAP_YMAX - MAP_YMIN), 5),
            }
        )
    route.sort(key=lambda point: point["tick"])
    return route


def _visibility_badge(state: VisibilityState) -> str:
    """Render authoritative enemy visibility without collapsing unknown state."""
    if state is VisibilityState.VISIBLE:
        return '<span style="color:#ff7b72">Visible to enemy</span>'
    if state is VisibilityState.HIDDEN:
        return '<span style="color:#bc8cff">Hidden from enemy</span>'
    return '<span style="color:#8b949e">Visibility unknown</span>'


def _insight_delta(event: object) -> str:
    """Format an activation-relative exact event without hiding time provenance."""
    game_time_delta_s = getattr(event, "game_time_delta_s", None)
    if game_time_delta_s is not None:
        return f"{game_time_delta_s:+d}s"
    tick_delta = getattr(event, "tick_delta", 0)
    return (
        f'<span title="Tick-derived from {tick_delta:+d} replay ticks">'
        f"{tick_delta / TICKS_PER_SEC:+.1f}s*</span>"
    )


def _smoke_fight_html(insights: list[SmokeFightInsight]) -> str:
    """Render composed smoke/fight records without recomputing association rules."""
    if not insights:
        return "—"

    status_labels = {
        SmokeFightStatus.LINKED: "Linked",
        SmokeFightStatus.TEMPORAL_ONLY: "Temporal only",
        SmokeFightStatus.AMBIGUOUS: "Ambiguous",
        SmokeFightStatus.PREEXISTING: "Pre-existing",
        SmokeFightStatus.NO_CANDIDATE: "No candidate",
    }
    event_labels = {
        ExactEventKind.MEMBER_REMOVAL: "Removal",
        ExactEventKind.AUTHORITATIVE_VISIBLE: "Visible",
        ExactEventKind.DIRECT_REVEAL: "Direct reveal",
        ExactEventKind.MEMBER_ACTION: "Action",
        ExactEventKind.FIRST_DEATH: "First death",
        ExactEventKind.FIGHT_END: "Fight end",
    }
    blocks: list[str] = []
    for insight in insights:
        visible = sum(
            member.authoritative_visibility is VisibilityState.VISIBLE for member in insight.members
        )
        hidden = sum(
            member.authoritative_visibility is VisibilityState.HIDDEN for member in insight.members
        )
        unknown = len(insight.members) - visible - hidden
        sequence = " · ".join(
            f"{event_labels[event.kind]} {_insight_delta(event)}"
            for event in insight.exact_events
            if event.kind is not ExactEventKind.ACTIVATION
        )
        if not sequence:
            sequence = "No later exact event observed"

        link = ""
        if insight.fight_index is not None:
            fight_number = insight.fight_index + 1
            link = (
                f'<a class="smoke-fight-link" href="#fight-{fight_number}" '
                f'data-report-target="fight-{fight_number}" '
                'data-report-snapshot="engagement_start">'
                f"View Fight #{fight_number}</a>"
            )
        gap_html = ""
        if insight.evidence_gaps:
            gap_html = (
                f'<div class="smoke-fight-gaps">Incomplete evidence: '
                f"{e(', '.join(insight.evidence_gaps))}</div>"
            )
        active_count = len(insight.active_smoked_player_ids)
        blocks.append(
            '<div class="smoke-fight-insight">'
            f'<div><span class="smoke-fight-status status-{insight.status.value}">'
            f"{status_labels[insight.status]}</span>"
            f'<span class="dim"> · {active_count} active smoked member'
            f"{'' if active_count == 1 else 's'}</span></div>"
            f'<div class="smoke-fight-visibility">Visible {visible} · Hidden {hidden} · '
            f"Unknown {unknown}</div>"
            f'<div class="smoke-fight-sequence">{sequence}</div>'
            f"{link}{gap_html}</div>"
        )
    return "".join(blocks)


def build_smokes(
    match: ParsedMatch,
    map_b64: str | None,
    insights: list[SmokeFightInsight] | None = None,
) -> str:
    """Build evidence-first Smoke of Deceit lifecycle analysis."""
    analyses = build_smoke_analysis(match)
    if not analyses:
        return ""
    if insights is None:
        insights = build_smoke_fight_insights(match)
    insights_by_smoke: dict[int, list[SmokeFightInsight]] = {}
    for insight in insights:
        insights_by_smoke.setdefault(insight.smoke_index, []).append(insight)

    map_events: list[dict[str, object]] = []
    rows: list[str] = []
    member_details: list[str] = []

    status_labels = {
        "no_members_observed": ("No members observed", "#8b949e"),
        "early_removal": ("Early removal", "#d29922"),
        "expired": ("Expired", "#3fb950"),
        "incomplete": ("Incomplete", "#8b949e"),
    }

    for index, analysis in enumerate(analyses, start=1):
        raw = match.smoke_events[index - 1] if index <= len(match.smoke_events) else None
        status_value = analysis.status.value
        status_label, status_color = status_labels[status_value]
        early_members = sorted(
            (
                member
                for member in analysis.members
                if member.lifecycle_status is SmokeLifecycleStatus.EARLY
                and member.removed_tick is not None
            ),
            key=lambda member: member.removed_tick or 0,
        )
        first_early = early_members[0] if early_members else None

        if first_early is None:
            early_html = "—"
            visibility_html = "—"
            nearest_html = "—"
        else:
            removed_tick = first_early.removed_tick or analysis.activation_tick
            elapsed_s = (removed_tick - analysis.activation_tick) / TICKS_PER_SEC
            early_html = (
                f'{e(hero(first_early.hero_name))}<br><span class="dim" '
                f'title="Replay tick {removed_tick}">{e(fmt_tick(removed_tick))} '
                f"(+{elapsed_s:.2f}s)</span>"
            )
            visibility_html = _visibility_badge(first_early.visibility_at_remove)
            if first_early.nearest_enemy_hero and first_early.nearest_enemy_distance is not None:
                nearest_html = (
                    f"{e(hero(first_early.nearest_enemy_hero))}<br>"
                    f'<span class="dim">{first_early.nearest_enemy_distance:,.0f}u sampled</span>'
                )
            else:
                nearest_html = '<span class="dim">Unavailable</span>'

        members_html = ", ".join(e(hero(member.hero_name)) for member in analysis.members) or "—"
        team_color = TEAM_COLOR_CSS.get(analysis.team, "#8b949e")
        team_html = (
            f'<span style="color:{team_color}">{e(team_name(analysis.team))}</span><br>'
            f'<span class="dim">{e(hero(analysis.activator))}</span>'
        )
        fight_html = _smoke_fight_html(insights_by_smoke.get(index - 1, []))

        rows.append(
            f'<tr id="smoke-operation-{index}">'
            f'<td class="r"><strong>#{index}</strong><br><span title="Replay tick '
            f'{analysis.activation_tick}">{e(fmt_tick(analysis.activation_tick))}</span></td>'
            f"<td>{team_html}</td>"
            f"<td>{members_html}</td>"
            f'<td><span style="color:{status_color}">{status_label}</span></td>'
            f"<td>{early_html}</td><td>{visibility_html}</td>"
            f"<td>{nearest_html}</td><td>{fight_html}</td>"
            "</tr>"
        )

        detail_rows = []
        raw_participants = {
            (participant.hero_name, participant.applied_tick): participant
            for participant in getattr(raw, "participants", [])
        }
        for member in analysis.members:
            participant = raw_participants.get((member.hero_name, member.applied_tick))
            end_html = "Unobserved"
            if member.removed_tick is not None:
                elapsed_s = (member.removed_tick - member.applied_tick) / TICKS_PER_SEC
                end_html = (
                    f'<span title="Replay tick {member.removed_tick}">'
                    f"{e(fmt_tick(member.removed_tick))} (+{elapsed_s:.2f}s)</span>"
                )
            duration_html = "—"
            if participant is not None and participant.modifier_duration_s is not None:
                duration_html = f"{participant.modifier_duration_s:.2f}s"
            evidence = []
            if member.same_tick_actions:
                evidence.append("action at same tick")
            if member.same_tick_deaths:
                evidence.append("death at same tick")
            evidence_html = ", ".join(evidence) or "—"
            detail_rows.append(
                "<tr>"
                f"<td>{e(hero(member.hero_name))}</td>"
                f'<td title="Replay tick {member.applied_tick}">{e(fmt_tick(member.applied_tick))}</td>'
                f"<td>{end_html}</td><td>{duration_html}</td>"
                f"<td>{_visibility_badge(member.visibility_at_apply)}</td>"
                f"<td>{_visibility_badge(member.visibility_at_remove)}</td>"
                f"<td>{evidence_html}</td>"
                "</tr>"
            )
        if not detail_rows:
            detail_rows.append(
                '<tr><td colspan="7" class="dim">No smoke members observed.</td></tr>'
            )
        member_details.append(
            f'<details style="margin-top:8px"><summary>#{index} member timing</summary>'
            '<table style="margin-top:8px"><thead><tr><th>Hero</th><th>Applied</th>'
            "<th>Removed</th><th>Expected duration</th><th>At apply</th>"
            f"<th>At removal</th><th>Same-tick evidence</th></tr></thead><tbody>{''.join(detail_rows)}"
            "</tbody></table></details>"
        )

        activation_x = analysis.activation_x
        activation_y = analysis.activation_y
        first_early_position = None
        if first_early is not None and raw is not None:
            for participant in raw.participants:
                if (
                    participant.hero_name == first_early.hero_name
                    and participant.removed_tick == first_early.removed_tick
                    and participant.removed_x is not None
                    and participant.removed_y is not None
                ):
                    first_early_position = {
                        "fx": round((participant.removed_x - MAP_XMIN) / (MAP_XMAX - MAP_XMIN), 5),
                        "fy": round(
                            1.0 - (participant.removed_y - MAP_YMIN) / (MAP_YMAX - MAP_YMIN),
                            5,
                        ),
                    }
                    break
        map_events.append(
            {
                "number": index,
                "team": analysis.team,
                "start": (
                    {
                        "fx": round((activation_x - MAP_XMIN) / (MAP_XMAX - MAP_XMIN), 5),
                        "fy": round(1.0 - (activation_y - MAP_YMIN) / (MAP_YMAX - MAP_YMIN), 5),
                    }
                    if activation_x is not None and activation_y is not None
                    else None
                ),
                "route": _smoke_route(match, raw) if raw is not None else [],
                "early": first_early_position,
            }
        )

    config = json.dumps({"events": map_events, "hasMap": bool(map_b64)}).replace("</", "<\\/")
    located_count = sum(bool(event["start"] or event["route"]) for event in map_events)
    map_html = ""
    if located_count:
        map_html = f"""
<div style="margin:14px 0">
  <canvas id="smokeCanvas" width="700" height="700"
    style="max-width:700px;width:100%;aspect-ratio:1;border:1px solid #30363d;border-radius:6px;display:block"></canvas>
  <p class="dim" style="font-size:12px;margin-top:6px">Solid dots mark activation, lines are sampled member centroids, and × marks the first observed early removal. Spatial samples are lower precision than combat-log ticks.</p>
</div>
<script type="application/json" id="smoke-data">{config}</script>
<script>
(function() {{
  var cfg = JSON.parse(document.getElementById('smoke-data').textContent || '{{}}');
  var canvas = document.getElementById('smokeCanvas');
  var ctx = canvas.getContext('2d');
  var mapImg = new Image();
  function draw() {{
    var W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);
    if (mapImg.complete && mapImg.naturalWidth > 0) ctx.drawImage(mapImg, 0, 0, W, H);
    else {{ ctx.fillStyle = '#111820'; ctx.fillRect(0, 0, W, H); }}
    (cfg.events || []).forEach(function(ev) {{
      var color = ev.team === 2 ? '#3fb950' : ev.team === 3 ? '#f85149' : '#8b949e';
      if (ev.route && ev.route.length) {{
        ctx.beginPath();
        ev.route.forEach(function(p, i) {{
          if (i === 0) ctx.moveTo(p.fx * W, p.fy * H);
          else ctx.lineTo(p.fx * W, p.fy * H);
        }});
        ctx.strokeStyle = color; ctx.globalAlpha = 0.85; ctx.lineWidth = 4; ctx.stroke();
      }}
      if (ev.start) {{
        var x = ev.start.fx * W, y = ev.start.fy * H;
        ctx.globalAlpha = 1; ctx.beginPath(); ctx.arc(x, y, 10, 0, 2 * Math.PI);
        ctx.fillStyle = color; ctx.fill(); ctx.fillStyle = '#fff';
        ctx.font = 'bold 11px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(ev.number, x, y);
      }}
      if (ev.early) {{
        var x = ev.early.fx * W, y = ev.early.fy * H;
        ctx.globalAlpha = 1; ctx.strokeStyle = '#ffd33d'; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(x - 7, y - 7); ctx.lineTo(x + 7, y + 7);
        ctx.moveTo(x + 7, y - 7); ctx.lineTo(x - 7, y + 7); ctx.stroke();
      }}
    }});
  }}
  mapImg.onload = draw;
  if (cfg.hasMap && window._GEM_MAP_SRC) mapImg.src = window._GEM_MAP_SRC;
  else draw();
}})();
</script>"""

    return (
        '<div class="card"><details open><summary>Smoke Operations</summary><div class="card-body">'
        '<p class="dim">Modifier removal, authoritative enemy visibility, sampled proximity, and bounded fight links are reported as separate evidence. Early removal does not by itself prove the hero was seen. * marks tick-derived elapsed time.</p>'
        + map_html
        + '<div style="overflow-x:auto"><table><thead><tr><th class="r">Activation</th><th>Team / activator</th>'
        "<th>Members</th><th>Lifecycle</th><th>First early removal</th>"
        "<th>Enemy state</th><th>Nearest enemy</th><th>Bounded fight evidence</th>"
        f"</tr></thead><tbody>{''.join(rows)}</tbody></table></div>{''.join(member_details)}"
        "</div></details></div>"
    )


def build_wards(match: ParsedMatch, map_b64: str | None) -> str:
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

    # Bundle every value that crosses the Python -> JS boundary into a single
    # inert ``<script type="application/json">`` config tag (mirrors the cleaner
    # ``build_farming`` pattern in this file). The executable ``<script>`` below
    # reads this tag via ``JSON.parse`` instead of having data interpolated into
    # it, so its body stays a plain string with natural single braces.
    ward_config = {
        "wards": ward_data,
        "gameStartTick": match.game_start_tick or 0,
        "sliderMin": slider_min,
        "sliderMax": slider_max,
        "worldWidth": _XMAX - _XMIN,
        "hasMap": bool(map_b64),
        "iconObs": ITEM_ICON_B64.get("ward_observer", ""),
        "iconSen": ITEM_ICON_B64.get("ward_sentry", ""),
    }
    # ``</`` is escaped so a stray ``</script>`` substring in the data cannot
    # close the data tag early (defensive; base64/JSON values won't contain it).
    ward_config_js = json.dumps(ward_config).replace("</", "<\\/")

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
<script type="application/json" id="ward-data">{ward_config_js}</script>
"""

    ward_script = """
<script>
(function() {
  var cfg = JSON.parse(document.getElementById('ward-data').textContent || '{}');
  var wards = cfg.wards || [];
  var imgSrc = cfg.hasMap ? (window._GEM_MAP_SRC || '') : '';
  var iconObsSrc = cfg.iconObs || '';
  var iconSenSrc = cfg.iconSen || '';
  var gameStartTick = cfg.gameStartTick || 0;
  var sliderMin = cfg.sliderMin || 0;
  var sliderMax = cfg.sliderMax || 0;
  var WORLD_WIDTH = cfg.worldWidth;
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
  mapImg.onload = function() { draw(currentTick); };
  if (imgSrc) { mapImg.src = imgSrc; }

  function _makeIcon(src) {
    var img = new Image();
    if (src) img.src = src;
    return img;
  }
  var iconObs = _makeIcon(iconObsSrc);
  var iconSen = _makeIcon(iconSenSrc);

  function fmtTick(tick) {
    var rel = tick - gameStartTick;
    var neg = rel < 0;
    var secs = Math.floor(Math.abs(rel) / 30);
    var m = Math.floor(secs / 60), s = secs % 60;
    var t = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    return neg ? '-' + t : t;
  }

  function draw(tick) {
    ctx.clearRect(0, 0, W, H);

    if (mapImg.complete && mapImg.naturalWidth > 0) {
      ctx.drawImage(mapImg, 0, 0, W, H);
    } else {
      ctx.fillStyle = '#1a2a1a';
      ctx.fillRect(0, 0, W, H);
    }


    function drawIcon(img, cx, cy, size, borderColor, alpha) {
      var half = size / 2;
      ctx.save();
      ctx.globalAlpha = alpha !== undefined ? alpha : 1.0;
      if (img && img.complete && img.naturalWidth > 0) {
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
      } else {
        ctx.beginPath();
        ctx.arc(cx, cy, half, 0, 2 * Math.PI);
        ctx.fillStyle = borderColor;
        ctx.fill();
      }
      ctx.restore();
    }

    for (var i = 0; i < wards.length; i++) {
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
    }

  }

  function setTick(tick) {
    currentTick = Math.max(sliderMin, Math.min(sliderMax, tick));
    slider.value = currentTick;
    timeLabel.textContent = fmtTick(currentTick);
    draw(currentTick);
  }

  function animFrame(ts) {
    if (!playing) return;
    if (lastTs !== null) {
      var speed = parseInt(speedSel.value) || 5;
      var delta = (ts - lastTs) * speed * 30 / 1000;
      currentTick = Math.min(sliderMax, currentTick + delta);
      slider.value = currentTick;
      timeLabel.textContent = fmtTick(Math.floor(currentTick));
      draw(Math.floor(currentTick));
      if (currentTick >= sliderMax) {
        playing = false;
        playBtn.textContent = '\u25b6';
        lastTs = null;
        return;
      }
    }
    lastTs = ts;
    requestAnimationFrame(animFrame);
  }

  playBtn.addEventListener('click', function() {
    if (playing) {
      playing = false;
      lastTs = null;
      playBtn.textContent = '\u25b6';
    } else {
      if (currentTick >= sliderMax) setTick(sliderMin);
      playing = true;
      playBtn.textContent = '\u23f8';
      lastTs = null;
      requestAnimationFrame(animFrame);
    }
  });

  slider.addEventListener('input', function() {
    playing = false;
    lastTs = null;
    playBtn.textContent = '\u25b6';
    currentTick = parseInt(this.value);
    timeLabel.textContent = fmtTick(currentTick);
    draw(currentTick);
    tooltip.innerHTML = '';
  });

  canvas.addEventListener('mousemove', function(e) {
    var rect = canvas.getBoundingClientRect();
    var mx = (e.clientX - rect.left) * (W / rect.width);
    var my = (e.clientY - rect.top) * (H / rect.height);
    var hit = null, hitType = null, bestDist = 12;

    for (var i = 0; i < wards.length; i++) {
      var w = wards[i];
      if (currentTick < w.placed) continue;
      if (w.removed !== null && currentTick > w.removed) continue;
      var dx = w.fx * W - mx, dy = w.fy * H - my;
      var dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < bestDist) { bestDist = dist; hit = w; hitType = 'ward'; }
    }
    if (hit && hitType === 'ward') {
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
    } else {
      tooltip.innerHTML = '';
      canvas.style.cursor = 'crosshair';
    }
  });
})();
</script>"""

    parts.append(canvas_html)
    parts.append(ward_script)

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


_LANE_ROLE_NAMES: dict[int, str] = {
    1: "Safe",
    2: "Mid",
    3: "Off",
    4: "Jungle",
    5: "Roaming",
    0: "—",
}


_LANE_COLORS: dict[int, str] = {
    1: "#4caf50",
    2: "#58a6ff",
    3: "#f44336",
    4: "#ff9800",
    5: "#ab47bc",
}


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
    match: ParsedMatch,
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


def build_laning(match: ParsedMatch, map_b64: str | None = None) -> str:
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

        hero_img = (
            f'<img src="{hero_icon_src(pp.hero_name)}" width="20" height="12" '
            f'style="object-fit:cover;border-radius:2px;vertical-align:middle;margin-right:5px">'
            if has_hero_icon(pp.hero_name)
            else ""
        )
        hero_cell_html = (
            f'{hero_img}<span style="color:{team_color}">{e(hero(pp.hero_name))}</span>'
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


_FARM_CAMP_COLORS: dict[str, str] = {
    "ancient": "#fbc02d",
    "large": "#ef5350",
    "medium": "#66bb6a",
    "small": "#42a5f5",
    "flooded_medium": "#ab47bc",
    "flooded_small": "#5c6bc0",
}


_FARM_TEAM_TRAIL: dict[int, str] = {2: "#7ee787", 3: "#ff7b72"}


def _load_camp_zones() -> dict:
    try:
        obj = load_camp_zones()
        camps = obj.get("camps", [])
        if isinstance(camps, list):
            return obj
    except (OSError, ValueError):
        # Bundled-asset load failure (missing file / malformed JSON): the camp
        # overlay is optional, so fall back to an empty set rather than failing
        # the whole report. (json.JSONDecodeError is a ValueError subclass.)
        pass
    return {"camps": []}


def _farm_world_to_px(wx: float, wy: float, size: int) -> tuple[float, float]:
    px = (wx - MAP_XMIN) / (MAP_XMAX - MAP_XMIN) * size
    py = (1.0 - (wy - MAP_YMIN) / (MAP_YMAX - MAP_YMIN)) * size
    return px, py


def _farm_smooth_chunk(points: list[dict]) -> str:
    if not points:
        return ""
    if len(points) == 1:
        return f"M {float(points[0]['px']):.1f} {float(points[0]['py']):.1f}"
    if len(points) == 2:
        return (
            f"M {float(points[0]['px']):.1f} {float(points[0]['py']):.1f} "
            f"L {float(points[1]['px']):.1f} {float(points[1]['py']):.1f}"
        )

    cmds = [f"M {float(points[0]['px']):.1f} {float(points[0]['py']):.1f}"]
    for idx in range(1, len(points) - 1):
        x1 = float(points[idx]["px"])
        y1 = float(points[idx]["py"])
        x2 = float(points[idx + 1]["px"])
        y2 = float(points[idx + 1]["py"])
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        cmds.append(f"Q {x1:.1f} {y1:.1f} {mx:.1f} {my:.1f}")
    prev = points[-2]
    last = points[-1]
    cmds.append(
        f"Q {float(prev['px']):.1f} {float(prev['py']):.1f} "
        f"{float(last['px']):.1f} {float(last['py']):.1f}"
    )
    return " ".join(cmds)


def _farm_smooth_path(points: list[dict]) -> str:
    chunks: list[list[dict]] = []
    current: list[dict] = []
    for point in points:
        if point.get("break_before") and current:
            chunks.append(current)
            current = []
        current.append(point)
    if current:
        chunks.append(current)
    return " ".join(_farm_smooth_chunk(chunk) for chunk in chunks)


def _downsample_farming_route_points(
    points: list[FarmingRoutePoint],
    *,
    target_count: int = 1400,
) -> list[FarmingRoutePoint]:
    """Thin long routes without discarding observed discontinuities.

    ``target_count`` is a soft rendering budget: breakpoints and the samples
    immediately before them are retained even when that makes the result a few
    points larger. This prevents the rendered path from bridging sample gaps or
    large position jumps that the route analysis explicitly preserved.
    """
    if len(points) <= target_count:
        return list(points)

    step = max(1, math.ceil(len(points) / target_count))
    selected_indices = set(range(0, len(points), step))
    selected_indices.add(len(points) - 1)
    discontinuities = {
        FarmingBoundaryReason.SAMPLE_GAP,
        FarmingBoundaryReason.LARGE_JUMP,
    }
    for index, point in enumerate(points):
        if point.boundary_before in discontinuities:
            selected_indices.add(index)
            if index > 0:
                selected_indices.add(index - 1)

    return [points[index] for index in sorted(selected_indices)]


def _build_farming_map_svg(
    *,
    player: ParsedPlayer,
    route: FarmingRoute,
    camps: list[dict],
    visits: list[dict],
    map_b64: str | None,
    start_tick: int = 0,
    size: int = 680,
) -> tuple[str, list[dict]]:
    bg_img = (
        f'<image class="gem-map-bg" href="" x="0" y="0" width="{size}" height="{size}" '
        f'preserveAspectRatio="xMidYMid slice"/>'
        if map_b64
        else f'<rect x="0" y="0" width="{size}" height="{size}" fill="#0d1117"/>'
    )

    camp_elements: list[str] = []

    for camp in camps:
        center = camp["center"]
        cx, cy = _farm_world_to_px(float(center["x"]), float(center["y"]), size)
        zone = camp.get("zone", {})
        rx_w = float(zone.get("rx", 600.0))
        ry_w = float(zone.get("ry", 520.0))
        rx = rx_w / (MAP_XMAX - MAP_XMIN) * size
        ry = ry_w / (MAP_YMAX - MAP_YMIN) * size
        color = _FARM_CAMP_COLORS.get(str(camp["type"]), "#58a6ff")
        visited = any(int(v["camp_id"]) == int(camp["id"]) for v in visits)
        fill_opacity = "0.22" if visited else "0.08"
        stroke_opacity = "0.95" if visited else "0.35"
        stroke_w = "1.8" if visited else "1"

        camp_elements.append(
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="{color}" fill-opacity="{fill_opacity}" '
            f'stroke="{color}" stroke-opacity="{stroke_opacity}" stroke-width="{stroke_w}"/>'
        )

    raw_points = [point for point in route.points if point.tick >= start_tick]
    if not raw_points:
        raw_points = list(route.points)
    trail_points = _downsample_farming_route_points(raw_points)

    timeline_points: list[dict] = []
    for point in trail_points:
        px, py = _farm_world_to_px(point.x, point.y, size)
        timeline_points.append(
            {
                "tick": point.tick,
                "time": fmt_tick(point.tick),
                "px": round(px, 1),
                "py": round(py, 1),
                "camp_id": point.camp_id,
                "camp_type": point.camp_type or "",
                "break_before": (
                    point.boundary_before is not None
                    and point.boundary_before.value in {"sample_gap", "large_jump"}
                ),
            }
        )
    path_d = _farm_smooth_path(timeline_points)
    trail_base = ""
    trail_active = ""
    if path_d:
        color = _FARM_TEAM_TRAIL.get(player.team, "#58a6ff")
        trail_base = (
            f'<path d="{path_d}" fill="none" stroke="{color}" '
            f'stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0.08"/>'
            f'<path d="{path_d}" fill="none" stroke="{color}" '
            f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="0.24"/>'
        )
        first_path = _farm_smooth_path([timeline_points[0]])
        trail_active = (
            f'<path id="farm-active-trail-under-{player.player_id}" d="{first_path}" '
            f'fill="none" stroke="#0d1117" stroke-width="6.6" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="0.38"/>'
            f'<path id="farm-active-trail-{player.player_id}" d="{first_path}" '
            f'fill="none" stroke="{color}" stroke-width="3.8" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="0.96"/>'
        )

    markers = ""
    if timeline_points:
        sx = float(timeline_points[0]["px"])
        sy = float(timeline_points[0]["py"])
        ex = float(timeline_points[-1]["px"])
        ey = float(timeline_points[-1]["py"])
        markers = (
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4.5" fill="#ffffff" stroke="#0d1117" stroke-width="1.5"/>'
            f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5.0" fill="#ffd54f" stroke="#0d1117" stroke-width="1.5"/>'
        )
    current_marker = ""
    if timeline_points:
        current_marker = (
            f'<circle id="farm-current-point-{player.player_id}" cx="{timeline_points[0]["px"]:.1f}" '
            f'cy="{timeline_points[0]["py"]:.1f}" r="6.5" fill="#f9fafb" '
            f'stroke="#0d1117" stroke-width="2"/>'
        )

    svg = (
        f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" '
        f'class="farm-map-svg" style="border-radius:10px;overflow:hidden;border:1px solid #30363d">'
        f"{bg_img}{''.join(camp_elements)}{trail_base}{trail_active}{markers}{current_marker}</svg>"
    )
    return svg, timeline_points


def build_farming(match: ParsedMatch, map_b64: str | None) -> str:
    """Build the Farming tab from evidence-first route segments."""
    context_tag_display = {
        "own_side": "Own Side",
        "enemy_side": "Enemy Side",
        "border": "Border",
        "high_enemy_presence": "High Enemy Presence",
        "vision_disadvantage": "Modeled Vision Disadvantage",
        "tower_disadvantage": "Lane Tower Disadvantage",
        "enemy_aegis_active": "Enemy Aegis Active",
        "territorial_advance": "Territorial Advance",
        "incomplete_context": "Incomplete Context",
    }
    context_tag_class = {
        "own_side": "farm-tag-safe",
        "enemy_side": "farm-tag-invade-mid",
        "border": "farm-tag-pressured",
        "high_enemy_presence": "farm-tag-invade-risk",
        "vision_disadvantage": "farm-tag-invade-risk",
        "tower_disadvantage": "farm-tag-defensive",
        "enemy_aegis_active": "farm-tag-invade-risk",
        "territorial_advance": "farm-tag-invade-safe",
        "incomplete_context": "farm-tag-unavailable",
    }
    evidence_label_display = {
        "strong_farm_evidence": "Strong Farm Evidence",
        "weak_farm_evidence": "Weak Farm Evidence",
        "transit_like": "Transit-Like",
    }
    evidence_label_class = {
        "strong_farm_evidence": "farm-evidence-strong",
        "weak_farm_evidence": "farm-evidence-weak",
        "transit_like": "farm-evidence-transit",
    }

    camps_obj = _load_camp_zones()
    camps = list(camps_obj.get("camps", []))
    if not camps:
        return ""

    routes_by_player = {route.player_id: route for route in build_farming_routes(match)}
    players = [
        player
        for player in match.players
        if player.hero_name
        and routes_by_player.get(player.player_id) is not None
        and routes_by_player[player.player_id].points
    ]
    if not players:
        return ""

    category_rows = [
        (
            "Safe Home Farm",
            "Own-side farm with good cover and low contest risk.",
            "home side and safety >= 0.68 and pressure <= 0.40 and not losing",
        ),
        (
            "Cautious Home Farm",
            "Own-side farm with contest risk, but the team is not clearly being forced inward.",
            "fallback non-invade label when the visit is not safe and not forced",
        ),
        (
            "Forced Home Farm",
            "Own-side farm because the map state is pushing the team inward.",
            "(losing and pressure >= 0.52) or (pressure >= 0.70 and not winning) or "
            "(enemy Aegis and pressure >= 0.55 and not winning) or "
            "(structural deficit and pressure >= 0.45 and not winning)",
        ),
        (
            "Safe Invade",
            "Enemy-side farm while ahead enough to own the area.",
            "invading and safety >= 0.52 and pressure <= 0.48 and tower_diff >= -0.05 "
            "and ward_diff >= -0.10 and no enemy Aegis and winning",
        ),
        (
            "Contested Invade",
            "Enemy-side farm with contest risk, but not the most punishable invade state.",
            "fallback invade label when the visit is not safe invade and not high-risk invade",
        ),
        (
            "High-Risk Invade",
            "Enemy-side farm that looks highly punishable.",
            "invading and (pressure >= 0.70 or "
            "(enemy Aegis and (enemy presence in enemy half >= 0.35 or losing)))",
        ),
    ]
    category_rows_html = "".join(
        (f"<tr><td>{e(label)}</td><td>{e(explanation)}</td><td><code>{e(rule)}</code></td></tr>")
        for label, explanation, rule in category_rows
    )
    score_rows_html = "".join(
        (f"<tr><td>{e(label)}</td><td><code>{e(formula)}</code></td><td>{e(explanation)}</td></tr>")
        for label, formula, explanation in [
            (
                "Safety",
                "clamp(0.55 + 0.25*tower_diff + 0.20*ward_diff - 0.45*enemy_own_half "
                "- 0.20*enemy_aegis - 0.15*invading - 0.08*border_zone)",
                "Higher means the camp looks easier to hold from your team's perspective.",
            ),
            (
                "Pressure",
                "clamp(0.30 + 0.40*enemy_own_half + 0.20*enemy_river + "
                "0.20*max(0,-tower_diff) + 0.20*enemy_aegis + invade_bonus + 0.08*border_zone)",
                "Higher means the area looks more contestable or punishable.",
            ),
            (
                "Invade Bonus",
                "0.15 + 0.15*enemy_enemy_half when invading",
                "Extra pressure added only when the camp is in enemy territory.",
            ),
            (
                "Value",
                "clamp(0.5*camp_value + 0.5*evidence)",
                "Higher means the camp is more economically valuable or better supported by neutral/XP evidence.",
            ),
        ]
    )
    derived_rows_html = "".join(
        (f"<tr><td>{e(label)}</td><td><code>{e(formula)}</code></td><td>{e(explanation)}</td></tr>")
        for label, formula, explanation in [
            (
                "tower_diff",
                "(own_towers - enemy_towers) / 11",
                "Positive means your team still owns more towers.",
            ),
            (
                "ward_diff",
                "(own_observers - enemy_observers) / 6",
                "Positive means your team has better observer coverage.",
            ),
            (
                "winning",
                "NW adv >= 3500 or XP adv >= 4500",
                "Match-state shortcut for clearly ahead.",
            ),
            (
                "losing",
                "NW adv <= -3500 or XP adv <= -4500",
                "Match-state shortcut for clearly behind.",
            ),
            (
                "structural_deficit",
                "tower_diff < -0.25 or (lost mid T1 and ward_diff < -0.20)",
                "The map has opened up enough that own-side farm starts to look forced.",
            ),
            (
                "border_zone",
                "camp center in the diagonal strip abs(x - y) <= 1200",
                "Border camps are treated as slightly less safe and slightly more pressured, but they do not get a separate label.",
            ),
        ]
    )
    driver_rows_html = "".join(
        (
            "<tr>"
            f"<td><code>{e(driver)}</code></td>"
            f"<td><code>{e(trigger)}</code></td>"
            f"<td>{e(explanation)}</td>"
            "</tr>"
        )
        for driver, trigger, explanation in [
            (
                "lost_t1_mid",
                "own mid T1 is dead",
                "Your mid entrance is more open than a normal own-side farm state.",
            ),
            (
                "enemy_aegis_active",
                "Aegis active and holder team is enemy",
                "Temporary objective pressure that makes punish windows wider.",
            ),
            (
                "enemy_presence_high_own_half",
                "enemy_own_half >= 0.45",
                "Recent enemy movement density on your side of the map is high.",
            ),
            (
                "enemy_presence_high_river",
                "enemy_river >= 0.45",
                "Recent enemy movement density around the central border zone is high.",
            ),
            (
                "vision_deficit",
                "ward_diff < -0.15",
                "The enemy currently has better observer coverage than your team.",
            ),
            (
                "map_control_deficit",
                "tower_diff < -0.15",
                "Your team has lost enough towers that map ownership is materially worse.",
            ),
            (
                "border_zone_farm",
                "camp center falls in the diagonal border strip",
                "The camp is near the central boundary where ownership is naturally less stable.",
            ),
            (
                "invading_enemy_half",
                "camp is on enemy half",
                "The visit is happening in enemy-side territory.",
            ),
            (
                "high_farm_value",
                "value >= 0.70",
                "The camp is inherently valuable or strongly supported by neutral/XP evidence.",
            ),
        ]
    )
    context_guide_html = (
        '<details class="farm-guide" style="margin-top:16px">'
        "<summary>Legacy context heuristic reference</summary>"
        '<div class="farm-guide-section">'
        '<div class="farm-guide-title">Score Formulas</div>'
        '<div class="farm-table-wrap"><table class="farm-guide-table">'
        "<thead><tr><th>Score</th><th>Formula</th><th>Meaning</th></tr></thead>"
        f"<tbody>{score_rows_html}</tbody></table></div>"
        "</div>"
        '<div class="farm-guide-section">'
        '<div class="farm-guide-title">Derived Terms</div>'
        '<div class="farm-table-wrap"><table class="farm-guide-table">'
        "<thead><tr><th>Term</th><th>Formula</th><th>Meaning</th></tr></thead>"
        f"<tbody>{derived_rows_html}</tbody></table></div>"
        "</div>"
        '<div class="farm-guide-section">'
        '<div class="farm-guide-title">Category Rules</div>'
        '<div class="farm-table-wrap"><table class="farm-guide-table">'
        "<thead><tr><th>Category</th><th>Meaning</th><th>Rule</th></tr></thead>"
        f"<tbody>{category_rows_html}</tbody></table></div>"
        "</div>"
        '<div class="farm-guide-section">'
        '<div class="farm-guide-title">Driver Triggers</div>'
        '<div class="farm-table-wrap"><table class="farm-guide-table">'
        "<thead><tr><th>Driver</th><th>Trigger</th><th>Meaning</th></tr></thead>"
        f"<tbody>{driver_rows_html}</tbody></table></div>"
        "</div>"
        "</details>"
    )

    # Prioritize likely farm cores in the selector (higher final net worth first).
    players = sorted(
        players,
        key=lambda player: player.net_worth_t[-1] if player.net_worth_t else 0,
        reverse=True,
    )
    load_hero_icons([player.hero_name for player in players])

    panels: list[str] = []
    options: list[str] = []
    for idx, player in enumerate(players):
        route = routes_by_player[player.player_id]
        visits: list[dict] = []
        for segment in route.segments:
            context = segment.context
            visits.append(
                {
                    "order": segment.segment_index,
                    "start_tick": segment.start_tick,
                    "end_tick": segment.end_tick,
                    "camp_id": segment.camp_id,
                    "camp_type": segment.camp_type,
                    "duration_s": segment.duration_seconds,
                    "start_reason": segment.start_reason.value,
                    "end_reason": segment.end_reason.value,
                    "micro_exit_merged": segment.micro_exit_merged,
                    "sample_count": segment.sample_count,
                    "in_zone_sample_count": segment.in_zone_sample_count,
                    "position_coverage": segment.position_coverage,
                    "neutral_kills": segment.neutral_kills,
                    "neutral_damage": segment.neutral_damage,
                    "xp_gain": segment.window_xp_delta,
                    "gold_gain": segment.window_total_earned_gold_delta,
                    "evidence_strength": segment.evidence_strength.value,
                    "evidence_reasons": segment.evidence_reasons,
                    "evidence_gaps": segment.evidence_gaps,
                    "distance_travelled": segment.distance_travelled,
                    "camp_lane": segment.camp_lane,
                    "camp_area": segment.camp_area,
                    "camp_side": context.camp_side if context else "unknown",
                    "camp_catalog_version": segment.camp_catalog_version,
                    "camp_map_patch": segment.camp_map_patch,
                    "camp_topology_patch": segment.camp_topology_patch,
                    "context_status": context.status if context else "unavailable",
                    "context_tags": (
                        [tag.value for tag in context.tags] if context else ["incomplete_context"]
                    ),
                    "context_tag_reasons": context.tag_reasons if context else {},
                    "context_gaps": (
                        context.status_reasons if context else ["segment_context_unavailable"]
                    ),
                    "own_presence": context.own_presence_hero_seconds if context else None,
                    "enemy_presence": context.enemy_presence_hero_seconds if context else None,
                    "own_presence_coverage": (
                        context.own_presence_position_coverage if context else None
                    ),
                    "enemy_presence_coverage": (
                        context.enemy_presence_position_coverage if context else None
                    ),
                    "own_vision": context.own_point_vision_status if context else None,
                    "enemy_vision": context.enemy_point_vision_status if context else None,
                    "own_towers": context.own_relevant_towers_alive if context else None,
                    "enemy_towers": context.enemy_relevant_towers_alive if context else None,
                    "net_worth_advantage": context.net_worth_advantage if context else None,
                    "total_xp_advantage": (context.total_earned_xp_advantage if context else None),
                    "aegis_holder_team": context.aegis_holder_team if context else None,
                    "aegis_source": context.aegis_source if context else None,
                    "last_roshan_tick": context.last_roshan_tick if context else None,
                    "last_roshan_team": context.last_roshan_team if context else None,
                    "roshan_team_source": context.roshan_team_source if context else None,
                    "last_tormentor_tick": context.last_tormentor_tick if context else None,
                    "last_tormentor_team": context.last_tormentor_team if context else None,
                    "tormentor_team_source": (context.tormentor_team_source if context else None),
                    "territory_coverage_delta": (
                        context.territory_coverage_differential_pct if context else None
                    ),
                    "territory_depth_delta": (
                        context.territory_depth_differential if context else None
                    ),
                }
            )
        map_svg, timeline_points = _build_farming_map_svg(
            player=player,
            route=route,
            camps=camps,
            visits=visits,
            map_b64=map_b64,
            start_tick=match.game_start_tick or 0,
        )

        option_label = (
            f"{hero(player.hero_name)} "
            f"({team_name(player.team)}, NW {(player.net_worth_t[-1] if player.net_worth_t else 0):,})"
        )
        options.append(
            f'<option value="{player.player_id}"{" selected" if idx == 0 else ""}>{e(option_label)}</option>'
        )

        rows: list[str] = []
        visit_payload: list[dict] = []
        for visit in visits:
            context_tags = [str(tag) for tag in visit["context_tags"]]
            context_tags_html = " ".join(
                f'<span class="farm-tag {context_tag_class.get(tag, "farm-tag-pressured")}">'
                f"{e(context_tag_display.get(tag, tag.replace('_', ' ').title()))}</span>"
                for tag in context_tags
            )
            context_text = ", ".join(
                context_tag_display.get(tag, tag.replace("_", " ").title()) for tag in context_tags
            )

            def metric(value: object, *, suffix: str = "") -> str:
                if value is None:
                    return "unavailable"
                if isinstance(value, float):
                    return f"{value:.2f}{suffix}"
                return f"{value}{suffix}"

            context_parts = [
                f"topology: {visit['camp_side']}, {visit['camp_area']}/{visit['camp_lane']}",
                f"catalog: v{metric(visit['camp_catalog_version'])}, geometry "
                f"{metric(visit['camp_map_patch'])}, topology "
                f"{metric(visit['camp_topology_patch'])}",
                "local hero-seconds: "
                f"own {metric(visit['own_presence'])}, enemy {metric(visit['enemy_presence'])}",
                "position coverage: "
                f"own {metric(visit['own_presence_coverage'])}, "
                f"enemy {metric(visit['enemy_presence_coverage'])}",
                f"modeled point vision: own {metric(visit['own_vision'])}, "
                f"enemy {metric(visit['enemy_vision'])}",
                f"lane T1/T2 alive: own {metric(visit['own_towers'])}, "
                f"enemy {metric(visit['enemy_towers'])}",
                f"team advantage: NW {metric(visit['net_worth_advantage'])}, "
                f"total XP {metric(visit['total_xp_advantage'])}",
                f"Aegis: holder {metric(visit['aegis_holder_team'])}, "
                f"source {metric(visit['aegis_source'])}",
                f"last Roshan: tick {metric(visit['last_roshan_tick'])}, "
                f"team {metric(visit['last_roshan_team'])}, "
                f"source {metric(visit['roshan_team_source'])}",
                f"last Tormentor: tick {metric(visit['last_tormentor_tick'])}, "
                f"team {metric(visit['last_tormentor_team'])}, "
                f"source {metric(visit['tormentor_team_source'])}",
                f"territory delta: coverage {metric(visit['territory_coverage_delta'])}, "
                f"depth {metric(visit['territory_depth_delta'])}",
            ]
            tag_reason_map = visit["context_tag_reasons"]
            for tag in context_tags:
                reasons = tag_reason_map.get(tag, [])
                if reasons:
                    context_parts.append(f"{tag}: " + "; ".join(reasons))
            if visit["context_gaps"]:
                context_parts.append("gaps: " + ", ".join(visit["context_gaps"]))
            context_details = (
                '<details class="farm-context-details"><summary>Why these tags?</summary>'
                f"<div>{e(' · '.join(context_parts))}</div></details>"
            )

            evidence_strength = str(visit["evidence_strength"])
            evidence_text = evidence_label_display[evidence_strength]
            evidence_cls = evidence_label_class[evidence_strength]
            support_parts: list[str] = []
            if int(visit["neutral_kills"]) > 0:
                support_parts.append(f"{int(visit['neutral_kills'])} neutral kill(s)")
            if int(visit["neutral_damage"]) > 0:
                support_parts.append(f"{int(visit['neutral_damage']):,} neutral damage")
            xp_gain = visit["xp_gain"]
            gold_gain = visit["gold_gain"]
            support_parts.append(
                f"XP +{int(xp_gain):,}" if xp_gain is not None else "XP unavailable"
            )
            support_parts.append(
                f"gold +{int(gold_gain):,}" if gold_gain is not None else "gold unavailable"
            )
            support_parts.append(
                f"{int(visit['in_zone_sample_count'])}/{int(visit['sample_count'])} in-zone samples"
            )
            coverage = visit["position_coverage"]
            if coverage is not None:
                support_parts.append(f"{float(coverage):.0%} sampled-window coverage")
            distance_travelled = visit["distance_travelled"]
            if distance_travelled is not None:
                support_parts.append(f"{float(distance_travelled):,.0f} units travelled")
            support_parts.append(f"{visit['start_reason']} → {visit['end_reason']}")
            if bool(visit["micro_exit_merged"]):
                support_parts.append("micro-exit merged")
            if visit["evidence_gaps"]:
                support_parts.append("gaps: " + ", ".join(visit["evidence_gaps"]))
            support_text = ", ".join(support_parts)
            visit_payload.append(
                {
                    "order": int(visit["order"]),
                    "start_tick": int(visit["start_tick"]),
                    "end_tick": int(visit["end_tick"]),
                    "camp_id": int(visit["camp_id"]),
                    "camp_type": str(visit["camp_type"]),
                    "label_text": context_text,
                    "evidence_text": evidence_text,
                }
            )
            rows.append(
                f'<tr class="farm-visit-row" data-order="{int(visit["order"])}" '
                f'data-start-tick="{int(visit["start_tick"])}" data-end-tick="{int(visit["end_tick"])}">'
                f'<td class="r">{visit["order"]}</td>'
                f"<td>{e(fmt_tick(int(visit['start_tick'])))}</td>"
                f"<td>{e(fmt_tick(int(visit['end_tick'])))}</td>"
                f'<td class="r">{int(visit["camp_id"])}</td>'
                f"<td>{e(str(visit['camp_type']))}</td>"
                f'<td class="r">{visit["duration_s"]:.1f}s</td>'
                f'<td><span class="farm-tag {evidence_cls}">{e(evidence_text)}</span></td>'
                f'<td style="max-width:240px;white-space:normal">{context_tags_html}</td>'
                f'<td style="max-width:180px;white-space:normal">{e(support_text)}</td>'
                f'<td style="max-width:280px;white-space:normal">{context_details}</td>'
                "</tr>"
            )
        if not rows:
            rows.append(
                '<tr><td colspan="10" class="dim">No camp-path segments detected.</td></tr>'
            )

        display_style = "" if idx == 0 else "display:none"
        initial_point = timeline_points[0] if timeline_points else None
        initial_time = str(initial_point["time"]) if initial_point else "—"
        initial_tick = str(int(initial_point["tick"])) if initial_point else "—"
        if initial_point and initial_point.get("camp_id") is not None:
            initial_camp = f"#{int(initial_point['camp_id'])} {str(initial_point.get('camp_type') or '').replace('_', ' ')}"
        else:
            initial_camp = "Transit"
        initial_visit = None
        if initial_point is not None:
            for visit_item in visit_payload:
                if visit_item["start_tick"] <= int(initial_point["tick"]) <= visit_item["end_tick"]:
                    initial_visit = visit_item
                    break
        initial_context = str(initial_visit["label_text"]) if initial_visit else "Transit"
        initial_evidence = str(initial_visit["evidence_text"]) if initial_visit else "Transit"
        timeline_js = json.dumps(timeline_points)
        visits_js = json.dumps(visit_payload)
        panels.append(
            f'<div class="farm-panel" id="farm-panel-{player.player_id}" style="{display_style}">'
            f'<div class="farm-map-wrap">'
            f'<div class="farm-toolbar">'
            f'<button type="button" class="farm-play-btn" id="farm-play-{player.player_id}" '
            f'data-player-id="{player.player_id}">Play</button>'
            f'<input type="range" class="farm-slider" id="farm-slider-{player.player_id}" '
            f'data-player-id="{player.player_id}" min="0" max="{max(0, len(timeline_points) - 1)}" '
            f'value="0" step="1"/>'
            f"</div>"
            f'<div class="farm-meta">'
            f'<div class="farm-meta-chip"><span class="label">Time</span><span class="value" id="farm-time-{player.player_id}">{e(initial_time)}</span></div>'
            f'<div class="farm-meta-chip"><span class="label">Tick</span><span class="value" id="farm-tick-{player.player_id}">{e(initial_tick)}</span></div>'
            f'<div class="farm-meta-chip"><span class="label">Camp</span><span class="value" id="farm-camp-{player.player_id}">{e(initial_camp)}</span></div>'
            f'<div class="farm-meta-chip"><span class="label">Evidence</span><span class="value" id="farm-evidence-{player.player_id}">{e(initial_evidence)}</span></div>'
            f'<div class="farm-meta-chip"><span class="label">Context</span><span class="value" id="farm-context-{player.player_id}">{e(initial_context)}</span></div>'
            f"</div>"
            f'<div class="farm-map-shell">'
            f"{map_svg}"
            f"</div>"
            f'<p class="section-note">White dot: first sample. Yellow dot: last sample. '
            f"Use the slider or Play button to scrub the route by time.</p>"
            f'<script type="application/json" id="farm-data-{player.player_id}">{timeline_js}</script>'
            f'<script type="application/json" id="farm-visits-{player.player_id}">{visits_js}</script>'
            f"</div>"
            f'<div class="farm-table-wrap">'
            f"<table>"
            f"<thead><tr>"
            f'<th class="r">#</th><th>Start</th><th>End</th><th class="r">Camp</th><th>Type</th>'
            f'<th class="r">Duration</th><th>Evidence</th><th>Context Tags</th><th>Exact Support</th><th>Context Evidence</th>'
            f"</tr></thead>"
            f"<tbody>{''.join(rows)}</tbody>"
            f"</table>"
            f"</div>"
            f"</div>"
        )

    script = """
<script>
(function () {
  var sel = document.getElementById('farm-player-select');
  if (!sel) return;
  var playerState = {};

  function parseJsonScript(id) {
    var el = document.getElementById(id);
    if (!el) return [];
    try {
      return JSON.parse(el.textContent || '[]');
    } catch (err) {
      return [];
    }
  }

  function findVisit(visits, tick) {
    for (var i = 0; i < visits.length; i += 1) {
      if (tick >= visits[i].start_tick && tick <= visits[i].end_tick) {
        return visits[i];
      }
    }
    return null;
  }

  function buildSmoothPath(points, index) {
    if (!points.length) return '';
    var chunks = [], current = [];
    for (var pointIndex = 0; pointIndex <= index; pointIndex += 1) {
      var point = points[pointIndex];
      if (point.break_before && current.length) {
        chunks.push(current);
        current = [];
      }
      current.push(point);
    }
    if (current.length) chunks.push(current);
    return chunks.map(function (chunk) {
      if (chunk.length === 1) return 'M ' + chunk[0].px + ' ' + chunk[0].py;
      if (chunk.length === 2) {
        return 'M ' + chunk[0].px + ' ' + chunk[0].py + ' L ' + chunk[1].px + ' ' + chunk[1].py;
      }
      var cmd = ['M ' + chunk[0].px + ' ' + chunk[0].py];
      for (var i = 1; i < chunk.length - 1; i += 1) {
        var x1 = chunk[i].px;
        var y1 = chunk[i].py;
        var x2 = chunk[i + 1].px;
        var y2 = chunk[i + 1].py;
        var mx = (x1 + x2) / 2;
        var my = (y1 + y2) / 2;
        cmd.push('Q ' + x1 + ' ' + y1 + ' ' + mx + ' ' + my);
      }
      cmd.push(
        'Q ' + chunk[chunk.length - 2].px + ' ' + chunk[chunk.length - 2].py + ' ' +
        chunk[chunk.length - 1].px + ' ' + chunk[chunk.length - 1].py
      );
      return cmd.join(' ');
    }).join(' ');
  }

  function renderPlayer(pid, idx) {
    var state = playerState[pid];
    if (!state || !state.points.length) return;
    var index = Math.max(0, Math.min(idx, state.points.length - 1));
    state.index = index;
    state.slider.value = String(index);

    var point = state.points[index];
    var path = buildSmoothPath(state.points, index);
    state.activeTrail.setAttribute('d', path);
    if (state.activeTrailUnder) {
      state.activeTrailUnder.setAttribute('d', path);
    }
    state.currentPoint.setAttribute('cx', point.px);
    state.currentPoint.setAttribute('cy', point.py);
    state.timeEl.textContent = point.time;
    state.tickEl.textContent = String(point.tick);
    state.campEl.textContent = point.camp_id ? ('#' + point.camp_id + ' ' + (point.camp_type || '').split('_').join(' ')) : 'Transit';

    var visit = findVisit(state.visits, point.tick);
    state.evidenceEl.textContent = visit ? visit.evidence_text : 'Transit';
    state.contextEl.textContent = visit ? visit.label_text : 'Transit';
    state.rows.forEach(function (row) {
      var active = visit && row.getAttribute('data-order') === String(visit.order);
      row.classList.toggle('farm-visit-active', !!active);
    });
  }

  function togglePlay(pid) {
    var state = playerState[pid];
    if (!state || !state.points.length) return;
    if (state.timer) {
      window.clearInterval(state.timer);
      state.timer = null;
      state.playBtn.textContent = 'Play';
      return;
    }
    state.playBtn.textContent = 'Pause';
    state.timer = window.setInterval(function () {
      if (state.index >= state.points.length - 1) {
        window.clearInterval(state.timer);
        state.timer = null;
        state.playBtn.textContent = 'Play';
        return;
      }
      renderPlayer(pid, state.index + 1);
    }, 90);
  }

  function ensurePanel(pid) {
    if (playerState[pid]) return;
    var slider = document.getElementById('farm-slider-' + pid);
    var playBtn = document.getElementById('farm-play-' + pid);
    var activeTrail = document.getElementById('farm-active-trail-' + pid);
    var activeTrailUnder = document.getElementById('farm-active-trail-under-' + pid);
    var currentPoint = document.getElementById('farm-current-point-' + pid);
    if (!slider || !playBtn || !activeTrail || !currentPoint) return;
    var points = parseJsonScript('farm-data-' + pid);
    var visits = parseJsonScript('farm-visits-' + pid);
    playerState[pid] = {
      points: points,
      visits: visits,
      slider: slider,
      playBtn: playBtn,
      activeTrail: activeTrail,
      activeTrailUnder: activeTrailUnder,
      currentPoint: currentPoint,
      timeEl: document.getElementById('farm-time-' + pid),
      tickEl: document.getElementById('farm-tick-' + pid),
      campEl: document.getElementById('farm-camp-' + pid),
      evidenceEl: document.getElementById('farm-evidence-' + pid),
      contextEl: document.getElementById('farm-context-' + pid),
      rows: Array.prototype.slice.call(document.querySelectorAll('#farm-panel-' + pid + ' .farm-visit-row')),
      index: 0,
      timer: null
    };
    slider.addEventListener('input', function () {
      renderPlayer(pid, Number(slider.value || 0));
    });
    playBtn.addEventListener('click', function () {
      togglePlay(pid);
    });
    renderPlayer(pid, Number(slider.value || 0));
  }

  function apply() {
    var pid = sel.value;
    document.querySelectorAll('.farm-panel').forEach(function (el) {
      el.style.display = el.id === ('farm-panel-' + pid) ? '' : 'none';
    });
    Object.keys(playerState).forEach(function (key) {
      if (key === pid) return;
      var state = playerState[key];
      if (state && state.timer) {
        window.clearInterval(state.timer);
        state.timer = null;
        state.playBtn.textContent = 'Play';
      }
    });
    ensurePanel(pid);
  }
  sel.addEventListener('change', apply);
  apply();
})();
</script>
"""

    return (
        '<div class="card">'
        "<details open>"
        "<summary>Farming Patterns</summary>"
        '<div class="card-body">'
        '<p class="section-note">'
        "Segments follow documented camp-zone, sample-gap, large-jump, and micro-exit rules. "
        "Evidence labels distinguish neutral-death support, weaker interaction or dwell support, "
        "and transit-like touches without claiming player intent or a complete camp clear. "
        "Independent context tags compare bounded presence, modeled point vision, lane towers, "
        "objectives, and sampled territory. Missing inputs remain explicit and never become zero."
        "</p>"
        '<div style="margin:10px 0 14px 0">'
        '<label for="farm-player-select" style="font-size:12px;color:#8b949e;margin-right:8px">Hero</label>'
        f'<select id="farm-player-select" class="farm-select">{"".join(options)}</select>'
        "</div>"
        f"{''.join(panels)}"
        f"{context_guide_html}"
        f"{script}"
        "</div>"
        "</details>"
        "</div>"
    )
