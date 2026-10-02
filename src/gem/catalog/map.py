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
    """Load each neutral camp's ID, centre and type.

    A flat view of ``camp_zones.json``, the one camp catalog, so the two can't
    drift apart.

    Returns:
        One ``{"id", "x", "y", "type"}`` dict per camp, in catalog order.
    """
    return [
        {
            "id": camp["id"],
            "x": camp["center"]["x"],
            "y": camp["center"]["y"],
            "type": camp["type"],
        }
        for camp in load_camp_zones()["camps"]
    ]


def load_neutral_camp_centers() -> dict[int, tuple[float, float]]:
    """Load neutral camp IDs mapped to world-coordinate centers.

    Returns:
        Mapping of camp ID to ``(x, y)`` world-coordinate center.
    """
    camps = load_neutral_camps()
    return {int(c["id"]): (float(c["x"]), float(c["y"])) for c in camps}
