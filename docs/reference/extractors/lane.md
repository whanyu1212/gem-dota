# Lane Classifier

Lane role classification from a 10-minute position heatmap.

## Efficiency calculation

`lane_efficiency_pct` uses a fixed denominator of `4948`:

- Creep gold over first 10 minutes: `3448`
- Passive gold (1.5/sec): `900`
- Starting gold: `600`

Formula used by `match_builder` (truncating to integer):
`int(lane_total_gold / 4948 * 100)`

Note: `lane_total_gold` is cumulative total earned gold at 10 minutes (including
the starting 600 gold).

::: gem.extractors.lane