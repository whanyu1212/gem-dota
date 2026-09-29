"""Output data models for gem replay parsing.

Defines ``ParsedPlayer`` and ``ParsedMatch`` dataclasses that aggregate all
extracted information into a structured, ML-friendly output.

Reference: odota/parser src/main/java/opendota/CreateParsedDataBlob.java
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from gem.combat.log import CombatLogEntry, CombatLogSource
from gem.extractors.courier import CourierSnapshot
from gem.extractors.draft import DraftEvent
from gem.extractors.objectives import (
    AegisEvent,
    BannerPlant,
    BarracksKill,
    CourierDeath,
    RoshanKill,
    ShrineKill,
    TormentorKill,
    TowerKill,
)
from gem.extractors.teamfights import OpenDotaTeamfight, Teamfight
from gem.extractors.wards import WardEvent
from gem.state.game_clock import GameClock


class VisibilityState(str, Enum):
    """A team's authoritative visibility state for one hero entity.

    Attributes:
        VISIBLE: The team visibility bit is present and set.
        HIDDEN: The team visibility bit is present and clear.
        UNKNOWN: The team entity, visibility word, or hero identity is absent.
    """

    __str__ = str.__str__

    VISIBLE = "visible"
    HIDDEN = "hidden"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class HeroVisibilityEvent:
    """A visibility-state transition for one canonical player hero identity.

    Attributes:
        tick: Replay tick at the completed-packet boundary.
        player_id: Logical player slot from 0 through 9.
        hero_name: Canonical NPC hero name when available.
        entity_index: Entity-table index for this hero identity.
        entity_serial: Entity serial distinguishing reuse of the same index.
        radiant_state: Visibility of the hero to Radiant.
        dire_state: Visibility of the hero to Dire.
    """

    tick: int
    player_id: int
    hero_name: str
    entity_index: int
    entity_serial: int
    radiant_state: VisibilityState
    dire_state: VisibilityState


@dataclass(frozen=True, slots=True)
class EntityVisibilityEvent:
    """Packet-boundary visibility evidence for one networked Dota NPC entity.

    Only active networked entities whose send-table class derives from the
    Dota NPC schema (identified by ``m_iDayTimeVisionRange``) are sampled.
    Visibility states are evidence at completed packet boundaries, not a
    reconstruction of fog of war between packets.

    Attributes:
        tick: Replay tick at the completed-packet boundary.
        entity_index: Entity-table slot index.
        entity_serial: Entity serial distinguishing reuse of the same slot.
        class_name: Network send-table class name.
        npc_name: ``EntityNames`` value, or ``class_name`` when unavailable.
        team: Raw ``m_iTeamNum`` value, or ``None`` when unavailable.
        active: Whether this identity was active at the packet boundary.
        radiant_state: Visibility of the entity to Radiant.
        dire_state: Visibility of the entity to Dire.
    """

    tick: int
    entity_index: int
    entity_serial: int
    class_name: str
    npc_name: str
    team: int | None
    active: bool
    radiant_state: VisibilityState
    dire_state: VisibilityState


class VisionModifierSemantic(str, Enum):
    """How a tracked modifier contributes vision evidence."""

    __str__ = str.__str__

    DIRECT_TARGET_REVEAL = "direct_target_reveal"
    REVEAL_AURA = "reveal_aura"
    AURA_CARRIER = "aura_carrier"
    OTHER_VISION_RELEVANT = "other_vision_relevant"


class VisionModifierLifecycleStatus(str, Enum):
    """Best-supported lifecycle state for a modifier application."""

    __str__ = str.__str__

    REMOVED = "removed"
    EXPIRED = "expired"
    OPEN = "open"
    INCOMPLETE = "incomplete"


class VisionModifierCloseEvidence(str, Enum):
    """Evidence supporting the lifecycle close classification."""

    __str__ = str.__str__

    OBSERVED = "observed"
    DURATION_INFERRED = "duration_inferred"
    UNOBSERVED = "unobserved"
    AMBIGUOUS = "ambiguous"


class VisionModifierPairingStatus(str, Enum):
    """Confidence with which a removal was paired to an application."""

    __str__ = str.__str__

    EXACT = "exact"
    UNIQUE_FALLBACK = "unique_fallback"
    AMBIGUOUS = "ambiguous"
    UNMATCHED = "unmatched"


class VisionModifierTeamSource(str, Enum):
    """Evidence source used to attribute a modifier participant's team."""

    __str__ = str.__str__

    PROTOCOL = "protocol"
    SNAPSHOT_FALLBACK = "snapshot_fallback"
    UNKNOWN = "unknown"


@dataclass
class VisionModifierEvent:
    """One tracked vision-relevant modifier application and its evidence.

    Applications include direct hero reveals, non-hero targets, reveal auras,
    and aura carriers. Only a conservative subset is consumed by point-vision
    analysis; this record preserves the broader combat-log evidence.

    Attributes:
        tick: Game tick when the modifier was applied.
        end_tick: Game tick when the modifier was removed, or ``None`` if still
            active at game end or removal was not observed.
        modifier_name: Internal modifier name, e.g. ``"modifier_slardar_amplify_damage"``.
        target_name: NPC name of the unit that received the modifier.
        caster_name: NPC name of the unit that applied the modifier.
        caster_team: Team of the caster (2=Radiant, 3=Dire), or 0 if unknown.
        semantic: Descriptor-backed interpretation of the modifier.
        lifecycle_status: Removed, expired, open, or incomplete classification.
        close_evidence: Observed, duration-inferred, unobserved, or ambiguous close.
        pairing_status: Confidence linking an observed removal to this application.
        target_is_hero: Whether the application target was protocol-marked as a hero.
        caster_is_hero: Whether the application caster was protocol-marked as a hero.
        caster_is_illusion: Whether the application caster was an illusion.
        target_is_illusion: Whether the application target was an illusion.
        caster_is_hero_present: Whether caster hero status was explicit.
        target_is_hero_present: Whether target hero status was explicit.
        caster_is_illusion_present: Whether caster illusion status was explicit.
        target_is_illusion_present: Whether target illusion status was explicit.
        target_team: Team of the target, or 0 if unknown.
        caster_team_source: Evidence source used for ``caster_team``.
        target_team_source: Evidence source used for ``target_team``.
        add_attacker_team: Raw protocol attacker team on application.
        add_target_team: Raw protocol target team on application.
        remove_attacker_team: Raw protocol attacker team on removal.
        remove_target_team: Raw protocol target team on removal.
        add_source: Combat-log ingestion path for the application.
        remove_source: Combat-log ingestion path for the removal, when observed.
        add_game_time_s: Pause-aware application game time, when available.
        remove_game_time_s: Pause-aware removal game time, when available.
        add_modifier_duration_s: Intended duration reported on application.
        remove_modifier_duration_s: Intended duration reported on removal.
        add_modifier_elapsed_duration_s: Elapsed duration reported on application.
        remove_modifier_elapsed_duration_s: Elapsed duration reported on removal.
        add_aura_modifier: Optional aura flag reported on application.
        remove_aura_modifier: Optional aura flag reported on removal.
        remove_modifier_purged: Optional purge flag reported on removal.
        remove_modifier_purged_duration_s: Purged-duration evidence on removal.
        remove_caster_name: Caster name carried by the removal observation.
        remove_caster_is_hero: Explicit removal caster hero status, if present.
        remove_target_is_hero: Explicit removal target hero status, if present.
        remove_caster_is_illusion: Explicit removal caster illusion status, if present.
        remove_target_is_illusion: Explicit removal target illusion status, if present.
        evidence_gaps: Stable labels describing unavailable or ambiguous evidence.
    """

    tick: int
    end_tick: int | None
    modifier_name: str
    target_name: str
    caster_name: str
    caster_team: int
    semantic: VisionModifierSemantic = VisionModifierSemantic.DIRECT_TARGET_REVEAL
    lifecycle_status: VisionModifierLifecycleStatus = VisionModifierLifecycleStatus.OPEN
    close_evidence: VisionModifierCloseEvidence = VisionModifierCloseEvidence.UNOBSERVED
    pairing_status: VisionModifierPairingStatus = VisionModifierPairingStatus.EXACT
    target_is_hero: bool = True
    caster_is_hero: bool = False
    caster_is_illusion: bool = False
    target_is_illusion: bool = False
    caster_is_hero_present: bool = False
    target_is_hero_present: bool = False
    caster_is_illusion_present: bool = False
    target_is_illusion_present: bool = False
    target_team: int = 0
    caster_team_source: VisionModifierTeamSource = VisionModifierTeamSource.UNKNOWN
    target_team_source: VisionModifierTeamSource = VisionModifierTeamSource.UNKNOWN
    add_attacker_team: int | None = None
    add_target_team: int | None = None
    remove_attacker_team: int | None = None
    remove_target_team: int | None = None
    add_source: CombatLogSource = CombatLogSource.UNKNOWN
    remove_source: CombatLogSource | None = None
    add_game_time_s: int | None = None
    remove_game_time_s: int | None = None
    add_modifier_duration_s: float | None = None
    remove_modifier_duration_s: float | None = None
    add_modifier_elapsed_duration_s: float | None = None
    remove_modifier_elapsed_duration_s: float | None = None
    add_aura_modifier: bool | None = None
    remove_aura_modifier: bool | None = None
    remove_modifier_purged: bool | None = None
    remove_modifier_purged_duration_s: float | None = None
    remove_caster_name: str = ""
    remove_caster_is_hero: bool | None = None
    remove_target_is_hero: bool | None = None
    remove_caster_is_illusion: bool | None = None
    remove_target_is_illusion: bool | None = None
    evidence_gaps: list[str] = field(default_factory=list)


@dataclass
class VisionModifierPairingIssue:
    """Removal evidence that could not be paired to one application safely.

    Attributes:
        tick: Exact replay tick of the removal observation.
        reason: Stable machine-readable reason (``ambiguous`` or ``unmatched``).
        modifier_name: Internal modifier name.
        caster_name: Caster name carried by the removal.
        target_name: Target name carried by the removal.
        source: Combat-log ingestion path for the removal.
        candidate_add_ticks: Eligible application ticks when pairing was ambiguous.
        game_time_s: Pause-aware removal game time when available.
        modifier_duration_s: Duration carried by the removal when available.
        modifier_elapsed_duration_s: Elapsed duration carried by the removal.
        attacker_team: Protocol attacker team on the removal.
        target_team: Protocol target team on the removal.
        caster_is_hero: Explicit caster hero status on the removal, if present.
        target_is_hero: Explicit target hero status on the removal, if present.
        caster_is_illusion: Explicit caster illusion status, if present.
        target_is_illusion: Explicit target illusion status, if present.
    """

    tick: int
    reason: str
    modifier_name: str
    caster_name: str
    target_name: str
    source: CombatLogSource = CombatLogSource.UNKNOWN
    candidate_add_ticks: list[int] = field(default_factory=list)
    game_time_s: int | None = None
    modifier_duration_s: float | None = None
    modifier_elapsed_duration_s: float | None = None
    attacker_team: int | None = None
    target_team: int | None = None
    caster_is_hero: bool | None = None
    target_is_hero: bool | None = None
    caster_is_illusion: bool | None = None
    target_is_illusion: bool | None = None
    aura_modifier: bool | None = None
    modifier_purged: bool | None = None
    modifier_purged_duration_s: float | None = None


@dataclass
class SmokeParticipant:
    """One hero's observed Smoke of Deceit modifier lifecycle.

    Attributes:
        hero_name: NPC name of the hero that received the smoke modifier.
        player_id: Logical player slot from 0 through 9, or ``None`` when the
            hero could not be matched to a player snapshot.
        applied_tick: Exact combat-log tick when the modifier was added.
        removed_tick: Exact combat-log tick when the modifier was removed, or
            ``None`` when no removal was observed.
        modifier_duration_s: Intended modifier duration reported by the S2
            combat log, or ``None`` when unavailable.
        modifier_elapsed_duration_s: Elapsed duration reported on modifier
            removal, or ``None`` when unavailable.
        applied_x: Sampled world x coordinate at ``applied_tick``, or ``None``.
        applied_y: Sampled world y coordinate at ``applied_tick``, or ``None``.
        removed_x: Sampled world x coordinate at ``removed_tick``, or ``None``.
        removed_y: Sampled world y coordinate at ``removed_tick``, or ``None``.
        applied_game_time_s: Pause-aware game time when the modifier was added,
            or ``None`` when unavailable.
        removed_game_time_s: Pause-aware game time when the modifier was
            removed, or ``None`` when unavailable.
    """

    hero_name: str
    player_id: int | None
    applied_tick: int
    removed_tick: int | None = None
    modifier_duration_s: float | None = None
    modifier_elapsed_duration_s: float | None = None
    applied_x: float | None = None
    applied_y: float | None = None
    removed_x: float | None = None
    removed_y: float | None = None
    applied_game_time_s: int | None = None
    removed_game_time_s: int | None = None


@dataclass
class SmokeEvent:
    """One Smoke of Deceit activation.

    Attributes:
        tick: Game tick when the smoke item was consumed.
        activator: NPC hero name of the player who used the smoke.
        team: Team number (2=Radiant, 3=Dire), or 0 if unknown.
        smoked: NPC hero names of all heroes that received the buff.
        x: Legacy member-centroid world x coordinate, computed from participant
            positions at their individual modifier-application ticks, or
            ``None`` when no participant position is available.
        y: Legacy member-centroid world y coordinate, with the same semantics as
            ``x``.
        activation_x: Activating hero's sampled world x coordinate at the exact
            item-use tick, or ``None`` when unavailable.
        activation_y: Activating hero's sampled world y coordinate at the exact
            item-use tick, or ``None`` when unavailable.
        participants: Per-hero modifier lifecycles in observed application order.
        activation_game_time_s: Pause-aware game time when the item was used,
            or ``None`` when unavailable.
    """

    tick: int
    activator: str
    team: int
    smoked: list[str] = field(default_factory=list)
    x: float | None = None
    y: float | None = None
    activation_x: float | None = None
    activation_y: float | None = None
    participants: list[SmokeParticipant] = field(default_factory=list)
    activation_game_time_s: int | None = None


@dataclass
class BuybackEvent:
    """One buyback and its gold cost.

    The team data entity counts each player's gold spent on buybacks
    (``m_vecDataTeam.NNNN.m_iGoldSpentOnBuybacks``). It rises on the same tick as
    the BUYBACK combat-log entry, by exactly the cost, so ``cost`` is exact when
    that rise was observed (``cost_exact``). Otherwise ``cost`` falls back to the
    Dota 2 formula ``200 + net_worth // 13`` at the buyback tick (see
    :func:`gem.results.derived.buyback_cost`).

    ``reliable_gold`` / ``unreliable_gold`` estimate how the cost was paid. Dota
    spends unreliable gold first, so the estimate is ``min(cost, unreliable gold
    before the buyback)`` from the unreliable pool and the rest from the reliable
    pool. It is dropped when a pool fell by more than the estimate says was paid
    from it on that update (something else, such as a purchase, spent gold too).
    Income arriving in the same update before the buyback can still shift the
    true split by that income. ``None`` when the cost is not exact or the check
    fails.

    The raw combat-log entries remain on ``ParsedPlayer.buyback_log``; this is the
    structured, cost-bearing view alongside it.

    Attributes:
        tick: Game tick when the buyback fired.
        player_slot: The player's slot (0-9).
        cost: Buyback cost in gold: exact when ``cost_exact``, else the formula
            estimate.
        net_worth: Net worth at the buyback tick.
        cost_exact: Whether ``cost`` is the observed rise in gold spent on buybacks.
        reliable_gold: Estimated part of ``cost`` paid from reliable gold, or
            ``None``.
        unreliable_gold: Estimated part of ``cost`` paid from unreliable gold, or
            ``None``.
    """

    tick: int
    player_slot: int
    cost: int
    net_worth: int
    cost_exact: bool = False
    reliable_gold: int | None = None
    unreliable_gold: int | None = None


@dataclass
class GoldLedgerSnapshot:
    """One reading of a player's gold ledger from the team data entity.

    Every value is a running total since the start of the game, read from
    ``CDOTA_DataRadiant``/``CDOTA_DataDire`` ``m_vecDataTeam.NNNN.*``. None of the
    pinned upstream parsers reads these fields; their meaning is established
    against the replay's embedded postgame summary (``CMsgDOTAMatch``):

    - ``spent_on_items + spent_on_consumables`` equals the summary's
      ``gold_spent`` (and OpenDota's).
    - ``lost_to_death`` equals the summary's ``gold_lost_to_death``.
    - The earned sources (``hero_kill_gold`` through ``other_gold``) sum to the
      team data's ``m_iTotalEarnedGold``. ``shared_gold`` overlaps them and is
      not part of that sum. A gold source the game adds before the replay
      schema has a field for it is missing from the sum (seen once, on a newer
      patch).
    - ``spent_on_support`` is part of ``spent_on_items + spent_on_consumables``,
      not a separate category.

    Attributes:
        tick: Replay tick the values were read at.
        game_time_s: Game-relative seconds of that reading.
        hero_kill_gold: Gold from hero kills and assists (``m_iHeroKillGold``).
        creep_kill_gold: Gold from lane creep kills (``m_iCreepKillGold``).
        neutral_kill_gold: Gold from neutral creep kills (``m_iNeutralKillGold``).
        income_gold: Passive gold income (``m_iIncomeGold``).
        building_gold: Gold from buildings (``m_iBuildingGold``).
        roshan_gold: Gold from Roshan (``m_iRoshanGold``).
        bounty_gold: Gold from bounty runes (``m_iBountyGold``).
        ward_kill_gold: Gold from killing wards (``m_iWardKillGold``).
        courier_gold: Gold from killing couriers (``m_iCourierGold``).
        ability_gold: Gold granted by abilities (``m_iAbilityGold``).
        comeback_gold: Comeback gold (``m_iComebackGold``).
        creep_deny_gold: Gold from denies (``m_iCreepDenyGold``).
        other_gold: Other gold (``m_iOtherGold``).
        shared_gold: Gold shared from allies' kills (``m_iSharedGold``); already
            counted in the sources above.
        spent_on_items: Gold spent on items (``m_iGoldSpentOnItems``).
        spent_on_consumables: Gold spent on consumables
            (``m_iGoldSpentOnConsumables``).
        spent_on_support: Gold spent on support items (``m_iGoldSpentOnSupport``);
            a subset of the two above.
        spent_on_buybacks: Gold spent on buybacks (``m_iGoldSpentOnBuybacks``).
        lost_to_death: Gold lost on death (``m_iGoldLostToDeath``).
    """

    tick: int
    game_time_s: int
    hero_kill_gold: int = 0
    creep_kill_gold: int = 0
    neutral_kill_gold: int = 0
    income_gold: int = 0
    building_gold: int = 0
    roshan_gold: int = 0
    bounty_gold: int = 0
    ward_kill_gold: int = 0
    courier_gold: int = 0
    ability_gold: int = 0
    comeback_gold: int = 0
    creep_deny_gold: int = 0
    other_gold: int = 0
    shared_gold: int = 0
    spent_on_items: int = 0
    spent_on_consumables: int = 0
    spent_on_support: int = 0
    spent_on_buybacks: int = 0
    lost_to_death: int = 0


@dataclass
class GoldLedger:
    """A player's gold ledger at game end and at every game minute.

    Attributes:
        final: The ledger read at the game-end tick, or ``None`` when the game
            end was not reached (e.g. a truncated replay).
        per_minute: One snapshot per game minute, parallel to
            ``ParsedPlayer.game_times_min``. Empty when the replay had no
            complete per-minute interval data.
    """

    final: GoldLedgerSnapshot | None = None
    per_minute: list[GoldLedgerSnapshot] = field(default_factory=list)


@dataclass
class ChatEntry:
    """A single chat message from the match.

    Attributes:
        tick: Game tick when the message was sent.
        player_slot: Source player slot (0–9).
        channel: ``"all"`` for all-chat, ``"team"`` for team chat, or the raw
            ``DOTAChatChannelType_t`` number as a string for any other channel
            (for example ``"13"`` for spectator chat).
        text: Message text.
    """

    tick: int
    player_slot: int
    channel: str
    text: str


@dataclass
class NeutralItemFoundEvent:
    """A neutral item found event emitted by DOTA_UM_FoundNeutralItem.

    Attributes:
        tick: Game tick when the event was observed.
        player_id: Player slot that found the neutral item.
        item_ability_id: Numeric item ability ID for the neutral item.
        item_key: Internal item key resolved from ``item_ability_id``.
        item_tier: Neutral tier reported by the replay message.
        tier_item_count: Number of found items in this tier reported by the message.
        enhancement_ability_id: Numeric item ability ID for the neutral enhancement.
        enhancement_key: Internal item key resolved from ``enhancement_ability_id``.
        enhancement_level: Enhancement level reported by the replay message.
        trinket_level: Trinket level reported by the replay message.
    """

    tick: int
    player_id: int
    item_ability_id: int
    item_key: str = ""
    item_tier: int = 0
    tier_item_count: int = 0
    enhancement_ability_id: int = -1
    enhancement_key: str = ""
    enhancement_level: int = 0
    trinket_level: int = 0


# ---------------------------------------------------------------------------
# Per-player aggregated output
# ---------------------------------------------------------------------------


@dataclass
class ParsedPlayer:
    """Aggregated statistics for one player over a full match.

    Attributes:
        player_id: Player slot (0–9; 0–4 Radiant, 5–9 Dire).
        hero_name: NPC hero name, e.g. ``"npc_dota_hero_axe"``.
        player_name: Steam persona name (nickname), e.g. ``"Ame"``.
        steam_id: 64-bit Steam ID (e.g. ``76561197986172872``), or 0 if unavailable.
        account_id: 32-bit Steam account ID (e.g. ``25907144``), or 0 if unavailable.
            Derived as ``steam_id - 76561197960265728``.
        team: Team number (2=Radiant, 3=Dire).
        times: Sample tick values (parallel to gold_t / lh_t / …).
            Default sampling is every 30 ticks (1 game-second).
        gold_t: Current unspent gold at each sample tick (team data
            ``m_iReliableGold + m_iUnreliableGold``). Cash on hand: it drops
            on every purchase, so use ``total_earned_gold_t`` for curves.
        total_earned_gold_t: Cumulative total earned gold at each sample tick
            (``m_iTotalEarnedGold``).
        net_worth_t: Net worth (gold + item value) at each sample tick.
        lh_t: Last-hit count at each sample tick.
        dn_t: Deny count at each sample tick.
        xp_t: Current progress toward the next hero level at each sample tick
            (``m_iCurrentXP``); this resets on level-up.
        total_earned_xp_t: Cumulative total earned XP at each sample tick
            (``m_iTotalEarnedXP``).
        times_min: Tick values at each game-minute boundary (OpenDota-aligned).
        game_times_min: Game-relative seconds parallel to ``times_min`` and all
            ``*_t_min`` arrays. Values are exact non-negative minute boundaries
            (``0, 60, 120, ...``) and are the authoritative join key.
        gold_t_min: Cumulative earned gold at each game-minute boundary,
            matching OpenDota's ``gold_t`` (which is earned gold, not cash on
            hand). Read from interval data when complete, otherwise from the
            per-minute ``m_iTotalEarnedGold`` samples.
        total_earned_gold_t_min: Cumulative total earned gold at each game-minute boundary
            (``m_iTotalEarnedGold``). Used for ``radiant_gold_adv`` computation.
        total_earned_xp_t_min: Cumulative total earned XP at each game-minute boundary
            (``m_iTotalEarnedXP``). Used for ``radiant_xp_adv`` computation.
        net_worth_t_min: Net worth at each game-minute boundary.
        lh_t_min: Last-hit count at each game-minute boundary.
        dn_t_min: Deny count at each game-minute boundary.
        xp_t_min: Cumulative XP at each game-minute boundary.
        total_hero_damage_t_min: Cumulative hero-vs-hero damage dealt at each game-minute boundary.
        total_hero_healing_t_min: Cumulative healing dealt to allied heroes at each game-minute boundary.
        total_deaths_t_min: Cumulative death count at each game-minute boundary.
        total_stuns_t_min: Cumulative stun duration dealt (seconds) at each game-minute boundary.
        obs_log: Observer ward placement events for this player (gem's native
            ``WardEvent`` records, carrying coordinates, expiry, and killer).
        sen_log: Sentry ward placement events for this player (``WardEvent``).
        obs_left_log: OpenDota-shaped observer-ward *departure* events
            (``{time, type, key, slot, player_slot, x, y, entityleft,
            attackername}``), one per observer ward that left the map.
            ``attackername`` names the killer for a destroyed ward and is empty
            for a natural expiry. Coordinates are in OpenDota cell units. Mirrors
            OpenDota's ``obs_left_log`` shape; gem's detection is more complete
            (it also logs natural expiries OpenDota sometimes omits).
        sen_left_log: OpenDota-shaped sentry-ward departure events, as
            ``obs_left_log`` but for sentries; mirrors OpenDota's ``sen_left_log``.
        obs: Observer-ward placement coordinate histogram, nested
            ``{x: {y: count}}`` over rounded world coordinates. Mirrors
            OpenDota's ``obs``.
        sen: Sentry-ward placement coordinate histogram, mirroring OpenDota's
            ``sen``.
        damage: Total damage dealt, keyed by target NPC name, credited to the
            damage *source* (``damage_source_name``) so summon / spell /
            projectile damage lands on the owning hero. Illusion targets are keyed
            ``illusion_<npc>`` (OpenDota's ``computeIllusionString``); damage logged
            against an ability/modifier name rather than a real unit is excluded.
            Mirrors OpenDota's per-target ``damage`` reconstruction; the small
            residual is its engine-internal illusion split, not reproducible
            offline (see issue #68).
        damage_taken: Total damage received (non-illusion hero targets only),
            keyed by the damage source NPC name (``damage_source_name``),
            mirroring OpenDota's ``damage_taken`` dict.
        damage_by_type: Total damage dealt, keyed by damage type label
            (``"physical"``, ``"magical"``, ``"pure"``).
        damage_taken_by_type: Total damage received, keyed by damage type label
            (``"physical"``, ``"magical"``, ``"pure"``).
        damage_inflictor: Damage dealt to enemy heroes keyed by the inflictor
            (ability / item, ``item_`` prefix stripped; auto-attacks excluded),
            mirroring OpenDota's ``damage_inflictor``. Self-inflicted damage is
            excluded.
        damage_inflictor_received: Damage received from enemy heroes keyed by the
            enemy's inflictor name, mirroring OpenDota's
            ``damage_inflictor_received``.
        damage_targets: Nested ``inflictor -> {target_hero: damage}`` breakdown of
            damage dealt to enemy heroes, mirroring OpenDota's ``damage_targets``.
        ability_targets: Nested ``ability -> {target_hero: count}`` breakdown of
            ability casts that hit enemy heroes, mirroring OpenDota's
            ``ability_targets``.
        hero_hits: Count of damage instances landed on enemy heroes keyed by
            inflictor, mirroring OpenDota's ``hero_hits``.
        max_hero_hit: The single largest hit landed on an enemy hero as
            ``{time, type, unit, key, inflictor, value, max}``, or ``None`` if the
            player dealt no hero damage; mirrors OpenDota's ``max_hero_hit``.
        healing: Total healing dealt, credited to the heal *source*, keyed by
            target NPC name (illusion targets keyed ``illusion_<npc>``).
        ability_uses: Ability usage counts, keyed by ability name.
        ability_upgrades_arr: Ability upgrade IDs in learned order, matching
            OpenDota's ``ability_upgrades_arr``.
        item_uses: Item usage counts, keyed by item name.
        final_items: End-of-game inventory by slot index, keyed item name with
            the ``item_`` prefix (e.g. ``{0: "item_power_treads"}``). Slots 0-5
            are the main inventory, 6-8 the backpack, 9-16 the stash. Occupied
            slots only; empty slots are absent. Read from the hero entity at the
            game-end tick. Mirrors OpenDota's ``item_0``–``item_5`` /
            ``backpack_0``–``backpack_2`` / ``item_neutral`` (which use numeric
            item IDs rather than names).
        gold_reasons: Gold received per reason code.
        xp_reasons: XP received per reason code.
        kills_log: Combat log DEATH entries where this player was the attacker.
        purchase_log: Chronological PURCHASE combat log entries for this player,
            excluding recipes (matching OpenDota's ``purchase_log``; recipes are
            still counted in the ``purchase`` map).
        runes_log: PICKUP_RUNE entries for this player's rune pickups, from the
            replay's chat events. ``rune_type`` holds the rune; ``value`` is the
            player slot.
        buyback_log: BUYBACK combat log entries for this player.
        buybacks: Structured :class:`BuybackEvent` records, one per ``buyback_log``
            entry, with each buyback's gold cost: exact from the team data's
            gold-spent-on-buybacks counter when observed, else the formula
            estimate ``200 + net_worth // 13``.
        lane_pos: Dwell-tick counts keyed by ``"x_y"`` grid cell (64-unit resolution).
        position_log: Time-ordered ``(tick, x, y)`` tuples sampled at the
            extractor's interval. Useful for movement time-series and
            animated visualisations.
        stuns_dealt: Total stun duration dealt (seconds) accumulated from combat log.
        kills: Kill count from server scoreboard (``m_iKills``). Correctly accounts
            for reincarnation, summon kills, and all edge cases.
        deaths: Death count from server scoreboard (``m_iDeaths``).
        assists: Assist count from server scoreboard (``m_iAssists``).
        lane_role: Lane role inferred from the first-10-minute position heatmap.
            1=safe lane, 2=mid, 3=off lane, 4=jungle, 5=roaming, 0=unknown.
        lane_last_hits: Last-hit count at the 10-minute mark (``lh_t_min[10]``).
        lane_denies: Deny count at the 10-minute mark (``dn_t_min[10]``).
        lane_total_gold: Cumulative total earned gold at the 10-minute mark
            (``total_earned_gold_t_min[10]``).
        lane_total_xp: Cumulative total earned XP at the 10-minute mark
            (``total_earned_xp_t_min[10]``).
        lane_efficiency_pct: Tier-1 laning metric (OpenDota formula).
            ``floor(lane_total_gold / 4948 * 100)``. The denominator 4948 is the
            theoretical gold available from lane creeps + passive income + starting
            gold over 10 minutes. Values above 100 are normal for heroes with kills.
        lane_gold_adv: Tier-2 laning metric. Gold advantage at 10 minutes versus
            lane opponents on the opposing team (``lane_total_gold`` minus the sum
            of opponents' ``lane_total_gold``). Positive = ahead. ``None`` when no
            opponent with a matching lane role exists.
        lane_xp_adv: Tier-2 laning metric. XP advantage at 10 minutes versus
            lane opponents on the opposing team. Same pairing logic as
            ``lane_gold_adv``.
        net_worth: End-of-game net worth (gold + item value). From the
            replay-embedded ``CMsgDOTAMatch`` postgame summary when present,
            matching OpenDota's ``net_worth``; otherwise the last dense sample
            (``net_worth_t[-1]``). ``0`` if neither is available.
        last_hits: End-of-game last-hit count, the last dense sample
            (``lh_t[-1]``). Matches OpenDota's terminal ``last_hits`` scalar.
        denies: End-of-game deny count, the last dense sample (``dn_t[-1]``).
            Matches OpenDota's terminal ``denies`` scalar.
        camps_stacked: Neutral camps stacked over the match (``m_iCampsStacked``).
            Matches OpenDota's ``camps_stacked``.
        creeps_stacked: Neutral creeps stacked over the match
            (``m_iCreepsStacked``). Matches OpenDota's ``creeps_stacked``.
        obs_placed: Observer wards placed (``m_iObserverWardsPlaced``). Matches
            OpenDota's ``obs_placed``.
        sen_placed: Sentry wards placed (``m_iSentryWardsPlaced``). Matches
            OpenDota's ``sen_placed``.
        rune_pickups: Runes picked up (``m_iRunePickups``). Matches OpenDota's
            ``rune_pickups``.
        tower_kills: Towers this player last-hit (``m_iTowerKills``). Matches
            OpenDota's per-player ``tower_kills``.
        killed: Kills per target unit name, derived from ``kills_log`` (summon
            kills credited to the owner). Mirrors OpenDota's ``killed`` map.
        ancient_kills: Ancient-neutral creeps killed (from ``killed``).
        neutral_kills: All neutral creeps killed, including ancients.
        lane_kills: Lane creeps killed (whole game, not just the laning phase).
        courier_kills: Couriers killed.
        observer_kills: Observer wards killed.
        sentry_kills: Sentry wards killed.
        roshan_kills: Roshans last-hit by this player. Derived from ``kills_log``
            (combat-log attributed), matching OpenDota's ``roshan_kills`` rather
            than the unreliable ``m_iRoshanKills`` entity counter.
        hero_id: Numeric Dota 2 hero ID (e.g. 61 = Broodmother), mirroring
            OpenDota's ``hero_id``. ``0`` if unresolved.
        level: Terminal hero level, the last dense snapshot's level. Mirrors
            OpenDota's ``level``.
        gold_spent: Total gold spent on items and consumables over the game,
            from the replay-embedded ``CMsgDOTAMatch`` postgame summary; matches
            OpenDota's ``gold_spent``. Without the summary, the game-end gold
            ledger's ``spent_on_items + spent_on_consumables`` (the same value);
            ``0`` when neither is available. Earned minus current gold is not
            gold spent.
        life_state_dead: Seconds spent dead, sampled from the hero's life state.
            Mirrors OpenDota's ``life_state_dead``.
        firstblood_claimed: ``1`` if this player dealt the game's first-blood kill,
            else ``0``. Mirrors OpenDota's ``firstblood_claimed``.
        teamfight_participation: Fraction of OpenDota-compatible teamfights
            (``opendota_teamfights``) the player was involved in (0.0–1.0) — any
            death, buyback, damage, healing, or ability/item use in the window.
            Mirrors OpenDota's ``teamfight_participation``.
        purchase: Count of each item purchased, keyed by translated item name
            (``item_`` stripped); recipes included. Mirrors OpenDota's
            ``purchase``.
        purchase_time: Game-seconds of the player's *last* purchase of each item
            (recipes excluded), keyed by translated name. Mirrors OpenDota's
            ``purchase_time``.
        first_purchase_time: Game-seconds of the player's *first* purchase of each
            item (recipes excluded). Mirrors OpenDota's ``first_purchase_time``.
        purchase_tpscroll: Number of TP scrolls purchased. Mirrors OpenDota's
            ``purchase_tpscroll``.
        purchase_ward_observer: Number of observer wards purchased. Mirrors
            OpenDota's ``purchase_ward_observer``.
        purchase_ward_sentry: Number of sentry wards purchased. Mirrors OpenDota's
            ``purchase_ward_sentry``.
        observer_uses: Observer wards used (``item_uses['item_ward_observer']``).
            Mirrors OpenDota's ``observer_uses``.
        sentry_uses: Sentry wards used (``item_uses['item_ward_sentry']``).
            Mirrors OpenDota's ``sentry_uses``.
        observers_placed: Observer wards placed, derived from ``obs_log`` length.
            Mirrors OpenDota's ``observers_placed`` (a purchase/use-log-derived
            alias distinct from the entity-counter ``obs_placed``).
        kda: OpenDota KDA ratio, ``round((kills + assists) / (deaths + 1), 2)``.
            Note the ``+1`` denominator (not ``max(deaths, 1)``) and 2-decimal
            rounding; matches OpenDota's ``kda`` exactly.
        buyback_count: Number of buybacks used (``len(buyback_log)``). Matches
            OpenDota's ``buyback_count``.
        is_radiant: True if the player is on Radiant (team 2). Matches OpenDota's
            ``isRadiant``.
        win: ``1`` if this player's team won, else ``0`` (also ``0`` when the
            match winner is unknown). Matches OpenDota's ``win``.
        kills_per_min: Kills divided by match duration in minutes
            (``kills / (ParsedMatch.duration / 60)``). Unrounded float matching
            OpenDota's ``kills_per_min``. ``0.0`` when duration is unknown.
        hero_damage: Damage dealt to enemy heroes. Complete replays source the
            exact Game Coordinator value from the embedded ``CMsgDOTAMatch``
            postgame summary. Older or truncated replays fall back to combat-log
            reconstruction; :func:`gem.replays.fetch.apply_api_rates` can still
            overwrite it from an explicit API response.
        tower_damage: Damage dealt to building structures (towers, barracks,
            fort/ancient). Uses the embedded postgame summary when present and
            combat-log reconstruction otherwise; ``apply_api_rates`` can
            explicitly overwrite it.
        hero_healing: Healing given to allied heroes (excluding self-heal),
            using the embedded postgame summary when present and combat-log
            reconstruction otherwise. Can be overwritten via ``apply_api_rates``.
        gold_per_min: Game Coordinator gold per minute from the replay-embedded
            postgame summary. ``0`` when that summary/field is absent; optional
            API enrichment can overwrite it.
        xp_per_min: Game Coordinator XP per minute, with the same embedded-summary
            and optional API provenance as ``gold_per_min``.
        total_gold: Total gold, ``floor(gold_per_min * duration / 60)`` (OpenDota's
            own formula). ``0`` when ``gold_per_min`` is unavailable.
        total_xp: Total XP, ``floor(xp_per_min * duration / 60)``. ``0`` until
            ``xp_per_min`` is available.
        aghanims_scepter: OpenDota-compatible consumed Aghanim's Scepter flag.
            ``1`` when permanent buff ID 2 is present, ``0`` when its absence is
            confirmed, and ``None`` when no postgame summary or API value is
            available.
        aghanims_shard: OpenDota-compatible Aghanim's Shard flag using permanent
            buff ID 12, with the same ``1`` / ``0`` / ``None`` availability
            semantics as ``aghanims_scepter``.
        moonshard: OpenDota-compatible consumed Moon Shard flag using permanent
            buff ID 1, with the same ``1`` / ``0`` / ``None`` semantics.
        gold: End-of-game unspent gold (reliable + unreliable). From the
            replay-embedded postgame summary when present, matching OpenDota's
            ``gold``; otherwise the last dense sample (``gold_t[-1]``).
        gold_ledger: The player's :class:`GoldLedger`: gold earned by source,
            spent by category, and lost to death, at game end and per minute.
            ``None`` when the replay's team data has no complete ledger.
    """

    player_id: int
    hero_name: str = ""
    player_name: str = ""
    steam_id: int = 0
    account_id: int = 0
    team: int = 0
    times: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    total_earned_gold_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    times_min: list[int] = field(default_factory=list)
    gold_t_min: list[int] = field(default_factory=list)
    total_earned_gold_t_min: list[int] = field(default_factory=list)
    total_earned_xp_t_min: list[int] = field(default_factory=list)
    net_worth_t_min: list[int] = field(default_factory=list)
    lh_t_min: list[int] = field(default_factory=list)
    dn_t_min: list[int] = field(default_factory=list)
    xp_t_min: list[int] = field(default_factory=list)
    total_hero_damage_t_min: list[int] = field(default_factory=list)
    total_hero_healing_t_min: list[int] = field(default_factory=list)
    total_deaths_t_min: list[int] = field(default_factory=list)
    total_stuns_t_min: list[float] = field(default_factory=list)
    obs_log: list[WardEvent] = field(default_factory=list)
    sen_log: list[WardEvent] = field(default_factory=list)
    obs_left_log: list[dict[str, Any]] = field(default_factory=list)
    sen_left_log: list[dict[str, Any]] = field(default_factory=list)
    obs: dict[str, dict[str, int]] = field(default_factory=dict)
    sen: dict[str, dict[str, int]] = field(default_factory=dict)
    damage: dict[str, int] = field(default_factory=dict)
    damage_taken: dict[str, int] = field(default_factory=dict)
    damage_by_type: dict[str, int] = field(default_factory=dict)
    damage_taken_by_type: dict[str, int] = field(default_factory=dict)
    damage_inflictor: dict[str, int] = field(default_factory=dict)
    damage_inflictor_received: dict[str, int] = field(default_factory=dict)
    damage_targets: dict[str, dict[str, int]] = field(default_factory=dict)
    ability_targets: dict[str, dict[str, int]] = field(default_factory=dict)
    hero_hits: dict[str, int] = field(default_factory=dict)
    max_hero_hit: dict[str, Any] | None = None
    healing: dict[str, int] = field(default_factory=dict)
    ability_uses: dict[str, int] = field(default_factory=dict)
    ability_upgrades_arr: list[int] = field(default_factory=list)
    item_uses: dict[str, int] = field(default_factory=dict)
    final_items: dict[int, str] = field(default_factory=dict)
    gold_reasons: dict[str, int] = field(default_factory=dict)
    xp_reasons: dict[str, int] = field(default_factory=dict)
    kills_log: list[CombatLogEntry] = field(default_factory=list)
    purchase_log: list[CombatLogEntry] = field(default_factory=list)
    runes_log: list[CombatLogEntry] = field(default_factory=list)
    buyback_log: list[CombatLogEntry] = field(default_factory=list)
    buybacks: list[BuybackEvent] = field(default_factory=list)
    lane_pos: defaultdict[str, int] = field(default_factory=lambda: defaultdict(int))
    position_log: list[tuple[int, float, float]] = field(default_factory=list)
    stuns_dealt: float = 0.0
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    lane_role: int = 0
    lane_last_hits: int = 0
    lane_denies: int = 0
    lane_total_gold: int = 0
    lane_total_xp: int = 0
    lane_efficiency_pct: int = 0
    lane_gold_adv: int | None = None
    lane_xp_adv: int | None = None
    net_worth: int = 0
    last_hits: int = 0
    denies: int = 0
    camps_stacked: int = 0
    creeps_stacked: int = 0
    obs_placed: int = 0
    sen_placed: int = 0
    rune_pickups: int = 0
    tower_kills: int = 0
    kda: float = 0.0
    buyback_count: int = 0
    is_radiant: bool = False
    win: int = 0
    kills_per_min: float = 0.0
    hero_damage: int = 0
    tower_damage: int = 0
    hero_healing: int = 0
    gold_per_min: int = 0
    xp_per_min: int = 0
    total_gold: int = 0
    total_xp: int = 0
    # Derived kill aggregates (reshaped from kills_log; summon kills credited).
    killed: dict[str, int] = field(default_factory=dict)
    ancient_kills: int = 0
    neutral_kills: int = 0
    lane_kills: int = 0
    courier_kills: int = 0
    observer_kills: int = 0
    sentry_kills: int = 0
    roshan_kills: int = 0
    # OpenDota-parity terminal / derived scalars.
    hero_id: int = 0
    level: int = 0
    gold_spent: int = 0
    life_state_dead: int = 0
    firstblood_claimed: int = 0
    teamfight_participation: float = 0.0
    # OpenDota purchase-timeline aggregates, derived from purchase_log.
    purchase: dict[str, int] = field(default_factory=dict)
    purchase_time: dict[str, int] = field(default_factory=dict)
    first_purchase_time: dict[str, int] = field(default_factory=dict)
    purchase_tpscroll: int = 0
    purchase_ward_observer: int = 0
    purchase_ward_sentry: int = 0
    observer_uses: int = 0
    sentry_uses: int = 0
    observers_placed: int = 0
    _ability_snapshots: list[tuple[int, dict[str, int]]] = field(default_factory=list)
    # Append-only: ParsedPlayer is a public dataclass and supports positional
    # construction, so new fields go last to avoid shifting existing callers.
    game_times_min: list[int] = field(default_factory=list)
    aghanims_scepter: int | None = None
    aghanims_shard: int | None = None
    moonshard: int | None = None
    total_earned_xp_t: list[int] = field(default_factory=list)
    gold: int = 0
    gold_ledger: GoldLedger | None = None
    # Internal provenance for values copied from CMsgDOTAMatch. The serializer
    # omits this implementation detail from the public ParsedPlayer shape.
    _match_details_fields: set[str] = field(
        default_factory=set,
        init=False,
        repr=False,
        compare=False,
        metadata={"serialize": False},
    )

    def __repr__(self) -> str:
        hero = self.hero_name.removeprefix("npc_dota_hero_") if self.hero_name else "unknown"
        team = "Radiant" if self.team == 2 else "Dire" if self.team == 3 else f"team={self.team}"
        return (
            f"ParsedPlayer(slot={self.player_id}, hero={hero}, team={team}, "
            f"kda={self.kills}/{self.deaths}/{self.assists}, net_worth={self.net_worth})"
        )


# ---------------------------------------------------------------------------
# Match-level aggregated output
# ---------------------------------------------------------------------------


@dataclass
class ParsedMatch:
    """Top-level parsed output for a single Dota 2 replay.

    Attributes:
        match_id: Dota 2 match ID, or 0 if unavailable.
        game_mode: Game mode integer (e.g. 22 = All Pick Ranked).
        leagueid: League ID, or 0 for non-league matches.
        radiant_win: True if Radiant won, False if Dire won, None if unknown.
        radiant_team_id: Radiant tournament team ID (e.g. ``8261500``), or 0 for pub games.
            Matches the OpenDota ``/teams/{id}`` URL.
        radiant_team_name: Radiant team name (e.g. ``"Xtreme Gaming"``), or empty string.
        radiant_team_tag: Radiant team tag (e.g. ``"XG"``), or empty string.
        dire_team_id: Dire tournament team ID, or 0 for pub games.
        dire_team_name: Dire team name (e.g. ``"Team Falcons"``), or empty string.
        dire_team_tag: Dire team tag (e.g. ``"FLCN"``), or empty string.
        players: One ``ParsedPlayer`` per player slot (index 0–9).
        towers: All tower kill events in chronological order.
        barracks: All barracks kill events in chronological order.
        roshans: All Roshan kill events in chronological order.
        aegis_events: All Aegis pickup / steal / denial events.
        tormentors: All Tormentor (miniboss) kill events in chronological order.
        shrines: All Shrine of Wisdom destruction events in chronological order.
        courier_deaths: All courier deaths (combat-log DEATH on a courier).
        banner_plants: All Roshan's Banner plant events (tick, team, planter,
            and world position), recovered from the planted banner unit's
            creation in the entity stream.
        objectives: OpenDota-shaped unified objective timeline, merging building
            kills and the ``CHAT_MESSAGE_*`` events (Roshan, Aegis, Tormentor,
            first blood, courier lost) into one chronological list of
            ``{time, type, ...}`` dicts. Mirrors OpenDota's ``objectives``; gem's
            typed per-type fields (``towers``, ``roshans``, etc.) are retained
            alongside it.
        tower_status_radiant: End-of-game Radiant tower-status bitmask (Steam GC
            11-bit convention; bit set = tower standing). Reconstructed from tower
            kills. Mirrors OpenDota's ``tower_status_radiant``.
        tower_status_dire: End-of-game Dire tower-status bitmask. Mirrors
            OpenDota's ``tower_status_dire``.
        barracks_status_radiant: End-of-game Radiant barracks-status bitmask
            (6-bit; bit set = barracks standing). Mirrors OpenDota's
            ``barracks_status_radiant``.
        barracks_status_dire: End-of-game Dire barracks-status bitmask. Mirrors
            OpenDota's ``barracks_status_dire``.
        wards: All ward placement events with coordinates.
        radiant_gold_adv: Radiant gold advantage at each minute boundary.
        radiant_xp_adv: Radiant XP advantage at each minute boundary.
        game_times_min: Game-relative seconds parallel to
            ``radiant_gold_adv`` / ``radiant_xp_adv``. Values are exact
            non-negative minute boundaries and are the authoritative join key.
        combat_log: All raw combat log entries (unfiltered).
        chat: All chat messages in chronological order.
        courier_snapshots: Courier state snapshots at each sample interval.
        neutral_item_finds: Neutral item find events from ``DOTA_UM_FoundNeutralItem``.
        smoke_events: All Smoke of Deceit activations with grouped heroes and
            approximate activating-hero position.
        draft: Hero pick and ban events from the draft phase.
        teamfights: All detected teamfight windows with per-player breakdowns.
        opendota_teamfights: OpenDota-compatible temporal teamfight windows.
            These use OpenDota's 15-second death-window grouping and 3+ death
            filter, while ``teamfights`` keeps Gem's richer spatial detector.
        vision_modifiers: Vision-granting modifier events (Slardar Corrosive Haze,
            Bounty Hunter Track, Dust of Appearance, Gem of True Sight, etc.).
            Target-specific reveal evidence is exposed by
            ``assess_point_vision(..., target_player_id=...)``; modifiers are
            not arbitrary-point geometry sources.
        game_start_tick: Absolute tick when the game clock started (creeps spawn).
            ``None`` if the transition was not observed.
        game_end_tick: Absolute tick of the final parser tick. Replays can keep
            recording long after the Ancient falls, so this is the end of the
            recording, not the end of the match; see ``post_game_tick``.
        post_game_tick: Absolute tick at which the match entered post-game
            (GAME_STATE==6, the Ancient destroyed). ``None`` if not observed.
        game_clock: Pause-aware conversion between replay ticks and the in-game
            clock (see :class:`gem.GameClock`). ``None`` for matches assembled
            without parser clock state.
        parse_error: Why the parse ended early, when the replay data was
            truncated or corrupt (e.g. ``"TruncatedReplayError(...)"``). ``None``
            for a complete parse. Everything read before that point is kept.
        truncated_at_tick: The last tick read when the parse ended early, or
            ``None`` for a complete parse.
        duration: OpenDota-style match duration in seconds. Complete replays use
            the exact value from the embedded ``CMsgDOTAMatch`` postgame summary;
            otherwise this falls back to horn-anchored combat-log time at
            GAME_STATE==6 (ancient destroyed). ``0`` if neither is available.
            Distinct from the tick-derived ``duration_seconds`` property, which
            spans the raw parser ticks and includes pre/post-game time.
        radiant_score: Radiant's final kill score. From the replay-embedded
            ``CMsgDOTAMatch`` postgame summary when present, matching OpenDota's
            ``radiant_score``; otherwise the sum of Radiant players' kills.
        dire_score: Dire's final kill score, from the postgame summary when
            present (OpenDota's ``dire_score``); otherwise the sum of Dire
            players' kills.
        first_blood_time: Game-relative time in seconds of first blood. From the
            postgame summary when present, matching OpenDota's
            ``first_blood_time``; otherwise the combat-log time of the first real
            hero death. ``0`` if neither is available.
        pre_game_duration: The pre-game length in seconds, OpenDota's
            ``pre_game_duration`` (90 in current matches). Only the postgame
            summary carries it; ``0`` when that is absent.
    """

    match_id: int = 0
    game_mode: int = 0
    leagueid: int = 0
    radiant_win: bool | None = None
    radiant_team_id: int = 0
    radiant_team_name: str = ""
    radiant_team_tag: str = ""
    dire_team_id: int = 0
    dire_team_name: str = ""
    dire_team_tag: str = ""
    game_start_tick: int | None = None
    game_end_tick: int = 0
    duration: int = 0
    radiant_score: int = 0
    dire_score: int = 0
    first_blood_time: int = 0
    pre_game_duration: int = 0
    players: list[ParsedPlayer] = field(
        default_factory=lambda: [ParsedPlayer(player_id=i) for i in range(10)]
    )
    towers: list[TowerKill] = field(default_factory=list)
    barracks: list[BarracksKill] = field(default_factory=list)
    roshans: list[RoshanKill] = field(default_factory=list)
    aegis_events: list[AegisEvent] = field(default_factory=list)
    tormentors: list[TormentorKill] = field(default_factory=list)
    shrines: list[ShrineKill] = field(default_factory=list)
    courier_deaths: list[CourierDeath] = field(default_factory=list)
    objectives: list[dict[str, Any]] = field(default_factory=list)
    tower_status_radiant: int = 0
    tower_status_dire: int = 0
    barracks_status_radiant: int = 0
    barracks_status_dire: int = 0
    wards: list[WardEvent] = field(default_factory=list)
    radiant_gold_adv: list[int] = field(default_factory=list)
    radiant_xp_adv: list[int] = field(default_factory=list)
    combat_log: list[CombatLogEntry] = field(default_factory=list)
    chat: list[ChatEntry] = field(default_factory=list)
    courier_snapshots: list[CourierSnapshot] = field(default_factory=list)
    neutral_item_finds: list[NeutralItemFoundEvent] = field(default_factory=list)
    smoke_events: list[SmokeEvent] = field(default_factory=list)
    draft: list[DraftEvent] = field(default_factory=list)
    teamfights: list[Teamfight] = field(default_factory=list)
    opendota_teamfights: list[OpenDotaTeamfight] = field(default_factory=list)
    vision_modifiers: list[VisionModifierEvent] = field(default_factory=list)
    # Append-only: ParsedMatch is a public dataclass and supports positional
    # construction, so new fields go LAST to avoid shifting existing positional
    # arguments. (Logically these fields belong beside related timelines, but
    # inserting them there would silently misalign positional callers.)
    banner_plants: list[BannerPlant] = field(default_factory=list)
    game_times_min: list[int] = field(default_factory=list)
    hero_visibility_events: list[HeroVisibilityEvent] = field(default_factory=list)
    vision_modifier_pairing_issues: list[VisionModifierPairingIssue] = field(default_factory=list)
    entity_visibility_events: list[EntityVisibilityEvent] = field(default_factory=list)
    post_game_tick: int | None = None
    game_clock: GameClock | None = None
    parse_error: str | None = None
    truncated_at_tick: int | None = None
    # Internal provenance for match-level values copied from CMsgDOTAMatch.
    _match_details_fields: set[str] = field(
        default_factory=set,
        init=False,
        repr=False,
        compare=False,
        metadata={"serialize": False},
    )

    @property
    def duration_seconds(self) -> float:
        """Game duration in seconds, derived from ``game_start_tick`` and ``game_end_tick``."""
        start = self.game_start_tick or 0
        return max(self.game_end_tick - start, 0) / 30.0

    @property
    def duration_minutes(self) -> float:
        """Game duration in minutes, derived from ``game_start_tick`` and ``game_end_tick``."""
        return self.duration_seconds / 60.0

    def __repr__(self) -> str:
        winner = "Radiant" if self.radiant_win else "Dire" if self.radiant_win is False else "?"
        duration_min = (
            round(max(pp.times[-1] for pp in self.players if pp.times) / 30 / 60)
            if any(pp.times for pp in self.players)
            else 0
        )
        return (
            f"ParsedMatch(match_id={self.match_id}, winner={winner}, "
            f"duration=~{duration_min}min, players={len(self.players)})"
        )
