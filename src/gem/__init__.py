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
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import gem.constants as constants  # re-export so `gem.constants.hero_display()` works
from gem.batch import ParseResult, parse_many, parse_many_to_dataframe, parse_many_to_parquet
from gem.models import ChatEntry, ParsedMatch, ParsedPlayer

__version__ = "0.2.2"

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
    )


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
    "constants",
]
