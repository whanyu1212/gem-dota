"""Unit tests for local OpenDota validator helpers."""

from types import SimpleNamespace

import gem
from gem.combat.log import CombatLogEntry
from scripts.validate_opendota import (
    _compare_opendota_player_array,
    _opendota_teamfights_from_combat_log,
    validate_match,
)


def _death(game_time_s: int, *, target_is_illusion: bool = False) -> CombatLogEntry:
    return CombatLogEntry(
        tick=999999,
        game_time_s=game_time_s,
        log_type="DEATH",
        target_name="npc_dota_hero_axe",
        target_is_hero=True,
        target_is_illusion=target_is_illusion,
    )


def test_opendota_teamfight_projection_uses_combat_log_game_time() -> None:
    fights = _opendota_teamfights_from_combat_log(
        [
            _death(1033),
            _death(1038),
            _death(1040),
        ]
    )

    assert fights == [{"start": 1018, "end": 1055, "last_death": 1040, "deaths": 3}]


def test_opendota_teamfight_projection_filters_short_and_illusion_windows() -> None:
    fights = _opendota_teamfights_from_combat_log(
        [
            _death(100),
            _death(105),
            _death(106, target_is_illusion=True),
            _death(200),
            _death(204),
            _death(208),
        ]
    )

    assert fights == [{"start": 185, "end": 223, "last_death": 208, "deaths": 3}]


def test_player_curve_comparison_passes_within_percent_tolerance() -> None:
    fields = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "gold_t",
        [0, 100, 190],
        [0, 100, 200],
        max_curve_error_pct=10.0,
    )

    assert [field.name for field in fields] == [
        "npc_dota_hero_axe/gold_t/length",
        "npc_dota_hero_axe/gold_t/minute_keys",
        "npc_dota_hero_axe/gold_t/final",
        "npc_dota_hero_axe/gold_t/max_curve_err%",
    ]
    assert all(field.ok for field in fields)
    assert fields[-1].gem_value == 5.0


def test_player_curve_comparison_fails_above_percent_tolerance() -> None:
    fields = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "xp_t",
        [0, 100, 300],
        [0, 100, 200],
        max_curve_error_pct=12.0,
    )

    assert fields[0].ok
    assert not fields[2].ok
    assert not fields[3].ok
    assert fields[3].gem_value == 50.0


def test_player_curve_length_mismatch_fails_and_skips_max_curve_error() -> None:
    fields = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "gold_t",
        [0, 100],
        [0, 100, 200],
        max_curve_error_pct=10.0,
    )

    assert not fields[0].ok
    assert fields[0].gem_value == 2
    assert fields[0].ref_value == 3
    assert [field.name for field in fields] == [
        "npc_dota_hero_axe/gold_t/length",
        "npc_dota_hero_axe/gold_t/minute_keys",
    ]


def test_missing_opendota_player_curve_is_skipped() -> None:
    fields = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "gold_t",
        [0, 100],
        [],
        max_curve_error_pct=10.0,
    )

    assert all(field.skip for field in fields)
    assert all(field.ok for field in fields)


def test_equal_length_shifted_player_curve_fails_minute_key_alignment() -> None:
    fields = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "gold_t",
        [0, 100, 200],
        [0, 100, 200],
        gem_times_s=[60, 120, 180],
        max_curve_error_pct=3.0,
    )

    assert fields[0].ok
    assert not fields[1].ok
    assert fields[1].name == "npc_dota_hero_axe/gold_t/minute_keys"
    assert fields[1].gem_value == "1..3 (3 keys)"
    assert fields[1].ref_value == "0..2 (3 keys)"
    assert len(fields) == 2


def test_player_curve_inside_hard_tolerance_can_warn() -> None:
    fields = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "gold_t",
        [0, 100, 196],
        [0, 100, 200],
        max_curve_error_pct=3.0,
        warning_curve_error_pct=1.0,
    )

    assert all(field.ok for field in fields)
    assert fields[-1].gem_value == 2.0
    assert fields[-1].status == "WARN"


def test_player_count_curve_comparison_uses_absolute_error_threshold() -> None:
    passing = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "lh_t",
        [0, 2, 8],
        [0, 3, 6],
        max_abs_error=3,
    )
    failing = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "dn_t",
        [0, 2, 9],
        [0, 3, 4],
        max_abs_error=3,
    )

    assert all(field.ok for field in passing)
    assert not failing[2].ok
    assert not failing[3].ok
    assert failing[3].gem_value == 5


def test_player_count_curve_comparison_can_scale_absolute_error_threshold() -> None:
    fields = _compare_opendota_player_array(
        "npc_dota_hero_axe",
        "lh_t",
        [0, 400, 985],
        [0, 400, 1000],
        max_abs_error=10,
        max_abs_error_pct=0.015,
    )

    assert all(field.ok for field in fields)
    assert fields[2].ref_value == 15
    assert fields[3].gem_value == 15
    assert fields[3].ref_value == 15


def test_scalar_validation_gates_embedded_postgame_fields_exactly(tmp_path, monkeypatch) -> None:
    fixture = tmp_path / "match.dem"
    fixture.write_bytes(b"synthetic")
    player = SimpleNamespace(
        player_id=0,
        hero_name="npc_dota_hero_axe",
        kills=3,
        deaths=2,
        net_worth=12000,
        last_hits=150,
        denies=7,
        hero_damage=23456,
        tower_damage=3456,
        hero_healing=789,
        gold_per_min=600,
        xp_per_min=700,
        total_gold=1200,
        total_xp=1400,
        aghanims_scepter=1,
        aghanims_shard=0,
        moonshard=1,
        _match_details_fields={
            "hero_damage",
            "tower_damage",
            "hero_healing",
            "gold_per_min",
            "xp_per_min",
            "total_gold",
            "total_xp",
            "aghanims_scepter",
            "aghanims_shard",
            "moonshard",
        },
    )
    parsed = SimpleNamespace(
        players=[player],
        radiant_win=True,
        towers=[],
        duration=120,
        _match_details_fields={"duration"},
    )
    monkeypatch.setattr(gem, "parse", lambda _: parsed)
    opendota = {
        "players": [
            {
                "player_slot": 0,
                "hero_id": 2,
                "kills": 3,
                "deaths": 2,
                "net_worth": 12000,
                "last_hits": 150,
                "denies": 7,
                "hero_damage": 23456,
                "tower_damage": 3456,
                "hero_healing": 789,
                "gold_per_min": 600,
                "xp_per_min": 700,
                "total_gold": 1200,
                "total_xp": 1400,
                "aghanims_scepter": 1,
                "aghanims_shard": 0,
                "moonshard": 1,
            }
        ],
        "radiant_win": True,
        "tower_status_radiant": 0x7FF,
        "tower_status_dire": 0x7FF,
        "duration": 120,
    }

    result = validate_match(1, fixture, od=opendota, mode="scalar")

    fields = {field.name: field for field in result.all_fields}
    assert fields["duration"].tolerance == 0
    assert fields["npc_dota_hero_axe/hero_damage"].tolerance == 0
    assert fields["npc_dota_hero_axe/gold_per_min"].tolerance == 0
    assert fields["npc_dota_hero_axe/total_xp"].tolerance == 0
    assert fields["npc_dota_hero_axe/aghanims_scepter"].tolerance == 0
    assert fields["duration"].status == "PASS"
    assert fields["npc_dota_hero_axe/hero_damage"].status == "PASS"
    assert fields["npc_dota_hero_axe/total_xp"].status == "PASS"
    assert fields["npc_dota_hero_axe/moonshard"].status == "PASS"
    assert result.failed == 0


def test_scalar_validation_skips_postgame_fields_without_exact_provenance(
    tmp_path, monkeypatch
) -> None:
    fixture = tmp_path / "match.dem"
    fixture.write_bytes(b"synthetic")
    player = SimpleNamespace(
        player_id=0,
        hero_name="npc_dota_hero_axe",
        kills=3,
        deaths=2,
        net_worth=12000,
        last_hits=150,
        denies=7,
        hero_damage=99999,
        tower_damage=99999,
        hero_healing=99999,
        gold_per_min=0,
        xp_per_min=0,
        total_gold=0,
        total_xp=0,
        aghanims_scepter=None,
        aghanims_shard=None,
        moonshard=None,
        _match_details_fields=set(),
    )
    parsed = SimpleNamespace(
        players=[player],
        radiant_win=True,
        towers=[],
        duration=119,
        _match_details_fields=set(),
    )
    monkeypatch.setattr(gem, "parse", lambda _: parsed)
    opendota = {
        "players": [
            {
                "player_slot": 0,
                "hero_id": 2,
                "kills": 3,
                "deaths": 2,
                "net_worth": 12000,
                "last_hits": 150,
                "denies": 7,
                "hero_damage": 23456,
                "tower_damage": 3456,
                "hero_healing": 789,
                "gold_per_min": 600,
                "xp_per_min": 700,
                "total_gold": 1200,
                "total_xp": 1400,
                "aghanims_scepter": 1,
                "aghanims_shard": 0,
                "moonshard": 1,
            }
        ],
        "radiant_win": True,
        "tower_status_radiant": 0x7FF,
        "tower_status_dire": 0x7FF,
        "duration": 120,
    }

    result = validate_match(1, fixture, od=opendota, mode="scalar")

    fields = {field.name: field for field in result.all_fields}
    exact_names = {
        "duration",
        "npc_dota_hero_axe/hero_damage",
        "npc_dota_hero_axe/tower_damage",
        "npc_dota_hero_axe/hero_healing",
        "npc_dota_hero_axe/gold_per_min",
        "npc_dota_hero_axe/xp_per_min",
        "npc_dota_hero_axe/total_gold",
        "npc_dota_hero_axe/total_xp",
        "npc_dota_hero_axe/aghanims_scepter",
        "npc_dota_hero_axe/aghanims_shard",
        "npc_dota_hero_axe/moonshard",
    }
    assert all(fields[name].status == "SKIP" for name in exact_names)
    assert result.failed == 0
