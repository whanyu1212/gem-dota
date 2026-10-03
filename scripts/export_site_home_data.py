"""Export the data behind the docs site's home page figures.

The home page (``site/src/pages/index.astro``) shows real gem output: Table 1 is
one team's players, Figure 1 is gem's map model over the 7.41 map, and Figure 2
is the Radiant gold advantage by minute. This script writes them to a committed
snapshot, so building the site never parses a replay:

- ``site/src/data/home.json``: the match, its players, ``radiant_gold_adv``, and
  the map overlay (half line, river, lotus pools, every neutral camp) in the
  coordinates of a 1000-unit square;
- ``site/src/assets/home-map.jpg``: the plain map square the overlay sits on.

The overlay comes from ``map_constants.json`` and ``camp_zones.json`` and is
placed with the report maps' calibrated window (``MAP_XMIN``…``MAP_YMAX``), the
same projection as ``scripts/render_readme_banner.py``.

Usage (defaults to the TI2026 fixture 8856501050, the committed snapshot)::

    uv run python scripts/export_site_home_data.py [replay.dem]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import gem  # noqa: E402
from gem.catalog.map import load_camp_zones, load_map_constants  # noqa: E402
from gem.constants import hero_display  # noqa: E402
from gem.reports._formatting import MAP_XMAX, MAP_XMIN, MAP_YMAX, MAP_YMIN  # noqa: E402

# TI2026 match 8856501050: Radiant fell 47,262 gold behind and won, which makes
# a readable Figure 2. The committed snapshot is this match.
DEFAULT_REPLAY = REPO_ROOT / "tests" / "fixtures" / "opendota" / "8856501050.dem"
DEFAULT_DATA = REPO_ROOT / "site" / "src" / "data" / "home.json"
DEFAULT_MAP_IMAGE = REPO_ROOT / "site" / "src" / "assets" / "home-map.jpg"
SOURCE_MAP = REPO_ROOT / "assets" / "maps" / "Game_map_7.41.jpg"

#: The overlay's coordinate square, and the map image's size in pixels.
SIZE = 1000
IMAGE_PX = 1200


def _project(x: float, y: float) -> list[float]:
    fx = (x - MAP_XMIN) / (MAP_XMAX - MAP_XMIN)
    fy = 1.0 - (y - MAP_YMIN) / (MAP_YMAX - MAP_YMIN)
    return [round(fx * SIZE, 1), round(fy * SIZE, 1)]


def map_overlay() -> dict:
    """gem's regions and camps, projected onto the map square."""
    regions = load_map_constants()["regions"]
    camps = load_camp_zones()["camps"]
    return {
        "size": SIZE,
        "half_line": [_project(*point) for point in regions["half_line"]],
        "river": [_project(*point) for point in regions["river_outline"]],
        "lotus_radius": round(regions["lotus_radius"] / (MAP_XMAX - MAP_XMIN) * SIZE, 1),
        "lotus_pools": [_project(pool["x"], pool["y"]) for pool in regions["lotus_pools"].values()],
        "camps": [
            {"type": camp["type"], "at": _project(camp["center"]["x"], camp["center"]["y"])}
            for camp in camps
        ],
    }


def write_map_image(path: Path) -> None:
    """The centred square of the map (the report maps' window) as a JPEG."""
    from PIL import Image

    with Image.open(SOURCE_MAP) as image:
        side = image.height
        left = (image.width - side) // 2
        square = image.convert("RGB").crop((left, 0, left + side, side))
        square = square.resize((IMAGE_PX, IMAGE_PX), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    square.save(path, "JPEG", quality=85, optimize=True, progressive=True)


def match_snapshot(replay: Path) -> dict:
    """The match facts the home page shows."""
    match = gem.parse(replay)
    return {
        "match_id": match.match_id,
        "radiant_team": match.radiant_team_name,
        "dire_team": match.dire_team_name,
        "radiant_win": match.radiant_win,
        "radiant_score": match.radiant_score,
        "dire_score": match.dire_score,
        "duration_s": match.duration,
        "players": [
            {
                "hero": hero_display(player.hero_name),
                "team": "radiant" if player.team == 2 else "dire",
                "kills": player.kills,
                "deaths": player.deaths,
                "assists": player.assists,
                "net_worth": player.net_worth,
                "gold_per_min": player.gold_per_min,
            }
            for player in match.players
        ],
        "radiant_gold_adv": match.radiant_gold_adv,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("replay", nargs="?", type=Path, default=DEFAULT_REPLAY)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--map-image", type=Path, default=DEFAULT_MAP_IMAGE)
    args = parser.parse_args(argv)

    data = {"match": match_snapshot(args.replay), "map": map_overlay()}
    args.data.parent.mkdir(parents=True, exist_ok=True)
    args.data.write_text(json.dumps(data, indent=1) + "\n")
    write_map_image(args.map_image)
    print(f"Wrote {args.data.relative_to(REPO_ROOT)} and {args.map_image.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
