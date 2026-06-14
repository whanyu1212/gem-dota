"""Deprecated compatibility shim for :mod:`gem.replays.fetch`."""

import warnings

warnings.warn(
    "gem.replay_fetch is deprecated; import from gem.replays.fetch instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.replays.fetch import (  # noqa: E402
    download_and_decompress,
    fetch_replay,
    fetch_replay_url,
)

__all__ = ["download_and_decompress", "fetch_replay", "fetch_replay_url"]
