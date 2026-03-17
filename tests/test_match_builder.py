"""Tests for gem.match_builder — ParsedMatch assembly.

Tests cover:
- _radiant_win_from_ancient (pure unit logic)
- build_parsed_match (via minimal stubs for all extractor/parser dependencies)

Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java
"""

from __future__ import annotations

from dataclasses import dataclass, field
from unittest.mock import MagicMock

import pytest

from gem.combatlog import CombatLogEntry
from gem.match_builder import _radiant_win_from_ancient, build_parsed_match
from gem.models import ChatEntry, ParsedMatch, SmokeEvent

# ---------------------------------------------------------------------------
# Helpers — minimal stubs
# ---------------------------------------------------------------------------


def _death(target: str, tick: int = 1) -> CombatLogEntry:
    return CombatLogEntry(tick=tick, log_type="DEATH", target_name=target)


def _buyback(pid: int, tick: int = 1) -> CombatLogEntry:
    return CombatLogEntry(tick=tick, log_type="BUYBACK", value=pid)


def _damage_entry(pid_attacker_name: str = "hero_a", tick: int = 100) -> CombatLogEntry:
    return CombatLogEntry(tick=tick, log_type="DAMAGE", attacker_name=pid_attacker_name)


# ---------------------------------------------------------------------------
# Minimal TimeSeries stub
# ---------------------------------------------------------------------------


@dataclass
class _FakeTimeSeries:
    ticks: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    total_earned_gold_t: list[int] = field(default_factory=list)
    total_earned_xp_t: list[int] = field(default_factory=list)
    total_hero_damage_t: list[int] = field(default_factory=list)
    total_hero_healing_t: list[int] = field(default_factory=list)
    total_deaths_t: list[int] = field(default_factory=list)
    total_stuns_t: list[float] = field(default_factory=list)


@dataclass
class _FakePlayerSnapshot:
    player_id: int
    tick: int
    npc_name: str
    team: int
    x: float | None = None
    y: float | None = None
    ability_levels: dict = field(default_factory=dict)


def _make_parser(
    match_id: int = 1001,
    radiant_win: bool | None = True,
    tick: int = 100000,
    game_start_tick: int | None = 6000,
    game_mode: int = 22,
    leagueid: int = 0,
    entity_manager=None,
) -> MagicMock:
    p = MagicMock()
    p.match_id = match_id
    p.radiant_win = radiant_win
    p.tick = tick
    p.game_start_tick = game_start_tick
    p.game_mode = game_mode
    p.leagueid = leagueid
    p.entity_manager = entity_manager
    return p


def _make_player_ext(
    snapshots=None,
    scoreboard=None,
    first_snapshot_tick=None,
    sample_interval: int = 30,
) -> MagicMock:
    ext = MagicMock()
    ext.snapshots = snapshots or []
    ext.scoreboard = scoreboard or {}
    ext.first_snapshot_tick = first_snapshot_tick or {}
    ext._sample_interval = sample_interval

    ts = _FakeTimeSeries()
    ext.time_series.return_value = ts
    ext.minute_time_series.return_value = ts
    return ext


def _make_obj_ext(
    towers=None, barracks=None, roshan=None, aegis=None, tormentors=None, shrines=None
) -> MagicMock:
    ext = MagicMock()
    ext.tower_kills = towers or []
    ext.barracks_kills = barracks or []
    ext.roshan_kills = roshan or []
    ext.aegis_events = aegis or []
    ext.tormentor_kills = tormentors or []
    ext.shrine_kills = shrines or []
    return ext


def _make_ward_ext(ward_events=None) -> MagicMock:
    ext = MagicMock()
    ext.ward_events = ward_events or []
    return ext


def _make_courier_ext(snapshots=None) -> MagicMock:
    ext = MagicMock()
    ext.snapshots = snapshots or []
    return ext


def _make_draft_ext(draft_events=None) -> MagicMock:
    ext = MagicMock()
    ext.draft_events = draft_events or []
    return ext


def _make_combat_agg() -> MagicMock:
    agg = MagicMock()
    agg.players = {}
    return agg


# ---------------------------------------------------------------------------
# _radiant_win_from_ancient
# ---------------------------------------------------------------------------


class TestRadiantWinFromAncient:
    def test_badguys_fort_death_returns_true(self):
        entries = [_death("npc_dota_badguys_fort")]
        assert _radiant_win_from_ancient(entries) is True

    def test_goodguys_fort_death_returns_false(self):
        entries = [_death("npc_dota_goodguys_fort")]
        assert _radiant_win_from_ancient(entries) is False

    def test_no_fort_death_returns_none(self):
        entries = [_death("npc_dota_hero_axe"), _death("npc_dota_goodguys_tower1_top")]
        assert _radiant_win_from_ancient(entries) is None

    def test_empty_log_returns_none(self):
        assert _radiant_win_from_ancient([]) is None

    def test_non_death_entries_are_ignored(self):
        """Only DEATH type entries should be inspected."""
        entries = [
            CombatLogEntry(tick=1, log_type="DAMAGE", target_name="npc_dota_badguys_fort"),
            CombatLogEntry(tick=2, log_type="HEAL", target_name="npc_dota_goodguys_fort"),
        ]
        assert _radiant_win_from_ancient(entries) is None

    def test_first_matching_fort_death_wins(self):
        """Only the first fort death matters; later ones are ignored."""
        entries = [
            _death("npc_dota_badguys_fort", tick=100),
            _death("npc_dota_goodguys_fort", tick=200),
        ]
        assert _radiant_win_from_ancient(entries) is True

    def test_goodguys_fort_first_returns_false(self):
        entries = [
            _death("npc_dota_goodguys_fort", tick=50),
            _death("npc_dota_badguys_fort", tick=200),
        ]
        assert _radiant_win_from_ancient(entries) is False


# ---------------------------------------------------------------------------
# build_parsed_match — basic smoke tests
# ---------------------------------------------------------------------------


class TestBuildParsedMatchSmoke:
    def _build(self, **kwargs) -> ParsedMatch:
        parser = _make_parser(**kwargs)
        player_ext = _make_player_ext()
        obj_ext = _make_obj_ext()
        ward_ext = _make_ward_ext()
        courier_ext = _make_courier_ext()
        draft_ext = _make_draft_ext()
        combat_agg = _make_combat_agg()
        return build_parsed_match(
            parser, player_ext, obj_ext, ward_ext, courier_ext, draft_ext, combat_agg, [], []
        )

    def test_returns_parsed_match(self):
        m = self._build()
        assert isinstance(m, ParsedMatch)

    def test_match_id_propagated(self):
        m = self._build(match_id=9999)
        assert m.match_id == 9999

    def test_game_mode_propagated(self):
        m = self._build(game_mode=22)
        assert m.game_mode == 22

    def test_leagueid_propagated(self):
        m = self._build(leagueid=15000)
        assert m.leagueid == 15000

    def test_game_end_tick_equals_parser_tick(self):
        m = self._build(tick=54321)
        assert m.game_end_tick == 54321

    def test_game_start_tick_propagated(self):
        m = self._build(game_start_tick=6000)
        assert m.game_start_tick == 6000

    def test_has_ten_players(self):
        m = self._build()
        assert len(m.players) == 10

    def test_player_ids_set(self):
        m = self._build()
        for i, pp in enumerate(m.players):
            assert pp.player_id == i


# ---------------------------------------------------------------------------
# radiant_win — three-tier resolution
# ---------------------------------------------------------------------------


class TestBuildParsedMatchRadiantWin:
    def _build_with_entries(self, parser_radiant_win, entries):
        parser = _make_parser(radiant_win=parser_radiant_win)
        player_ext = _make_player_ext()
        return build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            entries,
            [],
        )

    def test_parser_radiant_win_true_wins(self):
        m = self._build_with_entries(True, [])
        assert m.radiant_win is True

    def test_parser_radiant_win_false_wins(self):
        m = self._build_with_entries(False, [])
        assert m.radiant_win is False

    def test_none_falls_back_to_combat_log(self):
        entries = [_death("npc_dota_badguys_fort")]
        m = self._build_with_entries(None, entries)
        assert m.radiant_win is True

    def test_none_and_no_fort_gives_none(self):
        m = self._build_with_entries(None, [])
        assert m.radiant_win is None


# ---------------------------------------------------------------------------
# Extractor outputs plumbed through
# ---------------------------------------------------------------------------


class TestBuildParsedMatchExtractorOutputs:
    def _base_build(self, **kw) -> ParsedMatch:
        parser = _make_parser()
        player_ext = _make_player_ext()
        return build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(**kw.get("obj", {})),
            _make_ward_ext(**kw.get("ward", {})),
            _make_courier_ext(**kw.get("courier", {})),
            _make_draft_ext(**kw.get("draft", {})),
            _make_combat_agg(),
            kw.get("entries", []),
            kw.get("chat", []),
            smoke_events=kw.get("smoke_events"),
        )

    def test_combat_log_stored(self):
        entries = [_death("npc_dota_hero_axe")]
        m = self._base_build(entries=entries)
        assert m.combat_log is entries

    def test_chat_stored(self):
        chat = [ChatEntry(tick=1, player_slot=0, channel="all", text="gg")]
        m = self._base_build(chat=chat)
        assert m.chat is chat

    def test_smoke_events_stored(self):
        smokes = [SmokeEvent(tick=100, activator="npc_dota_hero_axe", team=2)]
        m = self._base_build(smoke_events=smokes)
        assert m.smoke_events is smokes

    def test_smoke_events_defaults_to_empty_list_when_none(self):
        m = self._base_build(smoke_events=None)
        assert m.smoke_events == []

    def test_draft_events_stored(self):
        from gem.extractors.draft import DraftEvent

        draft = [
            DraftEvent(
                tick=1, slot_index=0, hero_id=1, hero_name="npc_dota_hero_axe", is_pick=True, team=2
            )
        ]
        m = self._base_build(draft={"draft_events": draft})
        assert m.draft is draft

    def test_courier_snapshots_stored(self):
        from gem.extractors.courier import CourierSnapshot

        snaps = [CourierSnapshot(tick=1, team=2, state=0, flying=False, x=0.0, y=0.0)]
        m = self._base_build(courier={"snapshots": snaps})
        assert m.courier_snapshots is snaps


# ---------------------------------------------------------------------------
# Buyback — post-processing
# ---------------------------------------------------------------------------


class TestBuildParsedMatchBuyback:
    def test_buyback_entries_routed_to_correct_player(self):
        from gem.combat_aggregator import _ParsedPlayerAgg

        # Make real per-player aggregators
        aggs = {i: _ParsedPlayerAgg() for i in range(10)}
        combat_agg = MagicMock()
        combat_agg.players = aggs
        combat_agg._agg.side_effect = lambda pid: aggs[pid]

        entries = [
            _buyback(pid=3, tick=5000),
            _buyback(pid=7, tick=6000),
        ]
        parser = _make_parser()
        player_ext = _make_player_ext()
        build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            combat_agg,
            entries,
            [],
        )

        assert entries[0] in aggs[3].buyback_log
        assert entries[1] in aggs[7].buyback_log

    def test_buyback_with_invalid_pid_not_routed(self):
        from gem.combat_aggregator import _ParsedPlayerAgg

        aggs = {i: _ParsedPlayerAgg() for i in range(10)}
        combat_agg = MagicMock()
        combat_agg.players = aggs
        combat_agg._agg.side_effect = lambda pid: aggs[pid]

        # pid=10 is out of range — should not raise, should not be routed
        entries = [_buyback(pid=10, tick=1000)]
        parser = _make_parser()
        player_ext = _make_player_ext()
        build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            combat_agg,
            entries,
            [],
        )

        for agg in aggs.values():
            assert agg.buyback_log == []


# ---------------------------------------------------------------------------
# Player fields from combat_aggregator
# ---------------------------------------------------------------------------


class TestBuildParsedMatchPlayerCombatFields:
    def test_combat_agg_fields_applied_to_correct_player(self):
        from gem.combat_aggregator import _ParsedPlayerAgg

        agg3 = _ParsedPlayerAgg()
        agg3.damage = {"npc_dota_hero_axe": 1000}
        agg3.damage_taken = {"npc_dota_hero_sven": 500}
        agg3.damage_by_type = {"physical": 1000}
        agg3.damage_taken_by_type = {"magical": 500}
        agg3.healing = {}
        agg3.ability_uses = {"axe_battle_hunger": 5}
        agg3.item_uses = {}
        agg3.gold_reasons = {}
        agg3.xp_reasons = {}
        agg3.kills_log = []
        agg3.purchase_log = []
        agg3.runes_log = []
        agg3.buyback_log = []
        agg3.stuns_dealt = 2.5

        combat_agg = MagicMock()
        combat_agg.players = {3: agg3}
        combat_agg._agg.side_effect = lambda pid: {3: agg3}[pid]

        parser = _make_parser()
        player_ext = _make_player_ext(first_snapshot_tick={3: 0})
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            combat_agg,
            [],
            [],
        )

        pp = m.players[3]
        assert pp.damage == agg3.damage
        assert pp.damage_taken == agg3.damage_taken
        assert pp.damage_by_type == agg3.damage_by_type
        assert pp.ability_uses == agg3.ability_uses
        assert pp.stuns_dealt == pytest.approx(2.5)


# ---------------------------------------------------------------------------
# Scoreboard KDA
# ---------------------------------------------------------------------------


class TestBuildParsedMatchKDA:
    def test_kda_from_scoreboard(self):
        parser = _make_parser()
        player_ext = _make_player_ext(scoreboard={0: (10, 2, 5), 9: (1, 10, 3)})
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert (m.players[0].kills, m.players[0].deaths, m.players[0].assists) == (10, 2, 5)
        assert (m.players[9].kills, m.players[9].deaths, m.players[9].assists) == (1, 10, 3)

    def test_players_without_scoreboard_have_zero_kda(self):
        parser = _make_parser()
        player_ext = _make_player_ext(scoreboard={})
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        for pp in m.players:
            assert pp.kills == 0
            assert pp.deaths == 0
            assert pp.assists == 0


# ---------------------------------------------------------------------------
# Hero name + team from snapshots
# ---------------------------------------------------------------------------


class TestBuildParsedMatchHeroName:
    def test_hero_name_from_first_snapshot(self):
        snaps = [_FakePlayerSnapshot(player_id=2, tick=100, npc_name="npc_dota_hero_axe", team=2)]
        parser = _make_parser()
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert m.players[2].hero_name == "npc_dota_hero_axe"
        assert m.players[2].team == 2

    def test_hero_name_only_for_matching_player(self):
        snaps = [_FakePlayerSnapshot(player_id=1, tick=100, npc_name="npc_dota_hero_sven", team=3)]
        parser = _make_parser()
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert m.players[1].hero_name == "npc_dota_hero_sven"
        assert m.players[0].hero_name == ""  # no snapshot for player 0


# ---------------------------------------------------------------------------
# Ward log assignment
# ---------------------------------------------------------------------------


class TestBuildParsedMatchWards:
    def test_observer_ward_assigned_to_player(self):
        from gem.extractors.wards import WardEvent

        ward = WardEvent(
            tick=500,
            player_id=4,
            placer="npc_dota_hero_axe",
            ward_type="observer",
            team=2,
            x=100.0,
            y=200.0,
            expires_tick=None,
            killed_tick=None,
            killer="",
        )
        parser = _make_parser()
        player_ext = _make_player_ext()
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(ward_events=[ward]),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert ward in m.players[4].obs_log
        assert ward not in m.players[4].sen_log

    def test_sentry_ward_assigned_to_player(self):
        from gem.extractors.wards import WardEvent

        ward = WardEvent(
            tick=600,
            player_id=5,
            placer="npc_dota_hero_sven",
            ward_type="sentry",
            team=3,
            x=0.0,
            y=0.0,
            expires_tick=None,
            killed_tick=None,
            killer="",
        )
        parser = _make_parser()
        player_ext = _make_player_ext()
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(ward_events=[ward]),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert ward in m.players[5].sen_log
        assert ward not in m.players[5].obs_log

    def test_ward_with_invalid_player_id_not_assigned(self):
        from gem.extractors.wards import WardEvent

        ward = WardEvent(
            tick=700,
            player_id=99,
            placer="npc_dota_hero_axe",
            ward_type="observer",
            team=2,
            x=0.0,
            y=0.0,
            expires_tick=None,
            killed_tick=None,
            killer="",
        )
        parser = _make_parser()
        player_ext = _make_player_ext()
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(ward_events=[ward]),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        for pp in m.players:
            assert pp.obs_log == []
            assert pp.sen_log == []


# ---------------------------------------------------------------------------
# radiant_gold_adv / radiant_xp_adv
# ---------------------------------------------------------------------------


class TestBuildParsedMatchGoldXpAdv:
    def _build_with_ts(self, player_ts: dict[int, tuple[list[int], list[int], int]]) -> ParsedMatch:
        """player_ts: {player_id: (total_earned_gold, total_earned_xp, team)}"""
        ext = _make_player_ext()

        def make_ts(gold, xp):
            ts = _FakeTimeSeries()
            ts.total_earned_gold_t = gold
            ts.total_earned_xp_t = xp
            return ts

        def ts_for(pid):
            if pid in player_ts:
                gold, xp, _ = player_ts[pid]
                return make_ts(gold, xp)
            return _FakeTimeSeries()

        ext.time_series.side_effect = ts_for
        ext.minute_time_series.side_effect = ts_for

        # Build snapshot with team info
        snaps = []
        for pid, (_, _, team) in player_ts.items():
            snaps.append(_FakePlayerSnapshot(pid, 100, f"npc_dota_hero_hero{pid}", team))
        ext.snapshots = snaps

        parser = _make_parser()
        return build_parsed_match(
            parser,
            ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

    def test_radiant_ahead(self):
        """Radiant player has more gold than Dire player → positive adv."""
        ts = {
            0: ([1000, 2000], [500, 1000], 2),  # Radiant
            5: ([500, 1000], [200, 400], 3),  # Dire
        }
        m = self._build_with_ts(ts)
        # adv[0] = 1000 - 500 = 500, adv[1] = 2000 - 1000 = 1000
        assert m.radiant_gold_adv[0] == 500
        assert m.radiant_gold_adv[1] == 1000

    def test_dire_ahead(self):
        ts = {
            0: ([100, 200], [50, 100], 2),  # Radiant
            5: ([600, 1200], [300, 600], 3),  # Dire
        }
        m = self._build_with_ts(ts)
        assert m.radiant_gold_adv[0] == 100 - 600  # negative
        assert m.radiant_gold_adv[1] == 200 - 1200

    def test_no_active_players_produces_empty_adv(self):
        """When no players have time series, adv arrays should be empty."""
        m = self._build_with_ts({})
        assert m.radiant_gold_adv == []
        assert m.radiant_xp_adv == []


# ---------------------------------------------------------------------------
# Position log
# ---------------------------------------------------------------------------


class TestBuildParsedMatchPositionLog:
    def test_position_log_populated_from_snapshots(self):
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=100, npc_name="n", team=2, x=10.0, y=20.0),
            _FakePlayerSnapshot(player_id=0, tick=130, npc_name="n", team=2, x=15.0, y=25.0),
            _FakePlayerSnapshot(player_id=1, tick=100, npc_name="n2", team=3, x=50.0, y=60.0),
        ]
        parser = _make_parser()
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        pos0 = m.players[0].position_log
        assert (100, 10.0, 20.0) in pos0
        assert (130, 15.0, 25.0) in pos0
        # player 1's position should NOT be in player 0's log
        assert (100, 50.0, 60.0) not in pos0

    def test_snapshots_with_none_position_excluded(self):
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=100, npc_name="n", team=2, x=None, y=None),
            _FakePlayerSnapshot(player_id=0, tick=130, npc_name="n", team=2, x=5.0, y=6.0),
        ]
        parser = _make_parser()
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        pos0 = m.players[0].position_log
        # Only the snapshot with real coords should appear
        assert len(pos0) == 1
        assert pos0[0] == (130, 5.0, 6.0)


# ---------------------------------------------------------------------------
# Lane position heatmap
# ---------------------------------------------------------------------------


class TestBuildParsedMatchLanePos:
    def test_lane_pos_counts_within_window(self):
        # game_start_tick=6000, window = 6000 + 600*30 = 24000
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=6000, npc_name="n", team=2, x=128.0, y=256.0),
            _FakePlayerSnapshot(player_id=0, tick=12000, npc_name="n", team=2, x=128.0, y=256.0),
        ]
        parser = _make_parser(game_start_tick=6000)
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        # 128//64 = 2, 256//64 = 4 → cell "2_4"
        lane_pos = m.players[0].lane_pos
        assert lane_pos.get("2_4", 0) == 2

    def test_lane_pos_excludes_ticks_before_game_start(self):
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=100, npc_name="n", team=2, x=0.0, y=0.0),
        ]
        parser = _make_parser(game_start_tick=6000)
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert sum(m.players[0].lane_pos.values()) == 0

    def test_lane_pos_excludes_ticks_after_window(self):
        # game_start_tick=0, window end = 600*30=18000
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=99999, npc_name="n", team=2, x=0.0, y=0.0),
        ]
        parser = _make_parser(game_start_tick=0)
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert sum(m.players[0].lane_pos.values()) == 0

    def test_lane_pos_not_filtered_when_game_start_tick_is_none(self):
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=9999, npc_name="n", team=2, x=0.0, y=0.0),
        ]
        parser = _make_parser(game_start_tick=None)
        player_ext = _make_player_ext(snapshots=snaps)
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert sum(m.players[0].lane_pos.values()) == 1


# ---------------------------------------------------------------------------
# Lane 10-minute stats
# ---------------------------------------------------------------------------


class TestBuildParsedMatchLane10Min:
    def _build_with_min_series(self, pid: int, gold: list[int], xp: list[int]) -> ParsedMatch:
        ext = _make_player_ext()

        def ts_for(p):
            ts = _FakeTimeSeries()
            if p == pid:
                ts.total_earned_gold_t = gold
                ts.total_earned_xp_t = xp
                ts.lh_t = list(range(len(gold)))
                ts.dn_t = [0] * len(gold)
            return ts

        ext.time_series.side_effect = ts_for
        ext.minute_time_series.side_effect = ts_for
        parser = _make_parser()
        return build_parsed_match(
            parser,
            ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

    def test_lane_total_gold_at_10_min(self):
        gold = list(range(15))  # indices 0-14
        m = self._build_with_min_series(0, gold, list(range(15)))
        assert m.players[0].lane_total_gold == gold[10]

    def test_lane_total_xp_at_10_min(self):
        xp = [i * 10 for i in range(15)]
        m = self._build_with_min_series(0, list(range(15)), xp)
        assert m.players[0].lane_total_xp == xp[10]

    def test_lane_10min_not_set_when_series_too_short(self):
        gold = [100, 200, 300]  # only 3 entries — no index 10
        m = self._build_with_min_series(0, gold, gold)
        assert m.players[0].lane_total_gold == 0
        assert m.players[0].lane_total_xp == 0


# ---------------------------------------------------------------------------
# Player name extraction from entity manager
# ---------------------------------------------------------------------------


class TestBuildParsedMatchPlayerNames:
    def test_player_name_read_from_entity_manager(self):
        entity_manager = MagicMock()
        pr_entity = MagicMock()
        # Simulates m_vecPlayerData.0000.m_iszPlayerName returning a name
        pr_entity.get_string.side_effect = lambda field: "PlayerZero" if "0000" in field else ""
        entity_manager.find_by_class_name.return_value = pr_entity

        parser = _make_parser(entity_manager=entity_manager)
        player_ext = _make_player_ext()
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert m.players[0].player_name == "PlayerZero"

    def test_no_player_resource_entity_no_names_set(self):
        entity_manager = MagicMock()
        entity_manager.find_by_class_name.return_value = None

        parser = _make_parser(entity_manager=entity_manager)
        player_ext = _make_player_ext()
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        for pp in m.players:
            assert pp.player_name == ""

    def test_no_entity_manager_no_names_set(self):
        parser = _make_parser(entity_manager=None)
        player_ext = _make_player_ext()
        m = build_parsed_match(
            parser,
            player_ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        for pp in m.players:
            assert pp.player_name == ""


# ---------------------------------------------------------------------------
# Lotus pickups, tormentor kills, shrine kills — pass-through into ParsedMatch
# ---------------------------------------------------------------------------


def _item_entry(
    inflictor: str, target: str = "npc_dota_hero_axe", tick: int = 100
) -> CombatLogEntry:
    return CombatLogEntry(tick=tick, log_type="ITEM", inflictor_name=inflictor, target_name=target)


class TestNewObjectivesInParsedMatch:
    def _build(self, all_entries=None, obj_ext=None) -> ParsedMatch:
        parser = _make_parser()
        player_ext = _make_player_ext()
        return build_parsed_match(
            parser,
            player_ext,
            obj_ext or _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            all_entries or [],
            [],
        )

    def test_tormentor_kills_propagated_from_obj_ext(self):
        from gem.extractors.objectives import TormentorKill

        tk = TormentorKill(
            tick=1800, killer="npc_dota_hero_nevermore", killer_player_id=2, kill_number=1
        )
        m = self._build(obj_ext=_make_obj_ext(tormentors=[tk]))
        assert len(m.tormentors) == 1
        assert m.tormentors[0].kill_number == 1
        assert m.tormentors[0].killer_player_id == 2

    def test_shrine_kills_propagated_from_obj_ext(self):
        from gem.extractors.objectives import ShrineKill

        sk = ShrineKill(tick=2500, team=3)
        m = self._build(obj_ext=_make_obj_ext(shrines=[sk]))
        assert len(m.shrines) == 1
        assert m.shrines[0].team == 3

    def test_empty_tormentors_and_shrines_by_default(self):
        m = self._build()
        assert m.tormentors == []
        assert m.shrines == []
