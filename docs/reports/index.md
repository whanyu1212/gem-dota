# Match Reports

gem can generate self-contained HTML reports from real `.dem` replay files.

The `Farming` tab in the HTML report is documented in
[Experimental Features → Farming Patterns](../experimental/farming-patterns.md).

## Hosted samples

Sample reports are not bundled into this VitePress site. They are large,
self-contained HTML artifacts and should be hosted separately from the docs.

To generate your own report:

```bash
python examples/match_report.py path/to/replay.dem --output ./my_match_report.html
```
