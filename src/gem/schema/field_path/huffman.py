"""Huffman tree and flat decode table for field-path operations."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from gem.schema.field_path.operations import FIELD_PATH_OPS


@dataclass(order=True)
class _HNode:
    """Internal min-heap node for Huffman tree construction."""

    weight: int
    value: int
    left: _HNode | None = field(default=None, compare=False)
    right: _HNode | None = field(default=None, compare=False)

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def _build_huffman_tree(weights: list[int]) -> _HNode:
    """Build a Huffman tree from a list of symbol weights.

    Symbols with weight 0 are treated as weight 1 (must appear in tree).
    Tie-breaking: higher value wins (matches manta's Go implementation).

    Args:
        weights: Per-symbol frequency weights, indexed by symbol value.

    Returns:
        Root _HNode of the completed Huffman tree.
    """
    heap: list[tuple[int, int, _HNode]] = []
    for v, w in enumerate(weights):
        w = w or 1
        heapq.heappush(heap, (w, -v, _HNode(w, v)))

    counter = len(weights)
    while len(heap) > 1:
        wa, _, a = heapq.heappop(heap)
        wb, _, b = heapq.heappop(heap)
        merged = _HNode(wa + wb, counter, left=a, right=b)
        heapq.heappush(heap, (merged.weight, -counter, merged))
        counter += 1

    return heap[0][2]


def _build_decode_table(root: _HNode, table_bits: int) -> list[tuple[int, int]]:
    """Build a flat O(1) decode table from the Huffman tree.

    Each entry ``table[i] = (op_index, bits_consumed)`` covers all ``table_bits``-
    bit integers whose leading bits match the Huffman code for ``op_index``.
    Shorter codes fill multiple entries (one per possible suffix).

    Args:
        root: Root of the Huffman tree.
        table_bits: Width of the table in bits (``2**table_bits`` entries).

    Returns:
        List of ``(op_index, bits_consumed)`` tuples, indexed by the
        ``table_bits``-bit integer peeked from the bit stream.
    """
    size = 1 << table_bits
    table: list[tuple[int, int]] = [(0, 0)] * size

    stack: list[tuple[_HNode, int, int]] = [(root, 0, 0)]  # node, code, depth
    while stack:
        node, code, depth = stack.pop()
        if node.is_leaf:
            suffix_count = 1 << (table_bits - depth)
            for s in range(suffix_count):
                table[code | (s << depth)] = (node.value, depth)
        else:
            if node.left is not None:
                stack.append((node.left, code, depth + 1))
            if node.right is not None:
                stack.append((node.right, code | (1 << depth), depth + 1))

    return table


def _tree_depth(node: _HNode) -> int:
    """Return the maximum depth of the Huffman tree.

    Args:
        node: Root node.

    Returns:
        int: Maximum leaf depth (root = depth 0).
    """
    if node.is_leaf:
        return 0
    left_d = _tree_depth(node.left) + 1 if node.left else 0
    right_d = _tree_depth(node.right) + 1 if node.right else 0
    return max(left_d, right_d)


HUFF_TREE: _HNode = _build_huffman_tree([op.weight for op in FIELD_PATH_OPS])
_HUFF_TABLE_BITS: int = _tree_depth(HUFF_TREE)
_HUFF_DECODE_TABLE: list[tuple[int, int]] = _build_decode_table(HUFF_TREE, _HUFF_TABLE_BITS)
