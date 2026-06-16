"""Quantized float decoder for Source 2 networked fields."""

from __future__ import annotations

import math
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


_QFF_ROUNDDOWN = 1 << 0
_QFF_ROUNDUP = 1 << 1
_QFF_ENCODE_ZERO = 1 << 2
_QFF_ENCODE_INTEGERS = 1 << 3


class QuantizedFloatDecoder:
    """Decoder for Source 2 quantized floats (CNetworkedQuantizedFloat).

    Encodes a float in a fixed bit-width with optional round-up/down and
    zero-preservation flags. Parameters are derived from the field's
    send-table entry.

    Args:
        bit_count: Number of bits used to encode the value, or None/0/>=32
            for no-scale (raw 32-bit IEEE float).
        flags: Bitmask of QFF_* flags, or None for 0.
        low_value: Minimum representable value, or None for 0.0.
        high_value: Maximum representable value, or None for 1.0.
    """

    __slots__ = (
        "low",
        "high",
        "high_low_mul",
        "dec_mul",
        "bitcount",
        "flags",
        "no_scale",
    )

    def __init__(
        self,
        bit_count: int | None,
        flags: int | None,
        low_value: float | None,
        high_value: float | None,
    ) -> None:
        bc = bit_count or 0
        if bc == 0 or bc >= 32:
            self.no_scale = True
            self.bitcount = 32
            self.low = self.high = self.high_low_mul = self.dec_mul = 0.0
            self.flags = 0
            return

        self.no_scale = False
        self.bitcount = bc
        self.low = low_value if low_value is not None else 0.0
        self.high = high_value if high_value is not None else 1.0
        self.flags = flags if flags is not None else 0

        self._validate_flags()

        steps = 1 << self.bitcount
        range_ = self.high - self.low

        if self.flags & _QFF_ROUNDDOWN:
            self.high -= range_ / steps
        elif self.flags & _QFF_ROUNDUP:
            self.low += range_ / steps

        if self.flags & _QFF_ENCODE_INTEGERS:
            delta = max(self.high - self.low, 1.0)
            delta_log2 = math.ceil(math.log2(delta))
            range2 = 1 << int(delta_log2)
            bc2 = self.bitcount
            while (1 << bc2) <= range2:
                bc2 += 1
            if bc2 > self.bitcount:
                self.bitcount = bc2
                steps = 1 << self.bitcount
            offset = range2 / steps
            self.high = self.low + range2 - offset

        self._assign_multipliers(steps)

        if self.flags & _QFF_ROUNDDOWN and self._quantize(self.low) == self.low:
            self.flags &= ~_QFF_ROUNDDOWN
        if self.flags & _QFF_ROUNDUP and self._quantize(self.high) == self.high:
            self.flags &= ~_QFF_ROUNDUP
        if self.flags & _QFF_ENCODE_ZERO and self._quantize(0.0) == 0.0:
            self.flags &= ~_QFF_ENCODE_ZERO

    def _validate_flags(self) -> None:
        if not self.flags:
            return
        if (self.low == 0.0 and self.flags & _QFF_ROUNDDOWN) or (
            self.high == 0.0 and self.flags & _QFF_ROUNDUP
        ):
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.low == 0.0 and self.flags & _QFF_ENCODE_ZERO:
            self.flags |= _QFF_ROUNDDOWN
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.high == 0.0 and self.flags & _QFF_ENCODE_ZERO:
            self.flags |= _QFF_ROUNDUP
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.low > 0.0 or self.high < 0.0:
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.flags & _QFF_ENCODE_INTEGERS:
            self.flags &= ~(_QFF_ROUNDUP | _QFF_ROUNDDOWN | _QFF_ENCODE_ZERO)

    def _assign_multipliers(self, steps: int) -> None:
        range_ = self.high - self.low
        high_int = 0xFFFFFFFE if self.bitcount == 32 else (1 << self.bitcount) - 1
        high_mul = float(high_int) if abs(range_) <= 0.0 else high_int / range_
        if high_mul * range_ > high_int:
            for mult in (0.9999, 0.99, 0.9, 0.8, 0.7):
                high_mul = high_int / range_ * mult
                if high_mul * range_ <= high_int:
                    break
        self.high_low_mul = high_mul
        self.dec_mul = 1.0 / (steps - 1)

    def _quantize(self, val: float) -> float:
        i = int((val - self.low) * self.high_low_mul)
        return self.low + (self.high - self.low) * (i * self.dec_mul)

    def decode(self, r: BitReader) -> float:
        """Read and decode one quantized float from r.

        Args:
            r: BitReader positioned at the start of the encoded value.

        Returns:
            Decoded float value.
        """
        if self.no_scale:
            return struct.unpack("<f", struct.pack("<I", r.read_bits(32)))[0]
        if self.flags & _QFF_ROUNDDOWN and r.read_boolean():
            return self.low
        if self.flags & _QFF_ROUNDUP and r.read_boolean():
            return self.high
        if self.flags & _QFF_ENCODE_ZERO and r.read_boolean():
            return 0.0
        return self.low + (self.high - self.low) * r.read_bits(self.bitcount) * self.dec_mul
