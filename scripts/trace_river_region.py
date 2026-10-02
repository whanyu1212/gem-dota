"""Trace the river outline and half line for ``region_of`` from the map image.

``gem.region_of`` (``gem.analysis.regions``) reads ``regions.river_outline`` and
``regions.half_line`` from ``src/gem/data/map_constants.json``. This script
derives both from ``assets/maps/Game_map_7.41.jpg``:

1. Mark water pixels by colour (dark blue-green) on a 1800-px-wide copy.
2. Keep the water near a hand-traced seed line, between the east edge of the
   top-lane stone plaza and the west edge of the bottom-lane ford, so the lanes
   and the shrine pools beyond them stay out.
3. Close small gaps, take the piece holding Roshan pit 1's pool, fill its holes
   (the pits and islands), smooth it, and simplify its outline.
4. Build the half line from the middle of the traced water in each column, and
   continue it flat to past the map edges with the seed line's end points.
5. Project the pixels to world units through the report map window
   (``gem.reports._formatting``), which was fitted to replay landmarks.

The lotus pools are not traced: they are ``CDOTA_BaseNPC_LotusPool`` entity
positions, and this script leaves them alone. A map patch that moves the river
needs a new image and, if the river's shape changes, a new seed line and
lane-crossing columns.

OpenCV is not a project dependency, so run the script with it added::

    uv run --with opencv-python-headless python scripts/trace_river_region.py --check
    uv run --with opencv-python-headless python scripts/trace_river_region.py --write
    uv run --with opencv-python-headless python scripts/trace_river_region.py \\
        --overlay /tmp/regions.jpg

Reference: none of the pinned parsers (manta, clarity, odota/parser) defines map
regions; the geometry is gem's own, calibrated against replay 8974053011's
entity positions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from gem.reports._formatting import (  # noqa: E402
    MAP_XMAX,
    MAP_XMIN,
    map_image_to_world,
    world_to_map_image,
)

DEFAULT_IMAGE = REPO_ROOT / "assets" / "maps" / "Game_map_7.41.jpg"
DEFAULT_CONSTANTS = REPO_ROOT / "src" / "gem" / "data" / "map_constants.json"

# Tracing happens on a copy this wide; every pixel constant below is in its space.
TRACE_WIDTH = 1800

# A water pixel (after a 3-px blur) is dark and blue-green.
WATER_MAX_RED = 50
WATER_MAX_GREEN_BLUE = 64
WATER_MIN_TINT = 6  # green and blue each exceed red by at least this

# River centre line traced by eye, left map edge to right map edge. Only its parts
# outside the lane crossings survive into the half line; the rest bounds the
# corridor the water is taken from.
SEED_LINE = (
    (0, 635),
    (150, 630),
    (300, 625),
    (430, 632),
    (560, 655),
    (650, 720),
    (723, 787),
    (800, 860),
    (880, 930),
    (985, 1003),
    (1060, 1080),
    (1140, 1150),
    (1250, 1178),
    (1400, 1182),
    (1550, 1180),
    (1800, 1180),
)
CORRIDOR_PX = 190
# East edge of the top-lane stone plaza and west edge of the bottom-lane ford.
TOP_CROSSING_X = 400
BOTTOM_CROSSING_X = 1360
# A pixel in Roshan pit 1's pool, (row, column).
SEED_POOL = (640, 480)
CLOSE_RADIUS = 10
OPEN_RADIUS = 4
SIMPLIFY_PX = 7.0
MIDLINE_STEP = 45
# Middle samples start and stop this far inside the crossings.
MIDLINE_INSET_TOP = 12
MIDLINE_INSET_BOTTOM = 10


def trace_size(image_size: tuple[int, int]) -> tuple[int, int]:
    """Return the tracing copy's size for a map image size.

    Args:
        image_size: ``(width, height)`` of the source image.

    Returns:
        ``(width, height)`` of the copy, :data:`TRACE_WIDTH` wide.
    """
    width, height = image_size
    return TRACE_WIDTH, round(height * TRACE_WIDTH / width)


def image_to_world(px: float, py: float, width: int, height: int) -> tuple[float, float]:
    """Project a tracing-copy pixel to world units.

    Args:
        px: Pixel column.
        py: Pixel row.
        width: Tracing-copy width.
        height: Tracing-copy height.

    Returns:
        World ``(x, y)``, through ``gem.reports._formatting.map_image_to_world``.
    """
    return map_image_to_world(px, py, width, height)


def world_to_image(x: float, y: float, width: int, height: int) -> tuple[float, float]:
    """Project world units to a pixel of an image drawn like the tracing copy.

    Args:
        x: World x.
        y: World y.
        width: Image width.
        height: Image height.

    Returns:
        Pixel ``(column, row)``, through ``gem.reports._formatting.world_to_map_image``.
    """
    return world_to_map_image(x, y, width, height)


def water_mask(image: Image.Image) -> np.ndarray:
    """Mark the water pixels of a map image.

    Args:
        image: The full-resolution map image.

    Returns:
        A boolean array the size of the tracing copy.
    """
    small = image.convert("RGB").resize(trace_size(image.size), Image.BOX)
    pixels = np.asarray(small.filter(ImageFilter.GaussianBlur(3))).astype(int)
    red, green, blue = pixels[..., 0], pixels[..., 1], pixels[..., 2]
    return (
        (red < WATER_MAX_RED)
        & (green < WATER_MAX_GREEN_BLUE)
        & (blue < WATER_MAX_GREEN_BLUE)
        & (blue - red >= WATER_MIN_TINT)
        & (green - red >= WATER_MIN_TINT)
    )


def _distance_to_seed_line(shape: tuple[int, int]) -> np.ndarray:
    rows, cols = np.mgrid[0 : shape[0], 0 : shape[1]]
    line = np.array(SEED_LINE, dtype=float)
    distance = np.full(shape, np.inf)
    for (x1, y1), (x2, y2) in zip(line[:-1], line[1:], strict=True):
        dx, dy = x2 - x1, y2 - y1
        t = np.clip(((cols - x1) * dx + (rows - y1) * dy) / (dx * dx + dy * dy), 0, 1)
        distance = np.minimum(distance, np.hypot(cols - (x1 + t * dx), rows - (y1 + t * dy)))
    return distance


def trace_river(water: np.ndarray) -> tuple[np.ndarray, list[tuple[float, float]]]:
    """Trace the river from a water mask.

    Args:
        water: Output of :func:`water_mask`.

    Returns:
        The filled river mask, and its simplified outline in tracing-copy pixels.

    Raises:
        SystemExit: If OpenCV is not installed, or :data:`SEED_POOL` is not water.
    """
    try:
        import cv2
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise SystemExit(
            "OpenCV is required: uv run --with opencv-python-headless python "
            "scripts/trace_river_region.py ..."
        ) from exc

    def disc(radius: int) -> Any:
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * radius + 1, 2 * radius + 1))

    cols = np.mgrid[0 : water.shape[0], 0 : water.shape[1]][1]
    between_crossings = (cols >= TOP_CROSSING_X) & (cols <= BOTTOM_CROSSING_X)
    near_seed = _distance_to_seed_line(water.shape) <= CORRIDOR_PX
    mask = (water & near_seed & between_crossings).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, disc(CLOSE_RADIUS))
    _, labels = cv2.connectedComponents(mask)
    seed_label = labels[SEED_POOL]
    if seed_label == 0:
        # Label 0 is the background: on a new map image the seed is not water.
        raise SystemExit(
            f"SEED_POOL {SEED_POOL} (row, column) is not water in this image; "
            "move it into Roshan pit 1's pool"
        )
    mask = (labels == seed_label).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = cv2.drawContours(np.zeros_like(mask), contours, -1, 1, thickness=-1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, disc(OPEN_RADIUS))
    mask[:, :TOP_CROSSING_X] = 0
    mask[:, BOTTOM_CROSSING_X + 1 :] = 0
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    outline = cv2.approxPolyDP(max(contours, key=cv2.contourArea), SIMPLIFY_PX, True)
    return mask.astype(bool), [(float(p[0][0]), float(p[0][1])) for p in outline]


def half_line(river: np.ndarray) -> list[tuple[float, float]]:
    """Build the half line in tracing-copy pixels.

    Args:
        river: The filled river mask from :func:`trace_river`.

    Returns:
        The seed line's points outside the crossings, joined by the middle of the
        traced water in every :data:`MIDLINE_STEP`-th column between them.
    """
    first = TOP_CROSSING_X + MIDLINE_INSET_TOP
    last = BOTTOM_CROSSING_X - MIDLINE_INSET_BOTTOM
    middle = []
    for x in [*range(first, last, MIDLINE_STEP), last]:
        rows = np.nonzero(river[:, x])[0]
        if len(rows):
            middle.append((float(x), float((rows.min() + rows.max()) / 2)))
    before = [(float(x), float(y)) for x, y in SEED_LINE if x < TOP_CROSSING_X]
    after = [(float(x), float(y)) for x, y in SEED_LINE if x > BOTTOM_CROSSING_X]
    return [*before, *middle, *after]


def trace_regions(image_path: Path = DEFAULT_IMAGE) -> dict[str, list[list[int]]]:
    """Trace ``river_outline`` and ``half_line`` in world units.

    Args:
        image_path: The map image.

    Returns:
        ``{"river_outline": [[x, y], ...], "half_line": [[x, y], ...]}``.
    """
    with Image.open(image_path) as image:
        water = water_mask(image)
    height, width = water.shape
    river, outline = trace_river(water)

    def to_world(points: list[tuple[float, float]]) -> list[list[int]]:
        return [[round(c) for c in image_to_world(x, y, width, height)] for x, y in points]

    return {"river_outline": to_world(outline), "half_line": to_world(half_line(river))}


def _format_points(points: list[list[int]], per_line: int = 6) -> str:
    rows = [
        ", ".join(f"[{x}, {y}]" for x, y in points[i : i + per_line])
        for i in range(0, len(points), per_line)
    ]
    return "[\n      " + ",\n      ".join(rows) + "\n    ]"


def write_regions(constants_path: Path, traced: dict[str, list[list[int]]]) -> None:
    """Replace the traced arrays in ``map_constants.json``, keeping its layout.

    Args:
        constants_path: Path to ``map_constants.json``.
        traced: Output of :func:`trace_regions`.

    Raises:
        SystemExit: If an array is not found in the file.
    """
    text = constants_path.read_text(encoding="utf-8")
    for key, points in traced.items():
        pattern = re.compile(rf'("{key}": )\[\n.*?\n    \]', re.DOTALL)
        replacement = _format_points(points)

        def replace(match: re.Match[str], replacement: str = replacement) -> str:
            return match.group(1) + replacement

        text, count = pattern.subn(replace, text)
        if count != 1:
            raise SystemExit(f"{constants_path}: could not find regions.{key}")
    json.loads(text)
    constants_path.write_text(text, encoding="utf-8")


def render_overlay(image_path: Path, constants_path: Path, out_path: Path) -> None:
    """Draw the committed regions on the map image for review.

    Args:
        image_path: The map image.
        constants_path: Path to ``map_constants.json``.
        out_path: Where to save the preview.
    """
    regions = json.loads(constants_path.read_text(encoding="utf-8"))["regions"]
    with Image.open(image_path) as source:
        image = source.convert("RGB").resize(trace_size(source.size), Image.LANCZOS)
    width, height = image.size

    def px(points: list[list[float]]) -> list[tuple[float, float]]:
        return [world_to_image(x, y, width, height) for x, y in points]

    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.polygon(px(regions["river_outline"]), fill=(60, 140, 255, 110), outline=(150, 210, 255))
    draw.line(px(regions["half_line"]), fill=(255, 255, 255, 255), width=2)
    scale = height / (MAP_XMAX - MAP_XMIN)
    radius = regions["lotus_radius"] * scale
    for pos in regions["lotus_pools"].values():
        x, y = world_to_image(pos["x"], pos["y"], width, height)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(255, 200, 0, 110))
    Image.alpha_composite(image.convert("RGBA"), layer).convert("RGB").save(out_path, quality=90)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE, help="Map image")
    parser.add_argument(
        "--constants", type=Path, default=DEFAULT_CONSTANTS, help="map_constants.json path"
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--check", action="store_true", help="Fail unless the trace equals the committed regions"
    )
    action.add_argument(
        "--write", action="store_true", help="Write the trace into map_constants.json"
    )
    action.add_argument(
        "--overlay", type=Path, help="Save a preview of the committed regions on the map"
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.overlay is not None:
        render_overlay(args.image, args.constants, args.overlay)
        print(f"saved {args.overlay}")
        return 0
    traced = trace_regions(args.image)
    if args.check:
        committed = json.loads(args.constants.read_text(encoding="utf-8"))["regions"]
        stale = [key for key in traced if committed.get(key) != traced[key]]
        if stale:
            raise SystemExit(f"traced regions differ from {args.constants}: {', '.join(stale)}")
        print(f"traced regions match {args.constants}")
        return 0
    if args.write:
        write_regions(args.constants, traced)
        print(f"wrote river_outline and half_line to {args.constants}")
        return 0
    print(json.dumps(traced))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
