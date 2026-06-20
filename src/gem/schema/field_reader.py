"""Field decoder dispatch and entity field reading.

Mirrors ``manta/field_reader.go`` and the decoder-lookup logic in
``manta/field.go`` (getDecoderForFieldPath).
"""

from __future__ import annotations

from gem.binary.reader import BitReader
from gem.schema.field_decoder import FieldDecoder
from gem.schema.field_path import FieldPath, read_field_paths
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
    """Resolve the decoder for ``fp`` starting at ``serializer.fields[pos]``."""
    f: Field = serializer.fields[fp.path[pos]]
    return _resolve_field_decoder(f, fp, pos + 1)


def _resolve_field_decoder(f: Field, fp: FieldPath, pos: int) -> FieldDecoder | None:
    """Resolve the decoder for a field-path step within one send-table field."""
    model = f.model

    if model in (FIELD_MODEL_SIMPLE, FIELD_MODEL_FIXED_ARRAY):
        return f.decoder

    if model == FIELD_MODEL_FIXED_TABLE:
        # A path ending on the table field decodes the table presence bit.
        # Deeper paths continue inside the referenced serializer at the same
        # path position, matching manta/field.go:getDecoderForFieldPath.
        if fp.last == pos - 1:
            return f.base_decoder
        return _resolve_decoder(_require_serializer(f, fp, pos), fp, pos)

    if model == FIELD_MODEL_VARIABLE_ARRAY:
        # Variable arrays use the base decoder for length metadata and the
        # child decoder for element slots.
        if fp.last == pos:
            return f.child_decoder
        return f.base_decoder

    if model == FIELD_MODEL_VARIABLE_TABLE:
        # Variable tables encode a length/index layer before nested fields, so
        # recursion skips one extra path component.
        if fp.last >= pos + 1:
            return _resolve_decoder(_require_serializer(f, fp, pos), fp, pos + 1)
        return f.base_decoder

    return f.decoder


def _require_serializer(f: Field, fp: FieldPath, pos: int) -> Serializer:
    if f.serializer is None:
        path = fp.to_str()
        raise ValueError(
            f"{f.model_name()} field {f.var_name!r} needs a serializer "
            f"to resolve field path {path!r} at position {pos}"
        )
    return f.serializer


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
    fps = read_field_paths(r)
    for fp in fps:
        decoder = _resolve_decoder(serializer, fp, 0)
        if decoder is not None:
            value = decoder(r)
            state.set(fp, value)
