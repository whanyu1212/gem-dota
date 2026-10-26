"""Field decoder dispatch and entity field reading.

Mirrors ``manta/field_reader.go`` and the decoder-lookup logic in
``manta/field.go`` (getDecoderForFieldPath). A variable-length field's length is
bounded as Clarity bounds it (``model/s2/field/VectorField.java``
``prepareForWrite``), so a desynced stream fails at once.
"""

from __future__ import annotations

from gem.binary.reader import BitReader
from gem.errors import EntityStateError, ReplayDataError
from gem.schema.field_decoder import FieldDecoder
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

#: The highest element index Clarity can address at each field-path depth
#: (``S2LongFieldPathFormat.BITS_PER_COMPONENT``, pinned revision in CLAUDE.md).
#: That is Clarity's storage limit, not a game rule, but Clarity reads every Dota
#: replay within it, so a longer variable-length field means the stream desynced.
_MAX_INDEX_AT_DEPTH = (2047, 4095, 2047, 255, 127, 15, 15)


def _bounded_length(decoder: FieldDecoder | None, depth: int) -> FieldDecoder | None:
    """Wrap a variable-length field's length decoder with Clarity's bound at ``depth``.

    ``depth`` is its elements' field-path depth, one past the length's own: Clarity
    checks ``fp.last() + 1`` (``S2FieldReader``).
    """
    if decoder is None:
        return None
    limit = _MAX_INDEX_AT_DEPTH[depth] + 1 if depth < len(_MAX_INDEX_AT_DEPTH) else 0

    def read_length(r: BitReader) -> object:
        length = decoder(r)
        if isinstance(length, int) and length > limit:
            raise EntityStateError(
                f"decoder desync: variable-length field of length {length} with elements "
                f"at field-path depth {depth} exceeds the maximum of {limit}; an earlier field was "
                "likely read with the wrong decoder"
            )
        return length

    return read_length


def _resolve_decoder(
    serializer: Serializer,
    path: CompactFieldPath,
    pos: int,
) -> FieldDecoder | None:
    """Resolve the decoder for *path* starting at one serializer level."""
    f: Field = serializer.fields[path[pos]]
    return _resolve_field_decoder(f, path, pos + 1)


def _resolve_field_decoder(
    f: Field,
    path: CompactFieldPath,
    pos: int,
) -> FieldDecoder | None:
    """Resolve one field-path step using Source 2 field models."""
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
        return _resolve_decoder(_require_serializer(f, path, pos), path, pos)

    if model == FIELD_MODEL_VARIABLE_ARRAY:
        # Variable arrays use the base decoder for length metadata and the
        # child decoder for element slots.
        if last == pos:
            return f.child_decoder
        return _bounded_length(f.base_decoder, last + 1)

    if model == FIELD_MODEL_VARIABLE_TABLE:
        # Variable tables encode a length/index layer before nested fields, so
        # recursion skips one extra path component.
        if last >= pos + 1:
            return _resolve_decoder(_require_serializer(f, path, pos), path, pos + 1)
        if last == pos - 1:
            return _bounded_length(f.base_decoder, last + 1)
        return f.base_decoder

    return f.decoder


def _require_serializer(f: Field, path: CompactFieldPath, pos: int) -> Serializer:
    if f.serializer is None:
        path_string = "/".join(str(index) for index in path)
        raise ReplayDataError(
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
        decoder = _resolve_decoder(serializer, path, 0)
        serializer._resolved_decoders[path] = decoder
        return decoder


def read_fields(r: BitReader, serializer: Serializer, state: FieldState) -> None:
    """Read all field-path/value pairs from *r* into *state*.

    Args:
        r: BitReader positioned at the start of the entity delta.
        serializer: The Serializer schema for this entity class.
        state: The FieldState tree to update.
    """
    paths = _read_compact_field_paths(r)
    state._updated_paths = paths
    decoder_cache = serializer._resolved_decoders
    for path in paths:
        # The cache hit is inlined: this loop runs millions of times per replay.
        try:
            decoder = decoder_cache[path]
        except KeyError:
            decoder = _resolve_cached_decoder(serializer, path)
        if decoder is not None:
            value = decoder(r)
            state._set_compact(path, value)
