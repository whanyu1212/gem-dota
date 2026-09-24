"""Tests for gem serialization helpers."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import fields

import pytest

import gem
import gem.api
from gem.analysis.farming import build_farming_routes
from gem.analysis.roshan import build_rosh_conversions
from gem.analysis.smoke_fight import build_smoke_fight_insights
from gem.analysis.teamfight_positioning import build_teamfight_positioning
from gem.combat.log import CombatLogEntry, CombatLogSource, CombatLogType
from gem.extractors.objectives import AegisEvent, RoshanKill
from gem.extractors.teamfights import OpenDotaTeamfight, Teamfight, TeamfightPlayer
from gem.results.models import (
    EntityVisibilityEvent,
    HeroVisibilityEvent,
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisibilityState,
    VisionModifierEvent,
    VisionModifierPairingIssue,
    VisionModifierSemantic,
)
from gem.results.serialization import SCHEMA_VERSION
from gem.state.game_clock import GameClock, GamePause


class TestSerializationHelpers:
    def test_to_dict_converts_defaultdict_and_tuples(self):
        pp = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            times=[30],
            total_earned_xp_t=[725],
            position_log=[(30, 100.5, -50.25)],
        )
        pp.lane_pos = defaultdict(int, {"100_200": 3})

        match = ParsedMatch(
            match_id=42,
            players=[pp] + [ParsedPlayer(player_id=i) for i in range(1, 10)],
        )

        data = gem.to_dict(match)

        assert isinstance(data, dict)
        assert data["match_id"] == 42
        assert isinstance(data["players"][0]["lane_pos"], dict)
        assert data["players"][0]["lane_pos"]["100_200"] == 3
        assert isinstance(data["players"][0]["position_log"], list)
        assert data["players"][0]["position_log"][0] == [30, 100.5, -50.25]
        assert data["players"][0]["total_earned_xp_t"] == [725]

    def test_to_json_returns_valid_json(self):
        match = ParsedMatch(match_id=7)
        payload = gem.to_json(match, sort_keys=True)

        decoded = json.loads(payload)
        assert decoded["match_id"] == 7
        assert "players" in decoded
        assert decoded["schema_version"] == SCHEMA_VERSION
        assert isinstance(decoded["gem_version"], str)
        assert "analysis" not in decoded

    def test_farming_routes_serialize_enum_and_missing_evidence_values(self):
        player = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            position_log=[(0, 8647.0, 15564.0), (30, 8650.0, 15564.0)],
        )

        decoded = json.loads(
            json.dumps(gem.to_dict(build_farming_routes(ParsedMatch(players=[player]))))
        )
        segment = decoded[0]["segments"][0]

        assert segment["start_reason"] == "zone_entry"
        assert segment["end_reason"] == "log_end"
        assert segment["evidence_strength"] == "transit_like"
        assert segment["window_xp_delta"] is None
        assert segment["camp_owner_team"] == 2
        assert segment["camp_catalog_version"] == 2
        assert segment["camp_map_patch"] == "7.40"
        assert segment["camp_topology_patch"] == "7.41"
        assert segment["context"]["camp_side"] == "own_side"
        assert "own_side" in segment["context"]["tags"]
        assert "incomplete_context" in segment["context"]["tags"]

    def test_positioning_analysis_preserves_enum_values_and_unknowns(self):
        players = [
            ParsedPlayer(
                player_id=0,
                hero_name="npc_dota_hero_axe",
                team=2,
                position_log=[(1_000, 100.0, 200.0)],
            ),
            ParsedPlayer(player_id=5, hero_name="npc_dota_hero_bane", team=3),
        ]
        fight_players = [TeamfightPlayer(player_id=i) for i in range(10)]
        match = ParsedMatch(
            players=players,
            teamfights=[
                Teamfight(
                    start_tick=550,
                    end_tick=1_450,
                    first_death_tick=1_000,
                    last_death_tick=1_000,
                    deaths=1,
                    players=fight_players,
                )
            ],
        )

        payload = gem.to_dict(build_teamfight_positioning(match))
        decoded = json.loads(json.dumps(payload))

        assert decoded[0]["engagement_start_source"] == "first_death_fallback"
        assert decoded[0]["snapshots"][0]["kind"] == "pre_engagement"
        heroes = decoded[0]["snapshots"][1]["heroes"]
        assert {hero["visibility"] for hero in heroes} == {"unknown"}
        bane = next(hero for hero in heroes if hero["player_id"] == 5)
        assert bane["x"] is None
        assert bane["sample_tick"] is None

    def test_to_dict_includes_opendota_teamfights(self):
        match = ParsedMatch(
            match_id=7,
            opendota_teamfights=[OpenDotaTeamfight(start=10, end=30, last_death=15, deaths=3)],
        )

        data = gem.to_dict(match)

        assert data["opendota_teamfights"][0]["start"] == 10
        assert data["opendota_teamfights"][0]["players"][0]["damage"] == 0

    def test_to_dict_preserves_nested_smoke_lifecycle_ticks(self):
        match = ParsedMatch(
            smoke_events=[
                SmokeEvent(
                    tick=1_000,
                    activator="npc_dota_hero_axe",
                    team=2,
                    activation_game_time_s=10,
                    participants=[
                        SmokeParticipant(
                            hero_name="npc_dota_hero_axe",
                            player_id=0,
                            applied_tick=1_002,
                            removed_tick=1_452,
                            modifier_duration_s=45.0,
                            modifier_elapsed_duration_s=15.0,
                            applied_game_time_s=11,
                            removed_game_time_s=26,
                        )
                    ],
                )
            ]
        )

        data = gem.to_dict(match)

        smoke = data["smoke_events"][0]
        assert smoke["tick"] == 1_000
        assert smoke["activation_game_time_s"] == 10
        assert smoke["participants"][0]["applied_tick"] == 1_002
        assert smoke["participants"][0]["removed_tick"] == 1_452
        assert smoke["participants"][0]["modifier_elapsed_duration_s"] == 15.0
        assert smoke["participants"][0]["applied_game_time_s"] == 11
        assert smoke["participants"][0]["removed_game_time_s"] == 26

    def test_to_dict_serializes_public_smoke_fight_records(self):
        match = ParsedMatch(
            players=[
                ParsedPlayer(
                    player_id=0,
                    hero_name="npc_dota_hero_axe",
                    team=2,
                )
            ],
            smoke_events=[
                SmokeEvent(
                    tick=1_000,
                    activator="npc_dota_hero_axe",
                    team=2,
                    activation_game_time_s=10,
                    participants=[
                        SmokeParticipant(
                            hero_name="npc_dota_hero_axe",
                            player_id=0,
                            applied_tick=1_001,
                        )
                    ],
                )
            ],
        )

        payload = gem.to_dict(build_smoke_fight_insights(match))
        decoded = json.loads(json.dumps(payload))

        assert decoded[0]["smoke_index"] == 0
        assert decoded[0]["fight_index"] is None
        assert decoded[0]["status"] == "no_candidate"
        assert decoded[0]["activation"]["tick"] == 1_000
        assert decoded[0]["activation"]["game_time_s"] == 10
        assert decoded[0]["members"][0]["authoritative_visibility"] == "unknown"

    def test_to_dict_serializes_roshan_provenance_and_nested_fight_evidence(self):
        players = [
            ParsedPlayer(
                player_id=player_id,
                hero_name=f"npc_dota_hero_hero_{player_id}",
                team=2 if player_id < 5 else 3,
            )
            for player_id in range(10)
        ]
        fight_players = [TeamfightPlayer(player_id=player_id) for player_id in range(10)]
        fight_players[0].damage_dealt = 250
        fight_players[5].deaths = 1
        match = ParsedMatch(
            game_start_tick=0,
            game_end_tick=20000,
            players=players,
            roshans=[
                RoshanKill(
                    1000,
                    "npc_dota_hero_hero_0",
                    1,
                    killer_team=2,
                )
            ],
            aegis_events=[AegisEvent(1010, 0, "pickup")],
            teamfights=[
                Teamfight(
                    start_tick=1100,
                    end_tick=1400,
                    first_death_tick=1300,
                    last_death_tick=1300,
                    deaths=1,
                    winner="radiant",
                    players=fight_players,
                )
            ],
        )

        decoded = json.loads(json.dumps(gem.to_dict(build_rosh_conversions(match))))
        conversion = decoded[0]

        assert conversion["roshan_team_source"] == "protocol"
        assert conversion["conversion_team_source"] == "player_id"
        assert conversion["aegis_fate_source"] == "nominal_expiry"
        assert conversion["fight_evidence"][0]["relation"] == "in_window"
        assert conversion["fight_evidence"][0]["engagement_start_source"] in {
            "first_damage",
            "first_death_fallback",
        }

    def test_to_dict_omits_internal_match_details_provenance(self):
        match = ParsedMatch(match_id=7)
        match._match_details_fields.add("duration")
        match.players[0]._match_details_fields.add("hero_damage")

        data = gem.to_dict(match)

        assert "_match_details_fields" not in data
        assert "_match_details_fields" not in data["players"][0]

    def test_to_dict_preserves_vision_lifecycle_and_pairing_evidence(self):
        match = ParsedMatch(
            vision_modifiers=[
                VisionModifierEvent(
                    10,
                    20,
                    "modifier_slardar_amplify_damage",
                    "npc_dota_hero_riki",
                    "npc_dota_hero_slardar",
                    2,
                    semantic=VisionModifierSemantic.DIRECT_TARGET_REVEAL,
                    add_source=CombatLogSource.S2_DIRECT,
                )
            ],
            vision_modifier_pairing_issues=[
                VisionModifierPairingIssue(
                    tick=30,
                    reason="unmatched",
                    modifier_name="modifier_bounty_hunter_track",
                    caster_name="",
                    target_name="npc_dota_hero_riki",
                    source=CombatLogSource.S2_BULK,
                )
            ],
        )

        data = gem.to_dict(match)

        assert data["vision_modifiers"][0]["semantic"] == "direct_target_reveal"
        assert data["vision_modifiers"][0]["add_source"] == "s2_direct"
        assert data["vision_modifier_pairing_issues"][0]["reason"] == "unmatched"
        assert data["vision_modifier_pairing_issues"][0]["source"] == "s2_bulk"

    def test_to_dict_preserves_permanent_buff_availability(self):
        match = ParsedMatch()
        match.players[0].aghanims_scepter = 1
        match.players[0].aghanims_shard = 0

        data = gem.to_dict(match)

        assert data["players"][0]["aghanims_scepter"] == 1
        assert data["players"][0]["aghanims_shard"] == 0
        assert data["players"][0]["moonshard"] is None

    def test_parse_to_json_uses_parse_result(self, monkeypatch):
        fake_match = ParsedMatch(match_id=999)

        monkeypatch.setattr(gem.api, "parse", lambda path: fake_match)

        payload = gem.parse_to_json("dummy.dem")
        decoded = json.loads(payload)

        assert decoded["match_id"] == 999


def _awkward_match() -> ParsedMatch:
    """A match populating every type the JSON decoder has to restore."""
    player = ParsedPlayer(
        player_id=0,
        hero_name="npc_dota_hero_axe",
        team=2,
        times=[30, 60],
        gold_t=[500, 650],
        position_log=[(30, 100.5, -50.25), (60, 101.0, -49.0)],
        final_items={0: "item_blink", 5: "item_black_king_bar"},
        kills_log=[CombatLogEntry(tick=40, log_type=CombatLogType.DEATH)],
        damage_targets={"axe_counter_helix": {"npc_dota_hero_lina": 600}},
        max_hero_hit={"inflictor": "axe_culling_blade", "key": "x", "value": 700, "time": 912},
        _ability_snapshots=[(27_516, {"axe_berserkers_call": 1})],
    )
    player.lane_pos = defaultdict(int, {"64_64": 3})
    return ParsedMatch(
        match_id=8822520406,
        players=[player] + [ParsedPlayer(player_id=i) for i in range(1, 10)],
        combat_log=[
            CombatLogEntry(
                tick=10,
                log_type=CombatLogType.DAMAGE,
                value=5,
                source=CombatLogSource.S2_BULK,
            )
        ],
        objectives=[{"type": "building_kill", "time": 600, "key": "npc_dota_badguys_tower1_mid"}],
        hero_visibility_events=[
            HeroVisibilityEvent(
                tick=100,
                player_id=0,
                hero_name="npc_dota_hero_axe",
                entity_index=5,
                entity_serial=1,
                radiant_state=VisibilityState.VISIBLE,
                dire_state=VisibilityState.HIDDEN,
            )
        ],
        entity_visibility_events=[
            EntityVisibilityEvent(
                tick=120,
                entity_index=300,
                entity_serial=2,
                class_name="CDOTA_BaseNPC_Creep_Neutral",
                npc_name="npc_dota_neutral_kobold",
                team=None,
                active=True,
                radiant_state=VisibilityState.VISIBLE,
                dire_state=VisibilityState.UNKNOWN,
            )
        ],
        teamfights=[
            Teamfight(
                start_tick=1,
                end_tick=2,
                first_death_tick=1,
                last_death_tick=1,
                deaths=1,
                players=[TeamfightPlayer(player_id=0, item_uses={"item_blink": 1})],
            )
        ],
        game_clock=GameClock(
            game_start_tick=30_206,
            pauses=[GamePause(start_tick=31_143, end_tick=33_920), GamePause(40_000, None)],
            game_start_time_s=1019.3,
            net_tick_offset=374,
        ),
    )


class TestJsonRoundTrip:
    def test_from_dict_restores_every_field_type(self):
        match = _awkward_match()

        loaded = gem.from_dict(json.loads(gem.to_json(match)))

        assert loaded == match
        player = loaded.players[0]
        assert player.position_log[0] == (30, 100.5, -50.25)
        assert isinstance(player.position_log[0], tuple)
        assert isinstance(player._ability_snapshots[0], tuple)
        assert player.final_items == {0: "item_blink", 5: "item_black_king_bar"}
        assert isinstance(player.lane_pos, defaultdict)
        assert player.lane_pos.default_factory is int
        player.lane_pos["128_128"] += 1  # unseen cells still start at zero
        assert player.lane_pos["128_128"] == 1
        assert player.kills_log[0].log_type is CombatLogType.DEATH
        assert loaded.combat_log[0].source is CombatLogSource.S2_BULK
        assert loaded.hero_visibility_events[0].dire_state is VisibilityState.HIDDEN
        assert loaded.game_clock is not None
        assert loaded.game_clock.pauses[1] == GamePause(40_000, None)
        assert loaded.teamfights[0].players[0].item_uses == {"item_blink": 1}

    def test_from_dict_accepts_bare_to_dict_payload(self):
        match = _awkward_match()

        assert gem.from_dict(json.loads(json.dumps(gem.to_dict(match)))) == match

    def test_from_dict_ignores_unknown_keys_and_defaults_missing_ones(self):
        data = {"match_id": 7, "field_from_a_future_version": [1, 2]}

        loaded = gem.from_dict(data)

        assert loaded.match_id == 7
        assert loaded.combat_log == []

    def test_from_dict_rejects_newer_schema_version(self):
        with pytest.raises(ValueError, match="newer gem"):
            gem.from_dict({"schema_version": SCHEMA_VERSION + 1, "match_id": 7})

    def test_load_json_reads_file(self, tmp_path):
        match = _awkward_match()
        path = tmp_path / "match.json"
        path.write_text(gem.to_json(match), encoding="utf-8")

        assert gem.load_json(path) == match

    def test_analysis_section_is_embedded_on_request_and_ignored_on_load(self):
        match = _awkward_match()

        decoded = json.loads(gem.to_json(match, analysis=gem.analyze(match)))

        assert set(decoded["analysis"]) == {
            "smoke",
            "smoke_fights",
            "roshan_conversions",
            "farming_routes",
            "teamfight_positioning",
        }
        assert gem.from_dict(decoded) == match

    def test_to_json_rejects_nan(self):
        match = ParsedMatch()
        match.players[0].lane_efficiency_pct = float("nan")

        with pytest.raises(ValueError):
            gem.to_json(match)

    def test_metadata_keys_do_not_collide_with_match_fields(self):
        names = {f.name for f in fields(ParsedMatch)}

        assert not names & {"schema_version", "gem_version", "analysis"}

    def test_parse_to_json_embeds_analysis_when_requested(self, monkeypatch):
        monkeypatch.setattr(gem.api, "parse", lambda path: ParsedMatch(match_id=999))

        decoded = json.loads(gem.parse_to_json("dummy.dem", analyze=True))

        assert decoded["match_id"] == 999
        assert decoded["analysis"]["smoke"] == []


class TestAnalyze:
    def test_analyze_matches_individual_builders(self):
        players = [
            ParsedPlayer(
                player_id=player_id,
                hero_name=f"npc_dota_hero_hero_{player_id}",
                team=2 if player_id < 5 else 3,
                position_log=[(1_000, 100.0 * player_id, 200.0)],
            )
            for player_id in range(10)
        ]
        match = ParsedMatch(
            game_start_tick=0,
            game_end_tick=20_000,
            players=players,
            roshans=[RoshanKill(1000, "npc_dota_hero_hero_0", 1, killer_team=2)],
            aegis_events=[AegisEvent(1010, 0, "pickup")],
            teamfights=[
                Teamfight(
                    start_tick=1_100,
                    end_tick=1_400,
                    first_death_tick=1_300,
                    last_death_tick=1_300,
                    deaths=1,
                    players=[TeamfightPlayer(player_id=i) for i in range(10)],
                )
            ],
        )

        analysis = gem.analyze(match)

        assert isinstance(analysis, gem.MatchAnalysis)
        assert gem.to_dict(analysis.roshan_conversions) == gem.to_dict(
            build_rosh_conversions(match)
        )
        assert gem.to_dict(analysis.teamfight_positioning) == gem.to_dict(
            build_teamfight_positioning(match)
        )
        assert gem.to_dict(analysis.farming_routes) == gem.to_dict(build_farming_routes(match))
        assert gem.to_dict(analysis.smoke_fights) == gem.to_dict(build_smoke_fight_insights(match))
        assert gem.to_dict(analysis.smoke) == gem.to_dict(gem.build_smoke_analysis(match))


@pytest.mark.integration
@pytest.mark.slow
def test_full_replay_json_round_trip(canonical_parsed_match, tmp_path):
    path = tmp_path / "match.json"
    path.write_text(gem.to_json(canonical_parsed_match), encoding="utf-8")

    loaded = gem.load_json(path)

    assert loaded == canonical_parsed_match
    assert gem.to_dict(gem.analyze(loaded)) == gem.to_dict(gem.analyze(canonical_parsed_match))
