"""Replay utility helpers for fetching and batch-processing replay files."""

from gem.errors import (
    ReplayDecompressionError,
    ReplayDownloadError,
    ReplayError,
    ReplayFetchError,
    ReplayParseError,
    ReplayTimeoutError,
    ReplayUrlError,
)
from gem.replays.batch import (
    ParseResult,
    parse_many,
    parse_many_to_dataframe,
    parse_many_to_parquet,
)
from gem.replays.fetch import (
    apply_api_rates,
    download_and_decompress,
    enrich_with_api_rates,
    fetch_opendota_match,
    fetch_replay,
    fetch_replay_url,
)

__all__ = [
    "ReplayError",
    "ReplayParseError",
    "ReplayTimeoutError",
    "ReplayDownloadError",
    "ReplayFetchError",
    "ReplayUrlError",
    "ReplayDecompressionError",
    "ParseResult",
    "apply_api_rates",
    "download_and_decompress",
    "enrich_with_api_rates",
    "fetch_opendota_match",
    "fetch_replay",
    "fetch_replay_url",
    "parse_many",
    "parse_many_to_dataframe",
    "parse_many_to_parquet",
]
