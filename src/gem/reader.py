"""Deprecated compatibility wrapper for :mod:`gem.binary.reader`."""

import warnings

warnings.warn(
    "gem.reader is deprecated; import from gem.binary.reader instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.binary.reader import *  # noqa: E402,F403
