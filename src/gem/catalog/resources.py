"""Bundled catalog resource loading.

Core JSON assets live in :mod:`gem.data` so they can be loaded from an
installed wheel via :mod:`importlib.resources`.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any


def load_data_text(name: str) -> str:
    """Load a bundled data file as text.

    Args:
        name: File name within the ``gem.data`` resource package.

    Returns:
        UTF-8 decoded file contents.
    """
    return files("gem.data").joinpath(name).read_text(encoding="utf-8")


def load_data_json(name: str) -> Any:
    """Load a bundled JSON data file.

    Args:
        name: JSON file name within the ``gem.data`` resource package.

    Returns:
        Decoded JSON payload.
    """
    return json.loads(load_data_text(name))
