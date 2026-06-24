"""HTML report generation for parsed Dota 2 matches."""

from gem.reports.asset_cache import (
    ReportAssetPaths,
    ReportAssetStatus,
    add_map_image,
    default_report_asset_dir,
    ensure_report_asset_dirs,
    report_asset_paths,
    report_asset_status,
)
from gem.reports.assets import ReportAssets
from gem.reports.builder import ReportOptions, build_html, build_html_report, write_html_report
from gem.reports.player_names import (
    apply_opendota_player_names,
    apply_opendota_player_names_from_path,
    display_player_name,
    is_displayable_player_name,
)

__all__ = [
    "ReportAssets",
    "ReportAssetPaths",
    "ReportAssetStatus",
    "ReportOptions",
    "add_map_image",
    "apply_opendota_player_names",
    "apply_opendota_player_names_from_path",
    "build_html",
    "build_html_report",
    "default_report_asset_dir",
    "display_player_name",
    "ensure_report_asset_dirs",
    "is_displayable_player_name",
    "report_asset_paths",
    "report_asset_status",
    "write_html_report",
]
