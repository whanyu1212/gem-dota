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

The `Fights` tab includes one evidence-first positioning map per fight with
pre-engagement, engagement-start, first-death, and fight-end controls. Marker
visibility, position freshness, missing samples, and the current conservative
engagement-start fallback are documented in
[Experimental Features → Teamfight Positioning](../experimental/teamfight-positioning.md).

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
