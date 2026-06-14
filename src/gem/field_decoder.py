"""Deprecated compatibility wrapper for :mod:`gem.schema.field_decoder`."""

import warnings

warnings.warn(
    "gem.field_decoder is deprecated; import from gem.schema.field_decoder instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.schema.field_decoder import *  # noqa: E402,F403
