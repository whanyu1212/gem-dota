"""Tests for gem.field_state — FieldState nested tree.

Reference: manta/field_state.go
"""

import pytest

from gem.field_path import FieldPath
from gem.field_state import FieldState

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_fp(*indices: int) -> FieldPath:
    """Build a FieldPath with the given index sequence."""
    fp = FieldPath()
    for i, v in enumerate(indices):
        fp.path[i] = v
    fp.last = len(indices) - 1
    return fp


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestFieldStateInit:
    def test_initial_state_is_list_of_nones(self):
        fs = FieldState()
        assert fs._state == [None] * 8

    def test_initial_length_is_8(self):
        fs = FieldState()
        assert len(fs._state) == 8


# ---------------------------------------------------------------------------
# _ensure growth
# ---------------------------------------------------------------------------


class TestFieldStateEnsure:
    def test_no_growth_when_already_large_enough(self):
        fs = FieldState()
        original_len = len(fs._state)
        fs._ensure(5)  # needs idx+2 = 7, already have 8
        assert len(fs._state) == original_len

    def test_grows_when_index_exceeds_capacity(self):
        fs = FieldState()
        fs._ensure(7)  # needs idx+2 = 9, currently 8
        assert len(fs._state) >= 9

    def test_growth_doubles_when_small(self):
        fs = FieldState()
        # Ensure idx=7 → needs 9, doubles from 8 → 16
        fs._ensure(7)
        assert len(fs._state) == 16

    def test_growth_jumps_to_idx_plus_2_when_large_index(self):
        fs = FieldState()
        # Ensure idx=100 → needs 102; doubling 8→16→32→…→128 would be overkill,
        # max(102, 16) = 102 … actually max(idx+2, len*2)=max(102,16)=102
        fs._ensure(100)
        assert len(fs._state) >= 102

    def test_new_slots_are_none(self):
        fs = FieldState()
        fs._ensure(10)
        for v in fs._state:
            assert v is None


# ---------------------------------------------------------------------------
# get — depth 0 (single index)
# ---------------------------------------------------------------------------


class TestFieldStateGetDepth0:
    def test_get_returns_none_on_empty(self):
        fs = FieldState()
        fp = _make_fp(0)
        assert fs.get(fp) is None

    def test_get_returns_none_for_large_index(self):
        fs = FieldState()
        fp = _make_fp(100)
        assert fs.get(fp) is None

    def test_get_returns_set_value(self):
        fs = FieldState()
        fp = _make_fp(3)
        fs._state[3] = 42
        assert fs.get(fp) == 42

    def test_get_returns_various_types(self):
        fs = FieldState()
        for idx, val in [(0, 1.5), (1, "hello"), (2, True), (3, b"\xff")]:
            fs._state[idx] = val
            fp = _make_fp(idx)
            assert fs.get(fp) == val


# ---------------------------------------------------------------------------
# get — depth 1 (two indices)
# ---------------------------------------------------------------------------


class TestFieldStateGetDepth1:
    def test_get_returns_none_when_no_child(self):
        fs = FieldState()
        fp = _make_fp(0, 1)
        assert fs.get(fp) is None

    def test_get_returns_none_when_slot_is_leaf_not_child(self):
        fs = FieldState()
        fs._state[0] = 99  # leaf, not a FieldState
        fp = _make_fp(0, 1)
        assert fs.get(fp) is None

    def test_get_returns_nested_value(self):
        fs = FieldState()
        child = FieldState()
        child._state[2] = "nested"
        fs._state[0] = child
        fp = _make_fp(0, 2)
        assert fs.get(fp) == "nested"

    def test_get_returns_none_when_child_index_out_of_range(self):
        fs = FieldState()
        child = FieldState()
        fs._state[0] = child
        fp = _make_fp(0, 100)
        assert fs.get(fp) is None


# ---------------------------------------------------------------------------
# get — depth 2 (three indices)
# ---------------------------------------------------------------------------


class TestFieldStateGetDepth2:
    def test_get_three_levels_deep(self):
        fs = FieldState()
        child = FieldState()
        grandchild = FieldState()
        grandchild._state[5] = 777
        child._state[1] = grandchild
        fs._state[0] = child
        fp = _make_fp(0, 1, 5)
        assert fs.get(fp) == 777

    def test_get_returns_none_when_intermediate_missing(self):
        fs = FieldState()
        child = FieldState()
        fs._state[0] = child
        # child has no grandchild at [1]
        fp = _make_fp(0, 1, 5)
        assert fs.get(fp) is None


# ---------------------------------------------------------------------------
# set — depth 0
# ---------------------------------------------------------------------------


class TestFieldStateSetDepth0:
    def test_set_stores_integer(self):
        fs = FieldState()
        fp = _make_fp(0)
        fs.set(fp, 42)
        assert fs._state[0] == 42

    def test_set_stores_float(self):
        fs = FieldState()
        fp = _make_fp(1)
        fs.set(fp, 3.14)
        assert fs._state[1] == pytest.approx(3.14)

    def test_set_stores_string(self):
        fs = FieldState()
        fp = _make_fp(2)
        fs.set(fp, "hero")
        assert fs._state[2] == "hero"

    def test_set_overwrites_existing_leaf(self):
        fs = FieldState()
        fp = _make_fp(0)
        fs.set(fp, 1)
        fs.set(fp, 2)
        assert fs._state[0] == 2

    def test_set_does_not_overwrite_fieldstate_child(self):
        """set() must not clobber an existing FieldState node with a leaf value."""
        fs = FieldState()
        child = FieldState()
        child._state[0] = "existing"
        fs._state[0] = child
        fp = _make_fp(0)
        fs.set(fp, "overwrite_attempt")
        # child must still be there
        assert isinstance(fs._state[0], FieldState)

    def test_set_grows_list_for_large_index(self):
        fs = FieldState()
        fp = _make_fp(20)
        fs.set(fp, 99)
        assert fs._state[20] == 99

    def test_set_index_0(self):
        fs = FieldState()
        fp = _make_fp(0)
        fs.set(fp, "zero")
        assert fs.get(fp) == "zero"

    def test_set_then_get_roundtrip(self):
        fs = FieldState()
        fp = _make_fp(7)
        fs.set(fp, 123)
        assert fs.get(fp) == 123


# ---------------------------------------------------------------------------
# set — depth 1
# ---------------------------------------------------------------------------


class TestFieldStateSetDepth1:
    def test_set_creates_child_fieldstate(self):
        fs = FieldState()
        fp = _make_fp(0, 3)
        fs.set(fp, "leaf")
        assert isinstance(fs._state[0], FieldState)
        assert fs._state[0]._state[3] == "leaf"

    def test_set_reuses_existing_child(self):
        fs = FieldState()
        child = FieldState()
        child._state[1] = "existing"
        fs._state[0] = child
        fp = _make_fp(0, 2)
        fs.set(fp, "new")
        # same child object
        assert fs._state[0] is child
        assert child._state[2] == "new"
        assert child._state[1] == "existing"  # untouched

    def test_set_depth1_roundtrip(self):
        fs = FieldState()
        fp = _make_fp(2, 5)
        fs.set(fp, 999)
        assert fs.get(fp) == 999


# ---------------------------------------------------------------------------
# set — depth 2
# ---------------------------------------------------------------------------


class TestFieldStateSetDepth2:
    def test_set_creates_two_levels_of_children(self):
        fs = FieldState()
        fp = _make_fp(0, 1, 2)
        fs.set(fp, "deep")
        child = fs._state[0]
        assert isinstance(child, FieldState)
        grandchild = child._state[1]
        assert isinstance(grandchild, FieldState)
        assert grandchild._state[2] == "deep"

    def test_set_depth2_roundtrip(self):
        fs = FieldState()
        fp = _make_fp(1, 2, 3)
        fs.set(fp, 3.14)
        assert fs.get(fp) == pytest.approx(3.14)


# ---------------------------------------------------------------------------
# Multiple paths on the same FieldState
# ---------------------------------------------------------------------------


class TestFieldStateMultiplePaths:
    def test_two_sibling_depth0_paths(self):
        fs = FieldState()
        fs.set(_make_fp(0), 10)
        fs.set(_make_fp(1), 20)
        assert fs.get(_make_fp(0)) == 10
        assert fs.get(_make_fp(1)) == 20

    def test_two_depth1_paths_same_parent(self):
        fs = FieldState()
        fs.set(_make_fp(0, 0), "a")
        fs.set(_make_fp(0, 1), "b")
        assert fs.get(_make_fp(0, 0)) == "a"
        assert fs.get(_make_fp(0, 1)) == "b"

    def test_two_depth1_paths_different_parents(self):
        fs = FieldState()
        fs.set(_make_fp(0, 0), "x")
        fs.set(_make_fp(1, 0), "y")
        assert fs.get(_make_fp(0, 0)) == "x"
        assert fs.get(_make_fp(1, 0)) == "y"

    def test_shallow_and_deep_paths_independent(self):
        fs = FieldState()
        fp_shallow = _make_fp(0)
        fp_deep = _make_fp(1, 2, 3)
        fs.set(fp_shallow, "shallow")
        fs.set(fp_deep, "deep")
        assert fs.get(fp_shallow) == "shallow"
        assert fs.get(fp_deep) == "deep"

    def test_overwrite_leaf_at_depth1(self):
        fs = FieldState()
        fp = _make_fp(0, 5)
        fs.set(fp, "first")
        fs.set(fp, "second")
        assert fs.get(fp) == "second"

    def test_many_indices_in_sequence(self):
        """Simulate a realistic flurry of field writes at depth-0 and depth-1."""
        fs = FieldState()
        entries = [(i, i * 3) for i in range(30)]
        for idx, val in entries:
            fs.set(_make_fp(idx), val)
        for idx, val in entries:
            assert fs.get(_make_fp(idx)) == val


# ---------------------------------------------------------------------------
# FieldPath with last=0 but path[0]=0 (boundary)
# ---------------------------------------------------------------------------


class TestFieldStateBoundary:
    def test_path_index_exactly_at_list_boundary(self):
        """Index == len(state) - 2 is still readable without growing."""
        fs = FieldState()
        # Default list is 8 long; index 6 → needs 8 entries → OK
        fs._state[6] = "edge"
        fp = _make_fp(6)
        assert fs.get(fp) == "edge"

    def test_path_index_at_last_slot(self):
        """Index == len(state) - 1 requires growth (needs idx+2 = len+1)."""
        fs = FieldState()
        # index=7, len=8 → needs 9 → _ensure grows; but get() checks before set()
        fp = _make_fp(7)
        assert fs.get(fp) is None  # no growth in get(), returns None

    def test_set_then_get_at_last_slot(self):
        """set() grows on demand; get() must then find the value."""
        fs = FieldState()
        fp = _make_fp(7)
        fs.set(fp, "boundary")
        assert fs.get(fp) == "boundary"

    def test_none_is_valid_stored_value_at_depth0(self):
        """set() stores None as a leaf; get() returns None — same result as empty.
        This is correct: None is a valid decoded value (e.g., unset optional field).
        """
        fs = FieldState()
        fp = _make_fp(0)
        fs.set(fp, None)
        # The slot is now explicitly None — indistinguishable from empty at this API level
        assert fs.get(fp) is None


# ---------------------------------------------------------------------------
# Isolation between FieldState instances
# ---------------------------------------------------------------------------


class TestFieldStateIsolation:
    def test_two_instances_are_independent(self):
        fs1 = FieldState()
        fs2 = FieldState()
        fs1.set(_make_fp(0), "fs1")
        fs2.set(_make_fp(0), "fs2")
        assert fs1.get(_make_fp(0)) == "fs1"
        assert fs2.get(_make_fp(0)) == "fs2"

    def test_child_fieldstate_not_shared_between_parents(self):
        fs1 = FieldState()
        fs2 = FieldState()
        fs1.set(_make_fp(0, 0), "in_fs1")
        # fs2 has no children, so fp(0,0) should return None
        assert fs2.get(_make_fp(0, 0)) is None
