"""Vision report sections (wards, laning, farming maps).

Split out of the former monolithic ``_sections.py`` (see that module's
shim for backward-compatible re-exports).
"""

from __future__ import annotations

import json
import math

from gem.analysis import (
    FarmingBoundaryReason,
    FarmingRoute,
    FarmingRoutePoint,
    SmokeAnalysis,
    SmokeLifecycleStatus,
    SmokeMemberAnalysis,
    build_farming_routes,
    build_smoke_analysis,
)
from gem.catalog.map import load_camp_zones
from gem.extractors._cells import WORLD_UNITS_PER_CELL
from gem.extractors.lane import lane_for_cell
from gem.reports._formatting import (
    GAME_CLOCK_JS,
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    TEAM_COLOR_CSS,
    TICKS_PER_SEC,
    e,
    fmt_tick,
    game_clock,
    game_clock_js_config,
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
from gem.reports.sections._shared import fight_numbers, fight_outcome, game_seconds_between
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
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


_SMOKE_STATUS_LABELS: dict[str, str] = {
    "no_members_observed": "No members observed",
    "early_removal": "Broken early",
    "expired": "Expired",
    "incomplete": "Incomplete",
}


def _smoke_broke_html(analysis: SmokeAnalysis, first_early: SmokeMemberAnalysis | None) -> str:
    """Render when a smoke first broke, or how it ended when nobody broke it."""
    if first_early is None or first_early.removed_tick is None:
        label = _SMOKE_STATUS_LABELS.get(analysis.status.value, analysis.status.value)
        return f'<span class="dim">{e(label)}</span>'
    removed_tick = first_early.removed_tick
    return (
        f'<span title="Replay tick {removed_tick}">{e(fmt_tick(removed_tick))}</span> '
        f'<span class="dim">({game_seconds_between(analysis.activation_tick, removed_tick)} · '
        f"{e(hero(first_early.hero_name))})</span>"
    )


def _smoke_first_fight_html(analysis: SmokeAnalysis, numbers: dict[int, int]) -> str:
    """Render the first fight after a smoke: number, delay and winner."""
    fight = analysis.first_fight
    if fight is None or id(fight) not in numbers:
        return '<span class="dim">None within 60s</span>'
    number = numbers[id(fight)]
    return (
        f'<a class="smoke-fight-link" href="#fight-{number}" '
        f'data-report-target="fight-{number}" data-report-snapshot="engagement_start">'
        f"Fight #{number}</a> "
        f'<span class="dim">{game_seconds_between(analysis.activation_tick, fight.first_death_tick)}'
        f" · {fight_outcome(fight.winner)}</span>"
    )


def build_smokes(
    match: ParsedMatch,
    map_b64: str | None,
    analyses: list[SmokeAnalysis] | None = None,
) -> str:
    """Build the Smoke Operations section: when each smoke started, broke and led to a fight.

    Args:
        match: Parsed match carrying smoke events and fights.
        map_b64: Optional pre-encoded map background.
        analyses: Optional precomputed :func:`gem.build_smoke_analysis` output,
            shared with the Fights tab.

    Returns:
        Self-contained HTML, or an empty string when nobody used a smoke.
    """
    if analyses is None:
        analyses = build_smoke_analysis(match)
    if not analyses:
        return ""
    numbers = fight_numbers(match)

    map_events: list[dict[str, object]] = []
    rows: list[str] = []

    for index, analysis in enumerate(analyses, start=1):
        raw = match.smoke_events[index - 1] if index <= len(match.smoke_events) else None
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

        members_html = ", ".join(e(hero(member.hero_name)) for member in analysis.members) or "—"
        team_color = TEAM_COLOR_CSS.get(analysis.team, "#8b949e")
        rows.append(
            f'<tr id="smoke-operation-{index}">'
            f'<td class="r"><strong>#{index}</strong></td>'
            f'<td title="Replay tick {analysis.activation_tick}">'
            f"{e(fmt_tick(analysis.activation_tick))}</td>"
            f'<td><span style="color:{team_color}">{e(team_name(analysis.team))}</span></td>'
            f"<td>{members_html}</td>"
            f"<td>{_smoke_broke_html(analysis, first_early)}</td>"
            f"<td>{_smoke_first_fight_html(analysis, numbers)}</td>"
            "</tr>"
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
    if (mapImg.complete && mapImg.naturalWidth > 0) {{
      // Centred square of the map, as the SVG maps' "slice" shows (see MAP_XMIN).
      var side = Math.min(mapImg.naturalWidth, mapImg.naturalHeight);
      ctx.drawImage(mapImg, (mapImg.naturalWidth - side) / 2, (mapImg.naturalHeight - side) / 2,
                    side, side, 0, 0, W, H);
    }} else {{ ctx.fillStyle = '#111820'; ctx.fillRect(0, 0, W, H); }}
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
        '<p class="dim">Broke = the first member to lose the smoke before it ran out, '
        "with the in-game time since activation. First fight = the first fight whose first "
        "death came within 60 seconds of activation.</p>"
        + map_html
        + '<div style="overflow-x:auto"><table><thead><tr><th class="r">#</th><th>Time</th>'
        "<th>Team</th><th>Members</th><th>Broke</th><th>First fight</th>"
        f"</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
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
    # Playback ends when the Ancient falls; wards can nominally expire later, in
    # the post-game recording.
    slider_max = match.post_game_tick or max(max_tick, match.game_end_tick or max_tick)
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
        "gameClock": game_clock_js_config(game_clock()),
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

    ward_script = (
        """
<script>
(function() {
"""
        + GAME_CLOCK_JS
        + """
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

  var gameClock = cfg.gameClock || {
    gameStartTick: gameStartTick, gameStartTimeS: null, netTickOffset: 0, pauses: []
  };
  function fmtTick(tick) {
    return gemFormatClock(gameClock, tick);
  }

  function draw(tick) {
    ctx.clearRect(0, 0, W, H);

    if (mapImg.complete && mapImg.naturalWidth > 0) {
      // Centred square of the map, as the SVG maps' "slice" shows (see MAP_XMIN).
      var side = Math.min(mapImg.naturalWidth, mapImg.naturalHeight);
      ctx.drawImage(mapImg, (mapImg.naturalWidth - side) / 2, (mapImg.naturalHeight - side) / 2,
                    side, side, 0, 0, W, H);
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
    )

    parts.append(canvas_html)
    parts.append(ward_script)

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


_LANE_ROLE_NAMES: dict[int, str] = {
    1: "Safe",
    2: "Mid",
    3: "Off",
    4: "Jungle",
    0: "—",
}


_LANE_COLORS: dict[int, str] = {
    1: "#4caf50",
    2: "#58a6ff",
    3: "#f44336",
    4: "#ff9800",
}


def _lane_label(pp: ParsedPlayer) -> str:
    """Return a player's lane role name, marked when they roamed."""
    name = _LANE_ROLE_NAMES.get(pp.lane_role, "—")
    return f"{name} · roaming" if pp.is_roaming and pp.lane_role else name


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


# A hero's lane anchor is the busiest spot within this many cells (512 world units).
_LANE_ANCHOR_RADIUS_CELLS = 4


def _lane_anchor(pp: ParsedPlayer) -> tuple[float, float] | None:
    """Return the world position where a hero spent most of its laning time.

    Uses the first-10-minute ``lane_pos`` cells inside the player's assigned
    OpenDota lane (all cells when none are): the cell with the most samples within
    ``_LANE_ANCHOR_RADIUS_CELLS``, refined to the sample-weighted centre of that
    neighbourhood. A plain mean of every cell is pulled off the lane by time in
    base, rotations and the L-shaped side lanes.
    """
    cells = {
        (int(cx), int(cy)): count
        for cx, column in pp.lane_pos.items()
        for cy, count in column.items()
        if count > 0
    }
    if not cells:
        return None
    cells = {c: n for c, n in cells.items() if lane_for_cell(*c) == pp.lane} or cells
    radius_sq = _LANE_ANCHOR_RADIUS_CELLS**2

    def neighbourhood(centre: tuple[int, int]) -> list[tuple[tuple[int, int], int]]:
        return [
            (cell, n)
            for cell, n in cells.items()
            if (cell[0] - centre[0]) ** 2 + (cell[1] - centre[1]) ** 2 <= radius_sq
        ]

    busiest = max(cells, key=lambda c: (sum(n for _, n in neighbourhood(c)), cells[c], c))
    near = neighbourhood(busiest)
    total = sum(n for _, n in near)
    x = sum(cell[0] * n for cell, n in near) / total * WORLD_UNITS_PER_CELL
    y = sum(cell[1] * n for cell, n in near) / total * WORLD_UNITS_PER_CELL
    return x, y


def _spread_markers(
    points: list[tuple[float, float]], min_dist: float, size: float, iterations: int = 80
) -> list[tuple[float, float]]:
    """Push markers apart until no two are closer than ``min_dist``, inside the map.

    Lane partners share an anchor, so their icons would stack. Each overlapping
    pair is pushed apart along the line between them (markers on the same spot
    fan out at fixed angles, so the result is deterministic).

    Args:
        points: Marker centres in SVG pixels.
        min_dist: Smallest allowed distance between two centres.
        size: The square map's side, to keep markers inside it.
        iterations: Most relaxation passes.

    Returns:
        The adjusted centres, in the input order.
    """
    low, high = min_dist / 2, size - min_dist / 2

    def clamp(value: float) -> float:
        return min(max(value, low), high)

    # Clamp first: anchors outside the map that start apart can clamp onto one spot.
    pos = [[clamp(x), clamp(y)] for x, y in points]
    for _ in range(iterations):
        moved = False
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
                dist = math.hypot(dx, dy)
                if dist >= min_dist:
                    continue
                if dist < 1e-6:
                    angle = 2.399963 * (i + j)  # golden angle: distinct fan-out per pair
                    dx, dy, dist = math.cos(angle), math.sin(angle), 1.0
                push = (min_dist - dist) / 2
                ux, uy = dx / dist, dy / dist
                pos[i][0] -= ux * push
                pos[i][1] -= uy * push
                pos[j][0] += ux * push
                pos[j][1] += uy * push
                moved = True
        for p in pos:
            clamped = [clamp(p[0]), clamp(p[1])]
            if clamped != p:
                # A clamp can undo a push, so the overlaps need another pass.
                p[:] = clamped
                moved = True
        if not moved:
            break
    return [(x, y) for x, y in pos]


def _laning_minimap_svg(
    match: ParsedMatch,
    map_b64: str | None,
    size: int = 320,
) -> str:
    """Render a minimap SVG with each hero at the busiest spot of its laning lane.

    Icons that would overlap (lane partners) are spread apart; a dot and a short
    line mark the hero's true spot when its icon had to move.
    """
    _XMIN, _XMAX = MAP_XMIN, MAP_XMAX
    _YMIN, _YMAX = MAP_YMIN, MAP_YMAX

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

    icon_r = 13
    placed: list[tuple[ParsedPlayer, tuple[float, float]]] = []
    for pp in match.players:
        if not pp.lane_pos or not pp.hero_name:
            continue
        anchor = _lane_anchor(pp)
        if anchor is not None:
            placed.append((pp, _world_to_px(*anchor)))
    centres = _spread_markers([xy for _, xy in placed], 2 * icon_r + 2, size)

    leaders: list[str] = []
    icons: list[str] = []
    for (pp, (ax, ay)), (cx, cy) in zip(placed, centres, strict=True):
        ring_color = _LANE_COLORS.get(pp.lane_role, "#8b949e")
        if math.hypot(cx - ax, cy - ay) > 2:
            leaders.append(
                f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" '
                f'stroke="{ring_color}" stroke-width="1.5" stroke-opacity="0.85"/>'
                f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="2.5" fill="{ring_color}" '
                f'stroke="#0d1117" stroke-width="1"/>'
            )
        slot = pp.player_id
        clip_id = f"lane_clip_{slot}"
        src = hero_icon_src(pp.hero_name)
        role_label = _lane_label(pp)
        dash = ' stroke-dasharray="4 3"' if pp.is_roaming else ""
        icons.append(
            f'<defs><clipPath id="{clip_id}">'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}"/>'
            f"</clipPath></defs>"
            f'<image href="{src}" x="{cx - icon_r:.1f}" y="{cy - icon_r:.1f}" '
            f'width="{icon_r * 2}" height="{icon_r * 2}" '
            f'clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{icon_r}" fill="none" '
            f'stroke="{ring_color}" stroke-width="2.5"{dash}/>'
            f"<title>{e(hero(pp.hero_name))} ({role_label})</title>"
        )

    return (
        f'<svg class="lane-map-svg" width="{size}" height="{size}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'style="border-radius:8px;overflow:hidden;border:1px solid #30363d">'
        + bg_img
        + "".join(leaders)
        + "".join(icons)
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
        f"Ring colour = lane role, at the centre of the first-10-min heatmap; "
        f"a dashed ring marks a roaming player (under 45% of samples in one lane)"
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
        'N/A for jungle.">Gold Adv</th>'
        '<th class="r" title="XP advantage vs lane opponents at 10 min. '
        'N/A for jungle.">XP Adv</th>'
        "<th>Eff Bar</th>"
        "</tr></thead>"
    )
    parts.append("<tbody>")

    for pp in players:
        team_color = TEAM_COLOR_CSS.get(pp.team, "#888")
        row_cls = "row-radiant" if pp.team == 2 else "row-dire"
        role_name = _lane_label(pp)
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


_FARM_CORE_ROLES: dict[int, str] = {1: "Carry", 2: "Mid", 3: "Offlane"}


def _core_players(match: ParsedMatch) -> list[tuple[ParsedPlayer, str]]:
    """Return each team's carry, mid and offlaner, Radiant first.

    For each team and lane role (1 safe lane, 2 mid, 3 off lane) the core is the
    player with the most last hits at 10:00 (``lane_last_hits``); ties go to the
    lower player slot. A lane role with no player gives no core.
    """
    cores: list[tuple[ParsedPlayer, str]] = []
    for team in (2, 3):
        for lane_role, role_name in _FARM_CORE_ROLES.items():
            laners = [
                player
                for player in match.players
                if player.team == team and player.lane_role == lane_role and player.hero_name
            ]
            if laners:
                core = max(laners, key=lambda player: (player.lane_last_hits, -player.player_id))
                cores.append((core, role_name))
    return cores


def build_farming(match: ParsedMatch, map_b64: str | None) -> str:
    """Build the Farming tab: camp-by-camp routes for each team's cores."""
    camps_obj = _load_camp_zones()
    camps = list(camps_obj.get("camps", []))
    if not camps:
        return ""

    routes_by_player = {route.player_id: route for route in build_farming_routes(match)}
    cores = [
        (player, role_name)
        for player, role_name in _core_players(match)
        if routes_by_player.get(player.player_id) is not None
        and routes_by_player[player.player_id].points
    ]
    if not cores:
        return ""
    load_hero_icons([player.hero_name for player, _ in cores])

    panels: list[str] = []
    options: list[str] = []
    for idx, (player, role_name) in enumerate(cores):
        route = routes_by_player[player.player_id]
        segments = route.segments
        map_svg, timeline_points = _build_farming_map_svg(
            player=player,
            route=route,
            camps=camps,
            visits=[{"camp_id": segment.camp_id} for segment in segments],
            map_b64=map_b64,
            start_tick=match.game_start_tick or 0,
        )

        option_label = f"{hero(player.hero_name)} ({team_name(player.team)}, {role_name})"
        options.append(
            f'<option value="{player.player_id}"{" selected" if idx == 0 else ""}>{e(option_label)}</option>'
        )

        def gain(value: int | None) -> str:
            return "—" if value is None else f"+{value:,}"

        rows: list[str] = []
        visit_payload = [
            {
                "order": segment.segment_index,
                "start_tick": segment.start_tick,
                "end_tick": segment.end_tick,
            }
            for segment in segments
        ]
        for segment in segments:
            rows.append(
                f'<tr class="farm-visit-row" data-order="{segment.segment_index}" '
                f'data-start-tick="{segment.start_tick}" data-end-tick="{segment.end_tick}">'
                f'<td class="r">{segment.segment_index}</td>'
                f"<td>{e(fmt_tick(segment.start_tick))}</td>"
                f"<td>{e(fmt_tick(segment.end_tick))}</td>"
                f'<td class="r">{segment.camp_id}</td>'
                f"<td>{e(segment.camp_type)}</td>"
                f'<td class="r">{segment.duration_seconds:.1f}s</td>'
                f'<td class="r">{segment.neutral_kills}</td>'
                f'<td class="r">{gain(segment.window_total_earned_gold_delta)}</td>'
                f'<td class="r">{gain(segment.window_xp_delta)}</td>'
                "</tr>"
            )
        if not rows:
            rows.append('<tr><td colspan="9" class="dim">No camp visits detected.</td></tr>')

        display_style = "" if idx == 0 else "display:none"
        initial_point = timeline_points[0] if timeline_points else None
        initial_time = str(initial_point["time"]) if initial_point else "—"
        initial_tick = str(int(initial_point["tick"])) if initial_point else "—"
        if initial_point and initial_point.get("camp_id") is not None:
            initial_camp = f"#{int(initial_point['camp_id'])} {str(initial_point.get('camp_type') or '').replace('_', ' ')}"
        else:
            initial_camp = "Transit"
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
            f'<th class="r">Duration</th><th class="r">Neutral kills</th>'
            f'<th class="r">Gold</th><th class="r">XP</th>'
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
        "Camp-by-camp routes for each team's cores. For each team and lane role "
        "(safe lane → carry, mid → mid, off lane → offlaner), the core is the player "
        "with the most last hits at 10:00. A visit is time spent inside a camp zone. "
        "Neutral kills are the hero's kills inside that zone; gold and XP are everything "
        "the hero earned during the visit, from any source."
        "</p>"
        '<div style="margin:10px 0 14px 0">'
        '<label for="farm-player-select" style="font-size:12px;color:#8b949e;margin-right:8px">Hero</label>'
        f'<select id="farm-player-select" class="farm-select">{"".join(options)}</select>'
        "</div>"
        f"{''.join(panels)}"
        f"{script}"
        "</div>"
        "</details>"
        "</div>"
    )
