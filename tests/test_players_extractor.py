"""Unit tests for gem.extractors.players.

Covers _pos, _snapshot_hero, PlayerExtractor._on_entity, _maybe_sample,
_sample (with controller and data-team overlays), _read_abilities,
_read_inventory, _diff_inventory, hero_pos, and time_series.
All tests use fake entities and a fake parser — no real .dem files.
"""

from __future__ import annotations

from gem.entities import Entity, EntityOp
from gem.extractors.players import (
    PlayerExtractor,
    PlayerStateSnapshot,
    PlayerTimeSeries,
    _pos,
    _snapshot_hero,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class FakeClass:
    def __init__(self, name: str = "Test") -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _ent(class_name: str = "Test", index: int = 0, serial: int = 0, **state) -> Entity:
    e = Entity(index=index, serial=serial, cls=FakeClass(class_name))
    e._state.update(state)
    return e


def _hero(ending: str = "Axe", player_id: int = 0, **extra) -> Entity:
    """Build a minimal CDOTA_Unit_Hero_* entity."""
    return _ent(
        f"CDOTA_Unit_Hero_{ending}",
        **{
            "m_nPlayerID": player_id * 2,
            "m_iTeamNum": 2,
            "m_nCurrentLevel": 5,
            "m_iCurrentXP": 1000,
            "m_iHealth": 600,
            "m_iMaxHealth": 700,
            "m_flMana": 300.0,
            "m_flMaxMana": 400.0,
            "m_iLastHitCount": 20,
            "m_iDenies": 3,
            **extra,
        },
    )


class FakeCombatLog:
    def __init__(self):
        self.emitted = []

    def _emit(self, entry):
        self.emitted.append(entry)


class FakeParser:
    def __init__(self, tick: int = 300):
        self.tick = tick
        self.entity_manager = None
        self.string_tables = None
        self.combat_log = FakeCombatLog()
        self._handlers = []

    def on_entity(self, h):
        self._handlers.append(h)

    def on_game_start(self, h):
        pass

    def on_game_end(self, h):
        pass


# ---------------------------------------------------------------------------
# _pos
# ---------------------------------------------------------------------------


class TestPos:
    def test_all_fields_present(self):
        e = _ent(
            **{
                "CBodyComponent.m_cellX": 10,
                "CBodyComponent.m_cellY": 20,
                "CBodyComponent.m_vecX": 5.0,
                "CBodyComponent.m_vecY": 7.0,
            }
        )
        result = _pos(e)
        assert result == (10 * 128 + 5.0, 20 * 128 + 7.0)

    def test_missing_cell_x_returns_none(self):
        e = _ent(
            **{
                "CBodyComponent.m_cellY": 1,
                "CBodyComponent.m_vecX": 0.0,
                "CBodyComponent.m_vecY": 0.0,
            }
        )
        assert _pos(e) is None

    def test_missing_vec_y_returns_none(self):
        e = _ent(
            **{
                "CBodyComponent.m_cellX": 1,
                "CBodyComponent.m_cellY": 1,
                "CBodyComponent.m_vecX": 0.0,
            }
        )
        assert _pos(e) is None

    def test_zero_coordinates(self):
        e = _ent(
            **{
                "CBodyComponent.m_cellX": 0,
                "CBodyComponent.m_cellY": 0,
                "CBodyComponent.m_vecX": 0.0,
                "CBodyComponent.m_vecY": 0.0,
            }
        )
        assert _pos(e) == (0.0, 0.0)


# ---------------------------------------------------------------------------
# _snapshot_hero
# ---------------------------------------------------------------------------


class TestSnapshotHero:
    def test_basic_snapshot(self):
        e = _hero("Axe", player_id=0)
        snap = _snapshot_hero(e, tick=100)
        assert snap is not None
        assert snap.player_id == 0
        assert snap.tick == 100
        assert snap.npc_name == "npc_dota_hero_axe"
        assert snap.level == 5
        assert snap.xp == 1000
        assert snap.hp == 600

    def test_player_id_halved(self):
        e = _hero("Pudge", player_id=3)  # m_nPlayerID = 6
        snap = _snapshot_hero(e, tick=0)
        assert snap is not None
        assert snap.player_id == 3

    def test_negative_player_id_returns_none(self):
        e = _ent("CDOTA_Unit_Hero_Axe", **{"m_nPlayerID": -2})
        snap = _snapshot_hero(e, tick=0)
        assert snap is None

    def test_missing_player_id_returns_none(self):
        e = _ent("CDOTA_Unit_Hero_Axe")
        snap = _snapshot_hero(e, tick=0)
        assert snap is None

    def test_fallback_to_m_iPlayerID(self):
        e = _ent("CDOTA_Unit_Hero_Axe", **{"m_iPlayerID": 4})  # player 2
        snap = _snapshot_hero(e, tick=0)
        assert snap is not None
        assert snap.player_id == 2

    def test_gold_zero_by_default(self):
        snap = _snapshot_hero(_hero("Axe"), tick=0)
        assert snap is not None
        assert snap.gold == 0
        assert snap.net_worth == 0

    def test_pos_included_when_available(self):
        e = _hero(
            "Axe",
            **{
                "CBodyComponent.m_cellX": 5,
                "CBodyComponent.m_cellY": 10,
                "CBodyComponent.m_vecX": 1.0,
                "CBodyComponent.m_vecY": 2.0,
            },
        )
        snap = _snapshot_hero(e, tick=0)
        assert snap is not None
        assert snap.x == 5 * 128 + 1.0
        assert snap.y == 10 * 128 + 2.0

    def test_pos_none_when_missing(self):
        e = _hero("Axe")
        snap = _snapshot_hero(e, tick=0)
        assert snap is not None
        assert snap.x is None
        assert snap.y is None

    def test_camelcase_class_name_converted(self):
        e = _ent(
            "CDOTA_Unit_Hero_TemplarAssassin",
            **{
                "m_nPlayerID": 0,
                "m_iTeamNum": 2,
                "m_nCurrentLevel": 1,
                "m_iCurrentXP": 0,
                "m_iHealth": 100,
                "m_iMaxHealth": 100,
                "m_flMana": 0.0,
                "m_flMaxMana": 0.0,
                "m_iLastHitCount": 0,
                "m_iDenies": 0,
            },
        )
        snap = _snapshot_hero(e, tick=0)
        assert snap is not None
        assert snap.npc_name == "npc_dota_hero_templar_assassin"

    def test_underscore_class_name_converted(self):
        # "Shadow_Demon" → ending.replace("_","") = "ShadowDemon"
        # → re.sub camelCase → "_shadow_demon" → "npc_dota_hero_shadow_demon"
        e = _ent(
            "CDOTA_Unit_Hero_Shadow_Demon",
            **{
                "m_nPlayerID": 0,
                "m_iTeamNum": 3,
                "m_nCurrentLevel": 1,
                "m_iCurrentXP": 0,
                "m_iHealth": 100,
                "m_iMaxHealth": 100,
                "m_flMana": 0.0,
                "m_flMaxMana": 0.0,
                "m_iLastHitCount": 0,
                "m_iDenies": 0,
            },
        )
        snap = _snapshot_hero(e, tick=0)
        assert snap is not None
        assert snap.npc_name == "npc_dota_hero_shadow_demon"


# ---------------------------------------------------------------------------
# PlayerExtractor._on_entity — hero registration / deletion
# ---------------------------------------------------------------------------


class TestOnEntityHero:
    def test_hero_registered_on_created(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _hero("Axe", index=5)
        ext._on_entity(e, EntityOp.CREATED)
        assert 5 in ext._heroes
        assert "npc_dota_hero_axe" in ext._heroes_by_npc

    def test_hero_removed_on_deleted(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _hero("Axe", index=5)
        ext._on_entity(e, EntityOp.CREATED)
        ext._on_entity(e, EntityOp.DELETED)
        assert 5 not in ext._heroes

    def test_controller_registered(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTAPlayerController", **{"m_nPlayerID": 2})  # player 1
        ext._on_entity(e, EntityOp.CREATED)
        assert 1 in ext._controllers

    def test_controller_fallback_to_m_iPlayerID(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTAPlayerController", **{"m_iPlayerID": 4})  # player 2
        ext._on_entity(e, EntityOp.CREATED)
        assert 2 in ext._controllers

    def test_controller_deleted(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTAPlayerController", **{"m_nPlayerID": 0})
        ext._on_entity(e, EntityOp.CREATED)
        ext._on_entity(e, EntityOp.DELETED)
        assert 0 not in ext._controllers

    def test_data_radiant_registered(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTADataRadiant")
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._data_radiant is e

    def test_data_radiant_underscore_variant(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTA_DataRadiant")
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._data_radiant is e

    def test_data_dire_registered(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTADataDire")
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._data_dire is e

    def test_data_dire_deleted(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTADataDire")
        ext._on_entity(e, EntityOp.CREATED)
        ext._on_entity(e, EntityOp.DELETED)
        assert ext._data_dire is None

    def test_player_resource_registered(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTA_PlayerResource")
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._player_resource is e

    def test_player_resource_deleted(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("CDOTA_PlayerResource")
        ext._on_entity(e, EntityOp.CREATED)
        ext._on_entity(e, EntityOp.DELETED)
        assert ext._player_resource is None

    def test_unknown_class_ignored(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        e = _ent("SomeRandomClass")
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._heroes == {}
        assert ext._controllers == {}


# ---------------------------------------------------------------------------
# PlayerExtractor.hero_pos
# ---------------------------------------------------------------------------


class TestHeroPos:
    def test_returns_position_when_tracked(self):
        ext = PlayerExtractor()
        parser = FakeParser(tick=0)
        ext.attach(parser)
        e = _hero(
            "Axe",
            **{
                "CBodyComponent.m_cellX": 3,
                "CBodyComponent.m_cellY": 4,
                "CBodyComponent.m_vecX": 0.0,
                "CBodyComponent.m_vecY": 0.0,
            },
        )
        ext._on_entity(e, EntityOp.CREATED)
        pos = ext.hero_pos("npc_dota_hero_axe")
        assert pos is not None
        assert pos[0] == 3 * 128

    def test_returns_none_for_unknown_hero(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        assert ext.hero_pos("npc_dota_hero_nonexistent") is None


# ---------------------------------------------------------------------------
# PlayerExtractor._maybe_sample and _sample
# ---------------------------------------------------------------------------


class TestMaybeSample:
    def test_sample_taken_when_interval_elapsed(self):
        ext = PlayerExtractor(sample_interval=100)
        parser = FakeParser(tick=200)
        ext.attach(parser)
        ext._last_sample = 0
        e = _hero("Axe")
        ext._heroes[0] = e
        ext._maybe_sample()
        assert len(ext.snapshots) == 1

    def test_sample_skipped_when_too_soon(self):
        ext = PlayerExtractor(sample_interval=100)
        parser = FakeParser(tick=50)
        ext.attach(parser)
        ext._last_sample = 0
        e = _hero("Axe")
        ext._heroes[0] = e
        ext._maybe_sample()
        assert len(ext.snapshots) == 0

    def test_sample_without_parser_does_nothing(self):
        ext = PlayerExtractor()
        ext._parser = None
        ext._maybe_sample()  # should not raise

    def test_controller_gold_overlay(self):
        ext = PlayerExtractor(sample_interval=0)
        parser = FakeParser(tick=100)
        ext.attach(parser)
        hero = _hero("Axe", player_id=0)
        ctrl = _ent("CDOTAPlayerController", **{"m_iGold": 500, "m_iNetWorth": 1500})
        ext._heroes[0] = hero
        ext._controllers[0] = ctrl
        ext._last_sample = -999
        ext._sample(100)
        assert ext.snapshots[0].gold == 500
        assert ext.snapshots[0].net_worth == 1500

    def test_data_radiant_overlay(self):
        ext = PlayerExtractor(sample_interval=0)
        parser = FakeParser(tick=100)
        ext.attach(parser)
        hero = _hero("Axe", player_id=0)  # team=2 → radiant
        data = _ent(
            "CDOTADataRadiant",
            **{
                "m_vecDataTeam.0000.m_iNetWorth": 2000,
                "m_vecDataTeam.0000.m_iTotalEarnedGold": 3000,
                "m_vecDataTeam.0000.m_iLastHitCount": 50,
                "m_vecDataTeam.0000.m_iDenyCount": 5,
            },
        )
        ext._heroes[0] = hero
        ext._data_radiant = data
        ext._player_team_slot[0] = 0
        ext._last_sample = -999
        ext._sample(100)
        snap = ext.snapshots[0]
        assert snap.net_worth == 2000
        assert snap.gold == 3000
        assert snap.lh == 50
        assert snap.dn == 5

    def test_data_dire_overlay(self):
        ext = PlayerExtractor(sample_interval=0)
        parser = FakeParser(tick=100)
        ext.attach(parser)
        # team=3 → dire, player_id=5 (team slot 0)
        hero = _ent(
            "CDOTA_Unit_Hero_Axe",
            **{
                "m_nPlayerID": 10,  # player 5
                "m_iTeamNum": 3,
                "m_nCurrentLevel": 1,
                "m_iCurrentXP": 0,
                "m_iHealth": 100,
                "m_iMaxHealth": 100,
                "m_flMana": 0.0,
                "m_flMaxMana": 0.0,
                "m_iLastHitCount": 0,
                "m_iDenies": 0,
            },
        )
        data = _ent(
            "CDOTADataDire",
            **{
                "m_vecDataTeam.0000.m_iNetWorth": 1800,
                "m_vecDataTeam.0000.m_iLastHitCount": 30,
                "m_vecDataTeam.0000.m_iDenyCount": 2,
            },
        )
        ext._heroes[0] = hero
        ext._data_dire = data
        ext._player_team_slot[5] = 0
        ext._last_sample = -999
        ext._sample(100)
        snap = ext.snapshots[0]
        assert snap.net_worth == 1800
        assert snap.lh == 30


# ---------------------------------------------------------------------------
# PlayerExtractor.time_series
# ---------------------------------------------------------------------------


class TestTimeSeries:
    def test_empty_snapshots(self):
        ext = PlayerExtractor()
        ts = ext.time_series(0)
        assert isinstance(ts, PlayerTimeSeries)
        assert ts.ticks == []

    def test_filters_by_player_id(self):
        ext = PlayerExtractor()
        ext.snapshots = [
            PlayerStateSnapshot(
                tick=100,
                player_id=0,
                npc_name="",
                team=2,
                level=1,
                xp=0,
                gold=100,
                net_worth=200,
                lh=5,
                dn=1,
                hp=600,
                max_hp=700,
                mana=100.0,
                max_mana=200.0,
                x=None,
                y=None,
            ),
            PlayerStateSnapshot(
                tick=100,
                player_id=1,
                npc_name="",
                team=2,
                level=1,
                xp=0,
                gold=200,
                net_worth=300,
                lh=3,
                dn=0,
                hp=500,
                max_hp=600,
                mana=50.0,
                max_mana=100.0,
                x=None,
                y=None,
            ),
        ]
        ts = ext.time_series(0)
        assert ts.ticks == [100]
        assert ts.gold_t == [100]

    def test_time_series_fields(self):
        ext = PlayerExtractor()
        ext.snapshots = [
            PlayerStateSnapshot(
                tick=150,
                player_id=2,
                npc_name="",
                team=3,
                level=5,
                xp=1000,
                gold=500,
                net_worth=1500,
                lh=20,
                dn=3,
                hp=400,
                max_hp=700,
                mana=200.0,
                max_mana=400.0,
                x=1.0,
                y=2.0,
            ),
        ]
        ts = ext.time_series(2)
        assert ts.ticks == [150]
        assert ts.gold_t == [500]
        assert ts.net_worth_t == [1500]
        assert ts.lh_t == [20]
        assert ts.dn_t == [3]
        assert ts.xp_t == [1000]
        assert ts.hp_t == [400]
        assert ts.mana_t == [200.0]
        assert ts.x_t == [1.0]
        assert ts.y_t == [2.0]


# ---------------------------------------------------------------------------
# PlayerExtractor._read_abilities — no parser / no entity_manager / no table
# ---------------------------------------------------------------------------


class TestReadAbilities:
    def test_no_parser_returns_empty(self):
        ext = PlayerExtractor()
        ext._parser = None
        assert ext._read_abilities(_hero("Axe")) == {}

    def test_no_entity_manager_returns_empty(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        parser.entity_manager = None
        ext.attach(parser)
        assert ext._read_abilities(_hero("Axe")) == {}

    def test_no_entity_names_table_returns_empty(self):
        from gem.string_table import StringTables

        ext = PlayerExtractor()
        parser = FakeParser()
        parser.entity_manager = object()  # non-None
        parser.string_tables = StringTables()  # no EntityNames table
        ext.attach(parser)
        assert ext._read_abilities(_hero("Axe")) == {}


# ---------------------------------------------------------------------------
# PlayerExtractor._read_inventory — no parser / no entity_manager / no table
# ---------------------------------------------------------------------------


class TestReadInventory:
    def test_no_parser_returns_empty(self):
        ext = PlayerExtractor()
        ext._parser = None
        assert ext._read_inventory(_hero("Axe")) == {}

    def test_no_entity_manager_returns_empty(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        parser.entity_manager = None
        ext.attach(parser)
        assert ext._read_inventory(_hero("Axe")) == {}

    def test_no_entity_names_table_returns_empty(self):
        from gem.string_table import StringTables

        ext = PlayerExtractor()
        parser = FakeParser()
        parser.entity_manager = object()
        parser.string_tables = StringTables()
        ext.attach(parser)
        assert ext._read_inventory(_hero("Axe")) == {}


# ---------------------------------------------------------------------------
# PlayerExtractor._diff_inventory
# ---------------------------------------------------------------------------


class TestDiffInventory:
    def test_no_parser_skips(self):
        ext = PlayerExtractor()
        ext._parser = None
        ext._diff_inventory(_hero("Axe"), 0, "npc_dota_hero_axe", 0)
        # Should not raise

    def test_already_initialized_skips(self):
        ext = PlayerExtractor()
        parser = FakeParser()
        ext.attach(parser)
        ext._inventory_initialized.add(0)
        ext._diff_inventory(_hero("Axe"), 0, "npc_dota_hero_axe", 0)
        assert len(parser.combat_log.emitted) == 0

    def test_first_snapshot_sets_initialized(self):
        from gem.string_table import StringTables

        ext = PlayerExtractor()
        parser = FakeParser()
        parser.entity_manager = None  # _read_inventory will return {}
        parser.string_tables = StringTables()
        ext.attach(parser)
        ext._diff_inventory(_hero("Axe"), 0, "npc_dota_hero_axe", 100)
        assert 0 in ext._inventory_initialized
        assert ext.first_snapshot_tick[0] == 100


# ---------------------------------------------------------------------------
# PlayerExtractor._refresh_team_slots
# ---------------------------------------------------------------------------


class TestRefreshTeamSlots:
    def test_no_player_resource_does_nothing(self):
        ext = PlayerExtractor()
        ext._player_resource = None
        ext._refresh_team_slots()  # should not raise
        assert ext._player_team_slot == {}

    def test_reads_team_slots(self):
        ext = PlayerExtractor()
        pr = _ent(
            "CDOTA_PlayerResource",
            **{
                "m_vecPlayerTeamData.0000.m_iTeamSlot": 2,
                "m_vecPlayerTeamData.0001.m_iTeamSlot": 0,
            },
        )
        ext._player_resource = pr
        ext._refresh_team_slots()
        assert ext._player_team_slot[0] == 2
        assert ext._player_team_slot[1] == 0
