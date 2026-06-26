"""High-level public API for Dota 2 Source 2 replay parsing.

Public API
----------
``parse(path)``
    Parse a replay and return a :class:`ParsedMatch`.

``parse_to_dataframe(path)``
    Parse a replay and return a dict of pandas DataFrames.

``parse_many(source)``
    Parse multiple replays in parallel; return ``list[ParseResult]``.

``parse_many_to_dataframe(source)``
    Parse multiple replays and concatenate into per-table DataFrames.

``parse_many_to_parquet(source, output_dir)``
    Parse multiple replays and write each to its own parquet subdirectory.

``fetch_replay(match_id, out_dir)``
    Download and decompress a replay from OpenDota in one call.

``fetch_replay_url(match_id)``
    Fetch the replay download URL for a match from the OpenDota API.

``download_and_decompress(match_id, replay_url, out_dir)``
    Download and decompress a ``.dem.bz2`` to a ``.dem`` file.

``net_worth_at(player, tick)``
    Return the closest sampled net worth for a player at a tick.

``ward_vision_impact(ward, match)``
    Count distinct enemy heroes spotted by an observer ward.

``is_active_teamfight_participant(player_stats)``
    Check if a player actively participated in a teamfight.

``format_npc_name(name)``
    Convert an NPC entity name to a human-readable label.

``build_map_context_timeline(match, team, ...)``
    Build objective-aware map-control context buckets for farming analysis.

``score_camp_visit_context(...)``
    Score a camp visit as safe/contested/defensive/invade with drivers.

``build_rosh_conversions(match)``
    Summarize how each Roshan translated into fights, objectives, and map pressure.

``resolve_pick_team(event, players)``
    Resolve the team (Radiant/Dire) for a draft pick/ban event.

``gem.reports.build_html_report(match)``
    Build a self-contained HTML match report.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from importlib.metadata import PackageNotFoundError, version as _pkg_version
from pathlib import Path
from typing import TYPE_CHECKING, Any

import gem.catalog as catalog  # re-export so `gem.catalog.hero_display()` works
import gem.constants as constants  # re-export so `gem.constants.hero_display()` works
import gem.reports as reports  # re-export so `gem.reports.build_html_report()` works
from gem.analysis import (
    AbilityCast,
    CampVisitContext,
    MapContextBucket,
    RoshConversion,
    RoshTimelineEvent,
    VisionSource,
    ability_level_at_tick,
    build_map_context_timeline,
    build_rosh_conversions,
    estimate_vision,
    format_npc_name,
    group_ability_hits,
    heroes_near,
    is_active_teamfight_participant,
    net_worth_at,
    position_at_tick,
    score_camp_visit_context,
    teamfight_at_tick,
    ward_vision_impact,
)
from gem.catalog import hero_npc_name
from gem.extractors.draft import resolve_pick_team
from gem.extractors.teamfights import (
    OpenDotaTeamfight,
    OpenDotaTeamfightPlayer,
    detect_opendota_teamfights,
)
from gem.replays.batch import (
    ParseResult,
    parse_many,
    parse_many_to_dataframe,
    parse_many_to_parquet,
)
from gem.replays.fetch import (
    apply_api_rates,
    download_and_decompress,
    enrich_with_api_rates,
    fetch_opendota_match,
    fetch_replay,
    fetch_replay_url,
)
from gem.results.models import (
    BuybackEvent,
    ChatEntry,
    NeutralItemFoundEvent,
    ParsedMatch,
    ParsedPlayer,
    VisionModifierEvent,
)

try:
    __version__ = _pkg_version("gem-dota")
except PackageNotFoundError:  # editable/uninstalled checkout
    __version__ = "0.0.0+local"

if TYPE_CHECKING:
    import pandas as pd


def parse(path: str | Path) -> ParsedMatch:
    """Parse a Dota 2 replay file and return structured match data.

    Attaches all standard extractors (players, objectives, wards), runs the
    full parse, aggregates combat log entries per player, and assembles a
    :class:`ParsedMatch`.

    Args:
        path: Path to the ``.dem`` replay file.

    Returns:
        A :class:`ParsedMatch` with all extracted data populated.
    """
    from gem.combat.aggregator import _CombatAggregator
    from gem.combat.log import CombatLogEntry
    from gem.extractors.courier import CourierExtractor
    from gem.extractors.draft import DraftExtractor
    from gem.extractors.intervals import IntervalExtractor
    from gem.extractors.objectives import ObjectivesExtractor
    from gem.extractors.players import PlayerExtractor
    from gem.extractors.smoke_vision import SmokeExtractor, VisionModifierExtractor
    from gem.extractors.wards import WardsExtractor
    from gem.parser import ReplayParser
    from gem.results.assembly import build_parsed_match

    p = ReplayParser(path)
    player_ext = PlayerExtractor()
    obj_ext = ObjectivesExtractor()
    ward_ext = WardsExtractor()
    courier_ext = CourierExtractor()
    draft_ext = DraftExtractor()
    interval_ext = IntervalExtractor()

    player_ext.attach(p)
    interval_ext.attach(p)
    obj_ext.attach(p)
    ward_ext.attach(p)
    courier_ext.attach(p)
    draft_ext.attach(p)

    combat_agg = _CombatAggregator(player_ext)
    p.on_combat_log_entry(combat_agg.on_entry)

    all_entries: list[CombatLogEntry] = []
    p.on_combat_log_entry(all_entries.append)

    chat_entries: list[ChatEntry] = []
    p.on_chat_message(chat_entries.append)

    neutral_item_finds: list[NeutralItemFoundEvent] = []
    p.on_neutral_item_found(neutral_item_finds.append)

    # Smoke of Deceit and vision-granting modifiers are collected by dedicated
    # extractors (positions captured live at MODIFIER_ADD time; teams/centroids
    # back-filled from player snapshots in finalize() after parse). Both depend
    # on player_ext for hero positions and the NPC → team map.
    smoke_ext = SmokeExtractor(player_ext)
    vision_mod_ext = VisionModifierExtractor(player_ext)
    smoke_ext.attach(p)
    vision_mod_ext.attach(p)

    p.parse()
    draft_ext.finalize()
    ward_ext.finalize()
    smoke_events = smoke_ext.finalize()
    vision_modifier_events = vision_mod_ext.finalize()

    return build_parsed_match(
        parser=p,
        player_ext=player_ext,
        obj_ext=obj_ext,
        ward_ext=ward_ext,
        courier_ext=courier_ext,
        draft_ext=draft_ext,
        combat_agg=combat_agg,
        all_entries=all_entries,
        chat_entries=chat_entries,
        smoke_events=smoke_events,
        vision_modifier_events=vision_modifier_events,
        neutral_item_finds=neutral_item_finds,
        interval_ext=interval_ext,
    )


def find_player(match: ParsedMatch, hero: str) -> ParsedPlayer | None:
    """Look up a player by hero name.

    Accepts display names (``"Axe"``, ``"Anti-Mage"``), NPC names
    (``"npc_dota_hero_axe"``), or bare NPC suffixes (``"axe"``).

    Args:
        match: A parsed replay.
        hero: Hero display name, NPC name, or bare suffix.

    Returns:
        The matching :class:`ParsedPlayer`, or ``None`` if not found.
    """
    if hero.startswith("npc_dota_hero_"):
        npc = hero
    else:
        npc = hero_npc_name(hero) or f"npc_dota_hero_{hero.lower()}"
    return next((p for p in match.players if p.hero_name == npc), None)


def _to_json_compatible(value: Any) -> Any:
    """Recursively convert values to JSON-compatible Python types."""
    if is_dataclass(value):
        return {f.name: _to_json_compatible(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Mapping):
        return {str(k): _to_json_compatible(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_json_compatible(v) for v in value]
    return value


def to_dict(match: ParsedMatch) -> dict[str, Any]:
    """Convert a :class:`ParsedMatch` to a JSON-serializable dictionary."""
    return _to_json_compatible(match)


def to_json(match: ParsedMatch, *, indent: int | None = None, sort_keys: bool = False) -> str:
    """Serialize a :class:`ParsedMatch` to a JSON string."""
    return json.dumps(to_dict(match), indent=indent, sort_keys=sort_keys)


def parse_to_json(path: str | Path, *, indent: int | None = None, sort_keys: bool = False) -> str:
    """Parse a replay and return the result as JSON."""
    return to_json(parse(path), indent=indent, sort_keys=sort_keys)


def parse_to_dataframe(path: str | Path) -> dict[str, pd.DataFrame]:
    """Parse a replay and return tabular projections as pandas DataFrames.

    Convenience wrapper around :func:`parse` that converts the structured
    output into analysis-ready tables.

    Args:
        path: Path to the ``.dem`` replay file.

    Returns:
        Dictionary of DataFrames including (at minimum):
        - ``"players"``, ``"players_minute"``
        - ``"positions"``, ``"combat_log"``, ``"wards"``, ``"objectives"``, ``"chat"``
        - ``"match"``, ``"radiant_advantage"``
        - ``"draft"``, ``"teamfights"``, ``"smoke_events"``, ``"courier_snapshots"``
        - per-player event logs (kills/purchases/runes/buybacks)
    """
    from gem.results.dataframes import build_dataframes

    return build_dataframes(parse(path))


def to_parquet(match: ParsedMatch, output_dir: str | Path, *, index: bool = False) -> list[Path]:
    """Export DataFrame projections for a parsed match to parquet files.

    One parquet file is written per DataFrame key as ``<key>.parquet``.

    Args:
        match: Parsed replay output.
        output_dir: Directory to write parquet files into.
        index: Whether to include the DataFrame index in parquet output.

    Returns:
        List of parquet file paths written.
    """
    from gem.results.dataframes import build_dataframes

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for key, df in build_dataframes(match).items():
        file_path = out / f"{key}.parquet"
        try:
            df.to_parquet(file_path, index=index)
        except ImportError as exc:
            raise ImportError(
                "Parquet export requires an optional engine. Install 'pyarrow' or 'fastparquet'."
            ) from exc
        written.append(file_path)
    return written


def parse_to_parquet(
    path: str | Path, output_dir: str | Path, *, index: bool = False
) -> list[Path]:
    """Parse a replay and export DataFrame projections to parquet files."""
    return to_parquet(parse(path), output_dir, index=index)


# Re-export for convenience
__all__ = [
    "__version__",
    "parse",
    "to_dict",
    "to_json",
    "parse_to_json",
    "parse_to_dataframe",
    "to_parquet",
    "parse_to_parquet",
    "ParseResult",
    "parse_many",
    "parse_many_to_dataframe",
    "parse_many_to_parquet",
    "ParsedMatch",
    "ParsedPlayer",
    "OpenDotaTeamfight",
    "OpenDotaTeamfightPlayer",
    "ChatEntry",
    "NeutralItemFoundEvent",
    "BuybackEvent",
    "find_player",
    "hero_npc_name",
    "position_at_tick",
    "group_ability_hits",
    "AbilityCast",
    "teamfight_at_tick",
    "heroes_near",
    "ability_level_at_tick",
    "estimate_vision",
    "VisionSource",
    "VisionModifierEvent",
    "net_worth_at",
    "ward_vision_impact",
    "is_active_teamfight_participant",
    "detect_opendota_teamfights",
    "format_npc_name",
    "MapContextBucket",
    "CampVisitContext",
    "build_map_context_timeline",
    "score_camp_visit_context",
    "RoshTimelineEvent",
    "RoshConversion",
    "build_rosh_conversions",
    "resolve_pick_team",
    "catalog",
    "constants",
    "reports",
    "fetch_replay",
    "fetch_replay_url",
    "download_and_decompress",
    "fetch_opendota_match",
    "apply_api_rates",
    "enrich_with_api_rates",
]
