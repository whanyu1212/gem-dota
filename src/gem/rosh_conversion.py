"""Deprecated compatibility shim for :mod:`gem.analysis.roshan`."""

import warnings

warnings.warn(
    "gem.rosh_conversion is deprecated; import from gem.analysis.roshan instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.analysis.roshan import (  # noqa: E402
    RoshConversion,
    RoshTimelineEvent,
    build_rosh_conversions,
)

__all__ = ["RoshConversion", "RoshTimelineEvent", "build_rosh_conversions"]
