"""Helpers for deprecating public API.

gem presents replay facts; interpretation (tags, scores, verdicts) left the
library in 0.13 (HY-96). These helpers deprecate a name for one release before it
is removed: deprecated names keep working until ``REMOVAL_VERSION`` and warn on
use.

Reference: no upstream parser defines these names; they are gem's public API.
"""

from __future__ import annotations

import functools
import warnings
from collections.abc import Callable, Mapping
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

#: The release that removes the names currently deprecated.
REMOVAL_VERSION = "0.14"


def warn_deprecated(
    name: str,
    *,
    alternative: str | None = None,
    removal: str = REMOVAL_VERSION,
    stacklevel: int = 3,
) -> None:
    """Emit the standard warning for a deprecated name.

    Args:
        name: The deprecated name, as users write it (e.g. ``gem.old_helper``).
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
        name: The public name to show in the warning (e.g. ``gem.old_helper``).
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


class deprecated_field:  # noqa: N801 - used like ``field``/``property``
    """Dataclass field default that warns when the deprecated field is read.

    Use it as the field's default, keeping it out of ``repr`` and ``==`` so that
    printing or comparing an object does not warn::

        context: Context | None = field(
            default=cast(Any, deprecated_field("context", "gem.Segment.context")),
            repr=False,
            compare=False,
        )

    Setting the field (including in ``__init__``) is silent; reading it through
    the instance warns. gem's own code reads it with :func:`read_quietly`. The
    class must not use ``slots``: the value lives in the instance ``__dict__``.

    Args:
        attr: The field's attribute name.
        name: The public name for the warning (e.g. ``gem.MatchAnalysis.old_field``).
        alternative: What to use instead, if anything.
        removal: The release that removes it.
        default: The value when none is given.
        default_factory: Called for the value when none is given (wins over ``default``).
    """

    def __init__(
        self,
        attr: str,
        name: str,
        *,
        alternative: str | None = None,
        removal: str = REMOVAL_VERSION,
        default: Any = None,
        default_factory: Callable[[], Any] | None = None,
    ) -> None:
        self._slot = f"_deprecated_{attr}"
        self._name = name
        self._alternative = alternative
        self._removal = removal
        self._default = default
        self._default_factory = default_factory

    def _make_default(self) -> Any:
        return self._default_factory() if self._default_factory is not None else self._default

    def read(self, obj: Any) -> Any:
        """Return the stored value without warning."""
        if self._slot not in obj.__dict__:
            obj.__dict__[self._slot] = self._make_default()
        return obj.__dict__[self._slot]

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        warn_deprecated(self._name, alternative=self._alternative, removal=self._removal)
        return self.read(obj)

    def __set__(self, obj: Any, value: Any) -> None:
        # dataclass passes the default (this descriptor) when no value is given.
        obj.__dict__[self._slot] = self._make_default() if value is self else value


def read_quietly(obj: Any, attr: str) -> Any:
    """Read an attribute, without the warning if it is a :class:`deprecated_field`.

    gem's own serializers and report code use this so producing output that still
    includes a deprecated field does not warn the user.

    Args:
        obj: The instance.
        attr: The attribute name.

    Returns:
        The attribute's value.
    """
    for klass in type(obj).__mro__:
        if attr in vars(klass):
            descriptor = vars(klass)[attr]
            if isinstance(descriptor, deprecated_field):
                return descriptor.read(obj)
            break
    return getattr(obj, attr)
