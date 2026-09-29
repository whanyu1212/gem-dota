# Lane Classifier

Lane role classification from a 10-minute position heatmap.

## Efficiency calculation

`lane_efficiency_pct` uses a fixed denominator of `4948`:

- Creep gold over first 10 minutes: `3448`
- Passive gold (1.5/sec): `900`
- Starting gold: `600`

Formula used by `results/assembly.py` (truncating to integer):
`int(lane_total_gold / 4948 * 100)`

Note: `lane_total_gold` is cumulative total earned gold at 10 minutes (including
the starting 600 gold).

---

## Generated API

## Module `gem.extractors.lane`

Lane assignment from a player's first-10-minute ``lane_pos`` heatmap.

Source: [src/gem/extractors/lane.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/lane.py#L1)

### Top-level functions

### `lane_for_cell`

```python
def lane_for_cell(x: int, y: int) -> int | None
```

Return OpenDota's lane for a map cell.

Source: [src/gem/extractors/lane.py:42](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/lane.py#L42)

### `assign_lane`

```python
def assign_lane(lane_pos: dict[str, dict[str, int]], team: int) -> LaneAssignment
```

Assign a lane from a ``lane_pos`` heatmap, as OpenDota does.

Source: [src/gem/extractors/lane.py:86](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/lane.py#L86)

### Top-level classes

### `LaneAssignment`

```python
class LaneAssignment
```

A player's lane, lane role and roaming flag.

Source: [src/gem/extractors/lane.py:71](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/lane.py#L71)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `lane` | `int` | `0` |
| `lane_role` | `int` | `0` |
| `is_roaming` | `bool` | `False` |
