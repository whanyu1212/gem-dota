"""The report map window places replay positions on their structures in the 7.41 image.

World positions were read from replay 8974053011's entity stream. Pixel centres are the
structures' centres in ``assets/maps/Game_map_7.41.jpg`` (8878 x 8356), read off
gridded full-resolution crops.
"""

from __future__ import annotations

import math

import pytest

from gem.reports._formatting import (
    MAP_IMAGE_HEIGHT,
    MAP_IMAGE_WIDTH,
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    map_image_to_world,
    world_to_map_image,
)

# name: (world x, world y, image x, image y)
_LANDMARKS = {
    "radiant fountain": (8928, 9446, 906, 7567),
    "radiant ancient": (10464, 11032, 1648, 6832),
    "dire ancient": (21912, 21384, 6823, 2112),
    "radiant lotus pool": (23888, 11979, 7748, 6400),
    "dire lotus pool": (8836, 20593, 878, 2472),
    "west wisdom shrine": (8296, 17152, 623, 4042),
    "east wisdom shrine": (24551, 15242, 8046, 4910),
    "bottom outpost": (12288, 15936, 2448, 4597),
    "top outpost": (19776, 15936, 5863, 4592),
}

# About 60 world units at 0.456 px per unit; the measurements are good to ~10 px.
_TOLERANCE_PX = 30


def _image_px(wx: float, wy: float) -> tuple[float, float]:
    """Project like the report's square SVG maps, then undo the "slice" crop."""
    return world_to_map_image(wx, wy, MAP_IMAGE_WIDTH, MAP_IMAGE_HEIGHT)


def test_window_is_square() -> None:
    # The image is drawn at one scale on both axes, and the viewports are square.
    assert MAP_XMAX - MAP_XMIN == MAP_YMAX - MAP_YMIN


@pytest.mark.parametrize("name", sorted(_LANDMARKS))
def test_landmark_lands_on_its_structure(name: str) -> None:
    wx, wy, ix, iy = _LANDMARKS[name]
    px, py = _image_px(wx, wy)
    assert math.hypot(px - ix, py - iy) <= _TOLERANCE_PX


def test_image_to_world_inverts_the_projection() -> None:
    for wx, wy, _, _ in _LANDMARKS.values():
        x, y = map_image_to_world(*_image_px(wx, wy))
        assert x == pytest.approx(wx)
        assert y == pytest.approx(wy)
