from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.render_camp_zones_overlay import (
    _camp_marker_kind,
    _camp_zone_color,
    _draw_camp_marker,
    _marker_scale,
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


def test_render_overlay_draws_camp_marker(tmp_path: Path) -> None:
    image_path = tmp_path / "map.jpg"
    zones_path = tmp_path / "zones.json"
    output_path = tmp_path / "annotated.png"

    Image.new("RGB", (120, 120), (255, 255, 255)).save(image_path)
    zones_path.write_text(
        json.dumps(
            {
                "world_bounds": {"xmin": 0, "xmax": 120, "ymin": 0, "ymax": 120},
                "camps": [
                    {
                        "id": 1,
                        "type": "medium",
                        "center": {"x": 60, "y": 60},
                        "zone": {"shape": "ellipse", "rx": 20, "ry": 20, "rotation_deg": 0},
                    }
                ],
            }
        ),
        encoding="utf-8",
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
    zones_path.write_text(
        json.dumps(
            {
                "world_bounds": {"xmin": 0, "xmax": 360, "ymin": 0, "ymax": 260},
                "camps": [],
            }
        ),
        encoding="utf-8",
    )

    render_overlay(image_path, zones_path, output_path)

    rendered = Image.open(output_path).convert("RGBA")
    top_right_pixels = [rendered.getpixel((x, y)) for x in range(220, 350) for y in range(10, 150)]
    assert any(pixel[:3] != (255, 255, 255) for pixel in top_right_pixels)
