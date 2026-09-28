"""Exceptions for problems in the replay data itself.

``ReplayParser.parse()`` tolerates these: a truncated or corrupt replay stops the
parse early, the reason is recorded (``ParsedMatch.parse_error``), and whatever was
read is kept. Any other exception, such as a bug in an extractor or in a callback
you registered, propagates instead of being mistaken for bad data.

Every class here is a ``ValueError``. The ones that replaced an older, more
specific error also keep that type, so existing ``except`` clauses still match.

Reference: gem-original. Manta (dotabuff/manta parser.go, pinned revision in
CLAUDE.md) likewise treats only the end of the file as a clean stop.
"""

from __future__ import annotations


class ReplayDataError(ValueError):
    """The replay's bytes can't be decoded: truncated, corrupt, or unsupported."""


class TruncatedReplayError(ReplayDataError, EOFError):
    """The replay file ends in the middle of a message."""


class UnsupportedReplayError(ReplayDataError, NotImplementedError):
    """The replay uses a format gem doesn't support (e.g. LZSS string tables)."""


class UnknownStringTableError(ReplayDataError, KeyError):
    """A string-table update refers to a table that was never created."""


class EntityStateError(ReplayDataError, RuntimeError):
    """An entity update contradicts the entity table (unknown class, missing entity)."""
