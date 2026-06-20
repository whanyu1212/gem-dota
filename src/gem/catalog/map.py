"""Map catalog lookups for static map and neutral-camp data.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from typing import Any

from gem.catalog.resources import load_data_json


def load_camp_zones() -> dict[str, Any]:
    """Load calibrated neutral-camp zone geometry.

    Returns:
        Decoded ``camp_zones.json`` payload.
    """
    return load_data_json("camp_zones.json")


def load_map_constants() -> dict[str, Any]:
    """Load static map calibration constants.

    Returns:
        Decoded ``map_constants.json`` payload.
    """
    return load_data_json("map_constants.json")


def load_neutral_camps() -> list[dict[str, Any]]:
    """Load static neutral-camp center data.

    Returns:
        Decoded ``neutral_camps.json`` payload.
    """
    return load_data_json("neutral_camps.json")


def load_neutral_camp_centers() -> dict[int, tuple[float, float]]:
    """Load neutral camp IDs mapped to world-coordinate centers.

    Returns:
        Mapping of camp ID to ``(x, y)`` world-coordinate center.
    """
    camps = load_neutral_camps()
    return {int(c["id"]): (float(c["x"]), float(c["y"])) for c in camps}
