"""gem — Dota 2 Source 2 replay parser for DS/ML use.

Public API
----------
``parse(path)``
    Parse a replay and return a :class:`ParsedMatch`.

``parse_to_dataframe(path)``
    Parse a replay and return a dict of pandas DataFrames.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import gem.constants as constants  # re-export so `gem.constants.hero_display()` works
from gem.models import ChatEntry, ParsedMatch, ParsedPlayer

__version__ = "0.1.0"

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
    # Reference: examples/ward_smoke_rosh.py WardSmokeCollector
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


def parse_to_dataframe(path: str | Path) -> dict[str, pd.DataFrame]:
    """Parse a replay and return key data as pandas DataFrames.

    Convenience wrapper around :func:`parse` that converts the structured
    output into tabular form suitable for analysis.

    Args:
        path: Path to the ``.dem`` replay file.

    Returns:
        Dictionary with keys:
        - ``"players"``: one row per player per sample tick (wide format).
        - ``"positions"``: one row per ``(player, tick)`` with x/y coordinates.
        - ``"combat_log"``: one row per combat log entry.
        - ``"wards"``: one row per ward placement.
        - ``"objectives"``: one row per tower/barracks/roshan kill.
        - ``"chat"``: one row per chat message.
    """
    from gem.dataframes import build_dataframes

    return build_dataframes(parse(path))


# Re-export for convenience
__all__ = [
    "__version__",
    "parse",
    "parse_to_dataframe",
    "ParsedMatch",
    "ParsedPlayer",
    "ChatEntry",
    "constants",
]
