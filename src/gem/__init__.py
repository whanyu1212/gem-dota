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

from gem.models import ChatEntry, ParsedMatch, ParsedPlayer

if TYPE_CHECKING:
    import pandas as pd

# Lane position grid resolution in world units (7d)
_LANE_GRID = 64


def _dedup_purchase_log(entries: list, first_snap_tick: int | None, sample_interval: int) -> list:
    """Deduplicate purchase log entries within the starting inventory window.

    The inventory snapshot and the combat log stream may both emit PURCHASE
    entries for the same item within the first sample window.  Outside that
    window, duplicate item purchases are legitimate (e.g. buying two separate
    Branches) and are kept as-is.

    Args:
        entries: Raw purchase log entries (unsorted).
        first_snap_tick: Tick of the player's first inventory snapshot, or
            ``None`` if no snapshot was taken.
        sample_interval: Width of the starting-item window in ticks.

    Returns:
        Deduplicated list sorted by tick.
    """
    if first_snap_tick is None:
        return sorted(entries, key=lambda e: e.tick)

    cutoff = first_snap_tick + sample_interval
    seen: set[tuple] = set()
    result = []
    for entry in sorted(entries, key=lambda e: e.tick):
        if entry.tick <= cutoff:
            key = (entry.tick, entry.value_name)
            if key in seen:
                continue
            seen.add(key)
        result.append(entry)
    return result


def _radiant_win_from_ancient(combat_log: list) -> bool | None:
    """Infer radiant_win from ancient DEATH events in the combat log.

    The destroying team is inferred from which ancient (fort) was killed:
    - ``npc_dota_badguys_fort`` dies → Radiant wins
    - ``npc_dota_goodguys_fort`` dies → Dire wins

    Args:
        combat_log: Full list of CombatLogEntry objects from the replay.

    Returns:
        True if Radiant won, False if Dire won, None if no ancient death found.
    """
    for e in combat_log:
        if e.log_type != "DEATH":
            continue
        if e.target_name == "npc_dota_badguys_fort":
            return True
        if e.target_name == "npc_dota_goodguys_fort":
            return False
    return None


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
    from gem.extractors.courier import CourierExtractor
    from gem.extractors.draft import DraftExtractor
    from gem.extractors.objectives import ObjectivesExtractor
    from gem.extractors.players import PlayerExtractor
    from gem.extractors.wards import WardsExtractor
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

    # Aggregate combat log entries per player
    _combat_aggregator = _CombatAggregator(player_ext)
    p.on_combat_log_entry(_combat_aggregator.on_entry)

    all_entries: list = []
    p.on_combat_log_entry(all_entries.append)

    # Collect chat messages (7e)
    chat_entries: list[ChatEntry] = []
    p.on_chat_message(chat_entries.append)

    p.parse()

    # Backfill hero names for draft events recorded before hero entities spawned.
    draft_ext.finalize()

    # radiant_win resolution — three tiers in priority order:
    #   1. CDemoFileInfo.game_winner (set during parse, empty for HLTV replays)
    #   2. m_pGameRules.m_nGameWinner entity field (set post-parse in parser.py)
    #   3. Ancient DEATH in combat log — no API needed
    radiant_win = p.radiant_win
    if radiant_win is None:
        radiant_win = _radiant_win_from_ancient(all_entries)

    match = ParsedMatch(
        match_id=p.match_id,
        game_mode=p.game_mode,
        leagueid=p.leagueid,
        radiant_win=radiant_win,
        towers=obj_ext.tower_kills,
        barracks=obj_ext.barracks_kills,
        roshans=obj_ext.roshan_kills,
        aegis_events=obj_ext.aegis_events,
        wards=ward_ext.ward_events,
        combat_log=all_entries,
        chat=chat_entries,
        courier_snapshots=courier_ext.snapshots,
        draft=draft_ext.draft_events,
    )

    # Post-process buybacks (7b).
    # For BUYBACK entries, entry.value = player slot (0-9).
    # Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java handleBuyback()
    for entry in all_entries:
        if entry.log_type != "BUYBACK":
            continue
        pid = entry.value
        if 0 <= pid < 10:
            _combat_aggregator._agg(pid).buyback_log.append(entry)

    # Build per-player time series and overlay combat log aggregates
    for player_id in range(10):
        ts = player_ext.time_series(player_id)
        pp = match.players[player_id]
        pp.player_id = player_id
        pp.times = ts.ticks
        pp.gold_t = ts.gold_t
        pp.net_worth_t = ts.net_worth_t
        pp.lh_t = ts.lh_t
        pp.dn_t = ts.dn_t
        pp.xp_t = ts.xp_t
        mts = player_ext.minute_time_series(player_id)
        pp.times_min = mts.ticks
        pp.gold_t_min = mts.gold_t
        pp.total_earned_gold_t_min = mts.total_earned_gold_t
        pp.total_earned_xp_t_min = mts.total_earned_xp_t
        pp.net_worth_t_min = mts.net_worth_t
        pp.lh_t_min = mts.lh_t
        pp.dn_t_min = mts.dn_t
        pp.xp_t_min = mts.xp_t
        pp.position_log = [
            (snap.tick, snap.x, snap.y)
            for snap in player_ext.snapshots
            if snap.player_id == player_id and snap.x is not None and snap.y is not None
        ]

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
            pp.purchase_log = _dedup_purchase_log(
                agg.purchase_log,
                player_ext.first_snapshot_tick.get(player_id),
                player_ext._sample_interval,
            )
            pp.runes_log = agg.runes_log
            pp.buyback_log = agg.buyback_log
            pp.stuns_dealt = agg.stuns_dealt

        # Lane position heatmap (7d) — post-process existing snapshots
        for snap in player_ext.snapshots:
            if snap.player_id != player_id or snap.x is None or snap.y is None:
                continue
            cell = f"{int(snap.x) // _LANE_GRID}_{int(snap.y) // _LANE_GRID}"
            pp.lane_pos[cell] = pp.lane_pos.get(cell, 0) + 1

    # Extract player names from CDOTA_PlayerResource entity.
    # Two field path variants: newer replays use m_vecPlayerData.{slot}.m_iszPlayerName,
    # older replays use m_iszPlayerNames.{slot}.
    # Reference: refs/manta/manta_test.go line ~703
    if p.entity_manager is not None:
        pr = p.entity_manager.find_by_class_name("CDOTA_PlayerResource")
        if pr is not None:
            for player_id in range(10):
                slot = f"{player_id:04d}"
                name, ok = pr.get_string(f"m_vecPlayerData.{slot}.m_iszPlayerName")
                if not ok or not name:
                    name, ok = pr.get_string(f"m_iszPlayerNames.{slot}")
                if ok and name:
                    match.players[player_id].player_name = name

    # Attach ward logs per player
    for ward in match.wards:
        if 0 <= ward.player_id < 10:
            pp = match.players[ward.player_id]
            if ward.ward_type == "observer":
                pp.obs_log.append(ward)
            else:
                pp.sen_log.append(ward)

    # Compute radiant_gold_adv / radiant_xp_adv per game-minute boundary.
    # For each minute index, sum gold_t_min (spendable gold) across all players:
    # Radiant players contribute positively, Dire players negatively.
    # Use the minimum series length across all players so all 10 contribute
    # to every minute bucket — prevents partial sums from skewing the curve.
    # Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java processAllPlayers()
    active_players = [
        pp for pp in match.players if pp.total_earned_gold_t_min and pp.total_earned_xp_t_min
    ]
    if active_players:
        n_minutes = min(
            min(len(pp.total_earned_gold_t_min), len(pp.total_earned_xp_t_min))
            for pp in active_players
        )
        gold_adv = [0] * n_minutes
        xp_adv = [0] * n_minutes
        for pp in active_players:
            sign = 1 if pp.team == 2 else -1  # 2=Radiant, 3=Dire
            for i in range(n_minutes):
                gold_adv[i] += sign * pp.total_earned_gold_t_min[i]
                xp_adv[i] += sign * (
                    pp.total_earned_xp_t_min[i] if i < len(pp.total_earned_xp_t_min) else 0
                )
        match.radiant_gold_adv = gold_adv
        match.radiant_xp_adv = xp_adv

    # Detect teamfights (Phase 9)
    from gem.extractors.teamfights import detect_teamfights

    hero_to_slot = {pp.hero_name: pp.player_id for pp in match.players if pp.hero_name}
    player_snaps = {
        pid: [s for s in player_ext.snapshots if s.player_id == pid] for pid in range(10)
    }
    match.teamfights = detect_teamfights(
        all_entries,
        hero_to_slot=hero_to_slot,
        player_snapshots=player_snaps,
    )

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
        - ``"positions"``: one row per ``(player, tick)`` with x/y coordinates.
        - ``"combat_log"``: one row per combat log entry.
        - ``"wards"``: one row per ward placement.
        - ``"objectives"``: one row per tower/barracks/roshan kill.
        - ``"chat"``: one row per chat message.
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

    # --- positions ---
    pos_rows: list[dict] = []
    for pp in match.players:
        for tick, x, y in pp.position_log:
            pos_rows.append(
                {
                    "player_id": pp.player_id,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": tick,
                    "x": x,
                    "y": y,
                }
            )
    positions_df = pd.DataFrame(pos_rows)

    # --- chat ---
    chat_df = pd.DataFrame([asdict(c) for c in match.chat]) if match.chat else pd.DataFrame()

    return {
        "players": players_df,
        "positions": positions_df,
        "combat_log": combat_df,
        "wards": wards_df,
        "objectives": objectives_df,
        "chat": chat_df,
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
        "runes_log",
        "buyback_log",
        "stuns_dealt",
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
        self.runes_log: list = []
        self.buyback_log: list = []
        self.stuns_dealt: float = 0.0


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

        # For GOLD/XP/PURCHASE in S2 replays, target_is_hero is False even for hero targets.
        # Fall back to name lookup unconditionally for those event types.
        if (
            target_pid is None
            and entry.target_name
            and entry.log_type in ("GOLD", "XP", "PURCHASE")
        ):
            target_pid = self._hero_to_pid(entry.target_name)

        # Accumulate stun duration dealt by the attacker (8d).
        if entry.stun_duration > 0 and attacker_pid is not None:
            self._agg(attacker_pid).stuns_dealt += entry.stun_duration

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
            case "PICKUP_RUNE":
                # entry.value = player slot (from CDOTAUserMsg_ChatEvent.playerid_1)
                pid = entry.value
                if 0 <= pid < 10:
                    self._agg(pid).runes_log.append(entry)
            case "BUYBACK":
                # Populated via post-processing in parse() after full name map is built.
                pass


# Re-export for convenience
__all__ = ["parse", "parse_to_dataframe", "ParsedMatch", "ParsedPlayer"]
