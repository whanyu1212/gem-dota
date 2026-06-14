"""Deprecated compatibility shim for :mod:`gem.replays.batch`."""

import warnings

warnings.warn(
    "gem.batch is deprecated; import from gem.replays.batch instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.replays.batch import (  # noqa: E402
    ParseResult,
    parse_many,
    parse_many_to_dataframe,
    parse_many_to_parquet,
)

__all__ = [
    "ParseResult",
    "parse_many",
    "parse_many_to_dataframe",
    "parse_many_to_parquet",
]
