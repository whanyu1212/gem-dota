"""Tests for per-player running combat totals added for ML / rapier use case.

Covers:
  - total_hero_damage, total_hero_healing, total_deaths, total_stuns on
    PlayerStateSnapshot and PlayerTimeSeries
  - Correct accumulation from combat log entries via PlayerExtractor
  - Monotonic growth across snapshots
  - Non-hero events (tower damage, creep deaths) are excluded
  - time_series() and minute_time_series() both include the new lists
  - Integration smoke test (skipped without fixture)
"""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "ti14_finals_g3_xg_vs_falcons.dem"

# ---------------------------------------------------------------------------
# Shared fakes
# ---------------------------------------------------------------------------


class FakeClass:
    def __init__(self, name: str) -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _make_entity(class_name: str, state: dict | None = None):
    from gem.entities import Entity

    e = Entity(index=0, serial=0, cls=FakeClass(class_name))
    if state:
        e._state.update(state)
    return e


class FakeParser:
    """Minimal parser stub that routes entity and combat-log callbacks."""

    def __init__(self, tick: int = 0) -> None:
        self.tick = tick
        self._entity_handlers: list = []
        self._combat_log_handlers: list = []
        self._game_start_handlers: list = []
        self._game_end_handlers: list = []
        self.entity_manager = None
        self.string_tables = type("ST", (), {"get_by_name": lambda self, n: None})()

    def on_entity(self, handler) -> None:
        self._entity_handlers.append(handler)

    def on_combat_log_entry(self, handler) -> None:
        self._combat_log_handlers.append(handler)

    def on_game_start(self, handler) -> None:
        self._game_start_handlers.append(handler)

    def on_game_end(self, handler) -> None:
        self._game_end_handlers.append(handler)

    # helpers for tests --------------------------------------------------

    def fire_entity(self, entity, op) -> None:
        for h in self._entity_handlers:
            h(entity, op)

    def fire_combat_log(self, entry) -> None:
        for h in self._combat_log_handlers:
            h(entry)

    def fire_game_start(self, tick: int = 0) -> None:
        self.tick = tick
        for h in self._game_start_handlers:
            h(tick)

    def fire_game_end(self, tick: int = 0) -> None:
        self.tick = tick
        for h in self._game_end_handlers:
            h(tick)


def _make_combat_entry(**kwargs):
    """Build a CombatLogEntry with sensible defaults for unspecified fields."""
    from gem.combatlog import CombatLogEntry

    defaults = {
        "tick": 0,
        "log_type": "DAMAGE",
        "attacker_name": "",
        "attacker_is_hero": False,
        "target_name": "",
        "target_is_hero": False,
        "value": 0,
        "stun_duration": 0.0,
        "inflictor_name": "",
        "gold_reason": 0,
        "xp_reason": 0,
        "damage_type": "",
        "value_name": "",
        "target_is_illusion": False,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


def _attach_hero(parser: FakeParser, npc_name: str, player_id_raw: int = 0):
    """Register a hero entity so _hero_to_pid() can resolve it."""
    from gem.entities import EntityOp

    # class name: strip "npc_dota_hero_" prefix, CamelCase it minimally
    suffix = npc_name.replace("npc_dota_hero_", "").replace("_", " ").title().replace(" ", "")
    cls_name = f"CDOTA_Unit_Hero_{suffix}"
    hero = _make_entity(
        cls_name,
        {
            "m_nPlayerID": player_id_raw,  # raw value; extractor divides by 2
            "m_iTeamNum": 2,
            "m_nCurrentLevel": 1,
            "m_iCurrentXP": 0,
            "m_iHealth": 1000,
            "m_iMaxHealth": 1000,
            "m_flMana": 200.0,
            "m_flMaxMana": 200.0,
            "m_iLastHitCount": 0,
            "m_iDenies": 0,
        },
    )
    parser.fire_entity(hero, EntityOp.CREATED)
    return hero


# ---------------------------------------------------------------------------
# Snapshot dataclass fields
# ---------------------------------------------------------------------------


class TestSnapshotFields:
    def test_new_fields_default_to_zero(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        snap = PlayerStateSnapshot(
            tick=0,
            player_id=0,
            npc_name="npc_dota_hero_axe",
            team=2,
            level=1,
            xp=0,
            gold=0,
            net_worth=0,
            lh=0,
            dn=0,
            hp=1000,
            max_hp=1000,
            mana=200.0,
            max_mana=200.0,
            x=None,
            y=None,
        )
        assert snap.total_hero_damage == 0
        assert snap.total_hero_healing == 0
        assert snap.total_deaths == 0
        assert snap.total_stuns == 0.0

    def test_new_fields_assignable(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        snap = PlayerStateSnapshot(
            tick=100,
            player_id=1,
            npc_name="npc_dota_hero_axe",
            team=2,
            level=5,
            xp=1000,
            gold=500,
            net_worth=500,
            lh=10,
            dn=0,
            hp=800,
            max_hp=1000,
            mana=200.0,
            max_mana=300.0,
            x=None,
            y=None,
            total_hero_damage=350,
            total_hero_healing=100,
            total_deaths=1,
            total_stuns=2.5,
        )
        assert snap.total_hero_damage == 350
        assert snap.total_hero_healing == 100
        assert snap.total_deaths == 1
        assert snap.total_stuns == 2.5


# ---------------------------------------------------------------------------
# PlayerTimeSeries fields
# ---------------------------------------------------------------------------


class TestTimeSeriesFields:
    def test_new_lists_default_empty(self):
        from gem.extractors._snapshots import PlayerTimeSeries

        ts = PlayerTimeSeries(player_id=0)
        assert ts.total_hero_damage_t == []
        assert ts.total_hero_healing_t == []
        assert ts.total_deaths_t == []
        assert ts.total_stuns_t == []


# ---------------------------------------------------------------------------
# Accumulator logic in PlayerExtractor
# ---------------------------------------------------------------------------


class TestPlayerExtractorAccumulation:
    def _setup(self, npc_name="npc_dota_hero_axe", player_id_raw=0):
        from gem.extractors.players import PlayerExtractor

        parser = FakeParser(tick=0)
        ext = PlayerExtractor(sample_interval=30, minute_snapshots=False)
        ext.attach(parser)
        _attach_hero(parser, npc_name, player_id_raw)
        return parser, ext

    # --- DAMAGE ---

    def test_hero_damage_increments(self):
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        entry = _make_combat_entry(
            log_type="DAMAGE",
            attacker_name="npc_dota_hero_axe",
            attacker_is_hero=True,
            target_name="npc_dota_hero_juggernaut",
            target_is_hero=True,
            value=200,
        )
        parser.fire_combat_log(entry)
        assert ext._total_hero_damage.get(0, 0) == 200

    def test_hero_damage_accumulates(self):
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        for _ in range(3):
            parser.fire_combat_log(
                _make_combat_entry(
                    log_type="DAMAGE",
                    attacker_name="npc_dota_hero_axe",
                    attacker_is_hero=True,
                    target_name="npc_dota_hero_juggernaut",
                    target_is_hero=True,
                    value=100,
                )
            )
        assert ext._total_hero_damage[0] == 300

    def test_non_hero_damage_excluded(self):
        """Damage dealt to a non-hero target (tower, creep) must not count."""
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_goodguys_tower1_top",
                target_is_hero=False,
                value=500,
            )
        )
        assert ext._total_hero_damage.get(0, 0) == 0

    def test_damage_from_non_hero_attacker_excluded(self):
        """Tower/creep damage dealt to a hero must not count."""
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_goodguys_tower1_top",
                attacker_is_hero=False,
                target_name="npc_dota_hero_axe",
                target_is_hero=True,
                value=300,
            )
        )
        assert ext._total_hero_damage.get(0, 0) == 0

    # --- HEALING ---

    def test_healing_increments(self):
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="HEAL",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_juggernaut",
                target_is_hero=True,
                value=150,
            )
        )
        assert ext._total_hero_healing[0] == 150

    def test_healing_non_hero_target_excluded(self):
        """Healing a non-hero (e.g. creep) must not count."""
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="HEAL",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_creep_radiant",
                target_is_hero=False,
                value=100,
            )
        )
        assert ext._total_hero_healing.get(0, 0) == 0

    # --- DEATHS ---

    def test_death_increments(self):
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DEATH",
                attacker_name="npc_dota_hero_juggernaut",
                attacker_is_hero=True,
                target_name="npc_dota_hero_axe",
                target_is_hero=True,
            )
        )
        assert ext._total_deaths[0] == 1

    def test_death_counts_all_causes(self):
        """Deaths from towers, creeps, and heroes all count."""
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        # killed by tower
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DEATH",
                attacker_name="npc_dota_badguys_tower1_top",
                attacker_is_hero=False,
                target_name="npc_dota_hero_axe",
                target_is_hero=True,
            )
        )
        # killed by hero
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DEATH",
                attacker_name="npc_dota_hero_juggernaut",
                attacker_is_hero=True,
                target_name="npc_dota_hero_axe",
                target_is_hero=True,
            )
        )
        assert ext._total_deaths[0] == 2

    def test_non_hero_death_excluded(self):
        """Deaths of non-hero units (creeps) must not be attributed to a player."""
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_creep_radiant",
                target_is_hero=False,
            )
        )
        # axe's death counter must stay 0 (they killed a creep, didn't die)
        assert ext._total_deaths.get(0, 0) == 0

    # --- STUNS ---

    def test_stun_accumulates(self):
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="ABILITY",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_juggernaut",
                target_is_hero=True,
                stun_duration=1.5,
            )
        )
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="ABILITY",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_lion",
                target_is_hero=True,
                stun_duration=2.0,
            )
        )
        assert abs(ext._total_stuns[0] - 3.5) < 1e-9

    def test_stun_zero_duration_not_counted(self):
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_juggernaut",
                target_is_hero=True,
                value=100,
                stun_duration=0.0,
            )
        )
        assert ext._total_stuns.get(0, 0.0) == 0.0

    def test_stun_non_hero_attacker_excluded(self):
        """Stuns applied by non-hero units must not be credited to a player."""
        parser, ext = self._setup("npc_dota_hero_axe", player_id_raw=0)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="ABILITY",
                attacker_name="npc_dota_creep_badguys",
                attacker_is_hero=False,
                target_name="npc_dota_hero_axe",
                target_is_hero=True,
                stun_duration=1.0,
            )
        )
        assert ext._total_stuns.get(0, 0.0) == 0.0

    # --- Multiple players ---

    def test_two_players_independent(self):
        from gem.extractors.players import PlayerExtractor

        parser = FakeParser(tick=0)
        ext = PlayerExtractor(sample_interval=30, minute_snapshots=False)
        ext.attach(parser)
        _attach_hero(parser, "npc_dota_hero_axe", player_id_raw=0)  # pid=0
        _attach_hero(parser, "npc_dota_hero_juggernaut", player_id_raw=2)  # pid=1

        # axe deals damage to jugg
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_juggernaut",
                target_is_hero=True,
                value=300,
            )
        )
        # jugg deals damage to axe
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_juggernaut",
                attacker_is_hero=True,
                target_name="npc_dota_hero_axe",
                target_is_hero=True,
                value=200,
            )
        )
        assert ext._total_hero_damage[0] == 300
        assert ext._total_hero_damage[1] == 200


# ---------------------------------------------------------------------------
# Snapshot stamping — running totals appear in snapshots
# ---------------------------------------------------------------------------


class TestSnapshotStamping:
    def _build_snapshot_with_damage(self, damage: int):
        from gem.entities import EntityOp
        from gem.extractors.players import PlayerExtractor

        parser = FakeParser(tick=0)
        ext = PlayerExtractor(sample_interval=1, minute_snapshots=False)
        ext.attach(parser)
        hero = _attach_hero(parser, "npc_dota_hero_axe", player_id_raw=0)

        # Fire a damage event before the next sample
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_juggernaut",
                target_is_hero=True,
                value=damage,
            )
        )
        # Trigger a sample by updating tick and firing entity update
        parser.tick = 10
        parser.fire_entity(hero, EntityOp.UPDATED)

        snaps = [s for s in ext.snapshots if s.player_id == 0]
        assert snaps, "expected at least one snapshot for player 0"
        return snaps[-1]

    def test_snapshot_carries_damage(self):
        snap = self._build_snapshot_with_damage(400)
        assert snap.total_hero_damage == 400

    def test_snapshot_carries_zero_when_no_damage(self):
        from gem.entities import EntityOp
        from gem.extractors.players import PlayerExtractor

        parser = FakeParser(tick=0)
        ext = PlayerExtractor(sample_interval=1, minute_snapshots=False)
        ext.attach(parser)
        hero = _attach_hero(parser, "npc_dota_hero_axe", player_id_raw=0)
        parser.tick = 10
        parser.fire_entity(hero, EntityOp.UPDATED)
        snaps = [s for s in ext.snapshots if s.player_id == 0]
        assert snaps[-1].total_hero_damage == 0
        assert snaps[-1].total_hero_healing == 0
        assert snaps[-1].total_deaths == 0
        assert snaps[-1].total_stuns == 0.0

    def test_snapshots_are_monotonic(self):
        """Running totals must never decrease across successive snapshots."""
        from gem.entities import EntityOp
        from gem.extractors.players import PlayerExtractor

        parser = FakeParser(tick=0)
        ext = PlayerExtractor(sample_interval=1, minute_snapshots=False)
        ext.attach(parser)
        hero = _attach_hero(parser, "npc_dota_hero_axe", player_id_raw=0)

        for tick in range(1, 11):
            parser.fire_combat_log(
                _make_combat_entry(
                    log_type="DAMAGE",
                    attacker_name="npc_dota_hero_axe",
                    attacker_is_hero=True,
                    target_name="npc_dota_hero_juggernaut",
                    target_is_hero=True,
                    value=50,
                )
            )
            parser.tick = tick
            parser.fire_entity(hero, EntityOp.UPDATED)

        snaps = [s for s in ext.snapshots if s.player_id == 0]
        damages = [s.total_hero_damage for s in snaps]
        assert damages == sorted(damages), "total_hero_damage must be non-decreasing"


# ---------------------------------------------------------------------------
# time_series() and minute_time_series() include new lists
# ---------------------------------------------------------------------------


class TestTimeSeriesInclusion:
    def _build_ext_with_events(self):
        from gem.entities import EntityOp
        from gem.extractors.players import PlayerExtractor

        parser = FakeParser(tick=0)
        ext = PlayerExtractor(sample_interval=1, minute_snapshots=True)
        ext.attach(parser)
        hero = _attach_hero(parser, "npc_dota_hero_axe", player_id_raw=0)

        # Simulate game start so minute snapshots are enabled
        parser.fire_game_start(0)

        # Fire some events and advance ticks
        for tick in [1, 30, 60]:
            parser.fire_combat_log(
                _make_combat_entry(
                    log_type="DAMAGE",
                    attacker_name="npc_dota_hero_axe",
                    attacker_is_hero=True,
                    target_name="npc_dota_hero_juggernaut",
                    target_is_hero=True,
                    value=100,
                )
            )
            parser.tick = tick
            parser.fire_entity(hero, EntityOp.UPDATED)

        return ext

    def test_time_series_has_new_lists(self):
        ext = self._build_ext_with_events()
        ts = ext.time_series(0)
        assert len(ts.total_hero_damage_t) > 0
        assert len(ts.total_hero_damage_t) == len(ts.ticks)

    def test_time_series_all_new_lists_same_length(self):
        ext = self._build_ext_with_events()
        ts = ext.time_series(0)
        n = len(ts.ticks)
        assert len(ts.total_hero_damage_t) == n
        assert len(ts.total_hero_healing_t) == n
        assert len(ts.total_deaths_t) == n
        assert len(ts.total_stuns_t) == n

    def test_time_series_damage_values_correct(self):
        ext = self._build_ext_with_events()
        ts = ext.time_series(0)
        # Each of the 3 fired events added 100 damage; values must be non-decreasing
        assert ts.total_hero_damage_t[-1] == 300
        assert ts.total_hero_damage_t == sorted(ts.total_hero_damage_t)

    def test_minute_time_series_has_new_lists(self):
        ext = self._build_ext_with_events()
        ts = ext.minute_time_series(0)
        # minute_time_series may be empty if no minute boundaries fired,
        # but if populated the lists must all have the same length as ticks
        if ts.ticks:
            n = len(ts.ticks)
            assert len(ts.total_hero_damage_t) == n
            assert len(ts.total_hero_healing_t) == n
            assert len(ts.total_deaths_t) == n
            assert len(ts.total_stuns_t) == n

    def test_per_minute_diff_gives_interval_damage(self):
        """Diff of total_hero_damage_t between consecutive minutes = damage in that window."""
        from gem.entities import EntityOp
        from gem.extractors.players import PlayerExtractor

        parser = FakeParser(tick=0)
        ext = PlayerExtractor(sample_interval=1, minute_snapshots=True)
        ext.attach(parser)
        hero = _attach_hero(parser, "npc_dota_hero_axe", player_id_raw=0)
        parser.fire_game_start(0)

        # Fire 100 damage in minute 0 (ticks 0–1799)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_juggernaut",
                target_is_hero=True,
                value=100,
            )
        )
        # Trigger minute-0 snapshot at tick 0
        parser.tick = 0
        parser.fire_entity(hero, EntityOp.UPDATED)

        # Fire 200 damage in minute 1 (after tick 1800)
        parser.fire_combat_log(
            _make_combat_entry(
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                target_name="npc_dota_hero_juggernaut",
                target_is_hero=True,
                value=200,
            )
        )
        # Trigger minute-1 snapshot at tick 1800
        parser.tick = 1800
        parser.fire_entity(hero, EntityOp.UPDATED)

        ts = ext.minute_time_series(0)
        assert len(ts.total_hero_damage_t) == 2
        assert ts.total_hero_damage_t[0] == 100  # end of minute 0: 100 cumulative
        assert ts.total_hero_damage_t[1] == 300  # end of minute 1: 300 cumulative
        # per-minute damage = diff
        assert ts.total_hero_damage_t[1] - ts.total_hero_damage_t[0] == 200


# ---------------------------------------------------------------------------
# Integration smoke test
# ---------------------------------------------------------------------------


@pytest.mark.slow
@pytest.mark.integration
class TestMLTotalsIntegration:
    @pytest.fixture(autouse=True)
    def _require_fixture(self):
        if not FIXTURE.exists():
            pytest.skip("Integration fixture not available")

    def test_running_totals_populated(self):
        from gem.extractors.players import PlayerExtractor
        from gem.parser import ReplayParser

        parser = ReplayParser(str(FIXTURE))
        ext = PlayerExtractor(sample_interval=300)
        ext.attach(parser)
        parser.parse()

        # At least one player should have non-zero hero damage by end of game
        total_damage_sum = sum(
            ext.time_series(pid).total_hero_damage_t[-1]
            for pid in range(10)
            if ext.time_series(pid).total_hero_damage_t
        )
        assert total_damage_sum > 0, "expected non-zero total hero damage across all players"

    def test_running_totals_monotonic_in_time_series(self):
        from gem.extractors.players import PlayerExtractor
        from gem.parser import ReplayParser

        parser = ReplayParser(str(FIXTURE))
        ext = PlayerExtractor(sample_interval=300)
        ext.attach(parser)
        parser.parse()

        for pid in range(10):
            ts = ext.time_series(pid)
            if not ts.total_hero_damage_t:
                continue
            assert ts.total_hero_damage_t == sorted(ts.total_hero_damage_t), (
                f"player {pid}: total_hero_damage_t not monotonic"
            )
            assert ts.total_deaths_t == sorted(ts.total_deaths_t), (
                f"player {pid}: total_deaths_t not monotonic"
            )

    def test_time_series_list_lengths_equal(self):
        from gem.extractors.players import PlayerExtractor
        from gem.parser import ReplayParser

        parser = ReplayParser(str(FIXTURE))
        ext = PlayerExtractor(sample_interval=300)
        ext.attach(parser)
        parser.parse()

        for pid in range(10):
            ts = ext.time_series(pid)
            n = len(ts.ticks)
            assert len(ts.total_hero_damage_t) == n, f"player {pid}: damage list length mismatch"
            assert len(ts.total_hero_healing_t) == n, f"player {pid}: healing list length mismatch"
            assert len(ts.total_deaths_t) == n, f"player {pid}: deaths list length mismatch"
            assert len(ts.total_stuns_t) == n, f"player {pid}: stuns list length mismatch"
