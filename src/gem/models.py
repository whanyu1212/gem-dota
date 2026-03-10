"""Output data models for gem replay parsing.

Defines ``ParsedPlayer`` and ``ParsedMatch`` dataclasses that aggregate all
extracted information into a structured, ML-friendly output.

Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java
"""

from __future__ import annotations

from dataclasses import dataclass, field

from gem.combatlog import CombatLogEntry
from gem.extractors.courier import CourierSnapshot
from gem.extractors.draft import DraftEvent
from gem.extractors.objectives import AegisEvent, BarracksKill, RoshanKill, TowerKill
from gem.extractors.teamfights import Teamfight
from gem.extractors.wards import WardEvent


@dataclass
class ChatEntry:
    """A single chat message from the match.

    Attributes:
        tick: Game tick when the message was sent.
        player_slot: Source player slot (0–9).
        channel: ``"all"`` for all-chat, ``"team"`` for team-chat, or raw channel type string.
        text: Message text.
    """

    tick: int
    player_slot: int
    channel: str
    text: str


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
        team: Team number (2=Radiant, 3=Dire).
        times: Sample tick values (parallel to gold_t / lh_t / …).
        gold_t: Gold at each sample tick.
        lh_t: Last-hit count at each sample tick.
        dn_t: Deny count at each sample tick.
        xp_t: Cumulative XP at each sample tick.
        obs_log: Observer ward placement events for this player.
        sen_log: Sentry ward placement events for this player.
        damage: Total damage dealt, keyed by target NPC name.
        damage_taken: Total damage received, keyed by attacker NPC name.
        healing: Total healing dealt, keyed by target NPC name.
        ability_uses: Ability usage counts, keyed by ability name.
        item_uses: Item usage counts, keyed by item name.
        gold_reasons: Gold received per reason code.
        xp_reasons: XP received per reason code.
        kills_log: Combat log DEATH entries where this player was the attacker.
        purchase_log: PURCHASE combat log entries for this player.
        runes_log: ITEM combat log entries for rune pickups.
        buyback_log: BUYBACK combat log entries for this player.
        lane_pos: Dwell-tick counts keyed by ``"x_y"`` grid cell (64-unit resolution).
        position_log: Time-ordered ``(tick, x, y)`` tuples sampled at the
            extractor's interval. Useful for movement time-series and
            animated visualisations.
        stuns_dealt: Total stun duration dealt (seconds) accumulated from combat log.
    """

    player_id: int
    hero_name: str = ""
    player_name: str = ""
    team: int = 0
    times: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    obs_log: list[WardEvent] = field(default_factory=list)
    sen_log: list[WardEvent] = field(default_factory=list)
    damage: dict[str, int] = field(default_factory=dict)
    damage_taken: dict[str, int] = field(default_factory=dict)
    healing: dict[str, int] = field(default_factory=dict)
    ability_uses: dict[str, int] = field(default_factory=dict)
    item_uses: dict[str, int] = field(default_factory=dict)
    gold_reasons: dict[str, int] = field(default_factory=dict)
    xp_reasons: dict[str, int] = field(default_factory=dict)
    kills_log: list[CombatLogEntry] = field(default_factory=list)
    purchase_log: list[CombatLogEntry] = field(default_factory=list)
    runes_log: list[CombatLogEntry] = field(default_factory=list)
    buyback_log: list[CombatLogEntry] = field(default_factory=list)
    lane_pos: dict[str, int] = field(default_factory=dict)
    position_log: list[tuple[int, float, float]] = field(default_factory=list)
    stuns_dealt: float = 0.0


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
        players: One ``ParsedPlayer`` per player slot (index 0–9).
        towers: All tower kill events in chronological order.
        barracks: All barracks kill events in chronological order.
        roshans: All Roshan kill events in chronological order.
        aegis_events: All Aegis pickup / steal / denial events.
        wards: All ward placement events with coordinates.
        radiant_gold_adv: Radiant gold advantage at each minute boundary.
        radiant_xp_adv: Radiant XP advantage at each minute boundary.
        combat_log: All raw combat log entries (unfiltered).
        chat: All chat messages in chronological order.
        courier_snapshots: Courier state snapshots at each sample interval.
        draft: Hero pick and ban events from the draft phase.
        teamfights: All detected teamfight windows with per-player breakdowns.
    """

    match_id: int = 0
    game_mode: int = 0
    leagueid: int = 0
    players: list[ParsedPlayer] = field(
        default_factory=lambda: [ParsedPlayer(player_id=i) for i in range(10)]
    )
    towers: list[TowerKill] = field(default_factory=list)
    barracks: list[BarracksKill] = field(default_factory=list)
    roshans: list[RoshanKill] = field(default_factory=list)
    aegis_events: list[AegisEvent] = field(default_factory=list)
    wards: list[WardEvent] = field(default_factory=list)
    radiant_gold_adv: list[int] = field(default_factory=list)
    radiant_xp_adv: list[int] = field(default_factory=list)
    combat_log: list[CombatLogEntry] = field(default_factory=list)
    chat: list[ChatEntry] = field(default_factory=list)
    courier_snapshots: list[CourierSnapshot] = field(default_factory=list)
    draft: list[DraftEvent] = field(default_factory=list)
    teamfights: list[Teamfight] = field(default_factory=list)
