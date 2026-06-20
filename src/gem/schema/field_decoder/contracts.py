"""Shared typing contracts for field-value decoder resolution."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


FieldDecoder = Callable[["BitReader"], object]


class _FieldTypeLike(Protocol):
    """Structural type for parsed field type objects used by dispatch."""

    @property
    def base_type(self) -> str: ...


class _FieldLike(Protocol):
    """Structural type for field objects passed to decoder factories."""

    @property
    def field_type(self) -> _FieldTypeLike: ...

    @property
    def var_name(self) -> str: ...

    @property
    def encoder(self) -> str: ...

    @property
    def bit_count(self) -> int | None: ...

    @property
    def encode_flags(self) -> int | None: ...

    @property
    def low_value(self) -> float | None: ...

    @property
    def high_value(self) -> float | None: ...
