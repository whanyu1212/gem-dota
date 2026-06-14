"""Deprecated compatibility wrapper for :mod:`gem.schema.field_state`."""

import warnings

warnings.warn(
    "gem.field_state is deprecated; import from gem.schema.field_state instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.schema.field_state import *  # noqa: E402,F403
