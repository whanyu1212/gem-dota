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

Source: [src/gem/binary/stream.py:48](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/stream.py#L48)

#### Methods

##### `close`

Signature: `def DemoStream.close(self) -> None`

Release memory-map and file descriptor resources, if any.

Source: [src/gem/binary/stream.py:82](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/stream.py#L82)

## `gem.binary.stream.OuterMessage`

### `OuterMessage`

```python
class OuterMessage
```

A single top-level demo message frame.

Source: [src/gem/binary/stream.py:33](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/stream.py#L33)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `msg_type` | `int` | `-` |
| `data` | `bytes` | `-` |

## `gem.binary.packet.read_inner_messages`

### `read_inner_messages`

```python
def read_inner_messages(data: bytes) -> list[tuple[int, bytes]]
```

Split a ``CDemoPacket.data`` blob into its inner messages.

Source: [src/gem/binary/packet.py:24](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/packet.py#L24)
