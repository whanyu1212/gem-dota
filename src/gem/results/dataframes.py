"""DataFrame conversion for :class:`ParsedMatch` output.

Converts the structured output of :func:`gem.parse` into flat pandas
DataFrames for tabular and cross-match analysis. The default (core) tables
hold only primitive cells and carry a leading ``match_id`` column so they can
be concatenated across replays. Nested post-parse analysis records are
available as opt-in groups; their full-fidelity form is the dataclass/JSON
output.

Reference: odota/parser CreateParsedDataBlob.java (pinned revision in
CLAUDE.md) for the OpenDota-compatible per-player field names.
"""

from __future__ import annotations

import functools
import json
import types
from collections.abc import Iterable
from dataclasses import asdict, fields
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal, Union, get_args, get_origin, get_type_hints

if TYPE_CHECKING:
    import pandas as pd

    from gem.results.models import ParsedMatch, ParsedPlayer

# Nullable pandas dtypes. Every table column is cast to one of these, so a
# column keeps the same dtype (and Parquet type) whether the match leaves it
# empty, all-missing, or fully populated.
_INT = "Int64"
_FLOAT = "Float64"
_BOOL = "boolean"
_STR = "string"

#: Tables returned by :func:`build_dataframes` by default.
CORE_TABLES: tuple[str, ...] = (
    "match",
    "player_summary",
    "player_timeseries",
    "players_minute",
    "player_breakdowns",
    "positions",
    "radiant_advantage",
    "combat_log",
    "wards",
    "objectives",
    "chat",
    "draft",
    "teamfights",
    "teamfight_players",
    "smoke_events",
    "smoke_members",
    "courier_snapshots",
    "neutral_item_finds",
    "hero_visibility_events",
    "entity_visibility",
    "vision_modifiers",
    "vision_modifier_pairing_issues",
    "player_kills_log",
    "player_purchase_log",
    "player_runes_log",
    "player_buyback_log",
)

#: Opt-in table groups, selected with ``build_dataframes(match, include=[...])``.
OPTIONAL_GROUPS: dict[str, tuple[str, ...]] = {
    "analysis": (
        "teamfight_positioning",
        "roshan_conversions",
        "roshan_conversion_fights",
        "smoke_fight_insights",
        "smoke_fight_members",
        "smoke_fight_followups",
        "farming_routes",
        "farming_route_segments",
        "farming_route_points",
        "farming_context_tags",
    ),
    "opendota": (
        "opendota_objectives",
        "opendota_teamfights",
    ),
}

# Per-player scalar fields exported once per player in ``player_summary``.
_PLAYER_SUMMARY_FIELDS: tuple[str, ...] = (
    "player_id",
    "player_name",
    "hero_name",
    "hero_id",
    "steam_id",
    "account_id",
    "team",
    "is_radiant",
    "win",
    "level",
    "kills",
    "deaths",
    "assists",
    "kda",
    "kills_per_min",
    "last_hits",
    "denies",
    "net_worth",
    "gold_per_min",
    "xp_per_min",
    "total_gold",
    "total_xp",
    "gold_spent",
    "hero_damage",
    "tower_damage",
    "hero_healing",
    "stuns_dealt",
    "teamfight_participation",
    "firstblood_claimed",
    "lane_role",
    "lane_last_hits",
    "lane_denies",
    "lane_total_gold",
    "lane_total_xp",
    "lane_efficiency_pct",
    "lane_gold_adv",
    "lane_xp_adv",
    "camps_stacked",
    "creeps_stacked",
    "obs_placed",
    "sen_placed",
    "observers_placed",
    "observer_uses",
    "sentry_uses",
    "purchase_tpscroll",
    "purchase_ward_observer",
    "purchase_ward_sentry",
    "rune_pickups",
    "tower_kills",
    "roshan_kills",
    "ancient_kills",
    "neutral_kills",
    "lane_kills",
    "courier_kills",
    "observer_kills",
    "sentry_kills",
    "buyback_count",
    "life_state_dead",
    "aghanims_scepter",
    "aghanims_shard",
    "moonshard",
)

# Per-player dict fields exported in long form in ``player_breakdowns``.
# Two-level ``outer -> {inner: value}`` dicts fill the ``subkey`` column.
_PLAYER_BREAKDOWN_FIELDS: tuple[str, ...] = (
    "damage",
    "damage_taken",
    "damage_inflictor",
    "damage_inflictor_received",
    "damage_targets",
    "ability_targets",
    "hero_hits",
    "healing",
    "killed",
    "ability_uses",
    "item_uses",
    "purchase",
    "purchase_time",
    "first_purchase_time",
    "gold_reasons",
    "xp_reasons",
    "lane_pos",
)

# ``TeamfightPlayer`` dict fields left out of ``teamfight_players``.
_TEAMFIGHT_PLAYER_DICTS: frozenset[str] = frozenset({"ability_uses", "item_uses"})


def build_dataframes(match: ParsedMatch, *, include: Iterable[str] = ()) -> dict[str, pd.DataFrame]:
    """Convert a :class:`ParsedMatch` into a dict of flat pandas DataFrames.

    Every table starts with a ``match_id`` column (``0`` when the replay does
    not carry one). Tables contain only primitive cells: list-valued fields
    are joined with ``";"`` and per-player dict fields are exported in long
    form in ``player_breakdowns``. Every column has a fixed nullable dtype
    (``Int64``, ``Float64``, ``boolean``, or ``string``) taken from the source
    dataclass type hints or the table's declared schema, so a table has the
    same columns and Parquet schema for every match, even an empty one.
    Missing values are ``pd.NA``.

    Args:
        match: Fully populated :class:`ParsedMatch`.
        include: Optional table groups to add (see :data:`OPTIONAL_GROUPS`).
            ``"analysis"`` runs the post-parse farming, smoke-fight, Roshan
            conversion, and teamfight-positioning analyses and flattens them;
            ``"opendota"`` adds the OpenDota-shaped objective and teamfight
            views. A single group name may be passed as a plain string.

    Returns:
        Dictionary mapping table name to DataFrame: every name in
        :data:`CORE_TABLES`, plus the tables of each requested group.

    Raises:
        ValueError: If ``include`` names an unknown group.
    """
    groups = _resolve_include(include)

    tables = _build_core_tables(match)
    if "analysis" in groups:
        tables.update(_build_analysis_tables(match))
    if "opendota" in groups:
        tables.update(_build_opendota_tables(match))

    import pandas as pd

    for df in tables.values():
        if "match_id" not in df.columns:
            df.insert(0, "match_id", pd.Series(match.match_id, index=df.index, dtype=_INT))
    return tables


def _resolve_include(include: Iterable[str]) -> set[str]:
    groups = {include} if isinstance(include, str) else set(include)
    unknown = groups - OPTIONAL_GROUPS.keys()
    if unknown:
        raise ValueError(
            f"Unknown DataFrame group(s) {sorted(unknown)}; "
            f"expected any of {sorted(OPTIONAL_GROUPS)}"
        )
    return groups


def _plain_row(item: Any) -> dict:
    """``asdict`` an item, demoting Enum field values to their raw value.

    Keeps DataFrame cells as primitives (e.g. ``"DAMAGE"`` rather than a
    ``CombatLogType`` member) so the exported schema stays backward
    compatible regardless of how internal fields are typed.
    """
    row = asdict(item)
    for key, value in row.items():
        if isinstance(value, Enum):
            row[key] = value.value
    return row


def _plain_rows(items: list) -> list[dict]:
    """``asdict`` each item with Enum field values demoted to primitives."""
    return [_plain_row(it) for it in items]


def _join(values: Iterable[Any]) -> str:
    """Join a list-valued field into one ``";"``-separated string cell."""
    return ";".join(str(value) for value in values)


def _hint_dtype(hint: Any) -> str:
    """Map a dataclass field annotation onto its nullable pandas dtype.

    ``X | None`` maps like ``X``, an Enum like its member values, a
    ``Literal`` like its values, and a list/tuple to a string because the
    tables export list-valued fields ``";"``-joined.
    """
    origin = get_origin(hint)
    if origin is Union or origin is types.UnionType:
        members = [arg for arg in get_args(hint) if arg is not type(None)]
        if len(members) == 1:
            return _hint_dtype(members[0])
    elif origin is Literal:
        return _hint_dtype(type(get_args(hint)[0]))
    elif origin in (list, tuple):
        return _STR
    elif isinstance(hint, type):
        if issubclass(hint, Enum):
            return _hint_dtype(type(next(iter(hint)).value))
        # bool subclasses int, so it must be tested first.
        if issubclass(hint, bool):
            return _BOOL
        if issubclass(hint, int):
            return _INT
        if issubclass(hint, float):
            return _FLOAT
        if issubclass(hint, str):
            return _STR
    raise TypeError(f"No DataFrame dtype for field annotation {hint!r}")


@functools.cache
def _type_hints(cls: type) -> dict[str, Any]:
    return get_type_hints(cls)


def _field_dtypes(
    cls: type, names: Iterable[str] | None = None, *, exclude: Iterable[str] = ()
) -> dict[str, str]:
    """Column dtypes for dataclass fields, derived from the type hints.

    Args:
        cls: Source dataclass.
        names: Fields to include, in column order. Defaults to every field in
            declaration order.
        exclude: Fields to leave out when ``names`` is omitted.

    Returns:
        Mapping of field name to nullable pandas dtype.
    """
    hints = _type_hints(cls)
    if names is None:
        skipped = set(exclude)
        names = [item.name for item in fields(cls) if item.name not in skipped]
    return {name: _hint_dtype(hints[name]) for name in names}


def _typed_frame(rows: list[dict[str, Any]], schema: dict[str, str]) -> pd.DataFrame:
    """Build a DataFrame with exactly ``schema``'s columns and dtypes."""
    import pandas as pd

    return pd.DataFrame(rows, columns=list(schema)).astype(schema)


def _player_summary_row(pp: ParsedPlayer) -> dict[str, Any]:
    row: dict[str, Any] = {name: getattr(pp, name) for name in _PLAYER_SUMMARY_FIELDS}
    for kind in ("physical", "magical", "pure"):
        row[f"damage_{kind}"] = pp.damage_by_type.get(kind, 0)
        row[f"damage_taken_{kind}"] = pp.damage_taken_by_type.get(kind, 0)
    hit = pp.max_hero_hit or {}
    row["max_hero_hit_value"] = hit.get("value")
    row["max_hero_hit_inflictor"] = hit.get("inflictor")
    row["max_hero_hit_target"] = hit.get("key")
    row["max_hero_hit_time"] = hit.get("time")
    return row


def _player_breakdown_rows(pp: ParsedPlayer) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stat in _PLAYER_BREAKDOWN_FIELDS:
        for key, value in getattr(pp, stat).items():
            if isinstance(value, dict):
                for subkey, inner in value.items():
                    rows.append(
                        {
                            "player_id": pp.player_id,
                            "stat": stat,
                            "key": str(key),
                            "subkey": str(subkey),
                            "value": inner,
                        }
                    )
            else:
                rows.append(
                    {
                        "player_id": pp.player_id,
                        "stat": stat,
                        "key": str(key),
                        "subkey": None,
                        "value": value,
                    }
                )
    return rows


def _build_core_tables(match: ParsedMatch) -> dict[str, pd.DataFrame]:
    from gem.combat.log import CombatLogEntry
    from gem.extractors.courier import CourierSnapshot
    from gem.extractors.draft import DraftEvent
    from gem.extractors.teamfights import Teamfight, TeamfightPlayer
    from gem.extractors.wards import WardEvent
    from gem.results.models import (
        BuybackEvent,
        ChatEntry,
        EntityVisibilityEvent,
        HeroVisibilityEvent,
        NeutralItemFoundEvent,
        ParsedMatch,
        ParsedPlayer,
        SmokeEvent,
        SmokeParticipant,
        VisionModifierEvent,
        VisionModifierPairingIssue,
    )

    player_identity = _field_dtypes(ParsedPlayer, ("player_id", "player_name", "hero_name", "team"))
    player_series = dict.fromkeys(
        ("gold", "total_earned_gold", "total_earned_xp", "net_worth", "lh", "dn", "xp"), _INT
    )
    combat_log_schema = _field_dtypes(CombatLogEntry)

    # --- players: one summary row, per-tick samples, long-form breakdowns ---
    summary_rows: list[dict] = []
    breakdown_rows: list[dict] = []
    player_rows: list[dict] = []
    player_min_rows: list[dict] = []
    player_kills_rows: list[dict] = []
    player_purchase_rows: list[dict] = []
    player_runes_rows: list[dict] = []
    player_buyback_rows: list[dict] = []

    for pp in match.players:
        summary_rows.append(_player_summary_row(pp))
        breakdown_rows.extend(_player_breakdown_rows(pp))

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
                    "total_earned_xp": (
                        pp.total_earned_xp_t[i] if i < len(pp.total_earned_xp_t) else 0
                    ),
                    "net_worth": pp.net_worth_t[i] if i < len(pp.net_worth_t) else 0,
                    "lh": pp.lh_t[i] if i < len(pp.lh_t) else 0,
                    "dn": pp.dn_t[i] if i < len(pp.dn_t) else 0,
                    "xp": pp.xp_t[i] if i < len(pp.xp_t) else 0,
                }
            )

        m = len(pp.times_min)
        for i in range(m):
            game_time_s = pp.game_times_min[i] if i < len(pp.game_times_min) else None
            player_min_rows.append(
                {
                    "player_id": pp.player_id,
                    "player_name": pp.player_name,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": pp.times_min[i],
                    "game_time_s": game_time_s,
                    "minute": game_time_s // 60 if game_time_s is not None else None,
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
            row = _plain_row(entry)
            row["player_id"] = pp.player_id
            player_kills_rows.append(row)

        for entry in pp.purchase_log:
            row = _plain_row(entry)
            row["player_id"] = pp.player_id
            player_purchase_rows.append(row)

        for entry in pp.runes_log:
            row = _plain_row(entry)
            row["player_id"] = pp.player_id
            player_runes_rows.append(row)

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
            player_buyback_rows.append(row)

    summary_schema = {
        **_field_dtypes(ParsedPlayer, _PLAYER_SUMMARY_FIELDS),
        **{f"damage_{kind}": _INT for kind in ("physical", "magical", "pure")},
        **{f"damage_taken_{kind}": _INT for kind in ("physical", "magical", "pure")},
        "max_hero_hit_value": _INT,
        "max_hero_hit_inflictor": _STR,
        "max_hero_hit_target": _STR,
        # Game seconds, or the float combat-log timestamp when that is missing.
        "max_hero_hit_time": _FLOAT,
    }
    player_summary_df = _typed_frame(summary_rows, summary_schema)
    player_timeseries_df = _typed_frame(
        player_rows, {**player_identity, "tick": _INT, **player_series}
    )
    player_breakdowns_df = _typed_frame(
        breakdown_rows,
        {"player_id": _INT, "stat": _STR, "key": _STR, "subkey": _STR, "value": _INT},
    )
    players_min_df = _typed_frame(
        player_min_rows,
        {**player_identity, "tick": _INT, "game_time_s": _INT, "minute": _INT, **player_series},
    )

    # --- combat_log ---
    combat_df = _typed_frame(_plain_rows(match.combat_log), combat_log_schema)

    # --- wards ---
    wards_df = _typed_frame([asdict(w) for w in match.wards], _field_dtypes(WardEvent))

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
                "killer_source": t.killer_source,
                "killer_team": t.killer_team,
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
                "killer_source": b.killer_source,
                "killer_team": b.killer_team,
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
                "killer_source": r.killer_source,
                "killer_team": r.killer_team,
                "kill_number": r.kill_number,
                # Comma-joined raw drop tokens (e.g. "aegis,cheese,banner"). A
                # string keeps the cell filterable (df.drops.str.contains(...))
                # and round-trips cleanly to Parquet/CSV/JSON, unlike a list cell.
                "drops": ",".join(r.drops),
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
                "killer_team": tm.killer_team,
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
    for cd in match.courier_deaths:
        obj_rows.append(
            {
                "type": "courier_death",
                "tick": cd.tick,
                "team": 0,
                "name": "npc_dota_courier",
                "killer": cd.killer,
            }
        )
    for bp in match.banner_plants:
        obj_rows.append(
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
        )
    # Union of every objective row's columns; each row type fills a subset.
    objectives_df = _typed_frame(
        obj_rows,
        {
            "type": _STR,
            "tick": _INT,
            "team": _INT,
            "name": _STR,
            "killer": _STR,
            "killer_source": _STR,
            "killer_team": _INT,
            "kill_number": _INT,
            "drops": _STR,
            "killer_player_id": _INT,
            "player_id": _INT,
            "event_type": _STR,
            "x": _FLOAT,
            "y": _FLOAT,
        },
    )

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
    positions_df = _typed_frame(
        pos_rows,
        {
            **_field_dtypes(ParsedPlayer, ("player_id", "hero_name", "team")),
            "tick": _INT,
            "x": _FLOAT,
            "y": _FLOAT,
        },
    )

    # --- chat ---
    chat_df = _typed_frame([asdict(c) for c in match.chat], _field_dtypes(ChatEntry))

    # --- match metadata ---
    match_schema = _field_dtypes(
        ParsedMatch,
        (
            "match_id",
            "game_mode",
            "leagueid",
            "radiant_win",
            "game_start_tick",
            "game_end_tick",
            "post_game_tick",
            "tower_status_radiant",
            "tower_status_dire",
            "barracks_status_radiant",
            "barracks_status_dire",
        ),
    )
    match_df = _typed_frame([{name: getattr(match, name) for name in match_schema}], match_schema)

    # --- radiant advantages ---
    adv_len = max(len(match.radiant_gold_adv), len(match.radiant_xp_adv))
    advantage_rows = [
        {
            "game_time_s": (match.game_times_min[i] if i < len(match.game_times_min) else i * 60),
            "minute": (match.game_times_min[i] // 60 if i < len(match.game_times_min) else i),
            "radiant_gold_adv": match.radiant_gold_adv[i] if i < len(match.radiant_gold_adv) else 0,
            "radiant_xp_adv": match.radiant_xp_adv[i] if i < len(match.radiant_xp_adv) else 0,
        }
        for i in range(adv_len)
    ]
    advantage_df = _typed_frame(
        advantage_rows,
        {"game_time_s": _INT, "minute": _INT, "radiant_gold_adv": _INT, "radiant_xp_adv": _INT},
    )

    # --- list-based domains ---
    draft_df = _typed_frame([asdict(d) for d in match.draft], _field_dtypes(DraftEvent))
    # Teamfights: one row per fight, with the per-player breakdown in its own
    # long table. The per-player ability/item use dicts stay in the JSON output.
    teamfight_schema = {"fight_index": _INT, **_field_dtypes(Teamfight, exclude=("players",))}
    teamfight_player_schema = {
        "fight_index": _INT,
        **_field_dtypes(TeamfightPlayer, exclude=_TEAMFIGHT_PLAYER_DICTS),
    }
    teamfight_rows: list[dict[str, Any]] = []
    teamfight_player_rows: list[dict[str, Any]] = []
    for fight_index, fight in enumerate(match.teamfights):
        teamfight_rows.append(
            {"fight_index": fight_index}
            | {name: getattr(fight, name) for name in list(teamfight_schema)[1:]}
        )
        for fight_player in fight.players:
            teamfight_player_rows.append(
                {"fight_index": fight_index}
                | {name: getattr(fight_player, name) for name in list(teamfight_player_schema)[1:]}
            )
    teamfights_df = _typed_frame(teamfight_rows, teamfight_schema)
    teamfight_players_df = _typed_frame(teamfight_player_rows, teamfight_player_schema)

    # Smoke events: participants are exported in ``smoke_members``.
    smoke_schema = _field_dtypes(SmokeEvent, exclude=("participants",))
    smoke_df = _typed_frame(
        [
            {name: getattr(smoke, name) for name in smoke_schema} | {"smoked": _join(smoke.smoked)}
            for smoke in match.smoke_events
        ],
        smoke_schema,
    )
    smoke_event_dtypes = _field_dtypes(
        SmokeEvent, ("tick", "activation_game_time_s", "activator", "team")
    )
    smoke_member_schema = {
        "smoke_event_index": _INT,
        "activation_tick": smoke_event_dtypes["tick"],
        "activation_game_time_s": smoke_event_dtypes["activation_game_time_s"],
        "activator": smoke_event_dtypes["activator"],
        "team": smoke_event_dtypes["team"],
        **_field_dtypes(SmokeParticipant),
    }
    smoke_member_rows = [
        {
            "smoke_event_index": event_index,
            "activation_tick": smoke.tick,
            "activation_game_time_s": smoke.activation_game_time_s,
            "activator": smoke.activator,
            "team": smoke.team,
            **asdict(participant),
        }
        for event_index, smoke in enumerate(match.smoke_events)
        for participant in smoke.participants
    ]
    smoke_members_df = _typed_frame(smoke_member_rows, smoke_member_schema)
    courier_df = _typed_frame(
        [asdict(cs) for cs in match.courier_snapshots], _field_dtypes(CourierSnapshot)
    )
    neutral_item_finds_df = _typed_frame(
        [asdict(event) for event in match.neutral_item_finds],
        _field_dtypes(NeutralItemFoundEvent),
    )
    hero_visibility_df = _typed_frame(
        _plain_rows(match.hero_visibility_events), _field_dtypes(HeroVisibilityEvent)
    )
    entity_visibility_df = _typed_frame(
        _plain_rows(match.entity_visibility_events), _field_dtypes(EntityVisibilityEvent)
    )
    vision_modifiers_df = _typed_frame(
        [
            row | {"evidence_gaps": _join(row["evidence_gaps"])}
            for row in _plain_rows(match.vision_modifiers)
        ],
        _field_dtypes(VisionModifierEvent),
    )
    vision_modifier_pairing_issues_df = _typed_frame(
        [
            row | {"candidate_add_ticks": _join(row["candidate_add_ticks"])}
            for row in _plain_rows(match.vision_modifier_pairing_issues)
        ],
        _field_dtypes(VisionModifierPairingIssue),
    )
    player_log_schema = {**combat_log_schema, "player_id": _INT}
    buyback_dtypes = _field_dtypes(BuybackEvent, ("cost", "net_worth"))

    return {
        "match": match_df,
        "player_summary": player_summary_df,
        "player_timeseries": player_timeseries_df,
        "players_minute": players_min_df,
        "player_breakdowns": player_breakdowns_df,
        "positions": positions_df,
        "radiant_advantage": advantage_df,
        "combat_log": combat_df,
        "wards": wards_df,
        "objectives": objectives_df,
        "chat": chat_df,
        "draft": draft_df,
        "teamfights": teamfights_df,
        "teamfight_players": teamfight_players_df,
        "smoke_events": smoke_df,
        "smoke_members": smoke_members_df,
        "courier_snapshots": courier_df,
        "neutral_item_finds": neutral_item_finds_df,
        "hero_visibility_events": hero_visibility_df,
        "entity_visibility": entity_visibility_df,
        "vision_modifiers": vision_modifiers_df,
        "vision_modifier_pairing_issues": vision_modifier_pairing_issues_df,
        "player_kills_log": _typed_frame(player_kills_rows, player_log_schema),
        "player_purchase_log": _typed_frame(player_purchase_rows, player_log_schema),
        "player_runes_log": _typed_frame(player_runes_rows, player_log_schema),
        "player_buyback_log": _typed_frame(
            player_buyback_rows, {**player_log_schema, **buyback_dtypes}
        ),
    }


def _build_opendota_tables(match: ParsedMatch) -> dict[str, pd.DataFrame]:
    from gem.extractors.teamfights import OpenDotaTeamfight

    # OpenDota-shaped views for OpenDota-compatible consumers. Objective rows
    # carry type-specific keys, so the table holds the union of them.
    objectives_df = _typed_frame(
        match.objectives,
        {
            "time": _INT,
            "type": _STR,
            "key": _STR,
            "unit": _STR,
            "slot": _INT,
            "player_slot": _INT,
            "team": _INT,
            "killer": _INT,
        },
    )
    # The nested per-player breakdown is keyed by hero/ability/item names, so it
    # is JSON-encoded to keep one string column rather than a match-specific
    # struct type.
    teamfight_rows = [asdict(tf) for tf in match.opendota_teamfights]
    for row in teamfight_rows:
        row["players"] = json.dumps(row["players"])
    teamfights_df = _typed_frame(teamfight_rows, _field_dtypes(OpenDotaTeamfight))
    return {"opendota_objectives": objectives_df, "opendota_teamfights": teamfights_df}


def _build_analysis_tables(match: ParsedMatch) -> dict[str, pd.DataFrame]:
    from gem.analysis.farming import build_farming_routes
    from gem.analysis.roshan import build_rosh_conversions
    from gem.analysis.smoke_fight import build_smoke_fight_insights
    from gem.analysis.teamfight_positioning import build_teamfight_positioning

    positioning_schema = {
        "fight_index": _INT,
        "fight_start_tick": _INT,
        "engagement_start_tick": _INT,
        "first_death_tick": _INT,
        "fight_end_tick": _INT,
        "engagement_start_source": _STR,
        "snapshot_kind": _STR,
        "snapshot_tick": _INT,
        "player_id": _INT,
        "player_name": _STR,
        "hero_name": _STR,
        "team": _INT,
        "active_participant": _BOOL,
        "near_fight": _BOOL,
        "x": _FLOAT,
        "y": _FLOAT,
        "sample_tick": _INT,
        "sample_age_ticks": _INT,
        "visibility": _STR,
        "distance_to_team_centroid": _FLOAT,
        "nearest_ally_distance": _FLOAT,
        "nearest_enemy_distance": _FLOAT,
        "active_smoke_activation_tick": _INT,
        "active_reveal_modifiers": _STR,
        "evidence_gaps": _STR,
        "radiant_expected_count": _INT,
        "radiant_positioned_count": _INT,
        "radiant_unpositioned_count": _INT,
        "radiant_completeness": _STR,
        "radiant_centroid_x": _FLOAT,
        "radiant_centroid_y": _FLOAT,
        "radiant_rms_spread": _FLOAT,
        "dire_expected_count": _INT,
        "dire_positioned_count": _INT,
        "dire_unpositioned_count": _INT,
        "dire_completeness": _STR,
        "dire_centroid_x": _FLOAT,
        "dire_centroid_y": _FLOAT,
        "dire_rms_spread": _FLOAT,
        "centroid_distance": _FLOAT,
        "active_participant_centroid_x": _FLOAT,
        "active_participant_centroid_y": _FLOAT,
    }
    positioning_rows: list[dict[str, Any]] = []
    for fight in build_teamfight_positioning(match):
        for snapshot in fight.snapshots:
            for hero in snapshot.heroes:
                positioning_rows.append(
                    {
                        "fight_index": fight.fight_index,
                        "fight_start_tick": fight.start_tick,
                        "engagement_start_tick": fight.engagement_start_tick,
                        "first_death_tick": fight.first_death_tick,
                        "fight_end_tick": fight.end_tick,
                        "engagement_start_source": fight.engagement_start_source.value,
                        "snapshot_kind": snapshot.kind.value,
                        "snapshot_tick": snapshot.tick,
                        "player_id": hero.player_id,
                        "player_name": hero.player_name,
                        "hero_name": hero.hero_name,
                        "team": hero.team,
                        "active_participant": hero.active_participant,
                        "near_fight": hero.near_fight,
                        "x": hero.x,
                        "y": hero.y,
                        "sample_tick": hero.sample_tick,
                        "sample_age_ticks": hero.sample_age_ticks,
                        "visibility": hero.visibility.value,
                        "distance_to_team_centroid": hero.distance_to_team_centroid,
                        "nearest_ally_distance": hero.nearest_ally_distance,
                        "nearest_enemy_distance": hero.nearest_enemy_distance,
                        "active_smoke_activation_tick": hero.active_smoke_activation_tick,
                        "active_reveal_modifiers": _join(hero.active_reveal_modifiers),
                        "evidence_gaps": _join(hero.evidence_gaps),
                        "radiant_expected_count": snapshot.radiant.expected_count,
                        "radiant_positioned_count": snapshot.radiant.positioned_count,
                        "radiant_unpositioned_count": snapshot.radiant.unpositioned_count,
                        "radiant_completeness": snapshot.radiant.completeness.value,
                        "radiant_centroid_x": snapshot.radiant.centroid_x,
                        "radiant_centroid_y": snapshot.radiant.centroid_y,
                        "radiant_rms_spread": snapshot.radiant.rms_spread,
                        "dire_expected_count": snapshot.dire.expected_count,
                        "dire_positioned_count": snapshot.dire.positioned_count,
                        "dire_unpositioned_count": snapshot.dire.unpositioned_count,
                        "dire_completeness": snapshot.dire.completeness.value,
                        "dire_centroid_x": snapshot.dire.centroid_x,
                        "dire_centroid_y": snapshot.dire.centroid_y,
                        "dire_rms_spread": snapshot.dire.rms_spread,
                        "centroid_distance": snapshot.centroid_distance,
                        "active_participant_centroid_x": (snapshot.active_participant_centroid_x),
                        "active_participant_centroid_y": (snapshot.active_participant_centroid_y),
                    }
                )
    teamfight_positioning_df = _typed_frame(positioning_rows, positioning_schema)

    # --- evidence-first Roshan conversions ---
    roshan_conversion_schema = {
        "rosh_number": _INT,
        "rosh_tick": _INT,
        "killer_name": _STR,
        "roshan_team": _INT,
        "roshan_team_source": _STR,
        "conversion_team": _INT,
        "conversion_team_source": _STR,
        "holder_player_id": _INT,
        "holder_name": _STR,
        "aegis_pickup_tick": _INT,
        "aegis_end_tick": _INT,
        "aegis_eval_end_tick": _INT,
        "aegis_fate": _STR,
        "aegis_fate_source": _STR,
        "aegis_fate_inferred": _BOOL,
        "aegis_outcome": _STR,
        "first_engagement_tick": _INT,
        "first_fight_tick": _INT,
        "first_objective_tick": _INT,
        "fight_count": _INT,
        "fight_differential": _INT,
        "conversion_towers": _INT,
        "opponent_towers": _INT,
        "unattributed_towers": _INT,
        "conversion_barracks": _INT,
        "opponent_barracks": _INT,
        "unattributed_barracks": _INT,
        "conversion_structure_value": _INT,
        "opponent_structure_value": _INT,
        "structure_delta": _INT,
        "net_worth_advantage_start": _INT,
        "net_worth_advantage_end": _INT,
        "net_worth_swing": _INT,
        "net_worth_swing_per_minute": _FLOAT,
        "xp_advantage_start": _INT,
        "xp_advantage_end": _INT,
        "xp_swing": _INT,
        "xp_swing_per_minute": _FLOAT,
        "before_conversion_coverage_pct": _FLOAT,
        "before_opponent_coverage_pct": _FLOAT,
        "during_conversion_coverage_pct": _FLOAT,
        "during_opponent_coverage_pct": _FLOAT,
        "coverage_swing_pct": _FLOAT,
        "depth_swing": _FLOAT,
        "conversion_forward_wards": _INT,
        "opponent_forward_wards": _INT,
        "forward_ward_delta": _INT,
        "conversion_tormentors": _INT,
        "opponent_tormentors": _INT,
        "unattributed_tormentors": _INT,
        "tormentor_delta": _INT,
        "conversion_tags": _STR,
        "tag_ruleset": _STR,
        "analysis_status": _STR,
        "analysis_status_reasons": _STR,
        "drops": _STR,
        "legacy_conversion_score": _INT,
        "legacy_conversion_label": _STR,
    }
    roshan_fight_schema = {
        "rosh_number": _INT,
        "fight_index": _INT,
        "relation": _STR,
        "engagement_start_tick": _INT,
        "engagement_start_source": _STR,
        "first_death_tick": _INT,
        "fight_end_tick": _INT,
        "winner": _STR,
        "deaths": _INT,
        "conversion_participant_ids": _STR,
        "opponent_participant_ids": _STR,
        "unknown_participant_ids": _STR,
    }
    roshan_conversion_rows: list[dict[str, Any]] = []
    roshan_fight_rows: list[dict[str, Any]] = []
    for conversion in build_rosh_conversions(match):
        profile = conversion.differential_profile
        roshan_conversion_rows.append(
            {
                "rosh_number": conversion.rosh_number,
                "rosh_tick": conversion.rosh_tick,
                "killer_name": conversion.killer_name,
                "roshan_team": conversion.roshan_team,
                "roshan_team_source": conversion.roshan_team_source.value,
                "conversion_team": conversion.conversion_team,
                "conversion_team_source": conversion.conversion_team_source.value,
                "holder_player_id": conversion.holder_player_id,
                "holder_name": conversion.holder_name,
                "aegis_pickup_tick": conversion.aegis_pickup_tick,
                "aegis_end_tick": conversion.aegis_end_tick,
                "aegis_eval_end_tick": conversion.aegis_eval_end_tick,
                "aegis_fate": conversion.aegis_fate,
                "aegis_fate_source": conversion.aegis_fate_source.value,
                "aegis_fate_inferred": conversion.aegis_fate_inferred,
                "aegis_outcome": conversion.aegis_outcome,
                "first_engagement_tick": conversion.first_engagement_tick,
                "first_fight_tick": conversion.first_fight_tick,
                "first_objective_tick": conversion.first_objective_tick,
                "fight_count": conversion.fight_count,
                "fight_differential": profile.fight_differential,
                "conversion_towers": profile.conversion_towers,
                "opponent_towers": profile.opponent_towers,
                "unattributed_towers": profile.unattributed_towers,
                "conversion_barracks": profile.conversion_barracks,
                "opponent_barracks": profile.opponent_barracks,
                "unattributed_barracks": profile.unattributed_barracks,
                "conversion_structure_value": profile.conversion_structure_value,
                "opponent_structure_value": profile.opponent_structure_value,
                "structure_delta": profile.structure_delta,
                "net_worth_advantage_start": profile.net_worth_advantage_start,
                "net_worth_advantage_end": profile.net_worth_advantage_end,
                "net_worth_swing": profile.net_worth_swing,
                "net_worth_swing_per_minute": profile.net_worth_swing_per_minute,
                "xp_advantage_start": profile.xp_advantage_start,
                "xp_advantage_end": profile.xp_advantage_end,
                "xp_swing": profile.xp_swing,
                "xp_swing_per_minute": profile.xp_swing_per_minute,
                "before_conversion_coverage_pct": (
                    profile.before_territory.conversion_coverage_pct
                ),
                "before_opponent_coverage_pct": (profile.before_territory.opponent_coverage_pct),
                "during_conversion_coverage_pct": (
                    profile.during_territory.conversion_coverage_pct
                ),
                "during_opponent_coverage_pct": (profile.during_territory.opponent_coverage_pct),
                "coverage_swing_pct": profile.coverage_swing_pct,
                "depth_swing": profile.depth_swing,
                "conversion_forward_wards": profile.conversion_forward_wards,
                "opponent_forward_wards": profile.opponent_forward_wards,
                "forward_ward_delta": profile.forward_ward_delta,
                "conversion_tormentors": profile.conversion_tormentors,
                "opponent_tormentors": profile.opponent_tormentors,
                "unattributed_tormentors": profile.unattributed_tormentors,
                "tormentor_delta": profile.tormentor_delta,
                "conversion_tags": ",".join(conversion.conversion_tags),
                "tag_ruleset": profile.tag_ruleset,
                "analysis_status": conversion.analysis_status,
                "analysis_status_reasons": ";".join(conversion.analysis_status_reasons),
                "drops": ",".join(conversion.drops),
                "legacy_conversion_score": conversion.conversion_score,
                "legacy_conversion_label": conversion.conversion_label,
            }
        )
        for evidence in conversion.fight_evidence:
            roshan_fight_rows.append(
                {
                    "rosh_number": conversion.rosh_number,
                    "fight_index": evidence.fight_index,
                    "relation": evidence.relation.value,
                    "engagement_start_tick": evidence.engagement_start_tick,
                    "engagement_start_source": evidence.engagement_start_source.value,
                    "first_death_tick": evidence.first_death_tick,
                    "fight_end_tick": evidence.end_tick,
                    "winner": evidence.winner,
                    "deaths": evidence.deaths,
                    "conversion_participant_ids": ",".join(
                        str(player_id) for player_id in evidence.conversion_participant_ids
                    ),
                    "opponent_participant_ids": ",".join(
                        str(player_id) for player_id in evidence.opponent_participant_ids
                    ),
                    "unknown_participant_ids": ",".join(
                        str(player_id) for player_id in evidence.unknown_participant_ids
                    ),
                }
            )
    roshan_conversions_df = _typed_frame(roshan_conversion_rows, roshan_conversion_schema)
    roshan_conversion_fights_df = _typed_frame(roshan_fight_rows, roshan_fight_schema)

    # --- bounded smoke/fight insights ---
    insight_schema = {
        "smoke_index": _INT,
        "fight_index": _INT,
        "status": _STR,
        "evidence_completeness": _STR,
        "smoke_team": _INT,
        "activator": _STR,
        "smoke_lifecycle_status": _STR,
        "activation_tick": _INT,
        "activation_game_time_s": _INT,
        "first_member_removal_tick": _INT,
        "first_authoritative_visible_tick": _INT,
        "first_direct_reveal_tick": _INT,
        "first_member_action_tick": _INT,
        "first_death_tick": _INT,
        "fight_end_tick": _INT,
        "active_smoked_member_count": _INT,
        "active_smoked_player_ids": _STR,
        "pre_engagement_expected_count": _INT,
        "pre_engagement_positioned_count": _INT,
        "pre_engagement_completeness": _STR,
        "pre_engagement_centroid_x": _FLOAT,
        "pre_engagement_centroid_y": _FLOAT,
        "pre_engagement_rms_spread": _FLOAT,
        "pre_engagement_max_pairwise_distance": _FLOAT,
        "engagement_expected_count": _INT,
        "engagement_positioned_count": _INT,
        "engagement_completeness": _STR,
        "engagement_centroid_x": _FLOAT,
        "engagement_centroid_y": _FLOAT,
        "engagement_rms_spread": _FLOAT,
        "engagement_max_pairwise_distance": _FLOAT,
        "sampled_near_fight_spread_ticks": _INT,
        "near_fight_centroid_source": _STR,
        "fight_deaths": _INT,
        "fight_radiant_kills": _INT,
        "fight_dire_kills": _INT,
        "fight_winner": _STR,
        "follow_up_start_tick": _INT,
        "follow_up_end_tick": _INT,
        "follow_up_end_reasons": _STR,
        "evidence_gaps": _STR,
    }
    member_schema = {
        "smoke_index": _INT,
        "fight_index": _INT,
        "status": _STR,
        "participant_index": _INT,
        "player_id": _INT,
        "hero_name": _STR,
        "resolved": _BOOL,
        "active_participant": _BOOL,
        "authoritative_visibility": _STR,
        "point_vision_status": _STR,
        "pre_engagement_x": _FLOAT,
        "pre_engagement_y": _FLOAT,
        "pre_engagement_sample_tick": _INT,
        "pre_engagement_sample_age_ticks": _INT,
        "engagement_x": _FLOAT,
        "engagement_y": _FLOAT,
        "engagement_sample_tick": _INT,
        "engagement_sample_age_ticks": _INT,
        "sampled_near_fight_tick": _INT,
        "sampled_near_fight_x": _FLOAT,
        "sampled_near_fight_y": _FLOAT,
        "sampled_near_fight_distance": _FLOAT,
        "evidence_gaps": _STR,
    }
    follow_up_schema = {
        "smoke_index": _INT,
        "fight_index": _INT,
        "kind": _STR,
        "source_index": _INT,
        "tick": _INT,
        "game_time_s": _INT,
        "tick_delta": _INT,
        "game_time_delta_s": _INT,
        "actor_name": _STR,
        "actor_player_id": _INT,
        "actor_team": _INT,
        "relation": _STR,
        "subject_name": _STR,
        "window_start_tick": _INT,
        "window_end_tick": _INT,
    }

    smoke_fight_insight_rows: list[dict[str, Any]] = []
    smoke_fight_member_rows: list[dict[str, Any]] = []
    smoke_fight_follow_up_rows: list[dict[str, Any]] = []
    for insight in build_smoke_fight_insights(match):
        pre = insight.pre_engagement_formation
        engagement = insight.engagement_formation
        outcome = insight.outcome
        window = insight.follow_up_window
        smoke_fight_insight_rows.append(
            {
                "smoke_index": insight.smoke_index,
                "fight_index": insight.fight_index,
                "status": insight.status.value,
                "evidence_completeness": insight.evidence_completeness.value,
                "smoke_team": insight.smoke_team,
                "activator": insight.activator,
                "smoke_lifecycle_status": insight.smoke_lifecycle_status.value,
                "activation_tick": insight.activation.tick,
                "activation_game_time_s": insight.activation.game_time_s,
                "first_member_removal_tick": (
                    insight.first_member_removal.tick if insight.first_member_removal else None
                ),
                "first_authoritative_visible_tick": (
                    insight.first_authoritative_visible.tick
                    if insight.first_authoritative_visible
                    else None
                ),
                "first_direct_reveal_tick": (
                    insight.first_direct_reveal.tick if insight.first_direct_reveal else None
                ),
                "first_member_action_tick": (
                    insight.first_member_action.tick if insight.first_member_action else None
                ),
                "first_death_tick": insight.first_death.tick if insight.first_death else None,
                "fight_end_tick": insight.fight_end.tick if insight.fight_end else None,
                "active_smoked_member_count": len(insight.active_smoked_player_ids),
                "active_smoked_player_ids": ",".join(
                    str(player_id) for player_id in insight.active_smoked_player_ids
                ),
                "pre_engagement_expected_count": pre.expected_count if pre else None,
                "pre_engagement_positioned_count": pre.positioned_count if pre else None,
                "pre_engagement_completeness": pre.completeness.value if pre else None,
                "pre_engagement_centroid_x": pre.centroid_x if pre else None,
                "pre_engagement_centroid_y": pre.centroid_y if pre else None,
                "pre_engagement_rms_spread": pre.rms_spread if pre else None,
                "pre_engagement_max_pairwise_distance": (
                    pre.max_pairwise_distance if pre else None
                ),
                "engagement_expected_count": engagement.expected_count if engagement else None,
                "engagement_positioned_count": (
                    engagement.positioned_count if engagement else None
                ),
                "engagement_completeness": (engagement.completeness.value if engagement else None),
                "engagement_centroid_x": engagement.centroid_x if engagement else None,
                "engagement_centroid_y": engagement.centroid_y if engagement else None,
                "engagement_rms_spread": engagement.rms_spread if engagement else None,
                "engagement_max_pairwise_distance": (
                    engagement.max_pairwise_distance if engagement else None
                ),
                "sampled_near_fight_spread_ticks": insight.sampled_near_fight_spread_ticks,
                "near_fight_centroid_source": (
                    insight.near_fight_centroid_source.value
                    if insight.near_fight_centroid_source
                    else None
                ),
                "fight_deaths": outcome.deaths if outcome else None,
                "fight_radiant_kills": outcome.radiant_kills if outcome else None,
                "fight_dire_kills": outcome.dire_kills if outcome else None,
                "fight_winner": outcome.winner if outcome else None,
                "follow_up_start_tick": window.start_tick if window else None,
                "follow_up_end_tick": window.end_tick if window else None,
                "follow_up_end_reasons": (
                    ",".join(reason.value for reason in window.end_reasons) if window else ""
                ),
                "evidence_gaps": ";".join(insight.evidence_gaps),
            }
        )

        for member in insight.members:
            pre_position = member.pre_engagement_position
            engagement_position = member.engagement_position
            near = member.sampled_near_fight
            smoke_fight_member_rows.append(
                {
                    "smoke_index": insight.smoke_index,
                    "fight_index": insight.fight_index,
                    "status": insight.status.value,
                    "participant_index": member.participant_index,
                    "player_id": member.player_id,
                    "hero_name": member.hero_name,
                    "resolved": member.resolved,
                    "active_participant": member.active_participant,
                    "authoritative_visibility": member.authoritative_visibility.value,
                    "point_vision_status": (
                        member.point_vision.status.value if member.point_vision else None
                    ),
                    "pre_engagement_x": pre_position.x if pre_position else None,
                    "pre_engagement_y": pre_position.y if pre_position else None,
                    "pre_engagement_sample_tick": (
                        pre_position.sample_tick if pre_position else None
                    ),
                    "pre_engagement_sample_age_ticks": (
                        pre_position.sample_age_ticks if pre_position else None
                    ),
                    "engagement_x": engagement_position.x if engagement_position else None,
                    "engagement_y": engagement_position.y if engagement_position else None,
                    "engagement_sample_tick": (
                        engagement_position.sample_tick if engagement_position else None
                    ),
                    "engagement_sample_age_ticks": (
                        engagement_position.sample_age_ticks if engagement_position else None
                    ),
                    "sampled_near_fight_tick": near.tick if near else None,
                    "sampled_near_fight_x": near.x if near else None,
                    "sampled_near_fight_y": near.y if near else None,
                    "sampled_near_fight_distance": near.distance if near else None,
                    "evidence_gaps": ";".join(member.evidence_gaps),
                }
            )

        for follow_up in insight.follow_ups:
            smoke_fight_follow_up_rows.append(
                {
                    "smoke_index": insight.smoke_index,
                    "fight_index": insight.fight_index,
                    "kind": follow_up.kind.value,
                    "source_index": follow_up.source_index,
                    "tick": follow_up.tick,
                    "game_time_s": follow_up.game_time_s,
                    "tick_delta": follow_up.tick_delta,
                    "game_time_delta_s": follow_up.game_time_delta_s,
                    "actor_name": follow_up.actor_name,
                    "actor_player_id": follow_up.actor_player_id,
                    "actor_team": follow_up.actor_team,
                    "relation": follow_up.relation.value,
                    "subject_name": follow_up.subject_name,
                    "window_start_tick": window.start_tick if window else None,
                    "window_end_tick": window.end_tick if window else None,
                }
            )

    smoke_fight_insights_df = _typed_frame(
        smoke_fight_insight_rows,
        insight_schema,
    )
    smoke_fight_members_df = _typed_frame(
        smoke_fight_member_rows,
        member_schema,
    )
    smoke_fight_followups_df = _typed_frame(
        smoke_fight_follow_up_rows,
        follow_up_schema,
    )

    # --- evidence-first farming routes ---
    farming_route_schema = {
        "player_id": _INT,
        "hero_name": _STR,
        "team": _INT,
        "camp_catalog_version": _INT,
        "camp_map_patch": _STR,
        "camp_topology_patch": _STR,
        "status": _STR,
        "status_reasons": _STR,
        "segment_count": _INT,
        "point_count": _INT,
    }
    farming_segment_schema = {
        "player_id": _INT,
        "hero_name": _STR,
        "team": _INT,
        "segment_index": _INT,
        "camp_id": _INT,
        "camp_type": _STR,
        "start_tick": _INT,
        "end_tick": _INT,
        "duration_seconds": _FLOAT,
        "start_reason": _STR,
        "end_reason": _STR,
        "sample_count": _INT,
        "in_zone_sample_count": _INT,
        "position_coverage": _FLOAT,
        "max_sample_gap_ticks": _INT,
        "micro_exit_merged": _BOOL,
        "neutral_kills": _INT,
        "neutral_damage": _INT,
        "window_xp_delta": _INT,
        "window_total_earned_gold_delta": _INT,
        "resource_start_sample_tick": _INT,
        "resource_end_sample_tick": _INT,
        "evidence_strength": _STR,
        "evidence_reasons": _STR,
        "evidence_gaps": _STR,
        "distance_travelled": _FLOAT,
        "camp_owner_team": _INT,
        "camp_lane": _STR,
        "camp_area": _STR,
        "camp_catalog_version": _INT,
        "camp_map_patch": _STR,
        "camp_topology_patch": _STR,
        "context_midpoint_tick": _INT,
        "context_lookback_start_tick": _INT,
        "context_camp_side": _STR,
        "context_status": _STR,
        "context_status_reasons": _STR,
        "context_tags": _STR,
        "own_presence_hero_seconds": _FLOAT,
        "enemy_presence_hero_seconds": _FLOAT,
        "own_presence_position_coverage": _FLOAT,
        "enemy_presence_position_coverage": _FLOAT,
        "own_point_vision_status": _STR,
        "enemy_point_vision_status": _STR,
        "own_point_vision_source_count": _INT,
        "enemy_point_vision_source_count": _INT,
        "own_observer_vision_source_count": _INT,
        "enemy_observer_vision_source_count": _INT,
        "own_point_vision_gaps": _STR,
        "enemy_point_vision_gaps": _STR,
        "own_relevant_towers_alive": _INT,
        "enemy_relevant_towers_alive": _INT,
        "net_worth_advantage": _INT,
        "total_earned_xp_advantage": _INT,
        "aegis_holder_team": _INT,
        "aegis_active": _BOOL,
        "aegis_source": _STR,
        "last_roshan_tick": _INT,
        "last_roshan_team": _INT,
        "roshan_team_source": _STR,
        "last_tormentor_tick": _INT,
        "last_tormentor_team": _INT,
        "tormentor_team_source": _STR,
        "territory_coverage_differential_pct": _FLOAT,
        "territory_depth_differential": _FLOAT,
    }
    farming_point_schema = {
        "player_id": _INT,
        "hero_name": _STR,
        "team": _INT,
        "segment_index": _INT,
        "tick": _INT,
        "x": _FLOAT,
        "y": _FLOAT,
        "camp_id": _INT,
        "camp_type": _STR,
        "inside_base_zone": _BOOL,
        "boundary_before": _STR,
    }
    farming_route_rows: list[dict[str, Any]] = []
    farming_segment_rows: list[dict[str, Any]] = []
    farming_point_rows: list[dict[str, Any]] = []
    farming_context_tag_rows: list[dict[str, Any]] = []
    for route in build_farming_routes(match):
        farming_route_rows.append(
            {
                "player_id": route.player_id,
                "hero_name": route.hero_name,
                "team": route.team,
                "camp_catalog_version": route.camp_catalog_version,
                "camp_map_patch": route.camp_map_patch,
                "camp_topology_patch": route.camp_topology_patch,
                "status": route.status,
                "status_reasons": ";".join(route.status_reasons),
                "segment_count": len(route.segments),
                "point_count": len(route.points),
            }
        )
        segment_by_point = {
            id(point): segment.segment_index
            for segment in route.segments
            for point in segment.points
        }
        for segment in route.segments:
            context = segment.context
            farming_segment_rows.append(
                {
                    "player_id": segment.player_id,
                    "hero_name": segment.hero_name,
                    "team": segment.team,
                    "segment_index": segment.segment_index,
                    "camp_id": segment.camp_id,
                    "camp_type": segment.camp_type,
                    "start_tick": segment.start_tick,
                    "end_tick": segment.end_tick,
                    "duration_seconds": segment.duration_seconds,
                    "start_reason": segment.start_reason.value,
                    "end_reason": segment.end_reason.value,
                    "sample_count": segment.sample_count,
                    "in_zone_sample_count": segment.in_zone_sample_count,
                    "position_coverage": segment.position_coverage,
                    "max_sample_gap_ticks": segment.max_sample_gap_ticks,
                    "micro_exit_merged": segment.micro_exit_merged,
                    "neutral_kills": segment.neutral_kills,
                    "neutral_damage": segment.neutral_damage,
                    "window_xp_delta": segment.window_xp_delta,
                    "window_total_earned_gold_delta": (segment.window_total_earned_gold_delta),
                    "resource_start_sample_tick": segment.resource_start_sample_tick,
                    "resource_end_sample_tick": segment.resource_end_sample_tick,
                    "evidence_strength": segment.evidence_strength.value,
                    "evidence_reasons": ";".join(segment.evidence_reasons),
                    "evidence_gaps": ";".join(segment.evidence_gaps),
                    "distance_travelled": segment.distance_travelled,
                    "camp_owner_team": segment.camp_owner_team,
                    "camp_lane": segment.camp_lane,
                    "camp_area": segment.camp_area,
                    "camp_catalog_version": segment.camp_catalog_version,
                    "camp_map_patch": segment.camp_map_patch,
                    "camp_topology_patch": segment.camp_topology_patch,
                    "context_midpoint_tick": context.midpoint_tick if context else None,
                    "context_lookback_start_tick": (
                        context.lookback_start_tick if context else None
                    ),
                    "context_camp_side": context.camp_side if context else None,
                    "context_status": context.status if context else None,
                    "context_status_reasons": (";".join(context.status_reasons) if context else ""),
                    "context_tags": (
                        ";".join(tag.value for tag in context.tags) if context else ""
                    ),
                    "own_presence_hero_seconds": (
                        context.own_presence_hero_seconds if context else None
                    ),
                    "enemy_presence_hero_seconds": (
                        context.enemy_presence_hero_seconds if context else None
                    ),
                    "own_presence_position_coverage": (
                        context.own_presence_position_coverage if context else None
                    ),
                    "enemy_presence_position_coverage": (
                        context.enemy_presence_position_coverage if context else None
                    ),
                    "own_point_vision_status": (
                        context.own_point_vision_status if context else None
                    ),
                    "enemy_point_vision_status": (
                        context.enemy_point_vision_status if context else None
                    ),
                    "own_point_vision_source_count": (
                        context.own_point_vision_source_count if context else None
                    ),
                    "enemy_point_vision_source_count": (
                        context.enemy_point_vision_source_count if context else None
                    ),
                    "own_observer_vision_source_count": (
                        context.own_observer_vision_source_count if context else None
                    ),
                    "enemy_observer_vision_source_count": (
                        context.enemy_observer_vision_source_count if context else None
                    ),
                    "own_point_vision_gaps": (
                        ";".join(context.own_point_vision_gaps) if context else ""
                    ),
                    "enemy_point_vision_gaps": (
                        ";".join(context.enemy_point_vision_gaps) if context else ""
                    ),
                    "own_relevant_towers_alive": (
                        context.own_relevant_towers_alive if context else None
                    ),
                    "enemy_relevant_towers_alive": (
                        context.enemy_relevant_towers_alive if context else None
                    ),
                    "net_worth_advantage": context.net_worth_advantage if context else None,
                    "total_earned_xp_advantage": (
                        context.total_earned_xp_advantage if context else None
                    ),
                    "aegis_holder_team": context.aegis_holder_team if context else None,
                    "aegis_active": context.aegis_active if context else None,
                    "aegis_source": context.aegis_source if context else None,
                    "last_roshan_tick": context.last_roshan_tick if context else None,
                    "last_roshan_team": context.last_roshan_team if context else None,
                    "roshan_team_source": context.roshan_team_source if context else None,
                    "last_tormentor_tick": context.last_tormentor_tick if context else None,
                    "last_tormentor_team": context.last_tormentor_team if context else None,
                    "tormentor_team_source": (context.tormentor_team_source if context else None),
                    "territory_coverage_differential_pct": (
                        context.territory_coverage_differential_pct if context else None
                    ),
                    "territory_depth_differential": (
                        context.territory_depth_differential if context else None
                    ),
                }
            )
            if context is not None:
                for tag in context.tags:
                    farming_context_tag_rows.append(
                        {
                            "player_id": segment.player_id,
                            "hero_name": segment.hero_name,
                            "team": segment.team,
                            "segment_index": segment.segment_index,
                            "camp_id": segment.camp_id,
                            "tag": tag.value,
                            "reasons": ";".join(context.tag_reasons.get(tag.value, [])),
                            "context_status": context.status,
                        }
                    )
        for point in route.points:
            farming_point_rows.append(
                {
                    "player_id": route.player_id,
                    "hero_name": route.hero_name,
                    "team": route.team,
                    "segment_index": segment_by_point.get(id(point)),
                    "tick": point.tick,
                    "x": point.x,
                    "y": point.y,
                    "camp_id": point.camp_id,
                    "camp_type": point.camp_type,
                    "inside_base_zone": point.inside_base_zone,
                    "boundary_before": (
                        point.boundary_before.value if point.boundary_before else None
                    ),
                }
            )
    farming_routes_df = _typed_frame(farming_route_rows, farming_route_schema)
    farming_route_segments_df = _typed_frame(farming_segment_rows, farming_segment_schema)
    farming_route_points_df = _typed_frame(farming_point_rows, farming_point_schema)
    farming_context_tags_df = _typed_frame(
        farming_context_tag_rows,
        {
            "player_id": _INT,
            "hero_name": _STR,
            "team": _INT,
            "segment_index": _INT,
            "camp_id": _INT,
            "tag": _STR,
            "reasons": _STR,
            "context_status": _STR,
        },
    )

    return {
        "teamfight_positioning": teamfight_positioning_df,
        "roshan_conversions": roshan_conversions_df,
        "roshan_conversion_fights": roshan_conversion_fights_df,
        "smoke_fight_insights": smoke_fight_insights_df,
        "smoke_fight_members": smoke_fight_members_df,
        "smoke_fight_followups": smoke_fight_followups_df,
        "farming_routes": farming_routes_df,
        "farming_route_segments": farming_route_segments_df,
        "farming_route_points": farming_route_points_df,
        "farming_context_tags": farming_context_tags_df,
    }
