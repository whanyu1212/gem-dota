"""Deprecated compatibility shim for :mod:`gem.state.entities`."""

import warnings

warnings.warn(
    "gem.entities is deprecated; import from gem.state.entities instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.state.entities import *  # noqa: E402,F403
