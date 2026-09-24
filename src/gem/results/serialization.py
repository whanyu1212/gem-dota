"""JSON serialization and deserialization for :class:`ParsedMatch`.

:func:`to_json` writes the full-fidelity match as JSON: every ``ParsedMatch``
field at the top level, plus ``schema_version`` and ``gem_version`` keys and,
optionally, an ``analysis`` section. :func:`load_json` / :func:`from_dict`
rebuild a ``ParsedMatch`` from that output (or from a bare :func:`to_dict`
payload written by older gem versions) using the dataclass type hints, so
enums, tuples, and integer-keyed dicts come back with their original types.

Reference: gem-original; the field layout mirrors ``results/models.py``.
"""

from __future__ import annotations

import json
import types
import typing
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from functools import cache
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TYPE_CHECKING, Any

from gem.results.models import ParsedMatch

if TYPE_CHECKING:
    from gem.analysis.bundle import MatchAnalysis

#: Version of the JSON layout written by :func:`to_json`. Bump it when a change
#: would make older gem versions misread new files.
SCHEMA_VERSION = 1

# Top-level keys added by ``to_json`` beside the ``ParsedMatch`` fields.
_METADATA_KEYS = frozenset({"schema_version", "gem_version", "analysis"})


def _to_json_compatible(value: Any) -> Any:
    """Recursively convert values to JSON-compatible Python types."""
    if is_dataclass(value):
        return {
            f.name: _to_json_compatible(getattr(value, f.name))
            for f in fields(value)
            if f.metadata.get("serialize", True)
        }
    if isinstance(value, Mapping):
        return {str(k): _to_json_compatible(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_json_compatible(v) for v in value]
    return value


def to_dict(value: Any) -> Any:
    """Convert a supported dataclass or nested value to JSON-compatible data.

    Args:
        value: Parsed match, analysis assessment, or another supported nested value.

    Returns:
        A recursively converted JSON-compatible value.
    """
    return _to_json_compatible(value)


def _gem_version() -> str:
    try:
        return version("gem-dota")
    except PackageNotFoundError:
        return "unknown"


def to_json(
    match: ParsedMatch,
    *,
    analysis: MatchAnalysis | None = None,
    indent: int | None = None,
    sort_keys: bool = False,
) -> str:
    """Serialize a :class:`ParsedMatch` to a JSON string.

    Every ``ParsedMatch`` field is written at the top level, preceded by
    ``schema_version`` and ``gem_version``. When ``analysis`` is given, its
    results are added under an ``analysis`` key.

    Args:
        match: The parsed match to serialize.
        analysis: Optional :class:`MatchAnalysis`, e.g. from :func:`gem.analyze`.
        indent: Indentation passed to :func:`json.dumps`.
        sort_keys: Whether to sort object keys.

    Returns:
        A strict JSON string (no ``NaN`` or ``Infinity`` literals).

    Raises:
        ValueError: If the match contains a ``NaN`` or infinite float.
    """
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "gem_version": _gem_version(),
    }
    payload.update(to_dict(match))
    if analysis is not None:
        payload["analysis"] = to_dict(analysis)
    return json.dumps(payload, indent=indent, sort_keys=sort_keys, allow_nan=False)


def from_dict(data: Mapping[str, Any]) -> ParsedMatch:
    """Rebuild a :class:`ParsedMatch` from :func:`to_json` or :func:`to_dict` data.

    Accepts both the :func:`to_json` layout and a bare :func:`to_dict` payload,
    including files written by gem versions without ``schema_version``. Keys
    the current ``ParsedMatch`` does not define are ignored, and missing keys
    fall back to the field defaults. The optional ``analysis`` section is not
    decoded; call :func:`gem.analyze` on the returned match instead.

    Args:
        data: Decoded JSON object.

    Returns:
        The reconstructed match.

    Raises:
        ValueError: If ``data`` was written with a newer ``schema_version``.
        TypeError: If a required field is missing or has an incompatible shape.
    """
    schema_version = data.get("schema_version")
    if isinstance(schema_version, int) and schema_version > SCHEMA_VERSION:
        raise ValueError(
            f"JSON schema_version {schema_version} was written by a newer gem "
            f"(this version reads up to {SCHEMA_VERSION}); upgrade gem-dota."
        )
    match_data = {key: value for key, value in data.items() if key not in _METADATA_KEYS}
    return _decode_dataclass(ParsedMatch, match_data)


def load_json(path: str | Path) -> ParsedMatch:
    """Load a :class:`ParsedMatch` from a JSON file written by :func:`to_json`.

    Loading is much faster than re-parsing the ``.dem`` file. The file's
    ``analysis`` section is not decoded; call :func:`gem.analyze` on the loaded
    match to recompute it.

    Args:
        path: Path to the JSON file.

    Returns:
        The reconstructed match.

    Raises:
        ValueError: If the file was written with a newer ``schema_version``.
    """
    with Path(path).open(encoding="utf-8") as handle:
        return from_dict(json.load(handle))


@cache
def _init_field_types(cls: type) -> dict[str, Any]:
    hints = typing.get_type_hints(cls)
    return {f.name: hints[f.name] for f in fields(cls) if f.init}


def _decode_dataclass(cls: type, data: Mapping[str, Any]) -> Any:
    field_types = _init_field_types(cls)
    kwargs = {name: _decode(data[name], field_types[name]) for name in field_types if name in data}
    return cls(**kwargs)


def _decode(value: Any, tp: Any) -> Any:
    if value is None or tp is Any:
        return value
    origin = typing.get_origin(tp)
    if origin is typing.Union or origin is types.UnionType:
        options = [arg for arg in typing.get_args(tp) if arg is not type(None)]
        return _decode(value, options[0]) if len(options) == 1 else value
    if origin is list:
        (item_type,) = typing.get_args(tp)
        return [_decode(item, item_type) for item in value]
    if origin is set:
        (item_type,) = typing.get_args(tp)
        return {_decode(item, item_type) for item in value}
    if origin is tuple:
        args = typing.get_args(tp)
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(_decode(item, args[0]) for item in value)
        return tuple(_decode(item, item_type) for item, item_type in zip(value, args, strict=True))
    if origin is dict:
        key_type, value_type = typing.get_args(tp)
        return {_decode(key, key_type): _decode(item, value_type) for key, item in value.items()}
    if isinstance(tp, type):
        if is_dataclass(tp):
            return _decode_dataclass(tp, value)
        if issubclass(tp, Enum):
            return tp(value)
        if tp is int and isinstance(value, str):
            return int(value)  # JSON object keys are always strings
    return value
