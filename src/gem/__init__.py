"""Public package surface for gem."""

from __future__ import annotations

from gem import api as _api
from gem._deprecation import deprecated_module_attrs as _deprecated_module_attrs
from gem.api import *  # noqa: F403
from gem.api import __all__ as __all__

__getattr__ = _deprecated_module_attrs(__name__, _api.DEPRECATED_NAMES)
