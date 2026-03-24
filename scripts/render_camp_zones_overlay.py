"""Render camp-zone overlays on a map image for calibration.

This script reads ``camp_zones.json`` in world coordinates and draws camp
boundaries plus IDs on top of a map image. It is intended for quick visual
tuning of zone geometry without touching parsing logic.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_IMAGE = REPO_ROOT / "tests" / "fixtures" / "camp_annotated.png"
DEFAULT_ZONES = REPO_ROOT / "src" / "gem" / "data" / "camp_zones.json"
DEFAULT_OUT = Path("/tmp/camp_zones_overlay_preview.png")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _world_to_px(
    wx: float,
    wy: float,
    width: int,
    height: int,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> tuple[float, float]:
    px = (wx - xmin) / (xmax - xmin) * width
    py = (1.0 - (wy - ymin) / (ymax - ymin)) * height
    return px, py


def _ellipse_world_points(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    rotation_deg: float,
    segments: int = 72,
) -> list[tuple[float, float]]:
    angle = math.radians(rotation_deg)
    ca = math.cos(angle)
    sa = math.sin(angle)
    points: list[tuple[float, float]] = []
    for i in range(segments):
        t = 2.0 * math.pi * i / segments
        ex = rx * math.cos(t)
        ey = ry * math.sin(t)
        rxp = ex * ca - ey * sa
        ryp = ex * sa + ey * ca
        points.append((cx + rxp, cy + ryp))
    return points


def _zone_world_points(camp: dict) -> list[tuple[float, float]]:
    center = camp["center"]
    cx = float(center["x"])
    cy = float(center["y"])
    zone = camp["zone"]
    shape = zone.get("shape", "ellipse")

    if shape == "ellipse":
        return _ellipse_world_points(
            cx=cx,
            cy=cy,
            rx=float(zone["rx"]),
            ry=float(zone["ry"]),
            rotation_deg=float(zone.get("rotation_deg", 0)),
        )

    if shape == "polygon":
        pts = zone.get("points", [])
        world_pts: list[tuple[float, float]] = []
        for p in pts:
            if isinstance(p, dict):
                world_pts.append((float(p["x"]), float(p["y"])))
            else:
                world_pts.append((float(p[0]), float(p[1])))
        if world_pts:
            return world_pts

    raise ValueError(f"Unsupported zone shape: {shape!r} for camp {camp.get('id')}")


def render_overlay(image_path: Path, zones_path: Path, output_path: Path) -> None:
    zones = _load_json(zones_path)
    bounds = zones["world_bounds"]
    xmin = float(bounds["xmin"])
    xmax = float(bounds["xmax"])
    ymin = float(bounds["ymin"])
    ymax = float(bounds["ymax"])

    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    color_by_type: dict[str, tuple[int, int, int]] = {
        "ancient": (255, 193, 7),
        "large": (244, 67, 54),
        "medium": (76, 175, 80),
        "small": (33, 150, 243),
        "flooded_medium": (156, 39, 176),
        "flooded_small": (63, 81, 181),
    }

    for camp in zones["camps"]:
        camp_id = int(camp["id"])
        camp_type = str(camp["type"])
        rgb = color_by_type.get(camp_type, (0, 255, 255))
        fill = (rgb[0], rgb[1], rgb[2], 64)
        outline = (rgb[0], rgb[1], rgb[2], 230)

        world_points = _zone_world_points(camp)
        pixel_points = [
            _world_to_px(wx, wy, width, height, xmin, xmax, ymin, ymax) for wx, wy in world_points
        ]

        draw.polygon(pixel_points, fill=fill, outline=outline)

        cx = float(camp["center"]["x"])
        cy = float(camp["center"]["y"])
        px, py = _world_to_px(cx, cy, width, height, xmin, xmax, ymin, ymax)

        r = 8
        draw.ellipse((px - r, py - r, px + r, py + r), fill=(255, 255, 255, 220))
        draw.ellipse((px - r, py - r, px + r, py + r), outline=(0, 0, 0, 255), width=2)

        draw.text(
            (px + 10, py - 10),
            str(camp_id),
            fill=(255, 255, 255, 255),
            stroke_width=2,
            stroke_fill=(0, 0, 0, 255),
        )

    composed = Image.alpha_composite(img, overlay)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    composed.save(output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--image",
        type=Path,
        default=DEFAULT_IMAGE,
        help=f"Background map image (default: {DEFAULT_IMAGE})",
    )
    parser.add_argument(
        "--zones",
        type=Path,
        default=DEFAULT_ZONES,
        help=f"Camp zones JSON (default: {DEFAULT_ZONES})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output PNG path (default: {DEFAULT_OUT})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    render_overlay(args.image, args.zones, args.output)
    print(f"Overlay written to: {args.output}")


if __name__ == "__main__":
    main()
