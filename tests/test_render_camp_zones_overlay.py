from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

from gem.catalog.map import (
    MAP_IMAGE_HEIGHT,
    MAP_IMAGE_WIDTH,
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    world_to_map_image,
)
from scripts.render_camp_zones_overlay import (
    DEFAULT_CONSTANTS,
    _camp_marker_kind,
    _camp_zone_color,
    _draw_camp_marker,
    _marker_scale,
    camp_pixel,
    render_overlay,
)


def test_camp_marker_kind_maps_flooded_types_to_base_tiers() -> None:
    assert _camp_marker_kind("small") == ("small", False)
    assert _camp_marker_kind("medium") == ("medium", False)
    assert _camp_marker_kind("large") == ("large", False)
    assert _camp_marker_kind("ancient") == ("ancient", False)
    assert _camp_marker_kind("flooded_small") == ("small", True)
    assert _camp_marker_kind("flooded_medium") == ("medium", True)


def test_camp_zone_color_uses_type_specific_palette() -> None:
    assert _camp_zone_color("small") == (86, 170, 255)
    assert _camp_zone_color("medium") == (54, 211, 153)
    assert _camp_zone_color("large") == (255, 149, 79)
    assert _camp_zone_color("ancient") == (255, 210, 77)
    assert _camp_zone_color("flooded_small") == (22, 186, 197)
    assert _camp_zone_color("flooded_medium") == (45, 125, 255)


def test_marker_scale_grows_for_large_map_images() -> None:
    assert _marker_scale(120, 120) == 1.0
    assert _marker_scale(8878, 8356) >= 6.0


def test_camp_marker_keeps_ring_without_filled_dot() -> None:
    image = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    _draw_camp_marker(ImageDraw.Draw(image, "RGBA"), 50, 50, "medium", scale=1.0)

    assert image.getpixel((63, 42))[3] == 0


# The centre of the report map window: the middle of any image with the 7.41 map's
# aspect ratio.
_WINDOW_CENTRE = ((MAP_XMIN + MAP_XMAX) / 2, (MAP_YMIN + MAP_YMAX) / 2)


def _write_zones(path: Path, camps: list[dict]) -> None:
    path.write_text(json.dumps({"camps": camps}), encoding="utf-8")


def test_camp_pixel_uses_the_report_projection() -> None:
    camp = {"center": {"x": 8928, "y": 9446}}
    assert camp_pixel(camp, MAP_IMAGE_WIDTH, MAP_IMAGE_HEIGHT) == world_to_map_image(
        8928, 9446, MAP_IMAGE_WIDTH, MAP_IMAGE_HEIGHT
    )


def test_render_overlay_draws_camp_marker(tmp_path: Path) -> None:
    image_path = tmp_path / "map.jpg"
    zones_path = tmp_path / "zones.json"
    output_path = tmp_path / "annotated.png"

    Image.new("RGB", (120, 120), (255, 255, 255)).save(image_path)
    cx, cy = _WINDOW_CENTRE
    _write_zones(
        zones_path,
        [
            {
                "id": 1,
                "type": "medium",
                "center": {"x": cx, "y": cy},
                "topology": {"owner_team": 2},
                "zone": {"shape": "ellipse", "rx": 2000, "ry": 2000, "rotation_deg": 0},
            }
        ],
    )

    render_overlay(image_path, zones_path, output_path)

    rendered = Image.open(output_path).convert("RGBA")
    center_pixels = [rendered.getpixel((x, y)) for x in range(50, 71) for y in range(50, 71)]
    assert any(pixel[:3] != (255, 255, 255) for pixel in center_pixels)


def test_render_overlay_draws_top_right_legend(tmp_path: Path) -> None:
    image_path = tmp_path / "map.jpg"
    zones_path = tmp_path / "zones.json"
    output_path = tmp_path / "annotated.png"

    Image.new("RGB", (360, 260), (255, 255, 255)).save(image_path)
    _write_zones(zones_path, [])

    render_overlay(image_path, zones_path, output_path)

    rendered = Image.open(output_path).convert("RGBA")
    top_right_pixels = [rendered.getpixel((x, y)) for x in range(220, 350) for y in range(10, 150)]
    assert any(pixel[:3] != (255, 255, 255) for pixel in top_right_pixels)


def test_render_overlay_draws_regions_inside_the_margin(tmp_path: Path) -> None:
    image_path = tmp_path / "map.jpg"
    zones_path = tmp_path / "zones.json"
    output_path = tmp_path / "annotated.png"

    Image.new("RGB", (400, 377), (255, 255, 255)).save(image_path)
    _write_zones(zones_path, [])

    render_overlay(image_path, zones_path, output_path, constants_path=DEFAULT_CONSTANTS, margin=20)

    rendered = Image.open(output_path).convert("RGB")
    assert rendered.size == (440, 417)
    # The margin keeps its background; the tints stop at the map's edge.
    assert rendered.getpixel((5, 400)) == (12, 14, 16)
    # Bottom-left of the map is the Radiant half (green tint), top-left the Dire half.
    r, g, b = rendered.getpixel((30, 380))
    assert g > r and g > b
    r, g, b = rendered.getpixel((30, 30))
    assert r > g and r > b
    # The top power rune is in the river (blue).
    x, y = world_to_map_image(14744, 17496, 400, 377)
    r, g, b = rendered.getpixel((round(x) + 20, round(y) + 20))
    assert b > r and b > g
