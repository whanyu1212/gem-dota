"""Huffman-coded field path decoder for Dota 2 Source 2 entity delta streams."""

from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from gem.schema.field_path.huffman import (
    _HUFF_DECODE_TABLE,
    _HUFF_TABLE_BITS,
    HUFF_TREE,
)
from gem.schema.field_path.models import FieldPath
from gem.schema.field_path.operations import FIELD_PATH_OPS

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


def read_field_paths(r: BitReader) -> list[FieldPath]:
    """Decode a Huffman-coded sequence of field paths from r.

    Uses a flat O(1) decode table to resolve each Huffman op in a single
    peek + skip rather than a per-bit tree walk. The peek/skip/rem_bits
    calls are inlined directly against BitReader's private attributes to
    eliminate millions of Python function calls per replay.

    Falls back to the tree walk for the last few bits when fewer than
    ``_HUFF_TABLE_BITS`` bits remain in the buffer.

    Args:
        r: BitReader positioned at the start of the field path sequence.

    Returns:
        List of FieldPath objects, one per updated field (not including the
        finish sentinel).
    """
    fp = FieldPath()
    paths: list[FieldPath] = []
    ops = FIELD_PATH_OPS
    table = _HUFF_DECODE_TABLE
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
            paths.append(fp.copy())

    return paths
