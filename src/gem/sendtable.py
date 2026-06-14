"""Deprecated compatibility wrapper for :mod:`gem.schema.sendtable`."""

import warnings

warnings.warn(
    "gem.sendtable is deprecated; import from gem.schema.sendtable instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.schema.sendtable import *  # noqa: E402,F403
