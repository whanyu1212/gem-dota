from __future__ import annotations

from gem.reports import ReportOptions, build_html_report, write_html_report
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
