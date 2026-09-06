"""Public field-path decoding API.

The implementation is split into models, operations, Huffman, and sequence
modules, but callers should continue to import from ``gem.schema.field_path``.
``__all__`` lists the stable public surface. The underscore-prefixed name
``_HUFF_TABLE_BITS`` re-exported below is an internal Huffman-table detail
shared with tests — importable by name, but not part of the public contract.
"""

from gem.schema.field_path.huffman import (
    _HUFF_TABLE_BITS as _HUFF_TABLE_BITS,
    HUFF_TREE,
)
from gem.schema.field_path.models import FieldPath
from gem.schema.field_path.operations import FIELD_PATH_OPS, FieldPathOp
from gem.schema.field_path.path_sequence import read_field_paths

__all__ = [
    "FIELD_PATH_OPS",
    "FieldPath",
    "FieldPathOp",
    "HUFF_TREE",
    "read_field_paths",
]
