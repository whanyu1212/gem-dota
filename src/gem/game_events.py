"""Deprecated compatibility shim for :mod:`gem.state.game_events`."""

import warnings

warnings.warn(
    "gem.game_events is deprecated; import from gem.state.game_events instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.state.game_events import *  # noqa: E402,F403
