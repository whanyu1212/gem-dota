"""DataFrame conversion for :class:`ParsedMatch` output.

Converts the structured output of :func:`gem.parse` into pandas DataFrames
suitable for tabular analysis.
"""

from __future__ import annotations

from dataclasses import asdict
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

    from gem.results.models import ParsedMatch, ParsedPlayer


def _plain_row(item: Any) -> dict[str, Any]:
    """``asdict`` an item, demoting Enum field values to their raw value.

    Keeps DataFrame cells as primitives (e.g. ``"DAMAGE"`` rather than a
    ``CombatLogType`` member) so the exported schema stays backward compatible
    regardless of how internal fields are typed.
    """
    row = asdict(item)
    for key, value in row.items():
        if isinstance(value, Enum):
            row[key] = value.value
    return row


def _plain_rows(items: list[Any]) -> list[dict[str, Any]]:
    """``asdict`` each item with Enum field values demoted to primitives."""
    return [_plain_row(it) for it in items]


def _dataclass_rows(items: list[Any]) -> list[dict[str, Any]]:
    """Convert dataclass instances to dictionaries."""
    return [asdict(item) for item in items]


def _at(values: list[Any], index: int, default: Any = 0) -> Any:
    """Return a list value at ``index`` or ``default`` when absent."""
    return values[index] if index < len(values) else default


_COMBAT_LOG_COLUMNS = [
    "tick",
    "log_type",
    "attacker_name",
    "damage_source_name",
    "target_name",
    "inflictor_name",
    "value",
    "attacker_is_hero",
    "target_is_hero",
    "attacker_is_illusion",
    "target_is_illusion",
    "ability_level",
    "gold_reason",
    "xp_reason",
    "value_name",
    "damage_type",
    "stun_duration",
    "neutral_camp_type",
    "neutral_camp_team",
    "location_x",
    "location_y",
    "timestamp_s",
    "game_time_s",
    "will_reincarnate",
]

_PLAYER_COLUMNS = [
    "player_id",
    "player_name",
    "hero_name",
    "team",
    "tick",
    "gold",
    "total_earned_gold",
    "net_worth",
    "lh",
    "dn",
    "xp",
    "kills",
    "deaths",
    "assists",
    "stuns_dealt",
    "lane_role",
    "lane_last_hits",
    "lane_denies",
    "lane_total_gold",
    "lane_total_xp",
    "lane_efficiency_pct",
    "lane_gold_adv",
    "lane_xp_adv",
    "final_net_worth",
    "final_last_hits",
    "final_denies",
    "camps_stacked",
    "creeps_stacked",
    "obs_placed",
    "sen_placed",
    "rune_pickups",
    "tower_kills",
    "kda",
    "buyback_count",
    "is_radiant",
    "win",
    "kills_per_min",
    "gold_per_min",
    "xp_per_min",
    "total_gold",
    "total_xp",
    "hero_damage",
    "tower_damage",
    "hero_healing",
    "damage_physical",
    "damage_magical",
    "damage_pure",
    "damage_taken_physical",
    "damage_taken_magical",
    "damage_taken_pure",
    "damage",
    "damage_taken",
    "damage_inflictor",
    "damage_inflictor_received",
    "damage_targets",
    "ability_targets",
    "hero_hits",
    "max_hero_hit",
    "healing",
    "ability_uses",
    "item_uses",
    "purchase",
    "purchase_time",
    "first_purchase_time",
    "purchase_tpscroll",
    "purchase_ward_observer",
    "purchase_ward_sentry",
    "observer_uses",
    "sentry_uses",
    "observers_placed",
    "gold_reasons",
    "xp_reasons",
    "lane_pos",
]

_PLAYER_MINUTE_COLUMNS = [
    "player_id",
    "player_name",
    "hero_name",
    "team",
    "tick",
    "gold",
    "total_earned_gold",
    "total_earned_xp",
    "net_worth",
    "lh",
    "dn",
    "xp",
]

_POSITION_COLUMNS = ["player_id", "hero_name", "team", "tick", "x", "y"]

_WARD_COLUMNS = [
    "tick",
    "player_id",
    "placer",
    "ward_type",
    "team",
    "x",
    "y",
    "expires_tick",
    "killed_tick",
    "killer",
]

_OBJECTIVE_COLUMNS = [
    "type",
    "tick",
    "team",
    "name",
    "killer",
    "kill_number",
    "drops",
    "killer_player_id",
    "player_id",
    "event_type",
    "x",
    "y",
]

_OPENDOTA_OBJECTIVE_COLUMNS = [
    "time",
    "type",
    "key",
    "unit",
    "slot",
    "player_slot",
    "team",
    "killer",
]

_CHAT_COLUMNS = ["tick", "player_slot", "channel", "text"]

_MATCH_COLUMNS = [
    "match_id",
    "game_mode",
    "leagueid",
    "radiant_win",
    "game_start_tick",
    "game_end_tick",
    "tower_status_radiant",
    "tower_status_dire",
    "barracks_status_radiant",
    "barracks_status_dire",
    "parse_error",
    "truncated_at_tick",
]

_RADIANT_ADVANTAGE_COLUMNS = ["minute", "radiant_gold_adv", "radiant_xp_adv"]

_DRAFT_COLUMNS = ["tick", "slot_index", "hero_id", "hero_name", "is_pick", "team"]

_TEAMFIGHT_COLUMNS = [
    "start_tick",
    "end_tick",
    "last_death_tick",
    "deaths",
    "first_death_tick",
    "radiant_kills",
    "dire_kills",
    "winner",
    "centroid_x",
    "centroid_y",
    "centroid_n",
    "players",
]

_OPENDOTA_TEAMFIGHT_COLUMNS = ["start", "end", "last_death", "deaths", "players"]

_SMOKE_EVENT_COLUMNS = ["tick", "activator", "team", "smoked", "x", "y"]

_VISION_MODIFIER_COLUMNS = [
    "tick",
    "end_tick",
    "modifier_name",
    "target_name",
    "caster_name",
    "caster_team",
]

_COURIER_SNAPSHOT_COLUMNS = ["tick", "team", "state", "flying", "x", "y"]

_NEUTRAL_ITEM_FIND_COLUMNS = [
    "tick",
    "player_id",
    "item_ability_id",
    "item_key",
    "item_tier",
    "tier_item_count",
    "enhancement_ability_id",
    "enhancement_key",
    "enhancement_level",
    "trinket_level",
]

_PLAYER_LOG_COLUMNS = [*_COMBAT_LOG_COLUMNS, "player_id"]
_PLAYER_BUYBACK_LOG_COLUMNS = [*_PLAYER_LOG_COLUMNS, "cost", "net_worth"]


def _dataframe(rows: list[dict[str, Any]], columns: list[str]) -> pd.DataFrame:
    """Build a DataFrame with declared columns present in every row shape."""
    import pandas as pd

    df = pd.DataFrame(rows)
    extra_columns = [column for column in df.columns if column not in columns]
    return df.reindex(columns=[*columns, *extra_columns])


def _player_sample_base_fields(pp: ParsedPlayer, index: int) -> dict[str, Any]:
    """Build base identity, tick, and scoreboard fields for a player sample."""
    return {
        "player_id": pp.player_id,
        "player_name": pp.player_name,
        "hero_name": pp.hero_name,
        "team": pp.team,
        "tick": pp.times[index],
        "gold": _at(pp.gold_t, index),
        "total_earned_gold": _at(pp.total_earned_gold_t, index),
        "net_worth": _at(pp.net_worth_t, index),
        "lh": _at(pp.lh_t, index),
        "dn": _at(pp.dn_t, index),
        "xp": _at(pp.xp_t, index),
        "kills": pp.kills,
        "deaths": pp.deaths,
        "assists": pp.assists,
    }


def _player_lane_fields(pp: ParsedPlayer) -> dict[str, Any]:
    """Build lane-related fields for a dense player sample."""
    return {
        "stuns_dealt": pp.stuns_dealt,
        "lane_role": pp.lane_role,
        "lane_last_hits": pp.lane_last_hits,
        "lane_denies": pp.lane_denies,
        "lane_total_gold": pp.lane_total_gold,
        "lane_total_xp": pp.lane_total_xp,
        "lane_efficiency_pct": pp.lane_efficiency_pct,
        "lane_gold_adv": pp.lane_gold_adv,
        "lane_xp_adv": pp.lane_xp_adv,
    }


def _player_terminal_fields(pp: ParsedPlayer) -> dict[str, Any]:
    """Build end-of-game terminal scalar fields for a dense player sample."""
    return {
        # Per-player end-of-game terminal scalars (constant across the
        # player's rows). Named ``final_*`` to avoid shadowing the
        # per-tick ``net_worth``/``lh``/``dn`` columns above.
        "final_net_worth": pp.net_worth,
        "final_last_hits": pp.last_hits,
        "final_denies": pp.denies,
        "camps_stacked": pp.camps_stacked,
        "creeps_stacked": pp.creeps_stacked,
        "obs_placed": pp.obs_placed,
        "sen_placed": pp.sen_placed,
        "rune_pickups": pp.rune_pickups,
        "tower_kills": pp.tower_kills,
    }


def _player_computed_fields(pp: ParsedPlayer) -> dict[str, Any]:
    """Build computed rate/total fields for a dense player sample."""
    return {
        "kda": pp.kda,
        "buyback_count": pp.buyback_count,
        "is_radiant": pp.is_radiant,
        "win": pp.win,
        "kills_per_min": pp.kills_per_min,
        "gold_per_min": pp.gold_per_min,
        "xp_per_min": pp.xp_per_min,
        "total_gold": pp.total_gold,
        "total_xp": pp.total_xp,
    }


def _player_damage_fields(pp: ParsedPlayer) -> dict[str, Any]:
    """Build damage scalar and attribution fields for a dense player sample."""
    return {
        "hero_damage": pp.hero_damage,
        "tower_damage": pp.tower_damage,
        "hero_healing": pp.hero_healing,
        "damage_physical": pp.damage_by_type.get("physical", 0),
        "damage_magical": pp.damage_by_type.get("magical", 0),
        "damage_pure": pp.damage_by_type.get("pure", 0),
        "damage_taken_physical": pp.damage_taken_by_type.get("physical", 0),
        "damage_taken_magical": pp.damage_taken_by_type.get("magical", 0),
        "damage_taken_pure": pp.damage_taken_by_type.get("pure", 0),
        "damage": dict(pp.damage),
        "damage_taken": dict(pp.damage_taken),
        "damage_inflictor": dict(pp.damage_inflictor),
        "damage_inflictor_received": dict(pp.damage_inflictor_received),
        "damage_targets": {k: dict(v) for k, v in pp.damage_targets.items()},
        "ability_targets": {k: dict(v) for k, v in pp.ability_targets.items()},
        "hero_hits": dict(pp.hero_hits),
        "max_hero_hit": pp.max_hero_hit,
        "healing": dict(pp.healing),
        "ability_uses": dict(pp.ability_uses),
        "item_uses": dict(pp.item_uses),
    }


def _player_purchase_fields(pp: ParsedPlayer) -> dict[str, Any]:
    """Build purchase/ward-use fields for a dense player sample."""
    return {
        "purchase": dict(pp.purchase),
        "purchase_time": dict(pp.purchase_time),
        "first_purchase_time": dict(pp.first_purchase_time),
        "purchase_tpscroll": pp.purchase_tpscroll,
        "purchase_ward_observer": pp.purchase_ward_observer,
        "purchase_ward_sentry": pp.purchase_ward_sentry,
        "observer_uses": pp.observer_uses,
        "sentry_uses": pp.sentry_uses,
        "observers_placed": pp.observers_placed,
        "gold_reasons": dict(pp.gold_reasons),
        "xp_reasons": dict(pp.xp_reasons),
        "lane_pos": dict(pp.lane_pos),
    }


def _player_sample_row(pp: ParsedPlayer, index: int) -> dict[str, Any]:
    """Build one dense per-player sample row."""
    row = _player_sample_base_fields(pp, index)
    row.update(_player_lane_fields(pp))
    row.update(_player_terminal_fields(pp))
    row.update(_player_computed_fields(pp))
    row.update(_player_damage_fields(pp))
    row.update(_player_purchase_fields(pp))
    return row


def _player_minute_row(pp: ParsedPlayer, index: int) -> dict[str, Any]:
    """Build one per-player minute sample row."""
    return {
        "player_id": pp.player_id,
        "player_name": pp.player_name,
        "hero_name": pp.hero_name,
        "team": pp.team,
        "tick": pp.times_min[index],
        "gold": _at(pp.gold_t_min, index),
        "total_earned_gold": _at(pp.total_earned_gold_t_min, index),
        "total_earned_xp": _at(pp.total_earned_xp_t_min, index),
        "net_worth": _at(pp.net_worth_t_min, index),
        "lh": _at(pp.lh_t_min, index),
        "dn": _at(pp.dn_t_min, index),
        "xp": _at(pp.xp_t_min, index),
    }


def _player_log_rows(entries: list[Any], player_id: int) -> list[dict[str, Any]]:
    """Build per-player combat-log-derived rows with ``player_id`` appended."""
    rows: list[dict[str, Any]] = []
    for entry in entries:
        row = _plain_row(entry)
        row["player_id"] = player_id
        rows.append(row)
    return rows


def _player_buyback_rows(pp: ParsedPlayer) -> list[dict[str, Any]]:
    """Build buyback rows, including aligned estimated cost/net worth."""
    rows: list[dict[str, Any]] = []
    # Buyback rows carry the estimated cost / net worth from the structured
    # BuybackEvent (built 1:1 with buyback_log) so the DataFrame surfaces cost
    # too. Iterate buyback_log (the source of truth that a buyback happened)
    # and pull cost from the aligned BuybackEvent when present, so a row is
    # never dropped if buybacks is unset.
    for i, entry in enumerate(pp.buyback_log):
        row = _plain_row(entry)
        row["player_id"] = pp.player_id
        bb = pp.buybacks[i] if i < len(pp.buybacks) else None
        row["cost"] = bb.cost if bb is not None else None
        row["net_worth"] = bb.net_worth if bb is not None else None
        rows.append(row)
    return rows


def _player_table_rows(match: ParsedMatch) -> dict[str, list[dict[str, Any]]]:
    """Build all player-centric table rows."""
    rows: dict[str, list[dict[str, Any]]] = {
        "players": [],
        "players_minute": [],
        "player_kills_log": [],
        "player_purchase_log": [],
        "player_runes_log": [],
        "player_buyback_log": [],
    }

    for pp in match.players:
        rows["players"].extend(_player_sample_row(pp, i) for i in range(len(pp.times)))
        rows["players_minute"].extend(_player_minute_row(pp, i) for i in range(len(pp.times_min)))
        rows["player_kills_log"].extend(_player_log_rows(pp.kills_log, pp.player_id))
        rows["player_purchase_log"].extend(_player_log_rows(pp.purchase_log, pp.player_id))
        rows["player_runes_log"].extend(_player_log_rows(pp.runes_log, pp.player_id))
        rows["player_buyback_log"].extend(_player_buyback_rows(pp))

    return rows


def _tower_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build tower objective rows."""
    return [
        {
            "type": "tower",
            "tick": t.tick,
            "team": t.team,
            "name": t.tower_name,
            "killer": t.killer,
        }
        for t in match.towers
    ]


def _barracks_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build barracks objective rows."""
    return [
        {
            "type": "barracks",
            "tick": b.tick,
            "team": b.team,
            "name": b.barracks_name,
            "killer": b.killer,
        }
        for b in match.barracks
    ]


def _roshan_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build Roshan objective rows."""
    return [
        {
            "type": "roshan",
            "tick": r.tick,
            "team": 0,
            "name": "roshan",
            "killer": r.killer,
            "kill_number": r.kill_number,
            # Comma-joined raw drop tokens (e.g. "aegis,cheese,banner"). A
            # string keeps the cell filterable (df.drops.str.contains(...))
            # and round-trips cleanly to Parquet/CSV/JSON, unlike a list cell.
            "drops": ",".join(r.drops),
        }
        for r in match.roshans
    ]


def _tormentor_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build Tormentor objective rows."""
    return [
        {
            "type": "tormentor",
            "tick": tm.tick,
            "team": 0,
            "name": "npc_dota_miniboss",
            "killer": tm.killer,
            "killer_player_id": tm.killer_player_id,
            "kill_number": tm.kill_number,
        }
        for tm in match.tormentors
    ]


def _shrine_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build shrine objective rows."""
    return [
        {
            "type": "shrine",
            "tick": s.tick,
            "team": s.team,
            "name": "shrine_of_wisdom",
            "killer": "",
        }
        for s in match.shrines
    ]


def _aegis_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build Aegis objective rows."""
    return [
        {
            "type": "aegis",
            "tick": a.tick,
            "team": 0,
            "name": a.event_type,
            "killer": "",
            "player_id": a.player_id,
            "event_type": a.event_type,
        }
        for a in match.aegis_events
    ]


def _courier_death_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build courier death objective rows."""
    return [
        {
            "type": "courier_death",
            "tick": cd.tick,
            "team": 0,
            "name": "npc_dota_courier",
            "killer": cd.killer,
        }
        for cd in match.courier_deaths
    ]


def _banner_plant_objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build banner plant objective rows."""
    return [
        {
            "type": "banner_plant",
            "tick": bp.tick,
            "team": bp.team,
            "name": "roshans_banner",
            "killer": "",
            "player_id": bp.player_id,
            # World plant position (None when the banner unit carried no
            # readable coordinates); enables spatial filtering downstream.
            "x": bp.x,
            "y": bp.y,
        }
        for bp in match.banner_plants
    ]


def _objective_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build gem-native objective rows from per-type objective collections."""
    rows: list[dict[str, Any]] = []
    rows.extend(_tower_objective_rows(match))
    rows.extend(_barracks_objective_rows(match))
    rows.extend(_roshan_objective_rows(match))
    rows.extend(_tormentor_objective_rows(match))
    rows.extend(_shrine_objective_rows(match))
    rows.extend(_aegis_objective_rows(match))
    rows.extend(_courier_death_objective_rows(match))
    rows.extend(_banner_plant_objective_rows(match))
    return rows


def _position_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build player position rows."""
    rows: list[dict[str, Any]] = []
    for pp in match.players:
        for tick, x, y in pp.position_log:
            rows.append(
                {
                    "player_id": pp.player_id,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": tick,
                    "x": x,
                    "y": y,
                }
            )
    return rows


def _match_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build the single match metadata row."""
    return [
        {
            "match_id": match.match_id,
            "game_mode": match.game_mode,
            "leagueid": match.leagueid,
            "radiant_win": match.radiant_win,
            "game_start_tick": match.game_start_tick,
            "game_end_tick": match.game_end_tick,
            "tower_status_radiant": match.tower_status_radiant,
            "tower_status_dire": match.tower_status_dire,
            "barracks_status_radiant": match.barracks_status_radiant,
            "barracks_status_dire": match.barracks_status_dire,
            "parse_error": match.parse_error,
            "truncated_at_tick": match.truncated_at_tick,
        }
    ]


def _radiant_advantage_rows(match: ParsedMatch) -> list[dict[str, Any]]:
    """Build per-minute Radiant gold/XP advantage rows."""
    adv_len = max(len(match.radiant_gold_adv), len(match.radiant_xp_adv))
    return [
        {
            "minute": i,
            "radiant_gold_adv": _at(match.radiant_gold_adv, i),
            "radiant_xp_adv": _at(match.radiant_xp_adv, i),
        }
        for i in range(adv_len)
    ]


def build_dataframes(match: ParsedMatch) -> dict[str, pd.DataFrame]:
    """Convert a :class:`ParsedMatch` into a dict of pandas DataFrames.

    Args:
        match: Fully populated :class:`ParsedMatch`.

    Returns:
        Dictionary with tabular projections of match-level, player-level,
        and event-level data. Existing keys are preserved and extended with
        event tables such as ``smoke_events``, ``vision_modifiers``, and
        ``neutral_item_finds``.
    """
    player_rows = _player_table_rows(match)

    return {
        "players": _dataframe(player_rows["players"], _PLAYER_COLUMNS),
        "players_minute": _dataframe(player_rows["players_minute"], _PLAYER_MINUTE_COLUMNS),
        "positions": _dataframe(_position_rows(match), _POSITION_COLUMNS),
        "combat_log": _dataframe(_plain_rows(match.combat_log), _COMBAT_LOG_COLUMNS),
        "wards": _dataframe(_dataclass_rows(match.wards), _WARD_COLUMNS),
        "objectives": _dataframe(_objective_rows(match), _OBJECTIVE_COLUMNS),
        "opendota_objectives": _dataframe(match.objectives, _OPENDOTA_OBJECTIVE_COLUMNS),
        "chat": _dataframe(_dataclass_rows(match.chat), _CHAT_COLUMNS),
        "match": _dataframe(_match_rows(match), _MATCH_COLUMNS),
        "radiant_advantage": _dataframe(_radiant_advantage_rows(match), _RADIANT_ADVANTAGE_COLUMNS),
        "draft": _dataframe(_dataclass_rows(match.draft), _DRAFT_COLUMNS),
        "teamfights": _dataframe(_dataclass_rows(match.teamfights), _TEAMFIGHT_COLUMNS),
        "opendota_teamfights": _dataframe(
            _dataclass_rows(match.opendota_teamfights), _OPENDOTA_TEAMFIGHT_COLUMNS
        ),
        "smoke_events": _dataframe(_dataclass_rows(match.smoke_events), _SMOKE_EVENT_COLUMNS),
        "vision_modifiers": _dataframe(
            _dataclass_rows(match.vision_modifiers), _VISION_MODIFIER_COLUMNS
        ),
        "courier_snapshots": _dataframe(
            _dataclass_rows(match.courier_snapshots), _COURIER_SNAPSHOT_COLUMNS
        ),
        "neutral_item_finds": _dataframe(
            _dataclass_rows(match.neutral_item_finds), _NEUTRAL_ITEM_FIND_COLUMNS
        ),
        "player_kills_log": _dataframe(player_rows["player_kills_log"], _PLAYER_LOG_COLUMNS),
        "player_purchase_log": _dataframe(player_rows["player_purchase_log"], _PLAYER_LOG_COLUMNS),
        "player_runes_log": _dataframe(player_rows["player_runes_log"], _PLAYER_LOG_COLUMNS),
        "player_buyback_log": _dataframe(
            player_rows["player_buyback_log"], _PLAYER_BUYBACK_LOG_COLUMNS
        ),
    }
