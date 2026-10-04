"""HTML report generation for parsed Dota 2 matches.

Deprecated: the HTML report is retired and will be removed in gem 0.14. Its views
move to the recipes on the docs site (https://whanyu1212.github.io/gem-dota/cookbook/), each a question answered from the match's facts (HY-124).
"""

from gem._deprecation import warn_deprecated as _warn_deprecated
from gem.reports.asset_cache import (
    ReportAssetPaths,
    ReportAssetStatus,
    add_map_image,
    default_report_asset_dir,
    ensure_report_asset_dirs,
    fetch_match_icons,
    match_icon_shorts,
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
    "fetch_match_icons",
    "is_displayable_player_name",
    "match_icon_shorts",
    "report_asset_paths",
    "report_asset_status",
    "write_html_report",
]

_warn_deprecated(
    "gem.reports",
    alternative="the recipes on the docs site (https://whanyu1212.github.io/gem-dota/cookbook/)",
    stacklevel=2,
)
