"""Nested mutable field-value tree for entity state storage.

Mirrors ``manta/field_state.go``.
"""

from __future__ import annotations

from typing import Any

from gem.field_path import FieldPath


class FieldState:
    """Nested mutable tree that stores decoded field values.

    The tree mirrors ``manta/field_state.go``: each node is a list of
    ``Any``, where a slot may hold a leaf value or a child ``FieldState``.
    Paths from ``read_field_paths`` index into this tree.
    """

    __slots__ = ("_state",)

    def __init__(self) -> None:
        self._state: list[Any] = [None] * 8

    def _ensure(self, idx: int) -> None:
        if len(self._state) < idx + 2:
            new_len = max(idx + 2, len(self._state) * 2)
            self._state.extend([None] * (new_len - len(self._state)))

    def get(self, fp: FieldPath) -> Any:
        """Read the value at the given field path.

        Args:
            fp: A FieldPath produced by read_field_paths.

        Returns:
            The stored value, or None if the slot is empty/missing.
        """
        node: FieldState = self
        for i in range(fp.last + 1):
            z = fp.path[i]
            if len(node._state) < z + 2:
                return None
            if i == fp.last:
                return node._state[z]
            child = node._state[z]
            if not isinstance(child, FieldState):
                return None
            node = child
        return None

    def set(self, fp: FieldPath, value: Any) -> None:
        """Write a value at the given field path, growing the tree as needed.

        Args:
            fp: A FieldPath produced by read_field_paths.
            value: The decoded value to store.
        """
        node: FieldState = self
        for i in range(fp.last + 1):
            z = fp.path[i]
            node._ensure(z)
            if i == fp.last:
                if not isinstance(node._state[z], FieldState):
                    node._state[z] = value
                return
            child = node._state[z]
            if not isinstance(child, FieldState):
                child = FieldState()
                node._state[z] = child
            node = child
