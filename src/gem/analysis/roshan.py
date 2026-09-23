"""Post-parse Roshan conversion analysis.

Turns existing replay facts (Roshan kills, Aegis events, teamfights, wards,
objectives, buybacks, and movement samples) into per-Roshan conversion records.
The goal is to answer a practical question: did the team translate Roshan into
fights, objectives, map expansion, or a game-closing sequence?
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Literal

from gem.analysis._shared import (
    _TEAM_DIRE,
    _TEAM_RADIANT,
    infer_match_end_tick,
    region_of,
)
from gem.analysis._territory import (
    DEFAULT_ROSH_TERRITORY_CONFIG,
    RoshCoverageCell as RoshCoverageCell,
    RoshTerritoryConfig as RoshTerritoryConfig,
    RoshTerritoryWindow,
    build_territory_window,
)
from gem.analysis.combat import is_active_teamfight_participant
from gem.analysis.teamfight_positioning import (
    EngagementStartSource,
    TeamfightPositioning,
    build_teamfight_positioning,
)
from gem.state.game_clock import game_clock_for

if TYPE_CHECKING:
    from gem.extractors.objectives import AegisEvent, BannerPlant
    from gem.extractors.teamfights import Teamfight
    from gem.results.models import ParsedMatch

_TICKS_PER_SEC = 30
_AEGIS_DURATION_TICKS = 5 * 60 * _TICKS_PER_SEC
_IMMEDIATE_WINDOW_TICKS = 180 * _TICKS_PER_SEC
_ASSOCIATION_WINDOW_TICKS = 30 * _TICKS_PER_SEC
_POST_AEGIS_ANALYSIS_TICKS = 120 * _TICKS_PER_SEC

# Non-exclusive evidence tags.  Thresholds are deliberately provisional and
# named here so calibration can change without rewriting the analysis flow.
ROSH_TAG_FIGHT_ADVANTAGE = "fight_advantage"
ROSH_TAG_OBJECTIVE_GAIN = "objective_gain"
ROSH_TAG_RESOURCE_GAIN = "resource_gain"
ROSH_TAG_TERRITORIAL_EXPANSION = "territorial_expansion"
ROSH_TAG_VISION_EXPANSION = "vision_expansion"
ROSH_TAG_TORMENTOR_SECURED = "tormentor_secured"
ROSH_TAG_GAME_CLOSING = "game_closing"
ROSH_TAG_COUNTER_CONVERSION = "counter_conversion"

_FIGHT_ADVANTAGE_THRESHOLD = 2
_OBJECTIVE_GAIN_THRESHOLD = 2
_NET_WORTH_SWING_THRESHOLD = 2_000
_XP_SWING_THRESHOLD = 1_500
_TERRITORY_SWING_THRESHOLD_PCT = 8.0
_WARD_DELTA_THRESHOLD = 2


class AegisFateSource(str, Enum):
    """Evidence or boundary used to classify an Aegis lifecycle."""

    __str__ = str.__str__

    DENIAL_EVENT = "denial_event"
    HOLDER_DEATH_INFERENCE = "holder_death_inference"
    NOMINAL_EXPIRY = "nominal_expiry"
    GAME_END_BOUNDARY = "game_end_boundary"
    NEXT_ROSHAN_BOUNDARY = "next_roshan_boundary"
    MISSING_EVENT = "missing_event"


class RoshTeamAttributionSource(str, Enum):
    """Provenance of a team attribution used by Roshan analysis."""

    __str__ = str.__str__

    PROTOCOL = "protocol"
    PLAYER_ID = "player_id"
    DAMAGE_SOURCE = "damage_source"
    ATTACKER = "attacker"
    UNKNOWN = "unknown"


class RoshFightRelation(str, Enum):
    """Temporal relationship between a fight and the conversion window."""

    __str__ = str.__str__

    PREEXISTING = "preexisting"
    IN_WINDOW = "in_window"


@dataclass(frozen=True, slots=True)
class RoshTagThresholds:
    """Inspectably configured thresholds for non-exclusive conversion tags."""

    fight_advantage: int = _FIGHT_ADVANTAGE_THRESHOLD
    objective_gain: int = _OBJECTIVE_GAIN_THRESHOLD
    net_worth_swing: int = _NET_WORTH_SWING_THRESHOLD
    xp_swing: int = _XP_SWING_THRESHOLD
    territory_swing_pct: float = _TERRITORY_SWING_THRESHOLD_PCT
    ward_delta: int = _WARD_DELTA_THRESHOLD
    counter_min_dimensions: int = 2
    ruleset: str = "provisional-v1"

    def __post_init__(self) -> None:
        numeric = (
            self.fight_advantage,
            self.objective_gain,
            self.net_worth_swing,
            self.xp_swing,
            self.territory_swing_pct,
            self.ward_delta,
            self.counter_min_dimensions,
        )
        if any(value < 0 for value in numeric):
            raise ValueError("Roshan tag thresholds must be nonnegative")
        if not self.ruleset:
            raise ValueError("Roshan tag threshold ruleset must not be empty")


DEFAULT_ROSH_TAG_THRESHOLDS = RoshTagThresholds()


@dataclass(frozen=True, slots=True)
class RoshFightEvidence:
    """Engagement-aware evidence for one fight associated with a Roshan window."""

    fight_index: int
    relation: RoshFightRelation
    engagement_start_tick: int
    engagement_start_source: EngagementStartSource
    first_death_tick: int
    end_tick: int
    winner: str
    deaths: int
    conversion_participant_ids: tuple[int, ...]
    opponent_participant_ids: tuple[int, ...]
    unknown_participant_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class _TeamAttribution:
    team: int | None
    source: RoshTeamAttributionSource


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
        "tower_lost",
        "tower_unknown",
        "barracks",
        "barracks_lost",
        "barracks_unknown",
        "buyback",
        "own_buyback",
        "tormentor",
        "opponent_tormentor",
        "tormentor_unknown",
        "banner",
        "opponent_banner",
        "aegis_end",
        "game_end",
    ]
    label: str
    fight_index: int | None = None


@dataclass
class RoshDifferentialProfile:
    """Evidence-first conversion-team profile over one hardened Rosh window.

    Count dimensions retain both sides' raw values as well as their signed
    conversion-minus-opponent differential.  Economy endpoints use the
    authoritative Radiant advantage curves, signed to ``conversion_team``.
    Unknown evidence is ``None`` rather than a fabricated zero.

    Attributes:
        conversion_team: Team being evaluated (2=Radiant, 3=Dire).
        opponent_team: Opposing team, or ``None`` when attribution failed.
        window_start_tick: Inclusive analysis-window start.
        window_end_tick: Inclusive analysis-window end.
        conversion_fights_won: Fights won by the conversion team.
        opponent_fights_won: Fights won by its opponent.
        fights_drawn: Explicitly drawn fights in the window.  All fight fields
            are unavailable if a fight winner is unknown.
        fight_differential: Conversion wins minus opponent wins.
        conversion_towers: Opponent towers destroyed by the conversion team.
        opponent_towers: Conversion-team towers destroyed by the opponent.
        conversion_barracks: Opponent barracks destroyed by the conversion team.
        opponent_barracks: Conversion-team barracks destroyed by the opponent.
        conversion_structure_value: Weighted structure value (T1=1, T2=2,
            T3=3, T4=4, barracks=4) gained by the conversion team.
        opponent_structure_value: Equivalent opponent value.
        structure_delta: Conversion minus opponent weighted structure value.
        net_worth_advantage_start: Conversion-signed gold/net-worth advantage at
            the first minute sample strictly after Roshan/Aegis pickup.
        net_worth_advantage_end: Conversion-signed advantage at the final sample.
        net_worth_swing: End minus start advantage.
        net_worth_swing_per_minute: Swing divided by sampled elapsed minutes.
        xp_advantage_start: Conversion-signed XP advantage at the first sample.
        xp_advantage_end: Conversion-signed XP advantage at the final sample.
        xp_swing: End minus start XP advantage.
        xp_swing_per_minute: XP swing per sampled minute.
        before_territory: Paired three-minute pre-Roshan territory evidence.
        during_territory: Paired territory evidence during the analysis window.
        conversion_coverage_swing_pct: Conversion team's during-minus-before
            coverage.
        opponent_coverage_swing_pct: Opponent's during-minus-before coverage.
        coverage_swing_pct: Double differential of the two coverage changes.
        conversion_depth_swing: Conversion team's during-minus-before depth p90.
        opponent_depth_swing: Opponent's during-minus-before depth p90.
        depth_swing: Double differential of the two depth changes.
        conversion_forward_wards: Conversion observer wards placed on enemy side.
        opponent_forward_wards: Opponent observer wards placed on enemy side.
        forward_ward_delta: Conversion minus opponent forward wards.
        conversion_tormentors: Tormentors attributed to the conversion team.
        opponent_tormentors: Tormentors attributed to the opponent.
        tormentor_delta: Conversion minus opponent Tormentors.
        tags: Non-exclusive evidence tags meeting provisional thresholds.
        status: Overall evidence availability.
        status_reasons: Machine-readable missing/partial evidence explanations.
    """

    conversion_team: int | None = None
    opponent_team: int | None = None
    window_start_tick: int | None = None
    window_end_tick: int | None = None
    conversion_fights_won: int | None = None
    opponent_fights_won: int | None = None
    fights_drawn: int | None = None
    fight_differential: int | None = None
    conversion_towers: int | None = None
    opponent_towers: int | None = None
    conversion_barracks: int | None = None
    opponent_barracks: int | None = None
    unattributed_towers: int = 0
    unattributed_barracks: int = 0
    conversion_structure_value: int | None = None
    opponent_structure_value: int | None = None
    structure_delta: int | None = None
    net_worth_advantage_start: int | None = None
    net_worth_advantage_end: int | None = None
    net_worth_swing: int | None = None
    net_worth_swing_per_minute: float | None = None
    xp_advantage_start: int | None = None
    xp_advantage_end: int | None = None
    xp_swing: int | None = None
    xp_swing_per_minute: float | None = None
    before_territory: RoshTerritoryWindow = field(default_factory=RoshTerritoryWindow)
    during_territory: RoshTerritoryWindow = field(default_factory=RoshTerritoryWindow)
    conversion_coverage_swing_pct: float | None = None
    opponent_coverage_swing_pct: float | None = None
    coverage_swing_pct: float | None = None
    conversion_depth_swing: float | None = None
    opponent_depth_swing: float | None = None
    depth_swing: float | None = None
    conversion_forward_wards: int | None = None
    opponent_forward_wards: int | None = None
    forward_ward_delta: int | None = None
    conversion_tormentors: int | None = None
    opponent_tormentors: int | None = None
    unattributed_tormentors: int = 0
    tormentor_delta: int | None = None
    tags: list[str] = field(default_factory=list)
    tag_ruleset: str = DEFAULT_ROSH_TAG_THRESHOLDS.ruleset
    status: Literal["complete", "partial", "unavailable"] = "unavailable"
    status_reasons: list[str] = field(default_factory=list)


@dataclass
class RoshConversion:
    """Derived summary for one Roshan kill and the advantage window that followed.

    Most fields summarise the Aegis window (holder, fights, objectives, map
    control). ``drops`` and ``had_high_value_drop`` describe what Roshan yielded
    beyond the Aegis itself.

    Attributes:
        conversion_score: Deprecated aggregate compatibility field. Prefer raw
            ``differential_profile`` values; retained through the 0.9 line and
            not scheduled for removal before 1.0.
        conversion_label: Deprecated exclusive compatibility field. Prefer
            non-exclusive ``conversion_tags``; retained through the 0.9 line
            and not scheduled for removal before 1.0.
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
        roshan_team: Attributable team that killed Roshan, independent of who
            ultimately claimed the Aegis.
        conversion_team: Aegis holder team for pickup/stolen events, otherwise
            the attributable Roshan-killer team for denied/missing Aegis.
        roshan_team_source: Provenance of ``roshan_team``.
        conversion_team_source: Provenance of ``conversion_team``.
        aegis_fate_source: Event, inference, or boundary used for lifecycle fate.
        aegis_fate_inferred: Whether ``consumed`` was inferred from the holder's
            death inside the validated ownership horizon.
        first_engagement_tick: Earliest engagement-aware start in the window.
        fight_evidence: Per-fight temporal, participant, and provenance records.
        conversion_tags: Non-exclusive evidence tags mirrored from the
            differential profile.
        analysis_status: ``complete``, ``partial``, or ``unavailable`` evidence.
        analysis_status_reasons: Machine-readable explanations for incomplete
            evidence.
        differential_profile: Paired conversion-team/opponent evidence profile.
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
    roshan_team: int | None = None
    conversion_team: int | None = None
    roshan_team_source: RoshTeamAttributionSource = RoshTeamAttributionSource.UNKNOWN
    conversion_team_source: RoshTeamAttributionSource = RoshTeamAttributionSource.UNKNOWN
    aegis_fate_source: AegisFateSource = AegisFateSource.MISSING_EVENT
    aegis_fate_inferred: bool = False
    first_engagement_tick: int | None = None
    fight_evidence: list[RoshFightEvidence] = field(default_factory=list)
    conversion_tags: list[str] = field(default_factory=list)
    analysis_status: Literal["complete", "partial", "unavailable"] = "unavailable"
    analysis_status_reasons: list[str] = field(default_factory=list)
    differential_profile: RoshDifferentialProfile = field(default_factory=RoshDifferentialProfile)


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


def _fight_evidence(
    match: ParsedMatch,
    conversion_team: int | None,
    positioning: TeamfightPositioning,
    window_start_tick: int,
) -> RoshFightEvidence:
    fight = match.teamfights[positioning.fight_index]
    teams_by_player = {
        player.player_id: player.team
        for player in match.players
        if player.team in (_TEAM_RADIANT, _TEAM_DIRE)
    }
    active_ids = tuple(
        stats.player_id for stats in fight.players if is_active_teamfight_participant(stats)
    )
    opponent_team = _enemy_team(conversion_team) if conversion_team is not None else None
    conversion_ids = tuple(
        player_id for player_id in active_ids if teams_by_player.get(player_id) == conversion_team
    )
    opponent_ids = tuple(
        player_id for player_id in active_ids if teams_by_player.get(player_id) == opponent_team
    )
    known = set(conversion_ids) | set(opponent_ids)
    unknown_ids = tuple(player_id for player_id in active_ids if player_id not in known)
    first_death_tick = (
        fight.first_death_tick
        if fight.start_tick <= fight.first_death_tick <= fight.end_tick
        else positioning.first_death_tick
    )
    return RoshFightEvidence(
        fight_index=positioning.fight_index,
        relation=(
            RoshFightRelation.PREEXISTING
            if positioning.engagement_start_tick < window_start_tick
            else RoshFightRelation.IN_WINDOW
        ),
        engagement_start_tick=positioning.engagement_start_tick,
        engagement_start_source=positioning.engagement_start_source,
        first_death_tick=first_death_tick,
        end_tick=fight.end_tick,
        winner=fight.winner,
        deaths=fight.deaths,
        conversion_participant_ids=conversion_ids,
        opponent_participant_ids=opponent_ids,
        unknown_participant_ids=unknown_ids,
    )


def _enemy_team(team: int) -> int:
    return _TEAM_DIRE if team == _TEAM_RADIANT else _TEAM_RADIANT


def _analysis_match_end_tick(match: ParsedMatch) -> int:
    if (match.post_game_tick or 0) > 0 or match.game_end_tick > 0:
        return infer_match_end_tick(match)
    observed = [infer_match_end_tick(match)]
    for events in (
        match.roshans,
        match.aegis_events,
        match.towers,
        match.barracks,
        match.wards,
        match.tormentors,
        match.combat_log,
        match.banner_plants,
    ):
        observed.extend(event.tick for event in events)
    observed.extend(fight.end_tick for fight in match.teamfights)
    return max(observed, default=0)


def _find_associated_aegis_event(
    match: ParsedMatch, rosh_tick: int, next_rosh_tick: int | None
) -> AegisEvent | None:
    association_end = min(
        rosh_tick + _ASSOCIATION_WINDOW_TICKS,
        _analysis_match_end_tick(match),
    )
    if next_rosh_tick is not None:
        association_end = min(association_end, next_rosh_tick - 1)
    for event in sorted(match.aegis_events, key=lambda item: item.tick):
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
        if start_tick <= tower.tick <= end_tick
        and _structure_destroyer_team(
            match, tower.team, tower.killer, tower.killer_source, tower.killer_team
        )
        == team
    )
    barracks_taken = sum(
        1
        for barracks in match.barracks
        if start_tick <= barracks.tick <= end_tick
        and _structure_destroyer_team(
            match,
            barracks.team,
            barracks.killer,
            barracks.killer_source,
            barracks.killer_team,
        )
        == team
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
    gated on side by attributed destruction and excluding allied denies.

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
    converted_lanes = [
        (barracks.tick, _rax_lane(barracks.barracks_name))
        for barracks in match.barracks
        if earliest_plant_tick <= barracks.tick <= end_tick
        and _structure_destroyer_team(
            match,
            barracks.team,
            barracks.killer,
            barracks.killer_source,
            barracks.killer_team,
        )
        == team
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
        if start_tick <= tower.tick <= end_tick
        and _structure_destroyer_team(
            match, tower.team, tower.killer, tower.killer_source, tower.killer_team
        )
        == team
    ]
    candidates.extend(
        barracks.tick
        for barracks in match.barracks
        if start_tick <= barracks.tick <= end_tick
        and _structure_destroyer_team(
            match,
            barracks.team,
            barracks.killer,
            barracks.killer_source,
            barracks.killer_team,
        )
        == team
    )
    return min(candidates) if candidates else None


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


def _team_attribution(
    match: ParsedMatch,
    *,
    killer: str,
    killer_source: str = "",
    protocol_team: int | None = None,
    player_id: int | None = None,
) -> _TeamAttribution:
    if protocol_team in (_TEAM_RADIANT, _TEAM_DIRE):
        return _TeamAttribution(protocol_team, RoshTeamAttributionSource.PROTOCOL)
    player_team = _team_for_player(match, player_id)
    if player_team is not None:
        return _TeamAttribution(player_team, RoshTeamAttributionSource.PLAYER_ID)
    for name, source in (
        (killer_source, RoshTeamAttributionSource.DAMAGE_SOURCE),
        (killer, RoshTeamAttributionSource.ATTACKER),
    ):
        if not name:
            continue
        candidates = {
            player.team
            for player in match.players
            if player.hero_name == name and player.team in (_TEAM_RADIANT, _TEAM_DIRE)
        }
        if len(candidates) == 1:
            return _TeamAttribution(candidates.pop(), source)
    if killer.startswith(("npc_dota_goodguys_", "npc_dota_creep_goodguys_")):
        return _TeamAttribution(_TEAM_RADIANT, RoshTeamAttributionSource.ATTACKER)
    if killer.startswith(("npc_dota_badguys_", "npc_dota_creep_badguys_")):
        return _TeamAttribution(_TEAM_DIRE, RoshTeamAttributionSource.ATTACKER)
    return _TeamAttribution(None, RoshTeamAttributionSource.UNKNOWN)


def _structure_destroyer_team(
    match: ParsedMatch,
    owner_team: int,
    killer: str,
    killer_source: str,
    killer_team: int | None = None,
) -> int | None:
    attribution = _team_attribution(
        match,
        killer=killer,
        killer_source=killer_source,
        protocol_team=killer_team,
    )
    if attribution.team == owner_team:
        return None
    return attribution.team


def _team_for_tormentor_kill(
    match: ParsedMatch,
    killer_player_id: int,
    killer: str,
    killer_team: int | None = None,
) -> int | None:
    return _team_attribution(
        match,
        killer=killer,
        protocol_team=killer_team,
        player_id=killer_player_id,
    ).team


def _tower_value(tower_name: str) -> int:
    for tier, value in (("tower4", 4), ("tower3", 3), ("tower2", 2), ("tower1", 1)):
        if tier in tower_name:
            return value
    return 0


def _structure_values(
    match: ParsedMatch, conversion_team: int, start_tick: int, end_tick: int
) -> tuple[int, int, int, int, int, int, int, int]:
    opponent_team = _enemy_team(conversion_team)
    conversion_towers = []
    opponent_towers = []
    unattributed_towers = 0
    for tower in match.towers:
        if not start_tick <= tower.tick <= end_tick:
            continue
        attribution = _team_attribution(
            match,
            killer=tower.killer,
            killer_source=tower.killer_source,
            protocol_team=tower.killer_team,
        )
        if attribution.team == tower.team:
            continue
        if attribution.team == conversion_team:
            conversion_towers.append(tower)
        elif attribution.team == opponent_team:
            opponent_towers.append(tower)
        else:
            unattributed_towers += 1

    conversion_barracks = []
    opponent_barracks = []
    unattributed_barracks = 0
    for barracks in match.barracks:
        if not start_tick <= barracks.tick <= end_tick:
            continue
        attribution = _team_attribution(
            match,
            killer=barracks.killer,
            killer_source=barracks.killer_source,
            protocol_team=barracks.killer_team,
        )
        if attribution.team == barracks.team:
            continue
        if attribution.team == conversion_team:
            conversion_barracks.append(barracks)
        elif attribution.team == opponent_team:
            opponent_barracks.append(barracks)
        else:
            unattributed_barracks += 1
    conversion_value = sum(_tower_value(tower.tower_name) for tower in conversion_towers)
    conversion_value += 4 * len(conversion_barracks)
    opponent_value = sum(_tower_value(tower.tower_name) for tower in opponent_towers)
    opponent_value += 4 * len(opponent_barracks)
    return (
        len(conversion_towers),
        len(opponent_towers),
        len(conversion_barracks),
        len(opponent_barracks),
        unattributed_towers,
        unattributed_barracks,
        conversion_value,
        opponent_value,
    )


def _resource_dimension(
    match: ParsedMatch,
    values: list[int],
    conversion_team: int,
    start_tick: int,
    end_tick: int,
) -> tuple[int | None, int | None, int | None, float | None]:
    count = min(len(match.game_times_min), len(values))
    if count < 2:
        return None, None, None, None
    # Minute samples are keyed by pause-aware game seconds; map them back to
    # replay ticks through the game clock so pauses do not shift the window.
    clock = game_clock_for(match)
    samples = []
    for index in range(count):
        game_seconds = match.game_times_min[index]
        sample_tick = clock.tick_at(game_seconds)
        if sample_tick is not None:
            samples.append((sample_tick, game_seconds, values[index]))
    # Strictly after pickup/Roshan excludes the direct bounty from the baseline.
    eligible = [sample for sample in samples if start_tick < sample[0] <= end_tick]
    if len(eligible) < 2:
        return None, None, None, None
    sign = 1 if conversion_team == _TEAM_RADIANT else -1
    _, first_seconds, first_value = eligible[0]
    _, last_seconds, last_value = eligible[-1]
    start_value = first_value * sign
    end_value = last_value * sign
    swing = end_value - start_value
    elapsed_minutes = (last_seconds - first_seconds) / 60
    rate = swing / elapsed_minutes if elapsed_minutes > 0 else None
    return start_value, end_value, swing, rate


def _territory_swing(
    before_conversion: float | None,
    during_conversion: float | None,
    before_opponent: float | None,
    during_opponent: float | None,
) -> tuple[float | None, float | None, float | None]:
    conversion_swing = (
        during_conversion - before_conversion
        if during_conversion is not None and before_conversion is not None
        else None
    )
    opponent_swing = (
        during_opponent - before_opponent
        if during_opponent is not None and before_opponent is not None
        else None
    )
    double_differential = (
        conversion_swing - opponent_swing
        if conversion_swing is not None and opponent_swing is not None
        else None
    )
    return conversion_swing, opponent_swing, double_differential


def _tormentor_counts(
    match: ParsedMatch, conversion_team: int, start_tick: int, end_tick: int
) -> tuple[int, int, int]:
    conversion_count = opponent_count = 0
    unattributed_count = 0
    for tormentor in match.tormentors:
        if not start_tick <= tormentor.tick <= end_tick:
            continue
        team = _team_for_tormentor_kill(
            match,
            tormentor.killer_player_id,
            tormentor.killer,
            tormentor.killer_team,
        )
        if team == conversion_team:
            conversion_count += 1
        elif team == _enemy_team(conversion_team):
            opponent_count += 1
        else:
            unattributed_count += 1
    return conversion_count, opponent_count, unattributed_count


def _forward_ward_count(
    match: ParsedMatch, team: int, start_tick: int, end_tick: int
) -> int | None:
    count = 0
    wanted_region = _enemy_half_name(team)
    for ward in match.wards:
        if ward.team != team or ward.ward_type != "observer":
            continue
        if not start_tick <= ward.tick <= end_tick:
            continue
        if ward.x is None or ward.y is None:
            return None
        if region_of(ward.x, ward.y) == wanted_region:
            count += 1
    return count


def _profile_tags(
    profile: RoshDifferentialProfile,
    game_closed: bool,
    thresholds: RoshTagThresholds,
) -> list[str]:
    tags: list[str] = []
    if (
        profile.fight_differential is not None
        and profile.fight_differential >= thresholds.fight_advantage
    ):
        tags.append(ROSH_TAG_FIGHT_ADVANTAGE)
    if profile.structure_delta is not None and profile.structure_delta >= thresholds.objective_gain:
        tags.append(ROSH_TAG_OBJECTIVE_GAIN)
    if (
        profile.net_worth_swing is not None
        and profile.net_worth_swing >= thresholds.net_worth_swing
    ) or (profile.xp_swing is not None and profile.xp_swing >= thresholds.xp_swing):
        tags.append(ROSH_TAG_RESOURCE_GAIN)
    if (
        profile.coverage_swing_pct is not None
        and profile.coverage_swing_pct >= thresholds.territory_swing_pct
    ):
        tags.append(ROSH_TAG_TERRITORIAL_EXPANSION)
    if profile.forward_ward_delta is not None and (
        profile.forward_ward_delta >= thresholds.ward_delta
        or (
            profile.forward_ward_delta >= 1
            and profile.coverage_swing_pct is not None
            and profile.coverage_swing_pct > 0
        )
    ):
        tags.append(ROSH_TAG_VISION_EXPANSION)
    if profile.tormentor_delta is not None and profile.tormentor_delta > 0:
        tags.append(ROSH_TAG_TORMENTOR_SECURED)
    if game_closed:
        tags.append(ROSH_TAG_GAME_CLOSING)

    positive = sum(
        (
            profile.fight_differential is not None
            and profile.fight_differential >= thresholds.fight_advantage,
            profile.structure_delta is not None
            and profile.structure_delta >= thresholds.objective_gain,
            profile.net_worth_swing is not None
            and profile.net_worth_swing >= thresholds.net_worth_swing,
            profile.xp_swing is not None and profile.xp_swing >= thresholds.xp_swing,
            profile.coverage_swing_pct is not None
            and profile.coverage_swing_pct >= thresholds.territory_swing_pct,
            profile.forward_ward_delta is not None
            and profile.forward_ward_delta >= thresholds.ward_delta,
            profile.tormentor_delta is not None and profile.tormentor_delta > 0,
        )
    )
    opponent_positive = sum(
        (
            profile.fight_differential is not None
            and profile.fight_differential <= -thresholds.fight_advantage,
            profile.structure_delta is not None
            and profile.structure_delta <= -thresholds.objective_gain,
            profile.net_worth_swing is not None
            and profile.net_worth_swing <= -thresholds.net_worth_swing,
            profile.xp_swing is not None and profile.xp_swing <= -thresholds.xp_swing,
            profile.coverage_swing_pct is not None
            and profile.coverage_swing_pct <= -thresholds.territory_swing_pct,
            profile.forward_ward_delta is not None
            and profile.forward_ward_delta <= -thresholds.ward_delta,
            profile.tormentor_delta is not None and profile.tormentor_delta < 0,
        )
    )
    # "Dominates" requires at least two meaningful opponent-positive dimensions,
    # avoiding a counter-conversion label from one noisy signal.
    if opponent_positive >= thresholds.counter_min_dimensions and opponent_positive > positive:
        tags.append(ROSH_TAG_COUNTER_CONVERSION)
    return tags


def _differential_profile(
    match: ParsedMatch,
    conversion_team: int | None,
    rosh_tick: int,
    window_start: int,
    window_end: int,
    fights: list[Teamfight],
    *,
    partial_aegis_evidence: bool,
    game_closed: bool,
    tag_thresholds: RoshTagThresholds,
    territory_config: RoshTerritoryConfig,
) -> RoshDifferentialProfile:
    profile = RoshDifferentialProfile(
        conversion_team=conversion_team,
        opponent_team=_enemy_team(conversion_team) if conversion_team is not None else None,
        window_start_tick=window_start,
        window_end_tick=window_end,
        tag_ruleset=tag_thresholds.ruleset,
    )
    if conversion_team is None:
        profile.status_reasons.append("conversion_team_unavailable")
        return profile

    wanted_winner = "radiant" if conversion_team == _TEAM_RADIANT else "dire"
    opponent_winner = "dire" if conversion_team == _TEAM_RADIANT else "radiant"
    if all(fight.winner in ("radiant", "dire", "draw") for fight in fights):
        profile.conversion_fights_won = sum(fight.winner == wanted_winner for fight in fights)
        profile.opponent_fights_won = sum(fight.winner == opponent_winner for fight in fights)
        profile.fights_drawn = sum(fight.winner == "draw" for fight in fights)
        profile.fight_differential = profile.conversion_fights_won - profile.opponent_fights_won

    (
        profile.conversion_towers,
        profile.opponent_towers,
        profile.conversion_barracks,
        profile.opponent_barracks,
        profile.unattributed_towers,
        profile.unattributed_barracks,
        profile.conversion_structure_value,
        profile.opponent_structure_value,
    ) = _structure_values(match, conversion_team, window_start, window_end)
    profile.structure_delta = profile.conversion_structure_value - profile.opponent_structure_value

    (
        profile.net_worth_advantage_start,
        profile.net_worth_advantage_end,
        profile.net_worth_swing,
        profile.net_worth_swing_per_minute,
    ) = _resource_dimension(
        match,
        match.radiant_gold_adv,
        conversion_team,
        window_start,
        window_end,
    )
    (
        profile.xp_advantage_start,
        profile.xp_advantage_end,
        profile.xp_swing,
        profile.xp_swing_per_minute,
    ) = _resource_dimension(
        match,
        match.radiant_xp_adv,
        conversion_team,
        window_start,
        window_end,
    )

    before_start = max(match.game_start_tick or 0, rosh_tick - _IMMEDIATE_WINDOW_TICKS)
    before_end = max(before_start, rosh_tick - 1)
    profile.before_territory = build_territory_window(
        match,
        conversion_team,
        before_start,
        before_end,
        config=territory_config,
    )
    profile.during_territory = build_territory_window(
        match,
        conversion_team,
        window_start,
        window_end,
        config=territory_config,
    )
    (
        profile.conversion_coverage_swing_pct,
        profile.opponent_coverage_swing_pct,
        profile.coverage_swing_pct,
    ) = _territory_swing(
        profile.before_territory.conversion_coverage_pct,
        profile.during_territory.conversion_coverage_pct,
        profile.before_territory.opponent_coverage_pct,
        profile.during_territory.opponent_coverage_pct,
    )
    (
        profile.conversion_depth_swing,
        profile.opponent_depth_swing,
        profile.depth_swing,
    ) = _territory_swing(
        profile.before_territory.conversion_depth_p90,
        profile.during_territory.conversion_depth_p90,
        profile.before_territory.opponent_depth_p90,
        profile.during_territory.opponent_depth_p90,
    )

    opponent_team = _enemy_team(conversion_team)
    profile.conversion_forward_wards = _forward_ward_count(
        match, conversion_team, window_start, window_end
    )
    profile.opponent_forward_wards = _forward_ward_count(
        match, opponent_team, window_start, window_end
    )
    if profile.conversion_forward_wards is not None and profile.opponent_forward_wards is not None:
        profile.forward_ward_delta = (
            profile.conversion_forward_wards - profile.opponent_forward_wards
        )
    (
        profile.conversion_tormentors,
        profile.opponent_tormentors,
        profile.unattributed_tormentors,
    ) = _tormentor_counts(match, conversion_team, window_start, window_end)
    if profile.conversion_tormentors is not None and profile.opponent_tormentors is not None:
        profile.tormentor_delta = profile.conversion_tormentors - profile.opponent_tormentors

    reasons: list[str] = []
    if partial_aegis_evidence:
        reasons.append("aegis_window_partial_or_unavailable")
    if profile.net_worth_swing is None:
        reasons.append("net_worth_series_unavailable")
    if profile.xp_swing is None:
        reasons.append("xp_series_unavailable")
    if profile.before_territory.status != "complete":
        reasons.append("before_territory_unavailable")
    if profile.during_territory.status != "complete":
        reasons.append("during_territory_unavailable")
    if profile.forward_ward_delta is None:
        reasons.append("forward_ward_positions_unavailable")
    if profile.unattributed_tormentors:
        reasons.append("tormentor_attribution_unavailable")
    if profile.unattributed_towers or profile.unattributed_barracks:
        reasons.append("structure_attribution_unavailable")
    if profile.fight_differential is None:
        reasons.append("fight_winner_unavailable")
    profile.status_reasons = reasons
    profile.status = "partial" if reasons else "complete"
    profile.tags = _profile_tags(profile, game_closed, tag_thresholds)
    return profile


def build_rosh_conversions(
    match: ParsedMatch,
    *,
    tag_thresholds: RoshTagThresholds = DEFAULT_ROSH_TAG_THRESHOLDS,
    territory_config: RoshTerritoryConfig = DEFAULT_ROSH_TERRITORY_CONFIG,
) -> list[RoshConversion]:
    """Summarise each Roshan with legacy fields and differential evidence.

    Args:
        match: Parsed match containing objective, combat, economy, vision, and
            movement timelines.
        tag_thresholds: Inspectable threshold rules for non-exclusive tags.
        territory_config: Inspectable sampling and coverage calibration inputs.

    Returns:
        One conversion record per Roshan kill, in chronological order.
    """
    if not match.roshans:
        return []

    game_end_tick = _analysis_match_end_tick(match)
    # Observed end of the match (Ancient destroyed), or 0 when unknown. Unlike
    # ``game_end_tick`` this never falls back to inferred sample ticks.
    match_end_tick = (
        infer_match_end_tick(match)
        if (match.post_game_tick or 0) > 0 or match.game_end_tick > 0
        else 0
    )
    conversions: list[RoshConversion] = []
    claimed_fights: set[int] = set()
    positioning_by_index = {
        positioning.fight_index: positioning for positioning in build_teamfight_positioning(match)
    }

    for index, roshan in enumerate(match.roshans, start=1):
        next_rosh_tick = match.roshans[index].tick if index < len(match.roshans) else None
        boundary = min(
            game_end_tick,
            next_rosh_tick - 1 if next_rosh_tick is not None else game_end_tick,
        )
        immediate_end_tick = min(roshan.tick + _IMMEDIATE_WINDOW_TICKS, boundary)
        roshan_attribution = _team_attribution(
            match,
            killer=roshan.killer,
            killer_source=getattr(roshan, "killer_source", ""),
            protocol_team=getattr(roshan, "killer_team", None),
        )
        roshan_team = roshan_attribution.team
        aegis_event = _find_associated_aegis_event(match, roshan.tick, next_rosh_tick)

        holder_player_id: int | None = None
        holder_team: int | None = None
        holder_name = ""
        aegis_pickup_tick: int | None = None
        aegis_fate: Literal["consumed", "expired", "denied", "game_end", "unknown"]
        aegis_fate = "unknown"
        aegis_fate_source = AegisFateSource.MISSING_EVENT
        aegis_fate_inferred = False
        conversion_team: int | None = None
        conversion_team_source = RoshTeamAttributionSource.UNKNOWN
        analysis_start = roshan.tick
        analysis_end = immediate_end_tick
        aegis_end_tick = immediate_end_tick
        timeline_events = [
            RoshTimelineEvent(
                tick=roshan.tick,
                kind="roshan",
                label=f"Roshan #{index} killed",
            )
        ]

        if aegis_event is not None and aegis_event.event_type == "denied":
            aegis_pickup_tick = aegis_event.tick
            aegis_end_tick = aegis_event.tick
            aegis_fate = "denied"
            aegis_fate_source = AegisFateSource.DENIAL_EVENT
            conversion_team = roshan_team
            conversion_team_source = roshan_attribution.source
            timeline_events.append(
                RoshTimelineEvent(
                    tick=aegis_event.tick,
                    kind="aegis_denied",
                    label="Aegis denied",
                )
            )
        elif aegis_event is not None and aegis_event.event_type in ("pickup", "stolen"):
            holder_player_id = aegis_event.player_id if aegis_event.player_id >= 0 else None
            holder_team = _team_for_player(match, holder_player_id)
            holder_name = _hero_for_player(match, holder_player_id)
            conversion_team = holder_team
            conversion_team_source = (
                RoshTeamAttributionSource.PLAYER_ID
                if holder_team is not None
                else RoshTeamAttributionSource.UNKNOWN
            )
            aegis_pickup_tick = aegis_event.tick
            analysis_start = aegis_event.tick
            timeline_events.append(
                RoshTimelineEvent(
                    tick=aegis_event.tick,
                    kind="aegis_pickup",
                    label=(
                        "Aegis -> " + holder_name.removeprefix("npc_dota_hero_").replace("_", " ")
                        if holder_name
                        else "Aegis claimed"
                    ),
                )
            )
            nominal_expiry = aegis_event.tick + _AEGIS_DURATION_TICKS
            ownership_end = min(nominal_expiry, boundary)
            consume_tick = _holder_death_tick(match, holder_name, aegis_event.tick, ownership_end)
            if consume_tick is not None:
                aegis_end_tick = consume_tick
                aegis_fate = "consumed"
                aegis_fate_source = AegisFateSource.HOLDER_DEATH_INFERENCE
                aegis_fate_inferred = True
            elif nominal_expiry <= boundary:
                aegis_end_tick = nominal_expiry
                aegis_fate = "expired"
                aegis_fate_source = AegisFateSource.NOMINAL_EXPIRY
            elif boundary == game_end_tick:
                aegis_end_tick = game_end_tick
                aegis_fate = "game_end"
                aegis_fate_source = AegisFateSource.GAME_END_BOUNDARY
            else:
                aegis_end_tick = boundary
                aegis_fate = "unknown"
                aegis_fate_source = AegisFateSource.NEXT_ROSHAN_BOUNDARY
            analysis_end = min(aegis_end_tick + _POST_AEGIS_ANALYSIS_TICKS, boundary)
            if aegis_fate == "consumed":
                overlapping = _window_teamfights(match, aegis_end_tick, aegis_end_tick)
                if overlapping:
                    analysis_end = min(
                        boundary,
                        max(analysis_end, max(fight.end_tick for fight in overlapping)),
                    )
        else:
            conversion_team = roshan_team
            conversion_team_source = roshan_attribution.source

        fight_records: list[tuple[int, Teamfight]] = []
        for fight_index, fight in enumerate(match.teamfights):
            if fight_index in claimed_fights:
                continue
            positioning = positioning_by_index[fight_index]
            if (
                positioning.engagement_start_tick <= analysis_end
                and fight.end_tick >= analysis_start
            ):
                fight_records.append((fight_index, fight))
                claimed_fights.add(fight_index)
        fights = [fight for _, fight in fight_records]
        fight_evidence = [
            _fight_evidence(
                match, conversion_team, positioning_by_index[fight_index], analysis_start
            )
            for fight_index, _ in fight_records
        ]

        if conversion_team is None:
            fights_won = fights_lost = 0
            fights_drawn = len(fights)
            towers_taken = barracks_taken = 0
            enemy_buybacks_forced = 0
            enemy_half_observer_delta = 0
            enemy_half_farm_share_before = 0.0
            enemy_half_farm_share_during = 0.0
            enemy_half_farm_share_delta = 0.0
            first_objective_tick = None
            banner_planted = False
            banner_rax_conversion = False
            banner_rax_lane: str | None = None
        else:
            wanted = "radiant" if conversion_team == _TEAM_RADIANT else "dire"
            opposing = "dire" if conversion_team == _TEAM_RADIANT else "radiant"
            fights_won = sum(fight.winner == wanted for fight in fights)
            fights_lost = sum(fight.winner == opposing for fight in fights)
            fights_drawn = len(fights) - fights_won - fights_lost
            towers_taken, barracks_taken = _count_objectives(
                match, conversion_team, analysis_start, analysis_end
            )
            enemy_buybacks_forced = _count_enemy_buybacks(
                match, conversion_team, analysis_start, analysis_end
            )
            own_forward_wards = _enemy_half_observer_placements(
                match, conversion_team, analysis_start, analysis_end
            )
            opponent_forward_wards = _enemy_half_observer_placements(
                match, _enemy_team(conversion_team), analysis_start, analysis_end
            )
            enemy_half_observer_delta = own_forward_wards - opponent_forward_wards
            baseline_start = max(match.game_start_tick or 0, roshan.tick - _IMMEDIATE_WINDOW_TICKS)
            enemy_half_farm_share_before = _enemy_half_farm_share(
                match, conversion_team, baseline_start, roshan.tick - 1
            )
            enemy_half_farm_share_during = _enemy_half_farm_share(
                match, conversion_team, roshan.tick, immediate_end_tick
            )
            enemy_half_farm_share_delta = (
                enemy_half_farm_share_during - enemy_half_farm_share_before
            )
            first_objective_tick = _first_objective_tick(
                match, conversion_team, analysis_start, analysis_end
            )
            banner_planted, banner_rax_conversion, banner_rax_lane = _banner_rax_signal(
                match, conversion_team, analysis_start, analysis_end
            )

        game_closed = (
            conversion_team is not None
            and match.radiant_win is not None
            and (
                (conversion_team == _TEAM_RADIANT and match.radiant_win)
                or (conversion_team == _TEAM_DIRE and not match.radiant_win)
            )
            and match_end_tick > 0
            and analysis_start <= match_end_tick <= analysis_end
        )
        profile = _differential_profile(
            match,
            conversion_team,
            roshan.tick,
            analysis_start,
            analysis_end,
            fights,
            partial_aegis_evidence=(
                aegis_event is None or aegis_event.event_type == "denied" or conversion_team is None
            ),
            game_closed=game_closed,
            tag_thresholds=tag_thresholds,
            territory_config=territory_config,
        )

        label = _conversion_label(
            holder_team=conversion_team,
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
            holder_team=conversion_team,
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
        if banner_rax_conversion:
            lane_text = f"{banner_rax_lane} " if banner_rax_lane else ""
            drivers.append(f"planted Roshan's Banner ahead of a {lane_text}barracks push")
        elif banner_planted:
            drivers.append("planted Roshan's Banner during the window")
        if enemy_buybacks_forced:
            drivers.append(f"forced {enemy_buybacks_forced} enemy buyback(s)")
        if enemy_half_observer_delta > 0:
            drivers.append(
                f"placed {enemy_half_observer_delta} more observer ward(s) in enemy territory than they conceded"
            )
        if aegis_outcome == "expired_unused":
            drivers.append("Aegis expired before delivering a second life")
        elif aegis_fate == "denied":
            drivers.append("Aegis was denied, so the team never got the immortality window")
        elif aegis_outcome == "window_lost":
            drivers.append("The Aegis window was lost without offsetting structures")
        elif aegis_fate == "consumed":
            drivers.append("Aegis was popped during the conversion window")

        first_fight_tick = min(
            (max(fight.first_death_tick, analysis_start) for fight in fights),
            default=None,
        )
        first_engagement_tick = min(
            (evidence.engagement_start_tick for evidence in fight_evidence),
            default=None,
        )
        for (fight_index, fight), evidence in zip(fight_records, fight_evidence, strict=True):
            fight_tick = max(evidence.engagement_start_tick, analysis_start)
            if conversion_team is None or fight.winner not in ("radiant", "dire"):
                kind: Literal["fight_win", "fight_loss", "fight_draw"] = "fight_draw"
                label_text = f"Fight ({fight.deaths} deaths)"
            elif (conversion_team == _TEAM_RADIANT and fight.winner == "radiant") or (
                conversion_team == _TEAM_DIRE and fight.winner == "dire"
            ):
                kind = "fight_win"
                label_text = f"Fight won ({fight.deaths} deaths)"
            else:
                kind = "fight_loss"
                label_text = f"Fight lost ({fight.deaths} deaths)"
            if evidence.relation is RoshFightRelation.PREEXISTING:
                label_text = "Fight already underway, " + label_text.removeprefix("Fight ")
            timeline_events.append(
                RoshTimelineEvent(
                    tick=fight_tick,
                    kind=kind,
                    label=label_text,
                    fight_index=fight_index,
                )
            )

        if conversion_team is not None:
            enemy_team = _enemy_team(conversion_team)
            for tower in match.towers:
                if not analysis_start <= tower.tick <= analysis_end:
                    continue
                killer_attribution = _team_attribution(
                    match,
                    killer=tower.killer,
                    killer_source=tower.killer_source,
                    protocol_team=tower.killer_team,
                )
                destroyer_team = (
                    None if killer_attribution.team == tower.team else killer_attribution.team
                )
                if destroyer_team == conversion_team:
                    timeline_events.append(
                        RoshTimelineEvent(tick=tower.tick, kind="tower", label="Tower taken")
                    )
                elif destroyer_team == enemy_team:
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=tower.tick,
                            kind="tower_lost",
                            label="Tower lost",
                        )
                    )
                elif killer_attribution.team is None:
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=tower.tick,
                            kind="tower_unknown",
                            label="Tower destroyed (team unavailable)",
                        )
                    )
            for barracks in match.barracks:
                if not analysis_start <= barracks.tick <= analysis_end:
                    continue
                killer_attribution = _team_attribution(
                    match,
                    killer=barracks.killer,
                    killer_source=barracks.killer_source,
                    protocol_team=barracks.killer_team,
                )
                destroyer_team = (
                    None if killer_attribution.team == barracks.team else killer_attribution.team
                )
                if destroyer_team == conversion_team:
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=barracks.tick,
                            kind="barracks",
                            label="Barracks taken",
                        )
                    )
                elif destroyer_team == enemy_team:
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=barracks.tick,
                            kind="barracks_lost",
                            label="Barracks lost",
                        )
                    )
                elif killer_attribution.team is None:
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=barracks.tick,
                            kind="barracks_unknown",
                            label="Barracks destroyed (team unavailable)",
                        )
                    )
            for player in match.players:
                if player.team not in (conversion_team, enemy_team):
                    continue
                for entry in player.buyback_log:
                    if analysis_start <= entry.tick <= analysis_end:
                        timeline_events.append(
                            RoshTimelineEvent(
                                tick=entry.tick,
                                kind="buyback" if player.team == enemy_team else "own_buyback",
                                label=(
                                    "Enemy buyback"
                                    if player.team == enemy_team
                                    else "Conversion-team buyback"
                                ),
                            )
                        )
            for tormentor in match.tormentors:
                if not analysis_start <= tormentor.tick <= analysis_end:
                    continue
                killer_team = _team_for_tormentor_kill(
                    match,
                    tormentor.killer_player_id,
                    tormentor.killer,
                    tormentor.killer_team,
                )
                if killer_team in (conversion_team, enemy_team):
                    label_text = (
                        "Tormentor secured"
                        if killer_team == conversion_team
                        else "Opponent secured Tormentor"
                    )
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=tormentor.tick,
                            kind=(
                                "tormentor"
                                if killer_team == conversion_team
                                else "opponent_tormentor"
                            ),
                            label=label_text,
                        )
                    )
                else:
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=tormentor.tick,
                            kind="tormentor_unknown",
                            label="Tormentor killed (team unavailable)",
                        )
                    )
            for plant in match.banner_plants:
                if not analysis_start <= plant.tick <= analysis_end:
                    continue
                if plant.team in (conversion_team, enemy_team):
                    timeline_events.append(
                        RoshTimelineEvent(
                            tick=plant.tick,
                            kind=("banner" if plant.team == conversion_team else "opponent_banner"),
                            label=(
                                "Roshan's Banner planted"
                                if plant.team == conversion_team
                                else "Opponent planted Roshan's Banner"
                            ),
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
        if game_closed:
            timeline_events.append(
                RoshTimelineEvent(
                    tick=match_end_tick,
                    kind="game_end",
                    label="Game ended",
                )
            )
        timeline_events.sort(key=lambda event: (event.tick, event.kind))

        drops = list(getattr(roshan, "drops", ()) or ())
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
                aegis_eval_end_tick=analysis_end,
                extended_end_tick=boundary,
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
                drops=drops,
                had_high_value_drop=any(drop in _HIGH_VALUE_DROPS for drop in drops),
                banner_planted=banner_planted,
                banner_rax_conversion=banner_rax_conversion,
                banner_rax_lane=banner_rax_lane,
                roshan_team=roshan_team,
                conversion_team=conversion_team,
                roshan_team_source=roshan_attribution.source,
                conversion_team_source=conversion_team_source,
                aegis_fate_source=aegis_fate_source,
                aegis_fate_inferred=aegis_fate_inferred,
                first_engagement_tick=first_engagement_tick,
                fight_evidence=fight_evidence,
                conversion_tags=list(profile.tags),
                analysis_status=profile.status,
                analysis_status_reasons=list(profile.status_reasons),
                differential_profile=profile,
            )
        )

    return conversions
