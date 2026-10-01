"""Match assembly — wires extractor outputs into a :class:`ParsedMatch`.

Takes the raw extractor state after a completed parse and builds the fully
populated :class:`ParsedMatch` returned by :func:`gem.parse`.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from gem.analysis import net_worth_at
from gem.catalog import hero_id
from gem.combat.log import opendota_translate
from gem.extractors._cells import WORLD_UNITS_PER_CELL, od_cell_index
from gem.extractors.intervals import LEDGER_FIELDS
from gem.extractors.lane import assign_lane
from gem.extractors.players import LANE_WINDOW_S
from gem.results.derived import (
    building_status,
    buyback_cost,
    categorize_kills,
    float32_json,
    kda,
    killed_counts,
)
from gem.results.models import BuybackEvent, GoldLedger, GoldLedgerSnapshot, ParsedMatch
from gem.results.permanent_buffs import permanent_buff_flags

if TYPE_CHECKING:
    from gem.combat.aggregator import _CombatAggregator
    from gem.combat.log import CombatLogEntry
    from gem.extractors.courier import CourierExtractor
    from gem.extractors.draft import DraftExtractor
    from gem.extractors.gold_ledger import BuybackSpend
    from gem.extractors.intervals import IntervalExtractor, IntervalSnapshot, IntervalTimeSeries
    from gem.extractors.objectives import ObjectivesExtractor
    from gem.extractors.players import PlayerExtractor
    from gem.extractors.wards import WardEvent, WardsExtractor
    from gem.parser import ReplayParser
    from gem.proto.dota_gcmessages_common_pb2 import CMsgDOTAMatch
    from gem.results.models import (
        ChatEntry,
        EntityVisibilityEvent,
        HeroVisibilityEvent,
        NeutralItemFoundEvent,
        ParsedPlayer,
        SmokeEvent,
        VisionModifierEvent,
        VisionModifierPairingIssue,
    )
    from gem.state.game_clock import GameClock


def _player_slot_to_player_id(player_slot: int) -> int | None:
    """Convert a Dota player slot to a gem player id."""
    if 0 <= player_slot <= 4:
        return player_slot
    if 128 <= player_slot <= 132:
        return 5 + (player_slot - 128)
    return None


def _player_id_to_player_slot(player_id: int) -> int:
    """Convert a gem player id (0-9) to OpenDota's ``player_slot`` encoding.

    OpenDota encodes Radiant players as ``0-4`` and Dire players as ``128-132``
    in ``player_slot`` fields, while the ``slot`` field stays ``0-9``. This is the
    inverse of :func:`_player_slot_to_player_id`.

    Args:
        player_id: gem logical player id, 0-9 (0-4 Radiant, 5-9 Dire).

    Returns:
        The OpenDota ``player_slot`` (0-4 for Radiant, 128-132 for Dire).
    """
    return player_id if player_id < 5 else 128 + (player_id - 5)


def _apply_match_details_scalars(match: ParsedMatch, details: CMsgDOTAMatch | None) -> None:
    """Overlay exact terminal scalars from the replay's postgame summary.

    Proto2 presence checks are intentional: an explicitly encoded zero is an
    authoritative result, while an absent scalar leaves the existing replay
    reconstruction/default untouched. A present player summary makes its
    repeated ``permanent_buffs`` list authoritative even when empty. Internal
    per-field provenance lets the validator distinguish these exact values from
    fallbacks without changing the public serialized output.
    """
    if details is None:
        return
    if details.HasField("duration"):
        match._match_details_fields.add("duration")

    for source in details.players:
        if not source.HasField("player_slot"):
            continue
        player_id = _player_slot_to_player_id(source.player_slot)
        if player_id is None or player_id >= len(match.players):
            continue

        player = match.players[player_id]
        buff_flags = permanent_buff_flags(
            int(buff.permanent_buff)
            for buff in source.permanent_buffs
            if buff.HasField("permanent_buff")
        )
        for field_name, value in buff_flags.items():
            setattr(player, field_name, value)
            player._match_details_fields.add(field_name)

        for field_name in (
            "hero_damage",
            "tower_damage",
            "hero_healing",
            "gold_spent",
            "gold",
            "net_worth",
        ):
            if source.HasField(field_name):
                setattr(player, field_name, int(getattr(source, field_name)))
                player._match_details_fields.add(field_name)

        if source.HasField("gold_per_min"):
            player.gold_per_min = int(source.gold_per_min)
            player.total_gold = (player.gold_per_min * match.duration) // 60
            player._match_details_fields.add("gold_per_min")
            if "duration" in match._match_details_fields:
                player._match_details_fields.add("total_gold")
        if source.HasField("xp_per_min"):
            player.xp_per_min = int(source.xp_per_min)
            player.total_xp = (player.xp_per_min * match.duration) // 60
            player._match_details_fields.add("xp_per_min")
            if "duration" in match._match_details_fields:
                player._match_details_fields.add("total_xp")


# (CMsgDOTAMatch field, ParsedMatch attribute) for match-level summary scalars.
_MATCH_DETAILS_MATCH_SCALARS = (
    ("first_blood_time", "first_blood_time"),
    ("pre_game_duration", "pre_game_duration"),
    ("radiant_team_score", "radiant_score"),
    ("dire_team_score", "dire_score"),
)


def _apply_match_details_match_scalars(match: ParsedMatch, details: CMsgDOTAMatch | None) -> None:
    """Overlay the postgame summary's first blood, pre-game and score values.

    These are the Game Coordinator values OpenDota reports as
    ``first_blood_time``, ``pre_game_duration``, ``radiant_score`` and
    ``dire_score`` (equal on every local fixture). A present field, including an
    explicit zero, replaces the replay reconstruction; an absent one keeps it.
    """
    if details is None:
        return
    for source_field, attr in _MATCH_DETAILS_MATCH_SCALARS:
        if details.HasField(source_field):
            setattr(match, attr, int(getattr(details, source_field)))
            match._match_details_fields.add(attr)


def _tick_game_seconds(tick: int, clock: GameClock) -> int:
    """Return an absolute tick's pause-aware game-relative time in seconds.

    Args:
        tick: Absolute parser tick.
        clock: Pause-aware game clock for the match.

    Returns:
        Game-relative seconds (negative pre-horn), or ``0`` with no clock ref.
    """
    seconds = clock.game_seconds_at(tick)
    return 0 if seconds is None else seconds


def _entry_game_seconds(entry: CombatLogEntry, clock: GameClock) -> int:
    """Return a combat-log entry's game-relative time in seconds.

    Prefers the OpenDota-aligned ``game_time_s`` when present, falling back to the
    pause-aware game clock at the entry's tick. Pre-horn events keep their
    negative offset, matching OpenDota.

    Args:
        entry: The combat log entry.
        clock: Pause-aware game clock for the match.

    Returns:
        Game-relative seconds (may be negative for pre-horn events), or ``0``
        when no clock reference is available.
    """
    if entry.game_time_s is not None:
        return int(entry.game_time_s)
    return _tick_game_seconds(entry.tick, clock)


def _count_only_purchase(key: str) -> bool:
    """Return whether a purchase counts in ``purchase`` but stays out of the log.

    OpenDota removes recipes and ``ward_dispenser`` from ``purchase_log`` before
    deriving ``purchase_time`` / ``first_purchase_time``, and keeps both in the
    ``purchase`` count map. The combat log emits a ``ward_dispenser`` purchase
    whenever an observer and a sentry ward merge, so it is not a real purchase.

    Reference: odota/core svc/util/compute.ts ``computeMatchData`` (read at
    7b4256f; odota/core is not one of the pinned parsers). The parity fixtures'
    OpenDota JSON confirms both halves.

    Args:
        key: OpenDota item key (``item_`` stripped).

    Returns:
        True for recipes and ``ward_dispenser``.
    """
    return key.startswith("recipe_") or key == "ward_dispenser"


def _build_purchase_aggregates(
    purchase_log: list[CombatLogEntry], clock: GameClock
) -> dict[str, Any]:
    """Derive OpenDota purchase-timeline aggregates from a player's purchase log.

    Mirrors OpenDota's semantics: the ``purchase`` count map includes recipes
    and ``ward_dispenser``; ``purchase_time`` / ``first_purchase_time`` (and the
    per-item scalars) exclude them (see :func:`_count_only_purchase`). Item
    names are translated (``item_`` stripped); times are game-seconds.

    Args:
        purchase_log: The player's deduped PURCHASE ``CombatLogEntry`` list.
        clock: Pause-aware game clock for the match.

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
        purchase[key] = purchase.get(key, 0) + 1  # recipes, dispensers included
        if _count_only_purchase(key):
            continue
        seconds = _entry_game_seconds(entry, clock)
        # OpenDota tests `!first_purchase_time[k]`, and 0 is falsy in JavaScript,
        # so a purchase at exactly 0:00 is replaced by the item's next purchase.
        # Reference: odota/core svc/util/compute.ts computeMatchData (7b4256f).
        if not first_purchase_time.get(key):
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
# divide by this to match. Reference: odota/parser Parse.java getPreciseLocation.


def _to_od_cell(world: float | None) -> float | None:
    """Convert a raw world coordinate to OpenDota's cell-unit coordinate."""
    if world is None:
        return None
    return world / WORLD_UNITS_PER_CELL


def _ward_coord_key(x: float | None, y: float | None) -> str | None:
    """Return OpenDota's ``"[x,y]"`` cell-rounded coordinate key for a ward.

    Rounds as OpenDota does: to one decimal, then half up (see
    :mod:`gem.extractors._cells`). This key also indexes the nested
    ``obs``/``sen`` maps.

    Args:
        x: Raw world x coordinate, or ``None``.
        y: Raw world y coordinate, or ``None``.

    Returns:
        ``"[<cell_x>,<cell_y>]"``, or ``None`` if a coord is missing.
    """
    if x is None or y is None:
        return None
    return f"[{od_cell_index(x)},{od_cell_index(y)}]"


def _lane_pos(samples: list[tuple[int, float, float]]) -> dict[str, dict[str, int]]:
    """Count lane samples per OpenDota map cell as ``{x: {y: count}}``.

    OpenDota rounds in-game samples to one decimal before keying them and
    pre-horn samples only once (see :mod:`gem.extractors._cells`).

    Args:
        samples: ``(game_time_s, world_x, world_y)`` per interval read.

    Returns:
        The nested cell histogram with cell-number string keys.
    """
    lane_pos: dict[str, dict[str, int]] = {}
    for seconds, x, y in samples:
        expanded = seconds >= 0
        column = lane_pos.setdefault(str(od_cell_index(x, expanded=expanded)), {})
        key = str(od_cell_index(y, expanded=expanded))
        column[key] = column.get(key, 0) + 1
    return lane_pos


def _ward_left_entry(ward: WardEvent, clock: GameClock) -> dict[str, Any] | None:
    """Build an OpenDota ``*_left_log`` expiry entry from a WardEvent, or None.

    A ward that left the map (killed or expired naturally) yields one expiry
    record; wards still alive at game end yield ``None``. As in OpenDota,
    ``attackername`` is the damage source of the combat-log ``DEATH`` paired
    with the ward leaving, so a natural expiry names the owner's hero.

    Reference: odota/parser processors/warding/Wards.java and Parse.java
    ``onWardKilled`` / ``buildWardEntry`` (pinned in CLAUDE.md).

    Args:
        ward: The ward placement record.
        clock: Pause-aware game clock for the match.

    Returns:
        The OpenDota-shaped expiry dict, or ``None`` if the ward never left.
    """
    left_tick = _ward_left_tick(ward)
    if left_tick is None:
        return None
    seconds = _tick_game_seconds(left_tick, clock)
    player_id = _ward_left_player_id(ward)
    entry: dict[str, Any] = {
        "time": seconds,
        "type": "obs_left_log" if ward.ward_type == "observer" else "sen_left_log",
        "key": _ward_coord_key(ward.x, ward.y),
        "slot": player_id,
        "player_slot": _player_id_to_player_slot(player_id),
        "x": _to_od_cell(ward.x),
        "y": _to_od_cell(ward.y),
        "entityleft": True,
    }
    attacker = ward.left_attacker if ward.left_attacker is not None else ward.killer
    if attacker:
        entry["attackername"] = attacker
    return entry


def _ward_left_tick(ward: WardEvent) -> int | None:
    """Return the tick a ward was killed or expired, or ``None`` if it never left."""
    return ward.killed_tick if ward.killed_tick is not None else ward.expires_tick


def _ward_left_player_id(ward: WardEvent) -> int:
    """Return the player a ward's leave is logged for.

    OpenDota reads the owner when the ward leaves; ``-1`` when that owner no
    longer resolves, so the leave belongs to no player. Wards without that
    record fall back to the placer.
    """
    return ward.left_player_id if ward.left_player_id is not None else ward.player_id


#: Target-name fragments OpenDota turns into a ``building_kill`` objective:
#: towers, barracks, shrines and the Ancient.
#: Reference: odota/parser CreateParsedDataBlob.java ``handleDeathCombat``.
_BUILDING_NAME_PARTS = ("_tower", "_rax_", "_healers", "_fort")


def _build_objectives(
    obj_ext: ObjectivesExtractor,
    combat_agg: _CombatAggregator,
    first_blood_entry: CombatLogEntry | None,
    pid_to_team: dict[int, int],
    clock: GameClock,
    chat_event_times: list[_ChatEventTime] | None = None,
    opendota_start_s: int | None = None,
    combat_log: Iterable[CombatLogEntry] = (),
) -> list[dict[str, Any]]:
    """Merge gem's per-type objective events into OpenDota's unified timeline.

    Produces the ``objectives`` list OpenDota exposes: ``building_kill`` plus the
    ``CHAT_MESSAGE_*`` events, each ``{time, type, ...}`` with type-specific
    fields, sorted chronologically. Killer heroes are resolved to OpenDota
    ``slot``/``player_slot`` via the combat aggregator's name→id map. When a
    chat-message objective pairs with its ``CDOTAUserMsg_ChatEvent``, the
    event's fields replace gem's reconstruction, as OpenDota builds these
    objectives from the chat events alone.

    Args:
        obj_ext: The objectives extractor (roshans, aegis, Tormentors, couriers).
        combat_agg: Combat aggregator, for killer-hero → player id resolution.
        first_blood_entry: The first-blood hero-death entry, or ``None``.
        pid_to_team: Map of player id (0-9) → team (2/3), for courier ownership.
        clock: Pause-aware game clock for the match.
        chat_event_times: The replay's chat events with OpenDota's tick-start
            clock; ``CHAT_MESSAGE_*`` objectives take their time and fields
            from them.
        opendota_start_s: OpenDota's game-start anchor for those clock values.
        combat_log: The match's combat log; building deaths in it become
            ``building_kill`` objectives.

    Returns:
        Chronologically-sorted list of OpenDota-shaped objective dicts.
    """
    # Every objective with the tick of the event it was built from, which
    # orders objectives that share a second.
    objectives: list[tuple[int, dict[str, Any]]] = []
    # Chat-message objectives, by type.
    chat_objectives: defaultdict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)

    def add_chat_objective(tick: int, entry: dict[str, Any]) -> None:
        objectives.append((tick, entry))
        chat_objectives[entry["type"]].append((tick, entry))

    def secs(tick: int) -> int:
        return _tick_game_seconds(tick, clock)

    def slot_fields(player_id: int | None) -> dict[str, Any]:
        if not isinstance(player_id, int) or not (0 <= player_id < 10):
            return {}
        return {"slot": player_id, "player_slot": _player_id_to_player_slot(player_id)}

    # building_kill — every building death OpenDota counts (towers, barracks,
    # shrines, the Ancient), timed like the combat-log entry. Attributed
    # source-first: a summon / projectile killer carries the owning hero in
    # damage_source_name. unit is the crediting source unit when present; an
    # empty name is CombatLogNames index 0, which OpenDota prints as dota_unknown.
    for death in combat_log:
        target = death.target_name
        if death.log_type != "DEATH" or not any(p in target for p in _BUILDING_NAME_PARTS):
            continue
        pid = combat_agg.resolve_kill_pid(death.damage_source_name, death.attacker_name)
        objectives.append(
            (
                death.tick,
                {
                    "time": _entry_game_seconds(death, clock),
                    "type": "building_kill",
                    "key": target,
                    "unit": death.damage_source_name or death.attacker_name or "dota_unknown",
                    **slot_fields(pid),
                },
            )
        )

    # CHAT_MESSAGE_ROSHAN_KILL — team that killed Roshan (killer's team).
    for rk in obj_ext.roshan_kills:
        pid = combat_agg.resolve_kill_pid(rk.killer_source, rk.killer)
        team = pid_to_team.get(pid) if pid is not None else None
        entry: dict[str, Any] = {"time": secs(rk.tick), "type": "CHAT_MESSAGE_ROSHAN_KILL"}
        if team is not None:
            entry["team"] = team
        add_chat_objective(rk.tick, entry)

    # CHAT_MESSAGE_AEGIS / _AEGIS_STOLEN / _DENIED_AEGIS.
    _aegis_type = {
        "pickup": "CHAT_MESSAGE_AEGIS",
        "stolen": "CHAT_MESSAGE_AEGIS_STOLEN",
        "denied": "CHAT_MESSAGE_DENIED_AEGIS",
    }
    for ae in obj_ext.aegis_events:
        pid = ae.player_id if 0 <= ae.player_id < 10 else None
        add_chat_objective(
            ae.tick,
            {
                "time": secs(ae.tick),
                "type": _aegis_type.get(ae.event_type, "CHAT_MESSAGE_AEGIS"),
                **slot_fields(pid),
            },
        )

    # CHAT_MESSAGE_MINIBOSS_KILL — Tormentor, by killing player + their team.
    for tm in obj_ext.tormentor_kills:
        pid = tm.killer_player_id if 0 <= tm.killer_player_id < 10 else None
        entry = {"time": secs(tm.tick), "type": "CHAT_MESSAGE_MINIBOSS_KILL", **slot_fields(pid)}
        team = pid_to_team.get(pid) if pid is not None else None
        if team is not None:
            entry["team"] = team
        add_chat_objective(tm.tick, entry)

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
            "time": _entry_game_seconds(first_blood_entry, clock),
            "type": "CHAT_MESSAGE_FIRSTBLOOD",
            **slot_fields(killer_pid),
        }
        if victim_pid is not None:
            entry["key"] = str(victim_pid)
        add_chat_objective(first_blood_entry.tick, entry)

    # CHAT_MESSAGE_COURIER_LOST — team is the courier's owner (killer's opposite).
    for cd in obj_ext.courier_deaths:
        killer_pid = combat_agg.resolve_kill_pid(cd.killer_source, cd.killer)
        killer_team = pid_to_team.get(killer_pid) if killer_pid is not None else None
        entry = {"time": secs(cd.tick), "type": "CHAT_MESSAGE_COURIER_LOST"}
        if killer_team in (2, 3):
            entry["team"] = 3 if killer_team == 2 else 2  # owner = opposite of killer
        if killer_pid is not None:
            entry["killer"] = _player_id_to_player_slot(killer_pid)
        add_chat_objective(cd.tick, entry)

    if chat_event_times:
        _apply_chat_events(chat_objectives, chat_event_times, opendota_start_s)
    # odota/core resolves the first-blood victim's 0-9 index in ``key`` to a
    # player_slot when it serves the match (compute.ts annotateFirstbloodVictim).
    for _, entry in chat_objectives.get("CHAT_MESSAGE_FIRSTBLOOD", ()):
        victim = entry.get("key")
        if victim is not None and victim.isdigit() and int(victim) < 10:
            entry["victim_player_slot"] = _player_id_to_player_slot(int(victim))
    # Within one tick OpenDota emits chat events before combat-log entries,
    # which Clarity defers to the tick's end, so building kills sort last.
    objectives.sort(key=lambda item: (item[1]["time"], item[0], item[1]["type"] == "building_kill"))
    return [entry for _, entry in objectives]


# A chat message lands within a couple of seconds of the event gem rebuilds an
# objective from (a combat-log death or an entity change).
_CHAT_MATCH_WINDOW_TICKS = 90


@dataclass(frozen=True, slots=True)
class _ChatEventTime:
    """One ``CDOTAUserMsg_ChatEvent`` with OpenDota's clock at its tick.

    Attributes:
        type: The ``DOTA_CHAT_MESSAGE`` value.
        player_id: ``playerid_1`` (the rune picker for rune pickups).
        value: The event's ``value`` (the rune type for rune pickups).
        tick: Replay tick the event arrived at.
        raw_s: OpenDota's running clock at that tick's start, before the
            game-start shift, or ``None`` when unavailable.
        player_id_2: ``playerid_2`` (the first-blood victim, the team that
            lost a courier), ``-1`` when unset.
    """

    type: int
    player_id: int
    value: int
    tick: int
    raw_s: int | None
    player_id_2: int = -1


def _align_ticks(first: list[int], second: list[int], window: int) -> list[tuple[int, int]]:
    """Pair two tick sequences one-to-one, preserving order.

    Among order-preserving pairings whose ticks differ by at most ``window``, it
    picks the one with the most pairs, then the smallest total tick distance.
    So an extra or missing event on either side cannot shift the pairs after it.

    Args:
        first: Ticks in ascending order.
        second: Ticks in ascending order.
        window: Largest allowed tick difference for a pair.

    Returns:
        ``(index in first, index in second)`` pairs, in order.
    """
    n, m = len(first), len(second)
    # best[i][j]: (pairs, -distance) for first[i:] and second[j:].
    best = [[(0, 0)] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            options = [best[i + 1][j], best[i][j + 1]]
            gap = abs(first[i] - second[j])
            if gap <= window:
                pairs, neg_distance = best[i + 1][j + 1]
                options.append((pairs + 1, neg_distance - gap))
            best[i][j] = max(options)
    pairs_out: list[tuple[int, int]] = []
    i = j = 0
    while i < n and j < m:
        gap = abs(first[i] - second[j])
        if gap <= window:
            pairs, neg_distance = best[i + 1][j + 1]
            if best[i][j] == (pairs + 1, neg_distance - gap):
                pairs_out.append((i, j))
                i, j = i + 1, j + 1
                continue
        if best[i][j] == best[i + 1][j]:
            i += 1
        else:
            j += 1
    return pairs_out


def _first_blood_death(
    combat_log: list[CombatLogEntry], chat_event_times: list[_ChatEventTime] | None
) -> CombatLogEntry | None:
    """Return the combat-log hero death that drew first blood.

    Only real hero deaths count: illusion deaths and reincarnation triggers are
    excluded (``target_is_hero`` stays true for an illusion). Not every such
    death is first blood (a hero killed by neutrals is not), so when the replay
    has a ``CHAT_MESSAGE_FIRSTBLOOD`` chat event, the death nearest its tick
    wins. Without one, the earliest real hero death is used.

    Args:
        combat_log: The match's combat log, in order.
        chat_event_times: The replay's chat events, or ``None``.

    Returns:
        The first-blood death entry, or ``None`` when there is none.
    """
    from gem.proto.dota_usermessages_pb2 import CHAT_MESSAGE_FIRSTBLOOD

    deaths = [
        e
        for e in combat_log
        if e.log_type == "DEATH"
        and e.target_is_hero
        and not e.target_is_illusion
        and not e.will_reincarnate
    ]
    event = next((e for e in chat_event_times or () if e.type == CHAT_MESSAGE_FIRSTBLOOD), None)
    if event is not None:
        near = [d for d in deaths if abs(d.tick - event.tick) <= _CHAT_MATCH_WINDOW_TICKS]
        if near:
            return min(near, key=lambda d: abs(d.tick - event.tick))
    return deaths[0] if deaths else None


def _od_slot_fields(player_id: int) -> dict[str, Any]:
    """Return OpenDota's ``slot``/``player_slot`` for a chat event's player id.

    OpenDota copies the id into ``slot`` as is, ``-1`` included, and adds
    ``player_slot`` only for a real player.
    """
    fields: dict[str, Any] = {"slot": player_id}
    if 0 <= player_id < 10:
        fields["player_slot"] = _player_id_to_player_slot(player_id)
    return fields


def _chat_event_fields(chat_type: str, event: _ChatEventTime) -> dict[str, Any] | None:
    """Return the objective fields OpenDota derives from a chat event.

    Reference: odota/parser CreateParsedDataBlob.java ``handleFirstblood``,
    ``handleMinibossKill`` and ``handleCourierLost``. Other chat types keep
    gem's reconstruction, which already matches, and return ``None``.
    """
    match chat_type:
        case "CHAT_MESSAGE_FIRSTBLOOD":
            return {**_od_slot_fields(event.player_id), "key": str(event.player_id_2)}
        case "CHAT_MESSAGE_MINIBOSS_KILL":
            return {**_od_slot_fields(event.player_id), "team": event.value}
        case "CHAT_MESSAGE_COURIER_LOST":
            player = event.player_id
            killer = _player_id_to_player_slot(player) if 0 <= player < 10 else -1
            return {"team": event.player_id_2, "killer": killer, "value": event.value}
    return None


def _apply_chat_events(
    chat_objectives: dict[str, list[tuple[int, dict[str, Any]]]],
    chat_event_times: list[_ChatEventTime],
    start_s: int | None,
) -> None:
    """Give each chat-message objective the time and fields of its chat event.

    OpenDota builds these objectives from ``CDOTAUserMsg_ChatEvent`` entries
    timed with its tick-start clock (odota/parser Parse.java ``onChatEvent``).
    gem rebuilds them from combat-log deaths or entity changes, so each is paired
    with the same-type chat event by :func:`_align_ticks`. A paired objective
    takes the event's fields (:func:`_chat_event_fields`) and, when the clock
    and ``start_s`` are known, its time. Unpaired objectives keep gem's values.
    """
    from gem.proto.dota_usermessages_pb2 import DOTA_CHAT_MESSAGE

    by_type: defaultdict[str, list[_ChatEventTime]] = defaultdict(list)
    for event in chat_event_times:
        try:
            by_type[DOTA_CHAT_MESSAGE.Name(event.type)].append(event)
        except ValueError:
            continue
    for chat_type, entries in chat_objectives.items():
        events = sorted(by_type.get(chat_type, ()), key=lambda e: e.tick)
        entries = sorted(entries, key=lambda item: item[0])
        pairs = _align_ticks(
            [tick for tick, _ in entries], [e.tick for e in events], _CHAT_MATCH_WINDOW_TICKS
        )
        for entry_index, event_index in pairs:
            entry, event = entries[entry_index][1], events[event_index]
            fields = _chat_event_fields(chat_type, event)
            if fields is not None:
                for key in ("slot", "player_slot", "team", "killer"):
                    entry.pop(key, None)
                entry.update(fields)
            if event.raw_s is not None and start_s is not None:
                entry["time"] = event.raw_s - start_s


def _retime_rune_pickups(
    entries: list[CombatLogEntry], chat_event_times: list[_ChatEventTime], start_s: int
) -> None:
    """Set each rune pickup's ``game_time_s`` to OpenDota's time for its chat event.

    Rune pickups come from ``CHAT_MESSAGE_RUNE_PICKUP`` chat events, which
    OpenDota times with its tick-start clock (odota/parser Parse.java
    ``onChatEvent``). Each ``PICKUP_RUNE`` entry is paired with the chat event of
    the same tick, player and rune type.
    """
    from gem.proto.dota_usermessages_pb2 import CHAT_MESSAGE_RUNE_PICKUP

    raw_by_key: defaultdict[tuple[int, int, int], list[int | None]] = defaultdict(list)
    for event in chat_event_times:
        if event.type == CHAT_MESSAGE_RUNE_PICKUP:
            raw_by_key[(event.tick, event.player_id, event.value)].append(event.raw_s)
    for entry in entries:
        if entry.log_type != "PICKUP_RUNE":
            continue
        queue = raw_by_key.get((entry.tick, entry.value, entry.rune_type or 0))
        if queue:
            raw_s = queue.pop(0)
            if raw_s is not None:
                entry.game_time_s = raw_s - start_s


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
) -> tuple[list[int], list[int], list[int]] | None:
    """Build Radiant gold/XP advantage from OpenDota-style interval snapshots."""
    batches = _complete_interval_batches(interval_ext)
    if batches is None:
        return None

    game_times_s: list[int] = []
    gold_adv: list[int] = []
    xp_adv: list[int] = []
    for by_player in batches:
        game_times_s.append(next(iter(by_player.values())).time_s)
        gold = 0
        xp = 0
        for snap in by_player.values():
            sign = 1 if snap.team == 2 else -1
            gold += sign * snap.gold
            xp += sign * snap.xp
        gold_adv.append(gold)
        xp_adv.append(xp)

    return game_times_s, gold_adv, xp_adv


_MINUTE_TICKS = 1800  # 60 s * 30 ticks/s


def _radiant_adv_from_minute_series(
    players: list[ParsedPlayer],
) -> tuple[list[int], list[int], list[int]] | None:
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
        ``(game_times_s, gold_adv, xp_adv)`` lists, or ``None`` if no player has
        minute data.
    """
    active = [pp for pp in players if pp.total_earned_gold_t_min and pp.total_earned_xp_t_min]
    if not active:
        return None

    # ``game_times_min`` is authoritative. ``times_min`` remains as a legacy
    # fallback for ParsedPlayer objects built by older/custom integrations. Its
    # global origin is the earliest sample tick across players, so a player who
    # first appears at minute 1 lands at index 1 rather than index 0.
    first_ticks = [pp.times_min[0] for pp in active if not pp.game_times_min and pp.times_min]
    origin = min(first_ticks) if first_ticks else 0

    def _minute_index(tick: int) -> int:
        return max(0, round((tick - origin) / _MINUTE_TICKS))

    # Per-player minute → (gold, xp), keyed by absolute minute.
    per_player: list[tuple[int, dict[int, tuple[int, int]]]] = []
    last_minute = 0
    for pp in active:
        sign = 1 if pp.team == 2 else -1  # 2=Radiant, 3=Dire
        by_minute: dict[int, tuple[int, int]] = {}
        gold_series = pp.total_earned_gold_t_min
        xp_series = pp.total_earned_xp_t_min
        if pp.game_times_min:
            n = min(len(pp.game_times_min), len(gold_series), len(xp_series))
            for i in range(n):
                minute = max(0, pp.game_times_min[i] // 60)
                by_minute[minute] = (gold_series[i], xp_series[i])
                last_minute = max(last_minute, minute)
        elif pp.times_min:
            n = min(len(pp.times_min), len(gold_series), len(xp_series))
            for i in range(n):
                minute = _minute_index(pp.times_min[i])
                by_minute[minute] = (gold_series[i], xp_series[i])
                last_minute = max(last_minute, minute)
        else:
            # A player with neither axis falls back to positional indexing so we
            # never silently drop their contribution.
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
    game_times_s = [minute * 60 for minute in range(n_minutes)]
    return game_times_s, gold_adv, xp_adv


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
            ts.ledger.append(snap.ledger)

    return series


# A buyback's gold-spent rise lands on the BUYBACK entry's own tick; allow a
# couple of ticks for an update delivered in the neighbouring packet.
_BUYBACK_SPEND_WINDOW_TICKS = 2


def _buyback_event(
    tick: int, player_id: int, net_worth: int, spends: list[BuybackSpend]
) -> BuybackEvent:
    """Build a buyback, taking its exact cost from the nearest unused spend."""
    nearest = min(
        (spend for spend in spends if abs(spend.tick - tick) <= _BUYBACK_SPEND_WINDOW_TICKS),
        key=lambda spend: abs(spend.tick - tick),
        default=None,
    )
    if nearest is None:
        return BuybackEvent(
            tick=tick, player_slot=player_id, cost=buyback_cost(net_worth), net_worth=net_worth
        )
    spends.remove(nearest)
    return BuybackEvent(
        tick=tick,
        player_slot=player_id,
        cost=nearest.cost,
        net_worth=net_worth,
        cost_exact=True,
        reliable_gold=nearest.reliable_gold,
        unreliable_gold=nearest.unreliable_gold,
    )


def _ledger_snapshot(tick: int, game_time_s: int, values: tuple[int, ...]) -> GoldLedgerSnapshot:
    attrs = {attr: value for (attr, _), value in zip(LEDGER_FIELDS, values, strict=True)}
    return GoldLedgerSnapshot(tick=tick, game_time_s=game_time_s, **attrs)


def _gold_ledger(
    interval_ts: IntervalTimeSeries | None,
    final: tuple[int, int, tuple[int, ...]] | None,
) -> GoldLedger | None:
    """Build a player's gold ledger from interval samples and the game-end read.

    ``per_minute`` stays parallel to ``game_times_min``: it is filled only when
    every interval sample carries a complete ledger, and left empty otherwise.
    """
    per_minute: list[GoldLedgerSnapshot] = []
    if interval_ts is not None and interval_ts.ledger and None not in interval_ts.ledger:
        per_minute = [
            _ledger_snapshot(tick, time_s, values)
            for tick, time_s, values in zip(
                interval_ts.ticks, interval_ts.times, interval_ts.ledger, strict=True
            )
            if values is not None
        ]
    final_snapshot = _ledger_snapshot(*final) if final is not None else None
    if final_snapshot is None and not per_minute:
        return None
    return GoldLedger(final=final_snapshot, per_minute=per_minute)


def _buyback_spends_by_player(
    spends: list[BuybackSpend] | None, interval_ext: IntervalExtractor | None
) -> dict[int, list[BuybackSpend]]:
    """Group observed buyback spends by logical player id."""
    by_player: dict[int, list[BuybackSpend]] = defaultdict(list)
    if not spends or interval_ext is None:
        return by_player
    for spend in spends:
        player_id = interval_ext.player_for_team_slot(spend.team, spend.team_slot)
        if player_id is not None:
            by_player[player_id].append(spend)
    return by_player


def _populate_player_series(
    match: ParsedMatch,
    *,
    player_ext: PlayerExtractor,
    combat_agg: _CombatAggregator,
    interval_ext: IntervalExtractor | None,
    interval_min_series: dict[int, IntervalTimeSeries],
    clock: GameClock,
    radiant_win: bool | None,
    buyback_spends: dict[int, list[BuybackSpend]] | None = None,
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
        clock: Pause-aware game clock for purchase times and the lane window.
        radiant_win: Resolved match winner, or ``None`` if unknown.
        buyback_spends: Observed rises in gold spent on buybacks, by player id.
    """
    lane_samples = getattr(player_ext, "lane_samples", None)
    if not isinstance(lane_samples, list):
        lane_samples = []
    interval_samples = getattr(player_ext, "interval_samples", None)
    if not isinstance(interval_samples, list):
        interval_samples = []
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
        pp.total_earned_xp_t = ts.total_earned_xp_t
        interval_ts = interval_min_series.get(player_id)
        if interval_ts is not None:
            # OpenDota interval records use cumulative earned gold/XP for
            # gold_t/xp_t. Mirror that on the minute arrays when complete
            # interval batches are available; keep dense series unchanged.
            pp.times_min = interval_ts.ticks
            pp.game_times_min = interval_ts.times
            pp.gold_t_min = interval_ts.gold_t
            pp.total_earned_gold_t_min = interval_ts.gold_t
            pp.total_earned_xp_t_min = interval_ts.xp_t
            pp.net_worth_t_min = interval_ts.net_worth_t
            pp.lh_t_min = interval_ts.lh_t
            pp.dn_t_min = interval_ts.dn_t
            pp.xp_t_min = interval_ts.xp_t
        else:
            pp.times_min = mts.ticks
            minute_game_times = list(getattr(mts, "game_times_s", []) or [])
            # Real PlayerTimeSeries objects always carry the explicit axis. Keep
            # a positional compatibility fallback for third-party/custom
            # extractors that still return the pre-axis shape.
            if len(minute_game_times) != len(pp.times_min):
                minute_game_times = [i * 60 for i in range(len(pp.times_min))]
            pp.game_times_min = minute_game_times
            # OpenDota's gold_t is cumulative earned gold, not cash on hand.
            pp.gold_t_min = mts.total_earned_gold_t
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
            # recipes and ward dispensers — matching OpenDota's purchase_log,
            # which still counts both in the `purchase` map (see
            # _count_only_purchase). OpenDota does NOT dedup starting items
            # (its log genuinely lists e.g. 2x faerie_fire), so collapsing
            # same-(tick, item) entries here under-counted starting consumables.
            sorted_purchases = sorted(agg.purchase_log, key=lambda e: e.tick)
            pp.purchase_log = [
                entry
                for entry in sorted_purchases
                if not _count_only_purchase(opendota_translate(entry.value_name) or "")
            ]
            # Aggregates are derived from the FULL log: the `purchase` count map
            # includes recipes and dispensers, while purchase_time and
            # first_purchase_time exclude them. _build_purchase_aggregates handles
            # that split internally.
            purchase_aggs = _build_purchase_aggregates(sorted_purchases, clock)
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
            # Structured buybacks. The cost is exact when the team data's gold
            # spent on buybacks rose with this entry; otherwise it falls back to
            # 200 + net_worth // 13 at the buyback tick (net_worth_t is populated
            # above, so net_worth_at() resolves the nearest sample).
            spends = list((buyback_spends or {}).get(player_id, ()))
            pp.buybacks = [
                _buyback_event(entry.tick, player_id, net_worth_at(pp, entry.tick), spends)
                for entry in agg.buyback_log
            ]
            pp.stuns_dealt = agg.stuns_dealt
            # Best-effort combat-log fallbacks. The embedded postgame summary is
            # applied after this loop when available.
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

        scoreboard = player_ext.scoreboard.get(player_id)
        if scoreboard is not None:
            pp.kills, pp.deaths, pp.assists = scoreboard

        # Lane heatmap over game time <= 600 s, pre-horn included, from OpenDota's
        # once-a-second interval reads. Replays read without tick-start callbacks
        # fall back to the dense snapshots.
        if lane_samples:
            player_lane_samples = [
                (seconds, x, y) for pid, seconds, x, y in lane_samples if pid == player_id
            ]
        else:
            player_lane_samples = [
                (seconds, snap.x, snap.y)
                for snap in player_ext.snapshots
                if snap.player_id == player_id and snap.x is not None and snap.y is not None
                if (seconds := clock.game_seconds_at(snap.tick)) is not None
                and seconds <= LANE_WINDOW_S
            ]
        pp.lane_pos = _lane_pos(player_lane_samples)

        # Lane assignment and 10-minute raw stats
        # OpenDota picks the side from the player slot; use it when the team is unknown.
        lane = assign_lane(pp.lane_pos, pp.team if pp.team in (2, 3) else 2 + (player_id >= 5))
        pp.lane, pp.lane_role, pp.is_roaming = lane.lane, lane.lane_role, lane.is_roaming
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
        if pp.gold_t:
            pp.gold = pp.gold_t[-1]
        final_ledgers = getattr(interval_ext, "final_ledgers", None)
        pp.gold_ledger = _gold_ledger(
            interval_ts,
            final_ledgers.get(player_id) if isinstance(final_ledgers, dict) else None,
        )
        final_ledger = pp.gold_ledger.final if pp.gold_ledger is not None else None
        if final_ledger is not None:
            # The postgame summary's gold_spent overrides this when present
            # (_apply_match_details_scalars); the two are equal when both exist.
            pp.gold_spent = final_ledger.spent_on_items + final_ledger.spent_on_consumables
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

        # life_state_dead: OpenDota counts its once-a-second interval reads, from
        # game time 0 until post-game, where the hero's m_lifeState is 1 or 2
        # (odota/core compute.ts: life_state[1] + life_state[2]). Without
        # interval reads, count distinct dead game-seconds of the dense snapshots.
        if interval_samples:
            pp.life_state_dead = sum(
                1 for sample in interval_samples if sample[2] == player_id and sample[6] in (1, 2)
            )
        else:
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
        pp.kda = kda(pp.kills, pp.deaths, pp.assists)
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
    hero_visibility_events: list[HeroVisibilityEvent] | None = None,
    vision_modifier_pairing_issues: list[VisionModifierPairingIssue] | None = None,
    entity_visibility_events: list[EntityVisibilityEvent] | None = None,
    buyback_spends: list[BuybackSpend] | None = None,
    chat_event_times: list[_ChatEventTime] | None = None,
) -> ParsedMatch:
    """Assemble a :class:`ParsedMatch` from extractor state after a completed parse.

    Handles radiant_win resolution (three-tier), per-player time series wiring,
    player name extraction, ward-to-player assignment, gold/XP advantage curves,
    and fight detection.

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
        hero_visibility_events: Authoritative hero visibility transitions.
        vision_modifier_pairing_issues: Ambiguous or unmatched modifier removals.
        entity_visibility_events: Authoritative networked Dota NPC visibility transitions.
        buyback_spends: Observed rises in the team data's gold spent on buybacks
            (``BuybackSpendTracker.spends``), giving exact buyback costs.
        chat_event_times: The replay's chat events with OpenDota's tick-start
            clock, which time rune pickups and chat-message objectives.

    Returns:
        Fully populated :class:`ParsedMatch`.
    """
    from gem.extractors.fights import detect_fights, detect_opendota_teamfights

    # radiant_win resolution — three tiers in priority order:
    #   1. CDemoFileInfo.game_winner (set during parse, empty for HLTV replays)
    #   2. m_pGameRules.m_nGameWinner entity field (set post-parse in parser.py)
    #   3. Ancient DEATH in combat log — no API needed
    radiant_win = parser.radiant_win
    if radiant_win is None:
        radiant_win = _radiant_win_from_ancient(all_entries)

    match_details = getattr(parser, "match_details", None)
    duration = getattr(parser, "duration_s", None) or 0
    if match_details is not None and match_details.HasField("duration"):
        duration = int(match_details.duration)

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
        hero_visibility_events=hero_visibility_events or [],
        vision_modifier_pairing_issues=vision_modifier_pairing_issues or [],
        entity_visibility_events=entity_visibility_events or [],
        draft=draft_ext.draft_events,
        game_start_tick=parser.game_start_tick,
        game_end_tick=parser.tick,
        post_game_tick=parser.post_game_tick,
        game_clock=parser.game_clock,
        duration=duration,
        parse_error=repr(parser.parse_error) if parser.parse_error is not None else None,
        truncated_at_tick=parser.truncated_at_tick,
    )
    clock = parser.game_clock

    # Post-process buybacks (7b).
    # For BUYBACK entries, entry.value = player slot (0-9).
    # Reference: odota/parser src/main/java/opendota/CreateParsedDataBlob.java handleBuyback()
    for entry in all_entries:
        if entry.log_type != "BUYBACK":
            continue
        pid = entry.value
        if 0 <= pid < 10:
            combat_agg._agg(pid).buyback_log.append(entry)

    # Capture game_start_tick once — used for the first-blood fallback below
    game_start_tick = parser.game_start_tick
    interval_min_series = _interval_series_by_player(interval_ext)

    # first_blood_time: game-clock time of the first-blood hero DEATH. The
    # per-player firstblood_claimed flag is read separately from the
    # authoritative CDOTA_PlayerResource field below, not reconstructed from
    # this entry.
    first_blood_entry = _first_blood_death(all_entries, chat_event_times)
    if first_blood_entry is not None:
        if first_blood_entry.game_time_s is not None:
            match.first_blood_time = int(first_blood_entry.game_time_s)
        elif game_start_tick is not None:
            match.first_blood_time = max(0, _tick_game_seconds(first_blood_entry.tick, clock))

    # pre_game_duration has no replay-stream reconstruction; it comes only from
    # the postgame summary (_apply_match_details_match_scalars below).

    # Build per-player time series and overlay combat log aggregates.
    _populate_player_series(
        match,
        player_ext=player_ext,
        combat_agg=combat_agg,
        interval_ext=interval_ext,
        interval_min_series=interval_min_series,
        clock=clock,
        radiant_win=radiant_win,
        buyback_spends=_buyback_spends_by_player(buyback_spends, interval_ext),
    )

    # Complete replays carry an embedded CMsgDOTAMatch postgame summary. Its
    # terminal combat scalars, GPM/XPM, and permanent buffs are the same Game
    # Coordinator values exposed by OpenDota, so they take precedence over
    # combat-log estimates and unavailable defaults.
    _apply_match_details_scalars(match, match_details)

    match_metadata = getattr(parser, "match_metadata", None)
    metadata = getattr(match_metadata, "metadata", None)
    for team in getattr(metadata, "teams", []) or []:
        for metadata_player in getattr(team, "players", []) or []:
            metadata_player_id = _player_slot_to_player_id(metadata_player.player_slot)
            if metadata_player_id is not None:
                match.players[metadata_player_id].ability_upgrades_arr = list(
                    metadata_player.ability_upgrades
                )

    # Tier-2: lane advantage vs opponents — paired by gold rank within the lane.
    # Players are sorted by lane_total_gold descending within each (team, lane_role)
    # group, then matched by rank: richest vs richest, poorest vs poorest.
    # This fairly pairs carries against carries and supports against supports
    # without requiring an explicit position field.
    # Jungle (4) and unknown (0) are excluded — no direct lane opponent.
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
    # Reference: dotabuff/manta manta_test.go line ~703, odota/parser Parse.java line ~602
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
    # Left logs are in the order wards left, as OpenDota logs them; a ward's
    # leave belongs to its owner at that time (see _ward_left_player_id).
    left_ticks = [(_ward_left_tick(ward), index) for index, ward in enumerate(match.wards)]
    for _, index in sorted((tick, i) for tick, i in left_ticks if tick is not None):
        ward = match.wards[index]
        left_entry = _ward_left_entry(ward, clock)
        left_id = _ward_left_player_id(ward)
        if left_entry is not None and 0 <= left_id < 10:
            left_player = match.players[left_id]
            if ward.ward_type == "observer":
                left_player.obs_left_log.append(left_entry)
            else:
                left_player.sen_left_log.append(left_entry)
    for ward in match.wards:
        if not (0 <= ward.player_id < 10):
            continue
        pp = match.players[ward.player_id]
        if ward.ward_type == "observer":
            pp.obs_log.append(ward)
            coord_map = pp.obs
        else:
            pp.sen_log.append(ward)
            coord_map = pp.sen
        if ward.x is not None and ward.y is not None:
            column = coord_map.setdefault(str(od_cell_index(ward.x)), {})
            yk = str(od_cell_index(ward.y))
            column[yk] = column.get(yk, 0) + 1

    # observers_placed: OpenDota's purchase/log-derived observer count, distinct
    # from the entity-counter obs_placed. Use the per-player obs_log length.
    for pp in match.players:
        pp.observers_placed = len(pp.obs_log)

    # OpenDota-shaped unified objectives timeline + building-status bitmasks.
    pid_to_team = {pp.player_id: pp.team for pp in match.players if pp.team}
    opendota_start_s = getattr(parser, "opendota_start_s", None)
    if chat_event_times and isinstance(opendota_start_s, int):
        _retime_rune_pickups(all_entries, chat_event_times, opendota_start_s)
    else:
        opendota_start_s = None
    match.objectives = _build_objectives(
        obj_ext,
        combat_agg,
        first_blood_entry,
        pid_to_team,
        clock,
        chat_event_times=chat_event_times,
        opendota_start_s=opendota_start_s,
        combat_log=all_entries,
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
    # Reference: odota/parser src/main/java/opendota/Parse.java interval block
    #   (m_vecDataTeam.%i.m_iTotalEarnedGold/XP) and CreateParsedDataBlob.java
    #   addIntervalData("xp_t"/"gold_t", ...).
    interval_adv = _radiant_adv_from_intervals(interval_ext)
    if interval_adv is not None:
        # Authoritative path: OpenDota-style interval snapshots are complete.
        game_times_s, gold_adv, xp_adv = interval_adv
        match.game_times_min = game_times_s
        match.radiant_gold_adv = gold_adv
        match.radiant_xp_adv = xp_adv
    else:
        # Fallback path: no complete interval batches were observed, so derive
        # the curves from the dense player minute series' total-earned arrays.
        minute_adv = _radiant_adv_from_minute_series(match.players)
        if minute_adv is not None:
            match.game_times_min, match.radiant_gold_adv, match.radiant_xp_adv = minute_adv

    # Detect fights (Phase 9)
    hero_to_slot = {pp.hero_name: pp.player_id for pp in match.players if pp.hero_name}
    slot_to_team = {pp.player_id: pp.team for pp in match.players if pp.team}
    player_snaps: dict[int, Any] = {
        pid: [s for s in player_ext.snapshots if s.player_id == pid] for pid in range(10)
    }
    match.fights = detect_fights(
        all_entries,
        hero_to_slot=hero_to_slot,
        player_snapshots=player_snaps,
        slot_to_team=slot_to_team,
    )
    interval_samples = getattr(player_ext, "interval_samples", None)
    match.opendota_teamfights = detect_opendota_teamfights(
        all_entries,
        hero_to_slot=hero_to_slot,
        player_snapshots=player_snaps,
        game_start_tick=match.game_start_tick,
        duration_s=match.duration or None,
        game_clock=clock,
        interval_samples=interval_samples if isinstance(interval_samples, list) else None,
        aegis_events=obj_ext.aegis_events,
    )

    # teamfight_participation: read the authoritative game-computed value from
    # CDOTA_PlayerResource.m_flTeamFightParticipation — the exact field OpenDota
    # reads (Parse.java), not a teamfight-window reconstruction (which OpenDota
    # itself does not do, and which can't match the engine's metric).
    if interval_ext is not None:
        for player_id in range(10):
            scalars = interval_ext.player_resource_scalars(player_id)
            match.players[player_id].teamfight_participation = float32_json(
                scalars["teamfight_participation"]
            )

    # Team kill scores = sum of each side's player kills; the postgame summary's
    # scores (and first blood / pre-game duration) take precedence when present.
    match.radiant_score = sum(pp.kills for pp in match.players if pp.team == 2)
    match.dire_score = sum(pp.kills for pp in match.players if pp.team == 3)
    _apply_match_details_match_scalars(match, match_details)

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
