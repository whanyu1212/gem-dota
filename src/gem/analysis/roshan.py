"""Post-parse Roshan conversion analysis.

Turns existing replay facts (Roshan kills, Aegis events, teamfights, wards,
objectives, buybacks, and movement samples) into per-Roshan conversion records.
The goal is to answer a practical question: did the team translate Roshan into
fights, objectives, map expansion, or a game-closing sequence?
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from gem.analysis._shared import (
    _TEAM_DIRE,
    _TEAM_RADIANT,
    infer_match_end_tick,
    region_of,
)

if TYPE_CHECKING:
    from gem.extractors.objectives import AegisEvent, BannerPlant
    from gem.extractors.teamfights import Teamfight
    from gem.results.models import ParsedMatch

_TICKS_PER_SEC = 30
_AEGIS_DURATION_TICKS = 5 * 60 * _TICKS_PER_SEC
_IMMEDIATE_WINDOW_TICKS = 180 * _TICKS_PER_SEC
_ASSOCIATION_WINDOW_TICKS = 30 * _TICKS_PER_SEC
_POST_CONSUME_GRACE_TICKS = 30 * _TICKS_PER_SEC

# Roshan drops worth flagging beyond the always-present Aegis. Cheese (burst
# heal/mana), the Refresher Shard (a free ultimate reset), and Roshan's Banner
# (a pushing siege unit) all materially raise the stakes of the kill. Surfaced
# descriptively only — they deliberately do not affect ``conversion_score`` or
# ``conversion_label`` so downstream consumers can weight them themselves.
_HIGH_VALUE_DROPS = frozenset({"cheese", "refresher_shard", "banner"})

# Lanes recognised in a barracks NPC name suffix (``..._rax_<lane>``).
_RAX_LANES = ("top", "mid", "bot")


def _rax_lane(barracks_name: str) -> str | None:
    """Return the lane (``"top"``/``"mid"``/``"bot"``) from a barracks NPC name.

    Mirrors the suffix parse in ``results/derived.py::_rax_bit`` but yields the
    lane token rather than a status-bit index — kept local so this post-parse
    module does not depend on the assembly layer.

    Args:
        barracks_name: e.g. ``"npc_dota_badguys_melee_rax_mid"``.

    Returns:
        The lane token, or ``None`` if no recognised lane suffix is present.
    """
    for lane in _RAX_LANES:
        if barracks_name.endswith(f"_rax_{lane}"):
            return lane
    return None


@dataclass
class RoshTimelineEvent:
    """One notable event inside a Roshan conversion sequence."""

    tick: int
    kind: Literal[
        "roshan",
        "aegis_pickup",
        "aegis_denied",
        "fight_win",
        "fight_loss",
        "fight_draw",
        "tower",
        "barracks",
        "buyback",
        "aegis_end",
        "game_end",
    ]
    label: str


@dataclass
class RoshConversion:
    """Derived summary for one Roshan kill and the advantage window that followed.

    Most fields summarise the Aegis window (holder, fights, objectives, map
    control). ``drops`` and ``had_high_value_drop`` describe what Roshan yielded
    beyond the Aegis itself.

    Attributes:
        drops: Short drop names captured from entity state at the kill tick (e.g.
            ``["aegis", "cheese", "banner"]``). Mirrors ``RoshanKill.drops`` and
            always includes ``"aegis"``. Empty only if drop tracking found nothing.
        had_high_value_drop: ``True`` when a non-Aegis premium drop (cheese,
            refresher shard, or banner) was present. Provided as a convenience
            signal; it does not influence ``conversion_score`` or
            ``conversion_label``.
        banner_planted: ``True`` when the Roshan holder's team planted a Roshan's
            Banner inside this conversion window. Independent of whether the
            ``"banner"`` drop was recorded — a banner from an *earlier* Roshan can
            be planted in this window.
        banner_rax_conversion: ``True`` when ``banner_planted`` and at least one
            enemy barracks fell *after* that plant within the window — an
            associative (lane + time) signal that the banner's siege push helped
            break a rax, not a proven spatial link. Like the drop flags it does
            not influence ``conversion_score`` or ``conversion_label``.
        banner_rax_lane: Lane (``"top"``/``"mid"``/``"bot"``) of the earliest such
            converted barracks, or ``None`` when there is no banner→rax link.
    """

    rosh_number: int
    rosh_tick: int
    killer_name: str
    holder_team: int | None
    holder_player_id: int | None
    holder_name: str
    aegis_pickup_tick: int | None
    immediate_end_tick: int
    aegis_end_tick: int
    aegis_eval_end_tick: int
    extended_end_tick: int
    aegis_fate: Literal["consumed", "expired", "denied", "game_end", "unknown"]
    first_fight_tick: int | None
    first_objective_tick: int | None
    fight_count: int
    fights_won: int
    fights_lost: int
    fights_drawn: int
    towers_taken: int
    barracks_taken: int
    enemy_buybacks_forced: int
    enemy_half_observer_delta: int
    enemy_half_farm_share_before: float
    enemy_half_farm_share_during: float
    enemy_half_farm_share_delta: float
    conversion_score: int
    conversion_label: Literal[
        "low_conversion",
        "fight_conversion",
        "objective_conversion",
        "map_squeeze",
        "game_closing_rosh",
    ]
    aegis_outcome: Literal[
        "consumed_in_fight",
        "expired_after_use",
        "expired_unused",
        "denied",
        "window_lost",
        "game_ended",
        "unknown",
    ]
    drivers: list[str] = field(default_factory=list)
    timeline_events: list[RoshTimelineEvent] = field(default_factory=list)
    # Roshan drop + banner→rax fields carry safe legacy defaults and sit last so
    # the public constructor stays backward-compatible: existing callers that
    # built a RoshConversion with the pre-drops keyword set keep working.
    drops: list[str] = field(default_factory=list)
    had_high_value_drop: bool = False
    banner_planted: bool = False
    banner_rax_conversion: bool = False
    banner_rax_lane: str | None = None


def _team_for_player(match: ParsedMatch, player_id: int | None) -> int | None:
    if player_id is None:
        return None
    for player in match.players:
        if player.player_id == player_id:
            return player.team if player.team in (_TEAM_RADIANT, _TEAM_DIRE) else None
    return None


def _hero_for_player(match: ParsedMatch, player_id: int | None) -> str:
    if player_id is None:
        return ""
    for player in match.players:
        if player.player_id == player_id:
            return player.hero_name
    return ""


def _window_overlaps(start_tick: int, end_tick: int, other_start: int, other_end: int) -> bool:
    return start_tick <= other_end and other_start <= end_tick


def _window_teamfights(match: ParsedMatch, start_tick: int, end_tick: int) -> list[Teamfight]:
    return [
        fight
        for fight in match.teamfights
        if _window_overlaps(start_tick, end_tick, fight.start_tick, fight.end_tick)
    ]


def _enemy_team(team: int) -> int:
    return _TEAM_DIRE if team == _TEAM_RADIANT else _TEAM_RADIANT


def _find_associated_aegis_event(
    match: ParsedMatch, rosh_tick: int, next_rosh_tick: int | None
) -> AegisEvent | None:
    association_end = rosh_tick + _ASSOCIATION_WINDOW_TICKS
    if next_rosh_tick is not None:
        association_end = min(association_end, next_rosh_tick - 1)
    for event in match.aegis_events:
        if event.tick < rosh_tick:
            continue
        if event.tick > association_end:
            break
        return event
    return None


def _holder_death_tick(
    match: ParsedMatch, holder_name: str, start_tick: int, end_tick: int
) -> int | None:
    if not holder_name:
        return None
    for entry in match.combat_log:
        if entry.tick < start_tick:
            continue
        if entry.tick > end_tick:
            break
        if (
            entry.log_type == "DEATH"
            and entry.target_name == holder_name
            and entry.target_is_hero
            and not entry.target_is_illusion
        ):
            return entry.tick
    return None


def _enemy_half_name(team: int) -> str:
    return "dire_half" if team == _TEAM_RADIANT else "radiant_half"


def _enemy_half_observer_placements(
    match: ParsedMatch, team: int, start_tick: int, end_tick: int
) -> int:
    region_name = _enemy_half_name(team)
    count = 0
    for ward in match.wards:
        if ward.team != team or ward.ward_type != "observer":
            continue
        if ward.x is None or ward.y is None:
            continue
        if ward.tick < start_tick or ward.tick > end_tick:
            continue
        if region_of(ward.x, ward.y) == region_name:
            count += 1
    return count


def _enemy_half_farm_share(match: ParsedMatch, team: int, start_tick: int, end_tick: int) -> float:
    region_name = _enemy_half_name(team)
    total_samples = 0
    enemy_half_samples = 0
    for player in match.players:
        if player.team != team:
            continue
        for tick, x, y in player.position_log:
            if tick < start_tick or tick > end_tick:
                continue
            total_samples += 1
            if region_of(x, y) == region_name:
                enemy_half_samples += 1
    if total_samples == 0:
        return 0.0
    return enemy_half_samples / total_samples


def _count_enemy_buybacks(match: ParsedMatch, team: int, start_tick: int, end_tick: int) -> int:
    count = 0
    enemy_team = _enemy_team(team)
    for player in match.players:
        if player.team != enemy_team:
            continue
        for entry in player.buyback_log:
            if start_tick <= entry.tick <= end_tick:
                count += 1
    return count


def _count_objectives(
    match: ParsedMatch, team: int, start_tick: int, end_tick: int
) -> tuple[int, int]:
    towers_taken = sum(
        1
        for tower in match.towers
        if start_tick <= tower.tick <= end_tick and tower.team == _enemy_team(team)
    )
    barracks_taken = sum(
        1
        for barracks in match.barracks
        if start_tick <= barracks.tick <= end_tick and barracks.team == _enemy_team(team)
    )
    return towers_taken, barracks_taken


def _banner_rax_signal(
    match: ParsedMatch, team: int, start_tick: int, end_tick: int
) -> tuple[bool, bool, str | None]:
    """Associate a banner plant with a barracks push inside the window.

    Roshan's Banner plants a stationary aura unit (movement speed + bonus attack
    damage to nearby allied heroes *and creeps*) used to amplify a high-ground
    siege. This is an associative lane+time signal, not a proven spatial one: gem
    does not store barracks world positions, so a banner→rax link means "the
    holder team planted a banner in this window and an enemy rax then fell",
    gated on side by ``_count_objectives``'s enemy-owned-barracks filter.

    Args:
        match: The parsed match.
        team: The Roshan holder's team.
        start_tick: Window start (inclusive).
        end_tick: Window end (inclusive).

    Returns:
        ``(banner_planted, banner_rax_conversion, banner_rax_lane)``.
    """
    plants: list[BannerPlant] = [
        plant
        for plant in match.banner_plants
        if plant.team == team and start_tick <= plant.tick <= end_tick
    ]
    if not plants:
        return False, False, None

    earliest_plant_tick = min(plant.tick for plant in plants)
    enemy_team = _enemy_team(team)
    converted_lanes = [
        (barracks.tick, _rax_lane(barracks.barracks_name))
        for barracks in match.barracks
        if barracks.team == enemy_team and earliest_plant_tick <= barracks.tick <= end_tick
    ]
    if not converted_lanes:
        return True, False, None

    # Earliest converted rax wins the lane attribution.
    _, lane = min(converted_lanes, key=lambda item: item[0])
    return True, True, lane


def _first_objective_tick(
    match: ParsedMatch, team: int, start_tick: int, end_tick: int
) -> int | None:
    candidates = [
        tower.tick
        for tower in match.towers
        if start_tick <= tower.tick <= end_tick and tower.team == _enemy_team(team)
    ]
    candidates.extend(
        barracks.tick
        for barracks in match.barracks
        if start_tick <= barracks.tick <= end_tick and barracks.team == _enemy_team(team)
    )
    return min(candidates) if candidates else None


def _fight_results(
    match: ParsedMatch, team: int, start_tick: int, end_tick: int
) -> tuple[list[Teamfight], int, int, int]:
    fights = _window_teamfights(match, start_tick, end_tick)
    won = lost = drawn = 0
    wanted_winner = "radiant" if team == _TEAM_RADIANT else "dire"
    enemy_winner = "dire" if team == _TEAM_RADIANT else "radiant"
    for fight in fights:
        if fight.winner == wanted_winner:
            won += 1
        elif fight.winner == enemy_winner:
            lost += 1
        else:
            drawn += 1
    return fights, won, lost, drawn


def _conversion_label(
    *,
    holder_team: int | None,
    aegis_fate: str,
    fights_won: int,
    fights_lost: int,
    towers_taken: int,
    barracks_taken: int,
    enemy_half_observer_delta: int,
    enemy_half_farm_share_delta: float,
    game_closed: bool,
) -> Literal[
    "low_conversion",
    "fight_conversion",
    "objective_conversion",
    "map_squeeze",
    "game_closing_rosh",
]:
    if game_closed and holder_team is not None:
        return "game_closing_rosh"
    if barracks_taken > 0 or towers_taken >= 2:
        return "objective_conversion"
    if fights_won > fights_lost and fights_won > 0:
        return "fight_conversion"
    if enemy_half_observer_delta > 0 or enemy_half_farm_share_delta >= 0.10:
        return "map_squeeze"
    return "low_conversion"


def _aegis_outcome(
    *,
    holder_team: int | None,
    aegis_fate: Literal["consumed", "expired", "denied", "game_end", "unknown"],
    fights_won: int,
    fights_lost: int,
    towers_taken: int,
    barracks_taken: int,
) -> Literal[
    "consumed_in_fight",
    "expired_after_use",
    "expired_unused",
    "denied",
    "window_lost",
    "game_ended",
    "unknown",
]:
    if aegis_fate == "denied":
        return "denied"
    if aegis_fate == "game_end":
        return "game_ended"
    if holder_team is None:
        return "unknown"
    if fights_lost > fights_won and towers_taken == 0 and barracks_taken == 0:
        return "window_lost"
    if aegis_fate == "consumed":
        return "consumed_in_fight"
    if aegis_fate == "expired":
        if fights_won == 0 and towers_taken == 0 and barracks_taken == 0:
            return "expired_unused"
        return "expired_after_use"
    return "unknown"


def _conversion_score(
    *,
    fights_won: int,
    fights_lost: int,
    towers_taken: int,
    barracks_taken: int,
    enemy_buybacks_forced: int,
    enemy_half_observer_delta: int,
    enemy_half_farm_share_delta: float,
    game_closed: bool,
    aegis_fate: str,
) -> int:
    raw = 25
    raw += fights_won * 12
    raw -= fights_lost * 12
    raw += towers_taken * 10
    raw += barracks_taken * 22
    raw += enemy_buybacks_forced * 7
    raw += max(enemy_half_observer_delta, 0) * 6
    raw += int(max(enemy_half_farm_share_delta, 0.0) * 40)
    if game_closed:
        raw += 30
    if aegis_fate == "expired" and fights_won == 0 and towers_taken == 0 and barracks_taken == 0:
        raw -= 14
    if aegis_fate == "denied":
        raw -= 18
    return max(0, min(100, raw))


@dataclass
class _RoshWindowBounds:
    """Tick boundaries for one Roshan conversion window."""

    next_rosh_tick: int | None
    immediate_end_tick: int
    extended_end_tick: int


@dataclass
class _AegisState:
    """Resolved Aegis ownership/fate plus initial timeline events."""

    holder_player_id: int | None
    holder_team: int | None
    holder_name: str
    aegis_pickup_tick: int | None
    aegis_end_tick: int
    aegis_fate: Literal["consumed", "expired", "denied", "game_end", "unknown"]
    timeline_events: list[RoshTimelineEvent]


@dataclass
class _HolderWindowStats:
    """Aggregated stats over the holder's evaluated conversion window."""

    holder_window_start: int
    holder_window_end: int
    fights: list[Teamfight]
    fights_won: int
    fights_lost: int
    fights_drawn: int
    towers_taken: int
    barracks_taken: int
    enemy_buybacks_forced: int
    enemy_half_observer_delta: int
    enemy_half_farm_share_before: float
    enemy_half_farm_share_during: float
    enemy_half_farm_share_delta: float
    first_objective_tick: int | None
    banner_planted: bool = False
    banner_rax_conversion: bool = False
    banner_rax_lane: str | None = None


def _rosh_window_bounds(
    match: ParsedMatch,
    rosh_index: int,
    rosh_tick: int,
    game_end_tick: int,
) -> _RoshWindowBounds:
    """Compute immediate and extended tick boundaries for one Roshan."""
    next_rosh_tick = match.roshans[rosh_index].tick if rosh_index < len(match.roshans) else None
    immediate_end_tick = min(rosh_tick + _IMMEDIATE_WINDOW_TICKS, game_end_tick)
    extended_end_tick = (next_rosh_tick - 1) if next_rosh_tick is not None else game_end_tick
    extended_end_tick = min(extended_end_tick, game_end_tick)
    return _RoshWindowBounds(
        next_rosh_tick=next_rosh_tick,
        immediate_end_tick=immediate_end_tick,
        extended_end_tick=extended_end_tick,
    )


def _initial_timeline_events(rosh_number: int, rosh_tick: int) -> list[RoshTimelineEvent]:
    """Create the timeline seed for one Roshan kill."""
    return [
        RoshTimelineEvent(
            tick=rosh_tick,
            kind="roshan",
            label=f"Roshan #{rosh_number} killed",
        )
    ]


def _aegis_pickup_label(holder_name: str) -> str:
    """Return the display label for an Aegis pickup event."""
    if not holder_name:
        return "Aegis claimed"
    return "Aegis -> " + holder_name.removeprefix("npc_dota_hero_").replace("_", " ")


def _resolve_aegis_state(
    match: ParsedMatch,
    *,
    rosh_tick: int,
    next_rosh_tick: int | None,
    game_end_tick: int,
    timeline_events: list[RoshTimelineEvent],
) -> _AegisState:
    """Resolve associated Aegis pickup/denial, holder, end tick, and fate."""
    aegis_event = _find_associated_aegis_event(match, rosh_tick, next_rosh_tick)
    holder_player_id: int | None = None
    holder_team: int | None = None
    holder_name = ""
    aegis_pickup_tick: int | None = None
    aegis_end_tick = min(rosh_tick + _AEGIS_DURATION_TICKS, game_end_tick)
    aegis_fate: Literal["consumed", "expired", "denied", "game_end", "unknown"] = "unknown"

    if aegis_event is not None:
        if aegis_event.event_type == "denied":
            aegis_pickup_tick = aegis_event.tick
            aegis_end_tick = aegis_event.tick
            aegis_fate = "denied"
            timeline_events.append(
                RoshTimelineEvent(tick=aegis_event.tick, kind="aegis_denied", label="Aegis denied")
            )
        else:
            holder_player_id = aegis_event.player_id if aegis_event.player_id >= 0 else None
            holder_team = _team_for_player(match, holder_player_id)
            holder_name = _hero_for_player(match, holder_player_id)
            aegis_pickup_tick = aegis_event.tick
            timeline_events.append(
                RoshTimelineEvent(
                    tick=aegis_event.tick,
                    kind="aegis_pickup",
                    label=_aegis_pickup_label(holder_name),
                )
            )
            raw_expiry_tick = min(aegis_event.tick + _AEGIS_DURATION_TICKS, game_end_tick)
            consume_tick = _holder_death_tick(match, holder_name, aegis_event.tick, raw_expiry_tick)
            if consume_tick is not None:
                aegis_end_tick = consume_tick
                aegis_fate = "consumed"
            elif raw_expiry_tick >= game_end_tick:
                aegis_end_tick = game_end_tick
                aegis_fate = "game_end"
            else:
                aegis_end_tick = raw_expiry_tick
                aegis_fate = "expired"

    return _AegisState(
        holder_player_id=holder_player_id,
        holder_team=holder_team,
        holder_name=holder_name,
        aegis_pickup_tick=aegis_pickup_tick,
        aegis_end_tick=aegis_end_tick,
        aegis_fate=aegis_fate,
        timeline_events=timeline_events,
    )


def _aegis_eval_end_tick(
    match: ParsedMatch,
    *,
    aegis_end_tick: int,
    aegis_fate: str,
    extended_end_tick: int,
    game_end_tick: int,
) -> int:
    """Return the end tick for evaluating the Aegis conversion window."""
    eval_end_tick = aegis_end_tick
    if aegis_fate == "consumed":
        overlapping = _window_teamfights(match, aegis_end_tick, aegis_end_tick)
        if overlapping:
            eval_end_tick = min(
                game_end_tick,
                max(
                    aegis_end_tick + _POST_CONSUME_GRACE_TICKS,
                    max(f.end_tick for f in overlapping),
                ),
            )
        else:
            eval_end_tick = min(game_end_tick, aegis_end_tick + _POST_CONSUME_GRACE_TICKS)

    # Clamp the holder window to this Roshan's upper boundary (next_rosh_tick
    # - 1). Without this, the post-consume grace can push aegis_eval_end_tick
    # past the next Roshan kill, so the same tower/barracks/teamfight/buyback
    # is counted in BOTH consecutive RoshConversion records. extended_end_tick
    # is purpose-built as the per-Roshan boundary; the counting windows must
    # respect it so each event belongs to exactly one Roshan.
    return min(eval_end_tick, extended_end_tick)


def _unknown_holder_window_stats(
    match: ParsedMatch,
    *,
    rosh_tick: int,
    holder_window_end: int,
) -> _HolderWindowStats:
    """Return neutral stats for a Roshan with no resolved holder team."""
    fights = _window_teamfights(match, rosh_tick, holder_window_end)
    return _HolderWindowStats(
        holder_window_start=rosh_tick,
        holder_window_end=holder_window_end,
        fights=fights,
        fights_won=0,
        fights_lost=0,
        fights_drawn=len(fights),
        towers_taken=0,
        barracks_taken=0,
        enemy_buybacks_forced=0,
        enemy_half_observer_delta=0,
        enemy_half_farm_share_before=0.0,
        enemy_half_farm_share_during=0.0,
        enemy_half_farm_share_delta=0.0,
        first_objective_tick=None,
    )


def _holder_window_stats(
    match: ParsedMatch,
    *,
    holder_team: int | None,
    aegis_pickup_tick: int | None,
    rosh_tick: int,
    immediate_end_tick: int,
    aegis_eval_end_tick: int,
) -> _HolderWindowStats:
    """Aggregate fight/objective/map-control stats over the holder window."""
    if holder_team is None:
        return _unknown_holder_window_stats(
            match,
            rosh_tick=rosh_tick,
            holder_window_end=aegis_eval_end_tick,
        )

    holder_window_start = aegis_pickup_tick or rosh_tick
    holder_window_end = aegis_eval_end_tick
    fights, fights_won, fights_lost, fights_drawn = _fight_results(
        match, holder_team, holder_window_start, holder_window_end
    )
    towers_taken, barracks_taken = _count_objectives(
        match, holder_team, holder_window_start, holder_window_end
    )
    enemy_buybacks_forced = _count_enemy_buybacks(
        match, holder_team, holder_window_start, holder_window_end
    )
    own_enemy_half_wards = _enemy_half_observer_placements(
        match, holder_team, holder_window_start, holder_window_end
    )
    enemy_enemy_half_wards = _enemy_half_observer_placements(
        match, _enemy_team(holder_team), holder_window_start, holder_window_end
    )
    enemy_half_observer_delta = own_enemy_half_wards - enemy_enemy_half_wards
    baseline_start = max((match.game_start_tick or 0), rosh_tick - _IMMEDIATE_WINDOW_TICKS)
    baseline_end = rosh_tick - 1
    enemy_half_farm_share_before = _enemy_half_farm_share(
        match, holder_team, baseline_start, baseline_end
    )
    enemy_half_farm_share_during = _enemy_half_farm_share(
        match, holder_team, rosh_tick, immediate_end_tick
    )
    enemy_half_farm_share_delta = enemy_half_farm_share_during - enemy_half_farm_share_before
    first_objective_tick = _first_objective_tick(
        match, holder_team, holder_window_start, holder_window_end
    )
    banner_planted, banner_rax_conversion, banner_rax_lane = _banner_rax_signal(
        match, holder_team, holder_window_start, holder_window_end
    )

    return _HolderWindowStats(
        holder_window_start=holder_window_start,
        holder_window_end=holder_window_end,
        fights=fights,
        fights_won=fights_won,
        fights_lost=fights_lost,
        fights_drawn=fights_drawn,
        towers_taken=towers_taken,
        barracks_taken=barracks_taken,
        enemy_buybacks_forced=enemy_buybacks_forced,
        enemy_half_observer_delta=enemy_half_observer_delta,
        enemy_half_farm_share_before=enemy_half_farm_share_before,
        enemy_half_farm_share_during=enemy_half_farm_share_during,
        enemy_half_farm_share_delta=enemy_half_farm_share_delta,
        first_objective_tick=first_objective_tick,
        banner_planted=banner_planted,
        banner_rax_conversion=banner_rax_conversion,
        banner_rax_lane=banner_rax_lane,
    )


def _first_fight_tick(stats: _HolderWindowStats) -> int | None:
    """Return the first fight tick inside a holder window."""
    return min(
        (max(fight.first_death_tick, stats.holder_window_start) for fight in stats.fights),
        default=None,
    )


def _game_closed_by_holder(
    match: ParsedMatch,
    *,
    holder_team: int | None,
    extended_end_tick: int,
) -> bool:
    """Return whether the holder team ended the game inside this Roshan window."""
    return (
        holder_team is not None
        and match.radiant_win is not None
        and (
            (holder_team == _TEAM_RADIANT and match.radiant_win)
            or (holder_team == _TEAM_DIRE and not match.radiant_win)
        )
        and match.game_end_tick > 0
        and match.game_end_tick <= extended_end_tick
    )


def _conversion_drivers(
    *,
    stats: _HolderWindowStats,
    aegis_outcome: str,
    aegis_fate: str,
) -> list[str]:
    """Build human-readable driver strings for a conversion summary."""
    drivers: list[str] = []
    if stats.fights_won:
        drivers.append(f"won {stats.fights_won} fight(s) during the Aegis window")
    if stats.fights_lost:
        drivers.append(f"lost {stats.fights_lost} fight(s) during the Aegis window")
    if stats.towers_taken:
        drivers.append(f"took {stats.towers_taken} tower(s)")
    if stats.barracks_taken:
        drivers.append(f"took {stats.barracks_taken} barracks")
    if stats.banner_rax_conversion:
        lane_text = f"{stats.banner_rax_lane} " if stats.banner_rax_lane else ""
        drivers.append(f"planted Roshan's Banner ahead of a {lane_text}barracks push")
    elif stats.banner_planted:
        drivers.append("planted Roshan's Banner during the window")
    if stats.enemy_buybacks_forced:
        drivers.append(f"forced {stats.enemy_buybacks_forced} enemy buyback(s)")
    if stats.enemy_half_observer_delta > 0:
        drivers.append(
            f"placed {stats.enemy_half_observer_delta} more observer ward(s) in enemy territory than they conceded"
        )
    if stats.enemy_half_farm_share_delta >= 0.10:
        drivers.append(
            f"expanded enemy-half presence by {round(stats.enemy_half_farm_share_delta * 100):d} percentage points"
        )
    if aegis_outcome == "expired_unused":
        drivers.append("Aegis expired before delivering a second life")
    elif aegis_outcome == "expired_after_use":
        drivers.append("Aegis expired after the team had already used the window")
    elif aegis_fate == "denied":
        drivers.append("Aegis was denied, so the team never got the immortality window")
    elif aegis_outcome == "window_lost":
        drivers.append("The Aegis window was lost without offsetting structures")
    elif aegis_fate == "consumed":
        drivers.append("Aegis was popped during the conversion window")
    return drivers


def _fight_timeline_event(
    fight: Teamfight,
    *,
    holder_team: int | None,
    holder_window_start: int,
) -> RoshTimelineEvent:
    """Build a timeline event for one fight in the conversion window."""
    fight_tick = max(fight.first_death_tick, holder_window_start)
    if holder_team is None or fight.winner == "draw":
        kind: Literal["fight_win", "fight_loss", "fight_draw"] = "fight_draw"
        label_text = (
            f"Fight already underway ({fight.deaths} deaths)"
            if fight.first_death_tick < holder_window_start
            else f"Fight ({fight.deaths} deaths)"
        )
    elif (holder_team == _TEAM_RADIANT and fight.winner == "radiant") or (
        holder_team == _TEAM_DIRE and fight.winner == "dire"
    ):
        kind = "fight_win"
        label_text = (
            f"Fight already underway, then won ({fight.deaths} deaths)"
            if fight.first_death_tick < holder_window_start
            else f"Fight won ({fight.deaths} deaths)"
        )
    else:
        kind = "fight_loss"
        label_text = (
            f"Fight already underway, then lost ({fight.deaths} deaths)"
            if fight.first_death_tick < holder_window_start
            else f"Fight lost ({fight.deaths} deaths)"
        )
    return RoshTimelineEvent(tick=fight_tick, kind=kind, label=label_text)


def _append_fight_timeline_events(
    timeline_events: list[RoshTimelineEvent],
    stats: _HolderWindowStats,
    holder_team: int | None,
) -> None:
    """Append fight events to the conversion timeline."""
    for fight in stats.fights:
        timeline_events.append(
            _fight_timeline_event(
                fight,
                holder_team=holder_team,
                holder_window_start=stats.holder_window_start,
            )
        )


def _append_objective_timeline_events(
    timeline_events: list[RoshTimelineEvent],
    match: ParsedMatch,
    *,
    holder_team: int | None,
    stats: _HolderWindowStats,
) -> None:
    """Append structure and buyback events to the conversion timeline."""
    if holder_team is None:
        return
    for tower in match.towers:
        if (
            stats.holder_window_start <= tower.tick <= stats.holder_window_end
            and tower.team == _enemy_team(holder_team)
        ):
            timeline_events.append(
                RoshTimelineEvent(tick=tower.tick, kind="tower", label="Tower taken")
            )
    for barracks in match.barracks:
        if (
            stats.holder_window_start <= barracks.tick <= stats.holder_window_end
            and barracks.team == _enemy_team(holder_team)
        ):
            timeline_events.append(
                RoshTimelineEvent(tick=barracks.tick, kind="barracks", label="Barracks taken")
            )
    enemy_team = _enemy_team(holder_team)
    for player in match.players:
        if player.team != enemy_team:
            continue
        for entry in player.buyback_log:
            if stats.holder_window_start <= entry.tick <= stats.holder_window_end:
                timeline_events.append(
                    RoshTimelineEvent(tick=entry.tick, kind="buyback", label="Enemy buyback")
                )


def _aegis_end_label(aegis_fate: str) -> str:
    """Return the timeline label for the Aegis window end."""
    return (
        "Aegis consumed"
        if aegis_fate == "consumed"
        else "Aegis expired"
        if aegis_fate == "expired"
        else "Aegis denied"
        if aegis_fate == "denied"
        else "Game ended"
        if aegis_fate == "game_end"
        else "Aegis window ended"
    )


def _finalize_timeline_events(
    timeline_events: list[RoshTimelineEvent],
    match: ParsedMatch,
    *,
    stats: _HolderWindowStats,
    holder_team: int | None,
    aegis_end_tick: int,
    aegis_fate: str,
    game_closed: bool,
) -> list[RoshTimelineEvent]:
    """Append derived timeline events and return them sorted."""
    _append_fight_timeline_events(timeline_events, stats, holder_team)
    _append_objective_timeline_events(timeline_events, match, holder_team=holder_team, stats=stats)
    timeline_events.append(
        RoshTimelineEvent(
            tick=aegis_end_tick,
            kind="aegis_end",
            label=_aegis_end_label(aegis_fate),
        )
    )
    if game_closed and match.game_end_tick > 0:
        timeline_events.append(
            RoshTimelineEvent(tick=match.game_end_tick, kind="game_end", label="Game ended")
        )
    timeline_events.sort(key=lambda event: (event.tick, event.kind))
    return timeline_events


def _build_conversion_record(
    match: ParsedMatch,
    *,
    rosh_number: int,
    roshan: Any,
    drops: list[str],
    had_high_value_drop: bool,
    bounds: _RoshWindowBounds,
    aegis: _AegisState,
    aegis_eval_end_tick: int,
    stats: _HolderWindowStats,
    game_closed: bool,
    timeline_events: list[RoshTimelineEvent],
) -> RoshConversion:
    """Build the final public conversion record from resolved inputs."""
    label = _conversion_label(
        holder_team=aegis.holder_team,
        aegis_fate=aegis.aegis_fate,
        fights_won=stats.fights_won,
        fights_lost=stats.fights_lost,
        towers_taken=stats.towers_taken,
        barracks_taken=stats.barracks_taken,
        enemy_half_observer_delta=stats.enemy_half_observer_delta,
        enemy_half_farm_share_delta=stats.enemy_half_farm_share_delta,
        game_closed=game_closed,
    )
    aegis_outcome = _aegis_outcome(
        holder_team=aegis.holder_team,
        aegis_fate=aegis.aegis_fate,
        fights_won=stats.fights_won,
        fights_lost=stats.fights_lost,
        towers_taken=stats.towers_taken,
        barracks_taken=stats.barracks_taken,
    )
    score = _conversion_score(
        fights_won=stats.fights_won,
        fights_lost=stats.fights_lost,
        towers_taken=stats.towers_taken,
        barracks_taken=stats.barracks_taken,
        enemy_buybacks_forced=stats.enemy_buybacks_forced,
        enemy_half_observer_delta=stats.enemy_half_observer_delta,
        enemy_half_farm_share_delta=stats.enemy_half_farm_share_delta,
        game_closed=game_closed,
        aegis_fate=aegis.aegis_fate,
    )
    drivers = _conversion_drivers(
        stats=stats,
        aegis_outcome=aegis_outcome,
        aegis_fate=aegis.aegis_fate,
    )
    timeline_events = _finalize_timeline_events(
        timeline_events,
        match,
        stats=stats,
        holder_team=aegis.holder_team,
        aegis_end_tick=aegis.aegis_end_tick,
        aegis_fate=aegis.aegis_fate,
        game_closed=game_closed,
    )

    return RoshConversion(
        rosh_number=rosh_number,
        rosh_tick=roshan.tick,
        killer_name=roshan.killer,
        drops=drops,
        had_high_value_drop=had_high_value_drop,
        banner_planted=stats.banner_planted,
        banner_rax_conversion=stats.banner_rax_conversion,
        banner_rax_lane=stats.banner_rax_lane,
        holder_team=aegis.holder_team,
        holder_player_id=aegis.holder_player_id,
        holder_name=aegis.holder_name,
        aegis_pickup_tick=aegis.aegis_pickup_tick,
        immediate_end_tick=bounds.immediate_end_tick,
        aegis_end_tick=aegis.aegis_end_tick,
        aegis_eval_end_tick=aegis_eval_end_tick,
        extended_end_tick=bounds.extended_end_tick,
        aegis_fate=aegis.aegis_fate,
        first_fight_tick=_first_fight_tick(stats),
        first_objective_tick=stats.first_objective_tick,
        fight_count=len(stats.fights),
        fights_won=stats.fights_won,
        fights_lost=stats.fights_lost,
        fights_drawn=stats.fights_drawn,
        towers_taken=stats.towers_taken,
        barracks_taken=stats.barracks_taken,
        enemy_buybacks_forced=stats.enemy_buybacks_forced,
        enemy_half_observer_delta=stats.enemy_half_observer_delta,
        enemy_half_farm_share_before=stats.enemy_half_farm_share_before,
        enemy_half_farm_share_during=stats.enemy_half_farm_share_during,
        enemy_half_farm_share_delta=stats.enemy_half_farm_share_delta,
        conversion_score=score,
        conversion_label=label,
        aegis_outcome=aegis_outcome,
        drivers=drivers,
        timeline_events=timeline_events,
    )


def build_rosh_conversions(match: ParsedMatch) -> list[RoshConversion]:
    """Summarise how well each Roshan was converted into advantage."""

    if not match.roshans:
        return []

    game_end_tick = infer_match_end_tick(match)
    conversions: list[RoshConversion] = []

    for index, roshan in enumerate(match.roshans, start=1):
        drops = list(getattr(roshan, "drops", ()) or ())
        had_high_value_drop = any(drop in _HIGH_VALUE_DROPS for drop in drops)
        bounds = _rosh_window_bounds(match, index, roshan.tick, game_end_tick)
        timeline_events = _initial_timeline_events(index, roshan.tick)

        aegis = _resolve_aegis_state(
            match,
            rosh_tick=roshan.tick,
            next_rosh_tick=bounds.next_rosh_tick,
            game_end_tick=game_end_tick,
            timeline_events=timeline_events,
        )
        aegis_eval_end_tick = _aegis_eval_end_tick(
            match,
            aegis_end_tick=aegis.aegis_end_tick,
            aegis_fate=aegis.aegis_fate,
            extended_end_tick=bounds.extended_end_tick,
            game_end_tick=game_end_tick,
        )
        stats = _holder_window_stats(
            match,
            holder_team=aegis.holder_team,
            aegis_pickup_tick=aegis.aegis_pickup_tick,
            rosh_tick=roshan.tick,
            immediate_end_tick=bounds.immediate_end_tick,
            aegis_eval_end_tick=aegis_eval_end_tick,
        )
        game_closed = _game_closed_by_holder(
            match,
            holder_team=aegis.holder_team,
            extended_end_tick=bounds.extended_end_tick,
        )

        conversions.append(
            _build_conversion_record(
                match,
                rosh_number=index,
                roshan=roshan,
                drops=drops,
                had_high_value_drop=had_high_value_drop,
                bounds=bounds,
                aegis=aegis,
                aegis_eval_end_tick=aegis_eval_end_tick,
                stats=stats,
                game_closed=game_closed,
                timeline_events=timeline_events,
            )
        )

    return conversions
