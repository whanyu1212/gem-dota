"""Generate a self-contained HTML match report from a Dota 2 replay.

Usage:
    python examples/match_report.py path/to/replay.dem [--output report.html]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from a source checkout without installing the package first.
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import gem
from gem.reports import ReportAssets, apply_opendota_player_names_from_path, write_html_report

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DEM = REPO_ROOT / "tests" / "fixtures" / "opendota" / "8868259993.dem"
DEFAULT_MAP = REPO_ROOT / "assets" / "maps" / "Game_map_7.40.jpg"


def _existing(path: Path) -> Path | None:
    return path if path.exists() else None


def main() -> None:
    """Parse a ``.dem`` replay and write a self-contained HTML report."""
    parser = argparse.ArgumentParser(
        description="Generate an HTML match report from a Dota 2 .dem replay file."
    )
    parser.add_argument("dem", nargs="?", help="Path to the .dem replay file")
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output HTML path (default: <dem_name>_report.html in the project root)",
    )
    parser.add_argument(
        "--map",
        default=None,
        help="Path to map image for report overlays (default: assets/maps/Game_map_7.40.jpg)",
    )
    parser.add_argument(
        "--asset-dir",
        default=None,
        help="Report asset cache root (default: GEM_REPORT_ASSET_DIR or the user cache)",
    )
    args = parser.parse_args()

    dem_path = Path(args.dem) if args.dem else DEFAULT_DEM
    output_path = Path(args.output) if args.output else REPO_ROOT / f"{dem_path.stem}_report.html"
    map_path = Path(args.map) if args.map else DEFAULT_MAP

    print(f"Parsing {dem_path} ...")
    match = gem.parse(dem_path)
    opendota_path = dem_path.with_suffix(".opendota.json")
    if opendota_path.exists():
        apply_opendota_player_names_from_path(match, opendota_path)
        print(f"Player names loaded: {opendota_path}")

    assets = ReportAssets.auto(
        root=Path(args.asset_dir) if args.asset_dir else None,
        fallback_map=map_path,
    )
    if args.map:
        assets = ReportAssets(
            map_image=_existing(map_path),
            hero_icon_dir=assets.hero_icon_dir,
            item_icon_dir=assets.item_icon_dir,
        )
    if assets.map_image:
        print(f"Map image loaded: {assets.map_image}")
    else:
        print(f"Map image not found at {map_path}; map-backed sections will render without it.")
    if not assets.hero_icon_dir or not assets.item_icon_dir:
        print(
            "Icon cache is incomplete; the report will use hero/item names instead. "
            "For icon visuals, run `python -m gem reports assets download --icons`."
        )

    written = write_html_report(match, output_path, assets=assets)
    print(f"Report written to: {written}")


if __name__ == "__main__":
    main()
