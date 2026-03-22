# DemoStream

Iterates over the outer `.dem` container format, handling tick-delimited messages and Snappy decompression.

See also: [The .dem Format](../understanding/02_dem_format.md), [Snappy Compression](../understanding/03_snappy.md)


---

## Generated API

## `gem.stream.DemoStream`

### `DemoStream`

```python
class DemoStream
```

Iterates outer messages from a Source 2 .dem file.

Source: [src/gem/stream.py:40](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/stream.py#L40)

#### Methods

##### `close`

Signature: `def DemoStream.close(self) -> None`

Release memory-map and file descriptor resources, if any.

Source: [src/gem/stream.py:73](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/stream.py#L73)

## `gem.stream.OuterMessage`

### `OuterMessage`

```python
class OuterMessage
```

A single decoded outer demo message.

Source: [src/gem/stream.py:26](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/stream.py#L26)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `msg_type` | `int` | `-` |
| `data` | `bytes` | `-` |
