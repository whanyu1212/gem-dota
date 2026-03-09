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
from typing import TYPE_CHECKING, Any

from gem.models import ParsedMatch, ParsedPlayer

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
    from gem.extractors.objectives import ObjectivesExtractor
    from gem.extractors.players import PlayerExtractor
    from gem.extractors.wards import WardsExtractor
    from gem.parser import ReplayParser

    p = ReplayParser(path)
    player_ext = PlayerExtractor()
    obj_ext = ObjectivesExtractor()
    ward_ext = WardsExtractor()

    player_ext.attach(p)
    obj_ext.attach(p)
    ward_ext.attach(p)

    # Aggregate combat log entries per player
    _combat_aggregator = _CombatAggregator(player_ext)
    p.on_combat_log_entry(_combat_aggregator.on_entry)

    all_entries: list = []
    p.on_combat_log_entry(all_entries.append)

    p.parse()

    match = ParsedMatch(
        towers=obj_ext.tower_kills,
        barracks=obj_ext.barracks_kills,
        roshans=obj_ext.roshan_kills,
        wards=ward_ext.ward_events,
        combat_log=all_entries,
    )

    # Build per-player time series and overlay combat log aggregates
    for player_id in range(10):
        ts = player_ext.time_series(player_id)
        pp = match.players[player_id]
        pp.player_id = player_id
        pp.times = ts.ticks
        pp.gold_t = ts.gold_t
        pp.lh_t = ts.lh_t
        pp.dn_t = ts.dn_t
        pp.xp_t = ts.xp_t

        # Resolve hero name from snapshots
        for snap in player_ext.snapshots:
            if snap.player_id == player_id:
                pp.hero_name = snap.npc_name
                pp.team = snap.team
                break

        agg = _combat_aggregator.players.get(player_id)
        if agg is not None:
            pp.damage = agg.damage
            pp.damage_taken = agg.damage_taken
            pp.healing = agg.healing
            pp.ability_uses = agg.ability_uses
            pp.item_uses = agg.item_uses
            pp.gold_reasons = agg.gold_reasons
            pp.xp_reasons = agg.xp_reasons
            pp.kills_log = agg.kills_log
            pp.purchase_log = agg.purchase_log

    # Attach ward logs per player
    for ward in match.wards:
        if 0 <= ward.player_id < 10:
            pp = match.players[ward.player_id]
            if ward.ward_type == "observer":
                pp.obs_log.append(ward)
            else:
                pp.sen_log.append(ward)

    return match


def parse_to_dataframe(path: str | Path) -> dict[str, pd.DataFrame]:
    """Parse a replay and return key data as pandas DataFrames.

    Convenience wrapper around :func:`parse` that converts the structured
    output into tabular form suitable for analysis.

    Args:
        path: Path to the ``.dem`` replay file.

    Returns:
        Dictionary with keys:
        - ``"players"``: one row per player per sample tick (wide format).
        - ``"combat_log"``: one row per combat log entry.
        - ``"wards"``: one row per ward placement.
        - ``"objectives"``: one row per tower/barracks/roshan kill.
    """
    import pandas as pd

    match = parse(path)

    # --- players ---
    player_rows: list[dict] = []
    for pp in match.players:
        n = len(pp.times)
        for i in range(n):
            player_rows.append(
                {
                    "player_id": pp.player_id,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": pp.times[i],
                    "gold": pp.gold_t[i] if i < len(pp.gold_t) else 0,
                    "lh": pp.lh_t[i] if i < len(pp.lh_t) else 0,
                    "dn": pp.dn_t[i] if i < len(pp.dn_t) else 0,
                    "xp": pp.xp_t[i] if i < len(pp.xp_t) else 0,
                }
            )
    players_df = pd.DataFrame(player_rows)

    # --- combat_log ---
    from dataclasses import asdict

    combat_df = pd.DataFrame([asdict(e) for e in match.combat_log])

    # --- wards ---
    wards_df = pd.DataFrame([asdict(w) for w in match.wards]) if match.wards else pd.DataFrame()

    # --- objectives ---
    obj_rows: list[dict] = []
    for t in match.towers:
        obj_rows.append(
            {
                "type": "tower",
                "tick": t.tick,
                "team": t.team,
                "name": t.tower_name,
                "killer": t.killer,
            }
        )
    for b in match.barracks:
        obj_rows.append(
            {
                "type": "barracks",
                "tick": b.tick,
                "team": b.team,
                "name": b.barracks_name,
                "killer": b.killer,
            }
        )
    for r in match.roshans:
        obj_rows.append(
            {"type": "roshan", "tick": r.tick, "team": 0, "name": "roshan", "killer": r.killer}
        )
    objectives_df = pd.DataFrame(obj_rows)

    return {
        "players": players_df,
        "combat_log": combat_df,
        "wards": wards_df,
        "objectives": objectives_df,
    }


# ---------------------------------------------------------------------------
# Internal combat log aggregator
# ---------------------------------------------------------------------------


class _ParsedPlayerAgg:
    """Mutable accumulator for per-player combat log aggregates."""

    __slots__ = (
        "damage",
        "damage_taken",
        "healing",
        "ability_uses",
        "item_uses",
        "gold_reasons",
        "xp_reasons",
        "kills_log",
        "purchase_log",
    )

    def __init__(self) -> None:
        self.damage: dict[str, int] = {}
        self.damage_taken: dict[str, int] = {}
        self.healing: dict[str, int] = {}
        self.ability_uses: dict[str, int] = {}
        self.item_uses: dict[str, int] = {}
        self.gold_reasons: dict[str, int] = {}
        self.xp_reasons: dict[str, int] = {}
        self.kills_log: list = []
        self.purchase_log: list = []


class _CombatAggregator:
    """Aggregates combat log entries into per-player buckets.

    Uses the hero NPC-name → player_id mapping from ``PlayerExtractor``.
    """

    def __init__(self, player_ext: Any) -> None:
        self._player_ext = player_ext
        self.players: dict[int, _ParsedPlayerAgg] = {}

    def _agg(self, player_id: int) -> _ParsedPlayerAgg:
        if player_id not in self.players:
            self.players[player_id] = _ParsedPlayerAgg()
        return self.players[player_id]

    def _hero_to_pid(self, npc_name: str) -> int | None:
        entity = self._player_ext._heroes_by_npc.get(npc_name.lower())
        if entity is None:
            return None
        pid, ok = entity.get_int32("m_nPlayerID")
        if not ok:
            pid, ok = entity.get_int32("m_iPlayerID")
        if not ok or pid < 0:
            return None
        return pid // 2

    def on_entry(self, entry: Any) -> None:
        attacker_pid = self._hero_to_pid(entry.attacker_name) if entry.attacker_is_hero else None
        target_pid = self._hero_to_pid(entry.target_name) if entry.target_is_hero else None

        match entry.log_type:
            case "DAMAGE":
                if attacker_pid is not None:
                    agg = self._agg(attacker_pid)
                    agg.damage[entry.target_name] = (
                        agg.damage.get(entry.target_name, 0) + entry.value
                    )
                if target_pid is not None:
                    agg = self._agg(target_pid)
                    agg.damage_taken[entry.attacker_name] = (
                        agg.damage_taken.get(entry.attacker_name, 0) + entry.value
                    )
            case "HEAL":
                if attacker_pid is not None:
                    agg = self._agg(attacker_pid)
                    agg.healing[entry.target_name] = (
                        agg.healing.get(entry.target_name, 0) + entry.value
                    )
            case "ABILITY":
                if attacker_pid is not None and entry.inflictor_name:
                    agg = self._agg(attacker_pid)
                    agg.ability_uses[entry.inflictor_name] = (
                        agg.ability_uses.get(entry.inflictor_name, 0) + 1
                    )
            case "ITEM":
                if attacker_pid is not None and entry.inflictor_name:
                    agg = self._agg(attacker_pid)
                    agg.item_uses[entry.inflictor_name] = (
                        agg.item_uses.get(entry.inflictor_name, 0) + 1
                    )
            case "GOLD":
                if target_pid is not None:
                    agg = self._agg(target_pid)
                    reason = str(entry.gold_reason)
                    agg.gold_reasons[reason] = agg.gold_reasons.get(reason, 0) + entry.value
            case "XP":
                if target_pid is not None:
                    agg = self._agg(target_pid)
                    reason = str(entry.xp_reason)
                    agg.xp_reasons[reason] = agg.xp_reasons.get(reason, 0) + entry.value
            case "DEATH":
                if attacker_pid is not None:
                    self._agg(attacker_pid).kills_log.append(entry)
            case "PURCHASE":
                # OpenDota uses targetname as the buyer unit for PURCHASE events
                pid = attacker_pid if attacker_pid is not None else target_pid
                if pid is not None:
                    self._agg(pid).purchase_log.append(entry)


# Re-export for convenience
__all__ = ["parse", "parse_to_dataframe", "ParsedMatch", "ParsedPlayer"]
