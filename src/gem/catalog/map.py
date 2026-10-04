"""Map catalog lookups for static map and neutral-camp data, and the map calibration.

The calibration (``MAP_XMIN``…``MAP_YMAX``, :func:`world_to_map_image`) places
world coordinates on ``assets/maps/Game_map_7.41.jpg``; the docs site's figures
and the map tooling in ``scripts/`` use it.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from typing import Any

from gem.catalog.resources import load_data_json

# World-coordinate window of the 7.41 map image,
# assets/maps/Game_map_7.41.jpg (8878 x 8356). The maps are square viewports that
# draw the image with ``preserveAspectRatio="xMidYMid slice"``, so they show its
# middle 8356 x 8356 pixels. The image is drawn at one scale on both axes,
# 0.456071 px per world unit, so the window spans 18322 world units on each axis.
# Calibrated by a least-squares fit of nine landmark positions read from replay
# 8974053011 (fountain, ancients, lotus pools, wisdom shrines, outposts) against
# their pixel centres in the image: 9 px RMS, at most 29 px (about 60 world units).
MAP_XMIN, MAP_XMAX = 7487, 25809
MAP_YMIN, MAP_YMAX = 7693, 26015
# Map image size, for views that place the full image themselves.
MAP_IMAGE_WIDTH, MAP_IMAGE_HEIGHT = 8878, 8356


def world_to_map_image(
    x: float, y: float, width: float = MAP_IMAGE_WIDTH, height: float = MAP_IMAGE_HEIGHT
) -> tuple[float, float]:
    """Project world coordinates onto the 7.41 map image.

    The map figures show the image's centred square, ``height`` pixels a side, as
    the ``MAP_XMIN``…``MAP_YMAX`` window. ``width`` and ``height`` may describe a
    resized copy of the image, as long as it keeps the original aspect ratio.

    Args:
        x: World x.
        y: World y.
        width: Image width in pixels.
        height: Image height in pixels.

    Returns:
        Pixel ``(column, row)``.
    """
    side = height
    fx = (x - MAP_XMIN) / (MAP_XMAX - MAP_XMIN)
    fy = 1.0 - (y - MAP_YMIN) / (MAP_YMAX - MAP_YMIN)
    return (width - side) / 2 + fx * side, fy * side


def map_image_to_world(
    px: float, py: float, width: float = MAP_IMAGE_WIDTH, height: float = MAP_IMAGE_HEIGHT
) -> tuple[float, float]:
    """Project a 7.41 map image pixel to world coordinates (inverse of :func:`world_to_map_image`).

    Args:
        px: Pixel column.
        py: Pixel row.
        width: Image width in pixels.
        height: Image height in pixels.

    Returns:
        World ``(x, y)``.
    """
    side = height
    x = MAP_XMIN + (px - (width - side) / 2) / side * (MAP_XMAX - MAP_XMIN)
    y = MAP_YMIN + (1 - py / side) * (MAP_YMAX - MAP_YMIN)
    return x, y


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
