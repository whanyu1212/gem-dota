"""Post-parse Roshan conversion analysis.

Turns existing replay facts (Roshan kills, Aegis events, teamfights, wards,
objectives, buybacks, and movement samples) into per-Roshan conversion records.
The goal is to answer a practical question: did the team translate Roshan into
fights, objectives, map expansion, or a game-closing sequence?
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from gem.extractors.objectives import AegisEvent
    from gem.extractors.teamfights import Teamfight
    from gem.models import ParsedMatch

_TEAM_RADIANT = 2
_TEAM_DIRE = 3
_TICKS_PER_SEC = 30
_AEGIS_DURATION_TICKS = 5 * 60 * _TICKS_PER_SEC
_IMMEDIATE_WINDOW_TICKS = 180 * _TICKS_PER_SEC
_ASSOCIATION_WINDOW_TICKS = 30 * _TICKS_PER_SEC
_POST_CONSUME_GRACE_TICKS = 30 * _TICKS_PER_SEC

_MAP_XMIN = 7563.0
_MAP_XMAX = 25900.0
_MAP_YMIN = 7800.0
_MAP_YMAX = 25600.0
_RADIANT_FOUNTAIN = (9684.0, 9684.0)
_DIRE_FOUNTAIN = (23120.0, 22350.0)


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
    """Derived summary for one Roshan kill and the advantage window that followed."""

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


def _infer_match_end_tick(match: ParsedMatch) -> int:
    if match.game_end_tick > 0:
        return match.game_end_tick
    max_tick = 0
    for player in match.players:
        if player.times:
            max_tick = max(max_tick, player.times[-1])
        if player.position_log:
            max_tick = max(max_tick, player.position_log[-1][0])
    return max_tick


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


def _region_of(x: float, y: float) -> str:
    if abs(x - y) <= 1200:
        return "river"
    dr = ((x - _RADIANT_FOUNTAIN[0]) ** 2 + (y - _RADIANT_FOUNTAIN[1]) ** 2) ** 0.5
    dd = ((x - _DIRE_FOUNTAIN[0]) ** 2 + (y - _DIRE_FOUNTAIN[1]) ** 2) ** 0.5
    return "radiant_half" if dr <= dd else "dire_half"


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
        if _region_of(ward.x, ward.y) == region_name:
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
            if _region_of(x, y) == region_name:
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


def build_rosh_conversions(match: ParsedMatch) -> list[RoshConversion]:
    """Summarise how well each Roshan was converted into advantage."""

    if not match.roshans:
        return []

    game_end_tick = _infer_match_end_tick(match)
    conversions: list[RoshConversion] = []

    for index, roshan in enumerate(match.roshans, start=1):
        next_rosh_tick = match.roshans[index].tick if index < len(match.roshans) else None
        immediate_end_tick = min(roshan.tick + _IMMEDIATE_WINDOW_TICKS, game_end_tick)
        extended_end_tick = (next_rosh_tick - 1) if next_rosh_tick is not None else game_end_tick
        extended_end_tick = min(extended_end_tick, game_end_tick)

        aegis_event = _find_associated_aegis_event(match, roshan.tick, next_rosh_tick)
        holder_player_id: int | None = None
        holder_team: int | None = None
        holder_name = ""
        aegis_pickup_tick: int | None = None
        aegis_end_tick = min(roshan.tick + _AEGIS_DURATION_TICKS, game_end_tick)
        aegis_fate: Literal["consumed", "expired", "denied", "game_end", "unknown"] = "unknown"
        timeline_events = [
            RoshTimelineEvent(
                tick=roshan.tick,
                kind="roshan",
                label=f"Roshan #{index} killed",
            )
        ]

        if aegis_event is not None:
            if aegis_event.event_type == "denied":
                aegis_pickup_tick = aegis_event.tick
                aegis_end_tick = aegis_event.tick
                aegis_fate = "denied"
                timeline_events.append(
                    RoshTimelineEvent(
                        tick=aegis_event.tick, kind="aegis_denied", label="Aegis denied"
                    )
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
                        label=(
                            "Aegis -> "
                            + holder_name.removeprefix("npc_dota_hero_").replace("_", " ")
                        )
                        if holder_name
                        else "Aegis claimed",
                    )
                )
                raw_expiry_tick = min(aegis_event.tick + _AEGIS_DURATION_TICKS, game_end_tick)
                consume_tick = _holder_death_tick(
                    match, holder_name, aegis_event.tick, raw_expiry_tick
                )
                if consume_tick is not None:
                    aegis_end_tick = consume_tick
                    aegis_fate = "consumed"
                elif raw_expiry_tick >= game_end_tick:
                    aegis_end_tick = game_end_tick
                    aegis_fate = "game_end"
                else:
                    aegis_end_tick = raw_expiry_tick
                    aegis_fate = "expired"
        else:
            aegis_end_tick = min(roshan.tick + _AEGIS_DURATION_TICKS, game_end_tick)

        aegis_eval_end_tick = aegis_end_tick
        if aegis_fate == "consumed":
            overlapping = _window_teamfights(match, aegis_end_tick, aegis_end_tick)
            if overlapping:
                aegis_eval_end_tick = min(
                    game_end_tick,
                    max(
                        aegis_end_tick + _POST_CONSUME_GRACE_TICKS,
                        max(f.end_tick for f in overlapping),
                    ),
                )
            else:
                aegis_eval_end_tick = min(game_end_tick, aegis_end_tick + _POST_CONSUME_GRACE_TICKS)

        if holder_team is None:
            holder_window_start = roshan.tick
            holder_window_end = aegis_eval_end_tick
            fights: list[Teamfight] = _window_teamfights(
                match, holder_window_start, holder_window_end
            )
            fights_won = fights_lost = 0
            fights_drawn = len(fights)
            towers_taken = 0
            barracks_taken = 0
            enemy_buybacks_forced = 0
            enemy_half_observer_delta = 0
            enemy_half_farm_share_before = 0.0
            enemy_half_farm_share_during = 0.0
            enemy_half_farm_share_delta = 0.0
            first_objective_tick = None
        else:
            holder_window_start = aegis_pickup_tick or roshan.tick
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
            baseline_start = max(
                (match.game_start_tick or 0), roshan.tick - _IMMEDIATE_WINDOW_TICKS
            )
            baseline_end = roshan.tick - 1
            enemy_half_farm_share_before = _enemy_half_farm_share(
                match, holder_team, baseline_start, baseline_end
            )
            enemy_half_farm_share_during = _enemy_half_farm_share(
                match, holder_team, roshan.tick, immediate_end_tick
            )
            enemy_half_farm_share_delta = (
                enemy_half_farm_share_during - enemy_half_farm_share_before
            )
            first_objective_tick = _first_objective_tick(
                match, holder_team, holder_window_start, holder_window_end
            )

        first_fight_tick = min(
            (max(fight.first_death_tick, holder_window_start) for fight in fights),
            default=None,
        )
        game_closed = (
            holder_team is not None
            and match.radiant_win is not None
            and (
                (holder_team == _TEAM_RADIANT and match.radiant_win)
                or (holder_team == _TEAM_DIRE and not match.radiant_win)
            )
            and match.game_end_tick > 0
            and match.game_end_tick <= extended_end_tick
        )

        label = _conversion_label(
            holder_team=holder_team,
            aegis_fate=aegis_fate,
            fights_won=fights_won,
            fights_lost=fights_lost,
            towers_taken=towers_taken,
            barracks_taken=barracks_taken,
            enemy_half_observer_delta=enemy_half_observer_delta,
            enemy_half_farm_share_delta=enemy_half_farm_share_delta,
            game_closed=game_closed,
        )
        aegis_outcome = _aegis_outcome(
            holder_team=holder_team,
            aegis_fate=aegis_fate,
            fights_won=fights_won,
            fights_lost=fights_lost,
            towers_taken=towers_taken,
            barracks_taken=barracks_taken,
        )
        score = _conversion_score(
            fights_won=fights_won,
            fights_lost=fights_lost,
            towers_taken=towers_taken,
            barracks_taken=barracks_taken,
            enemy_buybacks_forced=enemy_buybacks_forced,
            enemy_half_observer_delta=enemy_half_observer_delta,
            enemy_half_farm_share_delta=enemy_half_farm_share_delta,
            game_closed=game_closed,
            aegis_fate=aegis_fate,
        )

        drivers: list[str] = []
        if fights_won:
            drivers.append(f"won {fights_won} fight(s) during the Aegis window")
        if fights_lost:
            drivers.append(f"lost {fights_lost} fight(s) during the Aegis window")
        if towers_taken:
            drivers.append(f"took {towers_taken} tower(s)")
        if barracks_taken:
            drivers.append(f"took {barracks_taken} barracks")
        if enemy_buybacks_forced:
            drivers.append(f"forced {enemy_buybacks_forced} enemy buyback(s)")
        if enemy_half_observer_delta > 0:
            drivers.append(
                f"placed {enemy_half_observer_delta} more observer ward(s) in enemy territory than they conceded"
            )
        if enemy_half_farm_share_delta >= 0.10:
            drivers.append(
                f"expanded enemy-half presence by {round(enemy_half_farm_share_delta * 100):d} percentage points"
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

        for fight in fights:
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
            timeline_events.append(RoshTimelineEvent(tick=fight_tick, kind=kind, label=label_text))

        if holder_team is not None:
            for tower in match.towers:
                if (
                    holder_window_start <= tower.tick <= holder_window_end
                    and tower.team == _enemy_team(holder_team)
                ):
                    timeline_events.append(
                        RoshTimelineEvent(tick=tower.tick, kind="tower", label="Tower taken")
                    )
            for barracks in match.barracks:
                if (
                    holder_window_start <= barracks.tick <= holder_window_end
                    and barracks.team == _enemy_team(holder_team)
                ):
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=barracks.tick, kind="barracks", label="Barracks taken"
                        )
                    )
            enemy_team = _enemy_team(holder_team)
            for player in match.players:
                if player.team != enemy_team:
                    continue
                for entry in player.buyback_log:
                    if holder_window_start <= entry.tick <= holder_window_end:
                        timeline_events.append(
                            RoshTimelineEvent(
                                tick=entry.tick, kind="buyback", label="Enemy buyback"
                            )
                        )

        timeline_events.append(
            RoshTimelineEvent(
                tick=aegis_end_tick,
                kind="aegis_end",
                label=(
                    "Aegis consumed"
                    if aegis_fate == "consumed"
                    else "Aegis expired"
                    if aegis_fate == "expired"
                    else "Aegis denied"
                    if aegis_fate == "denied"
                    else "Game ended"
                    if aegis_fate == "game_end"
                    else "Aegis window ended"
                ),
            )
        )
        if game_closed and match.game_end_tick > 0:
            timeline_events.append(
                RoshTimelineEvent(tick=match.game_end_tick, kind="game_end", label="Game ended")
            )
        timeline_events.sort(key=lambda event: (event.tick, event.kind))

        conversions.append(
            RoshConversion(
                rosh_number=index,
                rosh_tick=roshan.tick,
                killer_name=roshan.killer,
                holder_team=holder_team,
                holder_player_id=holder_player_id,
                holder_name=holder_name,
                aegis_pickup_tick=aegis_pickup_tick,
                immediate_end_tick=immediate_end_tick,
                aegis_end_tick=aegis_end_tick,
                aegis_eval_end_tick=aegis_eval_end_tick,
                extended_end_tick=extended_end_tick,
                aegis_fate=aegis_fate,
                first_fight_tick=first_fight_tick,
                first_objective_tick=first_objective_tick,
                fight_count=len(fights),
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
                conversion_score=score,
                conversion_label=label,
                aegis_outcome=aegis_outcome,
                drivers=drivers,
                timeline_events=timeline_events,
            )
        )

    return conversions
