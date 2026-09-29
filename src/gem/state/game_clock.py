"""Pause-aware conversion between replay ticks and the in-game clock.

Replay ticks keep advancing while a match is paused, but the in-game clock does
not. Since Dota 2 7.32e the game-rules entity no longer carries
``m_fGameTime``; the clock is ``(server_tick - m_nTotalPausedTicks) / 30``,
frozen at ``m_nPauseStartTick`` while paused, and shifted by
``m_flGameStartTime``. :class:`GameClock` records the anchors and pause
intervals needed to reproduce that clock for any replay tick after parsing.

:class:`GameClockTracker` builds that clock while a replay is parsed.

Reference: odota/parser src/main/java/opendota/Parse.java (game-time and pause
tracking in ``onTickStart``; pinned revision in CLAUDE.md).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.proto.dota_shared_enums_pb2 import (
    DOTA_GAMERULES_STATE_GAME_IN_PROGRESS,
    DOTA_GAMERULES_STATE_POST_GAME,
)
from gem.schema.sendtable.models import FieldAccessPlan, ResolvedField

if TYPE_CHECKING:
    from gem.state.entities import Entity

TICKS_PER_SECOND = 30


def _round_half_up(value: float) -> int:
    """Round the way Java ``Math.round`` does (half up, also for negatives)."""
    return math.floor(value + 0.5)


@dataclass(frozen=True)
class GamePause:
    """One interval during which the in-game clock was stopped.

    Attributes:
        start_tick: First replay tick of the pause.
        end_tick: Replay tick at which the clock resumed (exclusive), or
            ``None`` when the replay ended while still paused.
    """

    start_tick: int
    end_tick: int | None

    @property
    def duration_ticks(self) -> int | None:
        """Paused length in ticks, or ``None`` for a pause that never ended."""
        if self.end_tick is None:
            return None
        return self.end_tick - self.start_tick


@dataclass
class GameClock:
    """Maps replay ticks to pause-aware in-game time and back.

    Replay ticks remain the canonical join key everywhere in gem; use this
    clock only to present or export times the way the in-game clock shows them.

    Attributes:
        game_start_tick: Replay tick at which the horn sounded (game time 0),
            or ``None`` if it was not observed.
        pauses: Observed pauses in chronological order.
        game_start_time_s: Engine ``m_flGameStartTime`` in seconds, when
            observed. Together with ``net_tick_offset`` it reproduces the
            engine/OpenDota clock exactly.
        net_tick_offset: ``net_tick - tick`` observed at game start. Engine
            pause fields count network ticks, which can lead replay ticks by a
            constant offset.
    """

    game_start_tick: int | None = None
    pauses: list[GamePause] = field(default_factory=list)
    game_start_time_s: float | None = None
    net_tick_offset: int = 0

    def paused_ticks_before(self, tick: int) -> int:
        """Return how many ticks of pause elapsed before ``tick``.

        Args:
            tick: Replay tick.

        Returns:
            Paused ticks in ``[replay start, tick)``; a tick inside a pause
            counts only the part of that pause already elapsed.
        """
        paused = 0
        for pause in self.pauses:
            if tick <= pause.start_tick:
                break
            end = tick if pause.end_tick is None else min(tick, pause.end_tick)
            paused += end - pause.start_tick
        return paused

    def _base_unpaused_tick(self) -> float | None:
        if self.game_start_time_s is not None:
            return self.game_start_time_s * TICKS_PER_SECOND - self.net_tick_offset
        if self.game_start_tick is not None:
            return self.game_start_tick - self.paused_ticks_before(self.game_start_tick)
        return None

    def game_time_at(self, tick: int) -> float | None:
        """Return the exact in-game clock reading at a replay tick.

        Args:
            tick: Replay tick.

        Returns:
            Seconds since the horn (negative before it), frozen during pauses,
            or ``None`` when the game start was never observed.
        """
        base = self._base_unpaused_tick()
        if base is None:
            return None
        return (tick - self.paused_ticks_before(tick) - base) / TICKS_PER_SECOND

    def game_seconds_at(self, tick: int) -> int | None:
        """Return whole in-game seconds at a replay tick, as OpenDota reports them.

        With engine anchors this reproduces OpenDota's
        ``round((tick - paused) / 30) - round(game_start_time)``; otherwise it
        floors the pause-aware offset from ``game_start_tick``.

        Args:
            tick: Replay tick.

        Returns:
            Whole seconds since the horn (negative before it), or ``None`` when
            the game start was never observed.
        """
        if self.game_start_time_s is not None:
            unpaused = tick + self.net_tick_offset - self.paused_ticks_before(tick)
            return _round_half_up(unpaused / TICKS_PER_SECOND) - _round_half_up(
                self.game_start_time_s
            )
        game_time = self.game_time_at(tick)
        return None if game_time is None else math.floor(game_time)

    def tick_at(self, game_time_s: float) -> int | None:
        """Return the first replay tick at which the in-game clock reads a time.

        Args:
            game_time_s: Seconds since the horn (negative before it).

        Returns:
            The earliest replay tick whose clock reading is at least
            ``game_time_s``, or ``None`` when the game start was never observed
            or the clock never reaches that time because a pause never ended.
        """
        base = self._base_unpaused_tick()
        if base is None:
            return None
        tick = math.ceil(base + game_time_s * TICKS_PER_SECOND)
        for pause in self.pauses:
            if pause.start_tick >= tick:
                break
            if pause.end_tick is None:
                return None
            tick += pause.end_tick - pause.start_tick
        return tick

    def format_tick(self, tick: int) -> str:
        """Format a replay tick as the in-game clock (``MM:SS``, ``-MM:SS`` pre-horn).

        Args:
            tick: Replay tick.

        Returns:
            The formatted clock reading, or ``"--:--"`` when unavailable.
        """
        seconds = self.game_seconds_at(tick)
        if seconds is None:
            return "--:--"
        sign = "-" if seconds < 0 else ""
        seconds = abs(seconds)
        return f"{sign}{seconds // 60:02d}:{seconds % 60:02d}"


def game_clock_for(match: object) -> GameClock:
    """Return a match's game clock, or a tick-only fallback for older matches.

    Args:
        match: A ``ParsedMatch`` (or any object with ``game_clock`` and
            ``game_start_tick`` attributes).

    Returns:
        ``match.game_clock`` when present; otherwise a pause-free clock anchored
        at ``match.game_start_tick``.
    """
    clock = getattr(match, "game_clock", None)
    if isinstance(clock, GameClock):
        return clock
    return GameClock(game_start_tick=getattr(match, "game_start_tick", None))


# ---------------------------------------------------------------------------
# Live tracking during a parse
# ---------------------------------------------------------------------------

_CLOCK_FIELDS = FieldAccessPlan(
    (
        "m_pGameRules.m_flGameStartTime",
        "m_pGameRules.m_fGameTime",
        "m_pGameRules.m_bGamePaused",
        "m_pGameRules.m_nPauseStartTick",
        "m_pGameRules.m_nTotalPausedTicks",
    )
)


def _round_positive_seconds(value: float) -> int:
    """Round positive replay seconds the same way Java ``Math.round`` does."""
    return int(value + 0.5)


def _raw_time_s(entity: Entity, fields: tuple[ResolvedField, ...], net_tick: int) -> int:
    """Return OpenDota's uncorrected clock from the game rules at ``net_tick``.

    ``round(m_fGameTime)`` when present; otherwise the unpaused network-tick
    count in seconds, frozen at the pause start while paused (Parse.java).
    """
    game_time = entity._get_float32_resolved(fields[1])
    if game_time is not None:
        return _round_positive_seconds(game_time)
    paused = entity._get_bool_resolved(fields[2]) or False
    pause_start_tick = entity._get_int32_resolved(fields[3])
    total_paused_ticks = entity._get_int32_resolved(fields[4]) or 0
    time_tick = pause_start_tick if paused and pause_start_tick is not None else net_tick
    return _round_positive_seconds((time_tick - total_paused_ticks) / 30.0)


class GameClockTracker:
    """Builds the in-game clock while a replay is parsed.

    ``ReplayParser`` feeds it network ticks, game-rules entity updates, and
    combat-log timestamps; it keeps the live clock readings OpenDota uses and
    records the :class:`GameClock` anchors and pauses for after the parse.

    Attributes:
        clock: The anchors and pauses observed so far.
        net_tick: Latest ``CNETMsg_Tick`` value.
        net_tick_seen: Whether any ``CNETMsg_Tick`` has arrived.
        tick_start_raw_s: OpenDota's running ``time`` at the start of the current
            outer tick, which it stamps chat events with; see
            :meth:`snapshot_tick_start`. ``None`` before the game rules and a
            network tick exist.
        opendota_start_s: OpenDota's game-start anchor: the first of the rounded
            ``GAME_IN_PROGRESS`` combat-log timestamp and the rounded
            ``m_flGameStartTime``. Never changes once set.
        raw_time_s: OpenDota's uncorrected clock (``time`` in ``Parse.java``):
            the rounded server game time, before subtracting the game start.
            Available in pregame, before :attr:`game_time_s`.
        game_time_s: OpenDota-style game time from the game-rules entity, or
            ``None`` before the game start time is known.
        game_start_tick: Replay tick at which the game start was first seen.
        combat_log_time_s: Horn-anchored time of the latest timed combat-log
            entry, or ``None`` before the ``GAME_IN_PROGRESS`` marker.
        duration_s: Combat-log time of the ``POST_GAME`` marker (OpenDota's
            ``duration``), or ``None`` until it arrives.
    """

    def __init__(self) -> None:
        self.clock = GameClock()
        self.net_tick = 0
        self.net_tick_seen = False
        self.raw_time_s: int | None = None
        self.game_time_s: int | None = None
        self.game_start_tick: int | None = None
        self.combat_log_time_s: int | None = None
        self.duration_s: int | None = None
        self._game_start_seen = False
        self._game_start_time_s: int | None = None
        self._combat_log_start_s: int | None = None
        # Open pause as ``(start_tick, total_paused_ticks_at_start)``.
        self._open_pause: tuple[int, int] | None = None
        # OpenDota's running ``time`` at the current outer tick's start, and its
        # game-start anchor (first seen, never changed). See snapshot_tick_start.
        self.tick_start_raw_s: int | None = None
        self.opendota_start_s: int | None = None

    def on_net_tick(self, net_tick: int) -> None:
        """Record a ``CNETMsg_Tick``."""
        self.net_tick = net_tick
        self.net_tick_seen = True

    def net_tick_offset(self, tick: int) -> int:
        """Return ``net_tick - tick``, or 0 before any network tick."""
        return self.net_tick - tick if self.net_tick_seen else 0

    def update(self, entity: Entity, tick: int) -> None:
        """Refresh the clock from the ``CDOTAGamerulesProxy`` entity.

        OpenDota timestamps interval records by reading ``m_fGameTime`` when
        available, or falling back to ``(tick - paused_ticks) / 30``. The stored
        output time is then shifted by ``m_flGameStartTime``.

        Args:
            entity: The game-rules entity.
            tick: Current replay tick.
        """
        fields = entity._resolve_fields(_CLOCK_FIELDS)
        paused_now = entity._get_bool_resolved(fields[2])
        if paused_now is not None:
            self.track_pause(
                paused_now,
                entity._get_int32_resolved(fields[3]),
                entity._get_int32_resolved(fields[4]),
                tick,
            )
        start = entity._get_float32_resolved(fields[0])
        if start is not None and start != 0.0:
            self._game_start_time_s = _round_positive_seconds(start)
            self.clock.game_start_time_s = start

        raw_time_s = _raw_time_s(entity, fields, self.net_tick if self.net_tick_seen else tick)
        self.raw_time_s = raw_time_s

        if self._game_start_time_s is not None:
            self.game_time_s = raw_time_s - self._game_start_time_s

    def snapshot_tick_start(self, entity: Entity | None) -> None:
        """Record OpenDota's running clock at the start of an outer replay tick.

        odota/parser (Parse.java ``@OnTickStart``) sets its ``time`` from the
        game rules before a tick's messages are processed, so it reads the
        network tick the *previous* tick left behind; Clarity also holds
        combat-log entries back until ``@OnTickEnd``. Chat events inside the tick
        are therefore stamped with this value. The parser calls this once per
        outer-tick change, before the tick's inner messages, when
        :attr:`net_tick` has not yet advanced. It also latches the game start
        (:attr:`opendota_start_s`) the first time the entity carries it.

        Args:
            entity: The game-rules entity as of the previous tick, or ``None``.
        """
        if entity is None or not self.net_tick_seen:
            self.tick_start_raw_s = None
            return
        fields = entity._resolve_fields(_CLOCK_FIELDS)
        start = entity._get_float32_resolved(fields[0])
        if self.opendota_start_s is None and start is not None and start != 0.0:
            self.opendota_start_s = _round_positive_seconds(start)
        self.tick_start_raw_s = _raw_time_s(entity, fields, self.net_tick)

    def observe_game_start(self, entity: Entity, tick: int) -> bool:
        """Refresh the clock, and report whether the game has just started.

        The game starts when ``m_pGameRules.m_flGameStartTime`` first becomes
        non-zero.

        Args:
            entity: The game-rules entity.
            tick: Current replay tick.

        Returns:
            ``True`` exactly once: on the update where the start is first seen.
        """
        self.update(entity, tick)
        if self._game_start_seen:
            return False
        start = entity._get_float32_resolved(entity._resolve_fields(_CLOCK_FIELDS)[0])
        if start is None or start == 0.0:
            return False
        self._game_start_seen = True
        self.game_start_tick = tick
        self.clock.game_start_tick = tick
        self.clock.net_tick_offset = self.net_tick_offset(tick)
        return True

    def track_pause(
        self,
        paused: bool,
        pause_start_net_tick: int | None,
        total_paused_ticks: int | None,
        tick: int,
    ) -> None:
        """Record pause intervals from ``m_bGamePaused`` transitions.

        The pause start comes from ``m_nPauseStartTick`` and the length from the
        growth of ``m_nTotalPausedTicks``; both count network ticks, so they are
        shifted onto the replay-tick axis. The observed transition tick is the
        fallback when either field is missing.

        Args:
            paused: Current ``m_bGamePaused``.
            pause_start_net_tick: Current ``m_nPauseStartTick``.
            total_paused_ticks: Current ``m_nTotalPausedTicks``.
            tick: Current replay tick.
        """
        if paused == (self._open_pause is not None):
            return
        if paused:
            start = (
                pause_start_net_tick - self.net_tick_offset(tick) if pause_start_net_tick else tick
            )
            self._open_pause = (start, total_paused_ticks or 0)
            return
        assert self._open_pause is not None
        start, total_before = self._open_pause
        self._open_pause = None
        paused_ticks = (total_paused_ticks or 0) - total_before
        end = start + paused_ticks if paused_ticks > 0 else tick
        if end > start:
            self.clock.pauses.append(GamePause(start_tick=start, end_tick=end))

    def combat_log_time(self, timestamp: float | None, game_state: int | None) -> int | None:
        """Return OpenDota-style game-relative time for a combat-log entry.

        OpenDota anchors combat-log time at the ``GAME_IN_PROGRESS`` entry's
        timestamp, then subtracts that rounded timestamp from later ones. This
        also refreshes :attr:`combat_log_time_s`, and captures
        :attr:`duration_s` at the ``POST_GAME`` entry (odota/parser Parse.java).

        Args:
            timestamp: The entry's ``timestamp``, or ``None`` if absent.
            game_state: The new game state for a ``GAME_STATE`` entry, else ``None``.

        Returns:
            Seconds since the horn, or ``None`` before the anchor is seen.
        """
        if timestamp is None:
            return None
        raw_time_s = _round_positive_seconds(timestamp)
        if self._combat_log_start_s is None and game_state == DOTA_GAMERULES_STATE_GAME_IN_PROGRESS:
            self._combat_log_start_s = raw_time_s
            if self.opendota_start_s is None:
                self.opendota_start_s = raw_time_s
        if self._combat_log_start_s is None:
            return None
        game_time_s = raw_time_s - self._combat_log_start_s
        self.combat_log_time_s = game_time_s
        if self.duration_s is None and game_state == DOTA_GAMERULES_STATE_POST_GAME:
            self.duration_s = game_time_s
        return game_time_s

    def finish(self) -> None:
        """Close a pause still open when the replay ends."""
        if self._open_pause is not None:
            self.clock.pauses.append(GamePause(start_tick=self._open_pause[0], end_tick=None))
            self._open_pause = None
