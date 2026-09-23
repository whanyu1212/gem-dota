"""Pause-aware conversion between replay ticks and the in-game clock.

Replay ticks keep advancing while a match is paused, but the in-game clock does
not. Since Dota 2 7.32e the game-rules entity no longer carries
``m_fGameTime``; the clock is ``(server_tick - m_nTotalPausedTicks) / 30``,
frozen at ``m_nPauseStartTick`` while paused, and shifted by
``m_flGameStartTime``. :class:`GameClock` records the anchors and pause
intervals needed to reproduce that clock for any replay tick after parsing.

Reference: odota/parser src/main/java/opendota/Parse.java (game-time and pause
tracking in ``onTickStart``; pinned revision in CLAUDE.md).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

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
