from __future__ import annotations

import json
from typing import Literal

from gem.analysis._territory import RoshCoverageCell, RoshTerritoryWindow
from gem.analysis.roshan import (
    RoshConversion,
    RoshDifferentialProfile,
    RoshTimelineEvent,
)
from gem.extractors.wards import WardEvent
from gem.reports import ReportOptions, build_html_report, builder as report_builder
from gem.reports._formatting import set_game_start_tick
from gem.reports.assets import ReportAssets
from gem.reports.sections import match as match_section
from gem.results.models import ParsedMatch


def _coverage_window(
    *,
    start_tick: int,
    end_tick: int,
    status: Literal["complete", "partial", "unavailable"] = "complete",
) -> RoshTerritoryWindow:
    conversion_cell = RoshCoverageCell(
        grid_x=12,
        grid_y=13,
        x_min=14763.0,
        x_max=15363.0,
        y_min=15600.0,
        y_max=16200.0,
        hero_seconds=64.0,
        distinct_heroes=2,
        occupied_buckets=2,
        bucket_count=3,
        occupancy_share=2 / 3,
    )
    opponent_cell = RoshCoverageCell(
        grid_x=12,
        grid_y=13,
        x_min=14763.0,
        x_max=15363.0,
        y_min=15600.0,
        y_max=16200.0,
        hero_seconds=42.0,
        distinct_heroes=2,
        occupied_buckets=1,
        bucket_count=3,
        occupancy_share=1 / 3,
    )
    return RoshTerritoryWindow(
        start_tick=start_tick,
        end_tick=end_tick,
        conversion_coverage_pct=12.5 if status != "unavailable" else None,
        opponent_coverage_pct=8.0 if status != "unavailable" else None,
        coverage_differential_pct=4.5 if status != "unavailable" else None,
        conversion_depth_p90=0.65 if status != "unavailable" else None,
        opponent_depth_p90=0.42 if status != "unavailable" else None,
        depth_differential=0.23 if status != "unavailable" else None,
        conversion_player_time_coverage=0.92 if status != "unavailable" else None,
        opponent_player_time_coverage=0.88 if status != "unavailable" else None,
        conversion_cells=[conversion_cell] if status != "unavailable" else [],
        opponent_cells=[opponent_cell] if status != "unavailable" else [],
        status=status,
        status_reasons=["position_samples_unavailable"] if status == "unavailable" else [],
    )


def _profile(*, maps_available: bool = True) -> RoshDifferentialProfile:
    map_status: Literal["complete", "unavailable"] = "complete" if maps_available else "unavailable"
    return RoshDifferentialProfile(
        conversion_team=2,
        opponent_team=3,
        window_start_tick=1000,
        window_end_tick=1600,
        conversion_fights_won=1,
        opponent_fights_won=3,
        fights_drawn=0,
        fight_differential=-2,
        conversion_towers=1,
        opponent_towers=2,
        conversion_barracks=0,
        opponent_barracks=1,
        conversion_structure_value=2,
        opponent_structure_value=7,
        structure_delta=-5,
        net_worth_advantage_start=-1000,
        net_worth_advantage_end=1500,
        net_worth_swing=2500,
        net_worth_swing_per_minute=1250.0,
        xp_advantage_start=None,
        xp_advantage_end=None,
        xp_swing=None,
        xp_swing_per_minute=None,
        before_territory=_coverage_window(
            start_tick=700,
            end_tick=999,
            status=map_status,
        ),
        during_territory=_coverage_window(
            start_tick=1000,
            end_tick=1600,
            status=map_status,
        ),
        conversion_coverage_swing_pct=8.0,
        opponent_coverage_swing_pct=0.5,
        coverage_swing_pct=7.5,
        conversion_depth_swing=0.10,
        opponent_depth_swing=0.225,
        depth_swing=-0.125,
        conversion_forward_wards=1,
        opponent_forward_wards=3,
        forward_ward_delta=-2,
        conversion_tormentors=1,
        opponent_tormentors=0,
        tormentor_delta=1,
        tags=["fight_advantage", "territorial_expansion"],
        status="partial",
        status_reasons=["xp_series_unavailable"],
    )


def _conversion(*, maps_available: bool = True) -> RoshConversion:
    profile = _profile(maps_available=maps_available)
    return RoshConversion(
        rosh_number=1,
        rosh_tick=1000,
        killer_name="npc_dota_hero_axe",
        holder_team=2,
        holder_player_id=0,
        holder_name="npc_dota_hero_axe",
        aegis_pickup_tick=1010,
        immediate_end_tick=1600,
        aegis_end_tick=1500,
        aegis_eval_end_tick=1600,
        extended_end_tick=4000,
        aegis_fate="consumed",
        first_fight_tick=1100,
        first_objective_tick=1250,
        fight_count=4,
        fights_won=1,
        fights_lost=3,
        fights_drawn=0,
        towers_taken=1,
        barracks_taken=0,
        enemy_buybacks_forced=1,
        enemy_half_observer_delta=-2,
        enemy_half_farm_share_before=0.15,
        enemy_half_farm_share_during=0.23,
        enemy_half_farm_share_delta=0.08,
        conversion_score=99,
        conversion_label="objective_conversion",
        aegis_outcome="consumed_in_fight",
        timeline_events=[
            RoshTimelineEvent(1400, "tormentor", "Tormentor secured"),
            RoshTimelineEvent(1000, "roshan", "Roshan #1 killed"),
            RoshTimelineEvent(1300, "buyback", "Bane buyback"),
            RoshTimelineEvent(1200, "fight_loss", "Fight lost"),
            RoshTimelineEvent(1350, "own_buyback", "Axe buyback"),
        ],
        drops=["aegis", "banner"],
        had_high_value_drop=True,
        banner_planted=True,
        banner_rax_conversion=True,
        banner_rax_lane="mid",
        roshan_team=2,
        conversion_team=2,
        aegis_fate_inferred=True,
        conversion_tags=["fight_advantage", "territorial_expansion"],
        analysis_status="partial",
        analysis_status_reasons=["xp_series_unavailable"],
        differential_profile=profile,
    )


def _render(monkeypatch, conversion: RoshConversion, *, map_b64: str | None = None) -> str:
    set_game_start_tick(0)
    monkeypatch.setattr(
        match_section,
        "build_rosh_conversions",
        lambda _match: [conversion],
    )
    match = ParsedMatch(
        game_start_tick=0,
        wards=[
            WardEvent(
                tick=1100,
                player_id=0,
                placer="npc_dota_hero_axe",
                ward_type="observer",
                team=2,
                x=15000.0,
                y=15900.0,
                expires_tick=None,
                killed_tick=None,
                killer="",
            )
        ],
    )
    return match_section.build_rosh_conversion(match, map_b64)


def test_report_renders_raw_signed_balance_resources_tags_and_status(monkeypatch) -> None:
    html = _render(monkeypatch, _conversion())

    assert "Fight differential: -2" in html
    assert "Weighted structure differential: -5" in html
    assert "Net worth swing: +2,500" in html
    assert "Coverage swing: +7.5 pp" in html
    assert "Depth swing: -0.125" in html
    assert "Forward-ward differential: -2" in html
    assert "Tormentor differential: +1" in html
    assert "Unavailable" in html
    assert "Insufficient samples" in html
    assert "-1,000" in html and "+1,500" in html and "+1,250.0" in html
    assert "Fight advantage" in html
    assert "Territorial expansion" in html
    assert "Evidence: Partial" in html
    assert "XP Series Unavailable" in html
    assert "Context: Objective Conversion" in html
    assert "conversion_score" not in html
    assert "radar" not in html.lower()


def test_report_timeline_is_semantic_two_sided_and_chronological(monkeypatch) -> None:
    html = _render(monkeypatch, _conversion())

    assert '<ol class="rosh-timeline-list">' in html
    assert 'aria-label="Chronological conversion evidence"' in html
    assert "Bane buyback" in html
    assert "Axe buyback" in html
    assert "Tormentor secured" in html
    assert "rosh-event-buyback" in html
    assert "rosh-event-own_buyback" in html
    assert "rosh-event-tormentor" in html
    assert html.index('data-tick="1000"') < html.index('data-tick="1200"')
    assert html.index('data-tick="1200"') < html.index('data-tick="1300"')
    assert html.index('data-tick="1300"') < html.index('data-tick="1350"')
    assert html.index('data-tick="1350"') < html.index('data-tick="1400"')


def test_report_renders_accessible_paired_maps_with_shared_background(monkeypatch) -> None:
    html = _render(monkeypatch, _conversion(), map_b64="QUJD")

    assert html.count('class="rosh-coverage-map"') == 2
    assert html.count('class="gem-map-bg"') == 2
    assert html.count('role="img"') >= 2
    assert "aria-labelledby=" in html
    assert "Before sampled territory occupancy" in html
    assert "During sampled territory occupancy" in html
    assert "Conversion team occupancy" in html
    assert "Opponent occupancy" in html
    assert "Contested cell" in html
    assert "rosh-coverage-cell contested" in html
    assert "rosh-ward-marker conversion observer" in html
    assert "sampled/sustained occupancy, not true control" in html


def test_report_maps_have_dark_fallback_and_explicit_unavailable_state(monkeypatch) -> None:
    complete_html = _render(monkeypatch, _conversion(), map_b64=None)
    unavailable_html = _render(monkeypatch, _conversion(maps_available=False), map_b64=None)

    assert complete_html.count('class="rosh-map-fallback"') == 2
    assert "gem-map-bg" not in complete_html
    assert unavailable_html.count("Coverage unavailable") >= 2
    assert "Position Samples Unavailable" in unavailable_html


def test_full_report_passes_map_background_to_roshan_builder(monkeypatch) -> None:
    seen: list[str | None] = []

    def _fake_roshan(_match: ParsedMatch, map_b64: str | None = None) -> str:
        seen.append(map_b64)
        return '<div class="rosh-map-probe"></div>'

    monkeypatch.setattr(report_builder, "_ext_build_rosh_conversion", _fake_roshan)
    html = build_html_report(
        ParsedMatch(game_start_tick=0, game_end_tick=30),
        assets=ReportAssets(),
        options=ReportOptions(include_movement=False),
        map_b64="QUJD",
    )

    assert seen == ["QUJD"]
    assert "rosh-map-probe" in html
    assert 'window._GEM_MAP_SRC="data:image/jpeg;base64,QUJD"' in html


def test_full_report_escapes_public_map_string_inside_script(monkeypatch) -> None:
    monkeypatch.setattr(
        report_builder,
        "_ext_build_rosh_conversion",
        lambda _match, _map_b64=None: "",
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
