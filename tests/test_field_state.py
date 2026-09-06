"""Tests for gem.schema.field_state — FieldState nested tree.

Reference: manta/field_state.go
"""

import pytest

from gem.schema.field_path import FieldPath
from gem.schema.field_path.models import CompactFieldPath
from gem.schema.field_state import FieldState, FieldValue

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


def _state_tree(state: FieldState):
    """Return nested list contents without comparing node identities."""
    return [
        _state_tree(value) if isinstance(value, FieldState) else value for value in state._state
    ]


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
# Hot-path traversal invariants
# ---------------------------------------------------------------------------


class TestFieldStateTraversal:
    def test_get_and_set_do_not_dispatch_through_helpers(self, monkeypatch):
        def fail(*_args):
            pytest.fail("hot traversal dispatched through a helper")

        monkeypatch.setattr(FieldState, "_has_slot", fail)
        monkeypatch.setattr(FieldState, "_ensure", fail)
        monkeypatch.setattr(FieldState, "_is_child", staticmethod(fail))

        fs = FieldState()
        fp = _make_fp(7, 100)
        fs.set(fp, "value")
        assert fs.get(fp) == "value"

    def test_sparse_nested_write_uses_exact_growth_rule(self):
        fs = FieldState()
        fs.set(_make_fp(7, 100), "value")

        assert len(fs._state) == 16
        child = fs._state[7]
        assert isinstance(child, FieldState)
        assert len(child._state) == 102
        assert child._state[100] == "value"

    def test_missing_nested_read_does_not_mutate_state(self):
        fs = FieldState()
        child = FieldState()
        child._state[0] = "existing"
        fs._state[0] = child
        root_before = list(fs._state)
        child_before = list(child._state)

        assert fs.get(_make_fp(0, 100)) is None
        assert fs._state == root_before
        assert child._state == child_before

    def test_deeper_write_replaces_intermediate_leaf_with_child(self):
        fs = FieldState()
        fs._state[0] = "leaf"

        fs.set(_make_fp(0, 1), "nested")

        assert isinstance(fs._state[0], FieldState)
        assert fs.get(_make_fp(0, 1)) == "nested"

    def test_leaf_write_preserves_subclass_child(self):
        class DerivedFieldState(FieldState):
            pass

        fs = FieldState()
        child = DerivedFieldState()
        child._state[0] = "existing"
        fs._state[0] = child

        fs.set(_make_fp(0), "replacement")

        assert fs._state[0] is child
        assert fs.get(_make_fp(0, 0)) == "existing"

    def test_maximum_depth_roundtrip(self):
        fs = FieldState()
        fp = _make_fp(0, 1, 2, 3, 4, 5, 6)

        fs.set(fp, "deep")

        assert fs.get(fp) == "deep"


# ---------------------------------------------------------------------------
# compact-path traversal
# ---------------------------------------------------------------------------


class TestFieldStateCompactTraversal:
    @pytest.mark.parametrize(
        "path",
        [(0,), (7,), (7, 100), (0, 1, 2, 3, 4, 5, 6)],
    )
    def test_roundtrip_matches_mutable_path(self, path):
        compact_state = FieldState()
        mutable_state = FieldState()

        compact_state._set_compact(path, "value")
        mutable_state.set(_make_fp(*path), "value")

        assert _state_tree(compact_state) == _state_tree(mutable_state)
        assert compact_state._get_compact(path) == "value"

    def test_write_sequence_preserves_tree_semantics(self):
        compact_state = FieldState()
        mutable_state = FieldState()
        writes = [((0,), "leaf"), ((0, 2), "nested"), ((0,), "ignored"), ((1,), None)]

        for path, value in writes:
            compact_state._set_compact(path, value)
            mutable_state.set(_make_fp(*path), value)

        assert _state_tree(compact_state) == _state_tree(mutable_state)
        assert compact_state._get_compact((0, 2)) == "nested"
        assert compact_state._get_compact((0,)) is compact_state._state[0]
        assert compact_state._get_compact((1,)) is None

    def test_missing_read_does_not_mutate_state(self):
        state = FieldState()
        state._set_compact((0, 1), "existing")
        root_before = list(state._state)
        child = state._state[0]
        assert isinstance(child, FieldState)
        child_before = list(child._state)

        assert state._get_compact((0, 100)) is None
        assert state._state == root_before
        assert child._state == child_before

    def test_empty_compact_path_is_a_noop(self):
        state = FieldState()
        before = list(state._state)

        state._set_compact((), "ignored")

        assert state._get_compact(()) is None
        assert state._state == before

    def test_compact_traversal_bypasses_public_methods(self, monkeypatch):
        def fail(*_args):
            pytest.fail("compact traversal dispatched through a public method")

        monkeypatch.setattr(FieldState, "get", fail)
        monkeypatch.setattr(FieldState, "set", fail)
        state = FieldState()

        state._set_compact((2, 3), "value")

        assert state._get_compact((2, 3)) == "value"


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
    def test_empty_active_path_returns_none(self):
        """An empty active FieldPath is defensive-only and stores no value."""
        fs = FieldState()
        fp = _make_fp()
        assert fp.last == -1
        assert fs.get(fp) is None

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


class _OriginalFieldState(FieldState):
    def _get_compact(self, path: CompactFieldPath) -> FieldValue:
        """Read an internal compact path without materializing a FieldPath."""
        state = self._state
        last = len(path) - 1
        for i, idx in enumerate(path):
            if len(state) < idx + 2:
                return None
            if i == last:
                return state[idx]
            child = state[idx]
            if not isinstance(child, FieldState):
                return None
            state = child._state
        return None

    def _set_compact(self, path: CompactFieldPath, value: FieldValue) -> None:
        """Write an internal compact path without materializing a FieldPath."""
        state = self._state
        last = len(path) - 1
        for i, idx in enumerate(path):
            current_len = len(state)
            if current_len < idx + 2:
                new_len = max(idx + 2, current_len * 2)
                state.extend([None] * (new_len - current_len))

            current = state[idx]
            if i == last:
                if not isinstance(current, FieldState):
                    state[idx] = value
                return
            if not isinstance(current, FieldState):
                current = FieldState()
                state[idx] = current
            state = current._state


def _outcome(call):
    try:
        return call()
    except (IndexError, TypeError) as exc:
        return type(exc), str(exc)


class TestShallowCompactEquivalence:
    @pytest.mark.parametrize("depth", range(1, 8))
    def test_operations_match_original_and_public(self, depth):
        states = [FieldState(), _OriginalFieldState(), FieldState()]
        value = object()
        for index in (0, 6, 7, 8, 15, 16, 100):
            path = (index,) * depth
            for i, state in enumerate(states):
                read = (
                    (lambda state=state, path=path: state.get(_make_fp(*path)))
                    if i == 2
                    else (lambda state=state, path=path: state._get_compact(path))
                )
                assert read() is None
                if i == 2:
                    state.set(_make_fp(*path), value)
                else:
                    state._set_compact(path, value)
                assert read() is value
            assert _state_tree(states[0]) == _state_tree(states[1]) == _state_tree(states[2])

    @pytest.mark.parametrize(
        "path",
        [
            (),
            (-1,),
            (-8,),
            (-9,),
            (True,),
            (False, True),
            (7, -9),
            (0, -1),
            (0, -8),
            (0, -9),
            (-9, 0),
            (1.5,),
            ("x",),
            (7, 1.5),
            (7, "x"),
        ],
    )
    def test_index_behavior_and_partial_failure(self, path):
        candidate, original, public = FieldState(), _OriginalFieldState(), FieldState()
        assert (
            _outcome(lambda: candidate._get_compact(path))
            == _outcome(lambda: original._get_compact(path))
            == _outcome(lambda: public.get(_make_fp(*path)))
        )
        assert (
            _outcome(lambda: candidate._set_compact(path, 42))
            == _outcome(lambda: original._set_compact(path, 42))
            == _outcome(lambda: public.set(_make_fp(*path), 42))
        )
        assert _state_tree(candidate) == _state_tree(original) == _state_tree(public)

    @pytest.mark.parametrize("depth", [1, 2])
    def test_extra_slot_bound_does_not_read_populated_last_slot(self, depth):
        state = FieldState()
        leaf = state
        if depth == 2:
            leaf = FieldState()
            state._state[0] = leaf
        leaf._state[7] = object()
        before = _state_tree(state)
        assert state._get_compact((0,) * (depth - 1) + (7,)) is None
        assert _state_tree(state) == before

    def test_aliases_children_and_mixed_depth_writes(self):
        class Child(FieldState):
            pass

        state = FieldState()
        root_storage = state._state
        child = Child()
        child_storage = child._state
        state._state[7] = child
        value = object()
        state._set_compact((7, 100), value)
        assert state._state is root_storage and len(root_storage) == 16
        assert state._state[7] is child and child._state is child_storage
        assert len(child_storage) == 102 and state._get_compact((7, 100)) is value
        for replacement in (None, 0, object(), FieldState()):
            state._set_compact((7,), replacement)
            assert state._get_compact((7,)) is child
        state._set_compact((7, 100, 0), value)
        terminal = state._get_compact((7, 100))
        for replacement in (None, 0, object(), FieldState()):
            state._set_compact((7, 100), replacement)
            assert state._get_compact((7, 100)) is terminal
        assert state._get_compact((7, 100, 0)) is value

    def test_compact_paths_bypass_helpers(self, monkeypatch):
        def fail(*args):
            pytest.fail("compact path dispatched through a helper")

        for name in ("get", "set", "_ensure", "_has_slot", "_is_child"):
            monkeypatch.setattr(FieldState, name, fail)
        state = FieldState()
        for path in ((100,), (100, 100), (100, 100, 100)):
            state._set_compact(path, 42)
            assert state._get_compact(path) == 42
