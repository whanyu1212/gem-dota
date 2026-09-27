"""Bit-level writers for building synthetic replay byte streams in tests."""

from __future__ import annotations


class BitWriter:
    """Write values into a LSB-first bit stream, matching BitReader's encoding."""

    def __init__(self) -> None:
        self._bits: list[int] = []

    def write_bits(self, value: int, n: int) -> None:
        for i in range(n):
            self._bits.append((value >> i) & 1)

    def write_ubit_var(self, value: int) -> None:
        """Encode matching BitReader.read_ubit_var (6-bit group, 2-bit selector)."""
        if value < 16:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(0, 2)  # selector 00
        elif value < 256:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(1, 2)  # selector 01
            self.write_bits((value >> 4) & 0x0F, 4)
        elif value < 4096:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(2, 2)  # selector 10
            self.write_bits((value >> 4) & 0xFF, 8)
        else:
            self.write_bits(value & 0x0F, 4)
            self.write_bits(3, 2)  # selector 11
            self.write_bits((value >> 4) & 0x0FFFFFFF, 28)

    def write_varuint32(self, value: int) -> None:
        while True:
            b = value & 0x7F
            value >>= 7
            if value:
                self.write_bits(b | 0x80, 8)
            else:
                self.write_bits(b, 8)
                break

    def write_bytes(self, data: bytes) -> None:
        for b in data:
            self.write_bits(b, 8)

    def to_bytes(self) -> bytes:
        bits = self._bits + [0] * (-len(self._bits) % 8)
        out = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte |= bits[i + j] << j
            out.append(byte)
        return bytes(out)


def make_inner_blob(messages: list[tuple[int, bytes]]) -> bytes:
    """Build a CDemoPacket.data bit-stream from (type_id, payload) pairs."""
    bw = BitWriter()
    for type_id, payload in messages:
        bw.write_ubit_var(type_id)
        bw.write_varuint32(len(payload))
        bw.write_bytes(payload)
    return bw.to_bytes()
