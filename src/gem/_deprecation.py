"""Deprecated-name helpers for renamed public API.

gem's own fight list was renamed from ``teamfights`` to ``fights`` (the word
"teamfight" is kept for OpenDota's definition: ``opendota_teamfights`` and
``teamfight_participation``). The old names keep working for one release and
emit a :class:`DeprecationWarning`.

Reference: no upstream parser defines these names; they are gem's public API.
"""

from __future__ import annotations

import functools
import warnings
from collections.abc import Callable, Mapping
from typing import Any, TypeVar

_T = TypeVar("_T", bound=type)


def warn_renamed(old: str, new: str, *, stacklevel: int = 3) -> None:
    """Emit the standard warning for a renamed name.

    Args:
        old: The deprecated name.
        new: The name to use instead.
        stacklevel: Passed to :func:`warnings.warn`, so the warning points at
            the caller's code.
    """
    warnings.warn(
        f"{old} is deprecated and will be removed in a future release; use {new} instead.",
        DeprecationWarning,
        stacklevel=stacklevel,
    )


def renamed_attribute(old: str, new: str) -> property:
    """Return a property that forwards a renamed attribute with a warning.

    Args:
        old: The deprecated attribute name.
        new: The attribute it now lives under.

    Returns:
        A read/write property for the class body, e.g.
        ``teamfights = renamed_attribute("teamfights", "fights")``.
    """

    def getter(self: Any) -> Any:
        warn_renamed(f"{type(self).__name__}.{old}", f"{type(self).__name__}.{new}")
        return getattr(self, new)

    def setter(self: Any, value: Any) -> None:
        warn_renamed(f"{type(self).__name__}.{old}", f"{type(self).__name__}.{new}")
        setattr(self, new, value)

    return property(getter, setter, doc=f"Deprecated alias of ``{new}``.")


def renamed_init_kwargs(renames: Mapping[str, str]) -> Callable[[_T], _T]:
    """Class decorator: accept renamed ``__init__`` keywords with a warning.

    Apply it above ``@dataclass`` so it wraps the generated ``__init__``.

    Args:
        renames: Deprecated keyword -> current keyword.

    Returns:
        The decorator.
    """

    def decorate(cls: _T) -> _T:
        init = cls.__init__  # type: ignore[misc]

        @functools.wraps(init)
        def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
            for old, new in renames.items():
                if old in kwargs:
                    if new in kwargs:
                        raise TypeError(f"{cls.__name__}() got both {old!r} and {new!r}")
                    warn_renamed(f"{cls.__name__}({old}=...)", f"{cls.__name__}({new}=...)")
                    kwargs[new] = kwargs.pop(old)
            init(self, *args, **kwargs)

        cls.__init__ = __init__  # type: ignore[misc]
        return cls

    return decorate


def renamed_module_attrs(
    module: str, renames: Mapping[str, str], namespace: Mapping[str, Any]
) -> Callable[[str], Any]:
    """Build a module ``__getattr__`` that serves renamed names with a warning.

    Args:
        module: The module's name, for the warning text.
        renames: Deprecated name -> current name.
        namespace: The module's ``globals()``, where the current names live.

    Returns:
        A PEP 562 module ``__getattr__``.
    """

    def __getattr__(name: str) -> Any:
        new = renames.get(name)
        if new is None:
            raise AttributeError(f"module {module!r} has no attribute {name!r}")
        warn_renamed(f"{module}.{name}", f"{module}.{new}")
        return namespace[new]

    return __getattr__
