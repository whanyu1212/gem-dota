"""Output data models for gem replay parsing.

Defines ``ParsedPlayer`` and ``ParsedMatch`` dataclasses that aggregate all
extracted information into a structured, ML-friendly output.

Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java
"""

from __future__ import annotations

from dataclasses import dataclass, field

from gem.combatlog import CombatLogEntry
from gem.extractors.objectives import BarracksKill, RoshanKill, TowerKill
from gem.extractors.wards import WardEvent

# ---------------------------------------------------------------------------
# Per-player aggregated output
# ---------------------------------------------------------------------------


@dataclass
class ParsedPlayer:
    """Aggregated statistics for one player over a full match.

    Attributes:
        player_id: Player slot (0–9; 0–4 Radiant, 5–9 Dire).
        hero_name: NPC hero name, e.g. ``"npc_dota_hero_axe"``.
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
    """

    player_id: int
    hero_name: str = ""
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


# ---------------------------------------------------------------------------
# Match-level aggregated output
# ---------------------------------------------------------------------------


@dataclass
class ParsedMatch:
    """Top-level parsed output for a single Dota 2 replay.

    Attributes:
        match_id: Dota 2 match ID, or 0 if unavailable.
        players: One ``ParsedPlayer`` per player slot (index 0–9).
        towers: All tower kill events in chronological order.
        barracks: All barracks kill events in chronological order.
        roshans: All Roshan kill events in chronological order.
        wards: All ward placement events with coordinates.
        radiant_gold_adv: Radiant gold advantage at each minute boundary.
        radiant_xp_adv: Radiant XP advantage at each minute boundary.
        combat_log: All raw combat log entries (unfiltered).
    """

    match_id: int = 0
    players: list[ParsedPlayer] = field(
        default_factory=lambda: [ParsedPlayer(player_id=i) for i in range(10)]
    )
    towers: list[TowerKill] = field(default_factory=list)
    barracks: list[BarracksKill] = field(default_factory=list)
    roshans: list[RoshanKill] = field(default_factory=list)
    wards: list[WardEvent] = field(default_factory=list)
    radiant_gold_adv: list[int] = field(default_factory=list)
    radiant_xp_adv: list[int] = field(default_factory=list)
    combat_log: list[CombatLogEntry] = field(default_factory=list)
