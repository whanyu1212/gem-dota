"""Draft / hero pick extractor for Dota 2 replays.

Polls ``CDOTAGamerulesProxy`` entity for hero bans and picks during the draft
phase and emits ``DraftEvent`` records in order of assignment.

Hero name resolution follows the reference implementation
(refs/parser/src/main/java/opendota/Parse.java lines 509-574, 736-739):
for picks, the NPC name is derived from the hero entity class name obtained by
resolving the player's ``m_hSelectedHero`` handle.  The static ``heroes.json``
mapping is used as a fallback for heroes whose entities do not yet exist (bans
or draft-phase picks before the entity spawns).

Reference: refs/parser/src/main/java/opendota/Parse.java lines 509-574
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.constants import HEROES
from gem.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

# Build reverse mapping: hero_id (int) → npc_name (str) from bundled data.
# This only covers heroes present in heroes.json (IDs ≤ 155 as of the bundled
# snapshot).  Newer heroes are resolved at parse time from entity class names.
_HERO_ID_TO_NPC: dict[int, str] = {v["id"]: k for k, v in HEROES.items() if "id" in v}

# Converts a hero entity class name to two candidate NPC name forms, matching
# the reference implementation logic:
#   "CDOTA_Unit_Hero_Anti_Mage" → "npc_dota_hero_anti_mage" (lowercase + _)
#   "CDOTA_Unit_Hero_AntiMage"  → "npc_dota_hero_antimage"  (camelCase fold)
_PREFIX = "CDOTA_Unit_Hero_"
_CAMEL_RE = re.compile(r"([A-Z])")


def _class_to_npc_names(class_name: str) -> tuple[str, str]:
    """Return the two candidate NPC names for a hero entity class name."""
    ending = class_name[len(_PREFIX) :]
    name1 = "npc_dota_hero_" + ending.lower()
    name2 = "npc_dota_hero" + _CAMEL_RE.sub(r"_\1", ending).lower()
    return name1, name2


def _class_to_npc(class_name: str) -> str:
    """Resolve a hero entity class name to an NPC name, or empty string."""
    n1, n2 = _class_to_npc_names(class_name)
    return n1 if n1 in HEROES else (n2 if n2 in HEROES else n1)


# Number of ban slots (indices 0-13) and pick slots (indices 0-9) in draft
_BAN_SLOTS = 14
_PICK_SLOTS = 10


@dataclass
class DraftEvent:
    """A single hero ban or pick in the draft.

    Attributes:
        tick: Game tick when the assignment was detected.
        slot_index: Draft order index — 0-13 for bans, 0-9 for picks.
        hero_id: Dota 2 internal hero ID.
        hero_name: NPC hero name (e.g. ``"npc_dota_hero_axe"``), or ``""`` if unknown.
        is_pick: True for a pick, False for a ban.
        team: Team number (2=Radiant, 3=Dire) that made this pick/ban, or 0 if unknown.
    """

    tick: int
    slot_index: int
    hero_id: int
    hero_name: str
    is_pick: bool
    team: int = 0


class DraftExtractor:
    """Detects hero picks and bans by polling ``CDOTAGamerulesProxy``.

    Hero names for picks are resolved by following the ``m_hSelectedHero``
    handle from ``CDOTA_PlayerResource`` to the hero entity class name, then
    converting the class name to an NPC name (e.g. ``CDOTA_Unit_Hero_Sven``
    → ``npc_dota_hero_sven``).  This matches the reference implementation and
    works for heroes not present in the bundled ``heroes.json``.

    Bans have no hero entity; their names are resolved from a live
    ``hero_id → npc_name`` map built from picked heroes, with the static
    ``heroes.json`` mapping as a final fallback.

    Attach to a ``ReplayParser`` before calling ``parse()``:

    Example:
        >>> extractor = DraftExtractor()
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> picks = [e for e in extractor.draft_events if e.is_pick]

    Attributes:
        draft_events: All detected ``DraftEvent`` objects in order of detection.
    """

    draft_events: list[DraftEvent]

    def __init__(self) -> None:
        self._parser: ReplayParser | None = None
        self._grp: Entity | None = None
        # Track which (is_pick, slot_index, hero_id) tuples have been emitted
        # to make processing idempotent across repeated entity updates.
        self._seen: set[tuple[bool, int, int]] = set()
        self.draft_events = []
        # Live hero_id → npc_name map built from hero entities at parse time.
        # Populated by _on_entity when CDOTA_PlayerResource provides handles.
        self._live_id_to_npc: dict[int, str] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register callbacks with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_entity(self._on_entity)

    def _resolve_name(self, hero_id: int) -> str:
        """Resolve a hero_id to an NPC name.

        Resolution order:
        1. Live map built from hero entity class names (most accurate; populated
           by ``_update_live_map`` once hero entities spawn in the game phase).
        2. ``heroes.json`` lookup with ``hero_id // 2`` — modern Dota 2 replays
           store ALL pick/ban IDs as ``api_id * 2`` in entity fields, so halving
           is always preferred over a direct lookup when the halved value resolves.
        3. Static ``heroes.json`` direct lookup — fallback for legacy replays.
        """
        if hero_id in self._live_id_to_npc:
            return self._live_id_to_npc[hero_id]
        half = hero_id // 2
        if half in _HERO_ID_TO_NPC:
            return _HERO_ID_TO_NPC[half]
        return _HERO_ID_TO_NPC.get(hero_id, "")

    def _update_live_map(self, pr: Entity) -> None:
        """Scan CDOTA_PlayerResource handles and update the live hero_id → npc map."""
        if self._parser is None or self._parser.entity_manager is None:
            return
        em = self._parser.entity_manager
        for i in range(_PICK_SLOTS):
            hid = pr.get_int32(f"m_vecPlayerTeamData.{i:04d}.m_nSelectedHeroID")
            if hid is None or hid <= 0 or hid in self._live_id_to_npc:
                continue
            handle = pr.get_uint32(f"m_vecPlayerTeamData.{i:04d}.m_hSelectedHero")
            if handle is None:
                continue
            hero_entity = em.find_by_handle(handle)
            if hero_entity is None:
                continue
            cls = hero_entity.get_class_name()
            if cls.startswith(_PREFIX):
                npc = _class_to_npc(cls)
                self._live_id_to_npc[hid] = npc

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()
        if cls == "CDOTA_PlayerResource" and not op.has(EntityOp.DELETED):
            self._update_live_map(entity)
            return
        if cls != "CDOTAGamerulesProxy":
            return
        if op.has(EntityOp.DELETED):
            self._grp = None
            return
        self._grp = entity
        self._check_draft(entity)

    def _check_draft(self, entity: Entity) -> None:
        tick = self._parser.tick if self._parser else 0
        active_team = entity.get_int32("m_pGameRules.m_iActiveTeam") or 0

        # Bans: m_pGameRules.m_BannedHeroes.0000-0013
        for i in range(_BAN_SLOTS):
            hero_id = entity.get_int32(f"m_pGameRules.m_BannedHeroes.{i:04d}")
            if hero_id is None or hero_id <= 0:
                continue
            key = (False, i, hero_id)
            if key in self._seen:
                continue
            self._seen.add(key)
            self.draft_events.append(
                DraftEvent(
                    tick=tick,
                    slot_index=i,
                    hero_id=hero_id,
                    hero_name=self._resolve_name(hero_id),
                    is_pick=False,
                    team=active_team,
                )
            )

        # Picks: m_pGameRules.m_SelectedHeroes.0000-0009
        for i in range(_PICK_SLOTS):
            hero_id = entity.get_int32(f"m_pGameRules.m_SelectedHeroes.{i:04d}")
            if hero_id is None or hero_id <= 0:
                continue
            key = (True, i, hero_id)
            if key in self._seen:
                continue
            self._seen.add(key)
            self.draft_events.append(
                DraftEvent(
                    tick=tick,
                    slot_index=i,
                    hero_id=hero_id,
                    hero_name=self._resolve_name(hero_id),
                    is_pick=True,
                    team=active_team,
                )
            )

    def finalize(self) -> None:
        """Re-resolve all hero names using the fully-populated live map.

        During the draft phase hero entities have not yet spawned, so picks are
        recorded with whatever the static fallback yields — which may be wrong
        (e.g. direct-ID lookup returns ``kotl`` when the correct hero is
        ``pugna`` because the replay stores ``api_id * 2``).  Call this after
        ``parser.parse()`` completes so that the live map (populated once hero
        entities appear) takes priority and corrects any mismatches.
        """
        for event in self.draft_events:
            resolved = self._resolve_name(event.hero_id)
            if resolved:
                event.hero_name = resolved
