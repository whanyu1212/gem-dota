"""gem.reports is deprecated (HY-136): it warns when used, and only then.

Subprocesses, because the test process has already imported gem and gem.reports.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

from gem.cli import main

_WARNING = "gem.reports is deprecated and will be removed in gem 0.14"


def _python(code: str, *flags: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *flags, "-c", code], capture_output=True, text=True, check=False
    )


def test_importing_gem_does_not_import_or_warn_about_the_report() -> None:
    run = _python(
        "import sys, gem; gem.parse; gem.to_json; gem.catalog.map.world_to_map_image\n"
        "assert 'gem.reports' not in sys.modules",
        "-W",
        "error::DeprecationWarning",
    )
    assert run.returncode == 0, run.stderr


def test_importing_gem_reports_warns() -> None:
    run = _python("import gem.reports", "-W", "always::DeprecationWarning")
    assert run.returncode == 0, run.stderr
    assert _WARNING in run.stderr
    assert "cookbook" in run.stderr


def test_gem_reports_still_works_through_the_package_attribute() -> None:
    run = _python(
        "import gem; assert callable(gem.reports.write_html_report)",
        "-W",
        "always::DeprecationWarning",
    )
    assert run.returncode == 0, run.stderr
    assert _WARNING in run.stderr


def test_gem_has_no_other_lazy_attributes() -> None:
    import gem

    with pytest.raises(AttributeError):
        _ = gem.not_a_module  # type: ignore[attr-defined]


def test_reports_cli_command_says_it_is_deprecated(monkeypatch, tmp_path, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv", ["gem", "reports", "assets", "path", "--asset-dir", str(tmp_path)]
    )

    main()

    captured = capsys.readouterr()
    assert "`python -m gem reports` is deprecated" in captured.err
    assert "Report asset cache paths" in captured.out
