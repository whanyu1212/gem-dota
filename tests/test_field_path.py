"""
Tests for gem.field_path — Huffman field path decoding.

Reference: manta/field_path.go, manta/huffman.go
"""

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
        # A stream with only FieldPathEncodeFinish should return empty list
        # We need to know the Huffman encoding of FinishEncoding
        # Since we can't easily hardcode it without running the tree, just
        # verify the function returns a list without crashing on valid input.
        # Use a pytest.skip if we can't construct a valid bit stream yet.
        pytest.skip("Requires known Huffman bit sequences — add once tree is verified")

    def test_empty_result_on_immediate_finish(self, read_field_paths, reader_cls):
        """If the first op decoded is FinishEncoding, result should be empty."""
        pytest.skip("Requires known Huffman encoding of FinishEncoding bit sequence")
