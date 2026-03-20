"""gem — Dota 2 Source 2 replay parser for DS/ML use.

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

``resolve_pick_team(event, players)``
    Resolve the team (Radiant/Dire) for a draft pick/ban event.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import gem.constants as constants  # re-export so `gem.constants.hero_display()` works
from gem.analysis import (
    AbilityCast,
    VisionSource,
    ability_level_at_tick,
    estimate_vision,
    format_npc_name,
    group_ability_hits,
    heroes_near,
    is_active_teamfight_participant,
    net_worth_at,
    position_at_tick,
    teamfight_at_tick,
    ward_vision_impact,
)
from gem.batch import ParseResult, parse_many, parse_many_to_dataframe, parse_many_to_parquet
from gem.constants import hero_npc_name
from gem.extractors.draft import resolve_pick_team
from gem.models import ChatEntry, ParsedMatch, ParsedPlayer, VisionModifierEvent
from gem.replay_fetch import download_and_decompress, fetch_replay, fetch_replay_url

__version__ = "0.2.6"

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
    from gem.combat_aggregator import _CombatAggregator
    from gem.combatlog import CombatLogEntry
    from gem.extractors.courier import CourierExtractor
    from gem.extractors.draft import DraftExtractor
    from gem.extractors.objectives import ObjectivesExtractor
    from gem.extractors.players import PlayerExtractor
    from gem.extractors.wards import WardsExtractor
    from gem.match_builder import build_parsed_match
    from gem.parser import ReplayParser

    p = ReplayParser(path)
    player_ext = PlayerExtractor()
    obj_ext = ObjectivesExtractor()
    ward_ext = WardsExtractor()
    courier_ext = CourierExtractor()
    draft_ext = DraftExtractor()

    player_ext.attach(p)
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

    # Smoke of Deceit collection — three combat log event types.
    # Position is captured live at MODIFIER_ADD time (when each hero actually
    # receives the buff) and averaged to give the group centroid.
    # Logic for SmokeEvent collection (item consumption + modifier arrival)
    from gem.models import SmokeEvent as _SmokeEvent
    from gem.models import VisionModifierEvent as _VisionModifierEvent

    # Vision modifier tracking — modifiers that reveal/grant vision of enemy heroes.
    # MODIFIER_ADD opens an event (end_tick=None); MODIFIER_REMOVE closes it.
    # The same hero can have the same modifier applied multiple times (e.g. refreshed
    # Dust), so we key by (modifier_name, target_name) and handle stacking by
    # maintaining a list (LIFO: remove closes the most recently opened open event).
    _VISION_MODIFIER_NAMES: frozenset[str] = frozenset(
        {
            # Slardar — Corrosive Haze (ultimate): true sight of target
            "modifier_slardar_amplify_damage",
            # Bounty Hunter — Track: true sight + gold bounty
            "modifier_bounty_hunter_track",
            # Dust of Appearance — item AoE reveal
            "modifier_item_dustofappearance",
            # Gem of True Sight — carrier aura (hero-level modifier on target)
            "modifier_item_gem_of_true_sight",
            "modifier_gem_active_truesight",
            # Oracle — False Promise: not a reveal but often comboed; skip
            # Zeus — Thundergods Wrath: global, not a per-hero modifier; skip
        }
    )
    vision_modifier_events: list[_VisionModifierEvent] = []
    # Track open (not-yet-closed) events: (modifier_name, target_name) → stack of events
    _open_vision_mods: dict[tuple[str, str], list[_VisionModifierEvent]] = {}

    def _on_vision_modifier_entry(entry: CombatLogEntry) -> None:
        if entry.log_type == "MODIFIER_ADD":
            mod = entry.inflictor_name
            if mod not in _VISION_MODIFIER_NAMES:
                return
            ev = _VisionModifierEvent(
                tick=entry.tick,
                end_tick=None,
                modifier_name=mod,
                target_name=entry.target_name,
                caster_name=entry.attacker_name,
                caster_team=0,  # back-filled after parse
            )
            vision_modifier_events.append(ev)
            key = (mod, entry.target_name)
            if key not in _open_vision_mods:
                _open_vision_mods[key] = []
            _open_vision_mods[key].append(ev)
        elif entry.log_type == "MODIFIER_REMOVE":
            mod = entry.inflictor_name
            if mod not in _VISION_MODIFIER_NAMES:
                return
            key = (mod, entry.target_name)
            stack = _open_vision_mods.get(key)
            if stack:
                stack.pop().end_tick = entry.tick
                if not stack:
                    del _open_vision_mods[key]

    p.on_combat_log_entry(_on_vision_modifier_entry)

    _pending_smokes: dict[str, _SmokeEvent] = {}  # activator npc → active event
    # Per-event accumulated positions: activator npc → list of (x, y) live coords
    _smoke_positions: dict[str, list[tuple[float, float]]] = {}
    smoke_events: list[_SmokeEvent] = []

    def _on_smoke_entry(entry: CombatLogEntry) -> None:
        if entry.log_type == "ITEM" and entry.inflictor_name == "item_smoke_of_deceit":
            new_ev = _SmokeEvent(tick=entry.tick, activator=entry.attacker_name, team=0)
            _pending_smokes[entry.attacker_name] = new_ev
            _smoke_positions[entry.attacker_name] = []
            smoke_events.append(new_ev)
        elif (
            entry.log_type == "MODIFIER_ADD"
            and entry.inflictor_name == "modifier_smoke_of_deceit"
            and entry.target_is_hero
        ):
            pending_ev = _pending_smokes.get(entry.attacker_name)
            if pending_ev is not None:
                pending_ev.smoked.append(entry.target_name)
                # Capture this hero's live position right now
                pos = player_ext.hero_pos(entry.target_name)
                if pos is not None:
                    _smoke_positions[entry.attacker_name].append(pos)
        elif (
            entry.log_type == "MODIFIER_REMOVE"
            and entry.inflictor_name == "modifier_smoke_of_deceit"
            and entry.target_is_hero
        ):
            pending_ev = _pending_smokes.get(entry.attacker_name)
            if pending_ev is not None and len(pending_ev.smoked) >= 1:
                _pending_smokes.pop(entry.attacker_name, None)

    p.on_combat_log_entry(_on_smoke_entry)

    p.parse()
    draft_ext.finalize()
    ward_ext.finalize()

    # Back-fill team; centroid x/y already collected live during MODIFIER_ADD
    _team_by_npc: dict[str, int] = {
        snap.npc_name: snap.team for snap in player_ext.snapshots if snap.team
    }

    for ev in smoke_events:
        ev.team = _team_by_npc.get(ev.activator, 0)
        positions = _smoke_positions.get(ev.activator, [])
        if positions:
            ev.x = sum(p[0] for p in positions) / len(positions)
            ev.y = sum(p[1] for p in positions) / len(positions)

    for vev in vision_modifier_events:
        vev.caster_team = _team_by_npc.get(vev.caster_name, 0)

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
    from gem.dataframes import build_dataframes

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
    from gem.dataframes import build_dataframes

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
    "ChatEntry",
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
    "format_npc_name",
    "resolve_pick_team",
    "constants",
    "fetch_replay",
    "fetch_replay_url",
    "download_and_decompress",
]
