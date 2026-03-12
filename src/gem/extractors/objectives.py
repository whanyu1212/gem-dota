"""Objective event extractor for Dota 2 replays.

Listens to combat log DEATH events and emits structured records for tower
kills, Roshan kills, and barracks destructions.

Reference: examples/ward_smoke_rosh.py, refs/parser/src/main/java/opendota/Parse.java
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from gem.combatlog import CombatLogEntry

if TYPE_CHECKING:
    from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Team constants
# ---------------------------------------------------------------------------

_TEAM_RADIANT = 2
_TEAM_DIRE = 3

# CDOTAUserMsg_ChatEvent type constants for Aegis
_CHAT_MSG_AEGIS = 8
_CHAT_MSG_AEGIS_STOLEN = 53
_CHAT_MSG_DENIED_AEGIS = 51

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
    """

    tick: int
    killer: str
    kill_number: int


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
    """Extracts tower kills, Roshan kills, and barracks kills from a replay.

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
    """

    tower_kills: list[TowerKill]
    roshan_kills: list[RoshanKill]
    barracks_kills: list[BarracksKill]
    aegis_events: list[AegisEvent]

    def __init__(self) -> None:
        self.tower_kills = []
        self.roshan_kills = []
        self.barracks_kills = []
        self.aegis_events = []

    def attach(self, parser: ReplayParser) -> None:
        """Register this extractor's callbacks with a parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        parser.on_combat_log_entry(self._on_combat_log)
        parser.on_chat_event(self._on_chat_event)

    def _on_chat_event(self, msg: Any, tick: int) -> None:
        event_type = _AEGIS_EVENT_TYPE.get(msg.type)
        if event_type is not None:
            self.aegis_events.append(
                AegisEvent(tick=tick, player_id=msg.playerid_1, event_type=event_type)
            )

    def _on_combat_log(self, entry: CombatLogEntry) -> None:
        if entry.log_type != "DEATH":
            return
        target = entry.target_name
        if target == "npc_dota_roshan":
            self.roshan_kills.append(
                RoshanKill(
                    tick=entry.tick,
                    killer=entry.attacker_name,
                    kill_number=len(self.roshan_kills) + 1,
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
