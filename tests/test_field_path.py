"""
Tests for gem.schema.field_path — Huffman field path decoding.

Reference: manta/field_path.go, manta/huffman.go
"""

import pytest


@pytest.fixture
def read_field_paths():
    from gem.schema.field_path import read_field_paths

    return read_field_paths


@pytest.fixture
def reader_cls():
    from gem.binary.reader import BitReader

    return BitReader


def _bits_to_bytes(bit_str: str) -> bytes:
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


class TestHuffmanTree:
    """Verify the Huffman tree is built with correct shape."""

    def test_tree_built_on_import(self):
        from gem.schema.field_path import HUFF_TREE

        assert HUFF_TREE is not None

    def test_finish_op_is_most_common(self):
        """FieldPathEncodeFinish has weight 25474 — highest weight, so should be shallow in tree."""
        from gem.schema.field_path import FIELD_PATH_OPS

        finish_op = next(op for op in FIELD_PATH_OPS if op.name == "FieldPathEncodeFinish")
        assert finish_op.weight == 25474

    def test_40_ops_defined(self):
        from gem.schema.field_path import FIELD_PATH_OPS

        assert len(FIELD_PATH_OPS) == 40


class TestFieldPath:
    def test_plus_one_increments_last(self):
        from gem.schema.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 5
        fp.plus_one()
        assert fp.path[0] == 6

    def test_reset_restores_initial_state(self):
        from gem.schema.field_path import FieldPath

        fp = FieldPath()
        fp.path[:] = [9, 8, 7, 6, 5, 4, 3]
        fp.last = 4
        fp.done = True
        fp.reset()
        assert fp.path == [-1, 0, 0, 0, 0, 0, 0]
        assert fp.last == 0
        assert fp.done is False

    def test_pop_reduces_depth(self):
        from gem.schema.field_path import FieldPath

        fp = FieldPath()
        fp.last = 2
        fp.path[1] = 3
        fp.path[2] = 7
        fp.pop(1)
        assert fp.last == 1
        assert fp.path[2] == 0  # zeroed

    def test_pop_all_but_one(self):
        from gem.schema.field_path import FieldPath

        fp = FieldPath()
        fp.last = 3
        fp.pop(3)
        assert fp.last == 0

    def test_copy_is_independent(self):
        from gem.schema.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 10
        fp2 = fp.copy()
        fp2.path[0] = 99
        assert fp.path[0] == 10

    def test_string_representation(self):
        from gem.schema.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 3
        fp.last = 0
        assert fp.to_str() == "3"

    def test_string_multi_level(self):
        from gem.schema.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 1
        fp.path[1] = 2
        fp.last = 1
        assert fp.to_str() == "1/2"

    @pytest.mark.parametrize(
        "indices",
        [(), (0,), (1, 2), (1, 2, 3), (1, 2, 3, 4, 5, 6, 7)],
    )
    def test_tuple_roundtrip_uses_only_active_indices(self, indices):
        from gem.schema.field_path import FieldPath

        fp = FieldPath._from_tuple(indices)

        assert fp.to_tuple() == indices
        assert fp.last == len(indices) - 1


class TestReadFieldPaths:
    def test_returns_list(self, read_field_paths, reader_cls):
        """read_field_paths returns a list (even a one-element list for PlusOne + Finish).

        Huffman bit sequences (LSB-first, verified against the built tree):
          PlusOne              = 0
          FieldPathEncodeFinish = 10
        """
        # PlusOne (0) then FieldPathEncodeFinish (10), padded to a full byte: 0b00000100 = 0x04
        data = _bits_to_bytes("010")
        r = reader_cls(data)
        result = read_field_paths(r)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].to_tuple() == (0,)

    def test_public_results_remain_independent_mutable_paths(self, read_field_paths, reader_cls):
        data = _bits_to_bytes("0010")  # PlusOne, PlusOne, Finish

        first, second = read_field_paths(reader_cls(data))
        first.path[0] = 99

        assert first.to_tuple() == (99,)
        assert second.to_tuple() == (1,)

    def test_compact_reader_does_not_copy_mutable_paths(self, monkeypatch, reader_cls):
        from gem.schema.field_path import FieldPath
        from gem.schema.field_path.path_sequence import _read_compact_field_paths

        def fail_copy(_self):
            pytest.fail("compact decoding must not call FieldPath.copy")

        monkeypatch.setattr(FieldPath, "copy", fail_copy)

        assert _read_compact_field_paths(reader_cls(_bits_to_bytes("0010"))) == [(0,), (1,)]

    def test_empty_result_on_immediate_finish(self, read_field_paths, reader_cls):
        """If the first op decoded is FinishEncoding, result should be empty.

        FieldPathEncodeFinish = bits 1,0 (LSB-first).
        """
        data = _bits_to_bytes("10")
        r = reader_cls(data)
        result = read_field_paths(r)
        assert result == []

    def test_short_buffer_uses_table_refill(self, read_field_paths, reader_cls):
        """A 3-byte stream exercises the optimized byte-at-a-time refill path.

        The Huffman table currently peeks 17 bits. One-byte examples fall back
        to the tree walk, while this payload has enough bits for table decoding
        without enough bytes for the 32-bit refill branch.
        """
        data = _bits_to_bytes("010" + ("0" * 21))
        r = reader_cls(data)
        result = read_field_paths(r)
        assert [fp.to_tuple() for fp in result] == [(0,)]


def _read_field_paths_tree_walk(r):
    """Reference implementation: original bit-at-a-time Huffman tree walk."""
    from gem.schema.field_path import FIELD_PATH_OPS, HUFF_TREE, FieldPath

    fp = FieldPath()
    node = HUFF_TREE
    paths = []
    while not fp.done:
        node = node.right if r.read_bits(1) else node.left
        assert node is not None
        if node.is_leaf:
            FIELD_PATH_OPS[node.value].fn(r, fp)
            if not fp.done:
                paths.append(fp.copy())
            node = HUFF_TREE
    return paths


class TestDecodeTableCrossValidation:
    """Cross-validate the flat decode table against the reference tree walk
    using real entity_data bytes extracted from the truncated fixture dem.

    These tests capture the actual bit streams that flow through read_field_paths
    during a real parse, so any divergence in decoded paths will be caught here
    before touching the full validation suite.
    """

    @pytest.fixture(scope="class")
    def captured_buffers(self):
        """Run a real parse on the truncated dem and capture entity_data payloads
        by monkey-patching read_field_paths to record the BitReader state."""
        import os

        fixture = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "ti14_finals_g3_xg_vs_falcons_truncated.dem",
        )
        if not os.path.exists(fixture):
            pytest.skip("truncated fixture not found")

        import gem.state.entities as entities_mod

        buffers = []
        MAX_CAPTURE = 2000

        original_read_fields = entities_mod.read_fields

        def capturing_read_fields(r, serializer, state):
            # Snapshot the full remaining bytes from the bit reader's buffer
            # at the current position (before any field paths are read).
            # We reconstruct a fresh bytes slice from _pos, adjusting for
            # any bits already loaded into _bit_val.
            if len(buffers) < MAX_CAPTURE:
                # Save current reader state so we can replay it
                saved_buf = r._buf
                saved_pos = r._pos
                saved_bit_val = r._bit_val
                saved_bit_count = r._bit_count
                buffers.append((saved_buf, saved_pos, saved_bit_val, saved_bit_count))
            return original_read_fields(r, serializer, state)

        entities_mod.read_fields = capturing_read_fields
        try:
            import gem

            gem.parse(fixture)
        except Exception:
            pass
        finally:
            entities_mod.read_fields = original_read_fields

        return buffers

    def test_captured_buffers_nonempty(self, captured_buffers):
        """Sanity check: we actually captured some reader snapshots."""
        assert len(captured_buffers) > 0

    def test_table_matches_tree_walk_on_real_data(self, captured_buffers, reader_cls):
        """For each captured reader snapshot, decode field paths with both
        implementations from identical starting state and assert they agree.

        This directly catches any divergence in the decode table without
        requiring a full parse.
        """
        from gem.schema.field_path.path_sequence import _read_compact_field_paths

        for buf, pos, bit_val, bit_count in captured_buffers:

            def make_reader(buf=buf, pos=pos, bit_val=bit_val, bit_count=bit_count):
                r = reader_cls(buf)
                r._pos, r._bit_val, r._bit_count = pos, bit_val, bit_count
                return r

            reference = make_reader()
            expected = [fp.to_tuple() for fp in _read_field_paths_tree_walk(reference)]
            compact = make_reader()
            assert _read_compact_field_paths(compact) == expected
            public = make_reader()
            from gem.schema.field_path import read_field_paths

            assert [fp.to_tuple() for fp in read_field_paths(public)] == expected
            assert compact.position() == public.position() == reference.position()
            assert compact.rem_bits() == public.rem_bits() == reference.rem_bits()


def _original_decode(r, table):
    import struct

    from gem.schema.field_path import _HUFF_TABLE_BITS, FIELD_PATH_OPS, HUFF_TREE, FieldPath

    fp = FieldPath()
    paths = []
    ops = FIELD_PATH_OPS
    table_bits = _HUFF_TABLE_BITS
    mask = (1 << table_bits) - 1

    buf = r._buf
    size = r._size
    unpack_from = struct.unpack_from

    while not fp.done:
        # Inline rem_bits: (size - pos) * 8 + bit_count.
        if (size - r._pos) * 8 + r._bit_count >= table_bits:
            # Inline peek_bits(table_bits): refill then read without consuming.
            while table_bits > r._bit_count:
                remaining = size - r._pos
                if remaining >= 4:
                    r._bit_val |= unpack_from("<I", buf, r._pos)[0] << r._bit_count
                    r._pos += 4
                    r._bit_count += 32
                elif remaining > 0:
                    r._bit_val |= buf[r._pos] << r._bit_count
                    r._pos += 1
                    r._bit_count += 8
                else:
                    break
            bits = r._bit_val & mask
            op_idx, consumed = table[bits]
            # Inline skip_bits(consumed).
            r._bit_val >>= consumed
            r._bit_count -= consumed
        else:
            # Fallback: tree walk for the last few bits.
            node = HUFF_TREE
            while not node.is_leaf:
                node = node.right if r.read_bits(1) else node.left  # type: ignore[assignment]
            op_idx = node.value

        ops[op_idx].fn(r, fp)
        if not fp.done:
            path = fp.path
            last = fp.last
            if last == 0:
                paths.append((path[0],))
            elif last == 1:
                paths.append((path[0], path[1]))
            elif last == 2:
                paths.append((path[0], path[1], path[2]))
            elif last == 3:
                paths.append((path[0], path[1], path[2], path[3]))
            elif last == 4:
                paths.append((path[0], path[1], path[2], path[3], path[4]))
            elif last == 5:
                paths.append((path[0], path[1], path[2], path[3], path[4], path[5]))
            else:
                paths.append((path[0], path[1], path[2], path[3], path[4], path[5], path[6]))

    return paths


@pytest.fixture(scope="module")
def original_table():
    from gem.schema.field_path import _HUFF_TABLE_BITS, HUFF_TREE

    table = [(0, 0)] * (1 << _HUFF_TABLE_BITS)
    stack = [(HUFF_TREE, 0, 0)]
    while stack:
        node, code, depth = stack.pop()
        if node.is_leaf:
            for suffix in range(1 << (_HUFF_TABLE_BITS - depth)):
                table[code | (suffix << depth)] = (node.value, depth)
        else:
            stack.append((node.left, code, depth + 1))
            stack.append((node.right, code | (1 << depth), depth + 1))
    return table


def _reader_state(r):
    return r._pos, r._bit_val, r._bit_count, r.position(), r.rem_bits()


def _decode_outcome(call):
    try:
        return call()
    except Exception as exc:
        return type(exc), str(exc)


def _exact_reader(bits, prefetched=0):
    from gem.binary.reader import BitReader

    # Align at the front so truncations have no invented trailing zero bits.
    padding = -len(bits) % 8
    r = BitReader(_bits_to_bytes("0" * padding + bits))
    r.read_bits(padding)
    if prefetched:
        r.peek_bits(min(prefetched, r.rem_bits()))
    return r


def _codes():
    from gem.schema.field_path import FIELD_PATH_OPS, HUFF_TREE

    result = {}
    stack = [(HUFF_TREE, "")]
    while stack:
        node, bits = stack.pop()
        if node.is_leaf:
            result[FIELD_PATH_OPS[node.value].name] = bits
        else:
            stack.extend([(node.left, bits + "0"), (node.right, bits + "1")])
    return result


class TestPackedHuffman:
    def test_every_entry_matches_original_and_tree(self, original_table):
        from gem.schema.field_path import _HUFF_TABLE_BITS, FIELD_PATH_OPS, HUFF_TREE
        from gem.schema.field_path.huffman import _HUFF_BITS, _HUFF_OPS

        assert type(_HUFF_OPS) is bytes and type(_HUFF_BITS) is bytes
        assert len(_HUFF_OPS) == len(_HUFF_BITS) == 1 << _HUFF_TABLE_BITS == 131072
        assert set(_HUFF_OPS) == set(range(len(FIELD_PATH_OPS)))
        assert min(_HUFF_BITS) > 0 and max(_HUFF_BITS) == 17
        for index, expected in enumerate(original_table):
            node, depth = HUFF_TREE, 0
            while not node.is_leaf:
                node = node.right if (index >> depth) & 1 else node.left
                depth += 1
            assert (_HUFF_OPS[index], _HUFF_BITS[index]) == expected == (node.value, depth)

    @pytest.mark.parametrize("prefetched", [0, 8, 16, 17, 18, 24, 32])
    def test_truncations_and_malformed_sequences_match_original(self, original_table, prefetched):
        from gem.schema.field_path.path_sequence import _read_compact_field_paths

        codes = _codes()
        finish = codes["FieldPathEncodeFinish"]
        sequences = [
            codes["PlusOne"] * 24 + finish,
            codes["PlusN"] + "0" * 12 + finish,
            codes["PushOneLeftDeltaNRightNonZeroPack6Bits"] + "001101" + finish,
            codes["PushOneLeftDeltaZeroRightZero"] * 7 + finish,
            codes["PopOnePlusOne"] + finish,
        ]
        for bits in sequences:
            for end in range(len(bits) + 1):
                candidate = _exact_reader(bits[:end], prefetched)
                original = _exact_reader(bits[:end], prefetched)
                assert _decode_outcome(
                    lambda candidate=candidate: _read_compact_field_paths(candidate)
                ) == (
                    _decode_outcome(
                        lambda original=original: _original_decode(original, original_table)
                    )
                )
                assert _reader_state(candidate) == _reader_state(original)

    @pytest.mark.parametrize("offset", range(8))
    @pytest.mark.parametrize("prefetched", [0, 17, 32])
    def test_consecutive_sequences_and_following_reads(self, original_table, offset, prefetched):
        from gem.binary.reader import BitReader
        from gem.schema.field_path.path_sequence import _read_compact_field_paths

        bits = "0" * offset + "010" + "0010" + "10100111" * 8
        readers = [BitReader(_bits_to_bytes(bits)) for _ in range(2)]
        for r in readers:
            r.read_bits(offset)
            if prefetched:
                r.peek_bits(prefetched)
        candidate, original = readers
        for _ in range(2):
            assert _read_compact_field_paths(candidate) == _original_decode(
                original, original_table
            )
            assert _reader_state(candidate) == _reader_state(original)
        assert candidate.read_bits(3) == original.read_bits(3)
        assert candidate.peek_bits(7) == original.peek_bits(7)
        candidate.skip_bits(7)
        original.skip_bits(7)
        assert candidate.read_bytes(3) == original.read_bytes(3)
        assert _reader_state(candidate) == _reader_state(original)
