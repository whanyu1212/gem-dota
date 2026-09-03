"""Mutable field-path model used while decoding entity deltas."""

from __future__ import annotations

from typing import TypeAlias

_RESET = [-1, 0, 0, 0, 0, 0, 0]
CompactFieldPath: TypeAlias = tuple[int, ...]


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

    def to_tuple(self) -> CompactFieldPath:
        """Return the active indices as an immutable tuple.

        Returns:
            Tuple of active integer indices, e.g. ``(2, 0, 5)``.
        """
        path = self.path
        last = self.last
        if last < 0:
            return ()
        if last == 0:
            return (path[0],)
        if last == 1:
            return (path[0], path[1])
        if last == 2:
            return (path[0], path[1], path[2])
        if last == 3:
            return (path[0], path[1], path[2], path[3])
        if last == 4:
            return (path[0], path[1], path[2], path[3], path[4])
        if last == 5:
            return (path[0], path[1], path[2], path[3], path[4], path[5])
        return (path[0], path[1], path[2], path[3], path[4], path[5], path[6])

    @classmethod
    def _from_tuple(cls, path: CompactFieldPath) -> FieldPath:
        """Materialize a mutable compatibility path from compact indices."""
        fp = cls()
        for index, value in enumerate(path):
            fp.path[index] = value
        fp.last = len(path) - 1
        return fp

    def to_str(self) -> str:
        """Return a slash-separated string of active indices.

        Returns:
            String like ``"2/0/5"``.
        """
        return "/".join(str(self.path[i]) for i in range(self.last + 1))

    def plus_one(self) -> None:
        """Increment the deepest index by 1."""
        self.path[self.last] += 1
