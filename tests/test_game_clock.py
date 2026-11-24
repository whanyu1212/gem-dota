"""Tests for the pause-aware game clock and its parser and assembly consumers."""

from __future__ import annotations

from types import SimpleNamespace

from gem.analysis._shared import infer_match_end_tick
from gem.extractors.wards import WardEvent
from gem.parser import ReplayParser
from gem.results.assembly import _tick_game_seconds, _ward_left_entry
from gem.results.models import ParsedMatch
from gem.state.entities import Entity
from gem.state.game_clock import GameClock, GameClockTracker, GamePause, game_clock_for
from tests._entities import set_fields

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


class TestPauseTracking:
    def _tracker(self, *, net_tick: int) -> GameClockTracker:
        tracker = GameClockTracker()
        tracker.on_net_tick(net_tick)
        return tracker

    def test_pause_is_shifted_from_network_ticks_to_replay_ticks(self) -> None:
        tracker = self._tracker(net_tick=58814)
        tracker.track_pause(True, 58813, 0, tick=58419)
        tracker.on_net_tick(59468)
        tracker.track_pause(False, 0, 654, tick=59073)
        assert tracker.clock.pauses == [GamePause(start_tick=58418, end_tick=59072)]

    def test_repeated_state_is_ignored(self) -> None:
        tracker = self._tracker(net_tick=100)
        tracker.track_pause(False, 0, 0, tick=100)
        tracker.track_pause(True, 100, 0, tick=100)
        tracker.track_pause(True, 100, 0, tick=100)
        tracker.on_net_tick(250)
        tracker.track_pause(False, 0, 150, tick=250)
        assert tracker.clock.pauses == [GamePause(100, 250)]

    def test_missing_pause_fields_fall_back_to_observed_ticks(self) -> None:
        tracker = self._tracker(net_tick=100)
        tracker.track_pause(True, None, None, tick=100)
        tracker.on_net_tick(190)
        tracker.track_pause(False, None, None, tick=190)
        assert tracker.clock.pauses == [GamePause(100, 190)]

    def test_pause_open_at_the_end_is_kept_open_ended(self) -> None:
        tracker = self._tracker(net_tick=100)
        tracker.track_pause(True, 100, 0, tick=100)
        tracker.finish()
        assert tracker.clock.pauses == [GamePause(100, None)]

    def test_odd_tick_pause_uses_last_unpaused_total(self) -> None:
        tracker = self._tracker(net_tick=200)
        tracker.track_pause(False, 0, 0, tick=200)
        # First pause started on odd net_tick 201, observed at 202 with total=1.
        tracker.on_net_tick(202)
        tracker.track_pause(True, 201, 1, tick=202)
        tracker.on_net_tick(302)
        tracker.track_pause(False, 0, 101, tick=302)
        # Second pause started on odd net_tick 401, observed at 402 with total=102.
        tracker.on_net_tick(400)
        tracker.track_pause(False, 0, 101, tick=400)
        tracker.on_net_tick(402)
        tracker.track_pause(True, 401, 102, tick=402)
        tracker.on_net_tick(452)
        tracker.track_pause(False, 0, 152, tick=452)

        assert tracker.clock.pauses == [GamePause(201, 302), GamePause(401, 452)]
        assert tracker.clock.paused_ticks_before(500) == 152

    def test_unpaused_sample_without_total_clears_cached_baseline(self) -> None:
        tracker = self._tracker(net_tick=200)
        tracker.track_pause(False, 0, 10, tick=200)
        # Subsequent unpaused sample omits m_nTotalPausedTicks, clearing (200, 10).
        tracker.on_net_tick(201)
        tracker.track_pause(False, 0, None, tick=201)
        tracker.on_net_tick(203)
        tracker.track_pause(True, 202, 11, tick=203)
        tracker.on_net_tick(252)
        tracker.track_pause(False, 0, 60, tick=252)

        assert tracker.clock.pauses == [GamePause(202, 251)]

    def test_missing_pause_start_keeps_first_paused_total(self) -> None:
        tracker = self._tracker(net_tick=200)
        tracker.track_pause(False, 0, 0, tick=200)
        tracker.on_net_tick(202)
        tracker.track_pause(True, None, 1, tick=202)
        tracker.on_net_tick(302)
        tracker.track_pause(False, 0, 101, tick=302)

        assert tracker.clock.pauses == [GamePause(202, 302)]

    def test_stale_unpaused_total_across_gap_is_ignored(self) -> None:
        tracker = self._tracker(net_tick=100)
        tracker.track_pause(False, 0, 0, tick=100)
        # Gap skips a 120-tick pause; next observed pause starts at 1000 and is
        # first seen late at 1200 (so tick - start > 120), resuming at 1300.
        tracker.on_net_tick(1200)
        tracker.track_pause(True, 1000, 120, tick=1200)
        tracker.on_net_tick(1300)
        tracker.track_pause(False, 0, 420, tick=1300)

        assert tracker.clock.pauses == [GamePause(1000, 1300)]


class TestRawClock:
    """The raw (unshifted) clock is readable in pregame, as OpenDota's ``time``."""

    @staticmethod
    def _rules(start: float) -> Entity:
        entity = Entity(
            index=0, serial=0, cls=SimpleNamespace(name="CDOTAGamerulesProxy", serializer=None)
        )
        set_fields(
            entity,
            {
                "m_pGameRules.m_flGameStartTime": start,
                "m_pGameRules.m_bGamePaused": False,
                "m_pGameRules.m_nTotalPausedTicks": 30,
            },
        )
        return entity

    def test_raw_clock_is_set_before_the_game_start(self) -> None:
        tracker = GameClockTracker()
        tracker.on_net_tick(24_761)
        tracker.update(self._rules(0.0), tick=24_313)
        assert tracker.raw_time_s == 824  # (24761 - 30) / 30 = 824.37
        assert tracker.game_time_s is None

    def test_game_time_is_the_raw_clock_minus_the_rounded_start(self) -> None:
        tracker = GameClockTracker()
        tracker.on_net_tick(24_798)
        tracker.update(self._rules(825.4), tick=24_350)
        assert tracker.raw_time_s == 826  # (24798 - 30) / 30 = 825.6
        assert tracker.game_time_s == 1  # the start rounds to 825


class TestParserGameEnd:
    def test_post_game_marker_records_tick(self) -> None:
        parser = ReplayParser(b"")
        parser.tick = 5000
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
