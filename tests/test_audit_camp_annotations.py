from __future__ import annotations

from pathlib import Path

from gem.combatlog import CombatLogEntry
from gem.models import ParsedMatch, ParsedPlayer
from scripts.audit_camp_annotations import (
    CampZone,
    audit_match,
    collect_neutral_observations,
    load_camp_zones,
    nearest_position,
    point_in_zone,
    summarize_camps,
)


def test_load_camp_zones_reads_ellipse_zones(tmp_path: Path) -> None:
    zones_path = tmp_path / "camp_zones.json"
    zones_path.write_text(
        """
        {
          "camps": [
            {
              "id": 7,
              "type": "small",
              "center": {"x": 100, "y": 200},
              "zone": {"shape": "ellipse", "rx": 50, "ry": 25, "rotation_deg": 0}
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    zones = load_camp_zones(zones_path)

    assert zones == (
        CampZone(id=7, type="small", x=100.0, y=200.0, shape="ellipse", rx=50.0, ry=25.0),
    )


def test_point_in_zone_supports_rotated_ellipse() -> None:
    zone = CampZone(
        id=1,
        type="large",
        x=100.0,
        y=100.0,
        shape="ellipse",
        rx=80.0,
        ry=20.0,
        rotation_deg=90.0,
    )

    assert point_in_zone(zone, 100.0, 160.0)
    assert not point_in_zone(zone, 160.0, 100.0)


def test_nearest_position_returns_closest_sample_within_window() -> None:
    samples = [(90, 9.0, 9.0), (110, 11.0, 11.0), (200, 20.0, 20.0)]

    assert nearest_position(samples, tick=104, max_delta_ticks=10) == (110, 11.0, 11.0)
    assert nearest_position(samples, tick=150, max_delta_ticks=10) is None


def test_collect_neutral_observations_assigns_deaths_to_camp_and_nearby_gold() -> None:
    player = ParsedPlayer(
        player_id=0,
        hero_name="npc_dota_hero_axe",
        position_log=[(95, 98.0, 101.0), (105, 102.0, 99.0)],
    )
    match = ParsedMatch(
        match_id=123,
        players=[player],
        combat_log=[
            CombatLogEntry(
                tick=100,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_neutral_ancient_frog",
                neutral_camp_type=4,
                neutral_camp_team=2,
            ),
            CombatLogEntry(
                tick=101,
                log_type="GOLD",
                attacker_name="npc_dota_hero_axe",
                value=88,
                gold_reason=6,
            ),
            CombatLogEntry(
                tick=130,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_crystal_maiden",
            ),
        ],
    )
    zones = (CampZone(id=1, type="large", x=100.0, y=100.0, shape="ellipse", rx=200.0, ry=200.0),)

    observations = collect_neutral_observations(match, zones, max_position_delta_ticks=30)

    assert len(observations) == 1
    assert observations[0].match_id == 123
    assert observations[0].camp_id == 1
    assert observations[0].annotated_type == "large"
    assert observations[0].neutral_name == "npc_dota_neutral_ancient_frog"
    assert observations[0].nearby_gold == 88
    assert observations[0].unit_type_hint == "ancient"
    assert observations[0].neutral_camp_type == 4
    assert observations[0].neutral_camp_team == 2
    assert observations[0].position_source == "hero_position"


def test_collect_neutral_observations_prefers_combat_log_location() -> None:
    player = ParsedPlayer(
        player_id=0,
        hero_name="npc_dota_hero_axe",
        position_log=[(100, 100.0, 100.0)],
    )
    match = ParsedMatch(
        match_id=123,
        players=[player],
        combat_log=[
            CombatLogEntry(
                tick=100,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_neutral_ancient_frog",
                location_x=500.0,
                location_y=500.0,
            ),
        ],
    )
    zones = (
        CampZone(id=1, type="large", x=100.0, y=100.0, shape="ellipse", rx=100.0, ry=100.0),
        CampZone(id=2, type="ancient", x=500.0, y=500.0, shape="ellipse", rx=100.0, ry=100.0),
    )

    observations = collect_neutral_observations(match, zones, max_position_delta_ticks=30)

    assert observations[0].camp_id == 2
    assert observations[0].position_source == "combat_log"


def test_summarize_camps_flags_inferred_type_mismatch() -> None:
    player = ParsedPlayer(
        player_id=0,
        hero_name="npc_dota_hero_axe",
        position_log=[(100, 100.0, 100.0), (130, 100.0, 100.0)],
    )
    match = ParsedMatch(
        match_id=123,
        players=[player],
        combat_log=[
            CombatLogEntry(
                tick=100,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_neutral_ancient_frog",
            ),
            CombatLogEntry(
                tick=130,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_neutral_ancient_frog_mage",
            ),
        ],
    )
    zones = (CampZone(id=1, type="large", x=100.0, y=100.0, shape="ellipse", rx=200.0, ry=200.0),)

    report = audit_match(match, zones, max_position_delta_ticks=30)
    summaries = summarize_camps(zones, report.observations)

    assert summaries[0].suggested_type == "ancient"
    assert summaries[0].status == "mismatch"
    assert summaries[0].observed_deaths == 2
    assert summaries[0].neutral_counts == {
        "npc_dota_neutral_ancient_frog": 1,
        "npc_dota_neutral_ancient_frog_mage": 1,
    }
