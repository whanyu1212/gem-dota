"""Helpers for renamed and deprecated public API.

Renames: gem's own fight list was renamed from ``teamfights`` to ``fights`` (the
word "teamfight" is kept for OpenDota's definition: ``opendota_teamfights`` and
``teamfight_participation``). The old names keep working for one release and
emit a :class:`DeprecationWarning`.

Deprecations: gem presents replay facts; interpretation (tags, scores, verdicts)
is leaving the library (HY-96). Deprecated names keep working until
``REMOVAL_VERSION`` and warn on use.

Reference: no upstream parser defines these names; they are gem's public API.
"""

from __future__ import annotations

import functools
import warnings
from collections.abc import Callable, Mapping
from typing import Any, TypeVar

_T = TypeVar("_T", bound=type)
_F = TypeVar("_F", bound=Callable[..., Any])

#: The release that removes the names deprecated in 0.12.
REMOVAL_VERSION = "0.13"


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


def warn_deprecated(
    name: str,
    *,
    alternative: str | None = None,
    removal: str = REMOVAL_VERSION,
    stacklevel: int = 3,
) -> None:
    """Emit the standard warning for a deprecated name.

    Args:
        name: The deprecated name, as users write it (e.g. ``gem.estimate_vision``).
        alternative: What to use instead, if anything.
        removal: The release that removes it.
        stacklevel: Passed to :func:`warnings.warn`, so the warning points at
            the caller's code.
    """
    advice = f"; use {alternative} instead" if alternative else ""
    warnings.warn(
        f"{name} is deprecated and will be removed in gem {removal}{advice}.",
        DeprecationWarning,
        stacklevel=stacklevel,
    )


def deprecated(
    name: str, *, alternative: str | None = None, removal: str = REMOVAL_VERSION
) -> Callable[[_F], _F]:
    """Function decorator: warn on every call.

    Args:
        name: The public name to show in the warning (e.g. ``gem.estimate_vision``).
        alternative: What to use instead, if anything.
        removal: The release that removes it.

    Returns:
        The decorator.
    """

    def decorate(func: _F) -> _F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warn_deprecated(name, alternative=alternative, removal=removal)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorate


def deprecated_module_attrs(
    module: str,
    deprecated_names: Mapping[str, tuple[Any, str | None, bool]],
    fallback: Callable[[str], Any] | None = None,
) -> Callable[[str], Any]:
    """Build a module ``__getattr__`` that serves deprecated names.

    The names must not be in the module's globals, or Python never calls the
    hook. Functions decorated with :func:`deprecated` already warn when called,
    so pass ``warn_on_access=False`` for them to warn once per use.

    Args:
        module: The module's name, for the warning text.
        deprecated_names: Name -> ``(object, alternative, warn_on_access)``.
        fallback: Another ``__getattr__`` to try for other names (e.g. one from
            :func:`renamed_module_attrs`).

    Returns:
        A PEP 562 module ``__getattr__``.
    """

    def __getattr__(name: str) -> Any:
        entry = deprecated_names.get(name)
        if entry is None:
            if fallback is not None:
                return fallback(name)
            raise AttributeError(f"module {module!r} has no attribute {name!r}")
        obj, alternative, warn_on_access = entry
        if warn_on_access:
            warn_deprecated(f"{module}.{name}", alternative=alternative)
        return obj

    return __getattr__
