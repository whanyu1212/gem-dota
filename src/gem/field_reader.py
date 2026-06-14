"""Deprecated compatibility wrapper for :mod:`gem.schema.field_reader`."""

import warnings

warnings.warn(
    "gem.field_reader is deprecated; import from gem.schema.field_reader instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.schema.field_reader import *  # noqa: E402,F403
