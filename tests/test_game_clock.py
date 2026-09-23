"""Tests for the pause-aware game clock and its parser/assembly/report consumers."""

from __future__ import annotations

import pytest

from gem.analysis._shared import infer_match_end_tick
from gem.extractors.wards import WardEvent
from gem.parser import ReplayParser
from gem.reports._formatting import (
    fmt_tick,
    set_game_clock,
    set_game_start_tick,
    tick_after_game_seconds,
)
from gem.reports.sections.match import build_header
from gem.results.assembly import _tick_game_seconds, _ward_left_entry
from gem.results.models import ParsedMatch
from gem.state.game_clock import GameClock, GamePause, game_clock_for

# One 600-tick (20 s) pause starting 60 s after a horn at tick 1000.
_PAUSED = GameClock(
    game_start_tick=1000,
    pauses=[GamePause(start_tick=2800, end_tick=3400)],
)


class TestGameClock:
    def test_without_pauses_matches_tick_offset(self) -> None:
        clock = GameClock(game_start_tick=1000)
        assert clock.game_time_at(1000) == 0
        assert clock.game_time_at(1900) == 30
        assert clock.game_seconds_at(1915) == 30
        assert clock.game_seconds_at(985) == -1

    def test_clock_freezes_during_pause_and_resumes_after(self) -> None:
        assert _PAUSED.game_time_at(2800) == 60
        assert _PAUSED.game_time_at(3100) == 60
        assert _PAUSED.game_time_at(3400) == 60
        assert _PAUSED.game_time_at(3430) == 61
        assert _PAUSED.paused_ticks_before(3100) == 300
        assert _PAUSED.paused_ticks_before(9000) == 600

    def test_pause_before_horn_does_not_shift_game_time(self) -> None:
        clock = GameClock(game_start_tick=1000, pauses=[GamePause(100, 400)])
        assert clock.game_time_at(1000) == 0
        assert clock.game_time_at(1300) == 10
        assert clock.game_time_at(700) == -10

    def test_open_pause_freezes_until_replay_end(self) -> None:
        clock = GameClock(game_start_tick=0, pauses=[GamePause(300, None)])
        assert clock.game_time_at(10_000) == 10
        assert clock.pauses[0].duration_ticks is None
        assert clock.tick_at(11) is None

    def test_tick_at_inverts_pause_aware_time(self) -> None:
        assert _PAUSED.tick_at(0) == 1000
        assert _PAUSED.tick_at(60) == 2800
        assert _PAUSED.tick_at(61) == 3430
        for tick in (1000, 2000, 3400, 3430, 9000):
            game_time = _PAUSED.game_time_at(tick)
            assert game_time is not None
            assert _PAUSED.game_time_at(_PAUSED.tick_at(game_time) or 0) == game_time

    def test_engine_anchors_reproduce_opendota_rounding(self) -> None:
        # m_flGameStartTime = 690.3 s with network ticks 395 ahead of replay ticks,
        # as in TI2026 match 8860187335.
        clock = GameClock(
            game_start_tick=20315,
            game_start_time_s=690.3,
            net_tick_offset=395,
            pauses=[GamePause(58418, 59072)],
        )
        # round((tick + 395 - paused) / 30) - round(690.3), Java half-up rounding.
        assert clock.game_seconds_at(21369) == 35
        assert clock.game_seconds_at(111128) == round((111128 + 395 - 654) / 30) - 690
        assert clock.game_seconds_at(111128) == 3006

    def test_unknown_game_start(self) -> None:
        clock = GameClock()
        assert clock.game_time_at(500) is None
        assert clock.game_seconds_at(500) is None
        assert clock.tick_at(0) is None
        assert clock.format_tick(500) == "--:--"

    def test_format_tick(self) -> None:
        assert _PAUSED.format_tick(3430) == "01:01"
        assert _PAUSED.format_tick(100) == "-00:30"

    def test_game_clock_for_falls_back_to_start_tick(self) -> None:
        match = ParsedMatch(game_start_tick=900)
        clock = game_clock_for(match)
        assert clock.game_start_tick == 900
        assert clock.pauses == []
        match.game_clock = _PAUSED
        assert game_clock_for(match) is _PAUSED


class TestParserPauseTracking:
    def _parser(self, *, tick: int, net_tick: int) -> ReplayParser:
        parser = ReplayParser(b"")
        parser.tick = tick
        parser.net_tick = net_tick
        parser._net_tick_seen = True
        return parser

    def test_pause_is_shifted_from_network_ticks_to_replay_ticks(self) -> None:
        parser = self._parser(tick=58419, net_tick=58814)
        parser._track_pause(True, 58813, 0)
        parser.tick, parser.net_tick = 59073, 59468
        parser._track_pause(False, 0, 654)
        assert parser.game_clock.pauses == [GamePause(start_tick=58418, end_tick=59072)]

    def test_repeated_state_is_ignored(self) -> None:
        parser = self._parser(tick=100, net_tick=100)
        parser._track_pause(False, 0, 0)
        parser._track_pause(True, 100, 0)
        parser._track_pause(True, 100, 0)
        parser.tick = parser.net_tick = 250
        parser._track_pause(False, 0, 150)
        assert parser.game_clock.pauses == [GamePause(100, 250)]

    def test_missing_pause_fields_fall_back_to_observed_ticks(self) -> None:
        parser = self._parser(tick=100, net_tick=100)
        parser._track_pause(True, None, None)
        parser.tick = parser.net_tick = 190
        parser._track_pause(False, None, None)
        assert parser.game_clock.pauses == [GamePause(100, 190)]

    def test_post_game_marker_records_tick(self) -> None:
        parser = self._parser(tick=5000, net_tick=5000)
        parser._mark_game_end(5000)
        parser._mark_game_end(6000)
        assert parser.post_game_tick == 5000


class TestAssemblyTimes:
    def test_tick_seconds_subtract_pauses(self) -> None:
        assert _tick_game_seconds(3430, _PAUSED) == 61
        assert _tick_game_seconds(3430, GameClock()) == 0

    def test_ward_left_time_is_pause_aware(self) -> None:
        ward = WardEvent(
            tick=1300,
            player_id=0,
            team=2,
            ward_type="observer",
            x=100.0,
            y=100.0,
            placer="npc_dota_hero_axe",
            expires_tick=None,
            killed_tick=3430,
            killer="npc_dota_hero_axe",
        )
        entry = _ward_left_entry(ward, _PAUSED)
        assert entry is not None
        assert entry["time"] == 61


class TestMatchEndTick:
    def test_prefers_post_game_over_recording_end(self) -> None:
        match = ParsedMatch(game_end_tick=138878, post_game_tick=111131)
        assert infer_match_end_tick(match) == 111131

    def test_falls_back_to_recording_end(self) -> None:
        assert infer_match_end_tick(ParsedMatch(game_end_tick=5000)) == 5000


class TestReportClock:
    def teardown_method(self) -> None:
        set_game_start_tick(0)

    def test_fmt_tick_uses_configured_clock(self) -> None:
        set_game_clock(_PAUSED)
        assert fmt_tick(3430) == "01:01"
        set_game_start_tick(1000)
        assert fmt_tick(3430) == "01:21"

    def test_timers_stop_during_pauses(self) -> None:
        set_game_clock(_PAUSED)
        # 60 s before the pause plus 20 s of pause: a 2 s timer from 59 s ends at 61 s.
        assert tick_after_game_seconds(2770, 2) == 3430
        set_game_start_tick(1000)
        assert tick_after_game_seconds(2770, 2) == 2830

    @pytest.mark.parametrize(
        ("duration", "expected"),
        [(3005, "50:05"), (0, "01:00")],
    )
    def test_header_duration_ignores_post_game_recording(
        self, duration: int, expected: str
    ) -> None:
        set_game_start_tick(0)
        match = ParsedMatch(
            game_start_tick=0,
            game_end_tick=118_560,
            post_game_tick=1800,
            duration=duration,
        )
        html = build_header(match, fmt_tick, {})
        assert expected in html
        assert "65:52" not in html
