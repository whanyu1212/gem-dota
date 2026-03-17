"""MkDocs hook — copy raw files from docs/reports/ into site/reports/."""

import shutil
from pathlib import Path


def on_post_build(config: dict, **kwargs: object) -> None:
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])
    reports_src = docs_dir / "reports"
    reports_dst = site_dir / "reports"
    for src_file in reports_src.iterdir():
        if src_file.suffix == ".html":
            reports_dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, reports_dst / src_file.name)
