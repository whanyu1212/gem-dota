"""Deprecated compatibility shim for :mod:`gem.state.string_table`."""

import warnings

warnings.warn(
    "gem.string_table is deprecated; import from gem.state.string_table instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.state.string_table import *  # noqa: E402,F403
