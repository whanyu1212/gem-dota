"""Bit-level reader for Dota 2 Source 2 replay binary data.

Provides LSB-first bit reading, varint decoding, and all primitive
read operations required by the replay parsing pipeline.

Reference: manta/reader.go
"""

from __future__ import annotations

import math
import struct


class BufferError(Exception):
    """Raised when a read operation exceeds the available buffer."""


class BitReader:
    """Reads bits and structured values from a byte buffer in LSB-first order.

    The internal bit buffer accumulates bytes on demand, consuming them
    in least-significant-bit order. Byte-aligned reads use fast paths
    via struct.unpack to avoid per-bit overhead.

    Args:
        buf: The raw bytes to read from.
    """

    __slots__ = ("_buf", "_size", "_pos", "_bit_val", "_bit_count")

    def __init__(self, buf: bytes) -> None:
        self._buf = buf
        self._size = len(buf)
        self._pos = 0
        self._bit_val = 0  # accumulated bit buffer (up to 64 bits)
        self._bit_count = 0  # number of valid bits in _bit_val

    # ------------------------------------------------------------------
    # Internal primitives
    # ------------------------------------------------------------------

    def _next_byte(self) -> int:
        """Read the next raw byte from the buffer.

        Returns:
            int: The next byte as an integer (0–255).

        Raises:
            BufferError: If the buffer is exhausted.
        """
        if self._pos >= self._size:
            raise BufferError(
                f"insufficient buffer: need 1 byte at pos {self._pos}, size {self._size}"
            )
        b = self._buf[self._pos]
        self._pos += 1
        return b

    # ------------------------------------------------------------------
    # Bit-level reads
    # ------------------------------------------------------------------

    def read_bits(self, n: int) -> int:
        """Read n bits from the buffer in LSB-first order.

        Args:
            n: Number of bits to read (0 ≤ n ≤ 32).

        Returns:
            int: The unsigned integer value of the n bits read.

        Raises:
            BufferError: If the buffer is exhausted before n bits are read.
        """
        while n > self._bit_count:
            self._bit_val |= self._next_byte() << self._bit_count
            self._bit_count += 8

        x = self._bit_val & ((1 << n) - 1)
        self._bit_val >>= n
        self._bit_count -= n
        return x

    def read_boolean(self) -> bool:
        """Read a single bit as a boolean.

        Returns:
            bool: True if the bit is 1, False if 0.
        """
        return self.read_bits(1) == 1

    # ------------------------------------------------------------------
    # Byte-level reads
    # ------------------------------------------------------------------

    def _read_byte(self) -> int:
        """Read a single byte, using a fast path when bit-aligned.

        Returns:
            int: The byte value (0–255).
        """
        if self._bit_count == 0:
            return self._next_byte()
        return self.read_bits(8)

    def read_bytes(self, n: int) -> bytes:
        """Read exactly n bytes from the buffer.

        Uses a zero-copy slice when bit-aligned, otherwise reads byte by byte.

        Args:
            n: Number of bytes to read.

        Returns:
            bytes: The n bytes read.

        Raises:
            BufferError: If fewer than n bytes remain.
        """
        if self._bit_count == 0:
            end = self._pos + n
            if end > self._size:
                raise BufferError(
                    f"insufficient buffer: need {n} bytes at pos {self._pos}, size {self._size}"
                )
            chunk = self._buf[self._pos : end]
            self._pos = end
            return chunk

        return bytes(self.read_bits(8) for _ in range(n))

    def read_bits_as_bytes(self, n: int) -> bytes:
        """Read n bits, returning them packed into bytes.

        Args:
            n: Number of bits to read (need not be a multiple of 8).

        Returns:
            bytes: The bits packed into ceil(n/8) bytes.
        """
        out = bytearray()
        while n >= 8:
            out.append(self._read_byte())
            n -= 8
        if n > 0:
            out.append(self.read_bits(n))
        return bytes(out)

    # ------------------------------------------------------------------
    # Little-endian multi-byte reads (fast path via struct)
    # ------------------------------------------------------------------

    def read_le_uint32(self) -> int:
        """Read a little-endian unsigned 32-bit integer.

        Returns:
            int: The decoded uint32 value.
        """
        return struct.unpack_from("<I", self.read_bytes(4))[0]

    def read_le_uint64(self) -> int:
        """Read a little-endian unsigned 64-bit integer.

        Returns:
            int: The decoded uint64 value.
        """
        return struct.unpack_from("<Q", self.read_bytes(8))[0]

    # ------------------------------------------------------------------
    # Variable-length integers
    # ------------------------------------------------------------------

    def read_varuint32(self) -> int:
        """Read an unsigned 32-bit variable-length integer.

        Uses a continuation-bit scheme: the low 7 bits of each byte
        contribute to the value; the high bit signals more bytes follow.
        Stops after 5 bytes (35 bits) to prevent overflow.

        Returns:
            int: The decoded unsigned 32-bit integer.

        Raises:
            BufferError: If the buffer is exhausted mid-varint.
        """
        x = 0
        s = 0
        while True:
            b = self._read_byte()
            x |= (b & 0x7F) << s
            s += 7
            if (b & 0x80) == 0 or s == 35:
                break
        return x

    def read_varint32(self) -> int:
        """Read a signed 32-bit variable-length integer using zigzag encoding.

        Zigzag maps: 0→0, -1→1, 1→2, -2→3, 2→4, …

        Returns:
            int: The decoded signed 32-bit integer.
        """
        ux = self.read_varuint32()
        x = ux >> 1
        if ux & 1:
            x = ~x
        return x & 0xFFFFFFFF if x >= 0 else x | ~0xFFFFFFFF

    def read_varuint64(self) -> int:
        """Read an unsigned 64-bit variable-length integer.

        Returns:
            int: The decoded unsigned 64-bit integer.

        Raises:
            BufferError: If the buffer is exhausted mid-varint.
            OverflowError: If the encoded value exceeds uint64 range.
        """
        x = 0
        s = 0
        for i in range(10):
            b = self._read_byte()
            if b < 0x80:
                if i == 9 and b > 1:
                    raise OverflowError("varuint64 overflows uint64")
                return x | (b << s)
            x |= (b & 0x7F) << s
            s += 7
        raise OverflowError("varuint64 overflows uint64")

    def read_varint64(self) -> int:
        """Read a signed 64-bit variable-length integer using zigzag encoding.

        Returns:
            int: The decoded signed 64-bit integer.
        """
        ux = self.read_varuint64()
        x = ux >> 1
        if ux & 1:
            x = ~x
        return x

    # ------------------------------------------------------------------
    # Specialised unsigned bit-variable reads
    # ------------------------------------------------------------------

    def read_ubit_var(self) -> int:
        """Read a variable-length uint32 using a 6-bit group with 2-bit size hint.

        The top 2 bits of the initial 6-bit read encode how many more bits
        follow for the value:
          - 0b00 → no extension (value fits in low 4 bits)
          - 0b01 → 4 more bits
          - 0b10 → 8 more bits
          - 0b11 → 28 more bits

        Returns:
            int: The decoded unsigned integer.
        """
        ret = self.read_bits(6)
        match ret & 0x30:
            case 0x10:
                ret = (ret & 0x0F) | (self.read_bits(4) << 4)
            case 0x20:
                ret = (ret & 0x0F) | (self.read_bits(8) << 4)
            case 0x30:
                ret = (ret & 0x0F) | (self.read_bits(28) << 4)
        return ret

    def read_ubit_var_fp(self) -> int:
        """Read a variable-length uint32 using field-path encoding.

        Reads progressively more bits until a terminating condition,
        choosing among 2, 4, 10, 17, or 31-bit encodings.

        Returns:
            int: The decoded unsigned integer.
        """
        if self.read_boolean():
            return self.read_bits(2)
        if self.read_boolean():
            return self.read_bits(4)
        if self.read_boolean():
            return self.read_bits(10)
        if self.read_boolean():
            return self.read_bits(17)
        return self.read_bits(31)

    # ------------------------------------------------------------------
    # Float reads
    # ------------------------------------------------------------------

    def read_float(self) -> float:
        """Read an IEEE 754 single-precision float (little-endian).

        Returns:
            float: The decoded float32 value.
        """
        return struct.unpack_from("<f", self.read_bytes(4))[0]

    def read_coord(self) -> float:
        """Read a Source Engine network coordinate as a float.

        Coordinates are encoded as integer + fractional parts with a sign bit.
        An integer part of n is stored as (n - 1), giving a range of 1–16384.
        The fractional part provides 1/32 precision over 5 bits.

        Returns:
            float: The decoded coordinate value.
        """
        has_int = self.read_bits(1)
        has_frac = self.read_bits(1)

        if not has_int and not has_frac:
            return 0.0

        negative = self.read_boolean()
        int_val = (self.read_bits(14) + 1) if has_int else 0
        frac_val = self.read_bits(5) if has_frac else 0

        value = int_val + frac_val * (1.0 / 32.0)
        return -value if negative else value

    def read_angle(self, n: int) -> float:
        """Read a bit-encoded angle of n bits, mapping to [0, 360) degrees.

        Args:
            n: Bit width of the encoded angle.

        Returns:
            float: The angle in degrees.
        """
        return self.read_bits(n) * 360.0 / (1 << n)

    def read_normal(self) -> float:
        """Read a normalised float in the range [-1, 1] using 12 bits.

        Encoded as a sign bit followed by an 11-bit magnitude.

        Returns:
            float: The normalised float value.
        """
        negative = self.read_boolean()
        magnitude = self.read_bits(11)
        value = magnitude * (1.0 / ((1 << 11) - 1.0))
        return -value if negative else value

    def read_3bit_normal(self) -> list[float]:
        """Read a 3-component normal vector using compressed encoding.

        X and Y are each optionally present (1-bit flags), Z is derived
        from the constraint |v|=1. A final sign bit negates Z if set.

        Returns:
            list[float]: A [x, y, z] unit vector.
        """
        ret = [0.0, 0.0, 0.0]
        has_x = self.read_boolean()
        has_y = self.read_boolean()
        if has_x:
            ret[0] = self.read_normal()
        if has_y:
            ret[1] = self.read_normal()
        neg_z = self.read_boolean()
        prod_sum = ret[0] ** 2 + ret[1] ** 2
        ret[2] = math.sqrt(max(0.0, 1.0 - prod_sum))
        if neg_z:
            ret[2] = -ret[2]
        return ret

    # ------------------------------------------------------------------
    # String reads
    # ------------------------------------------------------------------

    def read_string(self) -> str:
        """Read a null-terminated UTF-8 string.

        Returns:
            str: The decoded string, without the null terminator.
        """
        buf = bytearray()
        while True:
            b = self._read_byte()
            if b == 0:
                break
            buf.append(b)
        return buf.decode("utf-8", errors="replace")

    def read_string_n(self, n: int) -> str:
        """Read exactly n bytes and return them as a string.

        Args:
            n: Number of bytes to read.

        Returns:
            str: The decoded string (may contain null bytes).
        """
        return self.read_bytes(n).decode("latin-1")

    # ------------------------------------------------------------------
    # State inspection
    # ------------------------------------------------------------------

    def rem_bits(self) -> int:
        """Return the number of unread bits remaining in the buffer.

        Returns:
            int: Remaining bits count.
        """
        return (self._size - self._pos) * 8 + self._bit_count

    def position(self) -> str:
        """Return a human-readable position string for debugging.

        Returns:
            str: Position as 'byte' or 'byte.bit_offset'.
        """
        if self._bit_count > 0:
            return f"{self._pos - 1}.{8 - self._bit_count}"
        return str(self._pos)
