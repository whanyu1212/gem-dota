"""
Tests for gem.field_path — Huffman field path decoding.

Reference: manta/field_path.go, manta/huffman.go
"""

from typing import Any

import pytest


@pytest.fixture
def read_field_paths():
    from gem.field_path import read_field_paths

    return read_field_paths


@pytest.fixture
def reader_cls():
    from gem.reader import BitReader

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
        from gem.field_path import HUFF_TREE

        assert HUFF_TREE is not None

    def test_finish_op_is_most_common(self):
        """FieldPathEncodeFinish has weight 25474 — highest weight, so should be shallow in tree."""
        from gem.field_path import FIELD_PATH_OPS

        finish_op = next(op for op in FIELD_PATH_OPS if op.name == "FieldPathEncodeFinish")
        assert finish_op.weight == 25474

    def test_40_ops_defined(self):
        from gem.field_path import FIELD_PATH_OPS

        assert len(FIELD_PATH_OPS) == 40


class TestFieldPath:
    def test_plus_one_increments_last(self):
        from gem.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 5
        fp.plus_one()
        assert fp.path[0] == 6

    def test_pop_reduces_depth(self):
        from gem.field_path import FieldPath

        fp = FieldPath()
        fp.last = 2
        fp.path[1] = 3
        fp.path[2] = 7
        fp.pop(1)
        assert fp.last == 1
        assert fp.path[2] == 0  # zeroed

    def test_pop_all_but_one(self):
        from gem.field_path import FieldPath

        fp = FieldPath()
        fp.last = 3
        fp.pop(3)
        assert fp.last == 0

    def test_copy_is_independent(self):
        from gem.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 10
        fp2 = fp.copy()
        fp2.path[0] = 99
        assert fp.path[0] == 10

    def test_string_representation(self):
        from gem.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 3
        fp.last = 0
        assert fp.to_str() == "3"

    def test_string_multi_level(self):
        from gem.field_path import FieldPath

        fp = FieldPath()
        fp.path[0] = 1
        fp.path[1] = 2
        fp.last = 1
        assert fp.to_str() == "1/2"


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

    def test_empty_result_on_immediate_finish(self, read_field_paths, reader_cls):
        """If the first op decoded is FinishEncoding, result should be empty.

        FieldPathEncodeFinish = bits 1,0 (LSB-first).
        """
        data = _bits_to_bytes("10")
        r = reader_cls(data)
        result = read_field_paths(r)
        assert result == []


def _read_field_paths_tree_walk(r):
    """Reference implementation: original bit-at-a-time Huffman tree walk."""
    from gem.field_path import FIELD_PATH_OPS, HUFF_TREE, FieldPath

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

        import gem.entities as entities_mod

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
        try:
            from gem.field_path import _HUFF_DECODE_TABLE, _HUFF_TABLE_BITS
        except ImportError:
            pytest.skip("decode table not yet implemented")
        from gem.field_path import FIELD_PATH_OPS, HUFF_TREE, FieldPath

        mismatches = 0
        total = 0

        for buf, pos, bit_val, bit_count in captured_buffers:
            # Restore identical reader state for both implementations
            def make_reader(
                _buf: bytes = buf,
                _pos: int = pos,
                _bit_val: int = bit_val,
                _bit_count: int = bit_count,
            ) -> Any:
                r = reader_cls(_buf)
                r._pos = _pos
                r._bit_val = _bit_val
                r._bit_count = _bit_count
                return r

            # Tree-walk reference
            ref_paths = _read_field_paths_tree_walk(make_reader())

            # Table-based candidate
            r_new = make_reader()
            fp = FieldPath()
            new_paths = []
            table = _HUFF_DECODE_TABLE
            table_bits = _HUFF_TABLE_BITS
            ops = FIELD_PATH_OPS
            while not fp.done:
                if r_new.rem_bits() >= table_bits:
                    bits = r_new.peek_bits(table_bits)
                    op_idx, consumed = table[bits]
                    r_new.skip_bits(consumed)
                else:
                    node = HUFF_TREE
                    while not node.is_leaf:
                        node = node.right if r_new.read_bits(1) else node.left
                    op_idx = node.value
                ops[op_idx].fn(r_new, fp)
                if not fp.done:
                    new_paths.append(fp.copy())

            ref_tuples = [p.to_tuple() for p in ref_paths]
            new_tuples = [p.to_tuple() for p in new_paths]

            total += 1
            if ref_tuples != new_tuples:
                mismatches += 1
                if mismatches <= 3:
                    pytest.fail(
                        f"Mismatch on snapshot #{total}:\n"
                        f"  ref[:{min(5, len(ref_tuples))}] = {ref_tuples[:5]}\n"
                        f"  new[:{min(5, len(new_tuples))}] = {new_tuples[:5]}\n"
                        f"  ref_len={len(ref_tuples)} new_len={len(new_tuples)}"
                    )

        assert mismatches == 0, f"{mismatches}/{total} snapshots had mismatches"
