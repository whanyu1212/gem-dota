"""Bits & bytes practice: build a tiny replay reader, one function at a time.

A companion to the Bits & Bytes crash course
(site/src/content/docs/cookbook/bits-and-bytes-primer.md). Each function below is an exercise
with a docstring saying what to do and which section of the course explains it.
Replace each ``raise NotImplementedError`` with your answer, then run:

    uv run python examples/bits_and_bytes_exercises.py

The grader checks every exercise, including against real bytes from replay
8855242704 and against gem's own ``BitReader``. Exercises you haven't started
show as "not done yet". Stuck? Solutions are in
``examples/bits_and_bytes_solutions.py``.
"""

from __future__ import annotations

import random
import sys
from collections.abc import Callable
from types import ModuleType
from typing import Any

# ---------------------------------------------------------------------------
# Exercises
# ---------------------------------------------------------------------------


def to_binary(byte: int) -> str:
    """Section 1. Return ``byte`` (0..255) as exactly 8 binary digits.

    ``to_binary(0xB7)`` returns ``"10110111"`` and ``to_binary(5)`` returns
    ``"00000101"``. Hint: ``format()``.
    """
    raise NotImplementedError


def get_bits(value: int, start: int, count: int) -> int:
    """Section 2. Return ``count`` bits of ``value``, starting at bit ``start``.

    Bit 0 is the rightmost bit. ``get_bits(0b1011_0111, 4, 2)`` returns
    ``0b11``. Hint: shift down, then mask with ``(1 << count) - 1``.
    """
    raise NotImplementedError


def split_command(command: int) -> tuple[int, bool]:
    """Section 2. Split an envelope's command into ``(msg_type, compressed)``.

    Bit 6 (``0x40``) means the payload is compressed; the other bits are the
    envelope kind. ``split_command(0x47)`` returns ``(7, True)``.
    """
    raise NotImplementedError


def read_le_u32(data: bytes, offset: int) -> int:
    """Section 3. Read a little-endian unsigned 32-bit int at ``offset``.

    Do it with bit operations, not ``struct`` or ``int.from_bytes``: the byte
    at ``offset`` is the lowest.
    """
    raise NotImplementedError


class BitStream:
    """Section 4. Read bits least-significant-bit first, across byte boundaries.

    ``BitStream(bytes([0b0000_1111, 0b1111_0000]))``: ``read_bits(4)`` returns
    ``0b1111``, then ``read_bits(8)`` returns ``0``, then ``read_bits(4)``
    returns ``0b1111``.

    Tip: keep the position as a bit index. For each bit you need, find its byte
    (``pos // 8``) and its bit within that byte (``pos % 8``).
    """

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0  # bit position of the next unread bit

    def read_bits(self, n: int) -> int:
        """Read ``n`` bits (0..32) and return them as an unsigned int."""
        raise NotImplementedError


def to_int32(u: int) -> int:
    """Section 5. Interpret the low 32 bits of ``u`` as a two's-complement int32.

    ``to_int32(0xFFFFFFFF)`` returns ``-1``; ``to_int32(0x1_0000_0005)``
    returns ``5`` (the extra high bit is thrown away).
    """
    raise NotImplementedError


def zigzag_decode(n: int) -> int:
    """Section 5. Decode a zigzag-encoded number.

    0, 1, 2, 3, 4 decode to 0, -1, 1, -2, 2.
    """
    raise NotImplementedError


def read_varint(data: bytes) -> tuple[int, int]:
    """Section 6. Decode one varint from the start of ``data``.

    Return ``(value, number_of_bytes_used)``. ``read_varint(b"\\xac\\x02")``
    returns ``(300, 2)``.
    """
    raise NotImplementedError


def read_ubit_var(stream: BitStream) -> int:
    """Section 6. Read one ``ubit_var`` from ``stream``.

    Read 6 bits. Their top 2 bits say how many more bits follow (0, 4, 8, or
    28); the low 4 bits are the lowest bits of the value.
    """
    raise NotImplementedError


def dequantize(stored: int, bits: int, low: float, high: float) -> float:
    """Section 7. Turn a quantized ``stored`` number back into a float.

    The value is spread in equal steps over ``low``..``high``:
    ``low + (high - low) * stored / (2**bits - 1)``.
    """
    raise NotImplementedError


def decode_prefix(bits: str, codes: dict[str, str]) -> list[str]:
    """Section 8. Decode a string of ``"0"``/``"1"`` with a prefix code.

    ``codes`` maps each code to its symbol, e.g. ``{"0": "A", "10": "B",
    "11": "C"}``. ``decode_prefix("010110", codes)`` returns
    ``["A", "B", "C", "A"]``.
    """
    raise NotImplementedError


def first_inner_message(packet_data: bytes) -> tuple[int, int]:
    """Section 9. Return the ``(type_id, size)`` of the first inner message.

    The bundle starts with a ``ubit_var`` type ID, then a varint size, packed
    back to back as a bitstream. Use your ``BitStream`` and ``read_ubit_var``;
    for the size, read the varint 8 bits at a time from the stream.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Grader (no need to read below this line)
# ---------------------------------------------------------------------------

# Real bytes from replay 8855242704.
_HEADER = bytes.fromhex("50 42 44 45 4d 53 32 00 e0 85 e7 11 6b 85 e7 11")
_FIRST_ENVELOPE = bytes.fromhex("01 ff ff ff ff 0f cb 01")
_FIRST_INNER = bytes.fromhex("88 b7 b4 81 02 01 d9 1b")


def _random_blobs() -> list[bytes]:
    rng = random.Random(8855242704)
    return [bytes(rng.randrange(256) for _ in range(40)) for _ in range(20)]


def _check_bitstream(m: ModuleType) -> None:
    from gem.binary.reader import BitReader

    s = m.BitStream(bytes([0b0000_1111, 0b1111_0000]))
    assert [s.read_bits(4), s.read_bits(8), s.read_bits(4)] == [0b1111, 0, 0b1111]
    rng = random.Random(0)
    for blob in _random_blobs():
        mine, gems = m.BitStream(blob), BitReader(blob)
        for _ in range(12):
            n = rng.randrange(1, 25)
            got, want = mine.read_bits(n), gems.read_bits(n)
            assert got == want, f"read_bits({n}) gave {got}, gem's BitReader gives {want}"


def _check_ubit_var(m: ModuleType) -> None:
    from gem.binary.reader import BitReader

    assert m.read_ubit_var(m.BitStream(_FIRST_INNER)) == 8, "first inner message type"
    assert m.read_ubit_var(m.BitStream(bytes.fromhex("d7 00"))) == 55, "svc_PacketEntities"
    for blob in _random_blobs():
        mine, gems = m.BitStream(blob), BitReader(blob)
        for _ in range(5):
            got, want = m.read_ubit_var(mine), gems.read_ubit_var()
            assert got == want, f"gave {got}, gem's BitReader gives {want}"


def _eq(fn: Callable[..., Any], *args: Any, want: Any) -> None:
    got = fn(*args)
    shown = ", ".join(repr(a) for a in args)
    ok = abs(got - want) < 1e-6 if isinstance(want, float) else got == want
    assert ok, f"{fn.__name__}({shown}) gave {got!r}, expected {want!r}"


# Exercise name -> list of (arguments, expected result).
_CASES: dict[str, list[tuple[tuple[Any, ...], Any]]] = {
    "to_binary": [((0xB7,), "10110111"), ((5,), "00000101"), ((0,), "00000000")],
    "get_bits": [((0b1011_0111, 4, 2), 0b11), ((0b1011_0111, 0, 4), 0b0111), ((0x88, 0, 6), 8)],
    "split_command": [((0x47,), (7, True)), ((0x07,), (7, False)), ((0x42,), (2, True))],
    "read_le_u32": [((_HEADER, 8), 300385760), ((_HEADER, 12), 300385643)],
    "to_int32": [
        ((0xFFFFFFFF,), -1),
        ((0x80000000,), -2147483648),
        ((0x7FFFFFFF,), 2147483647),
        ((0x1_0000_0005,), 5),
    ],
    "zigzag_decode": [
        ((n,), v) for n, v in [(0, 0), (1, -1), (2, 1), (3, -2), (4, 2), (4294967295, -2147483648)]
    ],
    "read_varint": [
        ((b"\x07",), (7, 1)),
        ((b"\xac\x02",), (300, 2)),
        ((_FIRST_ENVELOPE[1:],), (0xFFFFFFFF, 5)),
        ((_FIRST_ENVELOPE[6:],), (203, 2)),
    ],
    "dequantize": [
        ((0, 20, 0.0, 65536.0), 0.0),
        (((1 << 20) - 1, 20, 0.0, 65536.0), 65536.0),
        ((1, 8, 0.0, 255.0), 1.0),
    ],
    "decode_prefix": [
        (("010110", {"0": "A", "10": "B", "11": "C"}), list("ABCA")),
        (("", {"0": "A"}), []),
    ],
    "first_inner_message": [((_FIRST_INNER,), (8, 108894))],
}

# Exercises that need more than a table of cases.
_CUSTOM_CHECKS: dict[str, Callable[[ModuleType], None]] = {
    "BitStream.read_bits": _check_bitstream,
    "read_ubit_var": _check_ubit_var,
}

_ORDER = [
    "to_binary",
    "get_bits",
    "split_command",
    "read_le_u32",
    "BitStream.read_bits",
    "to_int32",
    "zigzag_decode",
    "read_varint",
    "read_ubit_var",
    "dequantize",
    "decode_prefix",
    "first_inner_message",
]


def _check(module: ModuleType, name: str) -> None:
    if name in _CUSTOM_CHECKS:
        _CUSTOM_CHECKS[name](module)
        return
    for args, want in _CASES[name]:
        _eq(getattr(module, name), *args, want=want)


def grade(module: ModuleType) -> tuple[int, int]:
    """Check every exercise in ``module`` and print one line per exercise.

    Returns:
        ``(passed, total)``.
    """
    passed = 0
    for name in _ORDER:
        try:
            _check(module, name)
        except NotImplementedError:
            print(f"  ·  {name}: not done yet")
        except AssertionError as exc:
            print(f"  ✗  {name}: {exc}")
        except Exception as exc:  # a crash in the learner's code
            print(f"  ✗  {name}: raised {type(exc).__name__}: {exc}")
        else:
            passed += 1
            print(f"  ✓  {name}")
    print(f"\n{passed}/{len(_ORDER)} exercises passing")
    return passed, len(_ORDER)


if __name__ == "__main__":
    grade(sys.modules[__name__])
