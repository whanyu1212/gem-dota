"""Field decoder dispatch and entity field reading.

Mirrors ``manta/field_reader.go`` and the decoder-lookup logic in
``manta/field.go`` (getDecoderForFieldPath).
"""

from __future__ import annotations

from typing import Any

from gem.field_path import FieldPath, read_field_paths
from gem.field_state import FieldState
from gem.reader import BitReader
from gem.sendtable import (
    FIELD_MODEL_FIXED_ARRAY,
    FIELD_MODEL_FIXED_TABLE,
    FIELD_MODEL_SIMPLE,
    FIELD_MODEL_VARIABLE_ARRAY,
    FIELD_MODEL_VARIABLE_TABLE,
    Field,
    Serializer,
)


def _get_decoder(serializer: Serializer, fp: FieldPath, pos: int) -> Any:
    f: Field = serializer.fields[fp.path[pos]]
    return _get_decoder_for_field(f, fp, pos + 1)


def _get_decoder_for_field(f: Field, fp: FieldPath, pos: int) -> Any:
    model = f.model

    if model in (FIELD_MODEL_SIMPLE, FIELD_MODEL_FIXED_ARRAY):
        return f.decoder

    if model == FIELD_MODEL_FIXED_TABLE:
        if fp.last == pos - 1:
            return f.base_decoder
        assert f.serializer is not None
        return _get_decoder(f.serializer, fp, pos)

    if model == FIELD_MODEL_VARIABLE_ARRAY:
        if fp.last == pos:
            return f.child_decoder
        return f.base_decoder

    if model == FIELD_MODEL_VARIABLE_TABLE:
        if fp.last >= pos + 1:
            assert f.serializer is not None
            return _get_decoder(f.serializer, fp, pos + 1)
        return f.base_decoder

    return f.decoder


def read_fields(r: BitReader, serializer: Serializer, state: FieldState) -> None:
    """Read all field-path/value pairs from *r* into *state*.

    Args:
        r: BitReader positioned at the start of the entity delta.
        serializer: The Serializer schema for this entity class.
        state: The FieldState tree to update.
    """
    fps = read_field_paths(r)
    for fp in fps:
        decoder = _get_decoder(serializer, fp, 0)
        if decoder is not None:
            value = decoder(r)
            state.set(fp, value)
