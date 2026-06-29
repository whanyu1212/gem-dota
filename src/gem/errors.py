"""Public exception types for gem replay parsing and download workflows."""

from __future__ import annotations


class GemError(Exception):
    """Base class for gem-specific exceptions."""


class ReplayError(GemError):
    """Base class for replay-related exceptions."""


class ReplayParseError(ReplayError):
    """Base class for replay parsing failures surfaced by gem helpers."""


class ReplayTimeoutError(TimeoutError, ReplayParseError):
    """Raised or returned when replay parsing exceeds a configured timeout."""


class ReplayDownloadError(OSError, ReplayError):
    """Base class for replay download/decompression failures."""


class ReplayFetchError(ValueError, ReplayDownloadError):
    """Raised when OpenDota replay metadata is missing or malformed."""


class ReplayUrlError(ValueError, ReplayDownloadError):
    """Raised when a replay download URL is not allowed or cannot be normalized."""


class ReplayDecompressionError(ReplayDownloadError):
    """Raised when a downloaded replay archive cannot be decompressed."""


__all__ = [
    "GemError",
    "ReplayError",
    "ReplayParseError",
    "ReplayTimeoutError",
    "ReplayDownloadError",
    "ReplayFetchError",
    "ReplayUrlError",
    "ReplayDecompressionError",
]
