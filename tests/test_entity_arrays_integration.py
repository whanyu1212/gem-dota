"""Full-replay check that variable-length arrays shrink like Clarity's.

Reference: skadistats/clarity VectorField.java (a length write resizes the
array node and drops elements past it)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from gem.parser import ReplayParser
from gem.state.entities import Entity, EntityOp

# Team-data arrays observed to shrink during real matches.
_ARRAYS = ("m_vecKnownClearCamps", "m_vecTrackedTeleports", "m_vecItemSlots")


@pytest.mark.integration
@pytest.mark.slow
def test_team_data_arrays_never_keep_elements_past_their_length(
    ti2026_short_replay_path: Path,
) -> None:
    shrinks = 0
    checked = 0
    violations: list[str] = []
    last_length: dict[tuple[int, str], int] = {}

    # The parser turns callback exceptions into an early stop, so record
    # problems here and assert after the parse.
    def check(entity: Entity, op: EntityOp) -> None:
        nonlocal shrinks, checked
        if op & EntityOp.DELETED or not entity.cls.name.startswith(
            ("CDOTA_DataRadiant", "CDOTA_DataDire", "CDOTADataRadiant", "CDOTADataDire")
        ):
            return
        for name in _ARRAYS:
            length = entity.get(name)
            if length is None:
                continue
            if not isinstance(length, int) or isinstance(length, bool):
                violations.append(f"{name} read as {type(length).__name__}")
                continue
            checked += 1
            # Every element at or past the length must be gone (probe well beyond it).
            for i in range(length, length + 64):
                if entity.get(f"{name}.{i:04d}") is not None:
                    violations.append(f"{name} length {length} keeps element {i}")
            key = (entity.index, name)
            if length < last_length.get(key, 0):
                shrinks += 1
            last_length[key] = length

    parser = ReplayParser(str(ti2026_short_replay_path))
    parser.on_entity(check)
    parser.parse()

    assert parser.parse_error is None
    assert violations[:5] == []
    assert checked > 0
    assert shrinks > 0, "no array shrank; the replay no longer exercises this path"
