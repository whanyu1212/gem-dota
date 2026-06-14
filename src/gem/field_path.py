"""Deprecated compatibility wrapper for :mod:`gem.schema.field_path`."""

import warnings

warnings.warn(
    "gem.field_path is deprecated; import from gem.schema.field_path instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.schema.field_path import *  # noqa: E402,F403
