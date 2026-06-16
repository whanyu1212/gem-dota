"""Public field-path decoding API.

The implementation is split into model, operation-table, Huffman, and decoder
modules, but callers should continue to import from ``gem.schema.field_path``.
"""

from gem.schema.field_path.decoder import read_field_paths
from gem.schema.field_path.huffman import _HUFF_DECODE_TABLE, _HUFF_TABLE_BITS, HUFF_TREE
from gem.schema.field_path.model import FieldPath
from gem.schema.field_path.ops import FIELD_PATH_OPS, FieldPathOp

__all__ = [
    "FIELD_PATH_OPS",
    "FieldPath",
    "FieldPathOp",
    "HUFF_TREE",
    "_HUFF_DECODE_TABLE",
    "_HUFF_TABLE_BITS",
    "read_field_paths",
]
