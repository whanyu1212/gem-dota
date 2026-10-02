from __future__ import annotations

import json

from gem.analysis.roshan import (
    AegisFateSource,
    RoshConversion,
    RoshTeamAttributionSource,
)
from gem.extractors.fights import Fight, FightPlayer
from gem.extractors.objectives import BarracksKill, TowerKill
from gem.reports import ReportOptions, build_html_report, builder as report_builder
from gem.reports._formatting import set_game_start_tick
from gem.reports.assets import ReportAssets
from gem.reports.sections import match as match_section
from gem.reports.sections.combat import build_fights
from gem.results.models import ParsedMatch


def _conversion(**overrides: object) -> RoshConversion:
    fields: dict[str, object] = {
        "rosh_number": 1,
        "rosh_tick": 1000,
        "killer_name": "npc_dota_hero_axe",
        "holder_team": 2,
        "holder_player_id": 0,
        "holder_name": "npc_dota_hero_axe",
        "aegis_pickup_tick": 1010,
        "immediate_end_tick": 1600,
        "aegis_end_tick": 1500,
        "aegis_eval_end_tick": 1600,
        "extended_end_tick": 4000,
        "aegis_fate": "consumed",
        "first_fight_tick": 1100,
        "first_objective_tick": 1250,
        "fight_count": 1,
        "fights_won": 0,
        "fights_lost": 1,
        "fights_drawn": 0,
        "towers_taken": 1,
        "barracks_taken": 0,
        "enemy_buybacks_forced": 0,
        "enemy_half_observer_delta": 0,
        "enemy_half_farm_share_before": 0.0,
        "enemy_half_farm_share_during": 0.0,
        "enemy_half_farm_share_delta": 0.0,
        "conversion_score": 99,
        "conversion_label": "objective_conversion",
        "aegis_outcome": "consumed_in_fight",
        "drops": ["aegis", "banner"],
        "roshan_team": 2,
        "conversion_team": 2,
        "roshan_team_source": RoshTeamAttributionSource.PROTOCOL,
        "conversion_team_source": RoshTeamAttributionSource.PLAYER_ID,
        "aegis_fate_source": AegisFateSource.HOLDER_DEATH_INFERENCE,
        "aegis_fate_inferred": True,
        "conversion_tags": ["fight_advantage", "territorial_expansion"],
        "analysis_status": "partial",
    }
    fields.update(overrides)
    return RoshConversion(**fields)  # type: ignore[arg-type]


def _fight(start_tick: int, end_tick: int, winner: str) -> Fight:
    players = [FightPlayer(player_id=player_id) for player_id in range(10)]
    players[0].deaths = 1
    return Fight(
        start_tick=start_tick,
        end_tick=end_tick,
        first_death_tick=start_tick + 100,
        last_death_tick=start_tick + 100,
        deaths=1,
        winner=winner,
        players=players,
    )


def _match() -> ParsedMatch:
    return ParsedMatch(
        game_start_tick=0,
        fights=[_fight(1100, 1300, "dire"), _fight(3000, 3200, "radiant")],
        towers=[
            TowerKill(
                tick=1200,
                team=3,
                killer="npc_dota_hero_axe",
                tower_name="npc_dota_badguys_tower1_mid",
                killer_team=2,
            ),
            # Denied by its owner during the hold: not taken by the holder's team.
            TowerKill(
                tick=1300,
                team=3,
                killer="npc_dota_hero_razor",
                tower_name="npc_dota_badguys_tower1_top",
                killer_team=3,
            ),
            TowerKill(tick=1250, team=2, killer="", tower_name="npc_dota_goodguys_tower1_bot"),
            TowerKill(tick=3100, team=3, killer="", tower_name="npc_dota_badguys_tower2_mid"),
        ],
        barracks=[
            BarracksKill(
                tick=1400,
                team=3,
                killer="npc_dota_hero_axe",
                barracks_name="npc_dota_badguys_melee_rax_mid",
                killer_team=2,
            ),
        ],
    )


def _render(conversion: RoshConversion) -> str:
    set_game_start_tick(0)
    return match_section.build_rosh_conversion(_match(), [conversion])


def test_roshan_tab_lists_kill_and_aegis_facts() -> None:
    html = _render(_conversion())

    assert "<summary>Roshan</summary>" in html
    assert 'id="roshan-1"' in html
    assert "Aegis, Banner" in html
    assert "picked up" in html
    assert "Consumed*" in html
    assert "* Consumed is inferred" in html
    # Only the fight overlapping the hold, and only enemy buildings in it.
    assert 'href="#fight-1"' in html
    assert 'href="#fight-2"' not in html
    assert "Dire won" in html
    assert "1 tower, 1 barracks" in html


def test_roshan_tab_drops_interpretation() -> None:
    html = _render(_conversion())

    for removed in (
        "Fight advantage",
        "Territorial expansion",
        "Consumed In Fight",
        "rosh-coverage-map",
        "Evidence: Partial",
        "conversion",
    ):
        assert removed not in html.replace("rosh-section", "")


def test_roshan_tab_denied_aegis_is_never_held() -> None:
    conversion = _conversion(aegis_fate="denied", aegis_fate_inferred=False, holder_name="")
    html = _render(conversion)

    assert '<td class="dim">Denied</td>' in html
    assert 'href="#fight-' not in html
    assert "during Aegis" not in build_fights(_match(), None, rosh_conversions=[conversion])


def test_roshan_tab_without_pickup_shows_no_hold() -> None:
    html = _render(
        _conversion(aegis_pickup_tick=None, aegis_fate="unknown", aegis_fate_inferred=False)
    )

    assert "Not picked up" in html
    assert 'href="#fight-' not in html


def test_fight_card_links_to_the_aegis_it_overlaps() -> None:
    html = build_fights(_match(), None, rosh_conversions=[_conversion()])

    assert 'href="#roshan-1"' in html
    assert 'data-report-target="roshan-1"' in html
    assert html.count("during Aegis #1") == 1


def test_full_report_escapes_public_map_string_inside_script(monkeypatch) -> None:
    monkeypatch.setattr(
        report_builder,
        "_ext_build_rosh_conversion",
        lambda _match, _conversions=None: "",
    )
    hostile = 'QUJD";window.pwned=1;//</script><script>'
    html = build_html_report(
        ParsedMatch(game_start_tick=0, game_end_tick=30),
        assets=ReportAssets(),
        options=ReportOptions(include_movement=False),
        map_b64=hostile,
    )

    expected = json.dumps(f"data:image/jpeg;base64,{hostile}")
    expected = expected.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    assert f"window._GEM_MAP_SRC={expected};" in html
    assert '";window.pwned=1;//</script>' not in html
