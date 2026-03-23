# Gem

<div class="hero-card">
  <h2>Python Dota 2 Replay Parser</h2>
  <p>
    <strong>gem</strong> reads Source 2 <code>.dem</code> replay files and turns them into structured match data.
    Start with Quickstart, then use Troubleshooting and Bits & Bytes Primer if you are new to replay internals.
  </p>
  <div class="hero-actions">
    <a class="VPButton medium brand" href="/guides/01_quickstart">Quickstart</a>
    <a class="VPButton medium alt" href="/guides/troubleshooting">Troubleshooting</a>
    <a class="VPButton medium alt" href="/cookbook/bits-and-bytes-primer">Bits & Bytes Primer</a>
    <a class="VPButton medium alt" href="/cookbook/">Proto Cookbook</a>
    <a class="VPButton medium alt" href="/replay-parser">Replay Parser</a>
    <a class="VPButton medium alt" href="/reports/">Reports</a>
  </div>
</div>

## What You Can Do Today

- Parse Source 2 `.dem` replays into typed match objects with `gem.parse(...)`.
- Export replay data as pandas DataFrames (`gem.parse_to_dataframe(...)`), JSON, or Parquet.
- Access built-in extraction outputs: players, objectives, wards, courier, draft, and teamfights.
- Navigate docs by depth: Quickstart, Troubleshooting, Bits & Bytes Primer, deep-dive guides, and API reference.
