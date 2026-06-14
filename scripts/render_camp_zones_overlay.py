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

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_IMAGE = REPO_ROOT / "assets" / "maps" / "camp_annotated.png"
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


def _camp_marker_kind(camp_type: str) -> tuple[str, bool]:
    """Return the visual marker tier and whether the camp is flooded."""
    flooded = camp_type.startswith("flooded_")
    if flooded:
        camp_type = camp_type.removeprefix("flooded_")
    if camp_type not in {"small", "medium", "large", "ancient"}:
        return "unknown", flooded
    return camp_type, flooded


def _camp_zone_color(camp_type: str) -> tuple[int, int, int]:
    """Return the annotation-zone color for a camp type."""
    color_by_type: dict[str, tuple[int, int, int]] = {
        "small": (86, 170, 255),
        "medium": (54, 211, 153),
        "large": (255, 149, 79),
        "ancient": (255, 210, 77),
        "flooded_small": (22, 186, 197),
        "flooded_medium": (45, 125, 255),
    }
    return color_by_type.get(camp_type, (0, 255, 255))


def _marker_scale(width: int, height: int) -> float:
    """Scale marker geometry for high-resolution map fixtures."""
    return max(1.0, min(width, height) / 1200.0)


def _draw_camp_marker(
    draw: ImageDraw.ImageDraw,
    px: float,
    py: float,
    camp_type: str,
    *,
    scale: float,
) -> None:
    marker_kind, flooded = _camp_marker_kind(camp_type)
    if marker_kind == "unknown":
        r = 12 * scale
        draw.ellipse((px - r, py - r, px + r, py + r), fill=(0, 255, 255, 230))
        draw.ellipse(
            (px - r, py - r, px + r, py + r),
            outline=(0, 0, 0, 255),
            width=max(2, round(2 * scale)),
        )
        return

    zone_rgb = _camp_zone_color(camp_type)
    halo_r = 22 * scale if marker_kind == "ancient" else 20 * scale
    halo_box = (px - halo_r, py - halo_r, px + halo_r, py + halo_r)
    draw.ellipse(
        halo_box,
        outline=(0, 0, 0, 180),
        width=max(3, round(4 * scale)),
    )
    draw.ellipse(
        halo_box,
        outline=(zone_rgb[0], zone_rgb[1], zone_rgb[2], 245),
        width=max(2, round(2 * scale)),
    )

    if flooded:
        draw.arc(
            (
                px - 12 * scale,
                py + 3 * scale,
                px + 12 * scale,
                py + 15 * scale,
            ),
            195,
            345,
            fill=(179, 242, 255, 255),
            width=max(2, round(2 * scale)),
        )

    size = 20 * scale if marker_kind == "ancient" else 17 * scale
    fill = (255, 214, 74, 245)
    outline = (35, 28, 10, 255)
    triangle = [
        (px, py - size),
        (px - size, py + size * 0.72),
        (px + size, py + size * 0.72),
    ]
    draw.polygon(triangle, fill=fill)
    draw.line([*triangle, triangle[0]], fill=outline, width=max(2, round(2 * scale)))

    if marker_kind == "ancient":
        inner_size = size * 0.48
        inner = [
            (px, py - inner_size),
            (px - inner_size, py + inner_size * 0.72),
            (px + inner_size, py + inner_size * 0.72),
        ]
        draw.line([*inner, inner[0]], fill=outline, width=max(2, round(2 * scale)))
        return

    bar_count = {"small": 0, "medium": 1, "large": 2}[marker_kind]
    bar_width = size * 1.55
    bar_height = 4 * scale
    start_y = py + size * 0.92
    for index in range(bar_count):
        y = start_y + index * 7 * scale
        draw.rounded_rectangle(
            (px - bar_width / 2, y, px + bar_width / 2, y + bar_height),
            radius=max(1, round(scale)),
            fill=fill,
            outline=outline,
            width=max(1, round(scale)),
        )


def _draw_camp_legend(
    draw: ImageDraw.ImageDraw,
    width: int,
    marker_scale: float,
) -> None:
    legend_scale = max(0.85, marker_scale * 0.62)
    margin = 16 * marker_scale
    padding_x = 13 * legend_scale
    padding_y = 11 * legend_scale
    row_gap = 30 * legend_scale
    panel_width = 174 * legend_scale
    panel_height = 218 * legend_scale
    x0 = width - margin - panel_width
    y0 = margin
    x1 = width - margin
    y1 = y0 + panel_height

    draw.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=max(4, round(4 * legend_scale)),
        fill=(4, 9, 12, 205),
        outline=(255, 255, 255, 135),
        width=max(1, round(legend_scale)),
    )

    title_font = ImageFont.load_default(size=round(15 * legend_scale))
    label_font = ImageFont.load_default(size=round(13 * legend_scale))
    title_x = x0 + padding_x
    title_y = y0 + padding_y
    draw.text(
        (title_x, title_y),
        "Camp types",
        fill=(255, 255, 255, 245),
        font=title_font,
        stroke_width=max(1, round(legend_scale * 0.6)),
        stroke_fill=(0, 0, 0, 255),
    )

    items = [
        ("Small", "small"),
        ("Medium", "medium"),
        ("Large", "large"),
        ("Ancient", "ancient"),
        ("Flooded small", "flooded_small"),
        ("Flooded medium", "flooded_medium"),
    ]
    row_y = y0 + padding_y + 34 * legend_scale
    icon_x = x0 + padding_x + 15 * legend_scale
    label_x = x0 + padding_x + 43 * legend_scale
    for label, camp_type in items:
        _draw_camp_marker(
            draw, icon_x, row_y + 7 * legend_scale, camp_type, scale=legend_scale * 0.58
        )
        draw.text(
            (label_x, row_y - 4 * legend_scale),
            label,
            fill=(255, 255, 255, 240),
            font=label_font,
            stroke_width=max(1, round(legend_scale * 0.45)),
            stroke_fill=(0, 0, 0, 255),
        )
        row_y += row_gap


def render_overlay(image_path: Path, zones_path: Path, output_path: Path) -> None:
    zones = _load_json(zones_path)
    bounds = zones["world_bounds"]
    xmin = float(bounds["xmin"])
    xmax = float(bounds["xmax"])
    ymin = float(bounds["ymin"])
    ymax = float(bounds["ymax"])

    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    marker_scale = _marker_scale(width, height)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    font = ImageFont.load_default(size=round(18 * marker_scale))

    for camp in zones["camps"]:
        camp_id = int(camp["id"])
        camp_type = str(camp["type"])
        rgb = _camp_zone_color(camp_type)
        fill = (rgb[0], rgb[1], rgb[2], 54)
        outline = (rgb[0], rgb[1], rgb[2], 230)

        world_points = _zone_world_points(camp)
        pixel_points = [
            _world_to_px(wx, wy, width, height, xmin, xmax, ymin, ymax) for wx, wy in world_points
        ]

        draw.polygon(pixel_points, fill=fill)
        draw.line(
            [*pixel_points, pixel_points[0]],
            fill=outline,
            width=max(2, round(2 * marker_scale)),
        )

        cx = float(camp["center"]["x"])
        cy = float(camp["center"]["y"])
        px, py = _world_to_px(cx, cy, width, height, xmin, xmax, ymin, ymax)

        _draw_camp_marker(draw, px, py, camp_type, scale=marker_scale)

        draw.text(
            (px + 34 * marker_scale, py - 15 * marker_scale),
            str(camp_id),
            fill=(255, 255, 255, 255),
            font=font,
            stroke_width=max(2, round(2 * marker_scale)),
            stroke_fill=(0, 0, 0, 255),
        )

    _draw_camp_legend(draw, width, marker_scale)

    composed = Image.alpha_composite(img, overlay)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".png":
        composed.save(output_path, optimize=True, compress_level=9)
    elif output_path.suffix.lower() in {".jpg", ".jpeg"}:
        composed.convert("RGB").save(output_path, quality=92, optimize=True)
    else:
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
