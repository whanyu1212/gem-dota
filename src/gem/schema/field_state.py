"""Nested mutable field-value tree for entity state storage.

Mirrors ``manta/field_state.go``.
"""

from __future__ import annotations

from typing import TypeAlias, TypeGuard

from gem.schema.field_path import FieldPath

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
        node: FieldState = self
        for i in range(fp.last + 1):
            z = fp.path[i]
            if not node._has_slot(z):
                return None
            if i == fp.last:
                return node._state[z]
            child = node._state[z]
            if not self._is_child(child):
                return None
            node = child
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
        node: FieldState = self
        for i in range(fp.last + 1):
            z = fp.path[i]
            node._ensure(z)
            if i == fp.last:
                if not self._is_child(node._state[z]):
                    node._state[z] = value
                return
            child = node._state[z]
            if not self._is_child(child):
                child = FieldState()
                node._state[z] = child
            node = child
