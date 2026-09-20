"""Unit tests for gem.extractors.smoke_vision.

Covers SmokeExtractor and VisionModifierExtractor — the attach()/finalize()
contract, team/centroid back-fill, the LIFO vision-modifier stacking, and the
documented empty-group smoke edge case. All tests use fake combat log entries —
no real .dem files.
"""

from __future__ import annotations

from types import SimpleNamespace
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
    snapshots: list[SimpleNamespace] | None = None,
) -> MagicMock:
    """A PlayerExtractor stand-in exposing sampled player states."""
    teams = teams or {}
    positions = positions or {}
    snaps = list(snapshots or [])
    for player_id, npc in enumerate(sorted(set(teams) | set(positions))):
        position = positions.get(npc)
        snaps.append(
            SimpleNamespace(
                tick=100,
                player_id=player_id,
                npc_name=npc,
                team=teams.get(npc, 0),
                x=position[0] if position else None,
                y=position[1] if position else None,
            )
        )
    pe = MagicMock()
    pe.snapshots = snaps
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

    def test_tracks_individual_removals_without_closing_group(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(
            _entry(
                tick=100,
                log_type="ITEM",
                inflictor_name="item_smoke_of_deceit",
                attacker_name="npc_dota_hero_axe",
            )
        )
        for tick, target in ((101, "npc_dota_hero_axe"), (102, "npc_dota_hero_lina")):
            parser.fire(
                _entry(
                    tick=tick,
                    log_type="MODIFIER_ADD",
                    inflictor_name="modifier_smoke_of_deceit",
                    target_name=target,
                    modifier_duration_s=45.0,
                )
            )
        parser.fire(
            _entry(
                tick=300,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_axe",
                modifier_elapsed_duration_s=6.6,
            )
        )

        participants = {p.hero_name: p for p in ext.finalize()[0].participants}
        assert participants["npc_dota_hero_axe"].removed_tick == 300
        assert participants["npc_dota_hero_axe"].modifier_elapsed_duration_s == 6.6
        assert participants["npc_dota_hero_lina"].removed_tick is None

    def test_duplicate_and_out_of_order_adds_use_canonical_activation(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        for tick in (100, 200):
            parser.fire(
                _entry(
                    tick=tick,
                    log_type="ITEM",
                    inflictor_name="item_smoke_of_deceit",
                )
            )

        # New activation arrives first, then a delayed add carrying an older tick.
        parser.fire(
            _entry(
                tick=202,
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_axe",
                modifier_duration_s=45.0,
            )
        )
        parser.fire(
            _entry(
                tick=120,
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_lina",
                modifier_duration_s=45.0,
            )
        )
        # Duplicate with an earlier canonical tick updates rather than appending.
        parser.fire(
            _entry(
                tick=118,
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_lina",
                modifier_duration_s=45.0,
            )
        )

        events = ext.finalize()
        assert [participant.hero_name for participant in events[0].participants] == [
            "npc_dota_hero_lina"
        ]
        assert events[0].participants[0].applied_tick == 118
        assert [participant.hero_name for participant in events[1].participants] == [
            "npc_dota_hero_axe"
        ]

    def test_stale_add_does_not_attach_to_historical_activation(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(tick=100, log_type="ITEM", inflictor_name="item_smoke_of_deceit"))
        parser.fire(
            _entry(
                tick=500,
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_lina",
            )
        )

        events = ext.finalize()
        assert len(events) == 1
        assert events[0].participants == []

    def test_late_join_with_shortened_duration_stays_with_activation(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(tick=100, log_type="ITEM", inflictor_name="item_smoke_of_deceit"))
        parser.fire(
            _entry(
                tick=182,
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_mars",
                modifier_duration_s=42.23,
            )
        )

        participant = ext.finalize()[0].participants[0]
        assert participant.hero_name == "npc_dota_hero_mars"
        assert participant.applied_tick == 182
        assert participant.modifier_duration_s == 42.23

    def test_stale_remove_does_not_close_historical_participant(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(tick=100, log_type="ITEM", inflictor_name="item_smoke_of_deceit"))
        parser.fire(
            _entry(
                tick=101,
                inflictor_name="modifier_smoke_of_deceit",
                modifier_duration_s=1.0,
            )
        )
        parser.fire(
            _entry(
                tick=500,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_smoke_of_deceit",
            )
        )

        assert ext.finalize()[0].participants[0].removed_tick is None

    def test_multiple_same_caster_and_concurrent_caster_activations_survive(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        uses = (
            (100, "npc_dota_hero_axe"),
            (130, "npc_dota_hero_axe"),
            (131, "npc_dota_hero_invoker"),
        )
        for tick, caster in uses:
            parser.fire(
                _entry(
                    tick=tick,
                    log_type="ITEM",
                    inflictor_name="item_smoke_of_deceit",
                    attacker_name=caster,
                )
            )
        parser.fire(
            _entry(
                tick=132,
                inflictor_name="modifier_smoke_of_deceit",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_lina",
            )
        )
        parser.fire(
            _entry(
                tick=133,
                inflictor_name="modifier_smoke_of_deceit",
                attacker_name="npc_dota_hero_invoker",
                target_name="npc_dota_hero_crystal_maiden",
            )
        )

        events = ext.finalize()
        assert len(events) == 3
        assert events[0].participants == []
        assert events[1].smoked == ["npc_dota_hero_lina"]
        assert events[2].smoked == ["npc_dota_hero_crystal_maiden"]

    def test_finalize_uses_each_canonical_tick_for_positions(self):
        snapshots = [
            SimpleNamespace(
                tick=100,
                player_id=0,
                npc_name="npc_dota_hero_axe",
                team=2,
                x=10.0,
                y=20.0,
            ),
            SimpleNamespace(
                tick=102,
                player_id=1,
                npc_name="npc_dota_hero_lina",
                team=2,
                x=30.0,
                y=40.0,
            ),
            SimpleNamespace(
                tick=500,
                player_id=1,
                npc_name="npc_dota_hero_lina",
                team=2,
                x=50.0,
                y=60.0,
            ),
        ]
        ext = SmokeExtractor(_fake_player_ext(snapshots=snapshots))
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(tick=100, log_type="ITEM", inflictor_name="item_smoke_of_deceit"))
        parser.fire(
            _entry(
                tick=102,
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_lina",
                modifier_duration_s=45.0,
            )
        )
        parser.fire(
            _entry(
                tick=500,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_smoke_of_deceit",
                target_name="npc_dota_hero_lina",
            )
        )

        event = ext.finalize()[0]
        participant = event.participants[0]
        assert event.activation_x == 10.0
        assert event.activation_y == 20.0
        assert event.x == 30.0
        assert event.y == 40.0
        assert participant.player_id == 1
        assert (participant.applied_x, participant.applied_y) == (30.0, 40.0)
        assert (participant.removed_x, participant.removed_y) == (50.0, 60.0)
