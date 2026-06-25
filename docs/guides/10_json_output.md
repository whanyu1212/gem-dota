# JSON Output Shape

`gem.to_json()` and `gem.parse_to_json()` serialize the same `ParsedMatch` object returned
by `gem.parse()`. The JSON is useful when you want the full nested match structure for an
API response, a saved artifact, or a downstream system that does not use pandas.

```python
import gem

json_str = gem.parse_to_json("my_replay.dem", indent=2)

match = gem.parse("my_replay.dem")
json_str = gem.to_json(match, indent=2)
data = gem.to_dict(match)
```

From the CLI:

```bash
python -m gem my_replay.dem --format json > match.json
```

## Top-level shape

The top-level object mirrors `ParsedMatch`:

```json
{
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
  "radiant_xp_adv": []
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
| `smoke_events` | Smoke of Deceit activations and grouped heroes |
| `neutral_item_finds` | Neutral item find user messages |
| `vision_modifiers` | Reveal/vision modifier windows used by vision analysis |

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

Use JSON when you need the complete nested match object. Use
`gem.parse_to_dataframe()` when you want analysis-ready tables with stable row shapes.

```python
frames = gem.parse_to_dataframe("my_replay.dem")

players = frames["players"]
combat = frames["combat_log"]
teamfights = frames["opendota_teamfights"]
```

See [Time-Series & DataFrames](05_timeseries.md) for the table list and export examples.
