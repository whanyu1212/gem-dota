"""DataFrame conversion for :class:`ParsedMatch` output.

Converts the structured output of :func:`gem.parse` into pandas DataFrames
suitable for tabular analysis.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

    from gem.models import ParsedMatch


def build_dataframes(match: ParsedMatch) -> dict[str, pd.DataFrame]:
    """Convert a :class:`ParsedMatch` into a dict of pandas DataFrames.

    Args:
        match: Fully populated :class:`ParsedMatch`.

    Returns:
        Dictionary with tabular projections of match-level, player-level,
        and event-level data. Existing keys are preserved:
        ``players``, ``positions``, ``combat_log``, ``wards``,
        ``objectives``, and ``chat``.
    """
    from dataclasses import asdict

    import pandas as pd

    # --- players (per sample tick) ---
    player_rows: list[dict] = []
    player_min_rows: list[dict] = []
    player_kills_rows: list[dict] = []
    player_purchase_rows: list[dict] = []
    player_runes_rows: list[dict] = []
    player_buyback_rows: list[dict] = []

    for pp in match.players:
        n = len(pp.times)
        for i in range(n):
            player_rows.append(
                {
                    "player_id": pp.player_id,
                    "player_name": pp.player_name,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": pp.times[i],
                    "gold": pp.gold_t[i] if i < len(pp.gold_t) else 0,
                    "total_earned_gold": (
                        pp.total_earned_gold_t[i] if i < len(pp.total_earned_gold_t) else 0
                    ),
                    "net_worth": pp.net_worth_t[i] if i < len(pp.net_worth_t) else 0,
                    "lh": pp.lh_t[i] if i < len(pp.lh_t) else 0,
                    "dn": pp.dn_t[i] if i < len(pp.dn_t) else 0,
                    "xp": pp.xp_t[i] if i < len(pp.xp_t) else 0,
                    "kills": pp.kills,
                    "deaths": pp.deaths,
                    "assists": pp.assists,
                    "stuns_dealt": pp.stuns_dealt,
                    "lane_role": pp.lane_role,
                    "lane_last_hits": pp.lane_last_hits,
                    "lane_denies": pp.lane_denies,
                    "lane_total_gold": pp.lane_total_gold,
                    "lane_total_xp": pp.lane_total_xp,
                    "lane_efficiency_pct": pp.lane_efficiency_pct,
                    "lane_gold_adv": pp.lane_gold_adv,
                    "lane_xp_adv": pp.lane_xp_adv,
                    "damage_physical": pp.damage_by_type.get("physical", 0),
                    "damage_magical": pp.damage_by_type.get("magical", 0),
                    "damage_pure": pp.damage_by_type.get("pure", 0),
                    "damage_taken_physical": pp.damage_taken_by_type.get("physical", 0),
                    "damage_taken_magical": pp.damage_taken_by_type.get("magical", 0),
                    "damage_taken_pure": pp.damage_taken_by_type.get("pure", 0),
                    "damage": dict(pp.damage),
                    "damage_taken": dict(pp.damage_taken),
                    "healing": dict(pp.healing),
                    "ability_uses": dict(pp.ability_uses),
                    "item_uses": dict(pp.item_uses),
                    "gold_reasons": dict(pp.gold_reasons),
                    "xp_reasons": dict(pp.xp_reasons),
                    "lane_pos": dict(pp.lane_pos),
                }
            )

        m = len(pp.times_min)
        for i in range(m):
            player_min_rows.append(
                {
                    "player_id": pp.player_id,
                    "player_name": pp.player_name,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": pp.times_min[i],
                    "gold": pp.gold_t_min[i] if i < len(pp.gold_t_min) else 0,
                    "total_earned_gold": (
                        pp.total_earned_gold_t_min[i] if i < len(pp.total_earned_gold_t_min) else 0
                    ),
                    "total_earned_xp": (
                        pp.total_earned_xp_t_min[i] if i < len(pp.total_earned_xp_t_min) else 0
                    ),
                    "net_worth": pp.net_worth_t_min[i] if i < len(pp.net_worth_t_min) else 0,
                    "lh": pp.lh_t_min[i] if i < len(pp.lh_t_min) else 0,
                    "dn": pp.dn_t_min[i] if i < len(pp.dn_t_min) else 0,
                    "xp": pp.xp_t_min[i] if i < len(pp.xp_t_min) else 0,
                }
            )

        for entry in pp.kills_log:
            row = asdict(entry)
            row["player_id"] = pp.player_id
            player_kills_rows.append(row)

        for entry in pp.purchase_log:
            row = asdict(entry)
            row["player_id"] = pp.player_id
            player_purchase_rows.append(row)

        for entry in pp.runes_log:
            row = asdict(entry)
            row["player_id"] = pp.player_id
            player_runes_rows.append(row)

        for entry in pp.buyback_log:
            row = asdict(entry)
            row["player_id"] = pp.player_id
            player_buyback_rows.append(row)

    players_df = pd.DataFrame(player_rows)
    players_min_df = pd.DataFrame(player_min_rows)

    # --- combat_log ---
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
            {
                "type": "roshan",
                "tick": r.tick,
                "team": 0,
                "name": "roshan",
                "killer": r.killer,
                "kill_number": r.kill_number,
            }
        )
    for tm in match.tormentors:
        obj_rows.append(
            {
                "type": "tormentor",
                "tick": tm.tick,
                "team": 0,
                "name": "npc_dota_miniboss",
                "killer": tm.killer,
                "killer_player_id": tm.killer_player_id,
                "kill_number": tm.kill_number,
            }
        )
    for s in match.shrines:
        obj_rows.append(
            {
                "type": "shrine",
                "tick": s.tick,
                "team": s.team,
                "name": "shrine_of_wisdom",
                "killer": "",
            }
        )
    for a in match.aegis_events:
        obj_rows.append(
            {
                "type": "aegis",
                "tick": a.tick,
                "team": 0,
                "name": a.event_type,
                "killer": "",
                "player_id": a.player_id,
                "event_type": a.event_type,
            }
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

    # --- match metadata ---
    match_df = pd.DataFrame(
        [
            {
                "match_id": match.match_id,
                "game_mode": match.game_mode,
                "leagueid": match.leagueid,
                "radiant_win": match.radiant_win,
                "game_start_tick": match.game_start_tick,
                "game_end_tick": match.game_end_tick,
            }
        ]
    )

    # --- radiant advantages ---
    adv_len = max(len(match.radiant_gold_adv), len(match.radiant_xp_adv))
    advantage_rows = [
        {
            "minute": i,
            "radiant_gold_adv": match.radiant_gold_adv[i] if i < len(match.radiant_gold_adv) else 0,
            "radiant_xp_adv": match.radiant_xp_adv[i] if i < len(match.radiant_xp_adv) else 0,
        }
        for i in range(adv_len)
    ]
    advantage_df = pd.DataFrame(advantage_rows)

    # --- list-based domains ---
    draft_df = pd.DataFrame([asdict(d) for d in match.draft]) if match.draft else pd.DataFrame()
    teamfights_df = (
        pd.DataFrame([asdict(tf) for tf in match.teamfights])
        if match.teamfights
        else pd.DataFrame()
    )
    smoke_df = (
        pd.DataFrame([asdict(se) for se in match.smoke_events])
        if match.smoke_events
        else pd.DataFrame()
    )
    courier_df = (
        pd.DataFrame([asdict(cs) for cs in match.courier_snapshots])
        if match.courier_snapshots
        else pd.DataFrame()
    )

    return {
        "players": players_df,
        "players_minute": players_min_df,
        "positions": positions_df,
        "combat_log": combat_df,
        "wards": wards_df,
        "objectives": objectives_df,
        "chat": chat_df,
        "match": match_df,
        "radiant_advantage": advantage_df,
        "draft": draft_df,
        "teamfights": teamfights_df,
        "smoke_events": smoke_df,
        "courier_snapshots": courier_df,
        "player_kills_log": pd.DataFrame(player_kills_rows),
        "player_purchase_log": pd.DataFrame(player_purchase_rows),
        "player_runes_log": pd.DataFrame(player_runes_rows),
        "player_buyback_log": pd.DataFrame(player_buyback_rows),
    }
