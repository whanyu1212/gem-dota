"""Match assembly — wires extractor outputs into a :class:`ParsedMatch`.

Takes the raw extractor state after a completed parse and builds the fully
populated :class:`ParsedMatch` returned by :func:`gem.parse`.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from gem.models import ParsedMatch

if TYPE_CHECKING:
    from gem.combat_aggregator import _CombatAggregator
    from gem.combatlog import CombatLogEntry
    from gem.extractors.courier import CourierExtractor
    from gem.extractors.draft import DraftExtractor
    from gem.extractors.objectives import ObjectivesExtractor
    from gem.extractors.players import PlayerExtractor
    from gem.extractors.wards import WardsExtractor
    from gem.models import ChatEntry
    from gem.parser import ReplayParser

# Lane position grid resolution in world units (7d)
_LANE_GRID = 64


def _radiant_win_from_ancient(combat_log: list[CombatLogEntry]) -> bool | None:
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


def build_parsed_match(
    parser: ReplayParser,
    player_ext: PlayerExtractor,
    obj_ext: ObjectivesExtractor,
    ward_ext: WardsExtractor,
    courier_ext: CourierExtractor,
    draft_ext: DraftExtractor,
    combat_agg: _CombatAggregator,
    all_entries: list[CombatLogEntry],
    chat_entries: list[ChatEntry],
) -> ParsedMatch:
    """Assemble a :class:`ParsedMatch` from extractor state after a completed parse.

    Handles radiant_win resolution (three-tier), per-player time series wiring,
    player name extraction, ward-to-player assignment, gold/XP advantage curves,
    and teamfight detection.

    Args:
        parser: Completed :class:`ReplayParser` instance.
        player_ext: Attached :class:`PlayerExtractor`.
        obj_ext: Attached :class:`ObjectivesExtractor`.
        ward_ext: Attached :class:`WardsExtractor`.
        courier_ext: Attached :class:`CourierExtractor`.
        draft_ext: Attached :class:`DraftExtractor` (already finalized).
        combat_agg: Populated :class:`_CombatAggregator`.
        all_entries: All :class:`CombatLogEntry` objects from the replay.
        chat_entries: All :class:`ChatEntry` objects from the replay.

    Returns:
        Fully populated :class:`ParsedMatch`.
    """
    from gem.combat_aggregator import _dedup_purchase_log
    from gem.extractors.teamfights import detect_teamfights

    # radiant_win resolution — three tiers in priority order:
    #   1. CDemoFileInfo.game_winner (set during parse, empty for HLTV replays)
    #   2. m_pGameRules.m_nGameWinner entity field (set post-parse in parser.py)
    #   3. Ancient DEATH in combat log — no API needed
    radiant_win = parser.radiant_win
    if radiant_win is None:
        radiant_win = _radiant_win_from_ancient(all_entries)

    match = ParsedMatch(
        match_id=parser.match_id,
        game_mode=parser.game_mode,
        leagueid=parser.leagueid,
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
            combat_agg._agg(pid).buyback_log.append(entry)

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

        agg = combat_agg.players.get(player_id)
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

        kda = player_ext.scoreboard.get(player_id)
        if kda is not None:
            pp.kills, pp.deaths, pp.assists = kda

        # Lane position heatmap (7d) — post-process existing snapshots
        lane_pos: defaultdict[str, int] = defaultdict(int)
        for snap in player_ext.snapshots:
            if snap.player_id != player_id or snap.x is None or snap.y is None:
                continue
            lane_pos[f"{int(snap.x) // _LANE_GRID}_{int(snap.y) // _LANE_GRID}"] += 1
        pp.lane_pos = lane_pos

    # Extract player names from CDOTA_PlayerResource entity.
    # Two field path variants: newer replays use m_vecPlayerData.{slot}.m_iszPlayerName,
    # older replays use m_iszPlayerNames.{slot}.
    # Reference: refs/manta/manta_test.go line ~703
    if parser.entity_manager is not None:
        pr = parser.entity_manager.find_by_class_name("CDOTA_PlayerResource")
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
    # Use total_earned fields (monotonically increasing) rather than spendable gold.
    # Compute the minimum series length so all 10 active players contribute to every bucket.
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
    hero_to_slot = {pp.hero_name: pp.player_id for pp in match.players if pp.hero_name}
    player_snaps: dict[int, Any] = {
        pid: [s for s in player_ext.snapshots if s.player_id == pid] for pid in range(10)
    }
    match.teamfights = detect_teamfights(
        all_entries,
        hero_to_slot=hero_to_slot,
        player_snapshots=player_snaps,
    )

    return match
