"""Low-level bit reader for Source 2 replay payloads.

Source 2 replay files and nested net-message payloads mix byte-aligned
protobuf messages with custom LSB-first bitstreams. This module provides the
primitive reads needed to move through those packed sections: bits, bytes,
protobuf-style varints, Source 2 variable-width integers, strings, coordinates,
angles, and compressed normal vectors.

Reference:
    manta/reader.go
"""

from __future__ import annotations

import math
import struct


class BufferReadError(EOFError):
    """Raised when a reader operation runs past the available buffer."""


class BitReader:
    """Stateful reader for Source 2's LSB-first binary encodings.

    The reader owns a small bit cache over the source buffer. Callers can mix
    bit, byte, varint, string, and Source network value reads without managing
    alignment themselves. Byte-aligned reads use fast paths via ``struct``;
    unaligned reads continue from the cached bit position.

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
        """Read the next physical byte from the backing buffer.

        Returns:
            int: The next byte as an integer in the range 0..255.

        Raises:
            BufferReadError: If the buffer is exhausted.
        """
        if self._pos >= self._size:
            raise BufferReadError(
                f"insufficient buffer: need 1 byte at pos {self._pos}, size {self._size}"
            )
        b = self._buf[self._pos]
        self._pos += 1
        return b

    # ------------------------------------------------------------------
    # Bit-level reads
    # ------------------------------------------------------------------

    def read_bits(self, n: int) -> int:
        """Read ``n`` bits in Source 2's LSB-first order.

        Refills the bit buffer in 4-byte chunks using struct.unpack_from
        when possible to reduce Python loop iterations.

        Args:
            n: Number of bits to read. Current callers use values in the
                range 0..32.

        Returns:
            int: The unsigned integer value represented by the consumed bits.

        Raises:
            BufferReadError: If the buffer is exhausted before n bits are read.
        """
        while n > self._bit_count:
            # Fast path: load 4 bytes at once if available
            remaining = self._size - self._pos
            if remaining >= 4:
                self._bit_val |= (
                    struct.unpack_from("<I", self._buf, self._pos)[0] << self._bit_count
                )
                self._pos += 4
                self._bit_count += 32
            elif remaining > 0:
                self._bit_val |= self._next_byte() << self._bit_count
                self._bit_count += 8
            else:
                raise BufferReadError(
                    f"insufficient buffer: need {n} bits at pos {self._pos}, size {self._size}"
                )

        x = self._bit_val & ((1 << n) - 1)
        self._bit_val >>= n
        self._bit_count -= n
        return x

    def read_boolean(self) -> bool:
        """Read one bit and interpret it as a boolean.

        Returns:
            bool: True if the bit is 1, False if 0.
        """
        if self._bit_count == 0:
            remaining = self._size - self._pos
            if remaining >= 4:
                self._bit_val = struct.unpack_from("<I", self._buf, self._pos)[0]
                self._pos += 4
                self._bit_count = 32
            else:
                self._bit_val = self._next_byte()
                self._bit_count = 8
        bit = self._bit_val & 1
        self._bit_val >>= 1
        self._bit_count -= 1
        return bit == 1

    # ------------------------------------------------------------------
    # Byte-level reads
    # ------------------------------------------------------------------

    def _read_byte(self) -> int:
        """Read one logical byte from the current bit position.

        Returns:
            int: The byte value in the range 0..255.
        """
        if self._bit_count == 0:
            return self._next_byte()
        return self.read_bits(8)

    def _read_bytes_slow(self, n: int) -> bytes:
        """Read ``n`` bytes using the original byte-by-byte bit path.

        This is intentionally kept as the correctness fallback for odd reader
        states and for benchmark comparisons against the optimized path.
        """
        out = bytearray(n)
        for i in range(n):
            out[i] = self.read_bits(8)
        return bytes(out)

    def read_bytes(self, n: int) -> bytes:
        """Read exactly ``n`` logical bytes from the current position.

        Uses slices for byte-aligned reads and a bulk compose path for
        unaligned reads. Falls back to ``_read_bytes_slow`` for very small
        or unusual states where the original implementation is simpler.

        Args:
            n: Number of bytes to read.

        Returns:
            bytes: The n bytes read.

        Raises:
            BufferReadError: If fewer than n bytes remain.
        """
        if n == 0:
            return b""

        if self._bit_count == 0:
            end = self._pos + n
            if end > self._size:
                raise BufferReadError(
                    f"insufficient buffer: need {n} bytes at pos {self._pos}, size {self._size}"
                )
            chunk = self._buf[self._pos : end]
            self._pos = end
            return chunk

        remaining_bits = (self._size - self._pos) * 8 + self._bit_count
        if n * 8 > remaining_bits:
            raise BufferReadError(
                f"insufficient buffer: need {n} bytes at pos {self.position()}, size {self._size}"
            )

        # Keep the old path for tiny reads; it avoids setup overhead and gives
        # us a local reference implementation for tests and benchmark toggles.
        if n <= 2:
            return self._read_bytes_slow(n)

        parts: list[bytes] = []
        remaining = n

        # The bit cache may hold one or more whole logical bytes because
        # read_bits()/peek_bits() prefetch in chunks. Drain those before
        # touching the backing buffer.
        cached_bytes = min(remaining, self._bit_count // 8)
        if cached_bytes:
            cached_mask = (1 << (cached_bytes * 8)) - 1
            parts.append((self._bit_val & cached_mask).to_bytes(cached_bytes, "little"))
            self._bit_val >>= cached_bytes * 8
            self._bit_count -= cached_bytes * 8
            remaining -= cached_bytes

        if remaining == 0:
            return b"".join(parts)

        if self._bit_count == 0:
            end = self._pos + remaining
            parts.append(self._buf[self._pos : end])
            self._pos = end
            return b"".join(parts)

        # General unaligned case. If the cache has s bits (1..7), each output
        # byte is those carry bits plus the low 8-s bits of the next physical
        # byte. Reading exactly `remaining` physical bytes leaves s carry bits.
        start = self._pos
        end = start + remaining
        carry_bits = self._bit_count
        raw = memoryview(self._buf)[start:end]
        combined = self._bit_val | (int.from_bytes(raw, "little") << carry_bits)
        packed = combined.to_bytes(remaining + 1, "little")

        parts.append(packed[:remaining])
        self._bit_val = combined >> (remaining * 8)
        self._bit_count = carry_bits
        self._pos = end
        return b"".join(parts)

    def read_bits_as_bytes(self, n: int) -> bytes:
        """Read ``n`` bits and return them packed into bytes.

        Full bytes are emitted in stream order. If ``n`` is not divisible by
        8, the final output byte contains the remaining low-order bits.
        Larger valid requests use bulk byte reads. Small and truncated requests
        retain byte-by-byte reads, including partial consumption on failure.

        Args:
            n: Number of bits to read (need not be a multiple of 8).

        Returns:
            bytes: The bits packed into ceil(n/8) bytes.
        """
        if n >= 24 and n <= self.rem_bits():
            full_bytes, remainder = divmod(n, 8)
            data = self.read_bytes(full_bytes)
            if remainder:
                data += bytes((self.read_bits(remainder),))
            return data

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
        """Read an unsigned 32-bit protobuf-style varint.

        Uses a continuation-bit scheme: the low 7 bits of each byte
        contribute to the value; the high bit signals more bytes follow.
        Mirrors Manta by stopping after at most 5 bytes.

        Returns:
            int: The decoded unsigned 32-bit integer.

        Raises:
            BufferReadError: If the buffer is exhausted mid-varint.
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
        """Read a signed 32-bit protobuf-style varint using zigzag decoding.

        Zigzag maps signed values onto unsigned varints:
        0 -> 0, -1 -> 1, 1 -> 2, -2 -> 3, 2 -> 4, ...

        Returns:
            int: The decoded signed 32-bit integer.
        """
        ux = self.read_varuint32()
        x = ux >> 1
        if ux & 1:
            x = ~x
        return x & 0xFFFFFFFF if x >= 0 else x | ~0xFFFFFFFF

    def read_varuint64(self) -> int:
        """Read an unsigned 64-bit protobuf-style varint.

        Returns:
            int: The decoded unsigned 64-bit integer.

        Raises:
            BufferReadError: If the buffer is exhausted mid-varint.
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
        """Read a signed 64-bit protobuf-style varint using zigzag decoding.

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
        """Read Source 2's ``UBitVar`` unsigned integer encoding.

        The low 4 bits of the initial 6-bit group hold the base value. The
        top 2 bits of that group select how many extension bits follow:

        - ``0b00``: no extension
        - ``0b01``: read 4 more bits
        - ``0b10``: read 8 more bits
        - ``0b11``: read 28 more bits

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
        """Read Source 2's field-path variable-width integer encoding.

        A sequence of selector bits chooses a 2-, 4-, 10-, 17-, or 31-bit
        payload. Field-path operations use this compact form heavily when
        addressing changed entity fields.

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
        """Read a little-endian IEEE 754 single-precision float.

        Returns:
            float: The decoded float32 value.
        """
        return struct.unpack_from("<f", self.read_bytes(4))[0]

    def read_coord(self) -> float:
        """Read a Source network coordinate.

        Coordinates are encoded as integer + fractional parts with a sign bit.
        An integer part of ``n`` is stored as ``n - 1``, giving a range of
        1..16384.
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
        """Read an angle encoded in ``n`` bits, mapped to [0, 360) degrees.

        Args:
            n: Bit width of the encoded angle.

        Returns:
            float: The angle in degrees.
        """
        return self.read_bits(n) * 360.0 / (1 << n)

    def read_normal(self) -> float:
        """Read a normalized float in the range [-1, 1].

        The value is encoded as a sign bit followed by an 11-bit magnitude.

        Returns:
            float: The normalised float value.
        """
        negative = self.read_boolean()
        magnitude = self.read_bits(11)
        value = magnitude * (1.0 / ((1 << 11) - 1.0))
        return -value if negative else value

    def read_3bit_normal(self) -> list[float]:
        """Read a compressed three-component unit normal vector.

        X and Y are each guarded by a 1-bit presence flag. Z is derived from
        the unit-vector constraint ``|v| = 1`` and may be negated by a final
        sign bit.

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
        """Read exactly ``n`` bytes and return them as a Latin-1 string.

        Args:
            n: Number of bytes to read.

        Returns:
            str: The decoded string, which may contain null bytes.
        """
        return self.read_bytes(n).decode("latin-1")

    # ------------------------------------------------------------------
    # State inspection
    # ------------------------------------------------------------------

    def peek_bits(self, n: int) -> int:
        """Return the next ``n`` bits without consuming logical bits.

        This may read ahead from the backing buffer to refill the internal
        cache, but it does not remove bits from that cache. A subsequent
        ``skip_bits(n)`` or ``read_bits(n)`` consumes the same value.

        Args:
            n: Number of bits to peek. Current callers use values in the
                range 0..32.

        Returns:
            int: The unsigned integer value of the next n bits.

        Raises:
            BufferReadError: If fewer than n bits remain.
        """
        while n > self._bit_count:
            remaining = self._size - self._pos
            if remaining >= 4:
                self._bit_val |= (
                    struct.unpack_from("<I", self._buf, self._pos)[0] << self._bit_count
                )
                self._pos += 4
                self._bit_count += 32
            elif remaining > 0:
                self._bit_val |= self._next_byte() << self._bit_count
                self._bit_count += 8
            else:
                raise BufferReadError(
                    f"insufficient buffer: need {n} bits at pos {self._pos}, size {self._size}"
                )
        return self._bit_val & ((1 << n) - 1)

    def skip_bits(self, n: int) -> None:
        """Discard ``n`` bits that are already loaded in the bit cache.

        This helper does not refill or bounds-check. Callers should only use it
        after ``peek_bits(n)`` or another operation has ensured that
        ``n <= _bit_count``.

        Args:
            n: Number of bits to skip.
        """
        self._bit_val >>= n
        self._bit_count -= n

    def rem_bits(self) -> int:
        """Return the number of logical unread bits remaining.

        Returns:
            int: Remaining bits count.
        """
        return (self._size - self._pos) * 8 + self._bit_count

    def position(self) -> str:
        """Return a reader position string for debugging.

        Returns:
            str: Position as 'byte' or 'byte.bit_offset'.
        """
        consumed_bits = self._pos * 8 - self._bit_count
        byte_pos, bit_offset = divmod(consumed_bits, 8)
        if bit_offset:
            return f"{byte_pos}.{bit_offset}"
        return str(byte_pos)
