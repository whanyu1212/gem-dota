"""Tests for gem CLI entrypoint."""

from __future__ import annotations

from pathlib import Path

import pytest

from gem.cli import main
from gem.replays.batch import ParseResult
from gem.results.models import ParsedMatch


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
    def test_python_m_adapter_uses_cli_main(self):
        import gem.__main__ as module_main
        import gem.cli as cli

        assert module_main.main is cli.main

    def test_summary_format_default_is_backward_compatible(self, monkeypatch, capsys):
        import gem.cli as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "██████" in out
        assert "Parsing fake.dem" in out
        assert "hero kills" in out
        assert "npc_dota_hero_axe" in out

    def test_json_format_prints_to_stdout_without_output(self, monkeypatch, capsys):
        import gem.cli as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--format", "json"])
        monkeypatch.setattr(cli, "parse_to_json", lambda path, indent=2: '{"match_id": 321}')

        main()

        out = capsys.readouterr().out
        assert '{"match_id": 321}' in out

    def test_json_format_writes_to_file_when_output_given(self, monkeypatch, tmp_path):
        import gem.cli as cli

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
        import gem.cli as cli

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
        import gem.cli as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--quiet"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "██████" not in out
        assert "Parsing fake.dem" not in out
        assert "npc_dota_hero_axe" in out

    def test_no_banner_hides_only_banner(self, monkeypatch, capsys):
        import gem.cli as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--no-banner"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "██████" not in out
        assert "Parsing fake.dem" in out
        assert "hero kills" in out

    def test_progress_prints_phase_messages(self, monkeypatch, capsys):
        import gem.cli as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--progress"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        # Rich Progress in non-TTY mode prints the completed task description after stop()
        assert "Parsing replay" in out
        assert "Rendering summary" in out

    def test_timings_prints_summary(self, monkeypatch, capsys):
        import gem.cli as cli

        monkeypatch.setattr("sys.argv", ["gem", "fake.dem", "--timings"])
        monkeypatch.setattr(cli, "parse", lambda path: _mock_match())

        main()

        out = capsys.readouterr().out
        assert "Timing summary" in out
        assert "Parsing replay" in out
        assert "Rendering summary" in out
        assert "Total" in out

    def test_json_timings_go_to_stderr_when_stdout_contains_payload(self, monkeypatch, capsys):
        import gem.cli as cli

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

    def test_reports_assets_path_command(self, monkeypatch, tmp_path, capsys):
        monkeypatch.setattr(
            "sys.argv",
            ["gem", "reports", "assets", "path", "--asset-dir", str(tmp_path)],
        )

        main()

        out = capsys.readouterr().out
        assert "Report asset cache paths" in out
        assert "Hero icons" in out
        assert "Item icons" in out

    def test_reports_assets_status_command(self, monkeypatch, tmp_path, capsys):
        monkeypatch.setattr(
            "sys.argv",
            ["gem", "reports", "assets", "status", "--asset-dir", str(tmp_path)],
        )

        main()

        out = capsys.readouterr().out
        assert "Report asset status" in out
        assert "Hero icons" in out
        assert "Item icons" in out
        assert "Map images" in out

    def test_batch_parquet_reports_failures_from_single_parse(self, monkeypatch, tmp_path, capsys):
        import gem
        import gem.replays.batch as batch

        out_dir = tmp_path / "out"
        good = tmp_path / "good.dem"
        bad = tmp_path / "bad.dem"
        match = _mock_match()
        results = [
            ParseResult(path=good, match=match, error=None),
            ParseResult(path=bad, match=None, error=ValueError("corrupt replay")),
        ]
        parse_calls = 0
        parquet_dirs: list[Path] = []

        def _fake_parse_many(source, **kwargs):
            nonlocal parse_calls
            parse_calls += 1
            assert source == [good, bad]
            assert kwargs["timeout"] == 2.5
            return results

        def _fake_to_parquet(parsed_match, output_dir):
            assert parsed_match is match
            parquet_dirs.append(Path(output_dir))
            return [Path(output_dir) / "players.parquet"]

        monkeypatch.setattr(
            "sys.argv",
            [
                "gem",
                "batch",
                str(good),
                str(bad),
                "--format",
                "parquet",
                "--output",
                str(out_dir),
                "--timeout",
                "2.5",
                "--no-banner",
            ],
        )
        monkeypatch.setattr(batch, "parse_many", _fake_parse_many)
        monkeypatch.setattr(gem, "to_parquet", _fake_to_parquet)

        main()

        out = capsys.readouterr().out
        assert parse_calls == 1
        assert parquet_dirs == [out_dir / "good"]
        assert "Wrote 1 parquet file(s)" in out
        assert "Batch summary" in out
        assert "1 succeeded" in out
        assert "1 failed" in out
        assert "ValueError" in out
        assert "corrupt replay" in out

    def test_batch_strict_exits_nonzero_on_failure(self, monkeypatch, tmp_path):
        import gem.replays.batch as batch

        out_dir = tmp_path / "out"
        bad = tmp_path / "bad.dem"
        results = [ParseResult(path=bad, match=None, error=ValueError("corrupt replay"))]

        monkeypatch.setattr(
            "sys.argv",
            [
                "gem",
                "batch",
                str(bad),
                "--format",
                "parquet",
                "--output",
                str(out_dir),
                "--strict",
                "--no-banner",
            ],
        )
        monkeypatch.setattr(batch, "parse_many", lambda *args, **kwargs: results)

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 1
