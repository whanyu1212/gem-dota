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

## Hosted samples

Sample reports are not bundled into this VitePress site. They are large,
self-contained HTML artifacts and should be hosted separately from the docs.

To generate your own report:

```bash
python examples/match_report.py path/to/replay.dem --output ./my_match_report.html
```
