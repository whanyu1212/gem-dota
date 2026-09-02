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

    def _on_entity_filtered(self, handler, **_filters):
        self.on_entity(handler)

    def on_game_end(self, handler):
        self.game_end_handlers.append(handler)


class TickStartFakeParser(FakeParser):
    """Fake parser exposing the pre-entity-update callback used in production."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tick_start_handlers = []

    def on_tick_start(self, handler):
        self.tick_start_handlers.append(handler)

    def fire_tick_start(self, net_tick: int) -> None:
        for handler in self.tick_start_handlers:
            handler(net_tick)


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


def test_allows_delayed_initial_boundary_after_clock_tick():
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


def test_preserves_pending_initial_boundary_after_clock_advances():
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=0, combat_log_time_s=0)
    ext.attach(parser)

    # Observe t=0 before the player and team entities are ready.
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    # A combat-log entry advances the authoritative clock before those entities
    # arrive. The pending initial boundary must still emit at t=0 with live data.
    parser.tick = 1801
    parser.game_time_s = 1
    parser.combat_log_time_s = 1
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2
    assert [snap.time_s for snap in ext.snapshots] == [0, 0]
    assert [snap.gold for snap in ext.snapshots] == [1000, 600]


def test_initial_boundary_keeps_live_nonzero_values():
    ext = IntervalExtractor()
    parser = FakeParser(tick=1799, game_time_s=-1)
    ext.attach(parser)

    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_zero_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_zero_dire_data(), EntityOp.UPDATED)

    # Both teams advance on the boundary tick. The t=0 snapshot must use these
    # live counters, not nudge back to the cached zero-valued pre-boundary frame.
    parser.tick = 1800
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    parser.game_time_s = 0
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2
    assert [snap.time_s for snap in ext.snapshots] == [0, 0]
    assert [snap.gold for snap in ext.snapshots] == [1000, 600]
    assert [snap.xp for snap in ext.snapshots] == [700, 450]
    assert [snap.lh for snap in ext.snapshots] == [22, 16]
    assert [snap.dn for snap in ext.snapshots] == [3, 1]


def test_allows_delayed_initial_boundary_with_nonzero_counters():
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=0)
    ext.attach(parser)

    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    parser.tick = 1801
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)

    assert len(ext.snapshots) == 2
    assert [snap.time_s for snap in ext.snapshots] == [0, 0]
    assert [snap.gold for snap in ext.snapshots] == [1000, 600]

    parser.tick = 3600
    parser.game_time_s = 60
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    assert len(ext.snapshots) == 4
    assert [snap.time_s for snap in ext.snapshots] == [0, 0, 60, 60]
    assert [snap.gold for snap in ext.snapshots[:2]] == [1000, 600]
    assert [snap.gold for snap in ext.snapshots[2:]] == [1000, 600]


def test_game_end_recovers_recent_elapsed_interval_boundary():
    ext, parser = _attach_ready_extractor(game_time_s=60)

    parser.tick = 3550
    parser.game_time_s = 122
    ext._on_game_end(parser.tick)

    assert len(ext.snapshots) == 4
    assert [snap.time_s for snap in ext.snapshots] == [60, 60, 120, 120]
    assert [snap.gold for snap in ext.snapshots[2:]] == [1000, 600]


def test_game_end_does_not_emit_future_interval_boundary():
    ext, parser = _attach_ready_extractor(game_time_s=60)

    parser.tick = 3550
    parser.game_time_s = 118
    ext._on_game_end(parser.tick)

    assert len(ext.snapshots) == 2
    assert [snap.time_s for snap in ext.snapshots] == [60, 60]


def test_game_end_does_not_recover_stale_interval_boundary():
    ext, parser = _attach_ready_extractor(game_time_s=60)

    parser.tick = 4100
    parser.game_time_s = 136
    ext._on_game_end(parser.tick)

    assert len(ext.snapshots) == 2
    assert [snap.time_s for snap in ext.snapshots] == [60, 60]


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


def _radiant_data_with(gold: int, xp: int, lh: int, dn: int, net_worth: int) -> Entity:
    """Radiant data entity carrying explicit team-slot-1 totals."""
    return _ent(
        "CDOTADataRadiant",
        **{
            "m_vecDataTeam.0001.m_iTotalEarnedGold": gold,
            "m_vecDataTeam.0001.m_iTotalEarnedXP": xp,
            "m_vecDataTeam.0001.m_iLastHitCount": lh,
            "m_vecDataTeam.0001.m_iDenyCount": dn,
            "m_vecDataTeam.0001.m_iNetWorth": net_worth,
        },
    )


def _dire_data_with(gold: int, xp: int, lh: int, dn: int, net_worth: int) -> Entity:
    """Dire data entity carrying explicit team-slot-4 totals."""
    return _ent(
        "CDOTA_DataDire",
        **{
            "m_vecDataTeam.0004.m_iTotalEarnedGold": gold,
            "m_vecDataTeam.0004.m_iTotalEarnedXP": xp,
            "m_vecDataTeam.0004.m_iLastHitCount": lh,
            "m_vecDataTeam.0004.m_iDenyCount": dn,
            "m_vecDataTeam.0004.m_iNetWorth": net_worth,
        },
    )


def test_tick_start_defers_crossing_by_one_net_tick():
    """Production sampling includes crossing-tick but not next-tick deltas."""
    ext = IntervalExtractor()
    parser = TickStartFakeParser(tick=1700, game_time_s=58)
    ext.attach(parser)  # type: ignore[arg-type]
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)

    # The first CNETMsg_Tick at t=60 queues the boundary. Its entity delta is
    # incorporated, then the next CNETMsg_Tick emits before any newer delta.
    parser.tick = 1800
    parser.game_time_s = 60
    parser.fire_tick_start(6000)
    assert ext.snapshots == []
    ext._on_entity(_radiant_data_with(1500, 1100, 30, 5, 2200), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    parser.tick = 1801
    parser.fire_tick_start(6001)

    assert len(ext.snapshots) == 2
    radiant = next(s for s in ext.snapshots if s.team == 2)
    assert radiant.time_s == 60
    assert radiant.gold == 1500
    assert radiant.xp == 1100
    assert radiant.lh == 30
    assert radiant.dn == 5


def test_tick_start_samples_minute_zero_before_same_tick_bounty_delta():
    ext = IntervalExtractor()
    parser = TickStartFakeParser(tick=1800, game_time_s=0)
    ext.attach(parser)  # type: ignore[arg-type]
    ext._on_entity(_player_resource(), EntityOp.UPDATED)
    ext._on_entity(_radiant_data_with(0, 0, 0, 0, 600), EntityOp.UPDATED)
    ext._on_entity(_zero_dire_data(), EntityOp.UPDATED)

    # Minute zero is OpenDota's immediate @OnTickStart read. A team-wide bounty
    # payout arriving later in this same tick must not leak into that boundary.
    parser.fire_tick_start(6000)
    assert [snap.gold for snap in ext.snapshots] == [0, 0]

    ext._on_entity(_radiant_data_with(40, 0, 0, 0, 640), EntityOp.UPDATED)
    parser.tick = 1801
    parser.fire_tick_start(6001)

    assert [snap.gold for snap in ext.snapshots] == [0, 0]


def test_tick_start_minute_zero_prefers_previous_team_data_frame():
    ext = IntervalExtractor()
    parser = TickStartFakeParser(tick=1798, game_time_s=0)
    ext.attach(parser)  # type: ignore[arg-type]
    ext._on_entity(_player_resource(), EntityOp.UPDATED)

    # The frame visible to OpenDota's minute-zero callback has all counters at
    # zero. Gem receives one newer team-data frame before its rounded game clock
    # reaches zero; that frame contains the engine's transient starting gold.
    ext._on_entity(_zero_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_zero_dire_data(), EntityOp.UPDATED)
    parser.tick = 1799
    ext._on_entity(_radiant_data_with(1, 2, 3, 4, 605), EntityOp.UPDATED)
    ext._on_entity(_dire_data_with(1, 2, 3, 4, 605), EntityOp.UPDATED)

    parser.tick = 1800
    parser.fire_tick_start(6000)

    assert [snap.gold for snap in ext.snapshots] == [0, 0]
    assert [snap.xp for snap in ext.snapshots] == [0, 0]
    assert [snap.lh for snap in ext.snapshots] == [0, 0]
    assert [snap.dn for snap in ext.snapshots] == [0, 0]
    assert [snap.net_worth for snap in ext.snapshots] == [600, 600]


def test_tick_start_delayed_minute_zero_retains_previous_frame_phase():
    ext = IntervalExtractor()
    parser = TickStartFakeParser(tick=1798, game_time_s=0)
    ext.attach(parser)  # type: ignore[arg-type]

    ext._on_entity(_zero_radiant_data(), EntityOp.UPDATED)
    ext._on_entity(_zero_dire_data(), EntityOp.UPDATED)
    parser.tick = 1799
    ext._on_entity(_radiant_data_with(1, 0, 0, 0, 601), EntityOp.UPDATED)
    ext._on_entity(_dire_data_with(1, 0, 0, 0, 601), EntityOp.UPDATED)

    # The initial callback cannot emit until PlayerResource establishes logical
    # slots. Its next-tick retry must keep minute zero's prior-frame semantics.
    parser.tick = 1800
    parser.fire_tick_start(6000)
    assert ext.snapshots == []
    ext._on_entity(_player_resource(), EntityOp.UPDATED)

    parser.tick = 1801
    parser.fire_tick_start(6001)

    assert [snap.gold for snap in ext.snapshots] == [0, 0]


def test_tick_start_preserves_nonzero_minute_zero_gold():
    ext = IntervalExtractor()
    parser = TickStartFakeParser(tick=1798, game_time_s=0)
    ext.attach(parser)  # type: ignore[arg-type]
    ext._on_entity(_player_resource(), EntityOp.UPDATED)

    # Real pre-horn earnings can already be present in both adjacent frames.
    # Selecting the prior frame must preserve those values verbatim rather than
    # applying a blanket minute-zero normalization.
    ext._on_entity(_radiant_data_with(322, 40, 0, 0, 922), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    parser.tick = 1799
    ext._on_entity(_radiant_data_with(322, 40, 0, 0, 922), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)

    parser.tick = 1800
    parser.fire_tick_start(6000)

    radiant = next(s for s in ext.snapshots if s.team == 2)
    dire = next(s for s in ext.snapshots if s.team == 3)
    assert radiant.gold == 322
    assert dire.gold == 600
    assert radiant.xp == 40


def test_nudge_reads_previous_data_frame_not_boundary_frame():
    """The boundary emit reads the team-data frame *before* the crossing tick.

    OpenDota samples its interval one entity frame earlier than gem's clock
    crossing, so the increment that lands on the boundary tick must not be
    counted. Once a prior data frame exists, ``_emit`` reads it rather than the
    live (boundary-tick) values. Here the data entity advances from 900 gold to
    1000 gold on the boundary tick; the emit must record 900, not 1000.

    Regression for the systematic +1 entity-frame residual measured against the
    OpenDota fixtures (88% / 97% / 100% reductions on gold_t).
    """
    ext = IntervalExtractor()
    parser = FakeParser(tick=1700, game_time_s=58)
    ext.attach(parser)
    ext._on_entity(_player_resource(), EntityOp.UPDATED)

    # Pre-boundary data frame: establishes the "previous" values (900 gold).
    parser.tick = 1798
    ext._on_entity(_radiant_data_with(900, 640, 20, 2, 1450), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    assert ext.snapshots == []  # entity clock not on a boundary yet

    # Boundary tick: data jumps to 1000, then the gamerules proxy crosses t=60.
    parser.tick = 1800
    parser.game_time_s = 60
    ext._on_entity(_radiant_data_with(1000, 700, 22, 3, 1600), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)

    radiant = next(s for s in ext.snapshots if s.team == 2)
    assert radiant.time_s == 60
    # Previous frame (900/640/20/2), NOT the boundary frame (1000/700/22/3).
    assert radiant.gold == 900
    assert radiant.xp == 640
    assert radiant.lh == 20
    assert radiant.dn == 2
    assert radiant.net_worth == 1450


def test_nudge_first_boundary_falls_back_to_live_values():
    """The first boundary has no prior frame, so it reads the live values.

    Before any earlier data update exists, ``_prev_data_*`` is empty and
    ``_team_data_values`` falls back to the live entity. This keeps the very
    first interval (and the single-update unit fixtures) reading the current
    totals — the previous and live frames agree there anyway.
    """
    ext, _parser = _attach_ready_extractor(game_time_s=60)

    radiant = next(s for s in ext.snapshots if s.team == 2)
    assert radiant.gold == 1000  # live values, no prior frame to fall back from
    assert radiant.xp == 700


def test_final_boundary_keeps_live_terminal_values_not_nudged():
    """The game-end flush deliberately reads terminal values, not a nudged frame.

    Unlike a regular boundary, ``_emit_final_boundary`` is a terminal read: there
    is no future crossing whose on-tick increment must be excluded, so it keeps
    the last-observed team-data values. The explicit live-value mode selects the
    current frame even when it arrives on the game-end tick. Here a terminal
    frame (1500 gold) is recorded over an older frame; the final boundary must
    emit 1500, not the earlier nudge frame.

    Guards against a future change wrongly extending the nudge to the final
    minute, which would regress the terminal value (measured to match OpenDota
    within 1 unit).
    """
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=60)
    ext.attach(parser)
    ext._on_entity(_player_resource(), EntityOp.UPDATED)

    # First boundary at t=60 establishes _next_interval_s = 120.
    ext._on_entity(_radiant_data_with(1000, 700, 22, 3, 1600), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)
    ext._on_entity(_ent("CDOTAGamerulesProxy"), EntityOp.UPDATED)
    assert len(ext.snapshots) == 2

    # Establish an older post-boundary frame that the regular nudge would use.
    parser.tick = 3500
    parser.game_time_s = 122
    ext._on_entity(_radiant_data_with(1300, 900, 27, 4, 1950), EntityOp.UPDATED)
    ext._on_entity(_dire_data(), EntityOp.UPDATED)

    # The terminal frame arrives on the same tick as postGame. Recovery must
    # bypass the normal crossing-tick nudge and retain these live values.
    parser.tick = 3560
    ext._on_entity(_radiant_data_with(1500, 1100, 30, 5, 2200), EntityOp.UPDATED)
    ext._on_game_end(parser.tick)

    final_radiant = next(s for s in ext.snapshots if s.team == 2 and s.time_s == 120)
    assert final_radiant.gold == 1500
    assert final_radiant.xp == 1100
    assert final_radiant.lh == 30


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


def test_team_counters_track_last_observed_values():
    """``team_counters`` returns the latest m_vecDataTeam counter totals.

    The counters (camps/creeps stacked, wards placed, rune pickups, tower kills)
    are read from the same data entity as gold/xp, keyed by logical player id via
    the same team-slot mapping used for interval emission.
    """
    ext = IntervalExtractor()
    parser = FakeParser(tick=1800, game_time_s=60)
    ext.attach(parser)
    ext._on_entity(_player_resource(), EntityOp.UPDATED)

    # Radiant slot 1 = player_id 0 in the _player_resource() mapping.
    radiant = _ent(
        "CDOTADataRadiant",
        **{
            "m_vecDataTeam.0001.m_iCampsStacked": 9,
            "m_vecDataTeam.0001.m_iCreepsStacked": 21,
            "m_vecDataTeam.0001.m_iObserverWardsPlaced": 6,
            "m_vecDataTeam.0001.m_iSentryWardsPlaced": 4,
            "m_vecDataTeam.0001.m_iRunePickups": 3,
            "m_vecDataTeam.0001.m_iTowerKills": 2,
        },
    )
    ext._on_entity(radiant, EntityOp.UPDATED)

    counters = ext.team_counters(0)
    assert counters["camps_stacked"] == 9
    assert counters["creeps_stacked"] == 21
    assert counters["obs_placed"] == 6
    assert counters["sen_placed"] == 4
    assert counters["rune_pickups"] == 3
    assert counters["tower_kills"] == 2

    # Unseen player defaults all counters to zero (and roshan_kills is absent).
    empty = ext.team_counters(5)
    assert empty == dict.fromkeys(
        (
            "camps_stacked",
            "creeps_stacked",
            "obs_placed",
            "sen_placed",
            "rune_pickups",
            "tower_kills",
        ),
        0,
    )
