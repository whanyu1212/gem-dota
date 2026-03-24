"""Per-tick player statistics extractor for Dota 2 replays.

Polls hero entity state at configurable tick intervals and accumulates
snapshots for time-series analysis.

Reference: examples/extraction_demo.py, refs/parser/src/main/java/opendota/Parse.java
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from gem.combatlog import CombatLogEntry
from gem.entities import Entity, EntityOp
from gem.extractors._snapshots import (
    _HERO_CLASS_PREFIX,
    PlayerStateSnapshot,
    PlayerTimeSeries,
    _pos,
    _snapshot_hero,
)

if TYPE_CHECKING:
    from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Inventory constants
# ---------------------------------------------------------------------------

# Slots 0-5 = main inventory, 6-8 = backpack, 9-16 = stash
# Reference: refs/parser/src/main/java/opendota/Parse.java getHeroItem() comment
_ITEM_SLOTS = 17  # total slots to scan (0-16)
_ABILITY_SLOTS = 32  # m_hAbilities.0000-0031 per hero entity
_NULL_HANDLE = 0xFFFFFF  # empty slot sentinel

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_TEAM_RADIANT = 2
_TEAM_DIRE = 3

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
                game-minute boundary (every 1800 ticks from game start),
                matching OpenDota's minute cadence. ``total_earned_gold_t`` /
                ``total_earned_xp_t`` align with OpenDota's cumulative gold/XP
                series; ``gold_t`` remains current unspent gold.
                Requires the parser to fire ``on_game_start``. Default True.
        """
        self._sample_interval = sample_interval
        self._minute_snapshots = minute_snapshots
        self._parser: ReplayParser | None = None
        self._last_sample: int = -sample_interval
        self._game_start_tick: int | None = None
        self._game_end_tick: int | None = None
        self._last_minute: int = -1  # last game-minute index sampled
        # entity index → Entity (mutable reference; entity is updated in place)
        self._heroes: dict[int, Entity] = {}
        # npc_name → Entity (for external position lookups)
        self._heroes_by_npc: dict[str, Entity] = {}
        # player_id → Entity (CDOTAPlayerController)
        self._controllers: dict[int, Entity] = {}
        # CDOTADataRadiant / CDOTADataDire entities (authoritative gold/LH/DN per team)
        self._data_radiant: Entity | None = None
        self._data_dire: Entity | None = None
        # player_id (0-9) → team slot (0-4) within CDOTADataRadiant/Dire
        # Read from CDOTA_PlayerResource.m_vecPlayerTeamData.%04d.m_iTeamSlot
        self._player_team_slot: dict[int, int] = {}
        # CDOTA_PlayerResource entity for slot lookups
        self._player_resource: Entity | None = None
        self.snapshots: list[PlayerStateSnapshot] = []
        self._minute_snaps: list[PlayerStateSnapshot] = []
        # player_id → (kills, deaths, assists) from server scoreboard at game end
        self.scoreboard: dict[int, tuple[int, int, int]] = {}
        # set of player_ids whose starting inventory has been emitted
        self._inventory_initialized: set[int] = set()
        # player_id → tick of first inventory snapshot (used to suppress
        # duplicate combat log PURCHASE events for the same window)
        self.first_snapshot_tick: dict[int, int] = {}
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
        parser.on_entity(self._on_entity)
        parser.on_combat_log_entry(self._on_combat_log_entry)
        if self._minute_snapshots:
            parser.on_game_start(self._on_game_start)
        parser.on_game_end(self._on_game_end)

    def _on_game_start(self, game_start_tick: int) -> None:
        self._game_start_tick = game_start_tick
        # Align the 150-tick sampler to game start so both series share origin
        self._last_sample = game_start_tick

    def _on_game_end(self, tick: int) -> None:
        # Force a final snapshot at the exact game-end tick so lh/nw/gold
        # match OpenDota's end-of-game values (sampled at postGame boundary).
        self._game_end_tick = tick
        self._sample(tick, minute=False)
        # Read authoritative kills/deaths/assists from the server scoreboard.
        # Reference: refs/parser/src/main/java/opendota/Parse.java lines 666-668
        # m_vecPlayerTeamData.%04d.m_iKills/Deaths/Assists on CDOTA_PlayerResource.
        pr = self._player_resource
        if pr is not None:
            for i in range(10):
                prefix = f"m_vecPlayerTeamData.{i:04d}"
                k = pr.get_int32(f"{prefix}.m_iKills")
                d = pr.get_int32(f"{prefix}.m_iDeaths")
                a = pr.get_int32(f"{prefix}.m_iAssists")
                if k is not None or d is not None or a is not None:
                    self.scoreboard[i] = (k or 0, d or 0, a or 0)

    def _on_combat_log_entry(self, entry: CombatLogEntry) -> None:
        """Accumulate per-player running totals from combat log entries.

        Updates monotonically increasing counters for hero damage dealt,
        healing dealt, deaths, and stun duration.  Called for every combat log
        entry; irrelevant entry types are ignored cheaply.

        Args:
            entry: The incoming combat log entry.
        """
        if entry.log_type == "DAMAGE" and entry.attacker_is_hero and entry.target_is_hero:
            pid = self._hero_to_pid(entry.attacker_name)
            if pid is not None:
                self._total_hero_damage[pid] = self._total_hero_damage.get(pid, 0) + entry.value

        elif entry.log_type == "HEAL" and entry.attacker_is_hero and entry.target_is_hero:
            pid = self._hero_to_pid(entry.attacker_name)
            if pid is not None:
                self._total_hero_healing[pid] = self._total_hero_healing.get(pid, 0) + entry.value

        elif entry.log_type == "DEATH" and entry.target_is_hero:
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
        entity = self._heroes_by_npc.get(npc_name.lower())
        if entity is None:
            return None
        pid = entity.get_int32("m_nPlayerID")
        if pid is None:
            pid = entity.get_int32("m_iPlayerID")
        if pid is None or pid < 0:
            return None
        return pid // 2

    def hero_pos(self, npc_name: str) -> tuple[float, float] | None:
        """Return the current world position of a hero by NPC name.

        Args:
            npc_name: NPC hero name, e.g. ``"npc_dota_hero_axe"``.

        Returns:
            ``(x, y)`` world coordinates, or ``None`` if the hero is not tracked.
        """
        entity = self._heroes_by_npc.get(npc_name.lower())
        if entity is None:
            return None
        pid = entity.get_int32("m_nPlayerID")
        if pid is None:
            pid = entity.get_int32("m_iPlayerID")
        if pid is not None and pid >= 0:
            canonical = self._canonical_hero_entity(pid // 2)
            if canonical is not None:
                return _pos(canonical)
        return _pos(entity)

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
        ``gold_t`` remains current unspent gold.

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
        if self._game_start_tick is not None:
            for snap in self._minute_snaps:
                if snap.player_id != player_id:
                    continue
                minute = (snap.tick - self._game_start_tick) // 1800
                seen[minute] = snap
        else:
            for i, snap in enumerate(s for s in self._minute_snaps if s.player_id == player_id):
                seen[i] = snap

        ts = PlayerTimeSeries(player_id=player_id)
        for snap in (seen[k] for k in sorted(seen)):
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

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls.startswith(_HERO_CLASS_PREFIX):
            idx = entity.get_index()
            ending = cls[len(_HERO_CLASS_PREFIX) :]
            # Register two name forms to cover inconsistent combat log names.
            # "combatLogName":  simple lowercase ("npc_dota_hero_templarassassin")
            # "combatLogName2": insert _ before each capital ("npc_dota_hero_templar_assassin")
            # Reference: refs/parser/src/main/java/opendota/Parse.java
            npc1 = "npc_dota_hero_" + ending.lower()
            npc2 = "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", ending.replace("_", "")).lower()
            if op.has(EntityOp.DELETED):
                self._heroes.pop(idx, None)
                self._heroes_by_npc.pop(npc1, None)
                self._heroes_by_npc.pop(npc2, None)
            else:
                self._heroes[idx] = entity
                self._heroes_by_npc[npc1] = entity
                self._heroes_by_npc[npc2] = entity
                self._maybe_sample()

        elif cls == "CDOTAPlayerController":
            pid = entity.get_int32("m_nPlayerID")
            if pid is None:
                pid = entity.get_int32("m_iPlayerID")
            if pid is not None and pid >= 0:
                pid //= 2
                if op.has(EntityOp.DELETED):
                    self._controllers.pop(pid, None)
                else:
                    self._controllers[pid] = entity

        elif cls in ("CDOTADataRadiant", "CDOTA_DataRadiant"):
            self._data_radiant = None if op.has(EntityOp.DELETED) else entity

        elif cls in ("CDOTADataDire", "CDOTA_DataDire"):
            self._data_dire = None if op.has(EntityOp.DELETED) else entity

        elif cls == "CDOTA_PlayerResource":
            if op.has(EntityOp.DELETED):
                self._player_resource = None
            else:
                self._player_resource = entity
                self._refresh_team_slots()

    def _refresh_team_slots(self) -> None:
        """Read m_iTeamSlot for each player from CDOTA_PlayerResource."""
        pr = self._player_resource
        if pr is None:
            return
        for i in range(10):
            slot = pr.get_int32(f"m_vecPlayerTeamData.{i:04d}.m_iTeamSlot")
            if slot is not None and slot >= 0:
                self._player_team_slot[i] = slot

    def _maybe_sample(self) -> None:
        if self._parser is None:
            return
        tick = self._parser.tick
        if self._game_end_tick is not None and tick >= self._game_end_tick:
            return

        # Minute-boundary sampling (OpenDota-aligned)
        minute_fired = False
        if self._minute_snapshots and self._game_start_tick is not None:
            elapsed = tick - self._game_start_tick
            if elapsed >= 0:
                current_minute = elapsed // 1800
                if current_minute > self._last_minute:
                    self._last_minute = current_minute
                    self._sample(tick, minute=True)
                    minute_fired = True

        # Regular interval sampling — skip if minute boundary just fired at same tick
        if tick - self._last_sample >= self._sample_interval:
            self._last_sample = tick
            if not minute_fired:
                self._sample(tick, minute=False)

    def _hero_handle_for_player(self, player_id: int) -> int | None:
        ctrl = self._controllers.get(player_id)
        if ctrl is not None:
            handle = ctrl.get_uint32("m_hAssignedHero")
            if handle is not None and handle != _NULL_HANDLE:
                return handle
        pr = self._player_resource
        if pr is None:
            return None
        handle = pr.get_uint32(f"m_vecPlayerTeamData.{player_id:04d}.m_hSelectedHero")
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

    def _sample(self, tick: int, minute: bool = False) -> None:
        entity_names = (
            self._parser.string_tables.get_by_name("EntityNames")
            if self._parser is not None and self._parser.string_tables is not None
            else None
        )
        snaps_by_player: dict[int, tuple[Entity, PlayerStateSnapshot]] = {}
        for player_id in range(10):
            entity = self._canonical_hero_entity(player_id)
            if entity is None:
                continue
            snap = _snapshot_hero(entity, tick)
            if snap is not None:
                snaps_by_player[snap.player_id] = (entity, snap)
        for _, entity in sorted(self._heroes.items()):
            snap = _snapshot_hero(entity, tick)
            if snap is None or snap.player_id in snaps_by_player:
                continue
            snaps_by_player[snap.player_id] = (entity, snap)
        for player_id in sorted(snaps_by_player):
            entity, snap = snaps_by_player[player_id]
            # Resolve canonical NPC name from the EntityNames string table so that
            # heroes like QueenOfPain (class "CDOTA_Unit_Hero_QueenOfPain") map to
            # "npc_dota_hero_queenofpain" rather than "npc_dota_hero_queen_of_pain".
            # The camelCase→snake_case conversion in _snapshot_hero inserts word
            # boundaries at every capital letter, which is wrong for compound names.
            if entity_names is not None:
                name_idx = entity.get_int32("m_pEntity.m_nameStringableIndex")
                if name_idx is not None and name_idx >= 0:
                    item = entity_names.items.get(name_idx)
                    if item is not None:
                        snap.npc_name = item[0]
            # Overlay current unspent gold + net_worth from CDOTAPlayerController.
            # m_iGold = current cash on hand (goes up/down as player earns/spends).
            # m_iNetWorth = gold + item value (also on controller for convenience).
            ctrl = self._controllers.get(snap.player_id)
            if ctrl is not None:
                gold = ctrl.get_int32("m_iGold")
                nw = ctrl.get_int32("m_iNetWorth")
                if gold is not None:
                    snap.gold = gold
                if nw is not None:
                    snap.net_worth = nw
            # Overlay authoritative cumulative stats from CDOTA_DataRadiant/Dire.
            # These are the canonical sources for advantage curves — they differ
            # from the hero/controller fields in important ways:
            #
            #   m_iTotalEarnedGold — monotonically increasing gold earned across
            #     the whole game. Use this for radiant_gold_adv, NOT m_iGold
            #     (spendable cash) which resets when items are purchased.
            #
            #   m_iTotalEarnedXP — monotonically increasing XP earned across the
            #     whole game. Use this for radiant_xp_adv, NOT m_iCurrentXP from
            #     the hero entity which resets to 0 on each level-up.
            #
            # Reference: refs/parser/Parse.java — getEntityProperty(dataTeam,
            #   "m_vecDataTeam.%i.m_iTotalEarnedGold/XP", teamSlot)
            data_entity = self._data_radiant if snap.team == _TEAM_RADIANT else self._data_dire
            if data_entity is not None:
                # Prefer authoritative team slot; fall back to pid % 5
                team_slot = self._player_team_slot.get(snap.player_id, snap.player_id % 5)
                prefix = f"m_vecDataTeam.{team_slot:04d}"
                nw = data_entity.get_int32(f"{prefix}.m_iNetWorth")
                if nw is not None and nw > 0:
                    snap.net_worth = nw
                teg = data_entity.get_int32(f"{prefix}.m_iTotalEarnedGold")
                if teg is not None and teg > 0:
                    snap.total_earned_gold = teg
                tex = data_entity.get_int32(f"{prefix}.m_iTotalEarnedXP")
                if tex is not None and tex > 0:
                    snap.total_earned_xp = tex
                lh = data_entity.get_int32(f"{prefix}.m_iLastHitCount")
                if lh is not None and lh > 0:
                    snap.lh = lh
                dn = data_entity.get_int32(f"{prefix}.m_iDenyCount")
                if dn is not None and dn > 0:
                    snap.dn = dn
            snap.ability_levels = self._read_abilities(entity)
            pid = snap.player_id
            snap.total_hero_damage = self._total_hero_damage.get(pid, 0)
            snap.total_hero_healing = self._total_hero_healing.get(pid, 0)
            snap.total_deaths = self._total_deaths.get(pid, 0)
            snap.total_stuns = self._total_stuns.get(pid, 0.0)
            if minute:
                self._minute_snaps.append(snap)
            else:
                self.snapshots.append(snap)
                self._diff_inventory(entity, snap.player_id, snap.npc_name, tick)

    def _read_abilities(self, hero: Entity) -> dict[str, int]:
        """Read current ability names and levels from a hero entity.

        Iterates ``m_hAbilities.0000``–``m_hAbilities.0031``, falling back to
        ``m_vecAbilities.*`` for older replays. Resolves each handle to an
        ability entity and reads ``m_iLevel`` and the name from the
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
        entity_names = self._parser.string_tables.get_by_name("EntityNames")
        if entity_names is None:
            return {}

        result: dict[str, int] = {}
        for slot in range(_ABILITY_SLOTS):
            handle = hero.get_uint32(f"m_hAbilities.{slot:04d}")
            if handle is None:
                handle = hero.get_uint32(f"m_vecAbilities.{slot:04d}")
            if handle is None or handle == _NULL_HANDLE:
                continue
            ability_entity = em.find_by_handle(handle)
            if ability_entity is None:
                continue
            name_idx = ability_entity.get_int32("m_pEntity.m_nameStringableIndex")
            if name_idx is None or name_idx < 0:
                continue
            item = entity_names.items.get(name_idx)
            if item is None:
                continue
            name = item[0] if isinstance(item, tuple) else str(item)
            if not name:
                continue
            level = ability_entity.get_int32("m_iLevel") or 0
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
        for slot in range(_ITEM_SLOTS):
            handle = hero.get_uint32(f"m_hItems.{slot:04d}")
            if handle is None or handle == _NULL_HANDLE:
                continue
            item_entity = em.find_by_handle(handle)
            if item_entity is None:
                continue
            name_idx = item_entity.get_int32("m_pEntity.m_nameStringableIndex")
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

    def _diff_inventory(self, hero: Entity, player_id: int, npc_name: str, tick: int) -> None:
        """Emit synthetic PURCHASE entries for a player's starting inventory.

        Called on the first snapshot per player. Reads all occupied item slots
        and emits a ``PURCHASE`` ``CombatLogEntry`` for each, filling the gap
        before the combat log stream begins recording.

        Args:
            hero: The hero entity.
            player_id: Player slot (0-9).
            npc_name: Hero NPC name for the combat log entry.
            tick: Current game tick.
        """
        if self._parser is None or player_id in self._inventory_initialized:
            return
        current = self._read_inventory(hero)

        if player_id not in self._inventory_initialized:
            # First snapshot — emit all current items as starting inventory.
            # Subsequent purchases are covered by DOTA_COMBATLOG_PURCHASE events.
            # Reference: refs/parser/Parse.java isPlayerStartingItemsWritten pattern
            self._inventory_initialized.add(player_id)
            self.first_snapshot_tick[player_id] = tick
            for item_name in current.values():
                if item_name and not item_name.startswith("item_recipe"):
                    entry = CombatLogEntry(
                        tick=tick,
                        log_type="PURCHASE",
                        target_name=npc_name,
                        value_name=item_name,
                    )
                    self._parser.combat_log._emit(entry)
