"""Per-tick player statistics extractor for Dota 2 replays.

Polls hero entity state at configurable tick intervals and accumulates
snapshots for time-series analysis.

Reference: examples/extraction_demo.py, odota/parser src/main/java/opendota/Parse.java
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors._snapshots import (
    _HERO_CLASS_PREFIX,
    TEAM_RADIANT,
    PlayerStateSnapshot,
    PlayerTimeSeries,
    _build_hero_snapshot,
    _player_id_from_entity,
    _pos,
    _snapshot_hero,  # noqa: F401 — retained private compatibility import
    _snapshot_player_id,
    scan_player_resource,
    team_data_field,
)
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser
    from gem.state.string_table import StringTable

# ---------------------------------------------------------------------------
# Inventory constants
# ---------------------------------------------------------------------------

# Slots 0-5 = main inventory, 6-8 = backpack, 9-16 = stash
# Reference: odota/parser src/main/java/opendota/Parse.java getHeroItem() comment
_ITEM_SLOTS = 17  # total slots to scan (0-16) for ongoing inventory snapshots
# Starting-inventory synthesis scans only slots 0-7 (6 inventory + backpack 6-7),
# matching OpenDota's getHeroInventory (`for i < 8`, Parse.java:818). Stash 9-16
# and backpack slot 8 are NOT counted as starting purchases.
_STARTING_ITEM_SLOTS = 8

#: Last game second OpenDota samples into ``lane_pos`` (``e.time <= 600``).
LANE_WINDOW_S = 600
_ABILITY_SLOTS = 32  # m_hAbilities.0000-0031 per hero entity
_NULL_HANDLE = 0xFFFFFF  # empty slot sentinel

_CONTROLLER_FIELDS = FieldAccessPlan(("m_hAssignedHero",))
_ENTITY_NAME_FIELDS = FieldAccessPlan(
    ("m_pEntity.m_nameStringTableIndex", "m_pEntity.m_nameStringableIndex")
)
_ABILITY_ENTITY_FIELDS = FieldAccessPlan(
    ("m_pEntity.m_nameStringTableIndex", "m_pEntity.m_nameStringableIndex", "m_iLevel")
)
_PLAYER_RESOURCE_KDA_FIELDS = FieldAccessPlan(
    tuple(
        f"m_vecPlayerTeamData.{resource_idx:04d}.{field_name}"
        for resource_idx in range(30)
        for field_name in ("m_iKills", "m_iDeaths", "m_iAssists")
    )
)
_PLAYER_RESOURCE_HERO_FIELDS = FieldAccessPlan(
    tuple(
        f"m_vecPlayerTeamData.{resource_idx:04d}.{field_name}"
        for resource_idx in range(30)
        for field_name in ("m_hSelectedHero", "m_iLevel")
    )
)
_TEAM_DATA_FIELDS = FieldAccessPlan(
    tuple(
        team_data_field(team_slot, field_name)
        for team_slot in range(5)
        for field_name in (
            "m_iNetWorth",
            "m_iTotalEarnedGold",
            "m_iTotalEarnedXP",
            "m_iLastHitCount",
            "m_iDenyCount",
            "m_iReliableGold",
            "m_iUnreliableGold",
        )
    )
)
_TEAM_DATA_STRIDE = 7  # fields per team slot in _TEAM_DATA_FIELDS
_ABILITY_HANDLE_FIELDS = FieldAccessPlan(
    tuple(
        field_name
        for slot in range(_ABILITY_SLOTS)
        for field_name in (f"m_hAbilities.{slot:04d}", f"m_vecAbilities.{slot:04d}")
    )
)
_ITEM_HANDLE_FIELDS = FieldAccessPlan(tuple(f"m_hItems.{slot:04d}" for slot in range(_ITEM_SLOTS)))

__all__ = ["PlayerExtractor", "PlayerStateSnapshot", "PlayerTimeSeries"]


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class PlayerExtractor:
    """Polls hero entity state each tick and accumulates player snapshots.

    Attach to a ``ReplayParser`` before calling ``parse()``:

    Example:
        >>> extractor = PlayerExtractor(sample_interval=30)
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> ts = extractor.time_series(player_id=0)

    Attributes:
        snapshots: All collected ``PlayerStateSnapshot`` objects in
            chronological order.
    """

    snapshots: list[PlayerStateSnapshot]

    def __init__(self, sample_interval: int = 30, minute_snapshots: bool = True) -> None:
        """Initialise the extractor.

        Args:
            sample_interval: Minimum tick gap between successive snapshots.
                Default 30 ticks = 1 second at 30 ticks/sec, producing a
                dense per-second series suitable for smooth time-series and
                ML features. Pass a larger value (e.g. 150) for sparser
                sampling. The separate ``_min`` arrays always sample at exact
                60-second game-time boundaries regardless of this setting.
            minute_snapshots: If True, also record a snapshot at each
                game-minute boundary. When the parser exposes replay game
                time, boundaries use that OpenDota-compatible clock; otherwise
                they fall back to every 1800 ticks from game start.
                ``total_earned_gold_t`` / ``total_earned_xp_t`` align with
                OpenDota's cumulative gold/XP series; ``gold_t`` remains
                current unspent gold.
                Requires the parser to fire ``on_game_start``. Default True.
        """
        self._sample_interval = sample_interval
        self._minute_snapshots = minute_snapshots
        self._parser: ReplayParser | None = None
        self._last_sample: int = -sample_interval
        self._game_start_tick: int | None = None
        self._game_end_tick: int | None = None
        self._last_minute: int = -1  # last game-minute index sampled
        self._last_sample_check_tick: int | None = None
        # entity index → Entity (mutable reference; entity is updated in place)
        self._heroes: dict[int, Entity] = {}
        # Combat-log hero name → player slot (OpenDota's name_to_slot). Only a
        # player's own hero entity may claim its names, and entries are never
        # removed: enemy-hero illusions share the real hero's class but carry the
        # caster's player ID, so the most recently updated hero-class entity is
        # not a safe owner. See _register_hero_names.
        self._player_id_by_npc: dict[str, int] = {}
        # player slot → the hero entity that claimed its names (position fallback
        # when the player's hero handle cannot be resolved).
        self._named_heroes: dict[int, Entity] = {}
        # Hero class name → combat-log NPC aliases.
        self._hero_aliases_by_class: dict[str, tuple[str, str]] = {}
        # player_id → Entity (CDOTAPlayerController)
        self._controllers: dict[int, Entity] = {}
        # CDOTADataRadiant / CDOTADataDire entities (authoritative gold/LH/DN per team)
        self._data_radiant: Entity | None = None
        self._data_dire: Entity | None = None
        # player_id (0-9) → team slot (0-4) within CDOTADataRadiant/Dire
        # Read from CDOTA_PlayerResource.m_vecPlayerTeamData.%04d.m_iTeamSlot
        self._player_team_slot: dict[int, int] = {}
        # logical player_id (0-9) → CDOTA_PlayerResource array index. Usually the
        # identity map, but a coach occupies a resource row and shifts later
        # players, so PlayerResource reads must go through this remap. Rebuilt
        # whenever _player_resource refreshes. Mirrors OpenDota's validIndices.
        self._resource_index_by_id: dict[int, int] = {}
        # CDOTA_PlayerResource entity for slot lookups
        self._player_resource: Entity | None = None
        self.snapshots: list[PlayerStateSnapshot] = []
        self._minute_snaps: list[PlayerStateSnapshot] = []
        # player_id → (kills, deaths, assists) from server scoreboard at game end
        self.scoreboard: dict[int, tuple[int, int, int]] = {}
        # set of player_ids whose starting inventory has been emitted
        self._inventory_initialized: set[int] = set()
        # player_id → tick the starting inventory was read at
        self.first_snapshot_tick: dict[int, int] = {}
        # Starting inventory follows OpenDota's once-a-second interval when the
        # parser has tick-start callbacks; see _on_tick_start. Otherwise (and
        # while OpenDota's clock is unknown) the first dense snapshot emits it.
        self._tick_start_inventory = False
        self._next_interval_raw_s: int | None = None
        # Starting-item entries awaiting OpenDota's game-start anchor, with the
        # raw clock second they were read at.
        self._untimed_starting_items: list[tuple[CombatLogEntry, int]] = []
        # Hero positions at each OpenDota interval up to game time
        # LANE_WINDOW_S, as (player_id, game_time_s, world_x, world_y). OpenDota
        # builds lane_pos from these; see _on_tick_start.
        self.lane_samples: list[tuple[int, int, float, float]] = []
        # Samples read before OpenDota's game-start anchor, with raw seconds.
        self._untimed_lane_samples: list[tuple[int, int, float, float]] = []
        self._lane_window_closed = False
        # Running combat log totals per player — stamped into each snapshot.
        # These are monotonically increasing so diffs give per-window rates.
        self._total_hero_damage: dict[int, int] = {}
        self._total_hero_healing: dict[int, int] = {}
        self._total_deaths: dict[int, int] = {}
        self._total_stuns: dict[int, float] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register callbacks with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser._on_entity_filtered(
            self._on_entity,
            class_names=(
                "CDOTAGamerulesProxy",
                "CDOTAPlayerController",
                "CDOTADataRadiant",
                "CDOTA_DataRadiant",
                "CDOTADataDire",
                "CDOTA_DataDire",
                "CDOTA_PlayerResource",
            ),
            class_prefixes=(_HERO_CLASS_PREFIX,),
        )
        parser.on_combat_log_entry(self._on_combat_log_entry)
        if self._minute_snapshots:
            parser.on_game_start(self._on_game_start)
        parser.on_game_end(self._on_game_end)
        on_tick_start = getattr(parser, "on_tick_start", None)
        if callable(on_tick_start):
            self._tick_start_inventory = True
            on_tick_start(self._on_tick_start)

    def _on_tick_start(self, net_tick: int) -> None:
        """Follow OpenDota's once-a-second interval for inventories and lanes.

        OpenDota's ``@OnTickStart`` interval fires when its clock reaches
        ``nextInterval``, which starts at the first clock reading and advances
        one second per firing. At each firing it reads every hero from the
        entity table as it stood before this tick's deltas:

        - Starting items (slots 0-7) are written once per player, at the first
          firing where the hero resolves, stamped with the tick-start clock. A
          later read can differ: a support's observer and sentry wards merge
          into a dispenser.
        - The hero's position becomes a ``lane_pos`` sample while game time is at
          most :data:`LANE_WINDOW_S`, pre-horn seconds included.

        Reference: odota/parser src/main/java/opendota/Parse.java
        (``nextInterval``, ``isPlayerStartingItemsWritten``) and
        src/main/java/opendota/CreateParsedDataBlob.java ``handleInterval``.

        Args:
            net_tick: Decoded ``CNETMsg_Tick.tick`` value (unused).
        """
        if self._parser is None or (
            self._lane_window_closed
            and len(self._inventory_initialized) >= 10
            and not self._untimed_starting_items
        ):
            return
        start_s = getattr(self._parser, "opendota_start_s", None)
        if isinstance(start_s, int):
            self._time_buffered_reads(start_s)
        raw_s = getattr(self._parser, "opendota_tick_start_raw_s", None)
        if not isinstance(raw_s, int) or self._game_end_tick is not None:
            return
        if self._next_interval_raw_s is None:
            self._next_interval_raw_s = raw_s
        # OpenDota's interval waits only for PlayerResource (its `init`), not for
        # ten mapped players: a truncated replay or a custom match with fewer
        # players never maps all ten. Its other `init` condition, no player
        # waiting to be drafted, holds long before heroes exist.
        if raw_s < self._next_interval_raw_s or self._player_resource is None:
            return
        self._next_interval_raw_s += 1
        game_s = raw_s - start_s if isinstance(start_s, int) else None
        if game_s is not None and game_s > LANE_WINDOW_S:
            self._lane_window_closed = True
        tables = self._parser.string_tables
        entity_names = tables.get_by_name("EntityNames") if tables is not None else None
        tick = self._parser.tick
        # Key each hero by its own player ID, as the dense snapshots do. Until the
        # roster remap resolves, the PlayerResource fallback reads row
        # `player_id`, which a coach or an empty row can shift onto another
        # player's hero; keying by the hero keeps that from claiming this slot.
        for player_id, hero in sorted(self._select_heroes().items()):
            if not self._lane_window_closed:
                pos = _pos(hero)
                if pos is not None:
                    if game_s is not None:
                        self.lane_samples.append((player_id, game_s, pos[0], pos[1]))
                    else:
                        self._untimed_lane_samples.append((player_id, raw_s, pos[0], pos[1]))
            if player_id in self._inventory_initialized:
                continue
            npc_name = (
                _hero_npc_name(hero, entity_names) or self._hero_aliases(hero.get_class_name())[0]
            )
            for entry in self._diff_inventory(hero, player_id, npc_name, tick):
                if game_s is not None:
                    entry.game_time_s = game_s
                else:
                    self._untimed_starting_items.append((entry, raw_s))

    def _time_buffered_reads(self, start_s: int) -> None:
        """Shift reads taken before OpenDota's game-start anchor onto game time."""
        for entry, read_s in self._untimed_starting_items:
            entry.game_time_s = read_s - start_s
        self._untimed_starting_items.clear()
        if self._untimed_lane_samples:
            # OpenDota applies `time <= 600` after shifting, like live samples.
            buffered = [
                (player_id, read_s - start_s, x, y)
                for player_id, read_s, x, y in self._untimed_lane_samples
                if read_s - start_s <= LANE_WINDOW_S
            ]
            self.lane_samples[:0] = buffered
            self._untimed_lane_samples.clear()

    def _on_game_start(self, game_start_tick: int) -> None:
        self._game_start_tick = game_start_tick
        # Align the 150-tick sampler to game start so both series share origin
        self._last_sample = game_start_tick
        # The first relevant entity in this tick can arrive before the parser's
        # gamerules callback establishes game time. Preserve the minute-zero
        # snapshot here while ordinary eligibility checks remain once per tick.
        game_time_s = getattr(self._parser, "game_time_s", None)
        if game_time_s == 0 and self._last_sample_check_tick == game_start_tick:
            self._maybe_sample_minute(game_start_tick)
        elif game_time_s is None:
            # Compatibility parsers without a game-time clock establish minute
            # zero from the next relevant entity callback, as before.
            self._last_sample_check_tick = None

    def _on_game_end(self, tick: int) -> None:
        # Force a final snapshot at the exact game-end tick so lh/nw/gold
        # match OpenDota's end-of-game values (sampled at postGame boundary).
        self._game_end_tick = tick
        self._sample(tick, minute=False)
        # Read authoritative kills/deaths/assists from the server scoreboard.
        # Reference: odota/parser src/main/java/opendota/Parse.java lines 666-668
        # m_vecPlayerTeamData.%04d.m_iKills/Deaths/Assists on CDOTA_PlayerResource.
        pr = self._player_resource
        if pr is not None:
            fields = pr._resolve_fields(_PLAYER_RESOURCE_KDA_FIELDS)
            for player_id in range(10):
                # Read at the resource-array index for this logical slot — a coach
                # shifts the array so index != slot. Reference: Parse.java
                # validIndices.
                offset = self._resource_index(player_id) * 3
                k = pr._get_int32_resolved(fields[offset])
                d = pr._get_int32_resolved(fields[offset + 1])
                a = pr._get_int32_resolved(fields[offset + 2])
                if k is not None or d is not None or a is not None:
                    self.scoreboard[player_id] = (k or 0, d or 0, a or 0)

    def _on_combat_log_entry(self, entry: CombatLogEntry) -> None:
        """Accumulate per-player running totals from combat log entries.

        Updates monotonically increasing counters for hero damage dealt,
        healing dealt, deaths, and stun duration.  Called for every combat log
        entry; irrelevant entry types are ignored cheaply.

        Hero damage/healing is credited to the damage *source*
        (``damage_source_name``), falling back to ``attacker_name`` when the
        source is empty — matching ``_CombatAggregator``'s attribution so the
        per-minute ``total_hero_damage_t``/``total_hero_healing_t`` curves stay
        consistent with the ``hero_damage``/``hero_healing`` scalars (a hero's
        spell/projectile damage lands on the hero, not the projectile).

        Args:
            entry: The incoming combat log entry.
        """
        if entry.log_type == "DAMAGE" and entry.target_is_hero and not entry.target_is_illusion:
            pid = self._source_to_pid(entry)
            if pid is not None:
                self._total_hero_damage[pid] = self._total_hero_damage.get(pid, 0) + entry.value

        elif (
            entry.log_type == "HEAL"
            and entry.target_is_hero
            and not entry.target_is_illusion
            # Exclude self-heal — total_hero_healing tracks healing to *allied*
            # heroes, matching the aggregator's hero_healing scalar.
            and entry.target_name != (entry.damage_source_name or entry.attacker_name)
        ):
            pid = self._source_to_pid(entry)
            if pid is not None:
                self._total_hero_healing[pid] = self._total_hero_healing.get(pid, 0) + entry.value

        elif (
            entry.log_type == "DEATH"
            and entry.target_is_hero
            # Skip reincarnation/aegis trigger deaths — the hero comes back, so the
            # trigger is not a real death. The subsequent true death (will_
            # reincarnate=False) is counted. Without this the cumulative death
            # curve double-counts WK/Aegis deaths. Reference: OpenDota
            # handleDeathCombat returns early for the aegis/reincarnation death.
            and not entry.will_reincarnate
        ):
            pid = self._hero_to_pid(entry.target_name)
            if pid is not None:
                self._total_deaths[pid] = self._total_deaths.get(pid, 0) + 1

        if entry.stun_duration > 0 and entry.attacker_is_hero:
            pid = self._hero_to_pid(entry.attacker_name)
            if pid is not None:
                self._total_stuns[pid] = self._total_stuns.get(pid, 0.0) + entry.stun_duration

    def _hero_to_pid(self, npc_name: str) -> int | None:
        """Resolve an NPC hero name to a player slot (0-9).

        Args:
            npc_name: Hero NPC name as it appears in the combat log, e.g.
                ``"npc_dota_hero_axe"``.

        Returns:
            Player slot 0-9, or ``None`` if the hero is not tracked.
        """
        return self._player_id_by_npc.get(npc_name.lower())

    def _source_to_pid(self, entry: CombatLogEntry) -> int | None:
        """Resolve the damage/heal *source* hero of a combat log entry to a slot.

        Prefers ``damage_source_name`` (so a hero's spell/projectile damage lands
        on the hero), falling back to ``attacker_name`` when the source name is
        empty. Mirrors ``_CombatAggregator``'s attribution.

        Args:
            entry: The combat log entry.

        Returns:
            Player slot 0-9, or ``None`` if the source is not a tracked hero.
        """
        source_name = entry.damage_source_name or entry.attacker_name
        if not source_name:
            return None
        return self._hero_to_pid(source_name)

    def hero_pos(self, npc_name: str) -> tuple[float, float] | None:
        """Return the current world position of a hero by NPC name.

        Args:
            npc_name: NPC hero name, e.g. ``"npc_dota_hero_axe"``.

        Returns:
            ``(x, y)`` world coordinates, or ``None`` if the hero is not tracked.
        """
        pid = self._player_id_by_npc.get(npc_name.lower())
        if pid is None:
            return None
        entity = self._canonical_hero_entity(pid) or self._named_heroes.get(pid)
        return _pos(entity) if entity is not None else None

    def time_series(self, player_id: int) -> PlayerTimeSeries:
        """Aggregate snapshots for one player into time-series lists.

        Args:
            player_id: Player slot (0-9).

        Returns:
            A ``PlayerTimeSeries`` with parallel lists indexed by sample number.
        """
        ts = PlayerTimeSeries(player_id=player_id)
        for snap in self.snapshots:
            if snap.player_id != player_id:
                continue
            ts.ticks.append(snap.tick)
            ts.gold_t.append(snap.gold)
            ts.total_earned_gold_t.append(snap.total_earned_gold)
            ts.total_earned_xp_t.append(snap.total_earned_xp)
            ts.net_worth_t.append(snap.net_worth)
            ts.lh_t.append(snap.lh)
            ts.dn_t.append(snap.dn)
            ts.xp_t.append(snap.xp)
            ts.hp_t.append(snap.hp)
            ts.mana_t.append(snap.mana)
            ts.x_t.append(snap.x)
            ts.y_t.append(snap.y)
            ts.total_hero_damage_t.append(snap.total_hero_damage)
            ts.total_hero_healing_t.append(snap.total_hero_healing)
            ts.total_deaths_t.append(snap.total_deaths)
            ts.total_stuns_t.append(snap.total_stuns)
        return ts

    def minute_time_series(self, player_id: int) -> PlayerTimeSeries:
        """Aggregate per-minute snapshots for one player into time-series lists.

        Returns a ``PlayerTimeSeries`` sampled at each game-minute boundary
        (every 1800 ticks from game start). ``total_earned_gold_t`` /
        ``total_earned_xp_t`` match OpenDota's cumulative gold/XP semantics;
        ``gold_t`` remains current unspent gold. ``game_times_s`` is the
        authoritative parallel game-relative axis (``0, 60, 120, ...``).

        Only populated when ``minute_snapshots=True`` (the default) and the
        parser fires the game-start event.

        Args:
            player_id: Player slot (0-9).

        Returns:
            A ``PlayerTimeSeries`` with one entry per game minute.
        """
        # Deduplicate by game minute — keep the last snap per minute index.
        # Duplicates arise when on_game_end fires within the same minute as a
        # regular boundary sample, or when entity callbacks fire multiple times
        # at the same tick. Using a dict keyed by minute ensures one entry per
        # minute, with the latest (most accurate) value winning.
        seen: dict[int, PlayerStateSnapshot] = {}  # minute_index → snap
        for i, snap in enumerate(s for s in self._minute_snaps if s.player_id == player_id):
            if snap.game_time_s is not None and snap.game_time_s >= 0:
                minute = snap.game_time_s // 60
            elif self._game_start_tick is not None:
                minute = (snap.tick - self._game_start_tick) // 1800
            else:
                minute = i
            seen[minute] = snap

        ts = PlayerTimeSeries(player_id=player_id)
        for snap in (seen[k] for k in sorted(seen)):
            ts.ticks.append(snap.tick)
            # ``seen`` is keyed by the authoritative game-minute index. Preserve
            # that axis explicitly instead of asking consumers to reconstruct it
            # from absolute replay ticks (whose origin differs across replays).
            if snap.game_time_s is not None and snap.game_time_s >= 0:
                ts.game_times_s.append((snap.game_time_s // 60) * 60)
            elif self._game_start_tick is not None:
                ts.game_times_s.append(max(0, (snap.tick - self._game_start_tick) // 1800) * 60)
            else:
                ts.game_times_s.append(len(ts.game_times_s) * 60)
            ts.gold_t.append(snap.gold)
            ts.total_earned_gold_t.append(snap.total_earned_gold)
            ts.total_earned_xp_t.append(snap.total_earned_xp)
            ts.net_worth_t.append(snap.net_worth)
            ts.lh_t.append(snap.lh)
            ts.dn_t.append(snap.dn)
            ts.xp_t.append(snap.xp)
            ts.hp_t.append(snap.hp)
            ts.mana_t.append(snap.mana)
            ts.x_t.append(snap.x)
            ts.y_t.append(snap.y)
            ts.total_hero_damage_t.append(snap.total_hero_damage)
            ts.total_hero_healing_t.append(snap.total_hero_healing)
            ts.total_deaths_t.append(snap.total_deaths)
            ts.total_stuns_t.append(snap.total_stuns)
        return ts

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()
        should_sample = False

        if cls == "CDOTAGamerulesProxy":
            if not op.has(EntityOp.DELETED):
                should_sample = True

        elif cls.startswith(_HERO_CLASS_PREFIX):
            idx = entity.get_index()
            if op.has(EntityOp.DELETED):
                self._remove_hero(entity)
            else:
                previous = self._heroes.get(idx)
                if previous is not None and previous.get_serial() != entity.get_serial():
                    self._remove_hero(previous)
                self._heroes[idx] = entity
                self._register_hero_names(entity, cls)
                should_sample = True

        elif cls == "CDOTAPlayerController":
            pid = _player_id_from_entity(entity)
            if pid is not None:
                if op.has(EntityOp.DELETED):
                    self._controllers.pop(pid, None)
                else:
                    self._controllers[pid] = entity
                    should_sample = True

        elif cls in ("CDOTADataRadiant", "CDOTA_DataRadiant"):
            self._data_radiant = None if op.has(EntityOp.DELETED) else entity
            if not op.has(EntityOp.DELETED):
                should_sample = True

        elif cls in ("CDOTADataDire", "CDOTA_DataDire"):
            self._data_dire = None if op.has(EntityOp.DELETED) else entity
            if not op.has(EntityOp.DELETED):
                should_sample = True

        elif cls == "CDOTA_PlayerResource":
            if op.has(EntityOp.DELETED):
                self._player_resource = None
            else:
                self._player_resource = entity
                self._refresh_team_slots()
                should_sample = True

        if should_sample and self._parser is not None:
            tick = self._parser.tick
            if tick != self._last_sample_check_tick:
                self._last_sample_check_tick = tick
                self._maybe_sample()

    def _hero_aliases(self, class_name: str) -> tuple[str, str]:
        """Return cached combat-log aliases for a hero entity class."""
        cached = self._hero_aliases_by_class.get(class_name)
        if cached is not None:
            return cached

        ending = class_name[len(_HERO_CLASS_PREFIX) :]
        # Register two name forms to cover inconsistent combat log names.
        # Reference: odota/parser src/main/java/opendota/Parse.java
        aliases = (
            "npc_dota_hero_" + ending.lower(),
            "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", ending.replace("_", "")).lower(),
        )
        self._hero_aliases_by_class[class_name] = aliases
        return aliases

    def _register_hero_names(self, entity: Entity, class_name: str) -> None:
        """Map a hero entity's combat-log names to its player, if it owns them.

        Mirrors OpenDota's ``name_to_slot``, which is filled only from each
        player's selected-hero handle and never cleared. Enemy-hero illusions
        (Dark Seer's Wall of Replica, Shadow Demon's Disruption, Morphling's
        Replicate) are ``CDOTA_Unit_Hero_<Target>`` entities carrying the
        *caster's* player ID, so accepting any hero-class entity would hand the
        target hero's combat-log entries to the caster. Once the player's hero
        handle is known, only that entity may claim names; before then, an
        entity may claim only names nobody holds yet.

        Reference: odota/parser src/main/java/opendota/Parse.java
        (``name_to_slot`` from ``m_hSelectedHero``).
        """
        player_id = _player_id_from_entity(entity)
        if player_id is None:
            return
        npc1, npc2 = self._hero_aliases(class_name)
        already_named = self._player_id_by_npc.get(npc1) == player_id
        if already_named and self._named_heroes.get(player_id) is entity:
            return

        handle = self._hero_handle_for_player(player_id)
        if handle is not None:
            em = self._parser.entity_manager if self._parser is not None else None
            if em is None or em.find_by_handle(handle) is not entity:
                return
        elif npc1 in self._player_id_by_npc or npc2 in self._player_id_by_npc:
            return

        self._player_id_by_npc[npc1] = player_id
        self._player_id_by_npc[npc2] = player_id
        self._named_heroes[player_id] = entity

    def _remove_hero(self, entity: Entity) -> None:
        """Forget a hero entity only when the slot still holds this identity.

        Combat-log names stay mapped: OpenDota never removes ``name_to_slot``
        entries, and a deleted illusion must not orphan the real hero's name.
        """
        idx = entity.get_index()
        current = self._heroes.get(idx)
        if current is None or current.get_serial() != entity.get_serial():
            return

        self._heroes.pop(idx, None)

    def _refresh_team_slots(self) -> None:
        """Build the logical→resource remap and read m_iTeamSlot per player.

        OpenDota scans ``CDOTA_PlayerResource`` for rows whose team is Radiant or
        Dire (a coach has team 1/14 and is skipped), then uses the scan order as
        logical slot ``0..9``. The resource array index is not always the logical
        slot, so all PlayerResource reads go through ``_resource_index_by_id``.
        Reference: odota/parser Parse.java (validIndices).
        """
        pr = self._player_resource
        if pr is None:
            return

        scan = scan_player_resource(pr)
        # Keep team slots current even on a partial scan (matches prior behaviour).
        self._player_team_slot.update(scan.team_slot_by_id)

        # Only adopt the remap once it resolves all 10 players; partial scans
        # (early in the replay, before PlayerResource is fully populated) keep the
        # previous mapping rather than introducing a half-built shift.
        if scan.resolved:
            self._resource_index_by_id = scan.index_by_id

    def _resource_index(self, player_id: int) -> int:
        """Map a logical player slot to its CDOTA_PlayerResource array index.

        Falls back to the identity (``player_id``) until the remap is built —
        correct for the common no-coach case where they coincide.

        Args:
            player_id: Logical player slot 0-9.

        Returns:
            The resource-array index to read PlayerResource fields at.
        """
        return self._resource_index_by_id.get(player_id, player_id)

    def _maybe_sample(self) -> None:
        if self._parser is None:
            return
        tick = self._parser.tick
        if self._game_end_tick is not None and tick >= self._game_end_tick:
            return

        # Minute-boundary sampling (OpenDota-aligned)
        minute_fired = self._maybe_sample_minute(tick)

        # Regular interval sampling — skip if minute boundary just fired at same tick
        if tick - self._last_sample >= self._sample_interval:
            self._last_sample = tick
            if not minute_fired:
                self._sample(tick, minute=False)

    def _maybe_sample_minute(self, tick: int) -> bool:
        """Sample a newly reached minute boundary and report whether it fired."""
        if self._minute_snapshots and self._game_start_tick is not None:
            game_time_s = getattr(self._parser, "game_time_s", None)
            if game_time_s is not None and game_time_s >= 0 and game_time_s % 60 == 0:
                current_minute = game_time_s // 60
            elif game_time_s is not None:
                current_minute = None
            else:
                elapsed = tick - self._game_start_tick
                current_minute = elapsed // 1800 if elapsed >= 0 else None

            if current_minute is not None and current_minute > self._last_minute:
                self._last_minute = current_minute
                self._sample(tick, minute=True)
                return True
        return False

    def _hero_handle_for_player(self, player_id: int) -> int | None:
        ctrl = self._controllers.get(player_id)
        if ctrl is not None:
            assigned_hero = ctrl._resolve_fields(_CONTROLLER_FIELDS)[0]
            handle = ctrl._get_uint32_resolved(assigned_hero)
            if handle is not None and handle != _NULL_HANDLE:
                return handle
        pr = self._player_resource
        if pr is None:
            return None
        fields = pr._resolve_fields(_PLAYER_RESOURCE_HERO_FIELDS)
        offset = self._resource_index(player_id) * 2
        handle = pr._get_uint32_resolved(fields[offset])
        if handle is None or handle == _NULL_HANDLE:
            return None
        return handle

    def _canonical_hero_entity(self, player_id: int) -> Entity | None:
        if self._parser is None or self._parser.entity_manager is None:
            return None
        handle = self._hero_handle_for_player(player_id)
        if handle is None:
            return None
        entity = self._parser.entity_manager.find_by_handle(handle)
        if entity is None or not entity.get_class_name().startswith(_HERO_CLASS_PREFIX):
            return None
        return entity

    def _select_heroes(self) -> dict[int, Entity]:
        """Return each player's hero entity, keyed by the hero's own player ID.

        Canonical heroes (controller or PlayerResource handle) come first; the
        last one to claim an ID wins. Tracked hero entities fill in players no
        canonical hero claimed, first by entity index.
        """
        selected: dict[int, Entity] = {}
        for player_id in range(10):
            entity = self._canonical_hero_entity(player_id)
            if entity is None:
                continue
            resolved_id = _snapshot_player_id(entity)
            if resolved_id is not None:
                selected[resolved_id] = entity
        for _, entity in sorted(self._heroes.items()):
            resolved_id = _snapshot_player_id(entity)
            if resolved_id is not None and resolved_id not in selected:
                selected[resolved_id] = entity
        return selected

    def _sample(self, tick: int, minute: bool = False) -> None:
        entity_names = (
            self._parser.string_tables.get_by_name("EntityNames")
            if self._parser is not None and self._parser.string_tables is not None
            else None
        )
        # Finish selection before constructing full snapshots, preserving the
        # last canonical / first fallback winner and staging before overlays.
        selected = self._select_heroes()
        snaps_by_player: dict[int, tuple[Entity, PlayerStateSnapshot]] = {}
        for player_id, entity in selected.items():
            snap = _build_hero_snapshot(entity, tick, player_id)
            snap.game_time_s = getattr(self._parser, "game_time_s", None)
            snaps_by_player[player_id] = (entity, snap)
        for player_id in sorted(snaps_by_player):
            entity, snap = snaps_by_player[player_id]
            # Resolve canonical NPC name from the EntityNames string table so that
            # heroes like QueenOfPain (class "CDOTA_Unit_Hero_QueenOfPain") map to
            # "npc_dota_hero_queenofpain" rather than "npc_dota_hero_queen_of_pain".
            # The camelCase→snake_case conversion in _snapshot_hero inserts word
            # boundaries at every capital letter, which is wrong for compound names.
            npc_name = _hero_npc_name(entity, entity_names)
            if npc_name is not None:
                snap.npc_name = npc_name
            # Overlay per-player economy stats from CDOTA_DataRadiant/Dire. Mind
            # which gold is which:
            #
            #   m_iTotalEarnedGold — monotonically increasing gold earned across
            #     the whole game. Use this for radiant_gold_adv, NOT current
            #     gold, which drops on every purchase.
            #
            #   m_iReliableGold + m_iUnreliableGold — current unspent gold. The
            #     sum matches the postgame summary's per-player gold.
            #
            #   m_iTotalEarnedXP — monotonically increasing XP earned across the
            #     whole game. Use this for radiant_xp_adv, NOT m_iCurrentXP from
            #     the hero entity which resets to 0 on each level-up.
            #
            # Reference: odota/parser Parse.java — getEntityProperty(dataTeam,
            #   "m_vecDataTeam.%i.m_iTotalEarnedGold/XP", teamSlot)
            data_entity = self._data_radiant if snap.team == TEAM_RADIANT else self._data_dire
            if data_entity is not None:
                # Prefer authoritative team slot; fall back to pid % 5
                team_slot = self._player_team_slot.get(snap.player_id, snap.player_id % 5)
                data_fields = data_entity._resolve_fields(_TEAM_DATA_FIELDS)
                offset = team_slot * _TEAM_DATA_STRIDE
                nw = data_entity._get_int32_resolved(data_fields[offset])
                if nw is not None and nw > 0:
                    snap.net_worth = nw
                teg = data_entity._get_int32_resolved(data_fields[offset + 1])
                if teg is not None and teg > 0:
                    snap.total_earned_gold = teg
                tex = data_entity._get_int32_resolved(data_fields[offset + 2])
                if tex is not None and tex > 0:
                    snap.total_earned_xp = tex
                lh = data_entity._get_int32_resolved(data_fields[offset + 3])
                if lh is not None and lh > 0:
                    snap.lh = lh
                dn = data_entity._get_int32_resolved(data_fields[offset + 4])
                if dn is not None and dn > 0:
                    snap.dn = dn
                reliable = data_entity._get_int32_resolved(data_fields[offset + 5])
                unreliable = data_entity._get_int32_resolved(data_fields[offset + 6])
                if reliable is not None or unreliable is not None:
                    snap.gold = (reliable or 0) + (unreliable or 0)
            # Overlay authoritative hero level from CDOTA_PlayerResource
            # (m_vecPlayerTeamData.%i.m_iLevel) — the hero entity's
            # m_nCurrentLevel reads 0 in some replays. Mirrors OpenDota's
            # Parse.java level read. Use the coach-aware resource index.
            pr = self._player_resource
            if pr is not None:
                resource_fields = pr._resolve_fields(_PLAYER_RESOURCE_HERO_FIELDS)
                offset = self._resource_index(snap.player_id) * 2
                lvl = pr._get_int32_resolved(resource_fields[offset + 1])
                if lvl is not None and lvl > 0:
                    snap.level = lvl
            snap.ability_levels = self._read_abilities(entity)
            pid = snap.player_id
            snap.total_hero_damage = self._total_hero_damage.get(pid, 0)
            snap.total_hero_healing = self._total_hero_healing.get(pid, 0)
            snap.total_deaths = self._total_deaths.get(pid, 0)
            snap.total_stuns = self._total_stuns.get(pid, 0.0)
            if minute:
                self._minute_snaps.append(snap)
            else:
                # Dense series only: capture current inventory. The last dense
                # sample yields end-of-game inventory (read in assembly.py).
                snap.items = self._read_inventory(entity)
                self.snapshots.append(snap)
                if not self._tick_start_inventory or (
                    getattr(self._parser, "opendota_tick_start_raw_s", None) is None
                ):
                    self._diff_inventory(entity, snap.player_id, snap.npc_name, tick)

    def _read_abilities(self, hero: Entity) -> dict[str, int]:
        """Read current ability names and levels from a hero entity.

        Iterates ``m_hAbilities.0000``–``m_hAbilities.0031``, falling back to
        ``m_vecAbilities.*`` for older replays. Resolves each handle to an
        ability entity and reads ``m_iLevel``. Ability names come from the
        ``EntityNames`` string table.

        Args:
            hero: The hero entity to read from.

        Returns:
            Mapping of ability name → level for all abilities with level > 0.
        """
        if self._parser is None:
            return {}
        em = self._parser.entity_manager
        if em is None:
            return {}
        entity_names = (
            self._parser.string_tables.get_by_name("EntityNames")
            if self._parser.string_tables is not None
            else None
        )
        if entity_names is None:
            return {}

        result: dict[str, int] = {}
        handle_fields = hero._resolve_fields(_ABILITY_HANDLE_FIELDS)
        for slot in range(_ABILITY_SLOTS):
            offset = slot * 2
            handle = hero._get_uint32_resolved(handle_fields[offset])
            if handle is None:
                handle = hero._get_uint32_resolved(handle_fields[offset + 1])
            if handle is None or handle == _NULL_HANDLE:
                continue
            ability_entity = em.find_by_handle(handle)
            if ability_entity is None:
                continue
            ability_fields = ability_entity._resolve_fields(_ABILITY_ENTITY_FIELDS)
            name_idx = ability_entity._get_int32_resolved(ability_fields[0])
            if name_idx is None:
                name_idx = ability_entity._get_int32_resolved(ability_fields[1])
            if name_idx is None or name_idx < 0:
                continue
            item = entity_names.items.get(name_idx)
            if item is None:
                continue
            name = item[0] if isinstance(item, tuple) else str(item)
            if not name:
                continue
            level = ability_entity._get_int32_resolved(ability_fields[2]) or 0
            if level > 0:
                result[name] = level
        return result

    def _read_inventory(self, hero: Entity) -> dict[int, str]:
        """Read current item names from a hero entity's item slots.

        Reads ``m_hItems.0000``–``m_hItems.{_ITEM_SLOTS-1:04d}``, resolving each
        handle via the entity manager and looking up the item name from the
        ``EntityNames`` string table.

        Args:
            hero: The hero entity to read from.

        Returns:
            Mapping of slot index → item name for all occupied slots.
        """
        if self._parser is None:
            return {}
        em = self._parser.entity_manager
        if em is None:
            return {}
        entity_names = self._parser.string_tables.get_by_name("EntityNames")
        if entity_names is None:
            return {}

        result: dict[int, str] = {}
        handle_fields = hero._resolve_fields(_ITEM_HANDLE_FIELDS)
        for slot in range(_ITEM_SLOTS):
            handle = hero._get_uint32_resolved(handle_fields[slot])
            if handle is None or handle == _NULL_HANDLE:
                continue
            item_entity = em.find_by_handle(handle)
            if item_entity is None:
                continue
            # Newer replays use m_nameStringTableIndex; older ones use
            # m_nameStringableIndex. Try both, mirroring _read_abilities.
            name_fields = item_entity._resolve_fields(_ENTITY_NAME_FIELDS)
            name_idx = item_entity._get_int32_resolved(name_fields[0])
            if name_idx is None:
                name_idx = item_entity._get_int32_resolved(name_fields[1])
            if name_idx is None or name_idx < 0:
                continue
            # EntityNames items are stored as (key_str, value_bytes); key_str is the name
            item = entity_names.items.get(name_idx)
            if item is None:
                continue
            name = item[0] if isinstance(item, tuple) else str(item)
            if name:
                result[slot] = name
        return result

    def _diff_inventory(
        self, hero: Entity, player_id: int, npc_name: str, tick: int
    ) -> list[CombatLogEntry]:
        """Emit synthetic PURCHASE entries for a player's starting inventory.

        Called once per player, when its starting inventory is read. Emits a
        ``PURCHASE`` ``CombatLogEntry`` for each occupied item slot, filling the
        gap before the combat log stream begins recording.

        Args:
            hero: The hero entity.
            player_id: Player slot (0-9).
            npc_name: Hero NPC name for the combat log entry.
            tick: Current game tick.

        Returns:
            The emitted entries; empty if the inventory was already emitted.
        """
        if self._parser is None or player_id in self._inventory_initialized:
            return []
        current = self._read_inventory(hero)

        # Emit all current items as starting inventory. Later purchases are
        # covered by DOTA_COMBATLOG_PURCHASE events.
        # Reference: odota/parser Parse.java isPlayerStartingItemsWritten pattern
        self._inventory_initialized.add(player_id)
        self.first_snapshot_tick[player_id] = tick
        # Only slots 0-7 count as starting inventory (OpenDota getHeroInventory
        # scans `i < 8`); stash 9-16 and backpack slot 8 are excluded so they
        # are not miscounted as starting purchases. One entry per occupied slot
        # preserves per-unit copies (e.g. 2x branches), which OpenDota keeps.
        emitted: list[CombatLogEntry] = []
        for slot, item_name in current.items():
            if slot >= _STARTING_ITEM_SLOTS:
                continue
            if item_name and not item_name.startswith("item_recipe"):
                entry = CombatLogEntry(
                    tick=tick,
                    log_type=CombatLogType.PURCHASE,
                    target_name=npc_name,
                    value_name=item_name,
                )
                self._parser.combat_log._emit(entry)
                emitted.append(entry)
        return emitted


def _hero_npc_name(hero: Entity, entity_names: StringTable | None) -> str | None:
    """Return a hero entity's NPC name from the ``EntityNames`` string table.

    Class names are ambiguous for compound heroes: ``CDOTA_Unit_Hero_QueenOfPain``
    is ``npc_dota_hero_queenofpain``, not ``npc_dota_hero_queen_of_pain``.
    Current replays use ``m_nameStringTableIndex``; older ones
    ``m_nameStringableIndex``. Reference: odota/parser Parse.java
    ``getAbilityEntityStringTableIndex`` (same order).

    Args:
        hero: The hero entity.
        entity_names: The ``EntityNames`` string table, if loaded.

    Returns:
        The NPC name, or ``None`` when it cannot be resolved.
    """
    if entity_names is None:
        return None
    name_fields = hero._resolve_fields(_ENTITY_NAME_FIELDS)
    name_idx = hero._get_int32_resolved(name_fields[0])
    if name_idx is None:
        name_idx = hero._get_int32_resolved(name_fields[1])
    if name_idx is None or name_idx < 0:
        return None
    item = entity_names.items.get(name_idx)
    return item[0] if item is not None else None
