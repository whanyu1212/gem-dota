"""Huffman-coded field path decoder for Dota 2 Source 2 entity delta streams."""

from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from gem.schema.field_path.huffman import (
    _HUFF_DECODE_TABLE,
    _HUFF_TABLE_BITS,
    HUFF_TREE,
)
from gem.schema.field_path.models import CompactFieldPath, FieldPath
from gem.schema.field_path.operations import FIELD_PATH_OPS

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


def _read_compact_field_paths(r: BitReader) -> list[CompactFieldPath]:
    """Decode a Huffman-coded sequence into compact immutable paths.

    Uses a flat O(1) decode table to resolve each Huffman op in a single
    peek + skip rather than a per-bit tree walk. The peek/skip/rem_bits
    calls are inlined directly against BitReader's private attributes to
    eliminate millions of Python function calls per replay.

    Falls back to the tree walk for the last few bits when fewer than
    ``_HUFF_TABLE_BITS`` bits remain in the buffer.

    Args:
        r: BitReader positioned at the start of the field path sequence.

    Returns:
        Compact active-index tuples, one per updated field (not including the
        finish sentinel).
    """
    fp = FieldPath()
    paths: list[CompactFieldPath] = []
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


def read_field_paths(r: BitReader) -> list[FieldPath]:
    """Decode field paths into independent mutable compatibility objects.

    Production entity decoding consumes :func:`_read_compact_field_paths`
    directly.  This public wrapper preserves the established ``FieldPath``
    return type for schema callers and tests.

    Args:
        r: BitReader positioned at the start of the field path sequence.

    Returns:
        List of FieldPath objects, one per updated field (not including the
        finish sentinel).
    """
    return [FieldPath._from_tuple(path) for path in _read_compact_field_paths(r)]
