# Architecture

`gem` turns a raw `.dem` binary into structured Python objects in a single pass.
This page shows how the modules fit together and what each layer produces.

## Pipeline

Data flows top to bottom in a single pass. The schema layer feeds two parallel
consumers — event processing and the extractors — which both fan back into
assembly.

<div class="arch-flow">

  <div class="arch-flow-node arch-flow--io">
    <span class="arch-flow-title">Entry point</span>
    <span class="arch-flow-desc"><code>gem.parse()</code> · <code>gem.parse_to_dataframe()</code></span>
  </div>

  <div class="arch-flow-arrow" aria-hidden="true">↓</div>

  <div class="arch-flow-node arch-flow--parse">
    <span class="arch-flow-title">Binary decoding</span>
    <span class="arch-flow-desc">Outer demo frames → bits, bytes, and varints</span>
  </div>

  <div class="arch-flow-arrow" aria-hidden="true">↓</div>

  <div class="arch-flow-node arch-flow--parse">
    <span class="arch-flow-title">Schema &amp; state</span>
    <span class="arch-flow-desc">Serializer tree, field decoders, string tables, entity deltas</span>
  </div>

  <div class="arch-flow-arrow arch-flow-arrow--split" aria-hidden="true">↓</div>

  <div class="arch-flow-split">
    <div class="arch-flow-node arch-flow--parse">
      <span class="arch-flow-title">Events</span>
      <span class="arch-flow-desc">Game events &amp; the combat log (S1 + S2)</span>
    </div>
    <div class="arch-flow-node arch-flow--extract">
      <span class="arch-flow-title">Extractors</span>
      <span class="arch-flow-desc">Players, objectives, wards, courier, draft, teamfights</span>
    </div>
  </div>

  <div class="arch-flow-arrow arch-flow-arrow--merge" aria-hidden="true">↓</div>

  <div class="arch-flow-node arch-flow--assemble">
    <span class="arch-flow-title">Assembly</span>
    <span class="arch-flow-desc">Combat aggregation → typed result assembly</span>
  </div>

  <div class="arch-flow-arrow" aria-hidden="true">↓</div>

  <div class="arch-flow-node arch-flow--output">
    <span class="arch-flow-title">Output</span>
    <span class="arch-flow-desc"><code>ParsedMatch</code> → DataFrames · JSON · Parquet</span>
  </div>

</div>

## Layers at a glance

<div class="arch-layers">

  <div class="arch-layer arch-layer--io">
    <span class="arch-layer-label">Entry points</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">gem.parse()</span>
      <span class="arch-badge">gem.parse_to_dataframe()</span>
      <span class="arch-badge">gem.parse_to_json()</span>
      <span class="arch-badge">gem.parse_to_parquet()</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--parse">
    <span class="arch-layer-label">Binary decoding</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">binary/stream.py</span>
      <span class="arch-badge">binary/reader.py</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--parse">
    <span class="arch-layer-label">Schema decoding</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">schema/sendtable/</span>
      <span class="arch-badge">schema/field_decoder/</span>
      <span class="arch-badge">schema/field_path/</span>
      <span class="arch-badge">state/string_table.py</span>
      <span class="arch-badge">state/entities.py</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--parse">
    <span class="arch-layer-label">Events</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">state/game_events.py</span>
      <span class="arch-badge">combat/log.py</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--extract">
    <span class="arch-layer-label">Extractors</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">extractors/players.py</span>
      <span class="arch-badge">extractors/objectives.py</span>
      <span class="arch-badge">extractors/wards.py</span>
      <span class="arch-badge">extractors/courier.py</span>
      <span class="arch-badge">extractors/draft.py</span>
      <span class="arch-badge">extractors/teamfights.py</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--assemble">
    <span class="arch-layer-label">Assembly</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">combat/aggregator.py</span>
      <span class="arch-badge">results/assembly.py</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--output">
    <span class="arch-layer-label">Output</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">results/models.py · ParsedMatch</span>
      <span class="arch-badge">results/dataframes.py</span>
    </div>
  </div>

</div>

## Output model

`gem.parse()` returns a single `ParsedMatch`. Every field is either a scalar or
a list of typed dataclasses — no raw dicts, no untyped payloads.

<table class="output-table">
  <thead>
    <tr>
      <th>Field</th>
      <th>Type</th>
      <th>What it contains</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>players</code></td>
      <td><code>list[ParsedPlayer]</code></td>
      <td>One entry per player — KDA, gold/XP series, purchases, runes, buybacks, positions</td>
    </tr>
    <tr>
      <td><code>draft</code></td>
      <td><code>list[DraftEvent]</code></td>
      <td>Chronological pick and ban events with hero name and team</td>
    </tr>
    <tr>
      <td><code>combat_log</code></td>
      <td><code>list[CombatLogEntry]</code></td>
      <td>Every damage, kill, heal, ability-use, and modifier event</td>
    </tr>
    <tr>
      <td><code>towers / barracks</code></td>
      <td><code>list[TowerKill / BarracksKill]</code></td>
      <td>Objective deaths with tick, team, and killer</td>
    </tr>
    <tr>
      <td><code>roshans</code></td>
      <td><code>list[RoshanKill]</code></td>
      <td>Roshan kills with kill number and killer slot</td>
    </tr>
    <tr>
      <td><code>tormentors / shrines</code></td>
      <td><code>list[TormentorKill / ShrineKill]</code></td>
      <td>Tormentor and Shrine of Wisdom destruction events</td>
    </tr>
    <tr>
      <td><code>wards</code></td>
      <td><code>list[WardEvent]</code></td>
      <td>Ward placements with exact map coordinates</td>
    </tr>
    <tr>
      <td><code>teamfights</code></td>
      <td><code>list[Teamfight]</code></td>
      <td>Detected fight windows with per-player damage, kills, and healing</td>
    </tr>
    <tr>
      <td><code>smoke_events</code></td>
      <td><code>list[SmokeEvent]</code></td>
      <td>Smoke activations with grouped heroes and centroid position</td>
    </tr>
    <tr>
      <td><code>aegis_events</code></td>
      <td><code>list[AegisEvent]</code></td>
      <td>Aegis pickups, steals, and denies</td>
    </tr>
    <tr>
      <td><code>courier_snapshots</code></td>
      <td><code>list[CourierSnapshot]</code></td>
      <td>Courier state sampled each tick</td>
    </tr>
    <tr>
      <td><code>chat</code></td>
      <td><code>list[ChatEntry]</code></td>
      <td>All-chat and team-chat messages</td>
    </tr>
    <tr>
      <td><code>radiant_gold_adv / radiant_xp_adv</code></td>
      <td><code>list[int]</code></td>
      <td>Per-minute Radiant gold and XP advantage curves</td>
    </tr>
  </tbody>
</table>

For the full field listing see the [Models reference](reference/models.md) and
[Full Match Data guide](guides/04_match_data.md).
