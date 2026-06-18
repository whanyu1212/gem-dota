"""OpenDota-style interval snapshots for per-minute match curves.

The dense player extractor samples hero/controller state for general time
series use. OpenDota's ``gold_t``/``xp_t`` arrays, however, come from periodic
``interval`` entries built from ``CDOTA_PlayerResource`` plus
``CDOTA_DataRadiant``/``CDOTA_DataDire``. This extractor keeps that path
separate so match-level advantage curves can use the same authoritative fields
without overloading ``PlayerExtractor`` with another responsibility.

Reference:
    ``refs/parser/src/main/java/opendota/Parse.java`` interval block and
    ``refs/parser/src/main/java/opendota/CreateParsedDataBlob.java``
    ``handleInterval``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.extractors._snapshots import _HERO_CLASS_PREFIX
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

_TEAM_RADIANT = 2
_TEAM_DIRE = 3
_PLAYER_RESOURCE_SCAN_LIMIT = 30
_TICKS_PER_SECOND = 30
_FINAL_INTERVAL_GRACE_TICKS = 15 * _TICKS_PER_SECOND

# One observed team-data frame for a slot: (observed_tick, (gold, xp, lh, dn, nw)).
_TeamDataFrame = tuple[int, tuple[int, int, int, int, int]]

# Terminal counters read from the same ``m_vecDataTeam`` entry as gold/xp. These
# are monotonic totals consumed only as end-of-game scalars (not curves), so the
# extractor keeps the last observed value per team slot rather than a series.
# ``m_iRoshanKills`` is intentionally excluded: its team-data value disagrees with
# OpenDota's per-player ``roshan_kills`` (which uses combat-log last-hit
# attribution). gem reports Roshan kills via the objectives/combat-log path.
# Mapping is {ParsedPlayer attribute: m_vecDataTeam field}.
_TEAM_COUNTER_FIELDS: dict[str, str] = {
    "camps_stacked": "m_iCampsStacked",
    "creeps_stacked": "m_iCreepsStacked",
    "obs_placed": "m_iObserverWardsPlaced",
    "sen_placed": "m_iSentryWardsPlaced",
    "rune_pickups": "m_iRunePickups",
    "tower_kills": "m_iTowerKills",
}


@dataclass(frozen=True, slots=True)
class IntervalSnapshot:
    """One OpenDota-style interval sample for a player.

    ``gold`` and ``xp`` are cumulative earned totals from the team data entity,
    not current spendable gold or current-level XP. Those names mirror
    OpenDota's interval entry fields, which later become ``gold_t`` and
    ``xp_t`` arrays in parsed output.
    """

    tick: int
    time_s: int
    player_id: int
    player_slot: int
    team: int
    team_slot: int
    hero_name: str = ""
    gold: int = 0
    xp: int = 0
    lh: int = 0
    dn: int = 0
    net_worth: int = 0


@dataclass(slots=True)
class IntervalTimeSeries:
    """Parallel interval arrays for one player."""

    player_id: int
    ticks: list[int] = field(default_factory=list)
    times: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)


class IntervalExtractor:
    """Collect 60-second player intervals from authoritative team entities.

    The extractor is internal plumbing for OpenDota-parity output. It samples
    only when the parser's game clock lands on an exact interval boundary and
    falls silent otherwise; callers can fall back to existing player minute
    series when no complete interval data was observed for a replay.
    """

    snapshots: list[IntervalSnapshot]

    def __init__(self, interval_s: int = 60) -> None:
        """Initialise interval sampling.

        Args:
            interval_s: Game-time cadence in seconds. Defaults to 60 seconds,
                matching OpenDota's exported minute arrays.

        Raises:
            ValueError: If ``interval_s`` is not positive.
        """
        if interval_s <= 0:
            raise ValueError("interval_s must be positive")
        self._interval_s = interval_s
        self._parser: ReplayParser | None = None
        self._player_resource: Entity | None = None
        self._data_radiant: Entity | None = None
        self._data_dire: Entity | None = None
        # Per-team-slot team-data history, kept to the two most recent observed
        # frames as ``(observed_tick, (gold, xp, lh, dn, net_worth))``. OpenDota's
        # interval read lands one entity frame earlier than gem's clock crossing,
        # so emitting the live (boundary-tick) value double-counts the increment
        # that arrived on the boundary tick. ``_emit`` instead reads the latest
        # frame observed *strictly before* the boundary tick, removing the
        # systematic +1. Two frames suffice for that rule: when a slot updates on
        # the boundary tick the prior frame is used; when a slot is off-cadence
        # and did not update on the boundary tick its current frame already
        # precedes the crossing and is used directly. Entities mutate in place,
        # so values are copied eagerly rather than held by reference. See
        # ``_record_team_data`` / ``_team_data_values`` and
        # ``test_nudge_reads_previous_data_frame``.
        self._prev_data_radiant: dict[int, _TeamDataFrame] = {}
        self._prev_data_dire: dict[int, _TeamDataFrame] = {}
        self._cur_data_radiant: dict[int, _TeamDataFrame] = {}
        self._cur_data_dire: dict[int, _TeamDataFrame] = {}
        # Last observed terminal counters per (team, team_slot). These are
        # monotonic totals (camps/creeps stacked, wards placed, rune pickups,
        # tower kills) read from the same ``m_vecDataTeam`` entry as gold/xp;
        # consumed only as end-of-game scalars. ``{(team, slot): {attr: value}}``.
        self._team_counters: dict[tuple[int, int], dict[str, int]] = {}
        self._player_index_by_id: dict[int, int] = {}
        self._player_team: dict[int, int] = {}
        self._player_team_slot: dict[int, int] = {}
        self._hero_names: dict[int, str] = {}
        self._next_interval_s: int | None = None
        self._last_clock_tick: int | None = None
        self._last_emitted_time_s: int | None = None
        self._last_emitted_tick: int | None = None
        self._zero_clock_seen = False
        self._ended = False
        self.snapshots = []

    def attach(self, parser: ReplayParser) -> None:
        """Register parser callbacks."""
        self._parser = parser
        parser.on_entity(self._on_entity)
        parser.on_game_end(self._on_game_end)

    @property
    def all_snapshots(self) -> list[IntervalSnapshot]:
        """Return all collected interval snapshots."""
        return self.snapshots

    def series(self, player_id: int) -> IntervalTimeSeries:
        """Aggregate interval snapshots for one player.

        Args:
            player_id: OpenDota logical player slot, 0-9.

        Returns:
            Parallel arrays sorted by game time.
        """
        ts = IntervalTimeSeries(player_id=player_id)
        player_snaps = sorted(
            (snap for snap in self.snapshots if snap.player_id == player_id),
            key=lambda snap: (snap.time_s, snap.tick),
        )
        for snap in player_snaps:
            ts.ticks.append(snap.tick)
            ts.times.append(snap.time_s)
            ts.gold_t.append(snap.gold)
            ts.xp_t.append(snap.xp)
            ts.lh_t.append(snap.lh)
            ts.dn_t.append(snap.dn)
            ts.net_worth_t.append(snap.net_worth)
        return ts

    def _clock(self) -> int | None:
        """Return the game clock the extractor samples boundaries on.

        OpenDota times its interval boundaries and its postGame stop on a single
        axis: the combat-log timestamp axis, anchored at the GAME_STATE==5 horn.
        gem's entity-derived ``game_time_s`` differs from that axis by a
        per-replay constant (the gap between the horn timestamp and
        ``m_flGameStartTime``), large enough on some replays to drop the final
        minute boundary before ``_on_game_end`` (also combat-log timed) fires.

        Prefer the combat-log axis (``parser.combat_log_time_s``); fall back to
        the entity clock (``game_time_s``) before the horn timestamp is known,
        when no intervals should emit yet anyway.

        Reference: refs/parser/src/main/java/opendota/Parse.java — single
        ``time`` axis shifted by ``gameStartTime`` for intervals and postGame.
        """
        if self._parser is None:
            return None
        clock = getattr(self._parser, "combat_log_time_s", None)
        if clock is not None:
            return clock
        return getattr(self._parser, "game_time_s", None)

    def _on_game_end(self, tick: int) -> None:
        self._emit_final_boundary(tick)
        self._ended = True

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls == "CDOTAGamerulesProxy":
            if not op.has(EntityOp.DELETED):
                self._last_clock_tick = self._parser.tick if self._parser is not None else None
                if self._clock() == 0:
                    self._zero_clock_seen = True
                self._maybe_emit()
            return

        if cls == "CDOTA_PlayerResource":
            if op.has(EntityOp.DELETED):
                self._player_resource = None
                self._player_index_by_id.clear()
                self._player_team.clear()
                self._player_team_slot.clear()
            else:
                self._player_resource = entity
                self._refresh_player_mappings()
                self._maybe_emit()
            return

        if cls in ("CDOTADataRadiant", "CDOTA_DataRadiant"):
            if op.has(EntityOp.DELETED):
                self._data_radiant = None
            else:
                self._data_radiant = entity
                self._record_team_data(entity, self._cur_data_radiant, self._prev_data_radiant)
                self._record_team_counters(entity, _TEAM_RADIANT)
                self._maybe_emit()
            return

        if cls in ("CDOTADataDire", "CDOTA_DataDire"):
            if op.has(EntityOp.DELETED):
                self._data_dire = None
            else:
                self._data_dire = entity
                self._record_team_data(entity, self._cur_data_dire, self._prev_data_dire)
                self._record_team_counters(entity, _TEAM_DIRE)
                self._maybe_emit()
            return

        if cls.startswith(_HERO_CLASS_PREFIX):
            player_id = _player_id_from_hero(entity)
            if player_id is None:
                return
            if op.has(EntityOp.DELETED):
                self._hero_names.pop(player_id, None)
            else:
                self._hero_names[player_id] = self._hero_name(entity)
                self._maybe_emit()

    def _refresh_player_mappings(self) -> None:
        """Build OpenDota logical slot mappings from ``CDOTA_PlayerResource``.

        OpenDota first scans PlayerResource for valid player indices, then uses
        the scan order as output slot ``0..9``. The resource index is not always
        the same as the logical output slot, so keep the indirection explicit.
        """
        pr = self._player_resource
        if pr is None:
            return

        player_index_by_id: dict[int, int] = {}
        player_team: dict[int, int] = {}
        player_team_slot: dict[int, int] = {}

        for resource_idx in range(_PLAYER_RESOURCE_SCAN_LIMIT):
            team = pr.get_int32(f"m_vecPlayerData.{resource_idx:04d}.m_iPlayerTeam")
            team_slot = pr.get_int32(f"m_vecPlayerTeamData.{resource_idx:04d}.m_iTeamSlot")
            if team not in (_TEAM_RADIANT, _TEAM_DIRE) or team_slot is None or team_slot < 0:
                continue
            player_id = len(player_index_by_id)
            if player_id >= 10:
                break
            player_index_by_id[player_id] = resource_idx
            player_team[player_id] = team
            player_team_slot[player_id] = team_slot

        self._player_index_by_id = player_index_by_id
        self._player_team = player_team
        self._player_team_slot = player_team_slot

    def _maybe_emit(self) -> None:
        if self._parser is None or self._ended:
            return
        if self._player_resource is None or not self._player_index_by_id:
            return
        teams = set(self._player_team.values())
        if _TEAM_RADIANT in teams and self._data_radiant is None:
            return
        if _TEAM_DIRE in teams and self._data_dire is None:
            return

        game_time_s = self._clock()
        if game_time_s is None or game_time_s < 0:
            return
        # ``game_time_s`` is only refreshed by CDOTAGamerulesProxy. Other
        # entity updates may arrive on later ticks while that value is stale.
        # The one exception is OpenDota's leading zero baseline: if the clock
        # hit t=0 before team data arrived, emit it only while all exported
        # interval counters are still zero.
        if self._last_clock_tick != self._parser.tick and not self._can_emit_zero_baseline(
            game_time_s
        ):
            return
        if game_time_s % self._interval_s != 0:
            return
        if self._last_emitted_time_s == game_time_s:
            return
        if self._next_interval_s is not None and game_time_s < self._next_interval_s:
            return

        if (
            game_time_s == 0
            and self._last_emitted_time_s is None
            and not self._current_interval_counters_are_zero()
        ):
            self._emit_zero_baseline()
            return

        if game_time_s > 0 and self._last_emitted_time_s is None and self._zero_clock_seen:
            self._emit_zero_baseline()

        emitted = self._emit(game_time_s)
        if emitted:
            self._last_emitted_time_s = game_time_s
            self._last_emitted_tick = self._parser.tick
            self._next_interval_s = game_time_s + self._interval_s

    def _emit_final_boundary(self, tick: int) -> None:
        """Flush the last partial minute at game end if it is close enough.

        OpenDota's postGame stop emits one final interval for the in-progress
        minute when the game ends within ``_FINAL_INTERVAL_GRACE_TICKS`` of the
        next boundary. This is a terminal read, not a boundary crossing: unlike a
        regular boundary it deliberately keeps the live (last-observed) team-data
        values rather than nudging back one frame. The boundary nudge excludes
        the increment that lands *on* a future crossing tick; at game end there is
        no future crossing, so the terminal value is correct as-is. The
        ``observed_tick < emit_tick`` rule in :meth:`_team_data_values` produces
        this automatically because ``tick`` here is the game-end tick, later than
        every recorded data frame, so the current frame is selected. Measured:
        final-minute gold_t/xp_t match OpenDota to within 1 unit across the
        validation fixtures.

        Args:
            tick: The game-end tick reported by ``_on_game_end``.
        """
        if self._parser is None:
            return
        if self._next_interval_s is None or self._last_emitted_tick is None:
            return

        interval_ticks = self._interval_s * _TICKS_PER_SECOND
        ticks_since_last_emit = tick - self._last_emitted_tick
        if ticks_since_last_emit < 0:
            return
        if ticks_since_last_emit + _FINAL_INTERVAL_GRACE_TICKS < interval_ticks:
            return

        emitted = self._emit(self._next_interval_s)
        if emitted:
            self._last_emitted_time_s = self._next_interval_s
            self._last_emitted_tick = tick
            self._next_interval_s += self._interval_s

    def _can_emit_zero_baseline(self, game_time_s: int) -> bool:
        """Return whether a delayed t=0 OpenDota baseline is still safe."""
        if game_time_s != 0 or self._last_emitted_time_s is not None:
            return False
        if self._next_interval_s is not None:
            return False
        return self._current_interval_counters_are_zero()

    def _emit_zero_baseline(self) -> bool:
        """Prepend OpenDota's synthetic t=0 player baseline."""
        emitted = False
        tick = self._parser.tick if self._parser is not None else 0

        for player_id in sorted(self._player_index_by_id):
            team = self._player_team.get(player_id, 0)
            team_slot = self._player_team_slot.get(player_id)
            if team_slot is None:
                continue
            player_slot = team_slot if team == _TEAM_RADIANT else 128 + team_slot
            self.snapshots.append(
                IntervalSnapshot(
                    tick=tick,
                    time_s=0,
                    player_id=player_id,
                    player_slot=player_slot,
                    team=team,
                    team_slot=team_slot,
                    hero_name=self._hero_names.get(player_id, ""),
                    gold=0,
                    xp=0,
                    lh=0,
                    dn=0,
                    net_worth=0,
                )
            )
            emitted = True

        if emitted:
            self._last_emitted_time_s = 0
            self._last_emitted_tick = tick
            self._next_interval_s = self._interval_s
        return emitted

    def _current_interval_counters_are_zero(self) -> bool:
        for player_id in sorted(self._player_index_by_id):
            team = self._player_team.get(player_id, 0)
            team_slot = self._player_team_slot.get(player_id)
            if team_slot is None:
                return False
            data_entity = self._data_radiant if team == _TEAM_RADIANT else self._data_dire
            if data_entity is None:
                return False

            prefix = f"m_vecDataTeam.{team_slot:04d}"
            for field_name in (
                "m_iTotalEarnedGold",
                "m_iTotalEarnedXP",
                "m_iLastHitCount",
                "m_iDenyCount",
            ):
                if _int_or_zero(data_entity.get_int32(f"{prefix}.{field_name}")) != 0:
                    return False

        return bool(self._player_index_by_id)

    def _record_team_data(
        self,
        entity: Entity,
        cur: dict[int, _TeamDataFrame],
        prev: dict[int, _TeamDataFrame],
    ) -> None:
        """Record the latest two observed team-data frames per slot for one team.

        Entities mutate in place, so ``entity`` already holds the new frame's
        values. Stamp each slot's values with the current tick. Only demote the
        existing current frame into ``prev`` when this update advances to a new
        tick — repeated same-tick dispatches refresh the current frame without
        consuming the genuinely-prior frame ``_emit`` needs.

        Args:
            entity: The just-updated ``CDOTA_DataRadiant``/``CDOTA_DataDire``.
            cur: Per-team-slot cache of the most recent observed frame.
            prev: Per-team-slot cache of the frame before ``cur``.
        """
        tick = self._parser.tick if self._parser is not None else 0
        for team_slot in range(5):
            existing = cur.get(team_slot)
            if existing is not None and existing[0] != tick:
                prev[team_slot] = existing
            prefix = f"m_vecDataTeam.{team_slot:04d}"
            cur[team_slot] = (
                tick,
                (
                    _int_or_zero(entity.get_int32(f"{prefix}.m_iTotalEarnedGold")),
                    _int_or_zero(entity.get_int32(f"{prefix}.m_iTotalEarnedXP")),
                    _int_or_zero(entity.get_int32(f"{prefix}.m_iLastHitCount")),
                    _int_or_zero(entity.get_int32(f"{prefix}.m_iDenyCount")),
                    _int_or_zero(entity.get_int32(f"{prefix}.m_iNetWorth")),
                ),
            )

    def _record_team_counters(self, entity: Entity, team: int) -> None:
        """Record the latest monotonic terminal counters for one team's slots.

        These are end-of-game scalar totals (camps/creeps stacked, wards placed,
        rune pickups, tower kills) read from the same ``m_vecDataTeam`` entry as
        gold/xp. They are not curves, so only the most recent value per slot is
        kept; the last observed value is the terminal total.

        Args:
            entity: The just-updated ``CDOTA_DataRadiant``/``CDOTA_DataDire``.
            team: ``_TEAM_RADIANT`` or ``_TEAM_DIRE``.
        """
        for team_slot in range(5):
            prefix = f"m_vecDataTeam.{team_slot:04d}"
            counters = self._team_counters.setdefault((team, team_slot), {})
            for attr, field_name in _TEAM_COUNTER_FIELDS.items():
                value = entity.get_int32(f"{prefix}.{field_name}")
                if value is not None:
                    counters[attr] = value

    def team_counters(self, player_id: int) -> dict[str, int]:
        """Return the terminal counters observed for one logical player.

        Resolves the player's ``(team, team_slot)`` via the same mapping used for
        interval emission, so callers need only the 0-9 logical player id.

        Args:
            player_id: OpenDota logical player slot, 0-9.

        Returns:
            ``{attr: value}`` for each tracked counter, ``0`` where unseen. Keys
            are the ``ParsedPlayer`` attribute names (e.g. ``camps_stacked``).
        """
        team = self._player_team.get(player_id)
        team_slot = self._player_team_slot.get(player_id)
        observed: dict[str, int] = {}
        if team is not None and team_slot is not None:
            observed = self._team_counters.get((team, team_slot), {})
        return {attr: observed.get(attr, 0) for attr in _TEAM_COUNTER_FIELDS}

    def _team_data_values(
        self, team: int, team_slot: int, data_entity: Entity, emit_tick: int
    ) -> tuple[int, int, int, int, int]:
        """Return the team-data values observed strictly before the boundary tick.

        OpenDota samples the interval one entity frame before gem's clock
        crossing. Pick the latest recorded frame with ``observed_tick <
        emit_tick``: when the slot updated on the boundary tick that is the prior
        frame; when the slot is off-cadence and did not update on the boundary
        tick its current frame already precedes the crossing. Fall back to the
        live entity before any qualifying frame exists (first boundary), where
        the values agree anyway.

        Args:
            team: ``_TEAM_RADIANT`` or ``_TEAM_DIRE``.
            team_slot: The player's team slot, 0-4.
            data_entity: The live data entity for the team (fallback source).
            emit_tick: The tick of the boundary emit.

        Returns:
            ``(gold, xp, lh, dn, net_worth)`` for the boundary frame.
        """
        cur = self._cur_data_radiant if team == _TEAM_RADIANT else self._cur_data_dire
        prev = self._prev_data_radiant if team == _TEAM_RADIANT else self._prev_data_dire
        cur_frame = cur.get(team_slot)
        if cur_frame is not None and cur_frame[0] < emit_tick:
            return cur_frame[1]
        prev_frame = prev.get(team_slot)
        if prev_frame is not None and prev_frame[0] < emit_tick:
            return prev_frame[1]
        prefix = f"m_vecDataTeam.{team_slot:04d}"
        return (
            _int_or_zero(data_entity.get_int32(f"{prefix}.m_iTotalEarnedGold")),
            _int_or_zero(data_entity.get_int32(f"{prefix}.m_iTotalEarnedXP")),
            _int_or_zero(data_entity.get_int32(f"{prefix}.m_iLastHitCount")),
            _int_or_zero(data_entity.get_int32(f"{prefix}.m_iDenyCount")),
            _int_or_zero(data_entity.get_int32(f"{prefix}.m_iNetWorth")),
        )

    def _emit(self, game_time_s: int) -> bool:
        emitted = False
        tick = self._parser.tick if self._parser is not None else 0

        for player_id in sorted(self._player_index_by_id):
            team = self._player_team.get(player_id, 0)
            team_slot = self._player_team_slot.get(player_id)
            if team_slot is None:
                continue
            data_entity = self._data_radiant if team == _TEAM_RADIANT else self._data_dire
            if data_entity is None:
                continue

            gold, xp, lh, dn, net_worth = self._team_data_values(team, team_slot, data_entity, tick)
            player_slot = team_slot if team == _TEAM_RADIANT else 128 + team_slot
            self.snapshots.append(
                IntervalSnapshot(
                    tick=tick,
                    time_s=game_time_s,
                    player_id=player_id,
                    player_slot=player_slot,
                    team=team,
                    team_slot=team_slot,
                    hero_name=self._hero_names.get(player_id, ""),
                    gold=gold,
                    xp=xp,
                    lh=lh,
                    dn=dn,
                    net_worth=net_worth,
                )
            )
            emitted = True

        return emitted

    def _hero_name(self, entity: Entity) -> str:
        entity_names = (
            self._parser.string_tables.get_by_name("EntityNames")
            if self._parser is not None and self._parser.string_tables is not None
            else None
        )
        if entity_names is not None:
            name_idx = entity.get_int32("m_pEntity.m_nameStringableIndex")
            if name_idx is None:
                name_idx = entity.get_int32("m_pEntity.m_nameStringTableIndex")
            if name_idx is not None and name_idx >= 0:
                item = entity_names.items.get(name_idx)
                if item is not None:
                    return item[0] if isinstance(item, tuple) else str(item)

        ending = entity.get_class_name()[len(_HERO_CLASS_PREFIX) :].replace("_", "")
        return "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", ending).lower()


def _player_id_from_hero(entity: Entity) -> int | None:
    player_id = entity.get_int32("m_nPlayerID")
    if player_id is None:
        player_id = entity.get_int32("m_iPlayerID")
    if player_id is None or player_id < 0:
        return None
    return player_id // 2


def _int_or_zero(value: int | None) -> int:
    return value if value is not None else 0
