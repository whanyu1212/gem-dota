"""Field decoder dispatch and entity field reading.

Mirrors ``manta/field_reader.go`` and the decoder-lookup logic in
``manta/field.go`` (getDecoderForFieldPath).
"""

from __future__ import annotations

from gem.binary.reader import BitReader
from gem.schema.field_decoder import FieldDecoder
from gem.schema.field_path import FieldPath
from gem.schema.field_path.models import CompactFieldPath
from gem.schema.field_path.path_sequence import _read_compact_field_paths
from gem.schema.field_state import FieldState
from gem.schema.sendtable import (
    FIELD_MODEL_FIXED_ARRAY,
    FIELD_MODEL_FIXED_TABLE,
    FIELD_MODEL_SIMPLE,
    FIELD_MODEL_VARIABLE_ARRAY,
    FIELD_MODEL_VARIABLE_TABLE,
    Field,
    Serializer,
)


def _resolve_decoder(serializer: Serializer, fp: FieldPath, pos: int) -> FieldDecoder | None:
    """Compatibility resolver for a mutable ``FieldPath``."""
    return _resolve_compact_decoder(serializer, fp.to_tuple(), pos)


def _resolve_field_decoder(f: Field, fp: FieldPath, pos: int) -> FieldDecoder | None:
    """Compatibility field resolver for a mutable ``FieldPath``."""
    return _resolve_compact_field_decoder(f, fp.to_tuple(), pos)


def _resolve_compact_decoder(
    serializer: Serializer,
    path: CompactFieldPath,
    pos: int,
) -> FieldDecoder | None:
    """Resolve the decoder for a compact path from one serializer level."""
    f: Field = serializer.fields[path[pos]]
    return _resolve_compact_field_decoder(f, path, pos + 1)


def _resolve_compact_field_decoder(
    f: Field,
    path: CompactFieldPath,
    pos: int,
) -> FieldDecoder | None:
    """Resolve one compact field-path step using Source 2 field models."""
    model = f.model
    last = len(path) - 1

    if model in (FIELD_MODEL_SIMPLE, FIELD_MODEL_FIXED_ARRAY):
        return f.decoder

    if model == FIELD_MODEL_FIXED_TABLE:
        # A path ending on the table field decodes the table presence bit.
        # Deeper paths continue inside the referenced serializer at the same
        # path position, matching manta/field.go:getDecoderForFieldPath.
        if last == pos - 1:
            return f.base_decoder
        return _resolve_compact_decoder(_require_serializer(f, path, pos), path, pos)

    if model == FIELD_MODEL_VARIABLE_ARRAY:
        # Variable arrays use the base decoder for length metadata and the
        # child decoder for element slots.
        if last == pos:
            return f.child_decoder
        return f.base_decoder

    if model == FIELD_MODEL_VARIABLE_TABLE:
        # Variable tables encode a length/index layer before nested fields, so
        # recursion skips one extra path component.
        if last >= pos + 1:
            return _resolve_compact_decoder(_require_serializer(f, path, pos), path, pos + 1)
        return f.base_decoder

    return f.decoder


def _require_serializer(f: Field, path: CompactFieldPath, pos: int) -> Serializer:
    if f.serializer is None:
        path_string = "/".join(str(index) for index in path)
        raise ValueError(
            f"{f.model_name()} field {f.var_name!r} needs a serializer "
            f"to resolve field path {path_string!r} at position {pos}"
        )
    return f.serializer


def _resolve_cached_decoder(
    serializer: Serializer,
    path: CompactFieldPath,
) -> FieldDecoder | None:
    """Return a parse-scoped cached decoder, including explicit None results."""
    try:
        return serializer._resolved_decoders[path]
    except KeyError:
        decoder = _resolve_compact_decoder(serializer, path, 0)
        serializer._resolved_decoders[path] = decoder
        return decoder


# Backwards-compatible private aliases for older internal tests/imports.
_get_decoder = _resolve_decoder
_get_decoder_for_field = _resolve_field_decoder


def read_fields(r: BitReader, serializer: Serializer, state: FieldState) -> None:
    """Read all field-path/value pairs from *r* into *state*.

    Args:
        r: BitReader positioned at the start of the entity delta.
        serializer: The Serializer schema for this entity class.
        state: The FieldState tree to update.
    """
    paths = _read_compact_field_paths(r)
    decoder_cache = serializer._resolved_decoders
    for path in paths:
        try:
            decoder = decoder_cache[path]
        except KeyError:
            decoder = _resolve_compact_decoder(serializer, path, 0)
            decoder_cache[path] = decoder
        if decoder is not None:
            value = decoder(r)
            state._set_compact(path, value)
