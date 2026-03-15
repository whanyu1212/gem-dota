"""Tests for gem.field_reader — field decoder dispatch and read_fields.

Reference: manta/field_reader.go, manta/field.go (getDecoderForFieldPath)
"""

from __future__ import annotations

from gem.field_path import FieldPath
from gem.field_reader import _get_decoder, _get_decoder_for_field, read_fields
from gem.field_state import FieldState
from gem.sendtable import (
    FIELD_MODEL_FIXED_ARRAY,
    FIELD_MODEL_FIXED_TABLE,
    FIELD_MODEL_SIMPLE,
    FIELD_MODEL_VARIABLE_ARRAY,
    FIELD_MODEL_VARIABLE_TABLE,
    Field,
    Serializer,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_field(
    model: int,
    decoder=None,
    base_decoder=None,
    child_decoder=None,
    serializer=None,
) -> Field:
    """Create a minimal Field with the given model and decoders."""
    f = Field(
        var_name="test",
        var_type="uint32",
        send_node="",
        serializer_name="",
        serializer_version=0,
        encoder="",
        encode_flags=None,
        bit_count=None,
        low_value=None,
        high_value=None,
    )
    f.model = model
    f.decoder = decoder
    f.base_decoder = base_decoder
    f.child_decoder = child_decoder
    f.serializer = serializer
    return f


def _make_fp(*indices: int) -> FieldPath:
    """Build a FieldPath with the given index sequence."""
    fp = FieldPath()
    for i, v in enumerate(indices):
        fp.path[i] = v
    fp.last = len(indices) - 1
    return fp


def _make_serializer(*fields: Field, name: str = "TestSerializer") -> Serializer:
    s = Serializer(name=name, version=0)
    s.fields = list(fields)
    return s


# ---------------------------------------------------------------------------
# _get_decoder_for_field — FIELD_MODEL_SIMPLE
# ---------------------------------------------------------------------------


class TestGetDecoderSimple:
    def test_returns_field_decoder(self):
        def dec(r):
            return 42

        f = _make_field(FIELD_MODEL_SIMPLE, decoder=dec)
        fp = _make_fp(0)
        assert _get_decoder_for_field(f, fp, 1) is dec

    def test_returns_none_when_no_decoder(self):
        f = _make_field(FIELD_MODEL_SIMPLE, decoder=None)
        fp = _make_fp(0)
        assert _get_decoder_for_field(f, fp, 1) is None


# ---------------------------------------------------------------------------
# _get_decoder_for_field — FIELD_MODEL_FIXED_ARRAY
# ---------------------------------------------------------------------------


class TestGetDecoderFixedArray:
    def test_returns_field_decoder(self):
        def dec(r):
            return 99

        f = _make_field(FIELD_MODEL_FIXED_ARRAY, decoder=dec)
        fp = _make_fp(0, 3)
        assert _get_decoder_for_field(f, fp, 1) is dec

    def test_returns_none_when_decoder_absent(self):
        f = _make_field(FIELD_MODEL_FIXED_ARRAY, decoder=None)
        fp = _make_fp(0, 3)
        assert _get_decoder_for_field(f, fp, 1) is None


# ---------------------------------------------------------------------------
# _get_decoder_for_field — FIELD_MODEL_FIXED_TABLE
# ---------------------------------------------------------------------------


class TestGetDecoderFixedTable:
    def test_returns_base_decoder_when_path_ends_at_this_level(self):
        def base_dec(r):
            return True

        f = _make_field(FIELD_MODEL_FIXED_TABLE, base_decoder=base_dec)
        # fp.last == pos - 1  →  fp.last=0, pos=1
        fp = _make_fp(0)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is base_dec

    def test_recurses_into_serializer_when_deeper(self):
        def inner_dec(r):
            return 7

        inner_field = _make_field(FIELD_MODEL_SIMPLE, decoder=inner_dec)
        inner_ser = _make_serializer(inner_field, name="Inner")

        def base_dec(r):
            return True

        f = _make_field(FIELD_MODEL_FIXED_TABLE, base_decoder=base_dec, serializer=inner_ser)
        # path: [0, 0], fp.last=1 → at pos=1 the recursion starts with inner_ser
        fp = _make_fp(0, 0)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is inner_dec


# ---------------------------------------------------------------------------
# _get_decoder_for_field — FIELD_MODEL_VARIABLE_ARRAY
# ---------------------------------------------------------------------------


class TestGetDecoderVariableArray:
    def test_returns_child_decoder_at_element_index(self):
        def child_dec(r):
            return "elem"

        f = _make_field(FIELD_MODEL_VARIABLE_ARRAY, child_decoder=child_dec)
        # fp.last == pos  → fp.last=1, pos=1
        fp = _make_fp(0, 5)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is child_dec

    def test_returns_base_decoder_at_length_slot(self):
        def base_dec(r):
            return 3

        def child_dec(r):
            return "elem"

        f = _make_field(FIELD_MODEL_VARIABLE_ARRAY, base_decoder=base_dec, child_decoder=child_dec)
        # fp.last < pos  → fp.last=0, pos=1
        fp = _make_fp(0)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is base_dec


# ---------------------------------------------------------------------------
# _get_decoder_for_field — FIELD_MODEL_VARIABLE_TABLE
# ---------------------------------------------------------------------------


class TestGetDecoderVariableTable:
    def test_returns_base_decoder_at_length_slot(self):
        def base_dec(r):
            return 2

        f = _make_field(FIELD_MODEL_VARIABLE_TABLE, base_decoder=base_dec)
        # fp.last < pos+1  → fp.last=0, pos=1  → 0 < 2 → base
        fp = _make_fp(0)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is base_dec

    def test_returns_base_decoder_at_boundary(self):
        def base_dec(r):
            return 1

        f = _make_field(FIELD_MODEL_VARIABLE_TABLE, base_decoder=base_dec)
        # fp.last=1, pos=1  → fp.last >= pos+1 is 1>=2 → False → base
        fp = _make_fp(0, 3)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is base_dec

    def test_recurses_into_serializer_for_deep_paths(self):
        def inner_dec(r):
            return "deep"

        inner_field = _make_field(FIELD_MODEL_SIMPLE, decoder=inner_dec)
        inner_ser = _make_serializer(inner_field, name="Inner")

        def base_dec(r):
            return 0

        f = _make_field(FIELD_MODEL_VARIABLE_TABLE, base_decoder=base_dec, serializer=inner_ser)
        # path [0, idx, 0], fp.last=2, pos=1  → fp.last >= pos+1 is 2>=2 → True → recurse
        fp = _make_fp(0, 3, 0)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is inner_dec


# ---------------------------------------------------------------------------
# _get_decoder_for_field — unknown model falls through to f.decoder
# ---------------------------------------------------------------------------


class TestGetDecoderUnknownModel:
    def test_unknown_model_returns_decoder(self):
        def dec(r):
            return 0

        f = _make_field(99, decoder=dec)  # 99 is not a known model constant
        fp = _make_fp(0)
        result = _get_decoder_for_field(f, fp, 1)
        assert result is dec


# ---------------------------------------------------------------------------
# _get_decoder — top-level dispatch
# ---------------------------------------------------------------------------


class TestGetDecoder:
    def test_dispatches_to_first_field(self):
        def dec(r):
            return 5

        f0 = _make_field(FIELD_MODEL_SIMPLE, decoder=dec)
        f1 = _make_field(FIELD_MODEL_SIMPLE, decoder=lambda r: 6)
        ser = _make_serializer(f0, f1)
        fp = _make_fp(0)
        assert _get_decoder(ser, fp, 0) is dec

    def test_dispatches_to_second_field(self):
        def dec(r):
            return 6

        f0 = _make_field(FIELD_MODEL_SIMPLE, decoder=lambda r: 5)
        f1 = _make_field(FIELD_MODEL_SIMPLE, decoder=dec)
        ser = _make_serializer(f0, f1)
        fp = _make_fp(1)
        assert _get_decoder(ser, fp, 0) is dec

    def test_nested_path_recurses_via_fixed_table(self):
        def inner_dec(r):
            return 77

        inner_field = _make_field(FIELD_MODEL_SIMPLE, decoder=inner_dec)
        inner_ser = _make_serializer(inner_field, name="Inner")

        def base_dec(r):
            return True

        outer_field = _make_field(
            FIELD_MODEL_FIXED_TABLE, base_decoder=base_dec, serializer=inner_ser
        )
        outer_ser = _make_serializer(outer_field, name="Outer")

        # path: [0, 0], fp.last=1 — goes into inner serializer
        fp = _make_fp(0, 0)
        assert _get_decoder(outer_ser, fp, 0) is inner_dec


# ---------------------------------------------------------------------------
# read_fields — integration with BitReader
# ---------------------------------------------------------------------------


class TestReadFields:
    """Tests for read_fields() using a real BitReader and synthetic field paths.

    We use the Huffman-encoded bit patterns for the simplest field paths:
      PlusOne (op=0) → LSB-first bit: 0
      FieldPathEncodeFinish (op=FinishEncoding) → LSB-first bits: 1,0

    After PlusOne, path[0] goes from -1 to 0, so the path is [0] (depth-0,
    accessing serializer.fields[0]).
    """

    def _bits_to_bytes(self, bit_str: str) -> bytes:
        """Convert a LSB-first bit string to bytes."""
        padded = bit_str + "0" * (-len(bit_str) % 8)
        result = []
        for i in range(0, len(padded), 8):
            byte = 0
            for j, ch in enumerate(padded[i : i + 8]):
                if ch == "1":
                    byte |= 1 << j
            result.append(byte)
        return bytes(result)

    def test_read_fields_writes_decoded_value_into_state(self):
        """A PlusOne path followed by Finish should decode fields[0] once."""
        from gem.reader import BitReader

        # PlusOne (0) then FieldPathEncodeFinish (10) — see test_field_path.py
        data = self._bits_to_bytes("010")

        decoded_values = []

        def capturing_decoder(r: BitReader):
            decoded_values.append(42)
            return 42

        f = _make_field(FIELD_MODEL_SIMPLE, decoder=capturing_decoder)
        ser = _make_serializer(f)
        state = FieldState()

        r = BitReader(data)
        read_fields(r, ser, state)

        assert decoded_values == [42]
        # path[0] == 0 → fields[0] decoded → state slot [0] == 42
        fp = _make_fp(0)
        assert state.get(fp) == 42

    def test_read_fields_no_paths_when_immediate_finish(self):
        """If the first Huffman op is FieldPathEncodeFinish, no fields are decoded."""
        from gem.reader import BitReader

        # FieldPathEncodeFinish immediately
        data = self._bits_to_bytes("10")

        call_count = [0]

        def counting_decoder(r: BitReader):
            call_count[0] += 1
            return 0

        f = _make_field(FIELD_MODEL_SIMPLE, decoder=counting_decoder)
        ser = _make_serializer(f)
        state = FieldState()

        r = BitReader(data)
        read_fields(r, ser, state)

        assert call_count[0] == 0

    def test_read_fields_skips_none_decoder(self):
        """If a field has no decoder (None), read_fields must not call it
        and must leave the state slot untouched (i.e., None)."""
        from gem.reader import BitReader

        # PlusOne then Finish — targets fields[0]
        data = self._bits_to_bytes("010")

        f = _make_field(FIELD_MODEL_SIMPLE, decoder=None)
        ser = _make_serializer(f)
        state = FieldState()

        r = BitReader(data)
        read_fields(r, ser, state)

        fp = _make_fp(0)
        assert state.get(fp) is None

    def test_read_fields_does_not_raise_on_empty_state(self):
        """read_fields on an empty/fresh FieldState must not raise."""
        from gem.reader import BitReader

        data = self._bits_to_bytes("10")  # immediate finish
        ser = _make_serializer()
        state = FieldState()
        r = BitReader(data)
        read_fields(r, ser, state)  # should not raise

    def test_read_fields_calls_decoder_with_reader(self):
        """The decoder must receive the BitReader instance."""
        from gem.reader import BitReader

        data = self._bits_to_bytes("010")

        received_readers = []

        def capturing_decoder(r: BitReader):
            received_readers.append(r)
            return 0

        f = _make_field(FIELD_MODEL_SIMPLE, decoder=capturing_decoder)
        ser = _make_serializer(f)
        state = FieldState()

        r = BitReader(data)
        read_fields(r, ser, state)

        assert len(received_readers) == 1
        assert received_readers[0] is r

    def test_read_fields_returns_none(self):
        """read_fields is a void function — must return None."""
        from gem.reader import BitReader

        data = self._bits_to_bytes("10")
        f = _make_field(FIELD_MODEL_SIMPLE, decoder=lambda r: 0)
        ser = _make_serializer(f)
        state = FieldState()
        r = BitReader(data)
        assert read_fields(r, ser, state) is None
