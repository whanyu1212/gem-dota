"""Unit tests for local OpenDota validator helpers."""

from gem.combat.log import CombatLogEntry
from scripts.validate_opendota import _opendota_teamfights_from_combat_log


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
