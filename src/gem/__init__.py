"""Public package surface for gem."""

from __future__ import annotations

from gem import api as _api
from gem._deprecation import deprecated_module_attrs as _deprecated_module_attrs
from gem.api import *  # noqa: F403
from gem.api import __all__ as __all__


def _lazy_submodule(name: str) -> object:
    # gem.reports is deprecated: import it (and warn) only when it's used.
    if name == "reports":
        import importlib

        return importlib.import_module("gem.reports")
    raise AttributeError(f"module 'gem' has no attribute {name!r}")


__getattr__ = _deprecated_module_attrs(__name__, _api.DEPRECATED_NAMES, fallback=_lazy_submodule)
