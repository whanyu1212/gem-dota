# Players Extractor

Per-player state snapshots and time-series data.

---

## Generated API

## Module `gem.extractors.players`

Per-tick player statistics extractor for Dota 2 replays.

Source: [src/gem/extractors/players.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/players.py#L1)

### Top-level classes

### `PlayerExtractor`

```python
class PlayerExtractor
```

Polls hero entity state each tick and accumulates player snapshots.

Source: [src/gem/extractors/players.py:53](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/players.py#L53)

#### Methods

##### `attach`

Signature: `def PlayerExtractor.attach(self, parser: ReplayParser) -> None`

Register callbacks with the parser.

Source: [src/gem/extractors/players.py:132](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/players.py#L132)

##### `hero_pos`

Signature: `def PlayerExtractor.hero_pos(self, npc_name: str) -> tuple[float, float] | None`

Return the current world position of a hero by NPC name.

Source: [src/gem/extractors/players.py:254](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/players.py#L254)

##### `time_series`

Signature: `def PlayerExtractor.time_series(self, player_id: int) -> PlayerTimeSeries`

Aggregate snapshots for one player into time-series lists.

Source: [src/gem/extractors/players.py:273](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/players.py#L273)

##### `minute_time_series`

Signature: `def PlayerExtractor.minute_time_series(self, player_id: int) -> PlayerTimeSeries`

Aggregate per-minute snapshots for one player into time-series lists.

Source: [src/gem/extractors/players.py:304](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/players.py#L304)
