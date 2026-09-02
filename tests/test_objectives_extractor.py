"""Unit tests for gem.extractors.objectives.

Covers ObjectivesExtractor (roshan kills, tower kills, barracks kills,
aegis events), _find_team helper, and _AEGIS_EVENT_TYPE dispatch.
All tests use fake combat log entries — no real .dem files.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from gem.combat.log import CombatLogEntry

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_combat_log_entry(**kwargs):
    defaults = {
        "tick": 100,
        "log_type": "DEATH",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_juggernaut",
        "inflictor_name": "",
        "value": 0,
        "attacker_is_hero": True,
        "target_is_hero": True,
        "attacker_is_illusion": False,
        "target_is_illusion": False,
        "ability_level": 0,
        "gold_reason": 0,
        "xp_reason": 0,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


class FakeParser:
    def __init__(self) -> None:
        self._combat_log_handlers = []
        self._chat_event_handlers = []
        self._entity_handlers = []
        self.tick = 0
        self.entity_manager = None

    def on_combat_log_entry(self, handler) -> None:
        self._combat_log_handlers.append(handler)

    def on_chat_event(self, handler) -> None:
        self._chat_event_handlers.append(handler)

    def on_entity(self, handler) -> None:
        self._entity_handlers.append(handler)

    def _on_entity_filtered(self, handler, **_filters) -> None:
        self.on_entity(handler)

    def on_game_start(self, handler) -> None:
        pass

    def on_game_end(self, handler) -> None:
        pass

    def fire_combat_log(self, entry) -> None:
        for h in self._combat_log_handlers:
            h(entry)

    def fire_entity(self, entity, op, *, tick=None) -> None:
        if tick is not None:
            self.tick = tick
        for h in self._entity_handlers:
            h(entity, op)


class _FakeBannerEntity:
    """Minimal entity stub for the planted Roshan's Banner unit.

    Carries only the fields ``_on_banner_unit`` reads (class name, index,
    life state, team). Owner resolution and position are left absent so the
    handler falls back to ``player_id=-1`` / ``None`` coordinates.
    """

    def __init__(self, idx, life_state, team=2) -> None:
        self._idx = idx
        self._life_state = life_state
        self._team = team

    def get_class_name(self):
        return "CDOTA_Unit_Roshans_Banner"

    def get_index(self):
        return self._idx

    def get_int32(self, field):
        if field == "m_lifeState":
            return self._life_state
        if field == "m_iTeamNum":
            return self._team
        return None

    def get_uint32(self, field):
        return None

    def get_float32(self, field):
        return None


class _FakeItemEntity:
    """Minimal entity stub for a Roshan-dropped ``CDOTA_Item_*`` entity."""

    def __init__(self, idx, class_name) -> None:
        self._idx = idx
        self._class_name = class_name

    def get_class_name(self):
        return self._class_name

    def get_index(self):
        return self._idx

    def get_int32(self, field):
        return None

    def get_uint32(self, field):
        return None

    def get_float32(self, field):
        return None


# ---------------------------------------------------------------------------
# ObjectivesExtractor
# ---------------------------------------------------------------------------


class TestObjectivesExtractor:
    def _make(self):
        from gem.extractors.objectives import ObjectivesExtractor

        e = ObjectivesExtractor()
        parser = FakeParser()
        e.attach(parser)
        return e, parser

    def test_attach_registers_combat_log_callback(self):
        _, parser = self._make()
        assert len(parser._combat_log_handlers) == 1

    def test_roshan_kill_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=500, target_name="npc_dota_roshan", attacker_name="npc_dota_hero_axe"
            )
        )
        assert len(ext.roshan_kills) == 1
        kill = ext.roshan_kills[0]
        assert kill.tick == 500
        assert kill.killer == "npc_dota_hero_axe"
        assert kill.kill_number == 1

    def test_roshan_kill_number_increments(self):
        ext, parser = self._make()
        for tick in (500, 2000, 4000):
            parser.fire_combat_log(_make_combat_log_entry(tick=tick, target_name="npc_dota_roshan"))
        assert [k.kill_number for k in ext.roshan_kills] == [1, 2, 3]

    def test_tower_kill_radiant_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=300,
                target_name="npc_dota_goodguys_tower1_top",
                attacker_name="npc_dota_hero_axe",
            )
        )
        assert len(ext.tower_kills) == 1
        tk = ext.tower_kills[0]
        assert tk.team == 2
        assert tk.tower_name == "npc_dota_goodguys_tower1_top"

    def test_tower_kill_dire_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=300,
                target_name="npc_dota_badguys_tower1_top",
                attacker_name="npc_dota_hero_juggernaut",
            )
        )
        assert len(ext.tower_kills) == 1
        assert ext.tower_kills[0].team == 3

    def test_barracks_kill_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=700,
                target_name="npc_dota_goodguys_melee_rax_top",
                attacker_name="npc_dota_hero_axe",
            )
        )
        assert len(ext.barracks_kills) == 1
        bk = ext.barracks_kills[0]
        assert bk.team == 2
        assert bk.killer == "npc_dota_hero_axe"

    def test_non_death_entry_ignored(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(log_type="DAMAGE", target_name="npc_dota_roshan")
        )
        assert ext.roshan_kills == []
        assert ext.tower_kills == []

    def test_hero_death_not_captured(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(log_type="DEATH", target_name="npc_dota_hero_axe")
        )
        assert ext.roshan_kills == []
        assert ext.tower_kills == []
        assert ext.barracks_kills == []
        assert ext.courier_deaths == []

    def test_courier_death_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=500,
                target_name="npc_dota_courier",
                attacker_name="npc_dota_hero_axe",
            )
        )
        assert len(ext.courier_deaths) == 1
        cd = ext.courier_deaths[0]
        assert cd.tick == 500
        assert cd.killer == "npc_dota_hero_axe"

    def test_courier_death_suffixed_name(self):
        # Couriers may carry a suffixed name; prefix match still captures them.
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(tick=600, target_name="npc_dota_courier_radiant")
        )
        assert len(ext.courier_deaths) == 1


# ---------------------------------------------------------------------------
# _find_team helper
# ---------------------------------------------------------------------------


class TestFindTeam:
    def test_radiant_tower(self):
        from gem.extractors.objectives import _TOWER_TEAM, _find_team

        assert _find_team("npc_dota_goodguys_tower1", _TOWER_TEAM) == 2

    def test_dire_tower(self):
        from gem.extractors.objectives import _TOWER_TEAM, _find_team

        assert _find_team("npc_dota_badguys_tower3", _TOWER_TEAM) == 3

    def test_unknown_returns_zero(self):
        from gem.extractors.objectives import _TOWER_TEAM, _find_team

        assert _find_team("npc_dota_roshan", _TOWER_TEAM) == 0

    def test_radiant_barracks(self):
        from gem.extractors.objectives import _BARRACKS_TEAM, _find_team

        assert _find_team("npc_dota_goodguys_melee_rax_top", _BARRACKS_TEAM) == 2

    def test_dire_barracks(self):
        from gem.extractors.objectives import _BARRACKS_TEAM, _find_team

        assert _find_team("npc_dota_badguys_range_rax_bot", _BARRACKS_TEAM) == 3


# ---------------------------------------------------------------------------
# _AEGIS_EVENT_TYPE dispatch and _on_chat_event
# ---------------------------------------------------------------------------


class TestAegisEventType:
    def test_all_three_types_mapped(self):
        from gem.extractors.objectives import (
            _AEGIS_EVENT_TYPE,
            _CHAT_MSG_AEGIS,
            _CHAT_MSG_AEGIS_STOLEN,
            _CHAT_MSG_DENIED_AEGIS,
        )

        assert _AEGIS_EVENT_TYPE[_CHAT_MSG_AEGIS] == "pickup"
        assert _AEGIS_EVENT_TYPE[_CHAT_MSG_AEGIS_STOLEN] == "stolen"
        assert _AEGIS_EVENT_TYPE[_CHAT_MSG_DENIED_AEGIS] == "denied"

    def test_unknown_type_not_present(self):
        from gem.extractors.objectives import _AEGIS_EVENT_TYPE

        assert _AEGIS_EVENT_TYPE.get(9999) is None

    def test_on_chat_event_pickup(self):
        from gem.extractors.objectives import _CHAT_MSG_AEGIS, ObjectivesExtractor

        ext = ObjectivesExtractor()
        msg = MagicMock(type=_CHAT_MSG_AEGIS, playerid_1=3)
        ext._on_chat_event(msg, tick=1000)
        assert ext.aegis_events[0].event_type == "pickup"
        assert ext.aegis_events[0].player_id == 3

    def test_on_chat_event_stolen(self):
        from gem.extractors.objectives import _CHAT_MSG_AEGIS_STOLEN, ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_AEGIS_STOLEN, playerid_1=7), tick=2000)
        assert ext.aegis_events[0].event_type == "stolen"

    def test_on_chat_event_denied(self):
        from gem.extractors.objectives import _CHAT_MSG_DENIED_AEGIS, ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_DENIED_AEGIS, playerid_1=5), tick=3000)
        assert ext.aegis_events[0].event_type == "denied"

    def test_on_chat_event_ignores_unknown(self):
        from gem.extractors.objectives import ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=9999), tick=500)
        assert ext.aegis_events == []


# ---------------------------------------------------------------------------
# Tormentor kills
# ---------------------------------------------------------------------------


class TestTormentorKills:
    def _make(self):
        from gem.extractors.objectives import ObjectivesExtractor

        ext = ObjectivesExtractor()
        parser = FakeParser()
        ext.attach(parser)
        return ext, parser

    def test_miniboss_death_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=1800, target_name="npc_dota_miniboss", attacker_name="npc_dota_hero_axe"
            )
        )
        assert len(ext.tormentor_kills) == 1
        tk = ext.tormentor_kills[0]
        assert tk.tick == 1800
        assert tk.killer == "npc_dota_hero_axe"
        assert tk.kill_number == 1
        assert tk.killer_player_id == -1  # no chat event yet

    def test_kill_number_increments(self):
        ext, parser = self._make()
        for tick in (1800, 5400):
            parser.fire_combat_log(
                _make_combat_log_entry(tick=tick, target_name="npc_dota_miniboss")
            )
        assert [k.kill_number for k in ext.tormentor_kills] == [1, 2]

    def test_chat_event_patches_killer_player_id(self):
        from gem.extractors.objectives import _CHAT_MSG_MINIBOSS_KILL, ObjectivesExtractor

        ext = ObjectivesExtractor()
        # Simulate DEATH first, then MINIBOSS_KILL chat event
        ext._on_combat_log(_make_combat_log_entry(tick=1800, target_name="npc_dota_miniboss"))
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_MINIBOSS_KILL, playerid_1=4), tick=1800)
        assert ext.tormentor_kills[0].killer_player_id == 4

    def test_chat_event_without_prior_death_is_ignored(self):
        from gem.extractors.objectives import _CHAT_MSG_MINIBOSS_KILL, ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_MINIBOSS_KILL, playerid_1=2), tick=1800)
        assert ext.tormentor_kills == []

    def test_non_miniboss_death_not_captured(self):
        ext, parser = self._make()
        parser.fire_combat_log(_make_combat_log_entry(tick=1800, target_name="npc_dota_roshan"))
        assert ext.tormentor_kills == []


# ---------------------------------------------------------------------------
# Shrine kills
# ---------------------------------------------------------------------------


class TestShrineKills:
    def test_shrine_killed_chat_event(self):
        from gem.extractors.objectives import _CHAT_MSG_SHRINE_KILLED, ObjectivesExtractor

        ext = ObjectivesExtractor()
        # value = team that owned the shrine (2=Radiant, 3=Dire)
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_SHRINE_KILLED, value=3), tick=2500)
        assert len(ext.shrine_kills) == 1
        sk = ext.shrine_kills[0]
        assert sk.tick == 2500
        assert sk.team == 3

    def test_multiple_shrine_kills(self):
        from gem.extractors.objectives import _CHAT_MSG_SHRINE_KILLED, ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_SHRINE_KILLED, value=2), tick=1000)
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_SHRINE_KILLED, value=3), tick=2000)
        assert len(ext.shrine_kills) == 2
        assert ext.shrine_kills[0].team == 2
        assert ext.shrine_kills[1].team == 3

    def test_shrine_kill_zero_value_defaults(self):
        from gem.extractors.objectives import _CHAT_MSG_SHRINE_KILLED, ObjectivesExtractor

        ext = ObjectivesExtractor()
        ext._on_chat_event(MagicMock(type=_CHAT_MSG_SHRINE_KILLED, value=None), tick=500)
        assert ext.shrine_kills[0].team == 0


class TestBannerPlantCapture:
    def _make(self):
        from gem.extractors.objectives import ObjectivesExtractor

        ext = ObjectivesExtractor()
        parser = FakeParser()
        ext.attach(parser)
        return ext, parser

    def test_fresh_created_banner_is_a_plant(self):
        from gem.state.entities import EntityOp

        ext, parser = self._make()
        parser.fire_entity(_FakeBannerEntity(5, life_state=0, team=2), EntityOp.CREATED, tick=1000)
        assert len(ext.banner_plants) == 1
        assert ext.banner_plants[0].tick == 1000
        assert ext.banner_plants[0].team == 2

    def test_pure_update_on_live_banner_is_not_a_second_plant(self):
        from gem.state.entities import EntityOp

        ext, parser = self._make()
        parser.fire_entity(_FakeBannerEntity(5, life_state=0), EntityOp.CREATED, tick=1000)
        # A position refresh on the already-alive banner must not re-record it.
        parser.fire_entity(_FakeBannerEntity(5, life_state=0), EntityOp.UPDATED, tick=1005)
        assert len(ext.banner_plants) == 1

    def test_recycled_slot_re_entering_alive_is_a_plant(self):
        # The Codex P2 case: a banner reusing a slot that was deleted re-enters as
        # UPDATED|ENTERED, not CREATED. Gating on CREATED alone would drop it.
        from gem.state.entities import EntityOp

        ext, parser = self._make()
        # First banner on slot 5: planted, dies, slot deleted.
        parser.fire_entity(_FakeBannerEntity(5, life_state=0), EntityOp.CREATED, tick=1000)
        parser.fire_entity(_FakeBannerEntity(5, life_state=1), EntityOp.UPDATED, tick=1300)
        parser.fire_entity(_FakeBannerEntity(5, life_state=2), EntityOp.DELETED, tick=1301)
        # Second banner reuses slot 5, re-entering alive without a CREATED op.
        parser.fire_entity(
            _FakeBannerEntity(5, life_state=0),
            EntityOp.UPDATED | EntityOp.ENTERED,
            tick=2000,
        )
        assert [p.tick for p in ext.banner_plants] == [1000, 2000]

    def test_non_banner_entity_is_ignored(self):
        from gem.state.entities import EntityOp

        ext, parser = self._make()

        class _Other(_FakeBannerEntity):
            def get_class_name(self):
                return "CDOTA_Unit_Hero_Axe"

        parser.fire_entity(_Other(7, life_state=0), EntityOp.CREATED, tick=500)
        assert ext.banner_plants == []


class TestRoshanDropAttribution:
    """A drop belongs to the Roshan whose death it followed. A held-but-unused
    item from an earlier Roshan stays a live ``CDOTA_Item_*`` entity, so the
    snapshot must exclude it from a *later* Roshan's drops (regression for the
    duplicate-banner contamination on real replay 8855188139).
    """

    def _make(self):
        from gem.extractors.objectives import ObjectivesExtractor

        ext = ObjectivesExtractor()
        parser = FakeParser()
        ext.attach(parser)
        return ext, parser

    def test_single_roshan_snapshots_its_drops(self):
        from gem.state.entities import EntityOp

        ext, parser = self._make()
        # Aegis + banner spawn when Roshan spawns, before its death.
        parser.fire_entity(_FakeItemEntity(10, "CDOTA_Item_Aegis"), EntityOp.CREATED, tick=900)
        parser.fire_entity(
            _FakeItemEntity(11, "CDOTA_Item_Roshans_Banner"), EntityOp.CREATED, tick=900
        )
        parser.fire_combat_log(_make_combat_log_entry(tick=1000, target_name="npc_dota_roshan"))
        assert ext.roshan_kills[0].drops == ["aegis", "banner"]

    def test_held_drop_from_earlier_roshan_excluded_from_later(self):
        from gem.state.entities import EntityOp

        ext, parser = self._make()

        # --- Roshan #1: aegis + banner spawn, Roshan dies. ---
        parser.fire_entity(_FakeItemEntity(10, "CDOTA_Item_Aegis"), EntityOp.CREATED, tick=900)
        parser.fire_entity(
            _FakeItemEntity(11, "CDOTA_Item_Roshans_Banner"), EntityOp.CREATED, tick=900
        )
        parser.fire_combat_log(_make_combat_log_entry(tick=1000, target_name="npc_dota_roshan"))
        assert ext.roshan_kills[0].drops == ["aegis", "banner"]

        # Roshan #1's banner (idx 11) is picked up but NOT used — it stays a live
        # entity (no DELETED), exactly the real-replay case. Roshan #2 spawns its
        # own aegis + cheese after Roshan #1's death.
        parser.fire_entity(_FakeItemEntity(20, "CDOTA_Item_Aegis"), EntityOp.CREATED, tick=2900)
        parser.fire_entity(_FakeItemEntity(21, "CDOTA_Item_Cheese"), EntityOp.CREATED, tick=2900)
        parser.fire_combat_log(_make_combat_log_entry(tick=3000, target_name="npc_dota_roshan"))

        # Roshan #2's drops must be its own aegis + cheese — NOT the stale banner.
        assert ext.roshan_kills[1].drops == ["aegis", "cheese"]
        assert "banner" not in ext.roshan_kills[1].drops
