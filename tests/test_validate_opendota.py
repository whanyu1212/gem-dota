"""Unit tests for local OpenDota validator helpers."""

from gem.combat.log import CombatLogEntry
from scripts.validate_opendota import (
    _compare_opendota_player_array,
    _opendota_teamfights_from_combat_log,
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
    assert not fields[1].ok
    assert not fields[2].ok
    assert fields[2].gem_value == 50.0


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
        "npc_dota_hero_axe/gold_t/final",
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
    assert not failing[1].ok
    assert not failing[2].ok
    assert failing[2].gem_value == 5
