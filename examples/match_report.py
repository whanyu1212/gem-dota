"""Full match report — outputs a self-contained multi-tab HTML file.

Tabs and their sections:

  Overview   — Match header (always visible), Scoreboard, Gold & XP chart
  Combat     — Damage breakdown, Kill feed
  Laning     — Lane role minimap, LH/DN/Gold/XP@10, Eff%, Gold/XP advantage
  Farming    — Carry/core movement trails with camp-session context labels
  Fights     — Fight cards with minimap, participants, per-player stats
  Vision     — Ward map (interactive canvas with playback)
  Economy    — Purchase timeline, Buybacks, Runes
  Draft      — Pick/ban sequence + team picks with hero portraits
  Movement   — Interactive Plotly movement heatmap (requires plotly + map image)
  Misc       — Objectives timeline, Chat log

Built entirely on top of ``gem.parse()``. Plotly is optional — the Movement
tab is omitted if plotly is not installed or no map image is provided.

Usage:
    python examples/match_report.py path/to/replay.dem [--output report.html]
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from report.assets import (
    hero_icon_src as _hero_icon_src,
)
from report.assets import (
    load_hero_icons as _load_hero_icons,
)
from report.assets import (
    load_item_icons as _load_item_icons,
)
from report.helpers import (
    GAME_MODES,
    TEAM_COLOR_CSS,
    set_game_start_tick,
)
from report.helpers import (
    e as _e,
)
from report.helpers import (
    fmt_tick as _fmt_tick,
)
from report.helpers import (
    hero as _hero,
)
from report.html_sections import (
    build_buybacks as _ext_build_buybacks,
)
from report.html_sections import (
    build_chat as _ext_build_chat,
)
from report.html_sections import (
    build_combat_timeseries_chart as _ext_build_combat_timeseries_chart,
)
from report.html_sections import (
    build_damage as _ext_build_damage,
)
from report.html_sections import (
    build_draft as _ext_build_draft,
)
from report.html_sections import (
    build_farming as _ext_build_farming,
)
from report.html_sections import (
    build_gold_xp_chart as _ext_build_gold_xp_chart,
)
from report.html_sections import (
    build_header as _ext_build_header,
)
from report.html_sections import (
    build_hero_timeseries_chart as _ext_build_hero_timeseries_chart,
)
from report.html_sections import (
    build_kill_feed as _ext_build_kill_feed,
)
from report.html_sections import (
    build_laning as _ext_build_laning,
)
from report.html_sections import (
    build_objectives as _ext_build_objectives,
)
from report.html_sections import (
    build_purchases as _ext_build_purchases,
)
from report.html_sections import (
    build_rosh_conversion as _ext_build_rosh_conversion,
)
from report.html_sections import (
    build_runes as _ext_build_runes,
)
from report.html_sections import (
    build_scoreboard as _ext_build_scoreboard,
)
from report.html_sections import (
    build_teamfights as _ext_build_teamfights,
)
from report.html_sections import (
    build_wards as _ext_build_wards,
)
from report.style import REPORT_CSS as _CSS

import gem

# Section builders — return HTML strings
# ---------------------------------------------------------------------------


def _hero_cell(npc_name: str, team: int = 0) -> str:
    """Return an icon + name cell fragment for a hero NPC name.

    Args:
        npc_name: Hero NPC name e.g. ``"npc_dota_hero_axe"``.
        team: Team number for name colouring (2=Radiant, 3=Dire, 0=neutral).

    Returns:
        HTML fragment with a 20px portrait thumbnail followed by the display name.
    """
    src = _hero_icon_src(npc_name)
    name = _e(_hero(npc_name))
    color = TEAM_COLOR_CSS.get(team, "#e6edf3")
    return (
        f'<img src="{src}" width="20" height="12" '
        f'style="object-fit:cover;border-radius:2px;vertical-align:middle;margin-right:5px">'
        f'<span style="color:{color}">{name}</span>'
    )


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------


def _deduplicate_data_uris(html_body: str) -> str:
    """Replace repeated base64 data URIs with JS-variable references.

    Any data URI that appears more than once is hoisted into a single
    ``<script>`` block as ``window._gem_icon_N = "data:..."`` and every
    occurrence in src/href attributes is replaced with a sentinel placeholder
    ``data:_gem_icon_N``.  A second ``<script>`` block patches all elements
    on DOMContentLoaded.

    Args:
        html_body: Assembled HTML body string before the ``</body>`` close.

    Returns:
        HTML body with deduplicated data URIs.
    """
    import re as _re
    from collections import Counter as _Counter

    pattern = _re.compile(r"data:image/[^;]+;base64,[A-Za-z0-9+/=]+")
    all_uris = pattern.findall(html_body)
    counts = _Counter(all_uris)
    duplicates = {uri for uri, count in counts.items() if count > 1}
    if not duplicates:
        return html_body

    uri_to_var: dict[str, str] = {}
    definitions: list[str] = []
    for i, uri in enumerate(sorted(duplicates)):
        var = f"_gem_icon_{i}"
        uri_to_var[uri] = var
        definitions.append(f"window.{var}={json.dumps(uri)};")

    for uri, var in uri_to_var.items():
        html_body = html_body.replace(f'src="{uri}"', f'data-gem-uri="{var}" src=""')
        html_body = html_body.replace(f"src='{uri}'", f"data-gem-uri='{var}' src=''")
        html_body = html_body.replace(f'href="{uri}"', f'data-gem-uri="{var}" href=""')

    patch_js = (
        'document.addEventListener("DOMContentLoaded",function(){'
        'document.querySelectorAll("[data-gem-uri]").forEach(function(el){'
        'var v=el.getAttribute("data-gem-uri");'
        "var d=window[v];if(!d)return;"
        'if(el.hasAttribute("href")){el.setAttribute("href",d);}'
        "else{el.src=d;}});});"
    )

    dedup_script = "<script>" + "".join(definitions) + patch_js + "</script>"
    return dedup_script + "\n" + html_body


def _build_movement_tab(match: gem.ParsedMatch, map_b64: str | None) -> str:
    """Build the Movement tab content using Plotly.

    Returns an empty string if plotly is not installed or no map image is
    available — the tab is omitted from the report in that case.

    Args:
        match: Parsed match data.
        map_b64: Base64-encoded map image, or ``None``.

    Returns:
        HTML string for the tab content, or ``""`` if unavailable.
    """
    if map_b64 is None:
        return ""
    try:
        import plotly.graph_objects as go  # noqa: F401
        from report.movement import build_figure
    except Exception:
        return ""

    try:
        import tempfile

        import plotly.io as pio

        # Write map image to a temp file so build_figure can read it
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(base64.b64decode(map_b64))
            tmp_path = Path(tmp.name)

        fig = build_figure(match, tmp_path, dem_stem="match")
        tmp_path.unlink(missing_ok=True)

        # Embed as a standalone div (no full HTML wrapper, CDN Plotly).
        plotly_div = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs="cdn",
            config={"responsive": True},
        )

        # Extract the auto-generated div id so we can cancel autoplay via JS.
        # Plotly emits: <div id="..." class="plotly-graph-div" ...>
        import re as _re

        m = _re.search(r'<div id="([^"]+)" class="plotly-graph-div"', plotly_div)
        div_id = m.group(1) if m else ""

        # After Plotly initialises the figure, ensure it is paused at frame 0.
        # Plotly.animate(id, [null], {mode:'immediate', frame:{duration:0}})
        # stops any queued animation without advancing frames.
        pause_js = ""
        if div_id:
            pause_js = (
                f"<script>"
                f"(function waitForPlotly(){{"
                f'  var el = document.getElementById("{div_id}");'
                f"  if (!el || !el._fullLayout) {{ setTimeout(waitForPlotly, 50); return; }}"
                f'  Plotly.animate("{div_id}", [null], {{'
                f'    mode:"immediate",'
                f"    frame:{{duration:0,redraw:false}},"
                f"    transition:{{duration:0}}"
                f"  }});"
                f"}})();"
                f"</script>"
            )

        return (
            f'<div class="card"><div class="card-body" style="padding:8px">'
            f"{plotly_div}{pause_js}"
            f"</div></div>"
        )
    except Exception:
        return ""


def build_html(match: gem.ParsedMatch, map_b64: str | None = None) -> str:
    """Assemble the complete self-contained multi-tab HTML report.

    Args:
        match: Parsed match data from ``gem.parse()``.
        map_b64: Base64-encoded map image for the ward canvas and movement
            heatmap, or ``None``.

    Returns:
        Complete HTML string.
    """
    set_game_start_tick(match.game_start_tick or 0)

    # Pre-load icons for canvas ward/smoke markers and purchase timeline
    _canvas_icons = ["ward_observer", "ward_sentry", "smoke_of_deceit"]
    _purchase_icons = [
        e.value_name.removeprefix("item_")
        for pp in match.players
        for e in pp.purchase_log
        if e.value_name
    ]
    _load_item_icons(_canvas_icons + list(set(_purchase_icons)))

    # Pre-load hero portrait icons for the draft section
    _load_hero_icons([e.hero_name for e in match.draft if e.hero_name])

    # Build each tab's content
    header_html = _ext_build_header(match, _fmt_tick, GAME_MODES)

    tabs: list[tuple[str, str]] = [
        (
            "Overview",
            "\n".join(
                filter(
                    None,
                    [
                        _ext_build_scoreboard(match, _hero_cell),
                        _ext_build_hero_timeseries_chart(match),
                        _ext_build_gold_xp_chart(match),
                    ],
                )
            ),
        ),
        (
            "Combat",
            "\n".join(
                filter(
                    None,
                    [
                        _ext_build_combat_timeseries_chart(match),
                        _ext_build_damage(match, _hero_cell),
                        _ext_build_kill_feed(match, _hero_cell),
                    ],
                )
            ),
        ),
        ("Laning", _ext_build_laning(match, map_b64)),
        ("Farming", _ext_build_farming(match, map_b64)),
        ("Fights", _ext_build_teamfights(match, map_b64)),
        ("Roshan Conversion", _ext_build_rosh_conversion(match)),
        ("Vision", _ext_build_wards(match, map_b64)),
        (
            "Economy",
            "\n".join(
                filter(
                    None,
                    [
                        _ext_build_purchases(match),
                        _ext_build_buybacks(match),
                    ],
                )
            ),
        ),
        ("Draft", _ext_build_draft(match)),
        (
            "Misc",
            "\n".join(
                filter(
                    None,
                    [
                        _ext_build_objectives(match, _fmt_tick),
                        _ext_build_runes(match, _hero_cell),
                        _ext_build_chat(match),
                    ],
                )
            ),
        ),
    ]

    # Movement tab — optional (requires plotly + map image)
    movement_html = _build_movement_tab(match, map_b64)
    if movement_html:
        tabs.append(("Movement", movement_html))

    # Remove tabs with no content
    tabs = [(label, content) for label, content in tabs if content.strip()]

    # Build tab bar + pages
    tab_inputs = []
    tab_labels = []
    tab_pages = []
    for i, (label, content) in enumerate(tabs):
        tid = f"tab{i}"
        checked = " checked" if i == 0 else ""
        tab_inputs.append(f'<input type="radio" name="gemtab" id="{tid}"{checked}>')
        tab_labels.append(f'<label for="{tid}">{html.escape(label)}</label>')
        tab_pages.append(
            f'<div class="tab-page{" active" if i == 0 else ""}" id="page-{tid}">\n{content}\n</div>'
        )

    tab_bar = (
        '<div class="tab-bar">\n'
        + "\n".join(f"{inp}\n{lbl}" for inp, lbl in zip(tab_inputs, tab_labels, strict=False))
        + "\n</div>"
    )

    pages_html = "\n".join(tab_pages)

    # JS: switch active tab on radio change + resize Chart.js on tab show
    tab_js = """
<script>
(function() {
  function applyTeamfightFilters() {
    var deathsEl = document.getElementById('tf-deaths');
    var partsEl = document.getElementById('tf-participants');
    if (!deathsEl || !partsEl) return;

    var minDeaths = parseInt(deathsEl.value || '1', 10);
    var minParts = parseInt(partsEl.value || '1', 10);

    var dVal = document.getElementById('tf-deaths-val');
    var pVal = document.getElementById('tf-participants-val');
    if (dVal) dVal.textContent = String(minDeaths);
    if (pVal) pVal.textContent = String(minParts);

    var cards = Array.prototype.slice.call(document.querySelectorAll('.tf-fight-card'));
    var shown = 0;
    cards.forEach(function(card) {
      var deaths = parseInt(card.getAttribute('data-deaths') || '0', 10);
      var participants = parseInt(card.getAttribute('data-participants') || '0', 10);
      var visible = deaths >= minDeaths && participants >= minParts;
      card.classList.toggle('hidden', !visible);
      if (visible) shown++;
    });

    var vis = document.getElementById('tf-vis-count');
    if (vis) vis.textContent = String(shown);
    var noRes = document.getElementById('tf-no-results');
    if (noRes) noRes.style.display = shown === 0 ? 'block' : 'none';
  }

  var radios = document.querySelectorAll('input[name="gemtab"]');
  radios.forEach(function(r) {
    r.addEventListener('change', function() {
      document.querySelectorAll('.tab-page').forEach(function(p) {
        p.classList.remove('active');
      });
      var page = document.getElementById('page-' + r.id);
      if (page) page.classList.add('active');
      // Resize any Chart.js charts that just became visible
      if (window.Chart) {
        Object.values(Chart.instances).forEach(function(c) { c.resize(); });
      }
      applyTeamfightFilters();
    });
  });

  var tfDeaths = document.getElementById('tf-deaths');
  var tfParts = document.getElementById('tf-participants');
  if (tfDeaths) tfDeaths.addEventListener('input', applyTeamfightFilters);
  if (tfParts) tfParts.addEventListener('input', applyTeamfightFilters);
  applyTeamfightFilters();
})();
</script>"""

    # Emit map image once as a JS global; SVG <image class="gem-map-bg"> elements
    # are patched on DOMContentLoaded to avoid embedding the same base64 N times.
    map_js = ""
    if map_b64:
        map_js = (
            f'<script>window._GEM_MAP_SRC="data:image/jpeg;base64,{map_b64}";</script>\n'
            '<script>document.addEventListener("DOMContentLoaded",function(){'
            "var src=window._GEM_MAP_SRC;"
            'document.querySelectorAll("image.gem-map-bg").forEach(function(el){'
            'el.setAttribute("href",src);});});</script>'
        )

    body_parts = [map_js, header_html, tab_bar, pages_html, tab_js]
    body = "\n".join(p for p in body_parts if p)
    body = _deduplicate_data_uris(body)

    return "\n".join(
        [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            "<title>Dota 2 Match Report</title>",
            '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>',
            "<style>",
            _CSS,
            "</style>",
            "</head>",
            "<body>",
            '<div class="container">',
            body,
            "</div>",
            "</body>",
            "</html>",
        ]
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse a .dem replay and write a self-contained HTML match report."""
    parser = argparse.ArgumentParser(
        description="Generate an HTML match report from a Dota 2 .dem replay file."
    )
    parser.add_argument("dem", nargs="?", help="Path to the .dem replay file")
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output HTML file path (default: <dem_name>_report.html in project root)",
    )
    parser.add_argument(
        "--map",
        default=None,
        help="Path to map image for ward overlay (default: tests/fixtures/Game_map_7.40.jpg)",
    )
    args = parser.parse_args()

    if args.dem:
        dem_path = args.dem
    else:
        dem_path = str(
            Path(__file__).parent.parent / "tests" / "fixtures" / "ti14_finals_g3_xg_vs_falcons.dem"
        )

    print(f"Parsing {dem_path} ...")
    match = gem.parse(dem_path)

    # Load map image for ward canvas
    map_path = (
        Path(args.map)
        if args.map
        else Path(__file__).parent.parent / "tests" / "fixtures" / "Game_map_7.40.jpg"
    )
    map_b64: str | None = None
    if map_path.exists():
        map_b64 = base64.b64encode(map_path.read_bytes()).decode()
        print(f"Map image loaded: {map_path}")
    else:
        print(f"Map image not found at {map_path} — ward map will render without background.")

    if args.output:
        output_path = Path(args.output)
    else:
        dem_file = Path(dem_path)
        project_root = Path(__file__).parent.parent
        output_path = project_root / (dem_file.stem + "_report.html")

    html_content = build_html(match, map_b64)
    output_path.write_text(html_content, encoding="utf-8")
    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
