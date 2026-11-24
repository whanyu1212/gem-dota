"""The map calibration places replay positions on their structures in the 7.41 image.

World positions were read from replay 8974053011's entity stream. Pixel centres are the
structures' centres in ``assets/maps/Game_map_7.41.jpg`` (8878 x 8356), read off
gridded full-resolution crops.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from gem.catalog.map import (
    MAP_IMAGE_HEIGHT,
    MAP_IMAGE_WIDTH,
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    fountains_on_patch,
    map_image_to_world,
    world_to_map_image,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent

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


def test_742_map_shares_the_calibrated_canvas() -> None:
    """The 7.42 image is the 7.41 canvas scaled down, so the same window places it.

    It registers against the 7.41 export at scale 1 and offset 0 on that canvas
    (``assets/maps/README.md``); its height keeps the canvas's aspect ratio to
    within a pixel.
    """
    with Image.open(_REPO_ROOT / "assets" / "maps" / "Game_map_7.42.jpg") as image:
        width, height = image.size
    assert height == pytest.approx(width * MAP_IMAGE_HEIGHT / MAP_IMAGE_WIDTH, abs=0.5)


def _dire_fountain_lava_centroid(image_path: Path, wx: float, wy: float) -> tuple[float, float]:
    """Return the Dire fountain's glowing lava centroid on the 8878 x 8356 canvas."""
    with Image.open(image_path) as raw:
        width, height = raw.size
        px, py = world_to_map_image(wx, wy, width, height)
        radius = max(40, round(250 * width / MAP_IMAGE_WIDTH))
        x0 = max(0, int(px - radius))
        y0 = max(0, int(py - radius))
        x1 = min(width, int(px + radius))
        y1 = min(height, int(py + radius))
        crop = np.asarray(raw.crop((x0, y0, x1, y1)).convert("RGB"), dtype=np.float32)

    mask = (
        (crop[:, :, 0] > 180)
        & (crop[:, :, 1] > 70)
        & (crop[:, :, 2] < 60)
        & (crop[:, :, 0] - crop[:, :, 2] > 140)
    )
    ys, xs = np.nonzero(mask)
    assert len(xs) > 0
    cx = (x0 + float(xs.mean())) * MAP_IMAGE_WIDTH / width
    cy = (y0 + float(ys.mean())) * MAP_IMAGE_HEIGHT / height
    return cx, cy


def test_742_dire_fountain_realigns_with_image() -> None:
    """7.42's moved Dire fountain world anchor tracks the structure shift on the map image."""
    f741 = fountains_on_patch("7.41")["dire"]
    f742 = fountains_on_patch("7.42")["dire"]

    p741 = _image_px(f741["x"], f741["y"])
    p742 = _image_px(f742["x"], f742["y"])
    c741 = _dire_fountain_lava_centroid(
        _REPO_ROOT / "assets" / "maps" / "Game_map_7.41.jpg", f741["x"], f741["y"]
    )
    c742 = _dire_fountain_lava_centroid(
        _REPO_ROOT / "assets" / "maps" / "Game_map_7.42.jpg", f742["x"], f742["y"]
    )

    projected_shift = (p742[0] - p741[0], p742[1] - p741[1])
    measured_shift = (c742[0] - c741[0], c742[1] - c741[1])
    assert (
        math.hypot(measured_shift[0] - projected_shift[0], measured_shift[1] - projected_shift[1])
        <= 15
    )
    assert math.hypot(p742[0] - c742[0], p742[1] - c742[1]) < 50
    assert (
        math.hypot(p742[0] - c742[0], p742[1] - c742[1])
        < math.hypot(p741[0] - c742[0], p741[1] - c742[1]) / 2
    )
