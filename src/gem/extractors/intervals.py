"""OpenDota-style interval snapshots for per-minute match curves.

Internal extractor: ``IntervalExtractor`` and its snapshot/series dataclasses
are wired up by :func:`gem.api.parse` and consumed by
:mod:`gem.results.assembly`; they are intentionally not re-exported from
``gem.extractors`` and are not part of the public API.

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

from gem.extractors._snapshots import (
    _HERO_CLASS_PREFIX,
    TEAM_DIRE,
    TEAM_RADIANT,
    _player_id_from_entity,
    scan_player_resource,
    team_data_prefix,
)
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

_FINAL_INTERVAL_GRACE_S = 15

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

_TEAM_DATA_FIELD_NAMES = (
    "m_iTotalEarnedGold",
    "m_iTotalEarnedXP",
    "m_iLastHitCount",
    "m_iDenyCount",
    "m_iNetWorth",
    *_TEAM_COUNTER_FIELDS.values(),
)
_TEAM_DATA_FIELDS = FieldAccessPlan(
    tuple(
        f"{team_data_prefix(team_slot)}.{field_name}"
        for team_slot in range(5)
        for field_name in _TEAM_DATA_FIELD_NAMES
    )
)
_PLAYER_RESOURCE_SCALAR_FIELDS = FieldAccessPlan(
    tuple(
        f"m_vecPlayerTeamData.{resource_idx:04d}.{field_name}"
        for resource_idx in range(30)
        for field_name in ("m_flTeamFightParticipation", "m_iFirstBloodClaimed")
    )
)
_HERO_NAME_FIELDS = FieldAccessPlan(
    ("m_pEntity.m_nameStringableIndex", "m_pEntity.m_nameStringTableIndex")
)


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

    The extractor is internal plumbing for OpenDota-parity output. It queues an
    exact rounded-minute crossing, then samples at the following network tick
    start before that tick's entity deltas. This mirrors OpenDota's effective
    Clarity ``@OnTickStart`` phase; callers can fall back to existing player
    minute series when no complete interval data was observed for a replay.
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
        # frames as ``(observed_tick, (gold, xp, lh, dn, net_worth))``. The
        # production tick-start path reads ``cur`` after its one-tick deferral
        # for regular boundaries; minute zero reads it immediately.
        # ``prev`` preserves the entity-callback compatibility path, where the
        # latest frame strictly before a crossing is required. Entities mutate
        # in place, so values are copied eagerly rather than held by reference.
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
        # entity index → (serial, class name, player id, NPC name, stable)
        self._hero_name_by_entity: dict[int, tuple[int, str, int, str, bool]] = {}
        # player id → entity identity currently supplying its hero name
        self._hero_name_sources: dict[int, tuple[int, int]] = {}
        # (class name, EntityNames table id, item index) → canonical NPC name
        self._canonical_hero_names: dict[tuple[str, int, int], str] = {}
        self._fallback_hero_names: dict[str, str] = {}
        self._next_interval_s: int | None = None
        self._tick_start_driven = False
        # Clarity's @OnTickStart interval read is effectively one decoded net
        # tick after the first CNETMsg_Tick whose rounded clock reaches regular
        # boundaries. Minute zero is different: it is read immediately, before
        # same-tick bounty/entity deltas. Queue regular crossings and emit at the
        # next tick start, after the crossing tick's entity deltas but before the
        # next tick's.
        self._pending_tick_start_boundary: tuple[int, int] | None = None
        self._last_queued_time_s: int | None = None
        self._last_clock_tick: int | None = None
        self._last_emitted_time_s: int | None = None
        self._last_emitted_tick: int | None = None
        self._initial_boundary_pending = False
        self._ended = False
        self.snapshots = []

    def attach(self, parser: ReplayParser) -> None:
        """Register parser callbacks."""
        self._parser = parser
        parser._on_entity_filtered(
            self._on_entity,
            class_names=(
                "CDOTAGamerulesProxy",
                "CDOTA_PlayerResource",
                "CDOTADataRadiant",
                "CDOTA_DataRadiant",
                "CDOTADataDire",
                "CDOTA_DataDire",
            ),
            class_prefixes=(_HERO_CLASS_PREFIX,),
        )
        parser.on_game_end(self._on_game_end)
        on_tick_start = getattr(parser, "on_tick_start", None)
        if callable(on_tick_start):
            self._tick_start_driven = True
            on_tick_start(self._on_tick_start)

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
        """Return the clock used by the entity-callback fallback and final flush.

        Normal parsing samples ``parser.game_time_s`` directly from
        :meth:`_on_tick_start`; the parser refreshes it from ``CNETMsg_Tick``
        before current-tick entity deltas. The combat-log clock remains useful
        for the terminal recovery path because postGame is itself a combat-log
        event. It is also retained for parsers without tick-start callbacks.

        Reference: refs/parser/src/main/java/opendota/Parse.java —
        ``@OnTickStart`` for intervals and combat-log GAME_STATE 6 for postGame.
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

    def _on_tick_start(self, net_tick: int) -> None:
        """Sample minute zero immediately; defer later crossings one tick.

        ``ReplayParser`` refreshes ``game_time_s`` from ``net_tick`` before
        invoking this callback. At minute zero, Clarity reads the pre-update
        entity table immediately; delaying would incorrectly include same-tick
        bounty payouts. At later boundaries its interval output aligns one
        network tick after the first rounded-clock crossing observed here, so
        deferring includes the crossing tick's entity deltas while still reading
        before the next tick's mutations.

        Args:
            net_tick: Decoded ``CNETMsg_Tick.tick`` value.
        """
        if self._parser is None or self._ended:
            return
        game_time_s = getattr(self._parser, "game_time_s", None)
        if (
            self._pending_tick_start_boundary is None
            and game_time_s is not None
            and game_time_s >= 0
            and game_time_s % self._interval_s == 0
            and game_time_s != self._last_queued_time_s
        ):
            self._last_queued_time_s = game_time_s
            if game_time_s == 0 and self._last_emitted_time_s is None:
                self._try_emit(game_time_s, use_live=False, prefer_previous=True)
                if self._last_emitted_time_s == game_time_s:
                    return
            self._pending_tick_start_boundary = (game_time_s, net_tick)

        pending = self._pending_tick_start_boundary
        if pending is None or net_tick <= pending[1]:
            return
        boundary_time_s = pending[0]
        initial_boundary = boundary_time_s == 0 and self._last_emitted_time_s is None
        self._try_emit(
            boundary_time_s,
            use_live=not initial_boundary,
            prefer_previous=initial_boundary,
        )
        if self._last_emitted_time_s == boundary_time_s:
            self._pending_tick_start_boundary = None

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls == "CDOTAGamerulesProxy":
            if not op.has(EntityOp.DELETED):
                self._last_clock_tick = self._parser.tick if self._parser is not None else None
                if not self._tick_start_driven:
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
                if not self._tick_start_driven:
                    self._maybe_emit()
            return

        if cls in ("CDOTADataRadiant", "CDOTA_DataRadiant"):
            if op.has(EntityOp.DELETED):
                self._data_radiant = None
            else:
                self._data_radiant = entity
                self._record_team_data(entity, self._cur_data_radiant, self._prev_data_radiant)
                self._record_team_counters(entity, TEAM_RADIANT)
                if not self._tick_start_driven:
                    self._maybe_emit()
            return

        if cls in ("CDOTADataDire", "CDOTA_DataDire"):
            if op.has(EntityOp.DELETED):
                self._data_dire = None
            else:
                self._data_dire = entity
                self._record_team_data(entity, self._cur_data_dire, self._prev_data_dire)
                self._record_team_counters(entity, TEAM_DIRE)
                if not self._tick_start_driven:
                    self._maybe_emit()
            return

        if cls.startswith(_HERO_CLASS_PREFIX):
            idx = entity.get_index()
            serial = entity.get_serial()
            if op.has(EntityOp.DELETED):
                self._remove_hero_name_entity(idx, serial)
                return

            player_id = _player_id_from_entity(entity)
            if player_id is None:
                return

            cached = self._hero_name_by_entity.get(idx)
            if cached is not None and (cached[0] != serial or cached[1] != cls):
                self._remove_hero_name_entity(idx, cached[0])
                cached = None

            if cached is not None and cached[4]:
                hero_name = cached[3]
                stable = True
            else:
                hero_name, stable = self._hero_name(entity)

            if cached is not None and cached[2] != player_id:
                old_player_id = cached[2]
                if self._hero_name_sources.get(old_player_id) == (idx, serial):
                    self._hero_name_sources.pop(old_player_id, None)
                    self._hero_names.pop(old_player_id, None)

            self._hero_name_by_entity[idx] = (serial, cls, player_id, hero_name, stable)
            self._hero_name_sources[player_id] = (idx, serial)
            self._hero_names[player_id] = hero_name
            if not self._tick_start_driven:
                self._maybe_emit()

    def _remove_hero_name_entity(self, index: int, serial: int) -> None:
        """Remove cached hero-name state owned by one entity identity."""
        cached = self._hero_name_by_entity.get(index)
        if cached is None or cached[0] != serial:
            return

        self._hero_name_by_entity.pop(index, None)
        player_id = cached[2]
        if self._hero_name_sources.get(player_id) == (index, serial):
            self._hero_name_sources.pop(player_id, None)
            self._hero_names.pop(player_id, None)

    def _refresh_player_mappings(self) -> None:
        """Build OpenDota logical slot mappings from ``CDOTA_PlayerResource``.

        OpenDota first scans PlayerResource for valid player indices, then uses
        the scan order as output slot ``0..9``. The resource index is not always
        the same as the logical output slot, so keep the indirection explicit.
        """
        pr = self._player_resource
        if pr is None:
            return

        # Unlike PlayerExtractor, the interval extractor adopts the scan
        # unconditionally (including partial early-game scans) — its consumers
        # already guard on a fully-populated mapping before emitting.
        scan = scan_player_resource(pr)
        self._player_index_by_id = scan.index_by_id
        self._player_team = scan.team_by_id
        self._player_team_slot = scan.team_slot_by_id

    def _maybe_emit(self) -> None:
        if self._tick_start_driven or self._parser is None:
            return

        self._try_emit(self._clock(), use_live=False, require_fresh_clock=True)

    def _try_emit(
        self,
        game_time_s: int | None,
        *,
        use_live: bool,
        prefer_previous: bool = False,
        require_fresh_clock: bool = False,
    ) -> None:
        """Emit one complete interval batch when ``game_time_s`` is eligible."""
        if self._parser is None or self._ended:
            return

        if game_time_s is None or game_time_s < 0:
            return
        if game_time_s == 0 and self._last_emitted_time_s is None:
            self._initial_boundary_pending = True

        if self._player_resource is None or not self._player_index_by_id:
            return
        teams = set(self._player_team.values())
        if TEAM_RADIANT in teams and self._data_radiant is None:
            return
        if TEAM_DIRE in teams and self._data_dire is None:
            return

        initial_boundary = self._initial_boundary_pending and self._last_emitted_time_s is None
        boundary_time_s = 0 if initial_boundary else game_time_s
        # ``game_time_s`` is only refreshed by CDOTAGamerulesProxy. Other
        # entity updates may arrive on later ticks while that value is stale.
        # The one exception is a pending initial t=0 boundary: the clock callback
        # may precede the player/team entities needed for a complete batch, and
        # the combat-log clock may advance before those entities arrive.
        if (
            require_fresh_clock
            and self._last_clock_tick != self._parser.tick
            and not initial_boundary
        ):
            return
        if boundary_time_s % self._interval_s != 0:
            return
        if self._last_emitted_time_s == boundary_time_s:
            return
        if self._next_interval_s is not None and boundary_time_s < self._next_interval_s:
            return

        emitted = self._emit(
            boundary_time_s,
            use_live=use_live or (initial_boundary and not prefer_previous),
            prefer_previous=prefer_previous,
        )
        if emitted:
            if initial_boundary:
                self._initial_boundary_pending = False
            self._last_emitted_time_s = boundary_time_s
            self._last_emitted_tick = self._parser.tick
            self._next_interval_s = boundary_time_s + self._interval_s

    def _emit_final_boundary(self, tick: int) -> None:
        """Recover a recently elapsed interval boundary at game end.

        Entity dispatch can reach postGame before the gamerules callback that
        would normally emit a boundary. Recover that boundary only when the
        authoritative clock says it has already elapsed, and only within a small
        grace window. This prevents a short match from gaining a future minute
        sample. Terminal recovery deliberately keeps the live (last-observed)
        team-data values rather than nudging back one frame.

        Args:
            tick: The game-end tick reported by ``_on_game_end``.
        """
        if self._parser is None:
            return
        if self._next_interval_s is None or self._last_emitted_tick is None:
            return

        end_time_s = self._clock()
        if end_time_s is None:
            return
        lateness_s = end_time_s - self._next_interval_s
        if lateness_s < 0 or lateness_s > _FINAL_INTERVAL_GRACE_S:
            return

        emitted = self._emit(self._next_interval_s, use_live=True)
        if emitted:
            self._last_emitted_time_s = self._next_interval_s
            self._last_emitted_tick = tick
            self._next_interval_s += self._interval_s

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
        fields = entity._resolve_fields(_TEAM_DATA_FIELDS)
        width = len(_TEAM_DATA_FIELD_NAMES)
        for team_slot in range(5):
            existing = cur.get(team_slot)
            if existing is not None and existing[0] != tick:
                prev[team_slot] = existing
            offset = team_slot * width
            cur[team_slot] = (
                tick,
                (
                    _int_or_zero(entity._get_int32_resolved(fields[offset])),
                    _int_or_zero(entity._get_int32_resolved(fields[offset + 1])),
                    _int_or_zero(entity._get_int32_resolved(fields[offset + 2])),
                    _int_or_zero(entity._get_int32_resolved(fields[offset + 3])),
                    _int_or_zero(entity._get_int32_resolved(fields[offset + 4])),
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
            team: ``TEAM_RADIANT`` or ``TEAM_DIRE``.
        """
        fields = entity._resolve_fields(_TEAM_DATA_FIELDS)
        width = len(_TEAM_DATA_FIELD_NAMES)
        counter_offset = 5
        for team_slot in range(5):
            offset = team_slot * width + counter_offset
            counters = self._team_counters.setdefault((team, team_slot), {})
            for field_index, attr in enumerate(_TEAM_COUNTER_FIELDS):
                value = entity._get_int32_resolved(fields[offset + field_index])
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

    def player_resource_scalars(self, player_id: int) -> dict[str, float]:
        """Return end-of-game PlayerResource scalars for one logical player.

        Reads the authoritative game-computed fields OpenDota itself uses
        (``m_flTeamFightParticipation``, ``m_iFirstBloodClaimed``) from the final
        ``CDOTA_PlayerResource`` state, resolved through the coach-aware resource
        index. The parser mutates the entity in place, so the retained reference
        holds the terminal values once parsing completes.

        Reference: refs/parser/src/main/java/opendota/Parse.java (reads
        ``m_vecPlayerTeamData.%i.m_flTeamFightParticipation`` /
        ``m_iFirstBloodClaimed``).

        Args:
            player_id: OpenDota logical player slot, 0-9.

        Returns:
            ``{"teamfight_participation": float, "firstblood_claimed": int}``.
            Values default to ``0`` when the resource entity or index is missing.
        """
        result: dict[str, float] = {"teamfight_participation": 0.0, "firstblood_claimed": 0}
        pr = self._player_resource
        resource_idx = self._player_index_by_id.get(player_id)
        if pr is None or resource_idx is None:
            return result
        fields = pr._resolve_fields(_PLAYER_RESOURCE_SCALAR_FIELDS)
        offset = resource_idx * 2
        tf = pr._get_float32_resolved(fields[offset])
        if tf is not None and tf != float("inf"):
            result["teamfight_participation"] = tf
        fb = pr._get_int32_resolved(fields[offset + 1])
        if fb is not None:
            result["firstblood_claimed"] = fb
        return result

    def _team_data_values(
        self,
        team: int,
        team_slot: int,
        data_entity: Entity,
        emit_tick: int,
        *,
        use_live: bool = False,
        prefer_previous: bool = False,
    ) -> tuple[int, int, int, int, int]:
        """Return the team-data values for an interval boundary.

        Normal boundaries use the latest recorded frame strictly before the
        crossing tick, matching OpenDota's entity dispatch order. Tick-driven
        minute zero prefers the prior observed frame because Gem detects the
        rounded clock crossing one entity update after Clarity; terminal and
        compatibility-path boundaries can select the live frame explicitly.

        Args:
            team: ``TEAM_RADIANT`` or ``TEAM_DIRE``.
            team_slot: The player's team slot, 0-4.
            data_entity: The live data entity for the team (fallback source).
            emit_tick: The tick of the boundary emit.
            use_live: Select the current frame without the boundary nudge.
            prefer_previous: Select the prior observed frame when available.

        Returns:
            ``(gold, xp, lh, dn, net_worth)`` for the boundary frame.
        """
        cur = self._cur_data_radiant if team == TEAM_RADIANT else self._cur_data_dire
        prev = self._prev_data_radiant if team == TEAM_RADIANT else self._prev_data_dire
        cur_frame = cur.get(team_slot)
        prev_frame = prev.get(team_slot)
        if prefer_previous:
            if prev_frame is not None:
                return prev_frame[1]
            if cur_frame is not None:
                return cur_frame[1]
        if use_live and cur_frame is not None:
            return cur_frame[1]
        if cur_frame is not None and cur_frame[0] < emit_tick:
            return cur_frame[1]
        if prev_frame is not None and prev_frame[0] < emit_tick:
            return prev_frame[1]
        fields = data_entity._resolve_fields(_TEAM_DATA_FIELDS)
        offset = team_slot * len(_TEAM_DATA_FIELD_NAMES)
        return (
            _int_or_zero(data_entity._get_int32_resolved(fields[offset])),
            _int_or_zero(data_entity._get_int32_resolved(fields[offset + 1])),
            _int_or_zero(data_entity._get_int32_resolved(fields[offset + 2])),
            _int_or_zero(data_entity._get_int32_resolved(fields[offset + 3])),
            _int_or_zero(data_entity._get_int32_resolved(fields[offset + 4])),
        )

    def _emit(
        self,
        game_time_s: int,
        *,
        use_live: bool = False,
        prefer_previous: bool = False,
    ) -> bool:
        emitted = False
        tick = self._parser.tick if self._parser is not None else 0

        for player_id in sorted(self._player_index_by_id):
            team = self._player_team.get(player_id, 0)
            team_slot = self._player_team_slot.get(player_id)
            if team_slot is None:
                continue
            data_entity = self._data_radiant if team == TEAM_RADIANT else self._data_dire
            if data_entity is None:
                continue

            gold, xp, lh, dn, net_worth = self._team_data_values(
                team,
                team_slot,
                data_entity,
                tick,
                use_live=use_live,
                prefer_previous=prefer_previous,
            )
            player_slot = team_slot if team == TEAM_RADIANT else 128 + team_slot
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

    def _hero_name(self, entity: Entity) -> tuple[str, bool]:
        """Return a hero NPC name and whether its table identity is stable."""
        class_name = entity.get_class_name()
        entity_names = (
            self._parser.string_tables.get_by_name("EntityNames")
            if self._parser is not None and self._parser.string_tables is not None
            else None
        )
        if entity_names is not None:
            fields = entity._resolve_fields(_HERO_NAME_FIELDS)
            name_idx = entity._get_int32_resolved(fields[0])
            if name_idx is None:
                name_idx = entity._get_int32_resolved(fields[1])
            if name_idx is not None and name_idx >= 0:
                item = entity_names.items.get(name_idx)
                if item is not None:
                    key = (class_name, entity_names.index, name_idx)
                    cached = self._canonical_hero_names.get(key)
                    if cached is not None:
                        return cached, True
                    name = item[0] if isinstance(item, tuple) else str(item)
                    self._canonical_hero_names[key] = name
                    return name, True

        cached_fallback = self._fallback_hero_names.get(class_name)
        if cached_fallback is None:
            ending = class_name[len(_HERO_CLASS_PREFIX) :].replace("_", "")
            cached_fallback = "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", ending).lower()
            self._fallback_hero_names[class_name] = cached_fallback
        return cached_fallback, False


def _int_or_zero(value: int | None) -> int:
    return value if value is not None else 0
