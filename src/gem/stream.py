"""Outer message stream reader for Dota 2 Source 2 replay files.

Validates the file magic, then iterates outer demo messages, each
yielding a (tick, msg_type, payload) tuple. Handles Snappy
decompression when the DEM_IsCompressed flag is present.

Reference: manta/parser.go (NewStreamParser, readOuterMessage)
           manta/stream.go
"""

from __future__ import annotations

import mmap
import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

_MAGIC_S2 = b"PBDEMS2\x00"
_METADATA_SKIP = 8  # two int32s after magic — file size info, unused
_DEM_IS_COMPRESSED = 64  # EDemoCommands.DEM_IsCompressed = 0x40
_PREGAME_TICK = 0xFFFFFFFF


@dataclass(frozen=True, slots=True)
class OuterMessage:
    """A single decoded outer demo message.

    Attributes:
        tick: Game tick this message belongs to (pre-game normalised to 0).
        msg_type: EDemoCommands value identifying the message type.
        data: Raw (decompressed) protobuf payload bytes.
    """

    tick: int
    msg_type: int
    data: bytes


class DemoStream:
    """Iterates outer messages from a Source 2 .dem file.

    Accepts either a raw byte buffer or a file path. When given a path,
    the file is memory-mapped so large replays are not fully loaded into
    RAM before iteration begins.

    Validates the magic header on construction, then exposes the message
    stream via iteration. Each step yields a (tick, msg_type, data) tuple.

    Args:
        source: A bytes buffer or a str/Path pointing to a .dem file.

    Raises:
        ValueError: If the magic bytes do not match PBDEMS2.
    """

    def __init__(self, source: bytes | str | Path) -> None:
        self._mmap: mmap.mmap | None = None
        self._fd: int | None = None

        if isinstance(source, (str, Path)):
            path = Path(source)
            self._fd = os.open(path, os.O_RDONLY)
            self._mmap = mmap.mmap(self._fd, 0, access=mmap.ACCESS_READ)
            self._buf: bytes | mmap.mmap = self._mmap
        else:
            self._buf = source

        self._pos = 0
        self._validate_magic()
        self._pos += _METADATA_SKIP  # skip file-size metadata

    def close(self) -> None:
        """Release memory-map and file descriptor resources, if any."""
        if self._mmap is not None:
            self._mmap.close()
            self._mmap = None
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None

    def __enter__(self) -> DemoStream:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _validate_magic(self) -> None:
        """Read and validate the 8-byte Source 2 magic header.

        Raises:
            ValueError: If the header does not match 'PBDEMS2\\x00'.
        """
        magic = self._buf[self._pos : self._pos + 8]
        self._pos += 8
        if magic != _MAGIC_S2:
            raise ValueError(f"unexpected magic: expected {_MAGIC_S2!r}, got {magic!r}")

    def _read_varuint32(self) -> int:
        """Read an unsigned 32-bit varint from the raw buffer.

        Operates directly on self._buf / self._pos for performance,
        avoiding a BitReader allocation per outer message.

        Returns:
            int: The decoded varuint32 value.
        """
        x = 0
        s = 0
        while True:
            b = self._buf[self._pos]
            self._pos += 1
            x |= (b & 0x7F) << s
            s += 7
            if (b & 0x80) == 0 or s == 35:
                break
        return x

    def _read_message(self) -> OuterMessage | None:
        """Read and decode the next outer message from the buffer.

        Returns:
            OuterMessage if a message was read, or None at end of stream.
        """
        if self._pos >= len(self._buf):
            return None

        command = self._read_varuint32()
        msg_type = command & ~_DEM_IS_COMPRESSED
        compressed = bool(command & _DEM_IS_COMPRESSED)

        tick = self._read_varuint32()
        if tick == _PREGAME_TICK:
            tick = 0

        size = self._read_varuint32()
        payload = self._buf[self._pos : self._pos + size]
        self._pos += size

        if compressed:
            payload = _snappy_decompress(payload)

        return OuterMessage(tick=tick, msg_type=msg_type, data=payload)

    def __iter__(self) -> Iterator[tuple[int, int, bytes]]:
        """Iterate over all outer messages in the replay.

        Yields:
            tuple[int, int, bytes]: A (tick, msg_type, data) tuple for
            each message. Unpackable directly::

                for tick, msg_type, data in stream:
                    ...
        """
        while True:
            msg = self._read_message()
            if msg is None:
                return
            yield msg.tick, msg.msg_type, msg.data


def _snappy_decompress(data: bytes) -> bytes:
    """Decompress a Snappy-compressed payload.

    Args:
        data: Compressed bytes.

    Returns:
        bytes: The decompressed payload.

    Raises:
        ImportError: If python-snappy is not installed.
        Exception: If decompression fails.
    """
    try:
        import snappy
    except ImportError as exc:
        raise ImportError(
            "Snappy-compressed messages require 'python-snappy'. "
            "Install it with: uv add python-snappy"
        ) from exc
    return snappy.decompress(data)
