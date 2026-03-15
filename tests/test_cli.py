"""Tests for gem CLI entrypoint."""

from __future__ import annotations

from pathlib import Path

import pytest

from gem.__main__ import main
from gem.models import ParsedMatch


def _mock_match() -> ParsedMatch:
    match = ParsedMatch(match_id=123)
    pp = match.players[0]
    pp.hero_name = "npc_dota_hero_axe"
    pp.team = 2
    pp.times = [3000]
    pp.gold_t = [1500]
    pp.lh_t = [25]
    return match


class TestCli:
    def test_summary_format_default_is_backward_compatible(self, monkeypatch, capsys):
        from gem import __main__ as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "██████" in out
        assert "Parsing fake.dem" in out
        assert "hero kills" in out
        assert "npc_dota_hero_axe" in out

    def test_json_format_prints_to_stdout_without_output(self, monkeypatch, capsys):
        from gem import __main__ as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--format", "json"])
        monkeypatch.setattr(cli, "parse_to_json", lambda path, indent=2: '{"match_id": 321}')

        main()

        out = capsys.readouterr().out
        assert '{"match_id": 321}' in out

    def test_json_format_writes_to_file_when_output_given(self, monkeypatch, tmp_path):
        from gem import __main__ as cli

        out_file = tmp_path / "out.json"
        monkeypatch.setattr(
            "sys.argv",
            ["gem", "fake.dem", "--format", "json", "--output", str(out_file)],
        )
        monkeypatch.setattr(cli, "parse_to_json", lambda path, indent=2: '{"match_id": 321}')

        main()

        assert out_file.exists()
        assert out_file.read_text(encoding="utf-8") == '{"match_id": 321}'

    def test_parquet_requires_output(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--format", "parquet"])

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 2
        err = capsys.readouterr().err
        assert "--output is required" in err

    def test_parquet_calls_parse_to_parquet(self, monkeypatch, tmp_path, capsys):
        from gem import __main__ as cli

        out_dir = tmp_path / "pq"
        called: dict[str, Path | str] = {}

        def _fake_parse_to_parquet(path, output_dir):
            called["path"] = path
            called["output_dir"] = output_dir
            return [Path(output_dir) / "players.parquet"]

        monkeypatch.setattr(
            "sys.argv",
            ["gem", "fake.dem", "--format", "parquet", "--output", str(out_dir)],
        )
        monkeypatch.setattr(cli, "parse_to_parquet", _fake_parse_to_parquet)

        main()

        assert called["path"] == "fake.dem"
        assert Path(called["output_dir"]) == out_dir
        out = capsys.readouterr().out
        assert "Wrote 1 parquet file(s)" in out

    def test_quiet_suppresses_banner_and_parsing_line(self, monkeypatch, capsys):
        from gem import __main__ as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--quiet"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "██████" not in out
        assert "Parsing fake.dem" not in out
        assert "npc_dota_hero_axe" in out

    def test_no_banner_hides_only_banner(self, monkeypatch, capsys):
        from gem import __main__ as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--no-banner"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "██████" not in out
        assert "Parsing fake.dem" in out
        assert "hero kills" in out

    def test_progress_prints_phase_messages(self, monkeypatch, capsys):
        from gem import __main__ as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--progress"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        # Rich Progress in non-TTY mode prints the completed task description after stop()
        assert "Parsing replay" in out
        assert "Rendering summary" in out

    def test_timings_prints_summary(self, monkeypatch, capsys):
        from gem import __main__ as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--timings"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "Timing summary" in out
        assert "Parsing replay" in out
        assert "Rendering summary" in out
        assert "Total" in out

    def test_json_timings_go_to_stderr_when_stdout_contains_payload(self, monkeypatch, capsys):
        from gem import __main__ as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--format", "json", "--timings"])
        monkeypatch.setattr(cli, "parse_to_json", lambda path, indent=2: '{"match_id": 321}')

        main()

        captured = capsys.readouterr()
        assert captured.out.strip() == '{"match_id": 321}'
        assert "Timing summary" in captured.err

    def test_help_includes_examples(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["gem", "--help"])

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "Examples:" in out
        assert "python -m gem match.dem --format json" in out
