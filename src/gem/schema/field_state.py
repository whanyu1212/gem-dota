"""Nested mutable field-value tree for entity state storage.

Mirrors ``manta/field_state.go``.
"""

from __future__ import annotations

from typing import TypeAlias, TypeGuard

from gem.schema.field_path import FieldPath
from gem.schema.field_path.models import CompactFieldPath

FieldValue: TypeAlias = object | None


class FieldState:
    """Nested mutable tree that stores decoded field values.

    The tree mirrors ``manta/field_state.go``: each node is a list of
    ``FieldValue`` objects, where a slot may also hold a child ``FieldState``.
    Paths from ``read_field_paths`` index into this tree.
    """

    __slots__ = ("_state",)

    def __init__(self) -> None:
        self._state: list[FieldValue] = [None] * 8

    @staticmethod
    def _is_child(value: FieldValue) -> TypeGuard[FieldState]:
        return isinstance(value, FieldState)

    def _has_slot(self, idx: int) -> bool:
        return len(self._state) >= idx + 2

    def _ensure(self, idx: int) -> None:
        if not self._has_slot(idx):
            current_len = len(self._state)
            new_len = max(idx + 2, current_len * 2)
            self._state.extend([None] * (new_len - len(self._state)))

    def get(self, fp: FieldPath) -> FieldValue:
        """Read the value at the given field path.

        Args:
            fp: A FieldPath produced by read_field_paths.

        Returns:
            The stored value, or None if the slot is empty/missing.
        """
        path = fp.path
        last = fp.last
        state = self._state
        for i in range(last + 1):
            idx = path[i]
            if len(state) < idx + 2:
                return None
            if i == last:
                return state[idx]
            child = state[idx]
            if not isinstance(child, FieldState):
                return None
            state = child._state
        return None

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

    def set(self, fp: FieldPath, value: FieldValue) -> None:
        """Write a value at the given field path, growing the tree as needed.

        A leaf write never replaces an existing child ``FieldState``. That
        mirrors Manta's behavior and preserves nested values already decoded
        below the same path prefix.

        Args:
            fp: A FieldPath produced by read_field_paths.
            value: The decoded value to store.
        """
        path = fp.path
        last = fp.last
        state = self._state
        for i in range(last + 1):
            idx = path[i]
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
