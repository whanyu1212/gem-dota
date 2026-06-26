"""Unit tests for gem.extractors.smoke_vision.

Covers SmokeExtractor and VisionModifierExtractor — the attach()/finalize()
contract, team/centroid back-fill, the LIFO vision-modifier stacking, and the
documented empty-group smoke edge case. All tests use fake combat log entries —
no real .dem files.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from gem.combat.log import CombatLogEntry
from gem.extractors.smoke_vision import SmokeExtractor, VisionModifierExtractor

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _entry(**kwargs) -> CombatLogEntry:
    defaults = {
        "tick": 100,
        "log_type": "MODIFIER_ADD",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_lina",
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
        self._handlers: list = []

    def on_combat_log_entry(self, handler) -> None:
        self._handlers.append(handler)

    def fire(self, entry: CombatLogEntry) -> None:
        for h in self._handlers:
            h(entry)


def _fake_player_ext(
    *,
    teams: dict[str, int] | None = None,
    positions: dict[str, tuple[float, float]] | None = None,
) -> MagicMock:
    """A PlayerExtractor stand-in exposing snapshots + hero_pos."""
    teams = teams or {}
    positions = positions or {}
    snaps = []
    for npc, team in teams.items():
        snap = MagicMock()
        snap.npc_name = npc
        snap.team = team
        snaps.append(snap)
    pe = MagicMock()
    pe.snapshots = snaps
    pe.hero_pos.side_effect = lambda npc: positions.get(npc)
    return pe


# ---------------------------------------------------------------------------
# VisionModifierExtractor
# ---------------------------------------------------------------------------


class TestVisionModifierExtractor:
    def test_add_then_remove_opens_and_closes_window(self):
        pe = _fake_player_ext(teams={"npc_dota_hero_slardar": 2})
        ext = VisionModifierExtractor(pe)
        parser = FakeParser()
        ext.attach(parser)

        parser.fire(
            _entry(
                tick=100,
                log_type="MODIFIER_ADD",
                inflictor_name="modifier_slardar_amplify_damage",
                attacker_name="npc_dota_hero_slardar",
                target_name="npc_dota_hero_lina",
            )
        )
        parser.fire(
            _entry(
                tick=250,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_slardar_amplify_damage",
                attacker_name="npc_dota_hero_slardar",
                target_name="npc_dota_hero_lina",
            )
        )
        events = ext.finalize()
        assert len(events) == 1
        ev = events[0]
        assert ev.tick == 100
        assert ev.end_tick == 250
        assert ev.caster_team == 2  # back-filled from snapshots

    def test_non_vision_modifier_ignored(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(log_type="MODIFIER_ADD", inflictor_name="modifier_some_random_buff"))
        assert ext.finalize() == []

    def test_unclosed_modifier_keeps_none_end_tick(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(
            _entry(
                log_type="MODIFIER_ADD",
                inflictor_name="modifier_bounty_hunter_track",
            )
        )
        events = ext.finalize()
        assert len(events) == 1
        assert events[0].end_tick is None

    def test_stacked_adds_close_lifo(self):
        # Same (modifier, target) applied twice; two removes close most-recent-first.
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_item_dustofappearance",
            "target_name": "npc_dota_hero_riki",
        }
        parser.fire(_entry(tick=100, log_type="MODIFIER_ADD", **common))
        parser.fire(_entry(tick=120, log_type="MODIFIER_ADD", **common))
        parser.fire(_entry(tick=200, log_type="MODIFIER_REMOVE", **common))
        parser.fire(_entry(tick=300, log_type="MODIFIER_REMOVE", **common))
        events = ext.finalize()
        assert len(events) == 2
        # LIFO: the second add (tick=120) is closed first (end=200); first add
        # (tick=100) closed at 300.
        by_tick = {e.tick: e.end_tick for e in events}
        assert by_tick == {100: 300, 120: 200}


# ---------------------------------------------------------------------------
# SmokeExtractor
# ---------------------------------------------------------------------------


class TestSmokeExtractor:
    def test_item_then_modifiers_builds_group_and_centroid(self):
        pe = _fake_player_ext(
            teams={"npc_dota_hero_axe": 2},
            positions={
                "npc_dota_hero_lina": (100.0, 200.0),
                "npc_dota_hero_axe": (300.0, 400.0),
            },
        )
        ext = SmokeExtractor(pe)
        parser = FakeParser()
        ext.attach(parser)

        parser.fire(
            _entry(
                tick=500,
                log_type="ITEM",
                inflictor_name="item_smoke_of_deceit",
                attacker_name="npc_dota_hero_axe",
            )
        )
        for target in ("npc_dota_hero_lina", "npc_dota_hero_axe"):
            parser.fire(
                _entry(
                    tick=502,
                    log_type="MODIFIER_ADD",
                    inflictor_name="modifier_smoke_of_deceit",
                    attacker_name="npc_dota_hero_axe",
                    target_name=target,
                    target_is_hero=True,
                )
            )
        events = ext.finalize()
        assert len(events) == 1
        ev = events[0]
        assert ev.activator == "npc_dota_hero_axe"
        assert ev.team == 2
        assert set(ev.smoked) == {"npc_dota_hero_lina", "npc_dota_hero_axe"}
        # centroid = mean of (100,200) and (300,400)
        assert ev.x == 200.0
        assert ev.y == 300.0

    def test_non_hero_modifier_target_excluded_from_group(self):
        # Summoned units (target_is_hero=False) must not join the smoke group.
        pe = _fake_player_ext(teams={"npc_dota_hero_beastmaster": 3})
        ext = SmokeExtractor(pe)
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(
            _entry(
                tick=10,
                log_type="ITEM",
                inflictor_name="item_smoke_of_deceit",
                attacker_name="npc_dota_hero_beastmaster",
            )
        )
        parser.fire(
            _entry(
                tick=12,
                log_type="MODIFIER_ADD",
                inflictor_name="modifier_smoke_of_deceit",
                attacker_name="npc_dota_hero_beastmaster",
                target_name="npc_dota_beastmaster_boar",
                target_is_hero=False,
            )
        )
        events = ext.finalize()
        assert len(events) == 1
        assert events[0].smoked == []  # boar excluded

    def test_empty_group_edge_case_still_emits_event(self):
        # Documented case: smoke breaks instantly (sentry truesight) so no
        # MODIFIER_ADD fires. The ITEM event is still recorded with an empty group
        # and no position.
        pe = _fake_player_ext(teams={"npc_dota_hero_axe": 2})
        ext = SmokeExtractor(pe)
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(
            _entry(
                tick=10,
                log_type="ITEM",
                inflictor_name="item_smoke_of_deceit",
                attacker_name="npc_dota_hero_axe",
            )
        )
        events = ext.finalize()
        assert len(events) == 1
        assert events[0].smoked == []
        assert events[0].x is None
        assert events[0].y is None
        assert events[0].team == 2  # team still back-filled
