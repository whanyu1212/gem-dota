"""OpenDota's tick-start clock for chat events: tracker, parser hook, assembly."""

from __future__ import annotations

from contextlib import contextmanager
from types import SimpleNamespace

import pytest

import gem.parser
from gem.combat.log import CombatLogEntry, CombatLogType
from gem.parser import ReplayParser
from gem.proto.dota_shared_enums_pb2 import DOTA_GAMERULES_STATE_GAME_IN_PROGRESS
from gem.proto.dota_usermessages_pb2 import (
    CHAT_MESSAGE_COURIER_LOST,
    CHAT_MESSAGE_FIRSTBLOOD,
    CHAT_MESSAGE_MINIBOSS_KILL,
    CHAT_MESSAGE_RUNE_PICKUP,
)
from gem.results.assembly import (
    _align_ticks,
    _apply_chat_events,
    _ChatEventTime,
    _first_blood_death,
    _retime_rune_pickups,
)
from gem.state.entities import Entity
from gem.state.game_clock import GameClockTracker
from tests._entities import set_fields


def _rules(start: float = 0.0, *, paused: bool = False, pause_start: int = 0) -> Entity:
    entity = Entity(
        index=0, serial=0, cls=SimpleNamespace(name="CDOTAGamerulesProxy", serializer=None)
    )
    set_fields(
        entity,
        {
            "m_pGameRules.m_flGameStartTime": start,
            "m_pGameRules.m_bGamePaused": paused,
            "m_pGameRules.m_nPauseStartTick": pause_start,
            "m_pGameRules.m_nTotalPausedTicks": 30,
        },
    )
    return entity


class TestTickStartClock:
    def test_snapshot_uses_the_network_tick_from_before_the_packet(self):
        tracker = GameClockTracker()
        tracker.on_net_tick(3014)  # (3014 - 30) / 30 = 99.47
        tracker.snapshot_tick_start(_rules())
        tracker.on_net_tick(3015)  # this tick's net_Tick: 99.5 would round to 100

        assert tracker.tick_start_raw_s == 99

    def test_pause_freezes_the_clock_at_the_pause_start(self):
        tracker = GameClockTracker()
        tracker.on_net_tick(9000)
        tracker.snapshot_tick_start(_rules(paused=True, pause_start=3030))

        assert tracker.tick_start_raw_s == 100  # (3030 - 30) / 30

    def test_unavailable_without_game_rules_or_a_network_tick(self):
        tracker = GameClockTracker()
        tracker.snapshot_tick_start(_rules())
        assert tracker.tick_start_raw_s is None
        tracker.on_net_tick(3000)
        tracker.snapshot_tick_start(None)
        assert tracker.tick_start_raw_s is None

    def test_start_anchor_latches_the_game_rules_when_seen_first(self):
        tracker = GameClockTracker()
        tracker.on_net_tick(3000)
        tracker.snapshot_tick_start(_rules(825.4))
        tracker.combat_log_time(826.6, DOTA_GAMERULES_STATE_GAME_IN_PROGRESS)

        assert tracker.opendota_start_s == 825

    def test_start_anchor_latches_the_combat_log_when_seen_first(self):
        tracker = GameClockTracker()
        tracker.combat_log_time(826.6, DOTA_GAMERULES_STATE_GAME_IN_PROGRESS)
        tracker.on_net_tick(3000)
        tracker.snapshot_tick_start(_rules(825.4))

        assert tracker.opendota_start_s == 827

    def test_no_anchor_until_the_start_is_known(self):
        tracker = GameClockTracker()
        tracker.on_net_tick(3000)
        tracker.snapshot_tick_start(_rules(0.0))

        assert tracker.opendota_start_s is None


class TestParserHook:
    def test_snapshot_once_per_outer_tick_before_its_messages(self, monkeypatch):
        packets = [(10, 7, b""), (10, 7, b""), (12, 7, b"")]

        @contextmanager
        def fake_stream(_source):
            yield iter(packets)

        monkeypatch.setattr(gem.parser, "DemoStream", fake_stream)
        parser = ReplayParser(b"")
        parser._clock.on_net_tick(18)
        snapshots = []
        monkeypatch.setattr(
            parser._clock,
            "snapshot_tick_start",
            lambda _entity: snapshots.append((parser.tick, parser._clock.net_tick)),
        )
        # Each packet carries its own net_Tick, applied while it is dispatched.
        monkeypatch.setattr(
            parser, "_dispatch_outer", lambda *_: parser._clock.on_net_tick(parser.tick * 2)
        )

        parser.parse()

        assert snapshots == [(10, 18), (12, 20)]


class TestGameRulesCache:
    def _manager(self, *entities):
        manager = SimpleNamespace(entities=list(entities))
        manager.find_by_class_name = lambda name: next(
            (e for e in manager.entities if e is not None and e.get_class_name() == name), None
        )
        return manager

    def test_deleted_and_recreated_game_rules_are_looked_up_again(self):
        parser = ReplayParser(b"")
        old = _rules(825.4)
        parser.entity_manager = self._manager(old)
        assert parser._game_rules_entity() is old

        # Delete removes the entity from the table but leaves ``active`` set.
        new = _rules(900.0)
        parser.entity_manager.entities[0] = new

        assert parser._game_rules_entity() is new

    def test_live_cached_entity_is_reused(self):
        parser = ReplayParser(b"")
        rules = _rules()
        manager = self._manager(rules)
        parser.entity_manager = manager
        parser._game_rules_entity()
        manager.find_by_class_name = lambda name: pytest.fail("cache not reused")

        assert parser._game_rules_entity() is rules


class TestAlignTicks:
    def test_prefers_exact_pairs_over_an_earlier_candidate(self):
        # Greedy matching would pair 80 with 0 and 100 with 80.
        assert _align_ticks([80, 100], [0, 80, 100], 90) == [(0, 1), (1, 2)]

    def test_keeps_both_pairs_when_each_is_in_window(self):
        assert _align_ticks([80, 100], [0, 90], 90) == [(0, 0), (1, 1)]

    def test_missing_event_leaves_the_right_objective_unpaired(self):
        assert _align_ticks([80, 100], [100], 90) == [(1, 0)]

    def test_nothing_pairs_outside_the_window(self):
        assert _align_ticks([10], [500], 90) == []

    @pytest.mark.parametrize("first,second", [([], [1]), ([1], [])])
    def test_empty_sequences(self, first, second):
        assert _align_ticks(first, second, 90) == []


def _event(
    type_: int,
    tick: int,
    raw_s: int | None,
    player: int = 0,
    value: int = 0,
    player2: int = -1,
):
    return _ChatEventTime(type_, player, value, tick, raw_s, player_id_2=player2)


class TestRetiming:
    def test_chat_objectives_take_their_chat_event_time(self):
        courier = {"time": 101, "type": "CHAT_MESSAGE_COURIER_LOST"}
        _apply_chat_events(
            {"CHAT_MESSAGE_COURIER_LOST": [(3000, courier)]},
            [_event(CHAT_MESSAGE_COURIER_LOST, 3003, 925)],
            825,
        )
        assert courier["time"] == 100

    def test_unmatched_or_clockless_objectives_keep_their_time(self):
        first_blood = {"time": 183, "type": "CHAT_MESSAGE_FIRSTBLOOD"}
        courier = {"time": 101, "type": "CHAT_MESSAGE_COURIER_LOST"}
        _apply_chat_events(
            {
                "CHAT_MESSAGE_FIRSTBLOOD": [(5000, first_blood)],
                "CHAT_MESSAGE_COURIER_LOST": [(3000, courier)],
            },
            [
                _event(CHAT_MESSAGE_FIRSTBLOOD, 9000, 1100),  # out of the window
                _event(CHAT_MESSAGE_COURIER_LOST, 3001, None),  # no clock
            ],
            825,
        )
        assert (first_blood["time"], courier["time"]) == (183, 101)

    def test_courier_lost_takes_team_killer_and_value_from_its_event(self):
        # Reference: odota/parser CreateParsedDataBlob.java handleCourierLost.
        courier = {"time": 101, "type": "CHAT_MESSAGE_COURIER_LOST", "team": 3, "killer": 3}
        _apply_chat_events(
            {"CHAT_MESSAGE_COURIER_LOST": [(3000, courier)]},
            [_event(CHAT_MESSAGE_COURIER_LOST, 3000, 925, player=5, value=85, player2=2)],
            825,
        )
        assert courier == {
            "time": 100,
            "type": "CHAT_MESSAGE_COURIER_LOST",
            "team": 2,
            "killer": 128,
            "value": 85,
        }

    def test_courier_lost_to_a_non_player_has_killer_minus_one(self):
        courier = {"time": 101, "type": "CHAT_MESSAGE_COURIER_LOST", "team": 2}
        _apply_chat_events(
            {"CHAT_MESSAGE_COURIER_LOST": [(3000, courier)]},
            [_event(CHAT_MESSAGE_COURIER_LOST, 3000, None, player=-1, value=30, player2=2)],
            825,
        )
        assert (courier["killer"], courier["team"], courier["value"]) == (-1, 2, 30)

    def test_miniboss_kill_takes_killer_and_team_from_its_event(self):
        # Reference: handleMinibossKill: slot = playerid_1, team = value.
        kill = {"time": 1223, "type": "CHAT_MESSAGE_MINIBOSS_KILL", "slot": 6, "team": 3}
        _apply_chat_events(
            {"CHAT_MESSAGE_MINIBOSS_KILL": [(37000, kill)]},
            [_event(CHAT_MESSAGE_MINIBOSS_KILL, 37000, None, player=8, value=3)],
            825,
        )
        assert kill == {
            "time": 1223,
            "type": "CHAT_MESSAGE_MINIBOSS_KILL",
            "slot": 8,
            "player_slot": 131,
            "team": 3,
        }

    def test_miniboss_kill_without_a_player_keeps_slot_minus_one(self):
        # OpenDota prints slot -1 and no player_slot.
        kill = {"time": 2090, "type": "CHAT_MESSAGE_MINIBOSS_KILL"}
        _apply_chat_events(
            {"CHAT_MESSAGE_MINIBOSS_KILL": [(60000, kill)]},
            [_event(CHAT_MESSAGE_MINIBOSS_KILL, 60000, None, player=-1, value=3)],
            825,
        )
        assert kill == {"time": 2090, "type": "CHAT_MESSAGE_MINIBOSS_KILL", "slot": -1, "team": 3}

    def test_first_blood_takes_killer_and_victim_from_its_event(self):
        # Reference: handleFirstblood: slot = playerid_1, key = playerid_2.
        first_blood = {"time": 344, "type": "CHAT_MESSAGE_FIRSTBLOOD", "slot": 2, "key": "4"}
        _apply_chat_events(
            {"CHAT_MESSAGE_FIRSTBLOOD": [(32849, first_blood)]},
            [_event(CHAT_MESSAGE_FIRSTBLOOD, 32849, None, player=0, player2=8)],
            825,
        )
        assert (first_blood["slot"], first_blood["player_slot"], first_blood["key"]) == (0, 0, "8")

    def test_rune_pickups_get_their_chat_event_time_even_before_the_anchor(self):
        base = {"log_type": CombatLogType.PICKUP_RUNE, "value": 3, "rune_type": 5}
        runes = [CombatLogEntry(tick=100, **base), CombatLogEntry(tick=200, **base)]
        _retime_rune_pickups(
            runes,
            [
                _event(CHAT_MESSAGE_RUNE_PICKUP, 100, 820, player=3, value=5),  # pre-horn
                _event(CHAT_MESSAGE_RUNE_PICKUP, 200, 1642, player=3, value=5),
            ],
            825,
        )
        assert [r.game_time_s for r in runes] == [-5, 817]

    def test_rune_pickup_without_its_chat_event_is_left_alone(self):
        rune = CombatLogEntry(tick=100, log_type=CombatLogType.PICKUP_RUNE, value=3, rune_type=5)
        _retime_rune_pickups([rune], [_event(CHAT_MESSAGE_RUNE_PICKUP, 100, 900, 4, 5)], 825)
        assert rune.game_time_s is None


def _hero_death(tick: int, **kwargs) -> CombatLogEntry:
    return CombatLogEntry(tick=tick, log_type=CombatLogType.DEATH, target_is_hero=True, **kwargs)


class TestFirstBloodDeath:
    def test_a_death_to_neutrals_before_first_blood_is_skipped(self):
        # 8855188139: Bane died to a neutral at tick 29725; first blood was
        # Shadow Fiend on Keeper of the Light at 32849.
        neutral = _hero_death(29725, target_name="npc_dota_hero_bane")
        first_blood = _hero_death(32849, target_name="npc_dota_hero_keeper_of_the_light")
        events = [_event(CHAT_MESSAGE_FIRSTBLOOD, 32849, None, player=0, player2=8)]
        assert _first_blood_death([neutral, first_blood], events) is first_blood

    def test_without_the_chat_event_the_first_real_hero_death_is_used(self):
        illusion = _hero_death(10, target_is_illusion=True)
        reincarnation = _hero_death(20, will_reincarnate=True)
        death = _hero_death(30)
        assert _first_blood_death([illusion, reincarnation, death], None) is death
        assert _first_blood_death([illusion], []) is None

    def test_a_chat_event_with_no_death_nearby_falls_back(self):
        death = _hero_death(30)
        events = [_event(CHAT_MESSAGE_FIRSTBLOOD, 9000, None)]
        assert _first_blood_death([death], events) is death
