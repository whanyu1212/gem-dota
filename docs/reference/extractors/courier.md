# Courier Extractor

Courier state snapshots per tick.

---

## Generated API

## Module `gem.extractors.courier`

Courier state extractor for Dota 2 replays.

Source: [src/gem/extractors/courier.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/courier.py#L1)

### Top-level classes

### `CourierSnapshot`

```python
class CourierSnapshot
```

A single courier state sample at one tick.

Source: [src/gem/extractors/courier.py:22](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/courier.py#L22)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |
| `state` | `int` | `-` |
| `flying` | `bool` | `-` |
| `x` | `float | None` | `-` |
| `y` | `float | None` | `-` |

### `CourierExtractor`

```python
class CourierExtractor
```

Polls courier entity state and accumulates snapshots.

Source: [src/gem/extractors/courier.py:42](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/courier.py#L42)

#### Methods

##### `attach`

Signature: `def CourierExtractor.attach(self, parser: ReplayParser) -> None`

Register callbacks with the parser.

Source: [src/gem/extractors/courier.py:72](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/courier.py#L72)
