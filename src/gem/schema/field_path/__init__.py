"""Public field-path decoding API.

The implementation is split into models, operations, Huffman, and sequence
modules, but callers should continue to import from ``gem.schema.field_path``.
"""

from gem.schema.field_path.huffman import _HUFF_DECODE_TABLE, _HUFF_TABLE_BITS, HUFF_TREE
from gem.schema.field_path.models import FieldPath
from gem.schema.field_path.operations import FIELD_PATH_OPS, FieldPathOp
from gem.schema.field_path.path_sequence import read_field_paths

__all__ = [
    "FIELD_PATH_OPS",
    "FieldPath",
    "FieldPathOp",
    "HUFF_TREE",
    "_HUFF_DECODE_TABLE",
    "_HUFF_TABLE_BITS",
    "read_field_paths",
]
