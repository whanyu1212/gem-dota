"""Unit tests for the 40 Huffman field-path operations in gem.field_path.

Each op function is tested in isolation by calling ``FIELD_PATH_OPS[i].fn``
directly with a synthetic ``BitReader`` and a fresh ``FieldPath``, bypassing
Huffman decoding entirely.

Reference: manta/field_path.go, manta/huffman.go
"""

from __future__ import annotations

import pytest

from gem.field_path import FIELD_PATH_OPS, FieldPath
from gem.reader import BitReader

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fp(path: list[int] | None = None, last: int = 0) -> FieldPath:
    """Return a FieldPath with explicit initial state.

    Args:
        path: Seven-element list.  Defaults to the standard reset state
              ``[-1, 0, 0, 0, 0, 0, 0]``.
        last: Initial ``last`` depth.

    Returns:
        A FieldPath initialised with the given state.
    """
    fp = FieldPath()
    if path is not None:
        fp.path[:] = path
    fp.last = last
    return fp


def _r(bits: str) -> BitReader:
    """Build a BitReader from an LSB-first bit string.

    ``'0'`` → low bit 0, ``'1'`` → low bit 1.  The string is padded with
    trailing ``'0'``s to a multiple of 8 before packing.

    Args:
        bits: LSB-first bit string, e.g. ``"100"`` means bit-0=1, bit-1=0, bit-2=0.

    Returns:
        A BitReader containing the packed bytes.
    """
    padded = bits + "0" * (-len(bits) % 8)
    result = []
    for i in range(0, len(padded), 8):
        byte = 0
        for j, ch in enumerate(padded[i : i + 8]):
            if ch == "1":
                byte |= 1 << j
        result.append(byte)
    return BitReader(bytes(result))


def _r_zeros(n_bytes: int = 4) -> BitReader:
    """Return a BitReader filled with ``n_bytes`` zero bytes.

    ``read_ubit_var_fp()`` on all-zero bytes: first boolean = 0, second
    boolean = 0, … eventually reads 31 bits of zeros → returns 0.  Suitable
    for any op that reads one or more ``read_ubit_var_fp()`` calls that should
    all return 0.

    Args:
        n_bytes: Number of zero bytes to provide.

    Returns:
        A BitReader with ``n_bytes`` zero bytes.
    """
    return BitReader(b"\x00" * n_bytes)


# read_ubit_var_fp encoding:
#   leading bit 1  → read 2 more bits → total 3 bits consumed
#   leading bit 0, then 1 → read 4 more bits → total 6 bits consumed
#   leading bit 0, 0, then 1 → read 10 more bits → total 13 bits consumed
#   leading bit 0, 0, 0, then 1 → read 17 more bits → total 22 bits consumed
#   leading bit 0, 0, 0, 0 → read 31 more bits → total 35 bits consumed
#
# All-zero bytes → leading bit 0, 0, 0, 0 → reads 31 bits of zeros → returns 0.
# To encode value V in the 2-bit short form: emit bit 1 (selector) then V in 2 bits.
#   e.g. V=0 → "1" + "00" = "100"
#   e.g. V=1 → "1" + "10" = "110"   (LSB-first: bit0=1, bit1=1, bit2=0)
#   e.g. V=3 → "1" + "11" = "111"   (all three bits set)


def _ubit_var_fp_bits(value: int, form: str = "short") -> str:
    """Return an LSB-first bit string encoding *value* via read_ubit_var_fp.

    Args:
        value: The non-negative integer to encode.
        form: ``"short"`` for the 3-bit form (selector=1, 2-bit value 0-3),
              ``"medium"`` for the 6-bit form (selector=01, 4-bit value 0-15).

    Returns:
        LSB-first bit string.

    Raises:
        ValueError: If value is out of range for the chosen form.
    """
    if form == "short":
        if value > 3:
            raise ValueError(f"value {value} exceeds 2-bit short form range 0-3")
        bits = "1"  # selector bit
        bits += format(value, "02b")[::-1]  # 2-bit value, LSB-first
        return bits
    if form == "medium":
        if value > 15:
            raise ValueError(f"value {value} exceeds 4-bit medium form range 0-15")
        bits = "01"  # two selector bits: first=0, second=1
        bits += format(value, "04b")[::-1]  # 4-bit value, LSB-first
        return bits
    raise ValueError(f"unknown form: {form}")


def _varuint32_bytes(value: int) -> bytes:
    """Encode *value* as a varuint32 (continuation-bit encoding).

    Args:
        value: Non-negative integer to encode.

    Returns:
        Encoded bytes.
    """
    out = []
    while True:
        b = value & 0x7F
        value >>= 7
        if value:
            b |= 0x80
        out.append(b)
        if not value:
            break
    return bytes(out)


def _varint32_bytes(value: int) -> bytes:
    """Encode a signed integer as a zigzag varuint32.

    Args:
        value: Signed integer.

    Returns:
        Zigzag-encoded varuint32 bytes.
    """
    # zigzag encode
    uv = (value << 1) ^ (value >> 31)
    uv &= 0xFFFFFFFF
    return _varuint32_bytes(uv)


def _op(name: str):
    """Look up a FieldPathOp by name from FIELD_PATH_OPS.

    Args:
        name: The operation name, e.g. ``"PlusOne"``.

    Returns:
        The matching FieldPathOp.

    Raises:
        KeyError: If no op with that name exists.
    """
    for op in FIELD_PATH_OPS:
        if op.name == name:
            return op
    raise KeyError(f"no op named {name!r}")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _check_op_count():
    """Assert the table always has exactly 40 ops."""
    assert len(FIELD_PATH_OPS) == 40


# ---------------------------------------------------------------------------
# Group 1 — Simple increment ops (no bits read)
# ---------------------------------------------------------------------------


class TestSimpleIncrementOps:
    """PlusOne … PlusFour: increment path[last] by a fixed amount, no I/O."""

    def test_plus_one_from_initial(self):
        fp = _fp()  # path[0] starts at -1
        _op("PlusOne").fn(_r_zeros(), fp)
        assert fp.path[0] == 0
        assert fp.last == 0

    def test_plus_one_accumulates(self):
        fp = _fp([5, 0, 0, 0, 0, 0, 0])
        _op("PlusOne").fn(_r_zeros(), fp)
        assert fp.path[0] == 6

    def test_plus_one_at_depth_2(self):
        fp = _fp([3, 7, 0, 0, 0, 0, 0], last=1)
        _op("PlusOne").fn(_r_zeros(), fp)
        assert fp.path[1] == 8
        assert fp.path[0] == 3  # untouched

    def test_plus_two_from_initial(self):
        fp = _fp()
        _op("PlusTwo").fn(_r_zeros(), fp)
        assert fp.path[0] == 1

    def test_plus_two_accumulates(self):
        fp = _fp([10, 0, 0, 0, 0, 0, 0])
        _op("PlusTwo").fn(_r_zeros(), fp)
        assert fp.path[0] == 12

    def test_plus_three_from_initial(self):
        fp = _fp()
        _op("PlusThree").fn(_r_zeros(), fp)
        assert fp.path[0] == 2

    def test_plus_three_at_depth(self):
        fp = _fp([0, 0, 5, 0, 0, 0, 0], last=2)
        _op("PlusThree").fn(_r_zeros(), fp)
        assert fp.path[2] == 8

    def test_plus_four_from_initial(self):
        fp = _fp()
        _op("PlusFour").fn(_r_zeros(), fp)
        assert fp.path[0] == 3

    def test_plus_four_at_depth(self):
        fp = _fp([0, 0, 0, 2, 0, 0, 0], last=3)
        _op("PlusFour").fn(_r_zeros(), fp)
        assert fp.path[3] == 6

    def test_simple_ops_do_not_change_last(self):
        """None of the PlusN ops alter fp.last."""
        for name in ("PlusOne", "PlusTwo", "PlusThree", "PlusFour"):
            fp = _fp([0, 0, 0, 0, 0, 0, 0], last=2)
            _op(name).fn(_r_zeros(), fp)
            assert fp.last == 2, f"{name} should not change fp.last"

    def test_simple_ops_do_not_set_done(self):
        for name in ("PlusOne", "PlusTwo", "PlusThree", "PlusFour"):
            fp = _fp()
            _op(name).fn(_r_zeros(), fp)
            assert not fp.done, f"{name} should not set fp.done"


# ---------------------------------------------------------------------------
# Group 2 — PlusN (variable increment)
# ---------------------------------------------------------------------------


class TestPlusN:
    """PlusN: path[last] += read_ubit_var_fp() + 5."""

    def test_plus_n_zero_read(self):
        # all-zero bytes: read_ubit_var_fp() returns 0 → path[0] += 0+5 = 5
        fp = _fp()  # path[0] = -1
        _op("PlusN").fn(_r_zeros(8), fp)
        assert fp.path[0] == -1 + 5  # 4

    def test_plus_n_short_value_1(self):
        # read_ubit_var_fp in short form, value=1: bits "110" (selector=1, value=01 LSB-first)
        # path[0] += 1 + 5 = 6 → -1 + 6 = 5
        fp = _fp()
        r = _r(_ubit_var_fp_bits(1, "short") + "0" * 32)
        _op("PlusN").fn(r, fp)
        assert fp.path[0] == -1 + 6  # 5

    def test_plus_n_short_value_3(self):
        # value=3: bits "111"  → path[0] += 3+5 = 8 → -1+8=7
        fp = _fp()
        r = _r(_ubit_var_fp_bits(3, "short") + "0" * 32)
        _op("PlusN").fn(r, fp)
        assert fp.path[0] == -1 + 8  # 7

    def test_plus_n_medium_value_10(self):
        # medium form, value=10 → path[0] += 10+5=15 → -1+15=14
        fp = _fp()
        r = _r(_ubit_var_fp_bits(10, "medium") + "0" * 32)
        _op("PlusN").fn(r, fp)
        assert fp.path[0] == -1 + 15  # 14

    def test_plus_n_does_not_change_last(self):
        fp = _fp(last=2)
        fp.path[2] = 0
        _op("PlusN").fn(_r_zeros(8), fp)
        assert fp.last == 2

    def test_plus_n_operates_at_depth(self):
        fp = _fp([0, 0, 10, 0, 0, 0, 0], last=2)
        _op("PlusN").fn(_r_zeros(8), fp)
        assert fp.path[2] == 10 + 5


# ---------------------------------------------------------------------------
# Group 3 — Push-one ops (increase depth by 1)
# ---------------------------------------------------------------------------


class TestPushOneOps:
    """PushOne* ops: all increase fp.last by exactly 1."""

    # --- PushOneLeftDeltaZeroRightZero (idx 5) ---

    def test_push1_l0_r0_increments_last(self):
        fp = _fp()
        _op("PushOneLeftDeltaZeroRightZero").fn(_r_zeros(), fp)
        assert fp.last == 1

    def test_push1_l0_r0_sets_new_level_to_zero(self):
        fp = _fp([3, 99, 0, 0, 0, 0, 0], last=0)
        _op("PushOneLeftDeltaZeroRightZero").fn(_r_zeros(), fp)
        assert fp.path[1] == 0

    def test_push1_l0_r0_does_not_change_left(self):
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushOneLeftDeltaZeroRightZero").fn(_r_zeros(), fp)
        assert fp.path[0] == 5  # left unchanged

    # --- PushOneLeftDeltaZeroRightNonZero (idx 6) ---

    def test_push1_l0_rn_increments_last(self):
        fp = _fp()
        # short form, value=0 → new level = 0
        r = _r(_ubit_var_fp_bits(0, "short") + "0" * 32)
        _op("PushOneLeftDeltaZeroRightNonZero").fn(r, fp)
        assert fp.last == 1

    def test_push1_l0_rn_sets_new_level_from_read(self):
        fp = _fp([3, 0, 0, 0, 0, 0, 0], last=0)
        # short form, value=2 → new level = 2
        r = _r(_ubit_var_fp_bits(2, "short") + "0" * 32)
        _op("PushOneLeftDeltaZeroRightNonZero").fn(r, fp)
        assert fp.path[1] == 2
        assert fp.path[0] == 3  # left unchanged

    # --- PushOneLeftDeltaOneRightZero (idx 7) ---

    def test_push1_l1_r0_increments_left(self):
        fp = _fp([4, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushOneLeftDeltaOneRightZero").fn(_r_zeros(), fp)
        assert fp.path[0] == 5

    def test_push1_l1_r0_increments_last(self):
        fp = _fp()
        _op("PushOneLeftDeltaOneRightZero").fn(_r_zeros(), fp)
        assert fp.last == 1

    def test_push1_l1_r0_new_level_is_zero(self):
        fp = _fp()
        _op("PushOneLeftDeltaOneRightZero").fn(_r_zeros(), fp)
        assert fp.path[1] == 0

    # --- PushOneLeftDeltaOneRightNonZero (idx 8) ---

    def test_push1_l1_rn_increments_left_and_last(self):
        fp = _fp([4, 0, 0, 0, 0, 0, 0], last=0)
        r = _r(_ubit_var_fp_bits(3, "short") + "0" * 32)
        _op("PushOneLeftDeltaOneRightNonZero").fn(r, fp)
        assert fp.path[0] == 5
        assert fp.last == 1
        assert fp.path[1] == 3

    def test_push1_l1_rn_zero_read(self):
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=0)
        r = _r_zeros(8)  # read_ubit_var_fp() → 0
        _op("PushOneLeftDeltaOneRightNonZero").fn(r, fp)
        assert fp.path[0] == 1
        assert fp.last == 1
        assert fp.path[1] == 0

    # --- PushOneLeftDeltaNRightZero (idx 9) ---

    def test_push1_ln_r0_adds_read_to_left(self):
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        # short form value=2 → path[0] += 2 → 7
        r = _r(_ubit_var_fp_bits(2, "short") + "0" * 32)
        _op("PushOneLeftDeltaNRightZero").fn(r, fp)
        assert fp.path[0] == 7
        assert fp.last == 1
        assert fp.path[1] == 0

    def test_push1_ln_r0_zero_read(self):
        fp = _fp([10, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushOneLeftDeltaNRightZero").fn(_r_zeros(8), fp)
        assert fp.path[0] == 10  # += 0
        assert fp.last == 1
        assert fp.path[1] == 0

    # --- PushOneLeftDeltaNRightNonZero (idx 10) ---

    def test_push1_ln_rn_adds_read_plus2_to_left(self):
        # path[last] += read + 2; last += 1; path[last] = read2 + 1
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        # first read: short form value=0 → += 0+2=2 → path[0]=7
        # second read: short form value=1 → path[1]=1+1=2
        r = _r(_ubit_var_fp_bits(0, "short") + _ubit_var_fp_bits(1, "short") + "0" * 32)
        _op("PushOneLeftDeltaNRightNonZero").fn(r, fp)
        assert fp.path[0] == 7
        assert fp.last == 1
        assert fp.path[1] == 2

    def test_push1_ln_rn_both_zero(self):
        fp = _fp([10, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushOneLeftDeltaNRightNonZero").fn(_r_zeros(16), fp)
        assert fp.path[0] == 12  # += 0+2
        assert fp.last == 1
        assert fp.path[1] == 1  # 0+1

    # --- PushOneLeftDeltaNRightNonZeroPack6Bits (idx 11) ---

    def test_push1_ln_rn_pack6_zero_bits(self):
        # reads read_bits(3) and read_bits(3), both 0
        # path[0] += 0+2=2; last += 1; path[1] = 0+1=1
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushOneLeftDeltaNRightNonZeroPack6Bits").fn(_r_zeros(), fp)
        assert fp.path[0] == 7
        assert fp.last == 1
        assert fp.path[1] == 1

    def test_push1_ln_rn_pack6_specific_values(self):
        # 3-bit left = 5 (binary 101 LSB-first = "101"), 3-bit right = 3 (binary 011 LSB-first = "110")
        # path[0] += 5+2=7; path[1] = 3+1=4
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("101" + "110" + "0" * 8)  # left=5, right=3
        _op("PushOneLeftDeltaNRightNonZeroPack6Bits").fn(r, fp)
        assert fp.path[0] == 7
        assert fp.last == 1
        assert fp.path[1] == 4

    # --- PushOneLeftDeltaNRightNonZeroPack8Bits (idx 12) ---

    def test_push1_ln_rn_pack8_zero_bits(self):
        # reads read_bits(4) and read_bits(4), both 0
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushOneLeftDeltaNRightNonZeroPack8Bits").fn(_r_zeros(), fp)
        assert fp.path[0] == 7  # 5 + 0+2
        assert fp.last == 1
        assert fp.path[1] == 1  # 0+1

    def test_push1_ln_rn_pack8_specific_values(self):
        # 4-bit left = 7 (binary 0111 LSB-first = "1110"), 4-bit right = 5 (binary 0101 LSB-first = "1010")
        # path[0] += 7+2=9; path[1] = 5+1=6
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("1110" + "1010" + "0" * 8)  # left=7, right=5
        _op("PushOneLeftDeltaNRightNonZeroPack8Bits").fn(r, fp)
        assert fp.path[0] == 9
        assert fp.last == 1
        assert fp.path[1] == 6


# ---------------------------------------------------------------------------
# Group 4 — Push-two ops (increase depth by 2)
# ---------------------------------------------------------------------------


class TestPushTwoOps:
    """PushTwo* ops: all increase fp.last by exactly 2."""

    # --- PushTwoLeftDeltaZero (idx 13) ---

    def test_push2_l0_zero_reads(self):
        fp = _fp([3, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushTwoLeftDeltaZero").fn(_r_zeros(16), fp)
        assert fp.last == 2
        assert fp.path[1] == 0  # 0 += 0
        assert fp.path[2] == 0  # 0 += 0
        assert fp.path[0] == 3  # unchanged

    def test_push2_l0_with_values(self):
        fp = _fp([3, 0, 0, 0, 0, 0, 0], last=0)
        # first: short 2, second: short 1
        r = _r(_ubit_var_fp_bits(2, "short") + _ubit_var_fp_bits(1, "short") + "0" * 32)
        _op("PushTwoLeftDeltaZero").fn(r, fp)
        assert fp.last == 2
        assert fp.path[1] == 2
        assert fp.path[2] == 1

    # --- PushTwoPack5LeftDeltaZero (idx 14) ---

    def test_push2_pack5_l0_zero(self):
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushTwoPack5LeftDeltaZero").fn(_r_zeros(), fp)
        assert fp.last == 2
        assert fp.path[1] == 0
        assert fp.path[2] == 0

    def test_push2_pack5_l0_specific_values(self):
        # 5-bit values: left=17 (binary 10001 LSB-first "10001"), right=9 (binary 01001 LSB-first "10010")
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("10001" + "10010" + "0" * 8)  # 17, 9
        _op("PushTwoPack5LeftDeltaZero").fn(r, fp)
        assert fp.last == 2
        assert fp.path[1] == 17
        assert fp.path[2] == 9

    # --- PushThreeLeftDeltaZero (idx 15) ---

    def test_push3_l0_zero_reads(self):
        fp = _fp()
        _op("PushThreeLeftDeltaZero").fn(_r_zeros(32), fp)
        assert fp.last == 3

    def test_push3_l0_increments_are_cumulative(self):
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=0)
        # short form values: 1, 2, 3
        r = _r(
            _ubit_var_fp_bits(1, "short")
            + _ubit_var_fp_bits(2, "short")
            + _ubit_var_fp_bits(3, "short")
            + "0" * 32
        )
        _op("PushThreeLeftDeltaZero").fn(r, fp)
        assert fp.last == 3
        assert fp.path[1] == 1
        assert fp.path[2] == 2
        assert fp.path[3] == 3

    # --- PushThreePack5LeftDeltaZero (idx 16) ---

    def test_push3_pack5_l0_zero(self):
        fp = _fp()
        _op("PushThreePack5LeftDeltaZero").fn(_r_zeros(), fp)
        assert fp.last == 3
        assert fp.path[1] == 0
        assert fp.path[2] == 0
        assert fp.path[3] == 0

    def test_push3_pack5_l0_specific_values(self):
        # 5-bit: 3, 5, 7
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("11000" + "10100" + "11100" + "0" * 8)  # 3=0b00011, 5=0b00101, 7=0b00111
        _op("PushThreePack5LeftDeltaZero").fn(r, fp)
        assert fp.last == 3
        assert fp.path[1] == 3
        assert fp.path[2] == 5
        assert fp.path[3] == 7

    # --- PushTwoLeftDeltaOne (idx 17) ---

    def test_push2_l1_increments_left_and_pushes_two(self):
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushTwoLeftDeltaOne").fn(_r_zeros(16), fp)
        assert fp.path[0] == 6  # +1
        assert fp.last == 2
        assert fp.path[1] == 0
        assert fp.path[2] == 0

    # --- PushTwoPack5LeftDeltaOne (idx 18) ---

    def test_push2_pack5_l1_increments_left(self):
        fp = _fp([3, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushTwoPack5LeftDeltaOne").fn(_r_zeros(), fp)
        assert fp.path[0] == 4
        assert fp.last == 2

    # --- PushThreeLeftDeltaOne (idx 19) ---

    def test_push3_l1_increments_left_and_pushes_three(self):
        fp = _fp([2, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushThreeLeftDeltaOne").fn(_r_zeros(32), fp)
        assert fp.path[0] == 3
        assert fp.last == 3

    # --- PushThreePack5LeftDeltaOne (idx 20) ---

    def test_push3_pack5_l1_increments_left(self):
        fp = _fp([7, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushThreePack5LeftDeltaOne").fn(_r_zeros(), fp)
        assert fp.path[0] == 8
        assert fp.last == 3

    # --- PushTwoLeftDeltaN (idx 21) ---

    def test_push2_ln_adds_read_plus2(self):
        # path[last] += read_ubit_var() + 2
        # read_ubit_var() reads 6 bits with 2-bit selector; all-zero = 0
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushTwoLeftDeltaN").fn(_r_zeros(16), fp)
        assert fp.path[0] == 7  # 5 + 0 + 2
        assert fp.last == 2

    # --- PushTwoPack5LeftDeltaN (idx 22) ---

    def test_push2_pack5_ln_adds_read_plus2(self):
        fp = _fp([3, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushTwoPack5LeftDeltaN").fn(_r_zeros(16), fp)
        assert fp.path[0] == 5  # 3 + 0 + 2
        assert fp.last == 2

    # --- PushThreeLeftDeltaN (idx 23) ---

    def test_push3_ln_adds_read_plus2(self):
        fp = _fp([1, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushThreeLeftDeltaN").fn(_r_zeros(32), fp)
        assert fp.path[0] == 3  # 1 + 0 + 2
        assert fp.last == 3

    # --- PushThreePack5LeftDeltaN (idx 24) ---

    def test_push3_pack5_ln_adds_read_plus2(self):
        fp = _fp([4, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushThreePack5LeftDeltaN").fn(_r_zeros(32), fp)
        assert fp.path[0] == 6  # 4 + 0 + 2
        assert fp.last == 3


# ---------------------------------------------------------------------------
# Group 5 — PushN
# ---------------------------------------------------------------------------


class TestPushN:
    """PushN: dynamic depth push using read_ubit_var for count and offsets."""

    def test_push_n_zero_count(self):
        # n=0: no levels pushed; path[last] += read_ubit_var() = 0
        # read_ubit_var reads 6 bits; all-zero → 0
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushN").fn(_r_zeros(4), fp)
        assert fp.last == 0  # no levels pushed
        assert fp.path[0] == 5  # += 0

    def test_push_n_count_1(self):
        # n=1: pushes 1 level; path[last(old)] += read_ubit_var(), then path[last+1] += read_ubit_var_fp()
        # We craft: first read_ubit_var()=1 (6 bits, value=0b000001), then read_ubit_var()=0,
        # then read_ubit_var_fp()=0
        # read_ubit_var encoding: 6 bits read, top 2 bits (bits 4-5) = selector
        # value=1: 6-bit = 0b000001, selector bits (4-5) = 00 → no extension → returns 1
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=0)
        # Encode: first ubit_var=1 (6 bits: 0b000001 LSB-first = "100000"),
        # second ubit_var=0 (6 bits: "000000"), then ubit_var_fp=0 (35 bits zeros)
        r = _r("100000" + "000000" + "0" * 40)  # n=1, delta=0, new_level=0
        _op("PushN").fn(r, fp)
        assert fp.last == 1
        assert fp.path[0] == 0
        assert fp.path[1] == 0


# ---------------------------------------------------------------------------
# Group 6 — PushNAndNonTopological
# ---------------------------------------------------------------------------


class TestPushNAndNonTopological:
    """PushNAndNonTopological: conditional updates to existing levels + push."""

    def test_no_flags_no_count(self):
        # All booleans false (0 bits) for existing levels, then count=0 → nothing pushed
        # last=0 so 1 boolean read for existing levels: 0 (false, no update)
        # then read_ubit_var()=0 → 0 levels pushed
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        _op("PushNAndNonTopological").fn(_r_zeros(8), fp)
        assert fp.path[0] == 5  # unchanged
        assert fp.last == 0

    def test_flag_true_updates_existing_level(self):
        # last=0: read 1 boolean (true) → read varint32 → path[0] += varint32+1
        # For varint32=0 (zigzag bytes: 0x00): path[0] += 0+1 = 1
        # Then read_ubit_var()=0 → no levels pushed
        # bit stream: 1 (boolean true) then varint32(0) = 0x00 (8 bits) then ubit_var=0 (6 bits)
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        varint0 = _varint32_bytes(0)  # zigzag(0)=0x00
        # boolean=1 (1 bit), then varint32(0) bytes as bits, then ubit_var=0 (6 bits)
        varint_bits = "".join(format(b, "08b")[::-1] for b in varint0)
        r = _r("1" + varint_bits + "000000" + "0" * 32)
        _op("PushNAndNonTopological").fn(r, fp)
        assert fp.path[0] == 5 + 0 + 1  # 6
        assert fp.last == 0

    def test_push_levels_with_count(self):
        # last=0: boolean=0 (no update to path[0])
        # count=1: read_ubit_var()=1, then push 1 level with read_ubit_var_fp()=0
        # 6-bit ubit_var: value=1 = "100000"; then ubit_var_fp: all-zero → 0
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("0" + "100000" + "0" * 40)  # boolean=0, ubit_var=1, ubit_var_fp=0
        _op("PushNAndNonTopological").fn(r, fp)
        assert fp.last == 1
        assert fp.path[0] == 5  # unchanged
        assert fp.path[1] == 0


# ---------------------------------------------------------------------------
# Group 7 — Pop-one ops (decrease depth by 1)
# ---------------------------------------------------------------------------


class TestPopOneOps:
    """PopOnePlusOne and PopOnePlusN: pop 1 level then increment."""

    # --- PopOnePlusOne (idx 27) ---

    def test_pop1_plus1_decrements_last(self):
        fp = _fp([3, 7, 0, 0, 0, 0, 0], last=1)
        _op("PopOnePlusOne").fn(_r_zeros(), fp)
        assert fp.last == 0

    def test_pop1_plus1_increments_path_at_new_last(self):
        fp = _fp([3, 7, 0, 0, 0, 0, 0], last=1)
        _op("PopOnePlusOne").fn(_r_zeros(), fp)
        assert fp.path[0] == 4  # 3 + 1

    def test_pop1_plus1_zeroes_popped_level(self):
        fp = _fp([3, 7, 0, 0, 0, 0, 0], last=1)
        _op("PopOnePlusOne").fn(_r_zeros(), fp)
        assert fp.path[1] == 0  # zeroed by pop

    # --- PopOnePlusN (idx 28) ---

    def test_pop1_plus_n_zero_read(self):
        # read_ubit_var_fp() = 0 → path[last] += 0+1 = 1
        fp = _fp([5, 9, 0, 0, 0, 0, 0], last=1)
        _op("PopOnePlusN").fn(_r_zeros(8), fp)
        assert fp.last == 0
        assert fp.path[0] == 6  # 5 + 0 + 1

    def test_pop1_plus_n_specific_value(self):
        # short form value=2 → path[0] += 2+1=3
        fp = _fp([5, 9, 0, 0, 0, 0, 0], last=1)
        r = _r(_ubit_var_fp_bits(2, "short") + "0" * 32)
        _op("PopOnePlusN").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 8  # 5 + 3


# ---------------------------------------------------------------------------
# Group 8 — PopAllButOne ops
# ---------------------------------------------------------------------------


class TestPopAllButOneOps:
    """PopAllButOne* ops: pop all levels except depth 0, then increment path[0]."""

    # --- PopAllButOnePlusOne (idx 29) ---

    def test_pop_all_but1_plus1_from_depth3(self):
        fp = _fp([2, 3, 5, 7, 0, 0, 0], last=3)
        _op("PopAllButOnePlusOne").fn(_r_zeros(), fp)
        assert fp.last == 0
        assert fp.path[0] == 3  # 2 + 1
        # Previously occupied slots are zeroed by pop
        assert fp.path[1] == 0
        assert fp.path[2] == 0
        assert fp.path[3] == 0

    def test_pop_all_but1_plus1_already_at_depth0(self):
        # pop(0) is a no-op; path[0] += 1
        fp = _fp([10, 0, 0, 0, 0, 0, 0], last=0)
        _op("PopAllButOnePlusOne").fn(_r_zeros(), fp)
        assert fp.last == 0
        assert fp.path[0] == 11

    # --- PopAllButOnePlusN (idx 30) ---

    def test_pop_all_but1_plus_n_zero_read(self):
        # read_ubit_var_fp()=0 → path[0] += 0+1=1
        fp = _fp([8, 3, 1, 0, 0, 0, 0], last=2)
        _op("PopAllButOnePlusN").fn(_r_zeros(8), fp)
        assert fp.last == 0
        assert fp.path[0] == 9

    def test_pop_all_but1_plus_n_specific_value(self):
        # short form value=3 → path[0] += 3+1=4
        fp = _fp([1, 2, 3, 0, 0, 0, 0], last=2)
        r = _r(_ubit_var_fp_bits(3, "short") + "0" * 32)
        _op("PopAllButOnePlusN").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 5

    # --- PopAllButOnePlusNPack3Bits (idx 31) ---

    def test_pop_all_but1_pack3_zero_bits(self):
        # read_bits(3) = 0 → path[0] += 0+1=1
        fp = _fp([4, 5, 6, 0, 0, 0, 0], last=2)
        _op("PopAllButOnePlusNPack3Bits").fn(_r_zeros(), fp)
        assert fp.last == 0
        assert fp.path[0] == 5

    def test_pop_all_but1_pack3_value_7(self):
        # 3 bits all set = 7 → path[0] += 7+1=8
        fp = _fp([2, 3, 4, 0, 0, 0, 0], last=2)
        r = _r("111" + "0" * 8)  # 3-bit value = 7
        _op("PopAllButOnePlusNPack3Bits").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 10

    # --- PopAllButOnePlusNPack6Bits (idx 32) ---

    def test_pop_all_but1_pack6_zero_bits(self):
        # read_bits(6) = 0 → path[0] += 0+1=1
        fp = _fp([10, 1, 2, 3, 0, 0, 0], last=3)
        _op("PopAllButOnePlusNPack6Bits").fn(_r_zeros(), fp)
        assert fp.last == 0
        assert fp.path[0] == 11

    def test_pop_all_but1_pack6_value_63(self):
        # 6 bits all set = 63 → path[0] += 63+1=64
        fp = _fp([0, 5, 6, 0, 0, 0, 0], last=2)
        r = _r("111111" + "0" * 8)
        _op("PopAllButOnePlusNPack6Bits").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 64

    def test_pop_all_but1_pack6_specific_value(self):
        # 6-bit value = 10 (binary 001010 LSB-first = "010100")
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("010100" + "0" * 8)  # 6-bit: 10
        _op("PopAllButOnePlusNPack6Bits").fn(r, fp)
        assert fp.path[0] == 16  # 5 + 10 + 1


# ---------------------------------------------------------------------------
# Group 9 — PopN ops
# ---------------------------------------------------------------------------


class TestPopNOps:
    """PopNPlusOne, PopNPlusN, PopNAndNonTopographical."""

    # --- PopNPlusOne (idx 33) ---

    def test_pop_n_plus1_zero_read(self):
        # read_ubit_var_fp()=0 → pop(0) is no-op; path[last] += 1
        fp = _fp([0, 0, 4, 0, 0, 0, 0], last=2)
        _op("PopNPlusOne").fn(_r_zeros(8), fp)
        assert fp.last == 2  # pop(0) = no-op
        assert fp.path[2] == 5

    def test_pop_n_plus1_pop_1(self):
        # short form value=1 → pop(1); path[new last] += 1
        fp = _fp([3, 7, 0, 0, 0, 0, 0], last=1)
        r = _r(_ubit_var_fp_bits(1, "short") + "0" * 32)
        _op("PopNPlusOne").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 4

    def test_pop_n_plus1_pop_2(self):
        fp = _fp([5, 3, 8, 0, 0, 0, 0], last=2)
        r = _r(_ubit_var_fp_bits(2, "short") + "0" * 32)
        _op("PopNPlusOne").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 6

    # --- PopNPlusN (idx 34) ---

    def test_pop_n_plus_n_both_zero(self):
        # read_ubit_var_fp()=0 → pop(0); path[last] += read_varint32()=0
        fp = _fp([0, 0, 3, 0, 0, 0, 0], last=2)
        _op("PopNPlusN").fn(_r_zeros(16), fp)
        assert fp.last == 2  # pop(0) no-op
        assert fp.path[2] == 3  # += 0

    def test_pop_n_plus_n_pop1_add2(self):
        # pop 1 level; path[last] += 2
        # ubit_var_fp=1 (short): pop(1)
        # varint32=2: zigzag(2)=4; encode as varuint32(4) = bytes
        fp = _fp([5, 10, 0, 0, 0, 0, 0], last=1)
        fp_bits = _ubit_var_fp_bits(1, "short")
        # zigzag encode of 2: (2<<1)^(2>>31) = 4; varuint32(4) = 0x04 = bits "00100000" (6 bits with continuation)
        # actually varuint32 uses full bytes; 0x04 in 8-bit LSB = "00100000"
        varint_bits = "".join(format(b, "08b")[::-1] for b in _varint32_bytes(2))
        r = _r(fp_bits + varint_bits + "0" * 32)
        _op("PopNPlusN").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 7  # 5 + 2

    # --- PopNAndNonTopographical (idx 35) ---

    def test_pop_n_non_topo_no_flags(self):
        # pop(0) then no boolean flags true → nothing changed
        fp = _fp([0, 0, 5, 0, 0, 0, 0], last=2)
        _op("PopNAndNonTopographical").fn(_r_zeros(8), fp)
        assert fp.last == 2  # pop(0) no-op
        assert fp.path[2] == 5

    def test_pop_n_non_topo_pop1_no_updates(self):
        # pop 1 (short fp=1), then 2 boolean reads (for last=1 after pop) = false
        fp = _fp([3, 9, 0, 0, 0, 0, 0], last=1)
        fp_bits = _ubit_var_fp_bits(1, "short")
        # After pop(1): last=0, so 1 boolean for path[0]; boolean=0 → no update
        r = _r(fp_bits + "0" + "0" * 32)
        _op("PopNAndNonTopographical").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 3  # unchanged

    def test_pop_n_non_topo_flag_true_updates_level(self):
        # pop(0) then boolean=1 → path[0] += read_varint32()=3
        # read_ubit_var_fp() must return 0: use short form "100" (selector=1, value=00 → 0)
        # Then boolean=1 for path[0], then varint32(3)=zigzag 6
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        pop_bits = _ubit_var_fp_bits(0, "short")  # "100" — returns 0, pop(0) no-op
        varint_bits = "".join(format(b, "08b")[::-1] for b in _varint32_bytes(3))
        r = _r(pop_bits + "1" + varint_bits + "0" * 32)
        _op("PopNAndNonTopographical").fn(r, fp)
        assert fp.last == 0
        assert fp.path[0] == 8  # 5 + 3


# ---------------------------------------------------------------------------
# Group 10 — NonTopological ops
# ---------------------------------------------------------------------------


class TestNonTopologicalOps:
    """NonTopoComplex, NonTopoPenultimatePlusOne, NonTopoComplexPack4Bits."""

    # --- NonTopoComplex (idx 36) ---

    def test_non_topo_complex_no_flags(self):
        # All booleans false → no changes
        fp = _fp([3, 7, 2, 0, 0, 0, 0], last=2)
        _op("NonTopoComplex").fn(_r_zeros(4), fp)
        assert fp.path[0] == 3
        assert fp.path[1] == 7
        assert fp.path[2] == 2
        assert fp.last == 2

    def test_non_topo_complex_flag_first_level(self):
        # last=0: 1 boolean read; if true → path[0] += read_varint32()
        fp = _fp([10, 0, 0, 0, 0, 0, 0], last=0)
        # boolean=1, varint32=5
        varint_bits = "".join(format(b, "08b")[::-1] for b in _varint32_bytes(5))
        r = _r("1" + varint_bits + "0" * 32)
        _op("NonTopoComplex").fn(r, fp)
        assert fp.path[0] == 15
        assert fp.last == 0  # no depth change

    def test_non_topo_complex_updates_multiple_levels(self):
        # last=2: 3 boolean reads
        # flag[0]=1 → path[0] += varint32(1) = 1
        # flag[1]=0 → no change
        # flag[2]=1 → path[2] += varint32(-1) → zigzag(-1)=1, varuint32(1)=1
        fp = _fp([5, 3, 8, 0, 0, 0, 0], last=2)
        v1 = "".join(format(b, "08b")[::-1] for b in _varint32_bytes(1))
        v_neg1 = "".join(format(b, "08b")[::-1] for b in _varint32_bytes(-1))
        r = _r("1" + v1 + "0" + "1" + v_neg1 + "0" * 32)
        _op("NonTopoComplex").fn(r, fp)
        assert fp.path[0] == 6
        assert fp.path[1] == 3  # unchanged
        # varint32(-1): zigzag(-1) = (-1<<1)^(-1>>31) = (-2)^(-1) = 1
        # read_varint32(): reads varuint32=1, then x=1>>1=0, ux&1=1 so x=~0=-1
        # BUT: the function does x & 0xFFFFFFFF if x>=0 else x | ~0xFFFFFFFF
        # ~0 = -1, so negative case: x | (-1 & ~0xFFFFFFFF) = -1 | (mask beyond 32 bits)
        # Actually read_varint32 returns Python int, -1 for zigzag(1)
        # So path[2] += -1 → 8 + (-1) = 7
        assert fp.path[2] == 7
        assert fp.last == 2

    # --- NonTopoPenultimatePlusOne (idx 37) ---

    def test_non_topo_penultimate_plus1_basic(self):
        fp = _fp([3, 7, 0, 0, 0, 0, 0], last=1)
        _op("NonTopoPenultimatePlusOne").fn(_r_zeros(), fp)
        assert fp.path[0] == 4  # last-1 = 0, path[0] += 1
        assert fp.path[1] == 7  # unchanged
        assert fp.last == 1

    def test_non_topo_penultimate_plus1_at_depth3(self):
        fp = _fp([1, 2, 3, 4, 0, 0, 0], last=3)
        _op("NonTopoPenultimatePlusOne").fn(_r_zeros(), fp)
        assert fp.path[2] == 4  # penultimate is last-1 = 2
        assert fp.path[3] == 4  # unchanged
        assert fp.path[0] == 1  # unchanged
        assert fp.last == 3

    def test_non_topo_penultimate_does_not_change_last(self):
        fp = _fp([0, 5, 0, 0, 0, 0, 0], last=1)
        _op("NonTopoPenultimatePlusOne").fn(_r_zeros(), fp)
        assert fp.last == 1

    # --- NonTopoComplexPack4Bits (idx 38) ---

    def test_non_topo_pack4_no_flags(self):
        # All booleans false → no change
        fp = _fp([5, 3, 0, 0, 0, 0, 0], last=1)
        _op("NonTopoComplexPack4Bits").fn(_r_zeros(4), fp)
        assert fp.path[0] == 5
        assert fp.path[1] == 3
        assert fp.last == 1

    def test_non_topo_pack4_flag_true(self):
        # last=0: boolean=1 → path[0] += read_bits(4) - 7
        # 4-bit value = 0 → path[0] += 0-7 = -7
        fp = _fp([10, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("1" + "0000" + "0" * 8)  # boolean=1, 4 bits=0
        _op("NonTopoComplexPack4Bits").fn(r, fp)
        assert fp.path[0] == 3  # 10 + (0-7)

    def test_non_topo_pack4_value_7_is_zero_delta(self):
        # 4-bit value = 7 → path[0] += 7-7 = 0 → no net change
        fp = _fp([5, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("1" + "1110" + "0" * 8)  # boolean=1, 4 bits=7 (LSB-first: 1110)
        _op("NonTopoComplexPack4Bits").fn(r, fp)
        assert fp.path[0] == 5  # += 0

    def test_non_topo_pack4_value_15_max(self):
        # 4-bit value = 15 → path[0] += 15-7 = 8
        fp = _fp([2, 0, 0, 0, 0, 0, 0], last=0)
        r = _r("1" + "1111" + "0" * 8)  # boolean=1, 4 bits=15
        _op("NonTopoComplexPack4Bits").fn(r, fp)
        assert fp.path[0] == 10  # 2 + 8


# ---------------------------------------------------------------------------
# Group 11 — FieldPathEncodeFinish
# ---------------------------------------------------------------------------


class TestFieldPathEncodeFinish:
    """FieldPathEncodeFinish: sets fp.done = True."""

    def test_finish_sets_done(self):
        fp = _fp()
        _op("FieldPathEncodeFinish").fn(_r_zeros(), fp)
        assert fp.done is True

    def test_finish_does_not_change_path(self):
        fp = _fp([3, 7, 2, 0, 0, 0, 0], last=2)
        _op("FieldPathEncodeFinish").fn(_r_zeros(), fp)
        assert fp.path[0] == 3
        assert fp.path[1] == 7
        assert fp.path[2] == 2
        assert fp.last == 2

    def test_finish_does_not_change_last(self):
        fp = _fp([0, 0, 0, 0, 0, 0, 0], last=4)
        _op("FieldPathEncodeFinish").fn(_r_zeros(), fp)
        assert fp.last == 4

    def test_finish_is_last_op(self):
        assert FIELD_PATH_OPS[-1].name == "FieldPathEncodeFinish"


# ---------------------------------------------------------------------------
# Group 12 — Index and name sanity checks
# ---------------------------------------------------------------------------


class TestOpTableSanity:
    """Verify op names, indices, and weights match manta reference exactly."""

    # Op index map verified against manta/field_path.go _make_ops() return slice
    _EXPECTED = [
        (0, "PlusOne", 36271),
        (1, "PlusTwo", 10334),
        (2, "PlusThree", 1375),
        (3, "PlusFour", 646),
        (4, "PlusN", 4128),
        (5, "PushOneLeftDeltaZeroRightZero", 35),
        (6, "PushOneLeftDeltaZeroRightNonZero", 3),
        (7, "PushOneLeftDeltaOneRightZero", 521),
        (8, "PushOneLeftDeltaOneRightNonZero", 2942),
        (9, "PushOneLeftDeltaNRightZero", 560),
        (10, "PushOneLeftDeltaNRightNonZero", 471),
        (11, "PushOneLeftDeltaNRightNonZeroPack6Bits", 10530),
        (12, "PushOneLeftDeltaNRightNonZeroPack8Bits", 251),
        (13, "PushTwoLeftDeltaZero", 0),
        (14, "PushTwoPack5LeftDeltaZero", 0),
        (15, "PushThreeLeftDeltaZero", 0),
        (16, "PushThreePack5LeftDeltaZero", 0),
        (17, "PushTwoLeftDeltaOne", 0),
        (18, "PushTwoPack5LeftDeltaOne", 0),
        (19, "PushThreeLeftDeltaOne", 0),
        (20, "PushThreePack5LeftDeltaOne", 0),
        (21, "PushTwoLeftDeltaN", 0),
        (22, "PushTwoPack5LeftDeltaN", 0),
        (23, "PushThreeLeftDeltaN", 0),
        (24, "PushThreePack5LeftDeltaN", 0),
        (25, "PushN", 0),
        (26, "PushNAndNonTopological", 310),
        (27, "PopOnePlusOne", 2),
        (28, "PopOnePlusN", 0),
        (29, "PopAllButOnePlusOne", 1837),
        (30, "PopAllButOnePlusN", 149),
        (31, "PopAllButOnePlusNPack3Bits", 300),
        (32, "PopAllButOnePlusNPack6Bits", 634),
        (33, "PopNPlusOne", 0),
        (34, "PopNPlusN", 0),
        (35, "PopNAndNonTopographical", 1),
        (36, "NonTopoComplex", 76),
        (37, "NonTopoPenultimatePlusOne", 271),
        (38, "NonTopoComplexPack4Bits", 99),
        (39, "FieldPathEncodeFinish", 25474),
    ]

    @pytest.mark.parametrize("idx,name,weight", _EXPECTED)
    def test_op_name_and_weight(self, idx: int, name: str, weight: int):
        op = FIELD_PATH_OPS[idx]
        assert op.name == name, f"index {idx}: expected name {name!r}, got {op.name!r}"
        assert op.weight == weight, (
            f"index {idx} ({name}): expected weight {weight}, got {op.weight}"
        )

    def test_all_ops_have_callable_fn(self):
        for op in FIELD_PATH_OPS:
            assert callable(op.fn), f"op {op.name}.fn is not callable"

    def test_op_total_count(self):
        assert len(FIELD_PATH_OPS) == 40

    def test_plus_one_is_most_frequent(self):
        """PlusOne has the highest weight after FieldPathEncodeFinish."""
        weights_without_finish = [
            op.weight for op in FIELD_PATH_OPS if op.name != "FieldPathEncodeFinish"
        ]
        assert max(weights_without_finish) == 36271  # PlusOne
