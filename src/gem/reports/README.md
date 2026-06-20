# gem.reports

`gem.reports` turns a fully parsed `ParsedMatch` into one multi-tab HTML file
you can open in a browser with no server or build step. All match *data* and
images are self-contained — hero/item icons and the map are inlined as base64 —
but the report is **not fully offline**: charts load Chart.js from a CDN
(`builder.py:433`), and the optional Movement tab embeds Plotly via
`include_plotlyjs="cdn"` (`builder.py:179`). In an air-gapped environment the
HTML, tables, and SVG minimaps still render, but the Chart.js charts and the
Plotly Movement tab will not (you'd need to vendor those libraries locally). It
is the *presentation* layer: it asks "what does this match look like to a
human?", whereas its neighbors (`extractors`, `analysis`, `results`) answer
"what happened in this match?" and produce the structured data this package
renders.

This package is read-only with respect to the replay. It never touches `.dem`
bytes, entities, or the combat log directly — it reads the
`ParsedMatch`/`ParsedPlayer` dataclasses from `gem.results.models`, name/geometry
lookups from `gem.catalog`, the post-parse helpers in `gem.analysis`, and
(lazily, only inside `build_draft`) the `DraftEvent` / `resolve_pick_team`
helpers from `gem.extractors.draft` to assign pick/ban teams — then emits HTML
strings.

## Mental Model

A report is built as a tree of HTML strings that collapse into one document:

```text
ParsedMatch
  -> build_html_report()                 (builder.py — the orchestrator)
       -> configure assets, preload icons, set game-start tick
       -> for each tab:
            tab = (label, "\n".join of section build_*() outputs))
              -> build_scoreboard(match)         -> "<div class='card'>...</div>"
              -> build_gold_xp_chart(match)      -> "<div class='card'>...</div>"
              -> build_wards(match, map_b64)      -> "<svg>...</svg> + <script>"
              ...
       -> drop tabs whose joined content is empty
       -> wrap tabs in radio-driven .tab-bar / .tab-page markup
       -> _deduplicate_data_uris(body)
       -> wrap in <html><head>(REPORT_CSS + Chart.js CDN)</head><body>...</body>
```

Each **section builder** is a pure function `build_<name>(match, ...) -> str`.
It receives the `ParsedMatch` (and sometimes `map_b64`), reads whatever fields
it needs, and returns an HTML fragment — conventionally a `<div class="card">`
wrapper, but a section may also emit `<svg>` minimaps and inline `<script>`
blocks. If a section has no data to show it returns `""`; the builder filters
those out so empty tabs disappear.

The **builder** (`builder.py`) owns everything *between* sections: tab layout,
the global `<head>`, the Chart.js CDN include, the JS that switches tabs and
drives the teamfight filter sliders, the one-time map-image global, base64
deduplication, and the optional Plotly Movement tab.

## Section Builders And The `sections/` Package

The section builders live in `gem/reports/sections/`, grouped by domain. Each
module's docstring names its slice:

| Module | `build_*` functions |
|---|---|
| `sections/match.py` | `build_header`, `build_scoreboard`, `build_objectives`, `build_rosh_conversion`, `build_draft`, `build_chat` |
| `sections/economy.py` | `build_hero_timeseries_chart`, `build_gold_xp_chart`, `build_damage`, `build_purchases`, `build_buybacks`, `build_runes` |
| `sections/combat.py` | `build_combat_timeseries_chart`, `build_kill_feed`, `build_teamfights` |
| `sections/vision.py` | `build_wards`, `build_laning`, `build_farming` |
| `sections/_shared.py` | helpers used by more than one section module (e.g. `_ward_enemies_seen`, Radiant/Dire color palettes) |

`sections/__init__.py` re-exports all 18 `build_*` functions, so the package is
the single import surface: `from gem.reports.sections import build_wards`.

The grouping is by *what the section describes*, not by which tab it lands in.
The Overview tab, for instance, is assembled in `builder.py` from
`build_scoreboard` (match.py), `build_hero_timeseries_chart` (economy.py), and
`build_gold_xp_chart` (economy.py). The tab/section mapping lives entirely in
`build_html_report`'s `tabs` list (`builder.py:263`), not in the section
modules.

## The `_sections.py` Shim

`_sections.py` used to be a single ~3,700-line module holding every builder. It
is now a **backward-compatibility shim**: it imports the `build_*` functions
from `gem.reports.sections` and re-exports them, so old imports like
`from gem.reports._sections import build_rosh_conversion` keep working.
`builder.py` still imports through this shim (`builder.py:34`).

Prefer importing from `gem.reports.sections` in new code, but either import
surface is complete: the shim's `__all__` (`_sections.py:35`) lists the same 18
`build_*` functions as the canonical `sections/__init__.py` `__all__` — the two
lists are identical.

## How A `ParsedMatch` Becomes HTML

`build_html_report(match, *, assets, options, map_b64)` in `builder.py` is the
entry point. In order, it:

1. Resolves `assets` (default `ReportAssets()`) and `options` (default
   `ReportOptions()`), calls `configure_assets(assets)` to point the icon
   loaders at the right directories and clear stale icon caches, and loads the
   map image to base64 via `load_map_base64` unless a `map_b64` was passed.
2. Calls `set_game_start_tick(match.game_start_tick or 0)` so the module-level
   `fmt_tick` in `_formatting.py` renders game-relative `MM:SS` times.
3. **Preloads icons** by name: canvas marker icons (`ward_observer`,
   `ward_sentry`, `smoke_of_deceit`), every purchased item across all players'
   `purchase_log` (via `value_name` with the `item_` prefix removed), and every
   drafted hero portrait. These populate the global `ITEM_ICON_B64` /
   `HERO_ICON_B64` caches in `assets.py` so section builders can look icons up by
   short name without re-reading disk.
4. Builds the header once (`build_header`, always visible above the tabs) and
   assembles the `tabs` list, joining each tab's section outputs with `"\n"`
   through `filter(None, ...)` so empty sections vanish.
5. Appends the optional **Movement** tab (`_build_movement_tab`) when
   `options.include_movement` is set and it returns non-empty.
6. Drops any tab whose joined content is whitespace-only, then renders the
   radio-input `.tab-bar` and `.tab-page` divs (first tab `checked`/`active`).
7. Emits the tab-switching + teamfight-filter JS, the one-time map-image global
   JS, runs `_deduplicate_data_uris` over the body, and wraps everything in the
   final `<!DOCTYPE html>` document with `REPORT_CSS` inlined and the Chart.js
   CDN `<script>` in `<head>`.

`write_html_report(match, output_path, ...)` is the thin file-writing wrapper
(creates parent dirs, writes UTF-8, returns the `Path`). `build_html(match,
map_b64)` is a backward-compatible alias for the old example-helper name and
just forwards to `build_html_report`.

`__init__.py` exports the supported surface: `ReportAssets`, `ReportOptions`,
`build_html`, `build_html_report`, `write_html_report`. The public package
re-exports `gem.reports` so `gem.reports.build_html_report(match)` works
(`api.py:68`); `examples/match_report.py` is a thin CLI wrapper over
`write_html_report`.

## Tabs Are JS-Driven, Not Pure CSS

Tab switching is **JavaScript**, not a CSS `:checked` sibling selector. The CSS
(`styles.py`) only defines `.tab-page { display: none }` and
`.tab-page.active { display: block }`; the `tab_js` block in `builder.py`
listens for radio `change` events and toggles the `.active` class on the
matching `#page-tabN` div. The same handler resizes any visible Chart.js
instances (charts mis-measure when laid out while `display:none`) and re-applies
the teamfight slider filters (`tf-deaths` / `tf-participants` → show/hide
`.tf-fight-card` elements by their `data-deaths` / `data-participants`). The
slider/card markup those filters operate on is emitted by the teamfight section
in `sections/combat.py`; only the filter *handler* lives in `builder.py`.

## Assets: Base64 Icons And Map Images

`assets.py` owns asset loading and the inline-icon caches:

- `ReportAssets` is a frozen dataclass of three optional paths: `map_image`,
  `hero_icon_dir`, `item_icon_dir`. `gem` does **not** ship map images or icon
  caches in the wheel — callers point these at locally-fetched assets (see the
  `scripts/fetch_*_icons.py` tooling).
- Module-global dicts `ITEM_ICON_B64` and `HERO_ICON_B64` map short names to
  `"data:image/png;base64,..."` URIs. `configure_assets` resets them on every
  build so a second report with different asset dirs can't inherit stale icons.
- `load_item_icons` / `load_hero_icons` read `<short>.png` files and fill the
  caches; `item_icon_tag` / `hero_icon_src` render lookups (a missing hero icon
  falls back to `HERO_PLACEHOLDER_B64`, an inline 1×1 grey PNG). `hero_short`
  for the cell helpers comes from `_formatting.py` via `gem.catalog`.
- `load_map_base64` returns the map image as a base64 string, or `None` when no
  path is configured or the file is missing.

### Base64 Deduplication

Inlining icons can repeat the same multi-KB data URI dozens of times. Two
mechanisms shrink that:

- **Map image**: `build_html_report` emits the map exactly once as
  `window._GEM_MAP_SRC` and the SVG minimaps reference it via
  `<image class="gem-map-bg" href="">` placeholders, patched on
  `DOMContentLoaded`. Sections never inline the map themselves (see
  `vision.py` / `combat.py` `gem-map-bg` usage).
- **Repeated icons**: `_deduplicate_data_uris` (`builder.py:89`) scans the
  assembled body for `data:image/...;base64,...` URIs, and for any that appear
  more than once, hoists each into a single `window._gem_icon_N` JS variable,
  rewrites the `src=`/`href=` attributes to `data-gem-uri` sentinels, and adds a
  `DOMContentLoaded` patch script. Single-use URIs are left inline.

## The Optional Plotly Movement Tab

`_movement.py` builds an animated hero-movement heatmap with Plotly, and
`builder._build_movement_tab` embeds it. Plotly (and Pillow, used to thumbnail
the map) are **optional** dependencies. The Movement tab is silently omitted
when any of these hold:

- `options.include_movement` is `False`,
- no map image is available (`map_b64 is None`),
- `import plotly` fails (`ImportError`),
- rendering raises for any other reason (caught broadly, logged at `debug`).

`_build_movement_tab` writes the decoded map to a temp file (Plotly's
`build_figure` reads it as an image), embeds the figure with
`include_plotlyjs="cdn"`, and injects a small JS shim to pause the animation at
frame 0 so the tab opens static. `_movement.py` reads player `position_log`,
`purchase_log`, `kills_log`, `combat_log`, gold/XP/LH series, and ability-level
snapshots to build per-hero hover cards; world coordinates are mapped to `[0,1]`
fractions via the `MAP_X/Y` bounds shared from `_formatting.py`.

## Formatting And Styling Helpers

- `_formatting.py` holds the shared constants and HTML helpers: `TICKS_PER_SEC`
  (30), the `MAP_X/Y` world-coordinate bounds, team colors/names, rune and
  game-mode label tables, `set_game_start_tick` / `fmt_tick` (game-relative
  `MM:SS`), `e` (HTML escape), `team_badge`, and `hero_cell` (icon + name cell).
  `fmt_tick` reads a module-global game-start tick set once per build.
- `styles.py` is a single `REPORT_CSS` string (the dark GitHub-style theme,
  card/table/tab/teamfight-card rules) inlined verbatim into `<head>`.

## What This Package Does Not Do

`gem.reports` only renders an already-parsed match. It deliberately does not:

- **Parse replays or read `.dem` bytes** — that is `binary`, `schema`, `state`,
  the top-level `parser.py`, and `combat`. (`reports` imports none of those
  packages.)
- **Extract per-tick state** (gold/XP/position time series, ward events,
  teamfight windows, draft pick/ban events) — that is `extractors`, whose output
  is baked into `ParsedMatch`/`ParsedPlayer`. (The one exception: `build_draft`
  lazily imports `DraftEvent` / `resolve_pick_team` from `gem.extractors.draft`
  to map already-parsed draft events to a team at render time; it does not
  re-extract anything.)
- **Compute analytical facts** — net worth at a tick, vision estimates,
  ability-hit grouping, Roshan conversions, camp-context timelines, and
  position-at-tick all come from `gem.analysis` (imported by the section
  modules); reports just lay them out.
- **Define the data model** — `ParsedMatch`, `ParsedPlayer`,
  `VisionModifierEvent`, etc. live in `gem.results.models`. DataFrame/JSON/
  Parquet export lives in `results`/`api`, not here.
- **Resolve hero/item/ability names or load camp geometry** — those lookups
  come from `gem.catalog` (`hero_display`, `item_display`, `ability_display`,
  `load_camp_zones`, `league_name`).
- **Ship assets** — no map images or icon caches are bundled; `ReportAssets`
  points at locally-fetched files.

If a number on the report is *wrong*, the bug is almost always upstream in
`extractors` or `analysis`; this package's bugs look like broken layout,
mis-escaped HTML, a missing icon, or a tab that should/shouldn't appear.

## Common Pitfalls

### Section builders are stateful through module globals

`build_*` functions look pure but read three pieces of build-time global state:
the `_GAME_START_TICK` in `_formatting.py` (set by `set_game_start_tick`) and
the `ITEM_ICON_B64` / `HERO_ICON_B64` caches in `assets.py` (filled by
`configure_assets` + the preloaders). Call a section builder outside
`build_html_report` and you'll get unconfigured times (`fmt_tick` relative to
tick 0) and missing icons (placeholder fallbacks). This is by design — the
orchestrator sets that state up front — but it means the builders are not safe
to call concurrently across matches.

### Returning `""` is how a section opts out

A section with no data must return an empty string, not an empty `<div>`. The
builder's `filter(None, ...)` and the final
`[(label, content) for ... if content.strip()]` both depend on this to hide
empty sections and drop empty tabs. Returning a non-empty wrapper around no data
will leave a stray empty card or tab.

### Don't inline the map image inside a section

SVG minimaps must use `<image class="gem-map-bg" href="">` and let the builder's
one-time `window._GEM_MAP_SRC` patch fill the `href`. Inlining the base64 map
directly in a section defeats the dedup and bloats the file by the map size per
occurrence.

### The Movement tab failing is not an error

`_build_movement_tab` catches `ImportError` (no Plotly) and any rendering
exception, logs at `debug`, and returns `""`. A report without a Movement tab is
the expected outcome when Plotly/Pillow aren't installed or no map was provided
— not a regression.

### Charts need a network connection (the report is not fully offline)

Match data and images are inlined, but Chart.js (`builder.py:433`) and the
Plotly Movement tab (`builder.py:179`, `include_plotlyjs="cdn"`) load from a CDN.
Opening a report offline shows the tables, SVG minimaps, and layout fine but
leaves the chart canvases and the Movement tab blank. To make a report truly
self-contained, vendor those libraries (inline Chart.js into `<head>` and switch
Plotly to `include_plotlyjs=True`) — this is not done by default to keep file
size down.

### `build_html` is a legacy alias

`build_html(match, map_b64)` exists only for older example code; it forwards to
`build_html_report`. New callers should use `build_html_report` /
`write_html_report` for the full keyword surface (`assets`, `options`).

### Import from `sections`, not the `_sections` shim

`_sections.py` works but is a thin compatibility layer over
`gem.reports.sections`. Both expose the same complete `__all__` (18 `build_*`
functions), but new code should import from `gem.reports.sections` so it depends
on the canonical surface rather than the shim.

## When To Add Code Here

Add code to `gem.reports` when the change is about **how a parsed match is
presented**.

Good fits:

- a new section builder (`build_<thing>(match, ...) -> str`) plus wiring it into
  a tab in `build_html_report`'s `tabs` list and exporting it from
  `sections/__init__.py`,
- a new tab, layout, or CSS rule in `styles.py`,
- a formatting/escaping/icon helper shared across sections (`_formatting.py`,
  `assets.py`, or `sections/_shared.py`),
- enriching the Movement hover cards or fixing a rendering edge case.

To add a section: write `build_foo(match) -> str` in the domain-appropriate
`sections/*.py` module (return `""` when empty), add it to that module's
`__all__` and to `sections/__init__.py`, then add it to the right tab's joined
list in `build_html_report`. Preload any icons it needs in the builder's preload
block.

Poor fits (belong upstream):

- computing a new statistic or per-tick series — extend `extractors` or
  `analysis` and surface it on `ParsedMatch`,
- adding a field to the data model — that's `gem.results.models`,
- name/geometry lookups — `gem.catalog`,
- anything that needs to read the replay again — the parser pipeline.

Keep this package presentation-focused: it should be possible to change every
pixel of the report without touching a single line that parses a replay.