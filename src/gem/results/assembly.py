"""Match assembly — wires extractor outputs into a :class:`ParsedMatch`.

Takes the raw extractor state after a completed parse and builds the fully
populated :class:`ParsedMatch` returned by :func:`gem.parse`.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from gem.analysis import net_worth_at
from gem.catalog import hero_id
from gem.combat.log import opendota_translate
from gem.extractors.lane import classify_lane
from gem.results.derived import building_status, buyback_cost, categorize_kills, killed_counts
from gem.results.models import BuybackEvent, ParsedMatch

if TYPE_CHECKING:
    from gem.combat.aggregator import _CombatAggregator
    from gem.combat.log import CombatLogEntry
    from gem.extractors.courier import CourierExtractor
    from gem.extractors.draft import DraftExtractor
    from gem.extractors.intervals import IntervalExtractor, IntervalSnapshot, IntervalTimeSeries
    from gem.extractors.objectives import ObjectivesExtractor
    from gem.extractors.players import PlayerExtractor
    from gem.extractors.wards import WardEvent, WardsExtractor
    from gem.parser import ReplayParser
    from gem.results.models import (
        ChatEntry,
        NeutralItemFoundEvent,
        ParsedPlayer,
        SmokeEvent,
        VisionModifierEvent,
    )

# Lane position grid resolution in world units (7d)
_LANE_GRID = 64
# First 10 game-minutes in ticks (600s × 30 ticks/s)
_LANE_WINDOW = 600 * 30


def _metadata_slot_to_player_id(player_slot: int) -> int | None:
    """Convert match-metadata player slots to gem player ids."""
    if 0 <= player_slot <= 4:
        return player_slot
    if 128 <= player_slot <= 132:
        return 5 + (player_slot - 128)
    return None


def _player_id_to_player_slot(player_id: int) -> int:
    """Convert a gem player id (0-9) to OpenDota's ``player_slot`` encoding.

    OpenDota encodes Radiant players as ``0-4`` and Dire players as ``128-132``
    in ``player_slot`` fields, while the ``slot`` field stays ``0-9``. This is the
    inverse of :func:`_metadata_slot_to_player_id`.

    Args:
        player_id: gem logical player id, 0-9 (0-4 Radiant, 5-9 Dire).

    Returns:
        The OpenDota ``player_slot`` (0-4 for Radiant, 128-132 for Dire).
    """
    return player_id if player_id < 5 else 128 + (player_id - 5)


def _tick_game_seconds(tick: int, game_start_tick: int | None) -> int:
    """Return an absolute tick's game-relative time in seconds.

    Args:
        tick: Absolute parser tick.
        game_start_tick: Absolute tick of the game clock start, or ``None``.

    Returns:
        Game-relative seconds (negative pre-horn), or ``0`` with no clock ref.
    """
    if game_start_tick is None:
        return 0
    return (tick - game_start_tick) // 30


def _entry_game_seconds(entry: CombatLogEntry, game_start_tick: int | None) -> int:
    """Return a combat-log entry's game-relative time in seconds.

    Prefers the OpenDota-aligned ``game_time_s`` when present, falling back to the
    tick offset from ``game_start_tick`` (30 ticks/second). Pre-horn events keep
    their negative offset, matching OpenDota.

    Args:
        entry: The combat log entry.
        game_start_tick: Absolute tick of the game clock start, or ``None``.

    Returns:
        Game-relative seconds (may be negative for pre-horn events), or ``0``
        when no clock reference is available.
    """
    if entry.game_time_s is not None:
        return int(entry.game_time_s)
    return _tick_game_seconds(entry.tick, game_start_tick)


def _build_purchase_aggregates(
    purchase_log: list[CombatLogEntry], game_start_tick: int | None
) -> dict[str, Any]:
    """Derive OpenDota purchase-timeline aggregates from a player's purchase log.

    Mirrors OpenDota's ``handlePurchase`` semantics: the ``purchase`` count map
    includes recipes; ``purchase_time`` / ``first_purchase_time`` (and the
    per-item scalars) exclude ``recipe_`` items. Item names are translated
    (``item_`` stripped); times are game-seconds.

    Args:
        purchase_log: The player's deduped PURCHASE ``CombatLogEntry`` list.
        game_start_tick: Absolute tick of the game clock start, or ``None``.

    Returns:
        Dict with ``purchase``, ``purchase_time``, ``first_purchase_time`` (maps)
        and ``purchase_tpscroll`` / ``purchase_ward_observer`` /
        ``purchase_ward_sentry`` (ints).
    """
    purchase: dict[str, int] = {}
    purchase_time: dict[str, int] = {}
    first_purchase_time: dict[str, int] = {}
    for entry in sorted(purchase_log, key=lambda e: e.tick):
        key = opendota_translate(entry.value_name)
        if not key:
            continue
        purchase[key] = purchase.get(key, 0) + 1  # recipes included (OD parity)
        if key.startswith("recipe_"):
            continue
        seconds = _entry_game_seconds(entry, game_start_tick)
        if key not in first_purchase_time:
            first_purchase_time[key] = seconds
        # OpenDota's purchase_time is the SUM of every purchase time for the item
        # (a quirk of its additive map handler), not the latest buy. Match it for
        # parity. first_purchase_time stays the earliest buy. Verified against
        # fixture 8855188139: clarity=3696=sum([470,660,706,795,1065]).
        purchase_time[key] = purchase_time.get(key, 0) + seconds
    return {
        "purchase": purchase,
        "purchase_time": purchase_time,
        "first_purchase_time": first_purchase_time,
        "purchase_tpscroll": purchase.get("tpscroll", 0),
        "purchase_ward_observer": purchase.get("ward_observer", 0),
        "purchase_ward_sentry": purchase.get("ward_sentry", 0),
    }


# Source 2 world coordinates are ``cell * 128 + vec``; OpenDota reports ward
# positions in cell units (``(cell*128 + vec) / 128``). gem's WardEvent keeps the
# raw world coordinate for its own spatial helpers, so OD-shaped ward outputs
# divide by this to match. Reference: refs/parser/Parse.java getPreciseLocation.
_WORLD_UNITS_PER_CELL = 128.0


def _to_od_cell(world: float | None) -> float | None:
    """Convert a raw world coordinate to OpenDota's cell-unit coordinate."""
    if world is None:
        return None
    return world / _WORLD_UNITS_PER_CELL


def _ward_coord_key(x: float | None, y: float | None) -> str | None:
    """Return OpenDota's ``"[x,y]"`` cell-rounded coordinate key for a ward.

    World coordinates are converted to OpenDota cell units and rounded to the
    nearest integer, matching OpenDota's ``key`` and the nested ``obs``/``sen``
    map keys (which keep the float coordinate separately).

    Args:
        x: Raw world x coordinate, or ``None``.
        y: Raw world y coordinate, or ``None``.

    Returns:
        ``"[<round(cell_x)>,<round(cell_y)>]"``, or ``None`` if a coord is missing.
    """
    cx, cy = _to_od_cell(x), _to_od_cell(y)
    if cx is None or cy is None:
        return None
    return f"[{round(cx)},{round(cy)}]"


def _ward_left_entry(ward: WardEvent, game_start_tick: int | None) -> dict[str, Any] | None:
    """Build an OpenDota ``*_left_log`` expiry entry from a WardEvent, or None.

    A ward that left the map (killed or expired naturally) yields one expiry
    record; wards still alive at game end yield ``None``. ``attackername`` is the
    killer for a destroyed ward and empty for a natural expiry.

    Args:
        ward: The ward placement record.
        game_start_tick: Absolute tick of the game clock start, or ``None``.

    Returns:
        The OpenDota-shaped expiry dict, or ``None`` if the ward never left.
    """
    left_tick = ward.killed_tick if ward.killed_tick is not None else ward.expires_tick
    if left_tick is None:
        return None
    seconds = (left_tick - game_start_tick) // 30 if game_start_tick is not None else 0
    return {
        "time": seconds,
        "type": "obs_left_log" if ward.ward_type == "observer" else "sen_left_log",
        "key": _ward_coord_key(ward.x, ward.y),
        "slot": ward.player_id,
        "player_slot": _player_id_to_player_slot(ward.player_id),
        "x": _to_od_cell(ward.x),
        "y": _to_od_cell(ward.y),
        "entityleft": True,
        "attackername": ward.killer or "",
    }


def _build_objectives(
    obj_ext: ObjectivesExtractor,
    combat_agg: _CombatAggregator,
    first_blood_entry: CombatLogEntry | None,
    pid_to_team: dict[int, int],
    game_start_tick: int | None,
) -> list[dict[str, Any]]:
    """Merge gem's per-type objective events into OpenDota's unified timeline.

    Produces the ``objectives`` list OpenDota exposes: ``building_kill`` plus the
    ``CHAT_MESSAGE_*`` events, each ``{time, type, ...}`` with type-specific
    fields, sorted chronologically. Killer heroes are resolved to OpenDota
    ``slot``/``player_slot`` via the combat aggregator's name→id map.

    Args:
        obj_ext: The objectives extractor (towers, roshans, aegis, etc.).
        combat_agg: Combat aggregator, for killer-hero → player id resolution.
        first_blood_entry: The first real hero-death entry, or ``None``.
        pid_to_team: Map of player id (0-9) → team (2/3), for courier ownership.
        game_start_tick: Absolute tick of the game clock start, or ``None``.

    Returns:
        Chronologically-sorted list of OpenDota-shaped objective dicts.
    """
    objectives: list[dict[str, Any]] = []

    def secs(tick: int) -> int:
        return _tick_game_seconds(tick, game_start_tick)

    def slot_fields(player_id: int | None) -> dict[str, Any]:
        if not isinstance(player_id, int) or not (0 <= player_id < 10):
            return {}
        return {"slot": player_id, "player_slot": _player_id_to_player_slot(player_id)}

    # building_kill — towers and barracks, attributed source-first (a summon /
    # projectile killer carries the owning hero in killer_source). unit is the
    # crediting source unit when present, mirroring OpenDota.
    for tk in obj_ext.tower_kills:
        pid = combat_agg.resolve_kill_pid(tk.killer_source, tk.killer)
        objectives.append(
            {
                "time": secs(tk.tick),
                "type": "building_kill",
                "key": tk.tower_name,
                "unit": tk.killer_source or tk.killer,
                **slot_fields(pid),
            }
        )
    for bk in obj_ext.barracks_kills:
        pid = combat_agg.resolve_kill_pid(bk.killer_source, bk.killer)
        objectives.append(
            {
                "time": secs(bk.tick),
                "type": "building_kill",
                "key": bk.barracks_name,
                "unit": bk.killer_source or bk.killer,
                **slot_fields(pid),
            }
        )

    # CHAT_MESSAGE_ROSHAN_KILL — team that killed Roshan (killer's team).
    for rk in obj_ext.roshan_kills:
        pid = combat_agg.resolve_kill_pid(rk.killer_source, rk.killer)
        team = pid_to_team.get(pid) if pid is not None else None
        entry: dict[str, Any] = {"time": secs(rk.tick), "type": "CHAT_MESSAGE_ROSHAN_KILL"}
        if team is not None:
            entry["team"] = team
        objectives.append(entry)

    # CHAT_MESSAGE_AEGIS / _AEGIS_STOLEN / _DENIED_AEGIS.
    _aegis_type = {
        "pickup": "CHAT_MESSAGE_AEGIS",
        "stolen": "CHAT_MESSAGE_AEGIS_STOLEN",
        "denied": "CHAT_MESSAGE_DENIED_AEGIS",
    }
    for ae in obj_ext.aegis_events:
        pid = ae.player_id if 0 <= ae.player_id < 10 else None
        objectives.append(
            {
                "time": secs(ae.tick),
                "type": _aegis_type.get(ae.event_type, "CHAT_MESSAGE_AEGIS"),
                **slot_fields(pid),
            }
        )

    # CHAT_MESSAGE_MINIBOSS_KILL — Tormentor, by killing player + their team.
    for tm in obj_ext.tormentor_kills:
        pid = tm.killer_player_id if 0 <= tm.killer_player_id < 10 else None
        entry = {"time": secs(tm.tick), "type": "CHAT_MESSAGE_MINIBOSS_KILL", **slot_fields(pid)}
        team = pid_to_team.get(pid) if pid is not None else None
        if team is not None:
            entry["team"] = team
        objectives.append(entry)

    # CHAT_MESSAGE_FIRSTBLOOD — the first real hero death; key is the victim slot.
    if first_blood_entry is not None:
        # Resolve the killer source-first (like every other objective): a summon
        # or projectile first blood carries the owning hero in damage_source_name
        # while attacker_name is the non-hero unit.
        killer_pid = combat_agg.resolve_kill_pid(
            first_blood_entry.damage_source_name, first_blood_entry.attacker_name
        )
        victim_pid = combat_agg._hero_to_pid(first_blood_entry.target_name)
        entry = {
            "time": _entry_game_seconds(first_blood_entry, game_start_tick),
            "type": "CHAT_MESSAGE_FIRSTBLOOD",
            **slot_fields(killer_pid),
        }
        if victim_pid is not None:
            entry["key"] = str(victim_pid)
        objectives.append(entry)

    # CHAT_MESSAGE_COURIER_LOST — team is the courier's owner (killer's opposite).
    for cd in obj_ext.courier_deaths:
        killer_pid = combat_agg.resolve_kill_pid(cd.killer_source, cd.killer)
        killer_team = pid_to_team.get(killer_pid) if killer_pid is not None else None
        entry = {"time": secs(cd.tick), "type": "CHAT_MESSAGE_COURIER_LOST"}
        if killer_team in (2, 3):
            entry["team"] = 3 if killer_team == 2 else 2  # owner = opposite of killer
        if killer_pid is not None:
            entry["killer"] = _player_id_to_player_slot(killer_pid)
        objectives.append(entry)

    objectives.sort(key=lambda o: o["time"])
    return objectives


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


def _radiant_adv_from_intervals(
    interval_ext: IntervalExtractor | None,
) -> tuple[list[int], list[int]] | None:
    """Build Radiant gold/XP advantage from OpenDota-style interval snapshots."""
    batches = _complete_interval_batches(interval_ext)
    if batches is None:
        return None

    gold_adv: list[int] = []
    xp_adv: list[int] = []
    for by_player in batches:
        gold = 0
        xp = 0
        for snap in by_player.values():
            sign = 1 if snap.team == 2 else -1
            gold += sign * snap.gold
            xp += sign * snap.xp
        gold_adv.append(gold)
        xp_adv.append(xp)

    return gold_adv, xp_adv


_MINUTE_TICKS = 1800  # 60 s * 30 ticks/s


def _radiant_adv_from_minute_series(
    players: list[ParsedPlayer],
) -> tuple[list[int], list[int]] | None:
    """Build Radiant gold/XP advantage from dense per-player minute series.

    Fallback for when no complete interval batches exist. Buckets each player's
    samples by their *actual* game minute (derived from ``times_min``), not by
    list position — ``minute_time_series`` drops missing minutes, so a player who
    lacks an early sample would otherwise have their whole curve shifted earlier.
    Mirrors OpenDota's bucket-by-time sum in
    ``CreateParsedDataBlob.processAllPlayers``: at each minute a player
    contributes their last-known total-earned value (monotonic; carried forward
    past a stopped/leaver sample) and 0 before their first sample.

    Args:
        players: The parsed players, each with ``times_min`` and the
            ``total_earned_gold_t_min`` / ``total_earned_xp_t_min`` minute arrays.

    Returns:
        ``(gold_adv, xp_adv)`` lists, or ``None`` if no player has minute data.
    """
    active = [pp for pp in players if pp.total_earned_gold_t_min and pp.total_earned_xp_t_min]
    if not active:
        return None

    # Map each player's samples to absolute minute indices using times_min. The
    # global origin is the earliest sample tick across players, so a player who
    # first appears at minute 1 lands at index 1, not 0. Fall back to 0 when no
    # player has tick data (positional indexing kicks in per-player below).
    first_ticks = [pp.times_min[0] for pp in active if pp.times_min]
    origin = min(first_ticks) if first_ticks else 0

    def _minute_index(tick: int) -> int:
        return max(0, round((tick - origin) / _MINUTE_TICKS))

    # Per-player minute → (gold, xp), keyed by absolute minute.
    per_player: list[tuple[int, dict[int, tuple[int, int]]]] = []
    last_minute = 0
    for pp in active:
        sign = 1 if pp.team == 2 else -1  # 2=Radiant, 3=Dire
        by_minute: dict[int, tuple[int, int]] = {}
        ticks = pp.times_min
        gold_series = pp.total_earned_gold_t_min
        xp_series = pp.total_earned_xp_t_min
        n = min(len(ticks), len(gold_series), len(xp_series))
        for i in range(n):
            minute = _minute_index(ticks[i])
            by_minute[minute] = (gold_series[i], xp_series[i])
            last_minute = max(last_minute, minute)
        # A player with no times_min falls back to positional indexing so we never
        # silently drop their contribution.
        if not ticks:
            for i in range(min(len(gold_series), len(xp_series))):
                by_minute[i] = (gold_series[i], xp_series[i])
                last_minute = max(last_minute, i)
        per_player.append((sign, by_minute))

    n_minutes = last_minute + 1
    gold_adv = [0] * n_minutes
    xp_adv = [0] * n_minutes
    for sign, by_minute in per_player:
        carry_gold = 0
        carry_xp = 0
        for minute in range(n_minutes):
            if minute in by_minute:
                carry_gold, carry_xp = by_minute[minute]
            # Before a player's first sample carry_* stays 0 (no contribution);
            # after their last sample it holds the final monotonic value.
            gold_adv[minute] += sign * carry_gold
            xp_adv[minute] += sign * carry_xp
    return gold_adv, xp_adv


def _complete_interval_batches(
    interval_ext: IntervalExtractor | None,
) -> list[dict[int, IntervalSnapshot]] | None:
    """Return complete interval batches keyed by player id.

    Partial batches are ignored because missing one player's interval sample
    would silently skew both player-minute tables and match advantage curves.
    """
    if interval_ext is None:
        return None

    raw_snapshots = getattr(interval_ext, "all_snapshots", None)
    if raw_snapshots is None:
        raw_snapshots = getattr(interval_ext, "snapshots", [])
    snapshots: list[IntervalSnapshot] = list(raw_snapshots)
    if not snapshots:
        return None

    expected_players = {
        snap.player_id for snap in snapshots if snap.team in (2, 3) and 0 <= snap.player_id < 10
    }
    if not expected_players:
        return None

    by_time: defaultdict[int, dict[int, IntervalSnapshot]] = defaultdict(dict)
    for snap in snapshots:
        if snap.time_s < 0 or snap.team not in (2, 3):
            continue
        by_time[snap.time_s][snap.player_id] = snap

    batches: list[dict[int, IntervalSnapshot]] = []
    for time_s in sorted(by_time):
        by_player = by_time[time_s]
        if set(by_player) != expected_players:
            continue
        batches.append(by_player)

    if not batches:
        return None
    return batches


def _interval_series_by_player(
    interval_ext: IntervalExtractor | None,
) -> dict[int, IntervalTimeSeries]:
    """Build complete OpenDota-style player minute arrays from interval snapshots."""
    from gem.extractors.intervals import IntervalTimeSeries

    batches = _complete_interval_batches(interval_ext)
    if batches is None:
        return {}

    player_ids = sorted(batches[0])
    series = {player_id: IntervalTimeSeries(player_id=player_id) for player_id in player_ids}

    for by_player in batches:
        for player_id in player_ids:
            snap = by_player[player_id]
            ts = series[player_id]
            ts.ticks.append(snap.tick)
            ts.times.append(snap.time_s)
            ts.gold_t.append(snap.gold)
            ts.xp_t.append(snap.xp)
            ts.lh_t.append(snap.lh)
            ts.dn_t.append(snap.dn)
            ts.net_worth_t.append(snap.net_worth)

    return series


def _populate_player_series(
    match: ParsedMatch,
    *,
    player_ext: PlayerExtractor,
    combat_agg: _CombatAggregator,
    interval_ext: IntervalExtractor | None,
    interval_min_series: dict[int, IntervalTimeSeries],
    game_start_tick: int | None,
    radiant_win: bool | None,
) -> None:
    """Populate per-player time series and combat-log aggregates in place.

    Iterates the ten player slots and overlays each ``match.players[player_id]``
    with its dense/minute time series, combat-log attribution, kill aggregates,
    lane stats, terminal scalars, final inventory, and OpenDota-style computed
    fields. Each iteration is independent (no cross-player state), so the loop is
    a straight single-pass population of one ``ParsedPlayer`` per slot.

    Extracted verbatim from ``build_parsed_match`` (issue #106 item #3) to keep
    the orchestrator readable; behaviour is unchanged.

    Args:
        match: The match being assembled; ``match.players`` is mutated in place.
        player_ext: Source of per-player snapshots / time series / scoreboard.
        combat_agg: Per-player combat-log aggregates.
        interval_ext: OpenDota-style interval extractor (team counters, scalars).
        interval_min_series: Complete interval minute arrays by player id.
        game_start_tick: Horn tick used for the lane-window time filter.
        radiant_win: Resolved match winner, or ``None`` if unknown.
    """
    for player_id in range(10):
        ts = player_ext.time_series(player_id)
        mts = player_ext.minute_time_series(player_id)
        pp = match.players[player_id]
        pp.player_id = player_id
        pp.times = ts.ticks
        pp.gold_t = ts.gold_t
        pp.total_earned_gold_t = ts.total_earned_gold_t
        pp.net_worth_t = ts.net_worth_t
        pp.lh_t = ts.lh_t
        pp.dn_t = ts.dn_t
        pp.xp_t = ts.xp_t
        interval_ts = interval_min_series.get(player_id)
        if interval_ts is not None:
            # OpenDota interval records use cumulative earned gold/XP for
            # gold_t/xp_t. Mirror that on the minute arrays when complete
            # interval batches are available; keep dense series unchanged.
            pp.times_min = interval_ts.ticks
            pp.gold_t_min = interval_ts.gold_t
            pp.total_earned_gold_t_min = interval_ts.gold_t
            pp.total_earned_xp_t_min = interval_ts.xp_t
            pp.net_worth_t_min = interval_ts.net_worth_t
            pp.lh_t_min = interval_ts.lh_t
            pp.dn_t_min = interval_ts.dn_t
            pp.xp_t_min = interval_ts.xp_t
        else:
            pp.times_min = mts.ticks
            pp.gold_t_min = mts.gold_t
            pp.total_earned_gold_t_min = mts.total_earned_gold_t
            pp.total_earned_xp_t_min = mts.total_earned_xp_t
            pp.net_worth_t_min = mts.net_worth_t
            pp.lh_t_min = mts.lh_t
            pp.dn_t_min = mts.dn_t
            pp.xp_t_min = mts.xp_t
        pp.total_hero_damage_t_min = mts.total_hero_damage_t
        pp.total_hero_healing_t_min = mts.total_hero_healing_t
        pp.total_deaths_t_min = mts.total_deaths_t
        pp.total_stuns_t_min = mts.total_stuns_t
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
            pp.damage_by_type = agg.damage_by_type
            pp.damage_taken_by_type = agg.damage_taken_by_type
            # OpenDota per-inflictor / per-target attribution breakdowns. Nested
            # defaultdicts are flattened to plain dicts for clean serialization.
            pp.damage_inflictor = dict(agg.damage_inflictor)
            pp.damage_inflictor_received = dict(agg.damage_inflictor_received)
            pp.damage_targets = {k: dict(v) for k, v in agg.damage_targets.items()}
            pp.ability_targets = {k: dict(v) for k, v in agg.ability_targets.items()}
            pp.hero_hits = dict(agg.hero_hits)
            pp.max_hero_hit = agg.max_hero_hit
            pp.healing = agg.healing
            pp.ability_uses = agg.ability_uses
            pp.item_uses = agg.item_uses
            pp.gold_reasons = agg.gold_reasons
            pp.xp_reasons = agg.xp_reasons
            pp.kills_log = agg.kills_log
            # Chronological order, keeping every per-unit entry but EXCLUDING
            # recipes — matching OpenDota's purchase_log (CreateParsedDataBlob
            # filters key.startsWith("recipe_") out of the log while still counting
            # recipes in the `purchase` map). OpenDota does NOT dedup starting items
            # (its log genuinely lists e.g. 2x faerie_fire), so collapsing
            # same-(tick, item) entries here under-counted starting consumables.
            sorted_purchases = sorted(agg.purchase_log, key=lambda e: e.tick)
            pp.purchase_log = [
                entry
                for entry in sorted_purchases
                if not (opendota_translate(entry.value_name) or "").startswith("recipe_")
            ]
            # Aggregates are derived from the FULL log (with recipes): the `purchase`
            # count map includes recipes, while purchase_time/first_purchase_time
            # exclude them. _build_purchase_aggregates handles that split internally.
            purchase_aggs = _build_purchase_aggregates(sorted_purchases, game_start_tick)
            pp.purchase = purchase_aggs["purchase"]
            pp.purchase_time = purchase_aggs["purchase_time"]
            pp.first_purchase_time = purchase_aggs["first_purchase_time"]
            pp.purchase_tpscroll = purchase_aggs["purchase_tpscroll"]
            pp.purchase_ward_observer = purchase_aggs["purchase_ward_observer"]
            pp.purchase_ward_sentry = purchase_aggs["purchase_ward_sentry"]
            # Ward-use scalars: item_uses keys keep the item_ prefix.
            pp.observer_uses = agg.item_uses.get("item_ward_observer", 0)
            pp.sentry_uses = agg.item_uses.get("item_ward_sentry", 0)
            pp.runes_log = agg.runes_log
            pp.buyback_log = agg.buyback_log
            # Structured buybacks with an estimated cost. The per-buyback cost is
            # not in the replay stream, so it is derived from net worth at the
            # buyback tick (200 + net_worth // 13); net_worth_t is already
            # populated above, so net_worth_at() resolves the nearest sample.
            buybacks: list[BuybackEvent] = []
            for entry in agg.buyback_log:
                nw = net_worth_at(pp, entry.tick)
                buybacks.append(
                    BuybackEvent(
                        tick=entry.tick,
                        player_slot=player_id,
                        net_worth=nw,
                        cost=buyback_cost(nw),
                    )
                )
            pp.buybacks = buybacks
            pp.stuns_dealt = agg.stuns_dealt
            # OpenDota-style combat scalars (combat-log reconstruction; exact via
            # apply_api_rates). Best-effort offline estimates.
            pp.hero_damage = agg.hero_damage
            pp.tower_damage = agg.tower_damage
            pp.hero_healing = agg.hero_healing

        # OpenDota-shaped kill aggregates, derived from kills_log above.
        pp.killed = killed_counts(pp.kills_log)
        kill_cats = categorize_kills(pp.killed)
        pp.ancient_kills = kill_cats.ancient_kills
        pp.neutral_kills = kill_cats.neutral_kills
        pp.lane_kills = kill_cats.lane_kills
        pp.courier_kills = kill_cats.courier_kills
        pp.observer_kills = kill_cats.observer_kills
        pp.sentry_kills = kill_cats.sentry_kills
        pp.roshan_kills = kill_cats.roshan_kills

        kda = player_ext.scoreboard.get(player_id)
        if kda is not None:
            pp.kills, pp.deaths, pp.assists = kda

        # Lane position heatmap — restricted to first 10 game-minutes (OpenDota: t<=600s).
        # position_log above is left unfiltered; this loop is separate and independent.
        lane_pos: defaultdict[str, int] = defaultdict(int)
        for snap in player_ext.snapshots:
            if snap.player_id != player_id or snap.x is None or snap.y is None:
                continue
            if game_start_tick is not None and (
                snap.tick < game_start_tick or snap.tick > game_start_tick + _LANE_WINDOW
            ):
                continue
            lane_pos[f"{int(snap.x) // _LANE_GRID}_{int(snap.y) // _LANE_GRID}"] += 1
        pp.lane_pos = lane_pos

        # Lane role and 10-minute raw stats
        pp.lane_role = classify_lane(pp.lane_pos, pp.team)
        _LM = 10  # minute-series index for the 10-minute mark
        if len(pp.lh_t_min) > _LM:
            pp.lane_last_hits = pp.lh_t_min[_LM]
        if len(pp.dn_t_min) > _LM:
            pp.lane_denies = pp.dn_t_min[_LM]
        if len(pp.total_earned_gold_t_min) > _LM:
            pp.lane_total_gold = pp.total_earned_gold_t_min[_LM]
        if len(pp.total_earned_xp_t_min) > _LM:
            pp.lane_total_xp = pp.total_earned_xp_t_min[_LM]

        # End-of-game terminal scalars: read the LAST DENSE sample (not the last
        # minute boundary, which can lag the game end by up to ~59s). These match
        # OpenDota's terminal net_worth / last_hits / denies to the unit; see the
        # active "[30t]" checks in scripts/validate_opendota.py.
        if pp.net_worth_t:
            pp.net_worth = pp.net_worth_t[-1]
        if pp.lh_t:
            pp.last_hits = pp.lh_t[-1]
        if pp.dn_t:
            pp.denies = pp.dn_t[-1]

        # End-of-game inventory: the items on this player's last dense snapshot
        # (taken at the game-end tick). Mirrors OpenDota's per-slot item_0..5 /
        # backpack / item_neutral, but keyed by slot with names. Use the last
        # snapshot even when its inventory is empty — a player can legitimately
        # end with no items (sold/dropped/destroyed before Ancient death), and
        # filtering on non-empty would copy a stale earlier inventory.
        last_snap = next(
            (snap for snap in reversed(player_ext.snapshots) if snap.player_id == player_id),
            None,
        )
        if last_snap is not None:
            pp.final_items = dict(last_snap.items)
            # Terminal hero level from the last dense snapshot.
            pp.level = last_snap.level

        # Numeric hero_id from the resolved hero NPC name (robust per-player link;
        # avoids the draft pick-order trap). 0 if the hero is absent from the
        # bundled heroes.json snapshot.
        pp.hero_id = hero_id(pp.hero_name) if pp.hero_name else 0

        # gold_spent = total earned gold − current spendable gold (OpenDota parity).
        if pp.total_earned_gold_t and pp.gold_t:
            pp.gold_spent = max(0, pp.total_earned_gold_t[-1] - pp.gold_t[-1])

        # life_state_dead: seconds spent dead. OpenDota samples life_state once per
        # game-second and sums the non-alive samples (states 1 + 2). We mirror that
        # by counting DISTINCT dead game-seconds, which is robust to gem's snapshot
        # cadence (multiple dense samples can fall in one second). Falls back to the
        # tick second when game_time_s is unavailable (S1/early frames).
        dead_seconds: set[int] = set()
        for snap in player_ext.snapshots:
            if snap.player_id != player_id or snap.life_state == 0:
                continue
            sec = snap.game_time_s if snap.game_time_s is not None else snap.tick // 30
            dead_seconds.add(sec)
        pp.life_state_dead = len(dead_seconds)

        # Terminal team-data counters (camps/creeps stacked, wards placed, rune
        # pickups, tower kills) read from the same m_vecDataTeam entry as gold/xp.
        # The last observed value is the end-of-game total; each matches OpenDota's
        # per-player scalar to the unit. (m_iRoshanKills is intentionally NOT used
        # here — it disagrees with OpenDota's combat-log-attributed roshan_kills.)
        if interval_ext is not None:
            counters = interval_ext.team_counters(player_id)
            pp.camps_stacked = counters["camps_stacked"]
            pp.creeps_stacked = counters["creeps_stacked"]
            pp.obs_placed = counters["obs_placed"]
            pp.sen_placed = counters["sen_placed"]
            pp.rune_pickups = counters["rune_pickups"]
            pp.tower_kills = counters["tower_kills"]

        # firstblood_claimed: authoritative CDOTA_PlayerResource flag (the field
        # OpenDota reads), not a combat-log reconstruction.
        if interval_ext is not None:
            pp.firstblood_claimed = int(
                interval_ext.player_resource_scalars(player_id)["firstblood_claimed"]
            )

        # OpenDota-style computed convenience fields (no duration dependency).
        # kda uses a +1 denominator and 2-decimal rounding, matching OpenDota.
        pp.kda = round((pp.kills + pp.assists) / (pp.deaths + 1), 2)
        pp.buyback_count = len(pp.buyback_log)
        pp.is_radiant = pp.team == 2  # 2 = Radiant
        # win is 0 when the winner is unknown (radiant_win is None).
        pp.win = 1 if (radiant_win is not None and pp.is_radiant == radiant_win) else 0
        # kills_per_min uses OpenDota's gameplay duration (match.duration), which
        # is the horn-to-ancient combat-log span — not the raw tick span. 0.0 when
        # duration is unknown.
        if match.duration > 0:
            pp.kills_per_min = pp.kills / (match.duration / 60)

        # Tier-1: lane efficiency % (OpenDota formula, same denominator for all players)
        # Reference: odota/core svc/util/compute.ts
        # melee(40×60) + ranged(45×20) + siege(74×2) + passive(600×1.5) + starting(600) = 4948
        _LANE_GOLD_BASELINE = 4948
        if pp.lane_total_gold > 0:
            pp.lane_efficiency_pct = int(pp.lane_total_gold / _LANE_GOLD_BASELINE * 100)


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
    smoke_events: list[SmokeEvent] | None = None,
    vision_modifier_events: list[VisionModifierEvent] | None = None,
    neutral_item_finds: list[NeutralItemFoundEvent] | None = None,
    interval_ext: IntervalExtractor | None = None,
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
        smoke_events: All :class:`SmokeEvent` objects collected during parse.
        vision_modifier_events: All :class:`VisionModifierEvent` objects collected during parse.
        neutral_item_finds: Neutral item found events collected during parse.
        interval_ext: Optional internal interval extractor used for OpenDota-style
            match-level gold/XP advantage curves.

    Returns:
        Fully populated :class:`ParsedMatch`.
    """
    from gem.extractors.teamfights import detect_opendota_teamfights, detect_teamfights

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
        tormentors=obj_ext.tormentor_kills,
        shrines=obj_ext.shrine_kills,
        banner_plants=obj_ext.banner_plants,
        wards=ward_ext.ward_events,
        combat_log=all_entries,
        chat=chat_entries,
        courier_snapshots=courier_ext.snapshots,
        neutral_item_finds=neutral_item_finds or [],
        smoke_events=smoke_events or [],
        vision_modifiers=vision_modifier_events or [],
        draft=draft_ext.draft_events,
        game_start_tick=parser.game_start_tick,
        game_end_tick=parser.tick,
        duration=getattr(parser, "duration_s", None) or 0,
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

    # Capture game_start_tick once — used for lane_pos time filter below
    game_start_tick = parser.game_start_tick
    interval_min_series = _interval_series_by_player(interval_ext)

    # first_blood_time: game-clock time of the earliest real hero DEATH. Illusion
    # deaths and reincarnation triggers are excluded (target_is_hero stays true for
    # an illusion, so the explicit not-illusion filter is required). The per-player
    # firstblood_claimed flag is read separately from the authoritative
    # CDOTA_PlayerResource field below, not reconstructed from this entry.
    first_blood_entry = next(
        (
            e
            for e in all_entries
            if e.log_type == "DEATH"
            and e.target_is_hero
            and not e.target_is_illusion
            and not e.will_reincarnate
        ),
        None,
    )
    if first_blood_entry is not None:
        if first_blood_entry.game_time_s is not None:
            match.first_blood_time = int(first_blood_entry.game_time_s)
        elif game_start_tick is not None:
            match.first_blood_time = max(0, (first_blood_entry.tick - game_start_tick) // 30)

    # NOTE: pre_game_duration (horn → creep-spawn span, ~90s) is intentionally
    # left at its default 0 here. It requires the GAME_IN_PROGRESS state-transition
    # timestamp, which the parser does not yet expose separately from the clock
    # anchor (m_flGameStartTime is the engine clock zero, not the pre-game span).
    # Tracked as a follow-up rather than shipping a wrong value.

    # Build per-player time series and overlay combat log aggregates.
    _populate_player_series(
        match,
        player_ext=player_ext,
        combat_agg=combat_agg,
        interval_ext=interval_ext,
        interval_min_series=interval_min_series,
        game_start_tick=game_start_tick,
        radiant_win=radiant_win,
    )

    match_metadata = getattr(parser, "match_metadata", None)
    metadata = getattr(match_metadata, "metadata", None)
    for team in getattr(metadata, "teams", []) or []:
        for metadata_player in getattr(team, "players", []) or []:
            metadata_player_id = _metadata_slot_to_player_id(metadata_player.player_slot)
            if metadata_player_id is not None:
                match.players[metadata_player_id].ability_upgrades_arr = list(
                    metadata_player.ability_upgrades
                )

    # Tier-2: lane advantage vs opponents — paired by gold rank within the lane.
    # Players are sorted by lane_total_gold descending within each (team, lane_role)
    # group, then matched by rank: richest vs richest, poorest vs poorest.
    # This fairly pairs carries against carries and supports against supports
    # without requiring an explicit position field.
    # Jungle (4) and roaming (5) are excluded — no direct lane opponent.
    _LANE_ROLES_WITH_OPPONENTS = {1, 2, 3}
    for role in _LANE_ROLES_WITH_OPPONENTS:
        radiant = sorted(
            [pp for pp in match.players if pp.team == 2 and pp.lane_role == role],
            key=lambda p: p.lane_total_gold,
            reverse=True,
        )
        dire = sorted(
            [pp for pp in match.players if pp.team == 3 and pp.lane_role == role],
            key=lambda p: p.lane_total_gold,
            reverse=True,
        )
        for rad, dire_opp in zip(radiant, dire, strict=False):
            rad.lane_gold_adv = rad.lane_total_gold - dire_opp.lane_total_gold
            rad.lane_xp_adv = rad.lane_total_xp - dire_opp.lane_total_xp
            dire_opp.lane_gold_adv = dire_opp.lane_total_gold - rad.lane_total_gold
            dire_opp.lane_xp_adv = dire_opp.lane_total_xp - rad.lane_total_xp

    # Extract player names and Steam IDs from CDOTA_PlayerResource entity.
    # Two field path variants: newer replays use m_vecPlayerData.{slot}.m_iszPlayerName,
    # older replays use m_iszPlayerNames.{slot}.
    # Reference: refs/manta/manta_test.go line ~703, refs/parser/Parse.java line ~602
    _STEAM_ID_BASE = 76561197960265728
    if parser.entity_manager is not None:
        pr = parser.entity_manager.find_by_class_name("CDOTA_PlayerResource")
        if pr is not None:
            for player_id in range(10):
                slot = f"{player_id:04d}"
                name = pr.get_string(f"m_vecPlayerData.{slot}.m_iszPlayerName")
                if not name:
                    name = pr.get_string(f"m_iszPlayerNames.{slot}")
                if name:
                    match.players[player_id].player_name = name
                steam_id = pr.get_uint64(f"m_vecPlayerData.{slot}.m_iPlayerSteamID")
                if not steam_id:
                    steam_id = pr.get_uint64(f"m_iPlayerSteamIDs.{slot}")
                if isinstance(steam_id, int) and steam_id > 0:
                    match.players[player_id].steam_id = steam_id
                    if steam_id > _STEAM_ID_BASE:
                        match.players[player_id].account_id = steam_id - _STEAM_ID_BASE

        # Extract team names and tags from CDOTATeam entities.
        # m_iTeamNum 2 = Radiant, 3 = Dire.
        for ent in parser.entity_manager.entities:
            if ent is None or not ent.active or ent.get_class_name() != "CDOTATeam":
                continue
            team_num = ent.get_int32("m_iTeamNum")
            if team_num == 2:
                match.radiant_team_id = ent.get_uint32("m_unTournamentTeamID") or 0
                match.radiant_team_name = ent.get_string("m_szTeamname") or ""
                match.radiant_team_tag = ent.get_string("m_szTag") or ""
            elif team_num == 3:
                match.dire_team_id = ent.get_uint32("m_unTournamentTeamID") or 0
                match.dire_team_name = ent.get_string("m_szTeamname") or ""
                match.dire_team_tag = ent.get_string("m_szTag") or ""

    # Attach ward logs per player. obs_log/sen_log keep gem's native WardEvent
    # records; the OpenDota-shaped expiry logs (obs_left_log/sen_left_log) and the
    # nested placement coordinate maps (obs/sen) are derived alongside.
    for ward in match.wards:
        if not (0 <= ward.player_id < 10):
            continue
        pp = match.players[ward.player_id]
        left_entry = _ward_left_entry(ward, game_start_tick)
        if ward.ward_type == "observer":
            pp.obs_log.append(ward)
            if left_entry is not None:
                pp.obs_left_log.append(left_entry)
            coord_map = pp.obs
        else:
            pp.sen_log.append(ward)
            if left_entry is not None:
                pp.sen_left_log.append(left_entry)
            coord_map = pp.sen
        cx, cy = _to_od_cell(ward.x), _to_od_cell(ward.y)
        if cx is not None and cy is not None:
            xk, yk = str(round(cx)), str(round(cy))
            coord_map.setdefault(xk, {})[yk] = coord_map.setdefault(xk, {}).get(yk, 0) + 1

    # observers_placed: OpenDota's purchase/log-derived observer count, distinct
    # from the entity-counter obs_placed. Use the per-player obs_log length.
    for pp in match.players:
        pp.observers_placed = len(pp.obs_log)

    # OpenDota-shaped unified objectives timeline + building-status bitmasks.
    pid_to_team = {pp.player_id: pp.team for pp in match.players if pp.team}
    match.objectives = _build_objectives(
        obj_ext, combat_agg, first_blood_entry, pid_to_team, game_start_tick
    )
    match.courier_deaths = obj_ext.courier_deaths
    bitmasks = building_status(obj_ext.tower_kills, obj_ext.barracks_kills)
    match.tower_status_radiant = bitmasks["tower_status_radiant"]
    match.tower_status_dire = bitmasks["tower_status_dire"]
    match.barracks_status_radiant = bitmasks["barracks_status_radiant"]
    match.barracks_status_dire = bitmasks["barracks_status_dire"]

    # Compute radiant_gold_adv / radiant_xp_adv per game-minute boundary.
    # Both curves come from monotonically-increasing total-earned fields
    # (m_iTotalEarnedGold / m_iTotalEarnedXP), never spendable gold or
    # combat-log XP. OpenDota builds these the same way: its interval entries
    # read the team-data entity, and xp_t/gold_t are the minute-boundary
    # downsamples of those entries — combat-log XP only feeds the xp_reasons
    # histogram, not the advantage curves.
    # Reference: refs/parser/src/main/java/opendota/Parse.java interval block
    #   (m_vecDataTeam.%i.m_iTotalEarnedGold/XP) and CreateParsedDataBlob.java
    #   addIntervalData("xp_t"/"gold_t", ...).
    interval_adv = _radiant_adv_from_intervals(interval_ext)
    if interval_adv is not None:
        # Authoritative path: OpenDota-style interval snapshots are complete.
        gold_adv, xp_adv = interval_adv
        match.radiant_gold_adv = gold_adv
        match.radiant_xp_adv = xp_adv
    else:
        # Fallback path: no complete interval batches were observed, so derive
        # the curves from the dense player minute series' total-earned arrays.
        minute_adv = _radiant_adv_from_minute_series(match.players)
        if minute_adv is not None:
            match.radiant_gold_adv, match.radiant_xp_adv = minute_adv

    # Detect teamfights (Phase 9)
    hero_to_slot = {pp.hero_name: pp.player_id for pp in match.players if pp.hero_name}
    slot_to_team = {pp.player_id: pp.team for pp in match.players if pp.team}
    player_snaps: dict[int, Any] = {
        pid: [s for s in player_ext.snapshots if s.player_id == pid] for pid in range(10)
    }
    match.teamfights = detect_teamfights(
        all_entries,
        hero_to_slot=hero_to_slot,
        player_snapshots=player_snaps,
        slot_to_team=slot_to_team,
    )
    match.opendota_teamfights = detect_opendota_teamfights(
        all_entries,
        hero_to_slot=hero_to_slot,
        player_snapshots=player_snaps,
        game_start_tick=match.game_start_tick,
        duration_s=match.duration or None,
    )

    # teamfight_participation: read the authoritative game-computed value from
    # CDOTA_PlayerResource.m_flTeamFightParticipation — the exact field OpenDota
    # reads (Parse.java), not a teamfight-window reconstruction (which OpenDota
    # itself does not do, and which can't match the engine's metric).
    if interval_ext is not None:
        for player_id in range(10):
            scalars = interval_ext.player_resource_scalars(player_id)
            match.players[player_id].teamfight_participation = round(
                scalars["teamfight_participation"], 7
            )

    # Team kill scores = sum of each side's player kills (OpenDota parity).
    match.radiant_score = sum(pp.kills for pp in match.players if pp.team == 2)
    match.dire_score = sum(pp.kills for pp in match.players if pp.team == 3)

    # Build per-player ability level snapshots for ability_level_at_tick().
    # Collect (tick, ability_levels) pairs from minute-boundary snapshots,
    # sorted by tick, and attach as _ability_snapshots on each ParsedPlayer.
    for player_id in range(10):
        snaps = sorted(
            (s for s in player_ext.snapshots if s.player_id == player_id and s.ability_levels),
            key=lambda s: s.tick,
        )
        ability_snapshots: list[tuple[int, dict[str, int]]] = [
            (s.tick, s.ability_levels) for s in snaps
        ]
        match.players[player_id]._ability_snapshots = ability_snapshots

    return match
