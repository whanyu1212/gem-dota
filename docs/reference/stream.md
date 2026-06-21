# DemoStream

Iterates over the outer `.dem` container format, handling tick-delimited messages and Snappy decompression.

See also: [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)


---

## Generated API

## `gem.binary.stream.DemoStream`

### `DemoStream`

```python
class DemoStream
```

Iterate outer demo-message frames from a Source 2 ``.dem`` source.

Source: [src/gem/binary/stream.py:46](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/stream.py#L46)

#### Methods

##### `close`

Signature: `def DemoStream.close(self) -> None`

Release memory-map and file descriptor resources, if any.

Source: [src/gem/binary/stream.py:80](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/stream.py#L80)

## `gem.binary.stream.OuterMessage`

### `OuterMessage`

```python
class OuterMessage
```

A single top-level demo message frame.

Source: [src/gem/binary/stream.py:31](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/stream.py#L31)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `msg_type` | `int` | `-` |
| `data` | `bytes` | `-` |
