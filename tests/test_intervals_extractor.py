"""Unit tests for OpenDota-style interval extraction."""

from __future__ import annotations

import pytest

from gem.extractors.intervals import IntervalExtractor
from gem.state.entities import Entity, EntityOp


class FakeClass:
    def __init__(self, name: str = "Test") -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _ent(class_name: str = "Test", index: int = 0, serial: int = 0, **state) -> Entity:
    entity = Entity(index=index, serial=serial, cls=FakeClass(class_name))
    entity._state.update(state)
    return entity


class FakeParser:
    def __init__(
        self,
        tick: int = 1800,
        game_time_s: int | None = 60,
        combat_log_time_s: int | None = None,
    ) -> None:
        self.tick = tick
        self.game_time_s = game_time_s
        # Combat-log timestamp axis clock. When set, the extractor samples
        # boundaries on this axis (matching OpenDota); when None it falls back
        # to game_time_s, which keeps the legacy single-clock tests valid.
        self.combat_log_time_s = combat_log_time_s
        self.string_tables = None
        self.entity_handlers = []
        self.game_end_handlers = []

    def on_entity(self, handler):
        self.entity_handlers.append(handler)

    def on_game_end(self, handler):
        self.game_end_handlers.append(handler)


def _player_resource() -> Entity:
    """Build PlayerResource with non-contiguous resource indices."""
    return _ent(
        "CDOTA_PlayerResource",
        **{
            "m_vecPlayerData.0002.m_iPlayerTeam": 2,
            "m_vecPlayerTeamData.0002.m_iTeamSlot": 1,
            "m_vecPlayerData.0007.m_iPlayerTeam": 3,
            "m_vecPlayerTeamData.0007.m_iTeamSlot": 4,
            # Invalid spectator/coach-like rows should not become output players.
            "m_vecPlayerData.0011.m_iPlayerTeam": 1,
            "m_vecPlayerTeamData.0011.m_iTeamSlot": 0,
        },
    )


def _radiant_data() -> Entity:
    return _ent(
        "CDOTADataRadiant",
        **{
            "m_vecDataTeam.0001.m_iTotalEarnedGold": 1000,
            "m_vecDataTeam.0001.m_iTotalEarnedXP": 700,
            "m_vecDataTeam.0001.m_iLastHitCount": 22,
            "m_vecDataTeam.0001.m_iDenyCount": 3,
            "m_vecDataTeam.0001.m_iNetWorth": 1600,
        },
    )


def _dire_data() -> Entity:
    return _ent(
        "CDOTA_DataDire",
        **{
            "m_vecDataTeam.0004.m_iTotalEarnedGold": 600,
            "m_vecDataTeam.0004.m_iTotalEarnedXP": 450,
            "m_vecDataTeam.0004.m_iLastHitCount": 16,
            "m_vecDataTeam.0004.m_iDenyCount": 1,
            "m_vecDataTeam.0004.m_iNetWorth": 1200,
        },
    )


def _zero_radiant_data() -> Entity:
    return _ent(
        "CDOTADataRadiant",
        **{
            "m_vecDataTeam.0001.m_iTotalEarnedGold": 0,
            "m_vecDataTeam.0001.m_iTotalEarnedXP": 0,
            "m_vecDataTeam.0001.m_iLastHitCount": 0,
            "m_vecDataTeam.0001.m_iDenyCount": 0,
            "m_vecDataTeam.0001.m_iNetWorth": 600,
        },
    )


def _zero_dire_data() -> Entity:
    return _ent(
        "CDOTA_DataDire",
        **{
            "m_vecDataTeam.0004.m_iTotalEarnedGold": 0,
            "m_vecDataTeam.0004.m_iTotalEarnedXP": 0,
            "m_vecDataTeam.0004.m_iLastHitCount": 0,
            "m_vecDataTeam.0004.m_iDenyCount": 0,
            "m_vecDataTeam.0004.m_iNetWorth": 600,
        },
    )


def _attach_ready_extractor(game_time_s: int | None = 60) -> tuple[IntervalExtractor, FakeParser]:
    ext = IntervalExtractor()
    parser = FakeParser(game_time_s=game_time_s)
    ext.attach(parser)
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    return ext, parser


def test_interval_s_must_be_positive():
    with pytest.raises(ValueError, match="interval_s must be positive"):
        IntervalExtractor(interval_s=0)


def test_emits_complete_interval_batch_at_exact_boundary():
    ext, _parser = _attach_ready_extractor(game_time_s=60)

    assert len(ext.snapshots) == 2
    radiant, dire = ext.snapshots
    assert radiant.player_id == 0
    assert radiant.player_slot == 1
    assert radiant.team == 2
    assert radiant.team_slot == 1
    assert radiant.gold == 1000
    assert radiant.xp == 700
    assert radiant.lh == 22
    assert radiant.dn == 3
    assert radiant.net_worth == 1600
    assert dire.player_id == 1
    assert dire.player_slot == 132
    assert dire.team == 3
    assert dire.team_slot == 4
    assert dire.gold == 600
    assert dire.xp == 450


def test_skips_non_boundary_game_time():
    ext, _parser = _attach_ready_extractor(game_time_s=61)

    assert ext.snapshots == []


def test_does_not_emit_partial_batch_before_both_team_entities_arrive():
    ext = IntervalExtractor()
    parser = FakeParser(game_time_s=60)
    ext.attach(parser)

    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    assert ext.snapshots == []

    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    assert len(ext.snapshots) == 2


def test_dedupes_multiple_entity_callbacks_at_same_game_time():
    ext, _parser = _attach_ready_extractor(game_time_s=60)

    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2


def test_waits_for_game_clock_before_first_interval_emit():
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=60)
    ext.attach(parser)

    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    assert ext.snapshots == []

    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    assert len(ext.snapshots) == 2


def test_allows_delayed_zero_baseline_after_clock_tick():
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=0)
    ext.attach(parser)

    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    parser.tick = 1801
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_zero_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_zero_dire_data(), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2
    assert {snap.time_s for snap in ext.snapshots} == {0}
    assert {snap.gold for snap in ext.snapshots} == {0}
    assert {snap.xp for snap in ext.snapshots} == {0}
    assert {snap.lh for snap in ext.snapshots} == {0}
    assert {snap.dn for snap in ext.snapshots} == {0}


def test_replaces_nonzero_zero_boundary_with_synthetic_baseline():
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=0)
    ext.attach(parser)

    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2
    assert [snap.time_s for snap in ext.snapshots] == [0, 0]
    assert [snap.gold for snap in ext.snapshots] == [0, 0]
    assert [snap.xp for snap in ext.snapshots] == [0, 0]
    assert [snap.lh for snap in ext.snapshots] == [0, 0]
    assert [snap.dn for snap in ext.snapshots] == [0, 0]


def test_rejects_delayed_zero_baseline_with_nonzero_counters():
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=0)
    ext.attach(parser)

    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    parser.tick = 1801
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)

    assert ext.snapshots == []

    parser.tick = 3600
    parser.game_time_s = 60
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    assert len(ext.snapshots) == 4
    assert [snap.time_s for snap in ext.snapshots] == [0, 0, 60, 60]
    assert [snap.gold for snap in ext.snapshots[:2]] == [0, 0]
    assert [snap.gold for snap in ext.snapshots[2:]] == [1000, 600]


def test_game_end_emits_nearby_final_interval_boundary():
    ext, parser = _attach_ready_extractor(game_time_s=60)

    parser.tick = 3550
    parser.game_time_s = 118
    ext._on_game_end(parser.tick)

    assert len(ext.snapshots) == 4
    assert [snap.time_s for snap in ext.snapshots] == [60, 60, 120, 120]
    assert [snap.gold for snap in ext.snapshots[2:]] == [1000, 600]


def test_requires_fresh_game_clock_for_subsequent_interval_emit():
    ext, parser = _attach_ready_extractor(game_time_s=60)
    assert len(ext.snapshots) == 2

    parser.tick = 3600
    parser.game_time_s = 120
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    assert len(ext.snapshots) == 2

    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    assert len(ext.snapshots) == 4


def test_series_returns_parallel_arrays_sorted_by_time():
    ext, parser = _attach_ready_extractor(game_time_s=60)

    parser.tick = 3600
    parser.game_time_s = 120
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    ts = ext.series(0)
    assert ts.ticks == [1800, 3600]
    assert ts.times == [60, 120]
    assert ts.gold_t == [1000, 1000]
    assert ts.xp_t == [700, 700]
    assert ts.lh_t == [22, 22]
    assert ts.dn_t == [3, 3]
    assert ts.net_worth_t == [1600, 1600]


def test_game_end_stops_later_interval_emits():
    ext, parser = _attach_ready_extractor(game_time_s=60)

    ext._on_game_end(parser.tick)
    parser.tick = 3600
    parser.game_time_s = 120
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2


def test_prefers_combat_log_axis_over_entity_clock():
    """Boundaries are sampled on the combat-log axis when it is available.

    The entity clock (game_time_s) and the combat-log axis differ by a
    per-replay constant. OpenDota times its interval boundaries and its
    postGame stop on the combat-log axis, so gem must too. Here the entity
    clock is not on a boundary (61) but the combat-log axis is (60); the
    extractor must emit using the combat-log axis.
    """
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=61, combat_log_time_s=60)
    ext.attach(parser)

    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2
    assert {snap.time_s for snap in ext.snapshots} == {60}


def test_final_minute_survives_when_boundary_precedes_postgame_on_one_axis():
    """The final minute is emitted when its boundary precedes postGame.

    Regression for the cross-axis bug: on a ranked pub (8855517660) the fort
    death / postGame was at combat-log t=1867 while the entity clock read 1841
    at the same tick. Sampling boundaries on the entity clock dropped the
    t=1860 (minute 31) boundary because _ended fired first. With boundaries on
    the combat-log axis, the t=1860 boundary (< 1867 postGame) is emitted
    before the game ends, matching OpenDota's minute count.
    """
    ext = IntervalExtractor()
    # Combat-log axis is the authoritative one; entity clock lags by 19s.
    parser = FakeParser(tick=1800, game_time_s=41, combat_log_time_s=60)
    ext.attach(parser)
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    assert {snap.time_s for snap in ext.snapshots} == {60}

    # A later combat-log boundary (120) arrives before the game has ended; it
    # must be emitted even though the lagging entity clock is still below it.
    parser.tick = 3600
    parser.game_time_s = 101
    parser.combat_log_time_s = 120
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    assert {snap.time_s for snap in ext.snapshots} == {60, 120}
    assert len(ext.snapshots) == 4
