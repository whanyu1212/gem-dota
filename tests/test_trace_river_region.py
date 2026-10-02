from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
import pytest

from scripts.trace_river_region import (
    DEFAULT_CONSTANTS,
    image_to_world,
    trace_regions,
    trace_river,
    trace_size,
    world_to_image,
    write_regions,
)

# Full-resolution size of assets/maps/Game_map_7.41.jpg.
_IMAGE_SIZE = (8878, 8356)


def _committed_regions() -> dict:
    return json.loads(DEFAULT_CONSTANTS.read_text(encoding="utf-8"))["regions"]


def test_projection_round_trips() -> None:
    width, height = trace_size(_IMAGE_SIZE)
    assert (width, height) == (1800, 1694)
    x, y = image_to_world(412.0, 630.0, width, height)
    px, py = world_to_image(x, y, width, height)
    assert px == pytest.approx(412.0)
    assert py == pytest.approx(630.0)


def test_projection_places_the_fountain_like_the_report_maps() -> None:
    # The Radiant fountain entity and its pixel centre in the full-resolution image,
    # as pinned by tests/test_report_map_projection.py.
    px, py = world_to_image(8928, 9446, *_IMAGE_SIZE)
    assert abs(px - 906) <= 30
    assert abs(py - 7567) <= 30


def test_write_regions_keeps_the_committed_layout(tmp_path: Path) -> None:
    target = tmp_path / "map_constants.json"
    shutil.copy(DEFAULT_CONSTANTS, target)
    regions = _committed_regions()
    write_regions(
        target,
        {"river_outline": regions["river_outline"], "half_line": regions["half_line"]},
    )
    assert target.read_text(encoding="utf-8") == DEFAULT_CONSTANTS.read_text(encoding="utf-8")


def test_write_regions_replaces_the_arrays(tmp_path: Path) -> None:
    target = tmp_path / "map_constants.json"
    shutil.copy(DEFAULT_CONSTANTS, target)
    outline = [[1, 2], [3, 4], [5, 6]]
    write_regions(target, {"river_outline": outline})
    regions = json.loads(target.read_text(encoding="utf-8"))["regions"]
    assert regions["river_outline"] == outline
    assert regions["half_line"] == _committed_regions()["half_line"]


def test_trace_rejects_a_seed_outside_the_water() -> None:
    pytest.importorskip("cv2", reason="run with: uv run --with opencv-python-headless pytest")
    no_water = np.zeros(trace_size(_IMAGE_SIZE)[::-1], dtype=bool)
    with pytest.raises(SystemExit, match="SEED_POOL"):
        trace_river(no_water)


def test_trace_reproduces_the_committed_regions() -> None:
    pytest.importorskip("cv2", reason="run with: uv run --with opencv-python-headless pytest")
    regions = _committed_regions()
    assert trace_regions() == {
        "river_outline": regions["river_outline"],
        "half_line": regions["half_line"],
    }
