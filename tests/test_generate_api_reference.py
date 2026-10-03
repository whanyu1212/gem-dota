from __future__ import annotations

import shutil
from pathlib import Path

from scripts import generate_api_reference as gen

_REFERENCE = Path(__file__).resolve().parents[1] / "docs" / "reference"


def test_regenerating_is_stable(tmp_path: Path) -> None:
    # A second run must not change the first run's output: the narrative is kept
    # and only the generated section is replaced.
    pages = tmp_path / "reference"
    shutil.copytree(_REFERENCE, pages)
    assert gen.generate(pages) == len(list(_REFERENCE.rglob("*.md")))
    first = {page: page.read_text(encoding="utf-8") for page in pages.rglob("*.md")}
    gen.generate(pages)
    for page, text in first.items():
        assert page.read_text(encoding="utf-8") == text, page.name


def test_keeps_the_narrative_and_replaces_the_generated_section(tmp_path: Path) -> None:
    page = tmp_path / "dataframes.md"
    page.write_text(
        "# DataFrames\n\nHand-written text.\n\n---\n\n## Generated API\n\nstale\n",
        encoding="utf-8",
    )
    gen.generate(tmp_path)
    text = page.read_text(encoding="utf-8")

    narrative, generated = text.split("## Generated API\n")
    assert narrative == "# DataFrames\n\nHand-written text.\n\n---\n\n"
    assert "stale" not in generated
    assert "### `build_dataframes`" in generated
    assert (
        "https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/dataframes.py#L"
        in generated
    )


def test_main_writes_to_the_given_folder(tmp_path: Path, capsys) -> None:
    (tmp_path / "dataframes.md").write_text("# DataFrames\n", encoding="utf-8")
    assert gen.main(["--reference-dir", str(tmp_path)]) == 0
    assert "## Generated API" in (tmp_path / "dataframes.md").read_text(encoding="utf-8")
    assert "Generated 1 reference pages" in capsys.readouterr().out
