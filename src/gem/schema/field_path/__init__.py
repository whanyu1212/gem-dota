"""Public field-path decoding API.

The implementation is split into ``models``, ``operations``, ``huffman``, and
``path_sequence`` modules; callers import from ``gem.schema.field_path``.
``__all__`` lists the stable public surface. Internal helpers stay in their
defining modules.
"""

from gem.schema.field_path.huffman import HUFF_TREE
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
