"""Nested mutable field-value tree for entity state storage.

The tree layout and growth rule mirror ``manta/field_state.go``. Variable-length
arrays and tables additionally follow Clarity: a length write trims elements past
the new length, and reading the array's own path returns its length.

References:
    dotabuff/manta field_state.go (pinned revision in CLAUDE.md)
    skadistats/clarity VectorField.java, NestedArrayEntityState.java (pinned
    revision in CLAUDE.md)
"""

from __future__ import annotations

from typing import TypeAlias

from gem.schema.field_path import FieldPath
from gem.schema.field_path.models import CompactFieldPath

FieldValue: TypeAlias = object | None


class FieldState:
    """Nested mutable tree that stores decoded field values.

    The tree mirrors ``manta/field_state.go``: each node is a list of
    ``FieldValue`` objects, where a slot may also hold a child ``FieldState``.
    Paths from ``read_field_paths`` index into this tree.

    A child node holds a table's fields or an array's elements. A value written
    to the node's own path never replaces the node. The one exception is a
    variable-length array or table's length (an ``int``). The node records it and
    drops the elements at or past it, as Clarity does. Reading the node's own path
    returns that length, or ``True`` for a table without one.
    """

    __slots__ = ("_state", "_updated_paths", "_length")

    def __init__(self) -> None:
        self._state: list[FieldValue] = [None] * 8
        # The most recent decoder-provided delta paths. ``None`` preserves a
        # useful distinction for synthetic entities whose state is populated
        # directly rather than through ``read_fields``.
        self._updated_paths: list[CompactFieldPath] | None = None
        # Element count when this node is a variable-length array or table.
        self._length: int | None = None

    def get(self, fp: FieldPath) -> FieldValue:
        """Read the value at the given field path.

        Args:
            fp: A FieldPath produced by read_field_paths.

        Returns:
            The stored value, or None if the slot is empty/missing.
        """
        return self._get_compact(fp.to_tuple())

    def _get_compact(self, path: CompactFieldPath) -> FieldValue:
        """Read an internal compact path without materializing a FieldPath."""
        state = self._state
        depth = len(path)
        if depth == 1:
            idx = path[0]
            if len(state) < idx + 2:
                return None
            value = state[idx]
            return value._own_value() if isinstance(value, FieldState) else value
        if depth == 2:
            idx = path[0]
            if len(state) < idx + 2:
                return None
            child = state[idx]
            if not isinstance(child, FieldState):
                return None
            state = child._state
            idx = path[1]
            if len(state) < idx + 2:
                return None
            value = state[idx]
            return value._own_value() if isinstance(value, FieldState) else value
        last = depth - 1
        for i, idx in enumerate(path):
            if len(state) < idx + 2:
                return None
            if i == last:
                value = state[idx]
                return value._own_value() if isinstance(value, FieldState) else value
            child = state[idx]
            if not isinstance(child, FieldState):
                return None
            state = child._state
        return None

    def set(self, fp: FieldPath, value: FieldValue) -> None:
        """Write a value at the given field path, growing the tree as needed.

        A leaf write never replaces an existing child ``FieldState``. That
        mirrors Manta's behavior and preserves nested values already decoded
        below the same path prefix.

        Args:
            fp: A FieldPath produced by read_field_paths.
            value: The decoded value to store.
        """
        self._set_compact(fp.to_tuple(), value)

    def _set_compact(self, path: CompactFieldPath, value: FieldValue) -> None:
        """Write an internal compact path without materializing a FieldPath."""
        state = self._state
        depth = len(path)
        if depth == 1:
            idx = path[0]
            current_len = len(state)
            if current_len < idx + 2:
                state.extend([None] * (max(idx + 2, current_len * 2) - current_len))
            current = state[idx]
            if not isinstance(current, FieldState):
                state[idx] = value
            elif type(value) is int:
                current._resize(value)
            return
        if depth == 2:
            idx = path[0]
            current_len = len(state)
            if current_len < idx + 2:
                state.extend([None] * (max(idx + 2, current_len * 2) - current_len))
            current = state[idx]
            if not isinstance(current, FieldState):
                current = _child_replacing(current)
                state[idx] = current
            state = current._state
            idx = path[1]
            current_len = len(state)
            if current_len < idx + 2:
                state.extend([None] * (max(idx + 2, current_len * 2) - current_len))
            current = state[idx]
            if not isinstance(current, FieldState):
                state[idx] = value
            elif type(value) is int:
                current._resize(value)
            return
        last = depth - 1
        for i, idx in enumerate(path):
            current_len = len(state)
            if current_len < idx + 2:
                new_len = max(idx + 2, current_len * 2)
                state.extend([None] * (new_len - current_len))

            current = state[idx]
            if i == last:
                if not isinstance(current, FieldState):
                    state[idx] = value
                elif type(value) is int:
                    current._resize(value)
                return
            if not isinstance(current, FieldState):
                current = _child_replacing(current)
                state[idx] = current
            state = current._state

    def _resize(self, length: int) -> None:
        """Record a variable-length node's element count and drop elements past it."""
        self._length = length
        state = self._state
        if length < len(state):
            state[length:] = [None] * (len(state) - length)

    def _own_value(self) -> FieldValue:
        """Return what a read of this node's own path yields."""
        return self._length if self._length is not None else True


def _child_replacing(previous: FieldValue) -> FieldState:
    """Create the child node that replaces a leaf, keeping a length it held.

    The only leaves that later gain children are a table's presence flag
    (``bool``) and a variable-length array or table's length (``int``).
    """
    child = FieldState()
    if type(previous) is int:
        child._length = previous
    return child
