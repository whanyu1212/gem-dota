"""Manta-compatible field-path operation table.

The operation order and weights must stay byte-for-byte compatible with
``refs/manta/field_path.go`` because Huffman symbol values are table indices.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.schema.field_path.model import FieldPath

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


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
