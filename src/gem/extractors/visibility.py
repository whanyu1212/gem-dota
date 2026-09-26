"""Authoritative per-team NPC visibility extraction from team entity bitsets.

Reference: odota/parser src/main/java/opendota/Parse.java (team-data and
``EntityNames`` access), the ``CDOTA_DataNonSpectator`` replay send-table
schema, and the entity lifecycle in dotabuff/manta entity.go.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.results.models import EntityVisibilityEvent, HeroVisibilityEvent, VisibilityState
from gem.schema.sendtable.models import FieldAccessPlan, ResolvedField
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.extractors.players import PlayerExtractor
    from gem.parser import ReplayParser

_RADIANT_DATA_CLASSES = ("CDOTADataRadiant", "CDOTA_DataRadiant")
_DIRE_DATA_CLASSES = ("CDOTADataDire", "CDOTA_DataDire")
_HERO_IDENTITY_CLASSES = ("CDOTAPlayerController", "CDOTA_PlayerResource")
_HERO_CLASS_PREFIX = "CDOTA_Unit_Hero_"
_NPC_SCHEMA_FIELD = "m_iDayTimeVisionRange"
_ENTITY_NAME_FIELDS = (
    "m_pEntity.m_nameStringTableIndex",
    "m_pEntity.m_nameStringableIndex",
)
_ENTITY_METADATA_FIELDS = FieldAccessPlan((*_ENTITY_NAME_FIELDS, "m_iTeamNum"))
_VISIBILITY_FIELDS = FieldAccessPlan(tuple(f"m_bNPCVisibleState.{word:04d}" for word in range(256)))
_MISSING_WORD = object()


@dataclass(frozen=True, slots=True)
class _Observation:
    identity: tuple[int, int]
    hero_name: str
    radiant_state: VisibilityState
    dire_state: VisibilityState

    @property
    def states(self) -> tuple[VisibilityState, VisibilityState]:
        return self.radiant_state, self.dire_state


@dataclass(frozen=True, slots=True)
class _EntityObservation:
    identity: tuple[int, int]
    class_name: str
    npc_name: str
    team: int | None
    active: bool
    radiant_state: VisibilityState
    dire_state: VisibilityState


class VisibilityExtractor:
    """Collect authoritative visibility transitions for networked Dota NPCs.

    Entity callbacks update lifecycle state and mark the extractor dirty.
    Sampling happens at the parser's completed-packet boundary so visibility
    words, entity metadata, and canonical hero identity changes from the whole
    packet are observed atomically. ``events`` retains the existing canonical
    hero timeline; ``entity_events`` is the all-NPC identity-aware timeline.

    Args:
        player_extractor: The attached player extractor used to resolve each
            slot's canonical hero entity.

    Attributes:
        events: Chronological canonical-hero visibility transitions.
        entity_events: Chronological networked Dota NPC visibility and lifecycle
            transitions. Only active classes whose schema contains
            ``m_iDayTimeVisionRange`` are sampled; terminal events are inactive
            with unknown visibility.
    """

    def __init__(self, player_extractor: PlayerExtractor) -> None:
        self.events: list[HeroVisibilityEvent] = []
        self.entity_events: list[EntityVisibilityEvent] = []
        self._player_extractor = player_extractor
        self._parser: ReplayParser | None = None
        self._data_radiant: Entity | None = None
        self._data_dire: Entity | None = None
        self._dirty = False

        self._npc_classes: dict[int, bool] = {}
        self._metadata_paths: dict[int, frozenset[tuple[int, ...]]] = {}
        self._active_entities: dict[tuple[int, int], Entity] = {}
        self._identity_by_index: dict[int, tuple[int, int]] = {}
        self._pending_lifecycle: dict[tuple[int, int], tuple[bool, Entity]] = {}
        self._pending_metadata: set[tuple[int, int]] = set()
        self._entity_metadata: dict[tuple[int, int], tuple[str, str, int | None]] = {}
        self._entity_observations: dict[tuple[int, int], _EntityObservation] = {}
        self._radiant_words: dict[int, int | None] = {}
        self._dire_words: dict[int, int | None] = {}
        self._visibility_dirty = False

        self._observations: dict[int, _Observation] = {}
        self._coalesce_tick: int | None = None
        self._coalesce_start = 0
        self._coalesce_baseline: dict[int, _Observation] = {}
        self._entity_coalesce_start = 0
        self._entity_coalesce_baseline: dict[tuple[int, int], _EntityObservation] = {}
        self._entity_coalesce_terminals: dict[tuple[int, int], Entity] = {}
        self._entity_coalesce_affected: set[tuple[int, int]] = set()

    def attach(self, parser: ReplayParser) -> None:
        """Attach to visibility, NPC metadata/lifecycle, and packet boundaries."""
        self._parser = parser
        if hasattr(parser, "_on_entity_fields"):
            parser._on_entity_filtered(
                self._on_entity,
                class_names=_HERO_IDENTITY_CLASSES,
            )
            parser._on_entity_fields(
                self._on_entity,
                required_fields=(_VISIBILITY_FIELDS.names[0],),
                changed_fields=_VISIBILITY_FIELDS.names,
            )
            parser._on_entity_fields(
                self._on_entity,
                required_fields=(_NPC_SCHEMA_FIELD,),
                changed_fields=_ENTITY_METADATA_FIELDS.names,
            )
        else:
            # Lightweight parser doubles and older embedders do not expose the
            # private optimized registration path.
            parser.on_entity(self._on_entity)
        parser._on_packet_end(self._on_packet_end)

    @staticmethod
    def _same_identity(left: Entity | None, right: Entity) -> bool:
        return left is not None and (left.get_index(), left.get_serial()) == (
            right.get_index(),
            right.get_serial(),
        )

    def _is_npc_class(self, entity: Entity) -> bool:
        """Classify an NPC-derived send-table class once per class ID."""
        class_id = entity.get_class_id()
        cached = self._npc_classes.get(class_id)
        if cached is not None:
            return cached

        serializer = getattr(entity.cls, "serializer", None)
        if serializer is not None:
            is_npc = serializer._resolve_field(_NPC_SCHEMA_FIELD).path is not None
            if is_npc:
                self._metadata_paths[class_id] = frozenset(
                    field.path
                    for field in serializer._resolve_plan(_ENTITY_METADATA_FIELDS)
                    if field.path is not None
                )
        else:
            # Serializer-less entities only occur in lightweight unit fixtures;
            # their flat state remains faithful evidence of field existence.
            is_npc = _NPC_SCHEMA_FIELD in entity._state
        self._npc_classes[class_id] = is_npc
        return is_npc

    def _mark_terminal(self, entity: Entity) -> None:
        identity = (entity.get_index(), entity.get_serial())
        if self._active_entities.get(identity) is entity:
            self._active_entities.pop(identity, None)
        if self._identity_by_index.get(entity.get_index()) == identity:
            self._identity_by_index.pop(entity.get_index(), None)
        self._pending_lifecycle[identity] = (False, entity)

    def _mark_active(self, entity: Entity) -> None:
        identity = (entity.get_index(), entity.get_serial())
        previous_identity = self._identity_by_index.get(entity.get_index())
        if previous_identity is not None and previous_identity != identity:
            previous = self._active_entities.pop(previous_identity, None)
            if previous is not None:
                self._pending_lifecycle[previous_identity] = (False, previous)
        self._active_entities[identity] = entity
        self._identity_by_index[entity.get_index()] = identity
        self._entity_metadata[identity] = self._read_entity_metadata(entity)
        self._pending_lifecycle[identity] = (True, entity)

    def _metadata_changed(self, entity: Entity) -> bool:
        """Return whether sampled public metadata changed for an active identity."""
        updated_paths = entity._field_state._updated_paths
        if updated_paths is not None:
            metadata_paths = self._metadata_paths.get(entity.get_class_id(), frozenset())
            if not any(path in metadata_paths for path in updated_paths):
                return False
        identity = (entity.get_index(), entity.get_serial())
        previous = self._entity_observations.get(identity)
        metadata = self._read_entity_metadata(entity)
        changed = previous is None or metadata != self._entity_metadata.get(identity)
        if changed:
            self._entity_metadata[identity] = metadata
        return changed

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        class_name = entity.get_class_name()
        terminal = op.has(EntityOp.LEFT | EntityOp.DELETED)
        relevant = class_name in _HERO_IDENTITY_CLASSES or (
            class_name.startswith(_HERO_CLASS_PREFIX)
            and op.has(EntityOp.CREATED | EntityOp.ENTERED | EntityOp.LEFT | EntityOp.DELETED)
        )
        if class_name in _RADIANT_DATA_CLASSES:
            # Preserve the established canonical-hero timeline semantics: team
            # data remains readable while temporarily left and is cleared only
            # when its identity is deleted.
            if op.has(EntityOp.DELETED):
                if self._same_identity(self._data_radiant, entity):
                    self._data_radiant = None
            else:
                self._data_radiant = entity
            relevant = True
            self._visibility_dirty = True
        elif class_name in _DIRE_DATA_CLASSES:
            if op.has(EntityOp.DELETED):
                if self._same_identity(self._data_dire, entity):
                    self._data_dire = None
            else:
                self._data_dire = entity
            relevant = True
            self._visibility_dirty = True

        if self._is_npc_class(entity):
            if terminal:
                self._mark_terminal(entity)
                relevant = True
            elif entity.active and (
                op.has(EntityOp.CREATED | EntityOp.ENTERED)
                or (entity.get_index(), entity.get_serial()) not in self._active_entities
            ):
                self._mark_active(entity)
                relevant = True
            elif entity.active and self._metadata_changed(entity):
                self._pending_metadata.add((entity.get_index(), entity.get_serial()))
                relevant = True

        # Ordinary NPC state updates do not affect this timeline. Visibility
        # changes arrive on team-data entities; metadata and lifecycle changes
        # are detected explicitly above. Controller/resource updates remain
        # relevant because they can change canonical-hero ownership.
        self._dirty = self._dirty or relevant

    @staticmethod
    def _team_state(value: int | None, entity_index: int) -> VisibilityState:
        if value is None:
            return VisibilityState.UNKNOWN
        bit = entity_index & 63
        return VisibilityState.VISIBLE if value & (1 << bit) else VisibilityState.HIDDEN

    def _visibility_words(
        self, words: set[int]
    ) -> tuple[dict[int, int | None], dict[int, int | None]]:
        """Read each requested team/word pair exactly once for this sample."""
        radiant_fields = (
            self._data_radiant._resolve_fields(_VISIBILITY_FIELDS)
            if self._data_radiant is not None
            else ()
        )
        dire_fields = (
            self._data_dire._resolve_fields(_VISIBILITY_FIELDS)
            if self._data_dire is not None
            else ()
        )
        radiant = {
            word: (
                self._data_radiant._get_uint64_resolved(radiant_fields[word])
                if self._data_radiant is not None
                else None
            )
            for word in words
        }
        dire = {
            word: (
                self._data_dire._get_uint64_resolved(dire_fields[word])
                if self._data_dire is not None
                else None
            )
            for word in words
        }
        return radiant, dire

    def _entity_name(
        self, entity: Entity, fields: tuple[ResolvedField, ...] | None = None
    ) -> str | None:
        parser = self._parser
        if parser is None:
            return None
        names = parser.string_tables.get_by_name("EntityNames")
        if names is None:
            return None
        resolved = fields or entity._resolve_fields(_ENTITY_METADATA_FIELDS)
        for field in resolved[:2]:
            name_index = entity._get_int32_resolved(field)
            if name_index is None or name_index < 0:
                continue
            item = names.items.get(name_index)
            if item is not None and item[0]:
                return item[0]
        return None

    def _hero_name(self, player_id: int, hero: Entity) -> str:
        name = self._entity_name(hero)
        if name is not None:
            return name

        # PlayerExtractor's first alias deliberately preserves Valve's compound
        # class suffix (QueenOfPain -> queenofpain), making it a deterministic
        # canonical fallback without lossy camel-case splitting.
        aliases = self._player_extractor._hero_aliases(hero.get_class_name())
        if aliases[0]:
            return aliases[0]
        return f"npc_dota_hero_player_{player_id}"

    def _read_entity_metadata(self, entity: Entity) -> tuple[str, str, int | None]:
        class_name = entity.get_class_name()
        fields = entity._resolve_fields(_ENTITY_METADATA_FIELDS)
        return (
            class_name,
            self._entity_name(entity, fields) or class_name,
            entity._get_int32_resolved(fields[2]),
        )

    def _observation(
        self,
        player_id: int,
        hero: Entity,
        radiant_words: dict[int, int | None],
        dire_words: dict[int, int | None],
    ) -> _Observation:
        index = hero.get_index()
        word = index >> 6
        return _Observation(
            identity=(index, hero.get_serial()),
            hero_name=self._hero_name(player_id, hero),
            radiant_state=self._team_state(radiant_words.get(word), index),
            dire_state=self._team_state(dire_words.get(word), index),
        )

    def _entity_observation(
        self,
        entity: Entity,
        radiant_words: dict[int, int | None],
        dire_words: dict[int, int | None],
    ) -> _EntityObservation:
        index = entity.get_index()
        word = index >> 6
        class_name, npc_name, team = self._entity_metadata[
            (entity.get_index(), entity.get_serial())
        ]
        return _EntityObservation(
            identity=(index, entity.get_serial()),
            class_name=class_name,
            npc_name=npc_name,
            team=team,
            active=True,
            radiant_state=self._team_state(radiant_words.get(word), index),
            dire_state=self._team_state(dire_words.get(word), index),
        )

    def _terminal_observation(
        self, identity: tuple[int, int], entity: Entity | None
    ) -> _EntityObservation:
        previous = self._entity_coalesce_baseline.get(identity)
        metadata = self._entity_metadata.get(identity)
        if metadata is not None:
            class_name, npc_name, team = metadata
        elif previous is not None:
            class_name = previous.class_name
            npc_name = previous.npc_name
            team = previous.team
        elif entity is not None:
            class_name, npc_name, team = self._read_entity_metadata(entity)
        else:
            # Every terminal is backed by either a prior observation or the
            # lifecycle callback's entity. This is defensive for malformed input.
            class_name = ""
            npc_name = ""
            team = None
        return _EntityObservation(
            identity=identity,
            class_name=class_name,
            npc_name=npc_name,
            team=team,
            active=False,
            radiant_state=VisibilityState.UNKNOWN,
            dire_state=VisibilityState.UNKNOWN,
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

    @staticmethod
    def _entity_event(tick: int, observation: _EntityObservation) -> EntityVisibilityEvent:
        return EntityVisibilityEvent(
            tick=tick,
            entity_index=observation.identity[0],
            entity_serial=observation.identity[1],
            class_name=observation.class_name,
            npc_name=observation.npc_name,
            team=observation.team,
            active=observation.active,
            radiant_state=observation.radiant_state,
            dire_state=observation.dire_state,
        )

    def _rebuild_coalesced_events(self, tick: int) -> None:
        """Replace this tick's hero tail with net identity/state transitions."""
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

    def _rebuild_coalesced_entity_events(self, tick: int) -> None:
        """Replace this tick's entity tail with final state/lifecycle transitions."""
        del self.entity_events[self._entity_coalesce_start :]
        for identity in sorted(self._entity_coalesce_affected):
            previous = self._entity_coalesce_baseline.get(identity)
            current = self._entity_observations.get(identity)
            if current is not None:
                if previous is None or current != previous:
                    self.entity_events.append(self._entity_event(tick, current))
                continue
            if previous is not None:
                terminal = self._terminal_observation(
                    identity, self._entity_coalesce_terminals.get(identity)
                )
                self.entity_events.append(self._entity_event(tick, terminal))

    def _on_packet_end(self, tick: int) -> None:
        if not self._dirty:
            return
        self._dirty = False

        if self._coalesce_tick != tick:
            self._coalesce_tick = tick
            self._coalesce_start = len(self.events)
            self._coalesce_baseline = dict(self._observations)
            self._entity_coalesce_start = len(self.entity_events)
            self._entity_coalesce_baseline = dict(self._entity_observations)
            self._entity_coalesce_terminals = {}
            self._entity_coalesce_affected = set()

        for identity, (active, entity) in self._pending_lifecycle.items():
            if active:
                self._entity_coalesce_terminals.pop(identity, None)
            else:
                self._entity_coalesce_terminals[identity] = entity
        lifecycle = dict(self._pending_lifecycle)
        self._pending_lifecycle.clear()
        metadata_changed = set(self._pending_metadata)
        self._pending_metadata.clear()

        canonical_heroes: dict[int, Entity] = {}
        for player_id in range(10):
            hero = self._player_extractor._canonical_hero_entity(player_id)
            if hero is not None:
                canonical_heroes[player_id] = hero

        hero_words = {hero.get_index() >> 6 for hero in canonical_heroes.values()}
        uncached_hero_words = {
            word
            for word in hero_words
            if word not in self._radiant_words or word not in self._dire_words
        }
        identities_by_word: dict[int, set[tuple[int, int]]] = {}
        if self._visibility_dirty or uncached_hero_words:
            for identity in self._active_entities:
                word = identity[0] >> 6
                if self._visibility_dirty or word in uncached_hero_words:
                    identities_by_word.setdefault(word, set()).add(identity)
        affected = set(metadata_changed)
        for identity, (active, _entity) in lifecycle.items():
            if active:
                affected.add(identity)
            else:
                self._entity_observations.pop(identity, None)

        words_to_read = {
            identity[0] >> 6 for identity in affected if identity in self._active_entities
        }
        if self._visibility_dirty:
            words_to_read.update(identities_by_word)
            words_to_read.update(hero_words)
        else:
            words_to_read.update(uncached_hero_words)

        radiant_updates, dire_updates = self._visibility_words(words_to_read)
        changed_words: set[int] = set()
        for word in words_to_read:
            radiant_value = radiant_updates[word]
            dire_value = dire_updates[word]
            if (
                self._radiant_words.get(word, _MISSING_WORD) != radiant_value
                or self._dire_words.get(word, _MISSING_WORD) != dire_value
            ):
                changed_words.add(word)
            self._radiant_words[word] = radiant_value
            self._dire_words[word] = dire_value
        self._visibility_dirty = False

        for word in changed_words:
            affected.update(identities_by_word.get(word, ()))
        self._entity_coalesce_affected.update(affected)
        self._entity_coalesce_affected.update(lifecycle)
        for identity in affected:
            active_entity = self._active_entities.get(identity)
            if active_entity is not None:
                self._entity_observations[identity] = self._entity_observation(
                    active_entity, self._radiant_words, self._dire_words
                )
        self._rebuild_coalesced_entity_events(tick)

        self._observations = {
            player_id: self._observation(player_id, hero, self._radiant_words, self._dire_words)
            for player_id, hero in canonical_heroes.items()
        }
        self._rebuild_coalesced_events(tick)


__all__ = ["VisibilityExtractor"]
