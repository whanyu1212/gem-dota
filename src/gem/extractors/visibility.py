"""Authoritative per-team hero visibility extraction from team entity bitsets.

Reference: refs/parser/src/main/java/opendota/Parse.java (team-data entity access)
and the ``CDOTA_DataNonSpectator`` replay send-table schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.results.models import HeroVisibilityEvent, VisibilityState
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.extractors.players import PlayerExtractor
    from gem.parser import ReplayParser

_HERO_CLASS_PREFIX = "CDOTA_Unit_Hero_"
_RADIANT_DATA_CLASSES = ("CDOTADataRadiant", "CDOTA_DataRadiant")
_DIRE_DATA_CLASSES = ("CDOTADataDire", "CDOTA_DataDire")
_WATCHED_CLASSES = (
    *_RADIANT_DATA_CLASSES,
    *_DIRE_DATA_CLASSES,
    "CDOTAPlayerController",
    "CDOTA_PlayerResource",
)


@dataclass(frozen=True, slots=True)
class _Observation:
    identity: tuple[int, int]
    hero_name: str
    radiant_state: VisibilityState
    dire_state: VisibilityState

    @property
    def states(self) -> tuple[VisibilityState, VisibilityState]:
        return self.radiant_state, self.dire_state


class VisibilityExtractor:
    """Collect visibility transitions for each player's canonical hero.

    Entity callbacks only mark the extractor dirty. Sampling happens at the
    parser's completed-packet boundary so visibility bits and hero/controller
    identity changes from the entire packet are observed atomically.

    Args:
        player_extractor: The attached player extractor used to resolve each
            slot's canonical hero entity.

    Attributes:
        events: Chronological, identity-aware visibility transitions.
    """

    def __init__(self, player_extractor: PlayerExtractor) -> None:
        self.events: list[HeroVisibilityEvent] = []
        self._player_extractor = player_extractor
        self._parser: ReplayParser | None = None
        self._data_radiant: Entity | None = None
        self._data_dire: Entity | None = None
        self._dirty = False
        self._observations: dict[int, _Observation] = {}
        self._coalesce_tick: int | None = None
        self._coalesce_start = 0
        self._coalesce_baseline: dict[int, _Observation] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Attach to entity updates and the parser's private packet boundary.

        Args:
            parser: Replay parser that owns the entity stream.
        """
        self._parser = parser
        parser._on_entity_filtered(
            self._on_entity,
            class_names=_WATCHED_CLASSES,
            class_prefixes=(_HERO_CLASS_PREFIX,),
        )
        parser._on_packet_end(self._on_packet_end)

    @staticmethod
    def _same_identity(left: Entity | None, right: Entity) -> bool:
        return left is not None and (left.get_index(), left.get_serial()) == (
            right.get_index(),
            right.get_serial(),
        )

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        class_name = entity.get_class_name()
        if class_name in _RADIANT_DATA_CLASSES:
            if op.has(EntityOp.DELETED):
                if self._same_identity(self._data_radiant, entity):
                    self._data_radiant = None
            else:
                self._data_radiant = entity
        elif class_name in _DIRE_DATA_CLASSES:
            if op.has(EntityOp.DELETED):
                if self._same_identity(self._data_dire, entity):
                    self._data_dire = None
            else:
                self._data_dire = entity
        self._dirty = True

    @staticmethod
    def _team_state(team_data: Entity | None, entity_index: int) -> VisibilityState:
        if team_data is None:
            return VisibilityState.UNKNOWN
        word = entity_index >> 6
        bit = entity_index & 63
        value = team_data.get_uint64(f"m_bNPCVisibleState.{word:04d}")
        if value is None:
            return VisibilityState.UNKNOWN
        return VisibilityState.VISIBLE if value & (1 << bit) else VisibilityState.HIDDEN

    def _hero_name(self, player_id: int, hero: Entity) -> str:
        parser = self._parser
        if parser is not None:
            names = parser.string_tables.get_by_name("EntityNames")
            if names is not None:
                for field_name in (
                    "m_pEntity.m_nameStringTableIndex",
                    "m_pEntity.m_nameStringableIndex",
                ):
                    name_index = hero.get_int32(field_name)
                    if name_index is None or name_index < 0:
                        continue
                    item = names.items.get(name_index)
                    if item is not None and item[0]:
                        return item[0]

        # PlayerExtractor's first alias deliberately preserves Valve's compound
        # class suffix (QueenOfPain -> queenofpain), making it a deterministic
        # canonical fallback without lossy camel-case splitting.
        aliases = self._player_extractor._hero_aliases(hero.get_class_name())
        if aliases[0]:
            return aliases[0]
        return f"npc_dota_hero_player_{player_id}"

    def _observation(self, player_id: int, hero: Entity) -> _Observation:
        index = hero.get_index()
        return _Observation(
            identity=(index, hero.get_serial()),
            hero_name=self._hero_name(player_id, hero),
            radiant_state=self._team_state(self._data_radiant, index),
            dire_state=self._team_state(self._data_dire, index),
        )

    @staticmethod
    def _event(tick: int, player_id: int, observation: _Observation) -> HeroVisibilityEvent:
        return HeroVisibilityEvent(
            tick=tick,
            player_id=player_id,
            hero_name=observation.hero_name,
            entity_index=observation.identity[0],
            entity_serial=observation.identity[1],
            radiant_state=observation.radiant_state,
            dire_state=observation.dire_state,
        )

    def _rebuild_coalesced_events(self, tick: int) -> None:
        """Replace this tick's tail with net identity/state transitions."""
        del self.events[self._coalesce_start :]
        for player_id in range(10):
            previous = self._coalesce_baseline.get(player_id)
            current = self._observations.get(player_id)

            if previous is not None and (current is None or current.identity != previous.identity):
                terminal = _Observation(
                    identity=previous.identity,
                    hero_name=previous.hero_name,
                    radiant_state=VisibilityState.UNKNOWN,
                    dire_state=VisibilityState.UNKNOWN,
                )
                self.events.append(self._event(tick, player_id, terminal))

            if current is None:
                continue
            if (
                previous is None
                or current.identity != previous.identity
                or current.states != previous.states
                or current.hero_name != previous.hero_name
            ):
                self.events.append(self._event(tick, player_id, current))

    def _on_packet_end(self, tick: int) -> None:
        if not self._dirty:
            return
        self._dirty = False

        if self._coalesce_tick != tick:
            self._coalesce_tick = tick
            self._coalesce_start = len(self.events)
            self._coalesce_baseline = dict(self._observations)

        current_observations: dict[int, _Observation] = {}
        for player_id in range(10):
            hero = self._player_extractor._canonical_hero_entity(player_id)
            if hero is not None:
                current_observations[player_id] = self._observation(player_id, hero)

        self._observations = current_observations
        self._rebuild_coalesced_events(tick)


__all__ = ["VisibilityExtractor"]
