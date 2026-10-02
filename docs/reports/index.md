# Match Reports

gem can generate self-contained HTML reports from real `.dem` replay files.

The `Farming` tab in the HTML report is documented in
[Experimental Features → Farming Patterns](../experimental/farming-patterns.md).

The `Roshan Conversion` tab compares both teams across fights, structures,
resources, sustained forward territory, wards, and Tormentor kills. It uses
signed raw values, paired before/during occupancy maps, and a chronological
event timeline; see
[Experimental Features → Roshan Conversion](../experimental/rosh-conversion.md)
for the exact windows, formulas, and missing-data rules.
Roshan fight events and fight cards link to one another. Lifecycle and team
attribution provenance are shown explicitly; deprecated conversion scores and
exclusive labels are no longer rendered.

The `Fights` tab includes one evidence-first positioning map per fight with
pre-engagement, engagement-start, first-death, and fight-end controls. Marker
visibility, position freshness, missing samples, and the current conservative
engagement-start fallback are documented in
[Experimental Features → Fight Positioning](../experimental/fight-positioning.md).

The **Smoke Operations** view summarizes bounded smoke/fight evidence and links
unique associations directly to the matching fight snapshot. Exact lifecycle,
action, visibility, and death ticks remain distinct from sampled formation
context. See
[Experimental Features → Smoke/Fight Insights](../experimental/smoke-fight-insights.md).

## Hosted samples

Sample reports are not bundled into this VitePress site. They are large,
self-contained HTML artifacts and should be hosted separately from the docs.

To generate your own report:

```bash
python examples/match_report.py path/to/replay.dem --output ./my_match_report.html
```

Hero and item icons are Valve's artwork, so gem does not ship them. The script
downloads the icons the match needs into the report asset cache before rendering
(`--offline` skips this). From Python, call `gem.reports.fetch_match_icons(match)`
before `write_html_report`; any icon still missing is shown as a name, and the
report logs a warning listing them.
