"""Deprecated compatibility shim for :mod:`gem.results.dataframes`."""

import warnings

warnings.warn(
    "gem.dataframes is deprecated; import from gem.results.dataframes instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.results.dataframes import build_dataframes  # noqa: E402

__all__ = ["build_dataframes"]
