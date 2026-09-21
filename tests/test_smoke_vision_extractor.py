"""Unit tests for gem.extractors.smoke_vision.

Covers SmokeExtractor and VisionModifierExtractor — the attach()/finalize()
contract, team/centroid back-fill, evidence-aware vision-modifier pairing, and
the documented empty-group smoke edge case. All tests use fake combat log
entries — no real .dem files.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from gem.combat.log import CombatLogEntry, CombatLogSource
from gem.extractors.smoke_vision import (
    SmokeExtractor,
    VisionModifierExtractor,
)
from gem.results.models import (
    VisionModifierCloseEvidence,
    VisionModifierLifecycleStatus,
    VisionModifierPairingStatus,
    VisionModifierSemantic,
    VisionModifierTeamSource,
)

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
        "attacker_is_hero_present": True,
        "target_is_hero_present": True,
        "attacker_is_illusion_present": True,
        "target_is_illusion_present": True,
        "ability_level": 0,
        "gold_reason": 0,
        "xp_reason": 0,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


class FakeParser:
    def __init__(
        self,
        *,
        duration_s: int | None = None,
        combat_log_time_s: int | None = None,
    ) -> None:
        self._handlers: list = []
        self.duration_s = duration_s
        self.combat_log_time_s = combat_log_time_s

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
        assert ev.caster_team_source is VisionModifierTeamSource.SNAPSHOT_FALLBACK
        assert ev.lifecycle_status is VisionModifierLifecycleStatus.REMOVED
        assert ev.close_evidence is VisionModifierCloseEvidence.OBSERVED
        assert ev.target_is_hero_present is True
        assert ev.remove_target_is_hero is True
        assert ev.remove_target_is_illusion is False

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

    def test_duplicate_adds_are_not_closed_by_lifo_guess(self):
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
        by_tick = {e.tick: e.end_tick for e in events}
        assert by_tick == {100: None, 120: None}
        assert all(e.lifecycle_status is VisionModifierLifecycleStatus.INCOMPLETE for e in events)
        assert all(e.pairing_status is VisionModifierPairingStatus.AMBIGUOUS for e in events)
        assert [issue.reason for issue in ext.pairing_issues] == ["ambiguous", "ambiguous"]
        assert ext.pairing_issues[0].candidate_add_ticks == [100, 120]

    def test_exact_caster_match_disambiguates_candidates(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_bounty_hunter_track",
            "target_name": "npc_dota_hero_riki",
        }
        parser.fire(_entry(tick=100, attacker_name="npc_dota_hero_bounty_hunter", **common))
        parser.fire(_entry(tick=110, attacker_name="npc_dota_hero_rubick", **common))
        parser.fire(
            _entry(
                tick=200,
                log_type="MODIFIER_REMOVE",
                attacker_name="npc_dota_hero_rubick",
                **common,
            )
        )

        events = ext.finalize()

        assert events[0].end_tick is None
        assert events[1].end_tick == 200
        assert events[1].pairing_status is VisionModifierPairingStatus.EXACT
        assert ext.pairing_issues == []

    def test_elapsed_duration_disambiguates_same_caster(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_slardar_amplify_damage",
            "target_name": "npc_dota_hero_riki",
            "attacker_name": "npc_dota_hero_slardar",
        }
        parser.fire(_entry(tick=100, game_time_s=10, **common))
        parser.fire(_entry(tick=110, game_time_s=20, **common))
        parser.fire(
            _entry(
                tick=200,
                game_time_s=30,
                modifier_elapsed_duration_s=10.0,
                log_type="MODIFIER_REMOVE",
                **common,
            )
        )

        events = ext.finalize()

        assert events[0].end_tick is None
        assert events[1].end_tick == 200
        assert events[1].pairing_status is VisionModifierPairingStatus.EXACT

    def test_later_exact_removal_resolves_earlier_ambiguity(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_slardar_amplify_damage",
            "target_name": "npc_dota_hero_riki",
            "attacker_name": "npc_dota_hero_slardar",
        }
        parser.fire(_entry(tick=100, game_time_s=0, **common))
        parser.fire(_entry(tick=200, game_time_s=10, **common))
        parser.fire(_entry(tick=300, game_time_s=15, log_type="MODIFIER_REMOVE", **common))
        parser.fire(
            _entry(
                tick=400,
                game_time_s=20,
                modifier_elapsed_duration_s=10.0,
                log_type="MODIFIER_REMOVE",
                **common,
            )
        )

        events = ext.finalize()

        assert [event.end_tick for event in events] == [300, 400]
        assert ext.pairing_issues == []

    def test_intended_duration_does_not_disambiguate_early_purge(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_slardar_amplify_damage",
            "target_name": "npc_dota_hero_riki",
            "attacker_name": "npc_dota_hero_slardar",
            "modifier_duration_s": 20.0,
        }
        parser.fire(_entry(tick=100, game_time_s=0, **common))
        parser.fire(_entry(tick=200, game_time_s=15, **common))
        parser.fire(
            _entry(
                tick=300,
                game_time_s=20,
                log_type="MODIFIER_REMOVE",
                modifier_purged=True,
                **common,
            )
        )

        events = ext.finalize()

        assert all(event.end_tick is None for event in events)
        assert all(
            event.pairing_status is VisionModifierPairingStatus.AMBIGUOUS for event in events
        )
        assert ext.pairing_issues[0].reason == "ambiguous"

    def test_contradictory_caster_is_not_unique_fallback(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_slardar_amplify_damage",
            "target_name": "npc_dota_hero_riki",
        }
        parser.fire(_entry(attacker_name="npc_dota_hero_slardar", **common))
        parser.fire(
            _entry(
                tick=200,
                log_type="MODIFIER_REMOVE",
                attacker_name="npc_dota_hero_rubick",
                **common,
            )
        )

        event = ext.finalize()[0]

        assert event.end_tick is None
        assert event.pairing_status is VisionModifierPairingStatus.UNMATCHED
        assert ext.pairing_issues[0].reason == "unmatched"
        assert ext.pairing_issues[0].candidate_add_ticks == []

    def test_unnamed_caster_remains_compatible_with_named_removal(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_slardar_amplify_damage",
            "target_name": "npc_dota_hero_riki",
        }
        parser.fire(_entry(tick=100, attacker_name="", **common))
        parser.fire(_entry(tick=110, attacker_name="npc_dota_hero_slardar", **common))
        parser.fire(
            _entry(
                tick=200,
                log_type="MODIFIER_REMOVE",
                attacker_name="npc_dota_hero_slardar",
                **common,
            )
        )

        events = ext.finalize()

        assert all(event.end_tick is None for event in events)
        assert all(
            event.pairing_status is VisionModifierPairingStatus.AMBIGUOUS for event in events
        )
        assert ext.pairing_issues[0].candidate_add_ticks == [100, 110]

    def test_sole_unnamed_caster_is_unique_fallback_for_named_removal(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_bounty_hunter_track",
            "target_name": "npc_dota_hero_riki",
        }
        parser.fire(_entry(tick=100, attacker_name="", **common))
        parser.fire(
            _entry(
                tick=200,
                log_type="MODIFIER_REMOVE",
                attacker_name="npc_dota_hero_bounty_hunter",
                **common,
            )
        )

        event = ext.finalize()[0]

        assert event.end_tick == 200
        assert event.pairing_status is VisionModifierPairingStatus.UNIQUE_FALLBACK
        assert event.lifecycle_status is VisionModifierLifecycleStatus.INCOMPLETE
        assert ext.pairing_issues == []

    def test_contradictory_illusion_flag_does_not_close_real_target(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_item_dustofappearance",
            "target_name": "npc_dota_hero_riki",
        }
        parser.fire(_entry(target_is_illusion=False, **common))
        parser.fire(
            _entry(
                tick=200,
                log_type="MODIFIER_REMOVE",
                target_is_illusion=True,
                **common,
            )
        )

        event = ext.finalize()[0]

        assert event.end_tick is None
        assert ext.pairing_issues[0].reason == "unmatched"
        assert ext.pairing_issues[0].target_is_illusion is True

    def test_out_of_order_ticks_are_resolved_before_pairing(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {"inflictor_name": "modifier_bounty_hunter_track"}
        parser.fire(_entry(tick=200, log_type="MODIFIER_REMOVE", **common))
        parser.fire(_entry(tick=100, log_type="MODIFIER_ADD", **common))

        event = ext.finalize()[0]

        assert event.end_tick == 200
        assert ext.pairing_issues == []

    def test_same_tick_timestamp_orders_remove_before_ingested_add(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {"tick": 100, "inflictor_name": "modifier_bounty_hunter_track"}
        parser.fire(_entry(log_type="MODIFIER_REMOVE", timestamp_s=20.0, **common))
        parser.fire(_entry(log_type="MODIFIER_ADD", timestamp_s=10.0, **common))

        event = ext.finalize()[0]

        assert event.end_tick == 100
        assert ext.pairing_issues == []

    def test_repeated_same_tick_pairs_follow_ingestion_order(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {"tick": 100, "inflictor_name": "modifier_bounty_hunter_track"}
        for log_type in (
            "MODIFIER_ADD",
            "MODIFIER_REMOVE",
            "MODIFIER_ADD",
            "MODIFIER_REMOVE",
        ):
            parser.fire(_entry(log_type=log_type, **common))

        events = ext.finalize()

        assert [event.end_tick for event in events] == [100, 100]
        assert ext.pairing_issues == []

    def test_duplicate_same_tick_adds_and_removes_stay_ambiguous(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {"tick": 100, "inflictor_name": "modifier_item_dustofappearance"}
        parser.fire(_entry(log_type="MODIFIER_ADD", **common))
        parser.fire(_entry(log_type="MODIFIER_ADD", **common))
        parser.fire(_entry(log_type="MODIFIER_REMOVE", **common))
        parser.fire(_entry(log_type="MODIFIER_REMOVE", **common))

        events = ext.finalize()

        assert len(events) == 2
        assert all(event.end_tick is None for event in events)
        assert [issue.reason for issue in ext.pairing_issues] == ["ambiguous", "ambiguous"]

    def test_unmatched_removal_is_preserved_without_fake_application(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(
            _entry(
                tick=200,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_slardar_amplify_damage",
                source=CombatLogSource.S2_BULK,
                modifier_elapsed_duration_s=5.0,
                attacker_team=2,
                target_team=3,
            )
        )

        assert ext.finalize() == []
        assert len(ext.pairing_issues) == 1
        issue = ext.pairing_issues[0]
        assert issue.reason == "unmatched"
        assert issue.source is CombatLogSource.S2_BULK
        assert issue.modifier_elapsed_duration_s == 5.0
        assert issue.candidate_add_ticks == []

    def test_protocol_teams_take_precedence_and_nonhero_is_retained(self):
        ext = VisionModifierExtractor(
            _fake_player_ext(
                teams={
                    "npc_dota_hero_slardar": 3,
                    "npc_dota_neutral_centaur_khan": 2,
                }
            )
        )
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(
            _entry(
                inflictor_name="modifier_slardar_amplify_damage",
                attacker_name="npc_dota_hero_slardar",
                target_name="npc_dota_neutral_centaur_khan",
                target_is_hero=False,
                attacker_is_hero=False,
                attacker_is_illusion=True,
                target_is_illusion=True,
                attacker_team=2,
                target_team=3,
            )
        )

        event = ext.finalize()[0]

        assert event.target_is_hero is False
        assert event.caster_is_hero is False
        assert event.caster_is_illusion is True
        assert event.target_is_illusion is True
        assert event.caster_team == 2
        assert event.target_team == 3
        assert event.caster_team_source is VisionModifierTeamSource.PROTOCOL
        assert event.target_team_source is VisionModifierTeamSource.PROTOCOL

    def test_conflicting_snapshot_teams_are_not_used_as_fallback(self):
        caster = "npc_dota_hero_slardar"
        snapshots = [
            SimpleNamespace(
                tick=100,
                player_id=0,
                npc_name=caster,
                team=2,
                x=None,
                y=None,
            ),
            SimpleNamespace(
                tick=200,
                player_id=1,
                npc_name=caster,
                team=3,
                x=None,
                y=None,
            ),
        ]
        ext = VisionModifierExtractor(_fake_player_ext(snapshots=snapshots))
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(
            _entry(
                inflictor_name="modifier_slardar_amplify_damage",
                attacker_name=caster,
            )
        )

        event = ext.finalize()[0]

        assert event.caster_team == 0
        assert event.caster_team_source is VisionModifierTeamSource.UNKNOWN
        assert "caster_team_ambiguous" in event.evidence_gaps

    def test_gem_carrier_has_non_direct_semantic(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(inflictor_name="modifier_item_gem_of_true_sight"))

        event = ext.finalize()[0]

        assert event.semantic is VisionModifierSemantic.AURA_CARRIER

    def test_observed_expiry_and_duration_inferred_expiry_remain_distinct(self):
        observed = VisionModifierExtractor(_fake_player_ext())
        observed_parser = FakeParser()
        observed.attach(observed_parser)
        common = {
            "inflictor_name": "modifier_slardar_amplify_damage",
            "modifier_duration_s": 10.0,
        }
        observed_parser.fire(_entry(tick=100, game_time_s=5, **common))
        observed_parser.fire(
            _entry(
                tick=400,
                game_time_s=15,
                modifier_elapsed_duration_s=10.0,
                log_type="MODIFIER_REMOVE",
                **common,
            )
        )
        observed_event = observed.finalize()[0]

        inferred = VisionModifierExtractor(_fake_player_ext())
        inferred_parser = FakeParser(duration_s=30)
        inferred.attach(inferred_parser)
        inferred_parser.fire(_entry(tick=100, game_time_s=5, **common))
        inferred_event = inferred.finalize()[0]

        assert observed_event.lifecycle_status is VisionModifierLifecycleStatus.EXPIRED
        assert observed_event.close_evidence is VisionModifierCloseEvidence.OBSERVED
        assert observed_event.end_tick == 400
        assert inferred_event.lifecycle_status is VisionModifierLifecycleStatus.EXPIRED
        assert inferred_event.close_evidence is VisionModifierCloseEvidence.DURATION_INFERRED
        assert inferred_event.end_tick is None

    def test_explicit_zero_remove_duration_does_not_fall_back_to_add_duration(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {"inflictor_name": "modifier_slardar_amplify_damage"}
        parser.fire(_entry(tick=100, game_time_s=5, modifier_duration_s=10.0, **common))
        parser.fire(
            _entry(
                tick=400,
                game_time_s=15,
                modifier_duration_s=0.0,
                modifier_elapsed_duration_s=10.0,
                log_type="MODIFIER_REMOVE",
                **common,
            )
        )

        event = ext.finalize()[0]

        assert event.remove_modifier_duration_s == 0.0
        assert event.lifecycle_status is VisionModifierLifecycleStatus.REMOVED

    def test_matched_removal_with_missing_identity_keeps_incomplete_status(self):
        ext = VisionModifierExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        common = {
            "inflictor_name": "modifier_bounty_hunter_track",
            "target_name": "npc_dota_hero_riki",
            "attacker_name": "",
        }
        parser.fire(_entry(tick=100, **common))
        parser.fire(_entry(tick=200, log_type="MODIFIER_REMOVE", **common))

        event = ext.finalize()[0]

        assert event.end_tick == 200
        assert event.close_evidence is VisionModifierCloseEvidence.OBSERVED
        assert event.lifecycle_status is VisionModifierLifecycleStatus.INCOMPLETE
        assert "missing_caster_name" in event.evidence_gaps


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

    def test_pause_aware_game_time_accepts_remove_beyond_raw_tick_deadline(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(tick=100, log_type="ITEM", inflictor_name="item_smoke_of_deceit"))
        parser.fire(
            _entry(
                tick=101,
                game_time_s=10,
                inflictor_name="modifier_smoke_of_deceit",
                modifier_duration_s=1.0,
            )
        )
        # Raw ticks advanced far beyond the 1s duration + 2s grace while the
        # pause-aware game clock advanced by only one second.
        parser.fire(
            _entry(
                tick=500,
                game_time_s=11,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_smoke_of_deceit",
            )
        )

        assert ext.finalize()[0].participants[0].removed_tick == 500

    def test_parser_game_clock_is_pause_aware_fallback_for_source_one(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        parser.game_time_s = 10
        ext.attach(parser)
        parser.fire(_entry(tick=100, log_type="ITEM", inflictor_name="item_smoke_of_deceit"))
        parser.fire(
            _entry(
                tick=101,
                inflictor_name="modifier_smoke_of_deceit",
                modifier_duration_s=1.0,
            )
        )
        parser.game_time_s = 11
        parser.fire(
            _entry(
                tick=500,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_smoke_of_deceit",
            )
        )

        assert ext.finalize()[0].participants[0].removed_tick == 500

    def test_pause_aware_clock_rejects_stale_remove_despite_elapsed_metadata(self):
        ext = SmokeExtractor(_fake_player_ext())
        parser = FakeParser()
        ext.attach(parser)
        parser.fire(_entry(tick=100, log_type="ITEM", inflictor_name="item_smoke_of_deceit"))
        parser.fire(
            _entry(
                tick=101,
                game_time_s=10,
                inflictor_name="modifier_smoke_of_deceit",
                modifier_duration_s=1.0,
            )
        )
        parser.fire(
            _entry(
                tick=500,
                game_time_s=20,
                log_type="MODIFIER_REMOVE",
                inflictor_name="modifier_smoke_of_deceit",
                modifier_elapsed_duration_s=0.5,
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
