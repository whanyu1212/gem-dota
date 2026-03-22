# Draft Extractor

Hero pick and ban events with resolution.

---

## Generated API

## Module `gem.extractors.draft`

Draft / hero pick extractor for Dota 2 replays.

Source: [src/gem/extractors/draft.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/draft.py#L1)

### Top-level functions

### `resolve_pick_team`

```python
def resolve_pick_team(event: DraftEvent, players: list[ParsedPlayer]) -> int
```

Resolve the team (2=Radiant, 3=Dire) for a draft event.

Source: [src/gem/extractors/draft.py:82](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/draft.py#L82)

### Top-level classes

### `DraftEvent`

```python
class DraftEvent
```

A single hero ban or pick in the draft.

Source: [src/gem/extractors/draft.py:62](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/draft.py#L62)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `slot_index` | `int` | `-` |
| `hero_id` | `int` | `-` |
| `hero_name` | `str` | `-` |
| `is_pick` | `bool` | `-` |
| `team` | `int` | `0` |

### `DraftExtractor`

```python
class DraftExtractor
```

Detects hero picks and bans by polling ``CDOTAGamerulesProxy``.

Source: [src/gem/extractors/draft.py:124](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/draft.py#L124)

#### Methods

##### `attach`

Signature: `def DraftExtractor.attach(self, parser: ReplayParser) -> None`

Register callbacks with the parser.

Source: [src/gem/extractors/draft.py:162](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/draft.py#L162)

##### `finalize`

Signature: `def DraftExtractor.finalize(self) -> None`

Re-resolve all hero names using the fully-populated live map.

Source: [src/gem/extractors/draft.py:266](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/draft.py#L266)
