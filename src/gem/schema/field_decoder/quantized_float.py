"""Quantized float decoder for Source 2 networked fields.

Reference: dotabuff/manta quantizedfloat.go and skadistats/clarity
FloatQuantizedDecoder.java (pinned revisions in CLAUDE.md).
"""

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

_PRECISION_MULTIPLIERS = (0.9999, 0.99, 0.9, 0.8, 0.7)


def _f32(x: float) -> float:
    """Round ``x`` to the nearest IEEE 754 single-precision value."""
    return struct.unpack("<f", struct.pack("<f", x))[0]


def _float32_flags(bit_count: int, flags: int, low: float, high: float) -> int:
    """Return the flags Manta and Clarity keep, computed in float32 as they do.

    Whether ROUNDDOWN, ROUNDUP, and ENCODE_ZERO survive depends on exact
    floating-point equality tests (``quantize(low) == low`` and so on), which
    can come out differently in float32 and float64. Each surviving flag costs a
    bit per value, so this must match the encoder exactly. Every operation below
    rounds to float32 in the same order as ``newQuantizedFloatDecoder``,
    ``assignMultipliers``, and ``quantize`` in dotabuff/manta quantizedfloat.go.

    Args:
        bit_count: Encoded width in bits (1..31).
        flags: ``QFF_*`` bitmask, already validated.
        low: Lower bound before round-down/round-up adjustment.
        high: Upper bound before adjustment.

    Returns:
        The surviving flags, as an unsigned 32-bit mask.
    """
    flags &= 0xFFFFFFFF
    low, high = _f32(low), _f32(high)
    steps = 1 << bit_count

    if flags & _QFF_ROUNDDOWN:
        high = _f32(high - _f32(_f32(high - low) / _f32(steps)))
    elif flags & _QFF_ROUNDUP:
        low = _f32(low + _f32(_f32(high - low) / _f32(steps)))

    if flags & _QFF_ENCODE_INTEGERS:
        delta = max(_f32(high - low), 1.0)
        range2 = 1 << int(math.ceil(math.log2(delta)))
        bc = bit_count
        while (1 << bc) <= range2:
            bc += 1
        if bc > bit_count:
            bit_count = bc
            steps = 1 << bit_count
        offset = _f32(_f32(range2) / _f32(steps))
        high = _f32(_f32(low + _f32(range2)) - offset)

    range_ = _f32(high - low)
    high_int = (1 << bit_count) - 1
    high_int_f = _f32(high_int)
    mul = high_int_f if abs(range_) <= 0.0 else _f32(high_int_f / range_)
    if _f32(mul * range_) > high_int_f or _f32(mul * range_) > high_int:
        for m in _PRECISION_MULTIPLIERS:
            mul = _f32(_f32(high_int_f / range_) * _f32(m))
            if not (_f32(mul * range_) > high_int_f or _f32(mul * range_) > high_int):
                break
    dec_mul = _f32(1.0 / _f32(steps - 1))

    def quantize(val: float) -> float:
        if val < low:
            return low
        if val > high:
            return high
        i = int(_f32(_f32(val - low) * mul))
        return _f32(low + _f32(_f32(high - low) * _f32(_f32(i) * dec_mul)))

    if flags & _QFF_ROUNDDOWN and quantize(low) == low:
        flags &= ~_QFF_ROUNDDOWN
    if flags & _QFF_ROUNDUP and quantize(high) == high:
        flags &= ~_QFF_ROUNDUP
    if flags & _QFF_ENCODE_ZERO and quantize(0.0) == 0.0:
        flags &= ~_QFF_ENCODE_ZERO
    return flags & 0xFFFFFFFF


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
        validated_flags = self.flags

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

        # Which flags survive decides how many bits each value uses, so it must
        # match the reference parsers' float32 arithmetic exactly. The float64
        # bounds and multipliers above are kept for decoding values, which are
        # at most ~1e-4 more precise than float32 results.
        kept = _float32_flags(
            bc, validated_flags, low_value or 0.0, 1.0 if high_value is None else high_value
        )
        self.flags = kept - (1 << 32) if kept >= 1 << 31 else kept

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
