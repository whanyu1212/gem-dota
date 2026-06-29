# Error Types

Public exception classes exposed from `gem.errors` and top-level `gem`.
Replay-specific classes are also re-exported from `gem.replays`.

| Class | Compatibility base | When it is used |
|---|---|---|
| `GemError` | `Exception` | Base class for gem-specific exceptions |
| `ReplayError` | `GemError` | Base class for replay-related exceptions |
| `ReplayParseError` | `ReplayError` | Parser/batch parse failures surfaced by gem helpers |
| `ReplayTimeoutError` | `TimeoutError` | A replay exceeded `parse_many(timeout=...)` or CLI `batch --timeout` |
| `ReplayDownloadError` | `OSError` | Base class for replay metadata/download/decompression failures |
| `ReplayFetchError` | `ValueError` | OpenDota metadata is missing or malformed |
| `ReplayUrlError` | `ValueError` | Replay URL is not HTTPS and cannot be safely upgraded |
| `ReplayDecompressionError` | `OSError` | Downloaded `.dem.bz2` payload cannot be decompressed |

The compatibility bases are intentional: existing callers that catch `ValueError`,
`TimeoutError`, or `OSError` continue to work while callers can now catch typed
gem-specific errors for finer reporting.
