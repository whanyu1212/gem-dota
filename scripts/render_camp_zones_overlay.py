"""Render camp zones (and optionally the map regions) on the 7.41 map image.

Reads ``camp_zones.json`` in world coordinates and draws each camp's zone, a
type marker and its ID on a chip coloured by owner team. With ``--regions`` it
also draws the analysis regions from ``map_constants.json``: the two halves, the
river and the lotus areas. Points are placed with the report maps' calibrated
projection (``gem.reports._formatting.world_to_map_image``), so the picture
shows exactly where gem puts things.

    uv run python scripts/render_camp_zones_overlay.py --regions --width 1800 \
        --output docs/public/map-annotations.jpg
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from gem.reports._formatting import MAP_XMAX, MAP_XMIN, world_to_map_image  # noqa: E402

DEFAULT_IMAGE = REPO_ROOT / "assets" / "maps" / "Game_map_7.41.jpg"
DEFAULT_ZONES = REPO_ROOT / "src" / "gem" / "data" / "camp_zones.json"
DEFAULT_CONSTANTS = REPO_ROOT / "src" / "gem" / "data" / "map_constants.json"
DEFAULT_OUT = Path("/tmp/camp_zones_overlay_preview.png")

TEAM_CHIP_COLORS: dict[int | None, tuple[int, int, int]] = {
    2: (46, 160, 67),
    3: (200, 48, 48),
    None: (110, 110, 110),
}
REGION_COLORS: dict[str, tuple[int, int, int, int]] = {
    "radiant_half": (40, 200, 70, 46),
    "dire_half": (220, 50, 50, 46),
    "river": (60, 140, 255, 120),
    "lotus": (255, 200, 0, 120),
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _draw_regions(
    draw: ImageDraw.ImageDraw, width: int, height: int, regions: dict, marker_scale: float
) -> None:
    """Tint the halves, the river and the lotus areas, and draw the half line."""

    def px(points: list[list[float]]) -> list[tuple[float, float]]:
        return [world_to_map_image(x, y, width, height) for x, y in points]

    # The half line spans the map from edge to edge; Radiant is the side below it.
    line = px(regions["half_line"])
    below = [*line, (line[-1][0], height + 1), (line[0][0], height + 1)]
    above = [*line, (line[-1][0], -1), (line[0][0], -1)]
    draw.polygon(below, fill=REGION_COLORS["radiant_half"])
    draw.polygon(above, fill=REGION_COLORS["dire_half"])
    river = px(regions["river_outline"])
    draw.polygon(river, fill=REGION_COLORS["river"])
    draw.line([*river, river[0]], fill=(150, 210, 255, 255), width=max(2, round(2 * marker_scale)))
    radius = regions["lotus_radius"] * height / (MAP_XMAX - MAP_XMIN)
    for pos in regions["lotus_pools"].values():
        x, y = world_to_map_image(pos["x"], pos["y"], width, height)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=REGION_COLORS["lotus"])
    draw.line(line, fill=(255, 255, 255, 220), width=max(2, round(2 * marker_scale)))


def _draw_region_legend(draw: ImageDraw.ImageDraw, width: int, marker_scale: float) -> None:
    legend_scale = max(0.85, marker_scale * 0.62)
    margin = 16 * marker_scale
    padding = 12 * legend_scale
    row_gap = 26 * legend_scale
    rows = [
        ("radiant_half", (40, 200, 70), "rect"),
        ("dire_half", (220, 50, 50), "rect"),
        ("river", (60, 140, 255), "rect"),
        ("top_lotus / bottom_lotus", (255, 200, 0), "rect"),
        ("Radiant camp", TEAM_CHIP_COLORS[2], "chip"),
        ("Dire camp", TEAM_CHIP_COLORS[3], "chip"),
    ]
    panel_width = 236 * legend_scale
    panel_height = padding * 2 + 30 * legend_scale + row_gap * len(rows)
    x0 = width - margin - panel_width
    y0 = margin + 218 * legend_scale + 10 * marker_scale
    draw.rounded_rectangle(
        (x0, y0, x0 + panel_width, y0 + panel_height),
        radius=max(4, round(4 * legend_scale)),
        fill=(4, 9, 12, 205),
        outline=(255, 255, 255, 135),
        width=max(1, round(legend_scale)),
    )
    title_font = ImageFont.load_default(size=round(15 * legend_scale))
    label_font = ImageFont.load_default(size=round(13 * legend_scale))
    draw.text(
        (x0 + padding, y0 + padding),
        "Regions and owners",
        fill=(255, 255, 255, 245),
        font=title_font,
    )
    y = y0 + padding + 30 * legend_scale
    for label, rgb, kind in rows:
        box = (x0 + padding, y, x0 + padding + 22 * legend_scale, y + 14 * legend_scale)
        if kind == "rect":
            draw.rectangle(box, fill=(*rgb, 230), outline=(0, 0, 0, 255))
        else:
            draw.rounded_rectangle(box, radius=max(2, round(4 * legend_scale)), fill=(*rgb, 255))
        draw.text(
            (x0 + padding + 32 * legend_scale, y - 1 * legend_scale),
            label,
            fill=(255, 255, 255, 240),
            font=label_font,
        )
        y += row_gap


def camp_pixel(camp: dict, width: int, height: int) -> tuple[float, float]:
    """Return a camp centre's pixel on a ``width`` x ``height`` copy of the map image.

    Args:
        camp: One ``camp_zones.json`` camp.
        width: Image width.
        height: Image height.

    Returns:
        Pixel ``(column, row)``.
    """
    return world_to_map_image(float(camp["center"]["x"]), float(camp["center"]["y"]), width, height)


def render_overlay(
    image_path: Path,
    zones_path: Path,
    output_path: Path,
    *,
    constants_path: Path | None = None,
    width: int | None = None,
    margin: int = 0,
) -> None:
    """Draw the camp zones, and optionally the regions, on the map image.

    Args:
        image_path: The 7.41 map image (or a copy with the same aspect ratio).
        zones_path: ``camp_zones.json``.
        output_path: Where to save the picture (PNG or JPEG by suffix).
        constants_path: ``map_constants.json``; when given, the regions are drawn.
        width: Resize the image to this width first (keeps the aspect ratio).
        margin: Pad the picture by this many pixels on every side, so markers on
            the map's edge are not cut off.
    """
    zones = _load_json(zones_path)
    img = Image.open(image_path).convert("RGBA")
    if width is not None and width != img.width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    map_width, map_height = img.size
    if margin:
        canvas = Image.new(
            "RGBA", (map_width + 2 * margin, map_height + 2 * margin), (12, 14, 16, 255)
        )
        canvas.paste(img, (margin, margin))
        img = canvas
    width, height = img.size
    marker_scale = _marker_scale(map_width, map_height)

    def project(x: float, y: float) -> tuple[float, float]:
        px, py = world_to_map_image(x, y, map_width, map_height)
        return px + margin, py + margin

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    font = ImageFont.load_default(size=round(18 * marker_scale))

    if constants_path is not None:
        # Drawn on a map-sized layer so the tints stop at the map's edge.
        layer = Image.new("RGBA", (map_width, map_height), (0, 0, 0, 0))
        regions = _load_json(constants_path)["regions"]
        _draw_regions(ImageDraw.Draw(layer, "RGBA"), map_width, map_height, regions, marker_scale)
        overlay.alpha_composite(layer, (margin, margin))

    for camp in zones["camps"]:
        camp_id = int(camp["id"])
        camp_type = str(camp["type"])
        rgb = _camp_zone_color(camp_type)
        fill = (rgb[0], rgb[1], rgb[2], 54)
        outline = (rgb[0], rgb[1], rgb[2], 230)

        pixel_points = [project(wx, wy) for wx, wy in _zone_world_points(camp)]
        draw.polygon(pixel_points, fill=fill)
        draw.line(
            [*pixel_points, pixel_points[0]],
            fill=outline,
            width=max(2, round(2 * marker_scale)),
        )

        px, py = project(float(camp["center"]["x"]), float(camp["center"]["y"]))
        _draw_camp_marker(draw, px, py, camp_type, scale=marker_scale)

        owner = camp.get("topology", {}).get("owner_team")
        chip = TEAM_CHIP_COLORS.get(owner, TEAM_CHIP_COLORS[None])
        label_xy = (px + 26 * marker_scale, py - 15 * marker_scale)
        left, top, right, bottom = draw.textbbox(label_xy, str(camp_id), font=font)
        pad = 4 * marker_scale
        draw.rounded_rectangle(
            (left - pad, top - pad, right + pad, bottom + pad),
            radius=max(2, round(4 * marker_scale)),
            fill=(*chip, 235),
            outline=(0, 0, 0, 255),
            width=max(1, round(marker_scale)),
        )
        draw.text(label_xy, str(camp_id), fill=(255, 255, 255, 255), font=font)

    _draw_camp_legend(draw, width, marker_scale)
    if constants_path is not None:
        _draw_region_legend(draw, width, marker_scale)

    composed = Image.alpha_composite(img, overlay)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".png":
        composed.save(output_path, optimize=True, compress_level=9)
    elif output_path.suffix.lower() in {".jpg", ".jpeg"}:
        composed.convert("RGB").save(output_path, quality=88, optimize=True)
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
    parser.add_argument(
        "--regions",
        action="store_true",
        help="Also draw the halves, river and lotus areas from map_constants.json",
    )
    parser.add_argument(
        "--constants",
        type=Path,
        default=DEFAULT_CONSTANTS,
        help=f"map_constants.json for --regions (default: {DEFAULT_CONSTANTS})",
    )
    parser.add_argument("--width", type=int, help="Resize the map to this width first")
    parser.add_argument(
        "--margin", type=int, default=0, help="Pad the picture by this many pixels per side"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    render_overlay(
        args.image,
        args.zones,
        args.output,
        constants_path=args.constants if args.regions else None,
        width=args.width,
        margin=args.margin,
    )
    print(f"Overlay written to: {args.output}")


if __name__ == "__main__":
    main()
