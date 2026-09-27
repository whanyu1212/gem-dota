"""Solutions for examples/bits_and_bytes_exercises.py.

Try the exercises first. Each solution is written to be read, not to be fast;
gem's real implementations are in ``src/gem/binary/reader.py``.

    uv run python examples/bits_and_bytes_solutions.py
"""

from __future__ import annotations

import sys


def to_binary(byte: int) -> str:
    return format(byte, "08b")


def get_bits(value: int, start: int, count: int) -> int:
    return (value >> start) & ((1 << count) - 1)


def split_command(command: int) -> tuple[int, bool]:
    return command & ~0x40, bool(command & 0x40)


def read_le_u32(data: bytes, offset: int) -> int:
    b0, b1, b2, b3 = data[offset : offset + 4]
    return b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)


class BitStream:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def read_bits(self, n: int) -> int:
        value = 0
        for i in range(n):
            byte = self.data[self.pos // 8]
            bit = (byte >> (self.pos % 8)) & 1
            value |= bit << i  # the first bit read is the lowest bit of the result
            self.pos += 1
        return value


def to_int32(u: int) -> int:
    u &= 0xFFFFFFFF
    return u - (1 << 32) if u >= 1 << 31 else u


def zigzag_decode(n: int) -> int:
    return (n >> 1) ^ -(n & 1)


def read_varint(data: bytes) -> tuple[int, int]:
    value = shift = 0
    for i, b in enumerate(data):
        value |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            return value, i + 1
    raise ValueError("ran out of bytes")


def read_ubit_var(stream: BitStream) -> int:
    first = stream.read_bits(6)
    extra_bits = {0b00: 0, 0b01: 4, 0b10: 8, 0b11: 28}[first >> 4]
    return (first & 0b1111) | (stream.read_bits(extra_bits) << 4)


def dequantize(stored: int, bits: int, low: float, high: float) -> float:
    return low + (high - low) * stored / ((1 << bits) - 1)


def decode_prefix(bits: str, codes: dict[str, str]) -> list[str]:
    out: list[str] = []
    current = ""
    for bit in bits:
        current += bit
        if current in codes:
            out.append(codes[current])
            current = ""
    return out


def first_inner_message(packet_data: bytes) -> tuple[int, int]:
    stream = BitStream(packet_data)
    type_id = read_ubit_var(stream)
    size = shift = 0
    while True:
        b = stream.read_bits(8)  # a varint byte, even though it isn't byte-aligned
        size |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            return type_id, size


if __name__ == "__main__":
    from bits_and_bytes_exercises import grade

    grade(sys.modules[__name__])
