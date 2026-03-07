"""Huffman-coded field path decoder for Dota 2 Source 2 entity delta streams.

Field paths describe which fields of an entity have changed.  Each path is a
list of up to 7 integer indices (one per nesting level) that navigate from
a serializer root to a leaf field.  The sequence of paths in a packet is
Huffman-encoded using the operation weights defined below.

Reference: manta/field_path.go, manta/huffman.go
"""

from __future__ import annotations

import heapq
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.reader import BitReader

# ---------------------------------------------------------------------------
# FieldPath
# ---------------------------------------------------------------------------

_RESET = [-1, 0, 0, 0, 0, 0, 0]


class FieldPath:
    """A mutable path of up to 7 integer field indices.

    Starts at ``path = [-1, 0, 0, 0, 0, 0, 0]``, ``last = 0``.
    Operations mutate ``path`` and ``last`` in place.

    Attributes:
        path: Seven-element list; active indices are ``path[0:last+1]``.
        last: Index of the deepest active level (0-based).
        done: Set to True by ``FieldPathEncodeFinish`` to stop iteration.
    """

    __slots__ = ("path", "last", "done")

    def __init__(self) -> None:
        self.path: list[int] = [-1, 0, 0, 0, 0, 0, 0]
        self.last: int = 0
        self.done: bool = False

    def reset(self) -> None:
        """Reset to the initial empty state."""
        self.path[:] = _RESET
        self.last = 0
        self.done = False

    def pop(self, n: int) -> None:
        """Pop n levels off the path, zeroing the vacated slots.

        Args:
            n: Number of levels to remove.
        """
        for _ in range(n):
            self.path[self.last] = 0
            self.last -= 1

    def copy(self) -> FieldPath:
        """Return an independent copy of this path.

        Returns:
            A new FieldPath with identical state.
        """
        fp = FieldPath()
        fp.path[:] = self.path
        fp.last = self.last
        fp.done = self.done
        return fp

    def to_tuple(self) -> tuple[int, ...]:
        """Return the active indices as an immutable tuple.

        Returns:
            Tuple of active integer indices, e.g. ``(2, 0, 5)``.
        """
        return tuple(self.path[: self.last + 1])

    def to_str(self) -> str:
        """Return a slash-separated string of active indices.

        Returns:
            String like ``"2/0/5"``.
        """
        return "/".join(str(self.path[i]) for i in range(self.last + 1))

    def plus_one(self) -> None:
        """Increment the deepest index by 1."""
        self.path[self.last] += 1


# ---------------------------------------------------------------------------
# Huffman tree
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Field path operation table (40 ops, weights match manta exactly)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldPathOp:
    """A single field-path operation with its Huffman weight.

    Attributes:
        name: Human-readable operation name.
        weight: Huffman frequency weight (higher = shallower in tree).
        fn: Callable that mutates a FieldPath using bits from a BitReader.
    """

    name: str
    weight: int
    fn: Callable[[BitReader, FieldPath], None]


def _make_ops() -> list[FieldPathOp]:
    def plus_one(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 1

    def plus_two(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 2

    def plus_three(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 3

    def plus_four(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 4

    def plus_n(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_ubit_var_fp() + 5

    def push1_l0_r0(r: BitReader, fp: FieldPath) -> None:
        fp.last += 1
        fp.path[fp.last] = 0

    def push1_l0_rn(r: BitReader, fp: FieldPath) -> None:
        fp.last += 1
        fp.path[fp.last] = r.read_ubit_var_fp()

    def push1_l1_r0(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 1
        fp.last += 1
        fp.path[fp.last] = 0

    def push1_l1_rn(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 1
        fp.last += 1
        fp.path[fp.last] = r.read_ubit_var_fp()

    def push1_ln_r0(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] = 0

    def push1_ln_rn(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_ubit_var_fp() + 2
        fp.last += 1
        fp.path[fp.last] = r.read_ubit_var_fp() + 1

    def push1_ln_rn_pack6(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_bits(3) + 2
        fp.last += 1
        fp.path[fp.last] = r.read_bits(3) + 1

    def push1_ln_rn_pack8(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_bits(4) + 2
        fp.last += 1
        fp.path[fp.last] = r.read_bits(4) + 1

    def push2_l0(r: BitReader, fp: FieldPath) -> None:
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()

    def push2_pack5_l0(r: BitReader, fp: FieldPath) -> None:
        fp.last += 1
        fp.path[fp.last] = r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] = r.read_bits(5)

    def push3_l0(r: BitReader, fp: FieldPath) -> None:
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()

    def push3_pack5_l0(r: BitReader, fp: FieldPath) -> None:
        fp.last += 1
        fp.path[fp.last] = r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] = r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] = r.read_bits(5)

    def push2_l1(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 1
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()

    def push2_pack5_l1(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 1
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)

    def push3_l1(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 1
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()

    def push3_pack5_l1(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += 1
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)

    def push2_ln(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_ubit_var() + 2
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()

    def push2_pack5_ln(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_ubit_var() + 2
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)

    def push3_ln(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_ubit_var() + 2
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()
        fp.last += 1
        fp.path[fp.last] += r.read_ubit_var_fp()

    def push3_pack5_ln(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last] += r.read_ubit_var() + 2
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)
        fp.last += 1
        fp.path[fp.last] += r.read_bits(5)

    def push_n(r: BitReader, fp: FieldPath) -> None:
        n = r.read_ubit_var()
        fp.path[fp.last] += r.read_ubit_var()
        for _ in range(n):
            fp.last += 1
            fp.path[fp.last] += r.read_ubit_var_fp()

    def push_n_non_topo(r: BitReader, fp: FieldPath) -> None:
        for i in range(fp.last + 1):
            if r.read_boolean():
                fp.path[i] += r.read_varint32() + 1
        count = r.read_ubit_var()
        for _ in range(count):
            fp.last += 1
            fp.path[fp.last] = r.read_ubit_var_fp()

    def pop1_plus1(r: BitReader, fp: FieldPath) -> None:
        fp.pop(1)
        fp.path[fp.last] += 1

    def pop1_plus_n(r: BitReader, fp: FieldPath) -> None:
        fp.pop(1)
        fp.path[fp.last] += r.read_ubit_var_fp() + 1

    def pop_all_but1_plus1(r: BitReader, fp: FieldPath) -> None:
        fp.pop(fp.last)
        fp.path[0] += 1

    def pop_all_but1_plus_n(r: BitReader, fp: FieldPath) -> None:
        fp.pop(fp.last)
        fp.path[0] += r.read_ubit_var_fp() + 1

    def pop_all_but1_plus_n_pack3(r: BitReader, fp: FieldPath) -> None:
        fp.pop(fp.last)
        fp.path[0] += r.read_bits(3) + 1

    def pop_all_but1_plus_n_pack6(r: BitReader, fp: FieldPath) -> None:
        fp.pop(fp.last)
        fp.path[0] += r.read_bits(6) + 1

    def pop_n_plus1(r: BitReader, fp: FieldPath) -> None:
        fp.pop(r.read_ubit_var_fp())
        fp.path[fp.last] += 1

    def pop_n_plus_n(r: BitReader, fp: FieldPath) -> None:
        fp.pop(r.read_ubit_var_fp())
        fp.path[fp.last] += r.read_varint32()

    def pop_n_non_topo(r: BitReader, fp: FieldPath) -> None:
        fp.pop(r.read_ubit_var_fp())
        for i in range(fp.last + 1):
            if r.read_boolean():
                fp.path[i] += r.read_varint32()

    def non_topo_complex(r: BitReader, fp: FieldPath) -> None:
        for i in range(fp.last + 1):
            if r.read_boolean():
                fp.path[i] += r.read_varint32()

    def non_topo_penultimate_plus1(r: BitReader, fp: FieldPath) -> None:
        fp.path[fp.last - 1] += 1

    def non_topo_complex_pack4(r: BitReader, fp: FieldPath) -> None:
        for i in range(fp.last + 1):
            if r.read_boolean():
                fp.path[i] += r.read_bits(4) - 7

    def finish(r: BitReader, fp: FieldPath) -> None:
        fp.done = True

    return [
        FieldPathOp("PlusOne", 36271, plus_one),
        FieldPathOp("PlusTwo", 10334, plus_two),
        FieldPathOp("PlusThree", 1375, plus_three),
        FieldPathOp("PlusFour", 646, plus_four),
        FieldPathOp("PlusN", 4128, plus_n),
        FieldPathOp("PushOneLeftDeltaZeroRightZero", 35, push1_l0_r0),
        FieldPathOp("PushOneLeftDeltaZeroRightNonZero", 3, push1_l0_rn),
        FieldPathOp("PushOneLeftDeltaOneRightZero", 521, push1_l1_r0),
        FieldPathOp("PushOneLeftDeltaOneRightNonZero", 2942, push1_l1_rn),
        FieldPathOp("PushOneLeftDeltaNRightZero", 560, push1_ln_r0),
        FieldPathOp("PushOneLeftDeltaNRightNonZero", 471, push1_ln_rn),
        FieldPathOp("PushOneLeftDeltaNRightNonZeroPack6Bits", 10530, push1_ln_rn_pack6),
        FieldPathOp("PushOneLeftDeltaNRightNonZeroPack8Bits", 251, push1_ln_rn_pack8),
        FieldPathOp("PushTwoLeftDeltaZero", 0, push2_l0),
        FieldPathOp("PushTwoPack5LeftDeltaZero", 0, push2_pack5_l0),
        FieldPathOp("PushThreeLeftDeltaZero", 0, push3_l0),
        FieldPathOp("PushThreePack5LeftDeltaZero", 0, push3_pack5_l0),
        FieldPathOp("PushTwoLeftDeltaOne", 0, push2_l1),
        FieldPathOp("PushTwoPack5LeftDeltaOne", 0, push2_pack5_l1),
        FieldPathOp("PushThreeLeftDeltaOne", 0, push3_l1),
        FieldPathOp("PushThreePack5LeftDeltaOne", 0, push3_pack5_l1),
        FieldPathOp("PushTwoLeftDeltaN", 0, push2_ln),
        FieldPathOp("PushTwoPack5LeftDeltaN", 0, push2_pack5_ln),
        FieldPathOp("PushThreeLeftDeltaN", 0, push3_ln),
        FieldPathOp("PushThreePack5LeftDeltaN", 0, push3_pack5_ln),
        FieldPathOp("PushN", 0, push_n),
        FieldPathOp("PushNAndNonTopological", 310, push_n_non_topo),
        FieldPathOp("PopOnePlusOne", 2, pop1_plus1),
        FieldPathOp("PopOnePlusN", 0, pop1_plus_n),
        FieldPathOp("PopAllButOnePlusOne", 1837, pop_all_but1_plus1),
        FieldPathOp("PopAllButOnePlusN", 149, pop_all_but1_plus_n),
        FieldPathOp("PopAllButOnePlusNPack3Bits", 300, pop_all_but1_plus_n_pack3),
        FieldPathOp("PopAllButOnePlusNPack6Bits", 634, pop_all_but1_plus_n_pack6),
        FieldPathOp("PopNPlusOne", 0, pop_n_plus1),
        FieldPathOp("PopNPlusN", 0, pop_n_plus_n),
        FieldPathOp("PopNAndNonTopographical", 1, pop_n_non_topo),
        FieldPathOp("NonTopoComplex", 76, non_topo_complex),
        FieldPathOp("NonTopoPenultimatePlusOne", 271, non_topo_penultimate_plus1),
        FieldPathOp("NonTopoComplexPack4Bits", 99, non_topo_complex_pack4),
        FieldPathOp("FieldPathEncodeFinish", 25474, finish),
    ]


FIELD_PATH_OPS: list[FieldPathOp] = _make_ops()
HUFF_TREE: _HNode = _build_huffman_tree([op.weight for op in FIELD_PATH_OPS])


# ---------------------------------------------------------------------------
# Field path reading
# ---------------------------------------------------------------------------


def read_field_paths(r: BitReader) -> list[FieldPath]:
    """Decode a Huffman-coded sequence of field paths from r.

    Reads bits one at a time, traversing the Huffman tree until a leaf
    operation is reached.  Repeats until ``FieldPathEncodeFinish`` is decoded.

    Args:
        r: BitReader positioned at the start of the field path sequence.

    Returns:
        List of FieldPath objects, one per updated field (not including the
        finish sentinel).
    """
    fp = FieldPath()
    node = HUFF_TREE
    paths: list[FieldPath] = []

    while not fp.done:
        next_node = node.right if r.read_bits(1) else node.left
        assert next_node is not None
        node = next_node
        if node.is_leaf:
            FIELD_PATH_OPS[node.value].fn(r, fp)
            if not fp.done:
                paths.append(fp.copy())
            node = HUFF_TREE

    return paths
