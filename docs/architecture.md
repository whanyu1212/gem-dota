# Architecture

`gem` turns a raw `.dem` binary into structured Python objects in a single pass.
This page shows how the modules fit together and what each layer produces.

---

## Pipeline

```mermaid
flowchart TD
    A(["gem.parse()  /  gem.parse_to_dataframe()"])

    subgraph BINARY ["Binary decoding"]
        direction LR
        B["stream.py\nouter frames"] --> C["reader.py\nbits & varints"]
    end

    subgraph SCHEMA ["Schema & state"]
        direction LR
        D["sendtable.py\nserializer tree"] --> E["field_decoder.py\ntype dispatch"]
        D --> F["field_path.py\nHuffman paths"]
        G["string_table.py\nkey-value tables"]
        H["entities.py\ndelta updates"]
    end

    subgraph EVENTS ["Events"]
        direction LR
        I["game_events.py"]
        J["combatlog.py"]
    end

    subgraph EXTRACT ["Extractors"]
        direction LR
        X1["players"]
        X2["objectives"]
        X3["wards"]
        X4["courier"]
        X5["draft"]
        X6["teamfights"]
    end

    subgraph ASSEMBLE ["Assembly"]
        K["combat_aggregator.py"] --> L["match_builder.py"]
    end

    O(["ParsedMatch"])
    P(["dict[str, DataFrame]  /  JSON  /  Parquet"])

    A --> BINARY
    BINARY --> SCHEMA
    SCHEMA --> EVENTS
    SCHEMA --> EXTRACT
    EVENTS --> ASSEMBLE
    EXTRACT --> ASSEMBLE
    ASSEMBLE --> O
    O --> P
```

---

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
      <span class="arch-badge">stream.py</span>
      <span class="arch-badge">reader.py</span>
      <span class="arch-badge">sendtable.py</span>
      <span class="arch-badge">field_decoder.py</span>
      <span class="arch-badge">field_path.py</span>
      <span class="arch-badge">string_table.py</span>
      <span class="arch-badge">entities.py</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--parse">
    <span class="arch-layer-label">Events</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">game_events.py</span>
      <span class="arch-badge">combatlog.py</span>
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
      <span class="arch-badge">combat_aggregator.py</span>
      <span class="arch-badge">match_builder.py</span>
    </div>
  </div>

  <div class="arch-layer arch-layer--output">
    <span class="arch-layer-label">Output</span>
    <div class="arch-layer-modules">
      <span class="arch-badge">models.py · ParsedMatch</span>
      <span class="arch-badge">dataframes.py</span>
    </div>
  </div>

</div>

---

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
