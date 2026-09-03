"""Objective event extractor for Dota 2 replays.

Listens to combat log DEATH events and emits structured records for tower
kills, Roshan kills, and barracks destructions.

Reference: refs/parser/src/main/java/opendota/Parse.java
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from gem.combat.log import CombatLogEntry
from gem.extractors._snapshots import _player_id_from_entity, _pos
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser
    from gem.state.entities import Entity

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

# Planted Roshan's Banner *unit* entity (distinct from the position-less
# ``CDOTA_Item_Roshans_Banner`` drop). When a held banner is planted it spawns a
# stationary allied unit that projects a movement-speed / bonus-damage aura to
# nearby allied heroes and creeps — a siege amplifier used to push barracks. The
# unit carries a readable world position via ``CBodyComponent`` (same fields the
# ward extractor reads), so the plant location is recoverable here.
_BANNER_UNIT_CLASS = "CDOTA_Unit_Roshans_Banner"
_BANNER_FIELDS = FieldAccessPlan(("m_lifeState", "m_iTeamNum", "m_hOwnerEntity"))

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
        killer: NPC name of the unit that landed the killing blow
            (``attacker_name``).
        tower_name: Internal NPC name of the destroyed tower.
        killer_source: The ``damage_source_name`` (the owning hero for a summon /
            projectile kill), used for source-first killer attribution. Empty for
            an auto-attack where source == attacker.
    """

    tick: int
    team: int
    killer: str
    tower_name: str
    killer_source: str = ""


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
        killer_source: The ``damage_source_name`` (owning hero for a summon /
            projectile kill), for source-first killer attribution.
    """

    tick: int
    killer: str
    kill_number: int
    drops: list[str] = field(default_factory=list)
    killer_source: str = ""


@dataclass
class BarracksKill:
    """One barracks destruction event.

    Attributes:
        tick: Game tick when the barracks was destroyed.
        team: Team that *owned* the barracks (2=Radiant, 3=Dire).
        killer: NPC name of the unit that landed the killing blow.
        barracks_name: Internal NPC name of the destroyed barracks.
        killer_source: The ``damage_source_name`` (owning hero for a summon /
            projectile kill), for source-first killer attribution.
    """

    tick: int
    team: int
    killer: str
    barracks_name: str
    killer_source: str = ""


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


@dataclass
class BannerPlant:
    """One Roshan's Banner plant event.

    Recovered from the ``CDOTA_Unit_Roshans_Banner`` unit's creation in the
    entity stream — the unit spawns where the banner is planted and carries a
    world position, unlike the position-less banner *item* drop. The planter team
    and slot come from ``m_iTeamNum`` and the owner entity respectively.

    Attributes:
        tick: Game tick the banner was planted (the unit's creation tick).
        team: Team that planted the banner (2=Radiant, 3=Dire), or 0 if unknown.
        player_id: Player slot (0–9) of the planter, or -1 if unresolved.
        x: World x coordinate of the plant, or ``None`` if unavailable.
        y: World y coordinate of the plant, or ``None`` if unavailable.
    """

    tick: int
    team: int
    player_id: int
    x: float | None
    y: float | None


@dataclass
class CourierDeath:
    """One courier death, detected from the combat log.

    Captured from a ``DEATH`` entry whose target is ``npc_dota_courier``. The
    courier's owning team is not in the event name, so it is left ``0`` here and
    inferred (as the killer's opposite team) when the OpenDota ``objectives``
    timeline is assembled. The combat log carries no bounty value.

    Attributes:
        tick: Game tick of the courier's death.
        killer: NPC name of the unit that killed the courier, or empty string.
        killer_source: The ``damage_source_name`` (owning hero for a summon /
            projectile kill), for source-first killer attribution.
    """

    tick: int
    killer: str
    killer_source: str = ""


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
    courier_deaths: list[CourierDeath]
    banner_plants: list[BannerPlant]

    def __init__(self) -> None:
        self.tower_kills = []
        self.roshan_kills = []
        self.barracks_kills = []
        self.aegis_events = []
        self.tormentor_kills = []
        self.shrine_kills = []
        self.courier_deaths = []
        self.banner_plants = []
        # index → (creation_tick, short drop name) for currently-alive Roshan
        # item entities. The creation tick lets a Roshan death snapshot exclude
        # items held over from an earlier Roshan: a held but unused Cheese /
        # Refresher Shard / Banner stays a live CDOTA_Item_* entity, so without
        # this it would be re-counted as a later Roshan's drop (e.g. a banner
        # from Roshan #2 reappearing in Roshan #3's drops).
        self._roshan_items: dict[int, tuple[int, str]] = {}
        # Death tick of the most recently recorded Roshan; a drop belongs to the
        # next Roshan only if it was created after this tick.
        self._last_roshan_death_tick: int = -1
        # Banner-unit index → last seen m_lifeState. A plant is the transition
        # into alive (0), which fires on a fresh CREATED and on a recycled slot
        # re-entering as UPDATED|ENTERED — gating on CREATED alone would miss the
        # latter (same lifecycle the ward extractor handles).
        self._banner_lifestate: dict[int, int] = {}
        # Belt-and-suspenders against a transition re-emitted at the same tick:
        # one (index, spawn_tick) pair yields at most one BannerPlant.
        self._banner_seen: set[tuple[int, int]] = set()
        self._parser: ReplayParser | None = None

    def attach(self, parser: ReplayParser) -> None:
        """Register this extractor's callbacks with a parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_combat_log_entry(self._on_combat_log)
        parser.on_chat_event(self._on_chat_event)
        parser._on_entity_filtered(
            self._on_entity,
            class_names=(*_ROSHAN_ITEM_DROPS, _BANNER_UNIT_CLASS),
        )

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        name = entity.get_class_name()
        if name == _BANNER_UNIT_CLASS:
            self._on_banner_unit(entity, op)
            return
        drop_name = _ROSHAN_ITEM_DROPS.get(name)
        if drop_name is None:
            return
        idx = entity.get_index()
        # Use a bitwise test rather than ``op == EntityOp.DELETED_LEFT``: a delete
        # may arrive without the LEFT bit, and an exact composite match would then
        # leave the item in ``_roshan_items`` and inflate the drop snapshot.
        if op.has(EntityOp.DELETED):
            self._roshan_items.pop(idx, None)
        else:
            # Stamp the creation tick once and keep it across later updates so a
            # position/state refresh does not reset the item's age. A recycled
            # slot (DELETED then re-CREATED) is a genuinely new item, so re-stamp
            # only when the slot is not already tracked or the op is CREATED.
            if op.has(EntityOp.CREATED) or idx not in self._roshan_items:
                tick = self._parser.tick if self._parser is not None else 0
                self._roshan_items[idx] = (tick, drop_name)

    def _on_banner_unit(self, entity: Entity, op: EntityOp) -> None:
        # A banner plant is the unit's transition into the alive life state, not a
        # specific op: a fresh plant arrives as CREATED, but a banner reusing a
        # recycled slot re-enters as UPDATED|ENTERED. Detecting the life-state
        # edge (mirroring the ward extractor) captures both while ignoring pure
        # position updates on an already-planted banner. Deletes clear the slot.
        idx = entity.get_index()
        if op.has(EntityOp.DELETED):
            self._banner_lifestate.pop(idx, None)
            return

        fields = entity._resolve_fields(_BANNER_FIELDS)
        life_state = entity._get_int32_resolved(fields[0])
        if life_state is None:
            life_state = 0 if op.has(EntityOp.CREATED) else 2
        prev_ls = self._banner_lifestate.get(idx, 2)
        self._banner_lifestate[idx] = life_state

        # Only a transition into alive (0) from a non-alive prior is a plant.
        if not (life_state == 0 and prev_ls != 0):
            return

        tick = self._parser.tick if self._parser is not None else 0
        key = (idx, tick)
        if key in self._banner_seen:
            return
        self._banner_seen.add(key)

        pos = _pos(entity)
        team = entity._get_int32_resolved(fields[1]) or 0

        # Resolve the planter via m_hOwnerEntity → owner entity → player slot,
        # mirroring ward placer attribution (the owner may be an owned unit, so
        # allow the m_iPlayerOwnerID fallback). -1 = unresolved.
        player_id = -1
        owner_handle = entity._get_uint32_resolved(fields[2])
        if owner_handle is not None and self._parser is not None:
            em = self._parser.entity_manager
            if em is not None:
                owner = em.find_by_handle(owner_handle)
                resolved = _player_id_from_entity(owner, allow_owner=True)
                if resolved is not None:
                    player_id = resolved

        self.banner_plants.append(
            BannerPlant(
                tick=tick,
                team=team,
                player_id=player_id,
                x=pos[0] if pos else None,
                y=pos[1] if pos else None,
            )
        )

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
            # Snapshot alive Roshan item entities as this Roshan's drops. An
            # item entity is created when Roshan spawns and deleted when picked
            # up *and consumed*; a held-but-unused drop from an earlier Roshan
            # is still alive here, so restrict the snapshot to items created
            # after the previous Roshan's death — those belong to this Roshan.
            drops = sorted(
                token
                for created_tick, token in self._roshan_items.values()
                if created_tick > self._last_roshan_death_tick
            )
            self._last_roshan_death_tick = entry.tick
            self.roshan_kills.append(
                RoshanKill(
                    tick=entry.tick,
                    killer=entry.attacker_name,
                    kill_number=len(self.roshan_kills) + 1,
                    drops=drops,
                    killer_source=entry.damage_source_name,
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
                    killer_source=entry.damage_source_name,
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
                    killer_source=entry.damage_source_name,
                )
            )
        elif target.startswith("npc_dota_courier"):
            self.courier_deaths.append(
                CourierDeath(
                    tick=entry.tick,
                    killer=entry.attacker_name,
                    killer_source=entry.damage_source_name,
                )
            )
