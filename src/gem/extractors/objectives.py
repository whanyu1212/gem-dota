"""Objective event extractor for Dota 2 replays.

Listens to combat log DEATH events and emits structured records for tower
kills, Roshan kills, and barracks destructions.

Reference: refs/parser/src/main/java/opendota/Parse.java
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from gem.combatlog import CombatLogEntry
from gem.entities import EntityOp

if TYPE_CHECKING:
    from gem.entities import Entity
    from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Team constants
# ---------------------------------------------------------------------------

_TEAM_RADIANT = 2
_TEAM_DIRE = 3

# CDOTAUserMsg_ChatEvent type constants
_CHAT_MSG_AEGIS = 8
_CHAT_MSG_AEGIS_STOLEN = 53
_CHAT_MSG_DENIED_AEGIS = 51
_CHAT_MSG_SHRINE_KILLED = 101
_CHAT_MSG_MINIBOSS_KILL = 117  # Tormentor kill

# Roshan item entity class name → short drop name
_ROSHAN_ITEM_DROPS: dict[str, str] = {
    "CDOTA_Item_Aegis": "aegis",
    "CDOTA_Item_Cheese": "cheese",
    "CDOTA_Item_RefresherOrb_Shard": "refresher_shard",
    "CDOTA_Item_Roshans_Banner": "banner",
}

# Tower NPC name prefix → owning team
_TOWER_TEAM: dict[str, int] = {
    "npc_dota_goodguys_tower": _TEAM_RADIANT,
    "npc_dota_badguys_tower": _TEAM_DIRE,
}

# Barracks NPC name prefix → owning team
_BARRACKS_TEAM: dict[str, int] = {
    "npc_dota_goodguys_melee_rax": _TEAM_RADIANT,
    "npc_dota_goodguys_range_rax": _TEAM_RADIANT,
    "npc_dota_badguys_melee_rax": _TEAM_DIRE,
    "npc_dota_badguys_range_rax": _TEAM_DIRE,
}

# CDOTAUserMsg_ChatEvent type → AegisEvent event_type string
_AEGIS_EVENT_TYPE: dict[int, str] = {
    _CHAT_MSG_AEGIS: "pickup",
    _CHAT_MSG_AEGIS_STOLEN: "stolen",
    _CHAT_MSG_DENIED_AEGIS: "denied",
}


def _find_team(target_name: str, mapping: dict[str, int]) -> int:
    for prefix, team in mapping.items():
        if target_name.startswith(prefix):
            return team
    return 0


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class TowerKill:
    """One tower destruction event.

    Attributes:
        tick: Game tick when the tower was destroyed.
        team: Team that *owned* the tower (2=Radiant, 3=Dire).
        killer: NPC name of the unit that landed the killing blow.
        tower_name: Internal NPC name of the destroyed tower.
    """

    tick: int
    team: int
    killer: str
    tower_name: str


@dataclass
class RoshanKill:
    """One confirmed Roshan death.

    Attributes:
        tick: Game tick of the kill.
        killer: NPC name of the unit that landed the killing blow.
        kill_number: Sequential kill number (1-indexed) for this game.
        drops: Short names of items dropped (e.g. ``["aegis", "cheese",
            "refresher_shard", "banner"]``). Populated from entity state;
            always includes ``"aegis"`` when Roshan is killed.
    """

    tick: int
    killer: str
    kill_number: int
    drops: list[str] = field(default_factory=list)


@dataclass
class BarracksKill:
    """One barracks destruction event.

    Attributes:
        tick: Game tick when the barracks was destroyed.
        team: Team that *owned* the barracks (2=Radiant, 3=Dire).
        killer: NPC name of the unit that landed the killing blow.
        barracks_name: Internal NPC name of the destroyed barracks.
    """

    tick: int
    team: int
    killer: str
    barracks_name: str


@dataclass
class TormentorKill:
    """One Tormentor (miniboss) kill event.

    Attributes:
        tick: Game tick of the kill.
        killer: NPC name of the unit that landed the killing blow,
            or empty string if unknown.
        killer_player_id: Player slot (0–9) of the killing player from the
            ``CHAT_MESSAGE_MINIBOSS_KILL`` event, or ``-1`` if unavailable.
        kill_number: Sequential kill number (1-indexed) for this game.
    """

    tick: int
    killer: str
    killer_player_id: int
    kill_number: int


@dataclass
class ShrineKill:
    """One Shrine of Wisdom destruction event.

    Attributes:
        tick: Game tick of the event.
        team: Team that *owned* the destroyed shrine (2=Radiant, 3=Dire).
    """

    tick: int
    team: int


@dataclass
class AegisEvent:
    """An Aegis of the Immortal pickup, steal, or denial event.

    Attributes:
        tick: Game tick of the event.
        player_id: Player slot (0–9) who picked up / stole / denied the Aegis.
            -1 if the event had no player attribution.
        event_type: ``"pickup"``, ``"stolen"``, or ``"denied"``.
    """

    tick: int
    player_id: int
    event_type: str


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class ObjectivesExtractor:
    """Extracts tower kills, Roshan kills, barracks kills, tormentor kills, and shrine kills from a replay.

    Attach to a ``ReplayParser`` before calling ``parse()``:

    Example:
        >>> extractor = ObjectivesExtractor()
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> print(extractor.roshan_kills)

    Attributes:
        tower_kills: All tower kill events in chronological order.
        roshan_kills: All Roshan kill events in chronological order.
        barracks_kills: All barracks kill events in chronological order.
        aegis_events: All Aegis pickup / steal / denial events.
        tormentor_kills: All Tormentor (miniboss) kill events in chronological order.
        shrine_kills: All Shrine of Wisdom destruction events in chronological order.
    """

    tower_kills: list[TowerKill]
    roshan_kills: list[RoshanKill]
    barracks_kills: list[BarracksKill]
    aegis_events: list[AegisEvent]
    tormentor_kills: list[TormentorKill]
    shrine_kills: list[ShrineKill]

    def __init__(self) -> None:
        self.tower_kills = []
        self.roshan_kills = []
        self.barracks_kills = []
        self.aegis_events = []
        self.tormentor_kills = []
        self.shrine_kills = []
        # index → short drop name for currently-alive Roshan item entities
        self._roshan_items: dict[int, str] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register this extractor's callbacks with a parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        parser.on_combat_log_entry(self._on_combat_log)
        parser.on_chat_event(self._on_chat_event)
        parser.on_entity(self._on_entity)

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        name = entity.get_class_name()
        drop_name = _ROSHAN_ITEM_DROPS.get(name)
        if drop_name is None:
            return
        idx = entity.get_index()
        if op == EntityOp.DELETED_LEFT:
            self._roshan_items.pop(idx, None)
        else:
            self._roshan_items[idx] = drop_name

    def _on_chat_event(self, msg: Any, tick: int) -> None:
        event_type = _AEGIS_EVENT_TYPE.get(msg.type)
        if event_type is not None:
            self.aegis_events.append(
                AegisEvent(tick=tick, player_id=msg.playerid_1, event_type=event_type)
            )
        elif msg.type == _CHAT_MSG_SHRINE_KILLED:
            # value = team that owned the shrine (2=Radiant, 3=Dire)
            self.shrine_kills.append(ShrineKill(tick=tick, team=msg.value or 0))
        elif msg.type == _CHAT_MSG_MINIBOSS_KILL and self.tormentor_kills:
            # playerid_1 = player slot of the killer. Patch the most recently
            # recorded tormentor kill (from the DEATH combat log event) with
            # the player slot attribution from this chat event.
            self.tormentor_kills[-1].killer_player_id = msg.playerid_1

    def _on_combat_log(self, entry: CombatLogEntry) -> None:
        if entry.log_type != "DEATH":
            return
        target = entry.target_name
        if target == "npc_dota_roshan":
            # Snapshot alive Roshan item entities as drops. Items are created
            # when Roshan spawns and deleted when picked up, so the set alive
            # at the kill tick is exactly what Roshan dropped.
            self.roshan_kills.append(
                RoshanKill(
                    tick=entry.tick,
                    killer=entry.attacker_name,
                    kill_number=len(self.roshan_kills) + 1,
                    drops=sorted(self._roshan_items.values()),
                )
            )
        elif target == "npc_dota_miniboss":
            self.tormentor_kills.append(
                TormentorKill(
                    tick=entry.tick,
                    killer=entry.attacker_name,
                    killer_player_id=-1,  # resolved from chat event if available
                    kill_number=len(self.tormentor_kills) + 1,
                )
            )
        elif target.startswith("npc_dota_goodguys_tower") or target.startswith(
            "npc_dota_badguys_tower"
        ):
            self.tower_kills.append(
                TowerKill(
                    tick=entry.tick,
                    team=_find_team(target, _TOWER_TEAM),
                    killer=entry.attacker_name,
                    tower_name=target,
                )
            )
        elif (
            target.startswith("npc_dota_goodguys_melee_rax")
            or target.startswith("npc_dota_goodguys_range_rax")
            or target.startswith("npc_dota_badguys_melee_rax")
            or target.startswith("npc_dota_badguys_range_rax")
        ):
            self.barracks_kills.append(
                BarracksKill(
                    tick=entry.tick,
                    team=_find_team(target, _BARRACKS_TEAM),
                    killer=entry.attacker_name,
                    barracks_name=target,
                )
            )
