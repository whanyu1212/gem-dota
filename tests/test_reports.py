from __future__ import annotations

from gem.reports import (
    ReportOptions,
    apply_opendota_player_names,
    build_html_report,
    is_displayable_player_name,
    write_html_report,
)
from gem.results.models import ParsedMatch, ParsedPlayer


def _minimal_match() -> ParsedMatch:
    return ParsedMatch(
        match_id=123456789,
        game_mode=22,
        radiant_win=True,
        game_start_tick=0,
        game_end_tick=1800,
        players=[
            ParsedPlayer(player_id=0, hero_name="npc_dota_hero_axe", team=2, kills=1),
            ParsedPlayer(player_id=5, hero_name="npc_dota_hero_bane", team=3, deaths=1),
        ],
    )


def test_build_html_report_smoke_without_assets() -> None:
    html = build_html_report(
        _minimal_match(),
        options=ReportOptions(title="Smoke Report", include_movement=False),
    )

    assert "<!DOCTYPE html>" in html
    assert "<title>Smoke Report</title>" in html
    assert "Match ID" in html
    assert "123456789" in html


def test_player_name_display_gate_rejects_binary_looking_text() -> None:
    assert is_displayable_player_name("叽叽喳喳")
    assert is_displayable_player_name("宇宙にきらめく エメラルド")
    assert not is_displayable_player_name("0�ɛ�\x01")
    assert not is_displayable_player_name("�\x17�#�\x01")


def test_build_html_report_omits_malformed_replay_player_names() -> None:
    match = _minimal_match()
    match.players[0].player_name = "0�ɛ�\x01"

    html = build_html_report(match, options=ReportOptions(include_movement=False))

    assert "\ufffd" not in html
    assert "\x01" not in html


def test_opendota_player_names_make_reports_display_clean_cjk_names() -> None:
    match = _minimal_match()
    match.players[0].player_name = "0�ɛ�\x01"
    match.players[1].player_name = "�\x17�#�\x01"

    apply_opendota_player_names(
        match,
        {
            "players": [
                {"player_slot": 0, "personaname": "烟弹漏油"},
                {"player_slot": 128, "personaname": "李火旺"},
            ],
        },
    )
    html = build_html_report(match, options=ReportOptions(include_movement=False))

    assert match.players[0].player_name == "烟弹漏油"
    assert match.players[1].player_name == "李火旺"
    assert "烟弹漏油" in html
    assert "李火旺" in html
    assert "\ufffd" not in html


def test_write_html_report_returns_written_path(tmp_path) -> None:
    output = tmp_path / "report.html"

    written = write_html_report(
        _minimal_match(),
        output,
        options=ReportOptions(include_movement=False),
    )

    assert written == output
    assert output.exists()
    assert "Dota 2 Match Report" in output.read_text(encoding="utf-8")
