"""Deprecated compatibility wrapper for :mod:`gem.binary.stream`."""

import warnings

warnings.warn(
    "gem.stream is deprecated; import from gem.binary.stream instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.binary.stream import *  # noqa: E402,F403
