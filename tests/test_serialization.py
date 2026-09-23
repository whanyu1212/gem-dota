"""Tests for gem serialization helpers."""

from __future__ import annotations

import json
from collections import defaultdict

import gem
import gem.api
from gem.analysis.farming import build_farming_routes
from gem.analysis.roshan import build_rosh_conversions
from gem.analysis.smoke_fight import build_smoke_fight_insights
from gem.analysis.teamfight_positioning import build_teamfight_positioning
from gem.combat.log import CombatLogSource
from gem.extractors.objectives import AegisEvent, RoshanKill
from gem.extractors.teamfights import OpenDotaTeamfight, Teamfight, TeamfightPlayer
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisionModifierEvent,
    VisionModifierPairingIssue,
    VisionModifierSemantic,
)


class TestSerializationHelpers:
    def test_to_dict_converts_defaultdict_and_tuples(self):
        pp = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            times=[30],
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

    def test_to_json_returns_valid_json(self):
        match = ParsedMatch(match_id=7)
        payload = gem.to_json(match, sort_keys=True)

        decoded = json.loads(payload)
        assert decoded["match_id"] == 7
        assert "players" in decoded

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
