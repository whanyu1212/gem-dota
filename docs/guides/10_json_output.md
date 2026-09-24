# JSON Output Shape

`gem.to_json()` and `gem.parse_to_json()` serialize the same `ParsedMatch` object returned
by `gem.parse()`. JSON is gem's full-fidelity export: it keeps every nested record, and
`gem.load_json()` reads it back into a `ParsedMatch`. Use it for saved artifacts, API
responses, and downstream systems that do not use pandas.

```python
import gem

json_str = gem.parse_to_json("my_replay.dem", indent=2)

match = gem.parse("my_replay.dem")
json_str = gem.to_json(match, indent=2)
data = gem.to_dict(match)  # the same match fields as a plain dict, without metadata
```

From the CLI:

```bash
python -m gem my_replay.dem --format json > match.json
python -m gem my_replay.dem --format json --analysis --output match.json
```

## Saving and loading

Save a parsed match once and load it back later instead of re-parsing the replay.
Loading a 40-minute replay's ~57 MB JSON takes a few seconds; parsing the `.dem` again
takes about a minute.

```python
from pathlib import Path

import gem

match = gem.parse("my_replay.dem")
Path("match.json").write_text(gem.to_json(match), encoding="utf-8")

loaded = gem.load_json("match.json")
assert loaded == match

hero = gem.find_player(loaded, "Axe")  # every analysis helper works on a loaded match
```

`gem.load_json()` restores the original Python types: enums such as `log_type`, tuples such
as `position_log`, and integer keys such as `final_items` slots. `gem.from_dict()` does the
same for an already-decoded JSON object.

## Including analysis results

`gem.analyze(match)` runs every default post-parse analysis (smoke lifecycles, smoke/fight
insights, Roshan conversions, farming routes, and teamfight positioning) and returns a
`MatchAnalysis`. Pass it to `to_json()` to embed the results under an `analysis` key:

```python
analysis = gem.analyze(match)
json_str = gem.to_json(match, analysis=analysis)

# One call from a replay path:
json_str = gem.parse_to_json("my_replay.dem", analyze=True)
```

The `analysis` section is for JSON consumers such as web tools and other languages. It is
not decoded by `gem.load_json()`; in Python, call `gem.analyze(loaded)` again, which gives
the same results.

## Versioning and compatibility

Every `to_json()` payload carries `schema_version` (currently `1`) and `gem_version`
beside the match fields:

- Files from older gem versions, including ones written before `schema_version` existed,
  still load. Fields they do not contain fall back to their defaults.
- Keys the running gem does not know are ignored.
- A file with a `schema_version` newer than the running gem supports raises `ValueError`;
  upgrade `gem-dota` to read it.
- Output is strict JSON: `NaN` and infinite floats raise `ValueError` instead of being
  written as non-standard literals.

## Top-level shape

The top-level object mirrors `ParsedMatch`, plus the version keys and the optional
`analysis` section:

```json
{
  "schema_version": 1,
  "gem_version": "0.10.0",
  "match_id": 8461735141,
  "game_mode": 2,
  "leagueid": 18324,
  "radiant_win": true,
  "duration": 3264,
  "radiant_score": 31,
  "dire_score": 18,
  "players": [],
  "draft": [],
  "combat_log": [],
  "wards": [],
  "objectives": [],
  "teamfights": [],
  "opendota_teamfights": [],
  "smoke_events": [],
  "neutral_item_finds": [],
  "radiant_gold_adv": [],
  "radiant_xp_adv": [],
  "analysis": {}
}
```

The actual output includes more fields than this abbreviated example. For the generated
model documentation, see the [Models API Reference](../reference/models.md).

## Players

`players` contains one object per player slot, ordered 0-4 for Radiant and 5-9 for Dire.

```json
{
  "player_id": 0,
  "hero_name": "npc_dota_hero_sven",
  "player_name": "Ame",
  "team": 2,
  "kills": 11,
  "deaths": 0,
  "assists": 3,
  "net_worth": 37348,
  "last_hits": 605,
  "denies": 32,
  "lane_role": 1,
  "damage_by_type": {
    "physical": 8920,
    "magical": 12340,
    "pure": 450
  },
  "purchase_log": [],
  "position_log": []
}
```

Use `gem.constants.hero_display()` or `gem.catalog.hero_display()` to turn internal hero
NPC names into display names.

## Event arrays

Most match events are arrays of records:

| Field | Contents |
|---|---|
| `combat_log` | Normalized damage, death, heal, item, ability, modifier, gold, XP, rune, and buyback events |
| `draft` | Picks and bans in replay order |
| `wards` | Observer and sentry placements with coordinates |
| `objectives` | OpenDota-shaped objective timeline |
| `towers`, `barracks`, `roshans`, `tormentors`, `shrines` | Typed Gem objective lists |
| `teamfights` | Gem teamfight windows with richer participant stats |
| `opendota_teamfights` | OpenDota-compatible teamfight windows |
| `smoke_events` | Smoke activations with grouped heroes and exact per-member modifier lifecycles |
| `neutral_item_finds` | Neutral item find user messages |
| `vision_modifiers` | Vision-relevant modifier applications with semantic, lifecycle, pairing, and provenance evidence |
| `vision_modifier_pairing_issues` | Ambiguous or orphan modifier removals that were not force-paired |

## Combat log entries

Combat log records share one schema. `log_type` tells you which fields are meaningful for
that row.

```json
{
  "tick": 25969,
  "log_type": "DAMAGE",
  "attacker_name": "npc_dota_hero_sven",
  "target_name": "npc_dota_hero_pangolier",
  "inflictor_name": "sven_storm_bolt",
  "value": 58,
  "attacker_is_hero": true,
  "target_is_hero": true,
  "damage_type": "magical"
}
```

Common `log_type` values include `DAMAGE`, `DEATH`, `HEAL`, `ITEM`, `PURCHASE`,
`ABILITY`, `MODIFIER_ADD`, `MODIFIER_REMOVE`, `GOLD`, `XP`, `PICKUP_RUNE`, and
`BUYBACK`.

## JSON vs DataFrames

Use JSON when you need the complete nested match object, including per-player dicts,
teamfight player breakdowns, and evidence lists. Use `gem.parse_to_dataframe()` when you
want flat, analysis-ready tables with a fixed schema that concatenate across replays.

```python
frames = gem.parse_to_dataframe("my_replay.dem", include=["opendota"])

summary = frames["player_summary"]
combat = frames["combat_log"]
teamfights = frames["opendota_teamfights"]
```

See [Time-Series & DataFrames](05_timeseries.md) for the table list and export examples.
