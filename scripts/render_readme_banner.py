"""Render the README banner: the gem logo and wordmark over the 7.41 map.

The right half is the real map, faded into the dark background behind the
wordmark, with gem's own annotation on top: the two halves, the river, the lotus
pools and every neutral camp coloured by type. The overlay comes from
``map_constants.json`` and ``camp_zones.json`` and is placed with the report
maps' calibrated window (``MAP_XMIN``…``MAP_YMAX``), so it shows exactly where
gem puts things. The logo is read from ``site/public/logo.svg``.

Text is set in Inter (SIL OFL, the docs site's text font, from its Fontsource
package) and converted to paths, so the output does not depend on installed
fonts. Run ``npm install`` in ``site/`` first for the font, then:

    uv run --with cairosvg --with uharfbuzz --with fonttools --with brotli \
        python scripts/render_readme_banner.py

On macOS with Homebrew's cairo, prefix ``DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib``.
The README links to the PNG by its path on ``main``, so keep the default output
path. (It moved from ``docs/public/`` to ``site/public/`` in HY-118; releases
before that link the old path.)
"""

from __future__ import annotations

import argparse
import base64
import io
import re
import sys
from collections.abc import Iterable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from gem.catalog.map import (  # noqa: E402
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    load_camp_zones,
    load_map_constants,
)

DEFAULT_OUTPUT = REPO_ROOT / "site" / "public" / "gem-readme-banner-wordmark-subtitle-spaced.png"
DEFAULT_MAP = REPO_ROOT / "assets" / "maps" / "Game_map_7.41.jpg"
DEFAULT_FONT = (
    REPO_ROOT / "site/node_modules/@fontsource-variable/inter/files/inter-latin-opsz-normal.woff2"
)
LOGO = REPO_ROOT / "site" / "public" / "logo.svg"

WIDTH, HEIGHT = 1600, 500
BACKGROUND = "#0d1117"
CHIPS = ("Entities", "Combat log", "Fights", "Map regions")
# Camp colours match scripts/render_camp_zones_overlay.py and the docs figure.
CAMP_COLORS = {
    "small": "#56aaff",
    "medium": "#36d399",
    "large": "#ff954f",
    "ancient": "#ffd24d",
    "flooded_small": "#16bac5",
    "flooded_medium": "#2d7dff",
}
# The map square is drawn MAP_SIZE px a side at (MAP_X, MAP_Y), so the river
# runs across the banner and the bases fall outside it.
MAP_SIZE, MAP_X, MAP_Y = 1060, 640, -300


class _Font:
    """Inter shaped with HarfBuzz and drawn as SVG paths."""

    def __init__(self, path: Path) -> None:
        import uharfbuzz as hb
        from fontTools.ttLib import TTFont

        self._font = TTFont(path)
        self._glyph_order = self._font.getGlyphOrder()
        self._upem = self._font["head"].unitsPerEm
        self._font.flavor = None
        buffer = io.BytesIO()
        self._font.save(buffer)
        self._face = hb.Face(buffer.getvalue())

    def path(
        self, text: str, x: float, y: float, size: float, *, weight: int, opsz: float
    ) -> tuple[str, float]:
        """Return SVG path data for ``text`` with its baseline at ``(x, y)``, and its width."""
        import uharfbuzz as hb
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen

        location = {"wght": weight, "opsz": opsz}
        hb_font = hb.Font(self._face)
        hb_font.set_variations(location)
        buffer = hb.Buffer()
        buffer.add_str(text)
        buffer.guess_segment_properties()
        hb.shape(hb_font, buffer, {"kern": True, "liga": True})
        glyphs = self._font.getGlyphSet(location=location)
        scale = size / self._upem
        pen_x, parts = x, []
        for info, position in zip(buffer.glyph_infos, buffer.glyph_positions, strict=True):
            pen = SVGPathPen(glyphs)
            transform = (scale, 0, 0, -scale, pen_x + position.x_offset * scale, y)
            glyphs[self._glyph_order[info.codepoint]].draw(TransformPen(pen, transform))
            parts.append(pen.getCommands())
            pen_x += position.x_advance * scale
        return " ".join(part for part in parts if part), pen_x - x


def _points(points: Iterable[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def _project(x: float, y: float) -> tuple[float, float]:
    fx = (x - MAP_XMIN) / (MAP_XMAX - MAP_XMIN)
    fy = 1.0 - (y - MAP_YMIN) / (MAP_YMAX - MAP_YMIN)
    return MAP_X + fx * MAP_SIZE, MAP_Y + fy * MAP_SIZE


def _map_square_b64(map_path: Path) -> str:
    """The image's centred square (the report maps' window), as a base64 JPEG."""
    from PIL import Image

    with Image.open(map_path) as image:
        side = image.height
        left = (image.width - side) // 2
        square = image.convert("RGB").crop((left, 0, left + side, side))
        square = square.resize((MAP_SIZE * 2, MAP_SIZE * 2), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    square.save(buffer, "JPEG", quality=88)
    return base64.b64encode(buffer.getvalue()).decode()


def _overlay() -> str:
    regions = load_map_constants()["regions"]
    camps = load_camp_zones()["camps"]
    half = [_project(*point) for point in regions["half_line"]]
    river = _points(_project(*point) for point in regions["river_outline"])
    margin = 2000
    dire = [
        *half,
        _project(MAP_XMAX + margin, MAP_YMAX + margin),
        _project(MAP_XMIN - margin, MAP_YMAX + margin),
    ]
    radiant = [
        *half,
        _project(MAP_XMAX + margin, MAP_YMIN - margin),
        _project(MAP_XMIN - margin, MAP_YMIN - margin),
    ]
    lotus_radius = regions["lotus_radius"] / (MAP_XMAX - MAP_XMIN) * MAP_SIZE

    parts = [
        f'<polygon points="{_points(dire)}" fill="#dc3232" fill-opacity="0.14"/>',
        f'<polygon points="{_points(radiant)}" fill="#28c846" fill-opacity="0.14"/>',
        f'<polygon points="{river}" fill="none" stroke="#5aa0ff" stroke-opacity="0.25" '
        'stroke-width="15" stroke-linejoin="round"/>',
        f'<polygon points="{river}" fill="#3c8cff" fill-opacity="0.38" stroke="#9cc8ff" '
        'stroke-width="2.6" stroke-linejoin="round"/>',
        f'<polyline points="{_points(half)}" fill="none" stroke="#ffffff" stroke-opacity="0.55" '
        'stroke-width="2.1" stroke-dasharray="13 10"/>',
    ]
    for pool in regions["lotus_pools"].values():
        cx, cy = _project(pool["x"], pool["y"])
        parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{lotus_radius:.1f}" fill="#ba55ff" '
            'fill-opacity="0.45" stroke="#e3b8ff" stroke-width="1.2"/>'
        )
    for camp in camps:
        cx, cy = _project(camp["center"]["x"], camp["center"]["y"])
        color = CAMP_COLORS.get(camp["type"], "#ffffff")
        parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="{color}" fill-opacity="0.22"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="{color}" '
            f'stroke="{BACKGROUND}" stroke-width="2.4"/>'
        )
    return "".join(parts)


def _logo_body() -> str:
    svg = LOGO.read_text()
    body = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S)
    if body is None:
        raise ValueError(f"{LOGO} is not an SVG")
    return re.sub(r"<title>.*?</title>", "", body.group(1), flags=re.S)


def _brand(font: _Font) -> str:
    text_x = 420
    word, _ = font.path("gem", text_x, 250, 156, weight=750, opsz=32)
    tagline, _ = font.path(
        "A Dota 2 replay parser for Python", text_x + 10, 318, 34, weight=550, opsz=24
    )
    chips, chip_x = [], text_x + 6.0
    for label in CHIPS:
        _, label_width = font.path(label, 0, 0, 18, weight=600, opsz=14)
        chip_width = label_width + 32
        label_path, _ = font.path(label, chip_x + 16, 378, 18, weight=600, opsz=14)
        chips.append(
            f'<rect x="{chip_x:.1f}" y="352" width="{chip_width:.1f}" height="40" rx="20" '
            f'fill="#16301f" fill-opacity="0.92"/><path d="{label_path}" fill="#9eeebf"/>'
        )
        chip_x += chip_width + 12
    return (
        f'<g transform="translate(80,110) scale({280 / 64})">{_logo_body()}</g>'
        f'<path d="{word}" fill="#e8fff1"/><path d="{tagline}" fill="#b4cbbd"/>' + "".join(chips)
    )


def banner_svg(font: _Font, map_path: Path) -> str:
    """Return the banner as an SVG document with the map embedded."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <linearGradient id="fade-x" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{BACKGROUND}" stop-opacity="1"/>
      <stop offset="0.48" stop-color="{BACKGROUND}" stop-opacity="1"/>
      <stop offset="0.72" stop-color="{BACKGROUND}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{BACKGROUND}" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="fade-y" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="{BACKGROUND}" stop-opacity="0.75"/>
      <stop offset="0.2" stop-color="{BACKGROUND}" stop-opacity="0"/>
      <stop offset="0.8" stop-color="{BACKGROUND}" stop-opacity="0"/>
      <stop offset="1" stop-color="{BACKGROUND}" stop-opacity="0.75"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.14" cy="0.5" r="0.45">
      <stop offset="0" stop-color="#1f6f43" stop-opacity="0.5"/>
      <stop offset="1" stop-color="{BACKGROUND}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect width="{WIDTH}" height="{HEIGHT}"/></clipPath>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>
  <g clip-path="url(#frame)">
    <image x="{MAP_X}" y="{MAP_Y}" width="{MAP_SIZE}" height="{MAP_SIZE}"
      xlink:href="data:image/jpeg;base64,{_map_square_b64(map_path)}"/>
    <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_SIZE}" height="{MAP_SIZE}" fill="{BACKGROUND}" fill-opacity="0.12"/>
    {_overlay()}
  </g>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#fade-x)"/>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#fade-y)"/>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#glow)"/>
  {_brand(font)}
</svg>"""


def main(argv: list[str] | None = None) -> int:
    """Render the banner PNG.

    Args:
        argv: Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT)
    args = parser.parse_args(argv)

    if not args.font.exists():
        parser.error(f"{args.font} not found; run `npm install` in site/ or pass --font")
    import cairosvg
    from PIL import Image

    svg = banner_svg(_Font(args.font), args.map)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=WIDTH)
    with Image.open(io.BytesIO(png)) as image:
        image.convert("RGB").save(args.output, optimize=True)
    print(f"wrote {args.output} ({args.output.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
