"""Tests for gem.results.assembly — ParsedMatch assembly.

Tests cover:
- _radiant_win_from_ancient (pure unit logic)
- build_parsed_match (via minimal stubs for all extractor/parser dependencies)

Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java
"""

from __future__ import annotations

from dataclasses import dataclass, field
from unittest.mock import MagicMock

import pytest

import gem.results.models as model_module
from gem.combat.log import CombatLogEntry
from gem.extractors.intervals import IntervalSnapshot
from gem.results.assembly import _radiant_win_from_ancient, build_parsed_match
from gem.results.models import ChatEntry, ParsedMatch, SmokeEvent

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
    total_earned_xp: int = 0
    x: float | None = None
    y: float | None = None
    ability_levels: dict = field(default_factory=dict)
    items: dict = field(default_factory=dict)


def _make_parser(
    match_id: int = 1001,
    radiant_win: bool | None = True,
    tick: int = 100000,
    game_start_tick: int | None = 6000,
    game_mode: int = 22,
    leagueid: int = 0,
    entity_manager=None,
    match_metadata=None,
    duration_s: int | None = None,
) -> MagicMock:
    p = MagicMock()
    p.match_id = match_id
    p.radiant_win = radiant_win
    p.tick = tick
    p.game_start_tick = game_start_tick
    p.game_mode = game_mode
    p.leagueid = leagueid
    p.entity_manager = entity_manager
    p.match_metadata = match_metadata
    p.duration_s = duration_s
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

    def test_opendota_teamfights_populated(self):
        parser = _make_parser(game_start_tick=6000)
        player_ext = _make_player_ext(
            snapshots=[
                _FakePlayerSnapshot(
                    player_id=0,
                    tick=9000,
                    npc_name="npc_dota_hero_axe",
                    team=2,
                    x=10.0,
                    y=20.0,
                ),
                _FakePlayerSnapshot(
                    player_id=1,
                    tick=9030,
                    npc_name="npc_dota_hero_pudge",
                    team=3,
                    x=30.0,
                    y=40.0,
                ),
                _FakePlayerSnapshot(
                    player_id=2,
                    tick=9060,
                    npc_name="npc_dota_hero_lina",
                    team=3,
                    x=50.0,
                    y=60.0,
                ),
            ]
        )
        entries = [
            CombatLogEntry(
                tick=9000,
                game_time_s=100,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_pudge",
                target_is_hero=True,
            ),
            CombatLogEntry(
                tick=9030,
                game_time_s=101,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_lina",
                target_is_hero=True,
            ),
            CombatLogEntry(
                tick=9060,
                game_time_s=102,
                log_type="DEATH",
                attacker_name="npc_dota_hero_pudge",
                target_name="npc_dota_hero_axe",
                target_is_hero=True,
            ),
        ]

        m = build_parsed_match(
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

        assert len(m.opendota_teamfights) == 1
        assert m.opendota_teamfights[0].start == 85
        assert m.opendota_teamfights[0].end == 117
        assert m.opendota_teamfights[0].players[0].killed == {
            "npc_dota_hero_pudge": 1,
            "npc_dota_hero_lina": 1,
        }

    def test_has_ten_players(self):
        m = self._build()
        assert len(m.players) == 10

    def test_player_ids_set(self):
        m = self._build()
        for i, pp in enumerate(m.players):
            assert pp.player_id == i


# ---------------------------------------------------------------------------
# Match metadata ability upgrades
# ---------------------------------------------------------------------------


class TestBuildParsedMatchAbilityUpgrades:
    def _metadata(self):
        from gem.proto.dota_match_metadata_pb2 import CDOTAMatchMetadataFile

        metadata = CDOTAMatchMetadataFile()
        radiant = metadata.metadata.teams.add()
        dire = metadata.metadata.teams.add()

        p0 = radiant.players.add()
        p0.player_slot = 0
        p0.ability_upgrades.extend([1684, 7309])

        p4 = radiant.players.add()
        p4.player_slot = 4
        p4.ability_upgrades.extend([5625])

        p5 = dire.players.add()
        p5.player_slot = 128
        p5.ability_upgrades.extend([5134, 7325])

        p9 = dire.players.add()
        p9.player_slot = 132
        p9.ability_upgrades.extend([5106])

        invalid = dire.players.add()
        invalid.player_slot = 200
        invalid.ability_upgrades.extend([9999])

        return metadata

    def test_ability_upgrades_arr_from_match_metadata(self):
        parser = _make_parser(match_metadata=self._metadata())
        m = build_parsed_match(
            parser,
            _make_player_ext(),
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

        assert m.players[0].ability_upgrades_arr == [1684, 7309]
        assert m.players[4].ability_upgrades_arr == [5625]
        assert m.players[5].ability_upgrades_arr == [5134, 7325]
        assert m.players[9].ability_upgrades_arr == [5106]
        assert m.players[1].ability_upgrades_arr == []


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
        optional_kwargs = {}
        if "neutral_item_finds" in kw:
            optional_kwargs["neutral_item_finds"] = kw["neutral_item_finds"]
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
            **optional_kwargs,
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

    def test_neutral_item_finds_stored(self):
        neutral_event_cls = getattr(model_module, "NeutralItemFoundEvent", None)
        assert neutral_event_cls is not None
        events = [
            neutral_event_cls(
                tick=29858,
                player_id=6,
                item_ability_id=1861,
                item_key="stonefeather_satchel",
                enhancement_ability_id=1865,
                enhancement_key="enhancement_vital",
            )
        ]

        m = self._base_build(neutral_item_finds=events)

        assert m.neutral_item_finds is events

    def test_neutral_item_finds_defaults_to_empty_list_when_none(self):
        m = self._base_build(neutral_item_finds=None)
        assert m.neutral_item_finds == []

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
        from gem.combat.aggregator import _ParsedPlayerAgg

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
        from gem.combat.aggregator import _ParsedPlayerAgg

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
        from gem.combat.aggregator import _ParsedPlayerAgg

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
    def _build_with_ts(
        self,
        player_ts: dict[int, tuple[list[int], list[int], int]],
        all_entries: list[CombatLogEntry] | None = None,
        interval_snapshots: list[IntervalSnapshot] | None = None,
    ) -> ParsedMatch:
        """player_ts: {player_id: (total_earned_gold, total_earned_xp, team)}"""
        ext = _make_player_ext()

        def make_ts(gold, xp):
            ts = _FakeTimeSeries()
            ts.ticks = [1800 * (i + 1) for i in range(max(len(gold), len(xp)))]
            ts.gold_t = [value // 10 for value in gold]
            ts.total_earned_gold_t = gold
            ts.total_earned_xp_t = xp
            ts.net_worth_t = [value + 100 for value in gold]
            ts.lh_t = list(range(len(gold)))
            ts.dn_t = [value + 1 for value in range(len(gold))]
            ts.xp_t = xp
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
        interval_ext = None
        if interval_snapshots is not None:
            interval_ext = MagicMock()
            interval_ext.all_snapshots = interval_snapshots
        return build_parsed_match(
            parser,
            ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            all_entries or [],
            [],
            interval_ext=interval_ext,
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
        assert m.radiant_xp_adv == [300, 600]

    def test_dire_ahead(self):
        ts = {
            0: ([100, 200], [50, 100], 2),  # Radiant
            5: ([600, 1200], [300, 600], 3),  # Dire
        }
        m = self._build_with_ts(ts)
        assert m.radiant_gold_adv[0] == 100 - 600  # negative
        assert m.radiant_gold_adv[1] == 200 - 1200

    def test_combat_log_xp_does_not_override_total_earned_xp_adv(self):
        """Combat-log XP events must never feed radiant_xp_adv.

        OpenDota builds xp_t / radiant_xp_adv exclusively from the team-data
        entity's ``m_iTotalEarnedXP`` (mirrored here by ``total_earned_xp_t_min``);
        combat-log XP only feeds the per-reason ``xp_reasons`` histogram. Even
        with timed combat-log XP entries present, the advantage curve must come
        from the total-earned arrays.

        Reference: refs/parser/src/main/java/opendota/Parse.java interval block
        and CreateParsedDataBlob.java handleXp() (xp_reasons only).
        """
        ts = {
            0: ([1000, 2000, 3000], [5000, 5000, 5000], 2),
            5: ([500, 1000, 1500], [1000, 1000, 1000], 3),
        }
        entries = [
            CombatLogEntry(
                tick=100,
                game_time_s=10,
                log_type="XP",
                target_name="npc_dota_hero_hero0",
                value=100,
            ),
            CombatLogEntry(
                tick=200,
                game_time_s=60,
                log_type="XP",
                target_name="npc_dota_hero_hero5",
                value=40,
            ),
            CombatLogEntry(
                tick=300,
                game_time_s=61,
                log_type="XP",
                target_name="npc_dota_hero_hero0",
                value=30,
            ),
        ]

        m = self._build_with_ts(ts, all_entries=entries)

        # adv[i] = radiant_total_earned_xp - dire_total_earned_xp = 5000 - 1000
        assert m.radiant_xp_adv == [4000, 4000, 4000]

    def test_interval_snapshots_override_player_minute_adv(self):
        ts = {
            0: ([10], [10], 2),
            5: ([5], [5], 3),
        }
        interval_snapshots = [
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=0,
                player_slot=0,
                team=2,
                team_slot=0,
                gold=1000,
                xp=700,
            ),
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=5,
                player_slot=128,
                team=3,
                team_slot=0,
                gold=600,
                xp=450,
            ),
        ]

        m = self._build_with_ts(ts, interval_snapshots=interval_snapshots)

        assert m.radiant_gold_adv == [400]
        assert m.radiant_xp_adv == [250]

    def test_interval_xp_adv_wins_over_combat_log_xp(self):
        """Complete interval data is authoritative; combat-log XP is ignored.

        Regression for the precedence bug where _radiant_xp_adv_from_combat_log
        overrode the interval m_iTotalEarnedXP curve, producing grossly wrong
        advantage curves on long replays (e.g. -94899 vs OpenDota -30499).
        """
        ts = {
            0: ([10], [10], 2),
            5: ([5], [5], 3),
        }
        interval_snapshots = [
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=0,
                player_slot=0,
                team=2,
                team_slot=0,
                gold=1000,
                xp=700,
            ),
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=5,
                player_slot=128,
                team=3,
                team_slot=0,
                gold=600,
                xp=450,
            ),
        ]
        # Combat-log XP entries that, under the old buggy path, would have
        # produced a completely different curve. They must be ignored entirely.
        entries = [
            CombatLogEntry(
                tick=100,
                game_time_s=30,
                log_type="XP",
                target_name="npc_dota_hero_hero0",
                value=99999,
            ),
        ]

        m = self._build_with_ts(ts, all_entries=entries, interval_snapshots=interval_snapshots)

        # Authoritative interval XP advantage: 700 - 450 = 250.
        assert m.radiant_xp_adv == [250]
        assert m.radiant_gold_adv == [400]

    def test_interval_snapshots_populate_player_minute_arrays(self):
        ts = {
            0: ([10], [20], 2),
            5: ([5], [10], 3),
        }
        interval_snapshots = [
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=0,
                player_slot=0,
                team=2,
                team_slot=0,
                gold=1000,
                xp=700,
                lh=22,
                dn=3,
                net_worth=1600,
            ),
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=5,
                player_slot=128,
                team=3,
                team_slot=0,
                gold=600,
                xp=450,
                lh=16,
                dn=1,
                net_worth=1200,
            ),
        ]

        m = self._build_with_ts(ts, interval_snapshots=interval_snapshots)

        p0 = m.players[0]
        assert p0.times_min == [1800]
        assert p0.gold_t_min == [1000]
        assert p0.total_earned_gold_t_min == [1000]
        assert p0.xp_t_min == [700]
        assert p0.total_earned_xp_t_min == [700]
        assert p0.lh_t_min == [22]
        assert p0.dn_t_min == [3]
        assert p0.net_worth_t_min == [1600]

    def test_incomplete_interval_batches_fall_back_to_player_minute_adv(self):
        ts = {
            0: ([1000], [500], 2),
            5: ([500], [200], 3),
        }
        interval_snapshots = [
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=0,
                player_slot=0,
                team=2,
                team_slot=0,
                gold=10_000,
                xp=10_000,
            ),
            IntervalSnapshot(
                tick=3600,
                time_s=120,
                player_id=5,
                player_slot=128,
                team=3,
                team_slot=0,
                gold=9_000,
                xp=9_000,
            ),
        ]

        m = self._build_with_ts(ts, interval_snapshots=interval_snapshots)

        assert m.radiant_gold_adv == [500]
        assert m.radiant_xp_adv == [300]

    def test_incomplete_interval_batches_keep_player_minute_fallback(self):
        ts = {
            0: ([1000], [500], 2),
            5: ([500], [200], 3),
        }
        interval_snapshots = [
            IntervalSnapshot(
                tick=1800,
                time_s=60,
                player_id=0,
                player_slot=0,
                team=2,
                team_slot=0,
                gold=10_000,
                xp=10_000,
            ),
            IntervalSnapshot(
                tick=3600,
                time_s=120,
                player_id=5,
                player_slot=128,
                team=3,
                team_slot=0,
                gold=9_000,
                xp=9_000,
            ),
        ]

        m = self._build_with_ts(ts, interval_snapshots=interval_snapshots)

        p0 = m.players[0]
        assert p0.times_min == [1800]
        assert p0.gold_t_min == [100]
        assert p0.total_earned_gold_t_min == [1000]
        assert p0.xp_t_min == [500]
        assert p0.total_earned_xp_t_min == [500]
        assert p0.net_worth_t_min == [1100]

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
# build_parsed_match — final_items (end-of-game inventory)
# ---------------------------------------------------------------------------


class TestBuildParsedMatchFinalItems:
    def _build(self, snaps):
        return build_parsed_match(
            _make_parser(),
            _make_player_ext(snapshots=snaps),
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
        )

    def test_final_items_from_last_snapshot(self):
        snaps = [
            _FakePlayerSnapshot(
                player_id=0, tick=100, npc_name="n", team=2, items={0: "item_tango"}
            ),
            _FakePlayerSnapshot(
                player_id=0, tick=130, npc_name="n", team=2, items={0: "item_blink", 1: "item_bkb"}
            ),
        ]
        m = self._build(snaps)
        assert m.players[0].final_items == {0: "item_blink", 1: "item_bkb"}

    def test_empty_final_inventory_not_overwritten_by_stale_snapshot(self):
        # Regression: a player can legitimately end with no items (sold/dropped/
        # destroyed before Ancient death). The last snapshot wins even when empty;
        # an earlier non-empty snapshot must NOT be copied as the final state.
        snaps = [
            _FakePlayerSnapshot(
                player_id=0, tick=100, npc_name="n", team=2, items={0: "item_blink"}
            ),
            _FakePlayerSnapshot(player_id=0, tick=130, npc_name="n", team=2, items={}),
        ]
        m = self._build(snaps)
        assert m.players[0].final_items == {}

    def test_no_snapshots_leaves_default_empty(self):
        m = self._build([_FakePlayerSnapshot(player_id=5, tick=1, npc_name="n", team=3)])
        # player 0 has no snapshots at all → default {}
        assert m.players[0].final_items == {}


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
# End-of-game terminal scalars (net_worth / last_hits / denies)
# ---------------------------------------------------------------------------


class TestBuildParsedMatchTerminalScalars:
    def _build_with_dense_series(
        self,
        pid: int,
        net_worth: list[int],
        last_hits: list[int],
        denies: list[int],
    ) -> ParsedMatch:
        ext = _make_player_ext()

        def ts_for(p):
            ts = _FakeTimeSeries()
            if p == pid:
                ts.net_worth_t = net_worth
                ts.lh_t = last_hits
                ts.dn_t = denies
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

    def test_terminal_scalars_read_last_dense_sample(self):
        m = self._build_with_dense_series(
            0, net_worth=[600, 5000, 18763], last_hits=[0, 90, 175], denies=[0, 3, 5]
        )
        assert m.players[0].net_worth == 18763
        assert m.players[0].last_hits == 175
        assert m.players[0].denies == 5

    def test_terminal_scalars_default_zero_without_samples(self):
        m = self._build_with_dense_series(0, net_worth=[], last_hits=[], denies=[])
        assert m.players[0].net_worth == 0
        assert m.players[0].last_hits == 0
        assert m.players[0].denies == 0


# ---------------------------------------------------------------------------
# Team-data terminal counters (camps/creeps stacked, wards, runes, towers)
# ---------------------------------------------------------------------------


class TestBuildParsedMatchTeamCounters:
    def test_counters_wired_from_interval_extractor(self):
        ext = _make_player_ext()
        parser = _make_parser()

        counters_by_player = {
            0: {
                "camps_stacked": 13,
                "creeps_stacked": 30,
                "obs_placed": 7,
                "sen_placed": 4,
                "rune_pickups": 2,
                "tower_kills": 3,
            }
        }
        interval_ext = MagicMock()
        interval_ext.all_snapshots = []
        interval_ext.team_counters.side_effect = lambda pid: counters_by_player.get(
            pid, dict.fromkeys(counters_by_player[0], 0)
        )

        m = build_parsed_match(
            parser,
            ext,
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            _make_combat_agg(),
            [],
            [],
            interval_ext=interval_ext,
        )

        p0 = m.players[0]
        assert p0.camps_stacked == 13
        assert p0.creeps_stacked == 30
        assert p0.obs_placed == 7
        assert p0.sen_placed == 4
        assert p0.rune_pickups == 2
        assert p0.tower_kills == 3
        # A player with no observed counters defaults to zero.
        assert m.players[1].camps_stacked == 0

    def test_counters_default_zero_without_interval_extractor(self):
        ext = _make_player_ext()
        parser = _make_parser()
        m = build_parsed_match(
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
        assert m.players[0].camps_stacked == 0
        assert m.players[0].tower_kills == 0


# ---------------------------------------------------------------------------
# OpenDota-style computed fields (kda / buyback_count / is_radiant / win)
# ---------------------------------------------------------------------------


class TestBuildParsedMatchComputedFields:
    def _build(self, *, radiant_win, scoreboard, snaps):
        parser = _make_parser(radiant_win=radiant_win)
        ext = _make_player_ext(scoreboard=scoreboard, snapshots=snaps)
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

    def test_kda_uses_plus_one_denominator_and_two_decimals(self):
        # (1 + 10) / (7 + 1) = 1.375 -> 1.38 (round-half-to-even on 2 dp).
        snaps = [_FakePlayerSnapshot(player_id=0, tick=1, npc_name="npc_dota_hero_zuus", team=2)]
        m = self._build(radiant_win=True, scoreboard={0: (1, 7, 10)}, snaps=snaps)
        assert m.players[0].kda == 1.38

    def test_kda_zero_deaths_uses_plus_one(self):
        snaps = [_FakePlayerSnapshot(player_id=0, tick=1, npc_name="npc_dota_hero_zuus", team=2)]
        m = self._build(radiant_win=True, scoreboard={0: (5, 0, 3)}, snaps=snaps)
        assert m.players[0].kda == 8.0  # (5 + 3) / (0 + 1)

    def test_is_radiant_and_win_for_radiant_winner(self):
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=1, npc_name="npc_dota_hero_zuus", team=2),
            _FakePlayerSnapshot(player_id=5, tick=1, npc_name="npc_dota_hero_axe", team=3),
        ]
        m = self._build(radiant_win=True, scoreboard={}, snaps=snaps)
        assert m.players[0].is_radiant is True
        assert m.players[0].win == 1
        assert m.players[5].is_radiant is False
        assert m.players[5].win == 0

    def test_win_zero_for_both_when_winner_unknown(self):
        snaps = [
            _FakePlayerSnapshot(player_id=0, tick=1, npc_name="npc_dota_hero_zuus", team=2),
            _FakePlayerSnapshot(player_id=5, tick=1, npc_name="npc_dota_hero_axe", team=3),
        ]
        m = self._build(radiant_win=None, scoreboard={}, snaps=snaps)
        assert m.players[0].win == 0
        assert m.players[5].win == 0

    def test_buyback_count_matches_log_length(self):
        from gem.combat.aggregator import _ParsedPlayerAgg

        aggs = {i: _ParsedPlayerAgg() for i in range(10)}
        combat_agg = MagicMock()
        combat_agg.players = aggs
        combat_agg._agg.side_effect = lambda pid: aggs[pid]

        entries = [_buyback(pid=0, tick=1000), _buyback(pid=0, tick=2000)]
        m = build_parsed_match(
            _make_parser(radiant_win=True),
            _make_player_ext(),
            _make_obj_ext(),
            _make_ward_ext(),
            _make_courier_ext(),
            _make_draft_ext(),
            combat_agg,
            entries,
            [],
        )
        assert m.players[0].buyback_count == 2
        assert m.players[1].buyback_count == 0


class TestBuildParsedMatchDuration:
    def _build(self, *, duration_s, scoreboard=None, snaps=None):
        parser = _make_parser(duration_s=duration_s)
        ext = _make_player_ext(scoreboard=scoreboard or {}, snapshots=snaps or [])
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

    def test_duration_taken_from_parser_postgame_seconds(self):
        m = self._build(duration_s=2419)
        assert m.duration == 2419

    def test_duration_zero_when_postgame_not_observed(self):
        m = self._build(duration_s=None)
        assert m.duration == 0

    def test_kills_per_min_uses_match_duration(self):
        # 8 kills over 4177s = 8 / (4177/60).
        snaps = [_FakePlayerSnapshot(player_id=0, tick=1, npc_name="npc_dota_hero_zuus", team=2)]
        m = self._build(duration_s=4177, scoreboard={0: (8, 7, 12)}, snaps=snaps)
        assert m.players[0].kills_per_min == 8 / (4177 / 60)

    def test_kills_per_min_zero_without_duration(self):
        snaps = [_FakePlayerSnapshot(player_id=0, tick=1, npc_name="npc_dota_hero_zuus", team=2)]
        m = self._build(duration_s=None, scoreboard={0: (8, 7, 12)}, snaps=snaps)
        assert m.players[0].kills_per_min == 0.0


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


# ---------------------------------------------------------------------------
# _radiant_adv_from_minute_series — fallback advantage curve (B7)
# ---------------------------------------------------------------------------


class TestRadiantAdvFromMinuteSeries:
    """Fallback advantage curve must span the full game and align by real minute."""

    @staticmethod
    def _player(pid, team, gold, xp, times=None):
        from gem.results.models import ParsedPlayer

        pp = ParsedPlayer(player_id=pid, hero_name=f"npc_dota_hero_h{pid}", team=team)
        pp.total_earned_gold_t_min = gold
        pp.total_earned_xp_t_min = xp
        # Default to one sample per game minute starting at tick 0 (minute 0).
        pp.times_min = times if times is not None else [i * 1800 for i in range(len(gold))]
        return pp

    def test_full_length_equal_teams(self):
        from gem.results.assembly import _radiant_adv_from_minute_series

        players = [
            self._player(0, 2, [100, 200, 300], [10, 20, 30]),
            self._player(5, 3, [100, 200, 300], [10, 20, 30]),
        ]
        gold_adv, xp_adv = _radiant_adv_from_minute_series(players)
        assert gold_adv == [0, 0, 0]
        assert xp_adv == [0, 0, 0]

    def test_leaver_does_not_truncate_curve(self):
        # One Dire player's minute array stops early (disconnect). The curve must
        # still span the longest array; the leaver's last earned value carries
        # forward (total-earned is monotonic and never resets). Regression for the
        # min()-length truncation bug.
        from gem.results.assembly import _radiant_adv_from_minute_series

        players = [
            self._player(0, 2, [100, 200, 300, 400], [0, 0, 0, 0]),  # Radiant, full
            self._player(5, 3, [100, 200], [0, 0]),  # Dire, leaves after minute 1
        ]
        gold_adv, _ = _radiant_adv_from_minute_series(players)
        # Curve spans 4 minutes (longest), not 2 (shortest).
        assert len(gold_adv) == 4
        # Radiant pulls ahead as Dire's carried-forward value (200) stays flat.
        assert gold_adv == [0, 0, 100, 200]

    def test_leading_gap_aligned_by_real_minute(self):
        # A player whose first sample is at minute 1 (no minute-0 sample) must be
        # placed at index 1 — NOT have minute-1's value shifted into index 0.
        # Regression for Codex P2: index-as-minute corrupts the curve on leading
        # gaps. Radiant has a full series; Dire's first sample is minute 1.
        from gem.results.assembly import _radiant_adv_from_minute_series

        radiant = self._player(0, 2, [100, 200, 300], [0, 0, 0], times=[0, 1800, 3600])
        # Dire missing minute 0: samples land at ticks 1800 (min 1) and 3600 (min 2).
        dire = self._player(5, 3, [500, 700], [0, 0], times=[1800, 3600])
        gold_adv, _ = _radiant_adv_from_minute_series([radiant, dire])
        # Minute 0: only Radiant present (Dire contributes 0, not its minute-1 value).
        assert gold_adv[0] == 100
        # Minute 1: 200 - 500. Minute 2: 300 - 700.
        assert gold_adv[1] == 200 - 500
        assert gold_adv[2] == 300 - 700

    def test_returns_none_when_no_minute_data(self):
        from gem.results.assembly import _radiant_adv_from_minute_series

        players = [self._player(0, 2, [], [])]
        assert _radiant_adv_from_minute_series(players) is None
