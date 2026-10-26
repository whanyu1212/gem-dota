"""Full-replay check of string-table index jumps and key history.

``ActiveModifiers`` names each entry by its own index ("0", "1", ...), so a
replay carries its own answer key: every entry must sit at the index its name
says. Manta's rules (absolute jumps, keyed-only history) fail this after about
ten minutes of a match; Clarity's rules pass it.

Reference: skadistats/clarity S2StringTableEmitter.java (pinned revision in
CLAUDE.md)
"""

from __future__ import annotations

import pytest


@pytest.mark.integration
@pytest.mark.slow
def test_active_modifiers_entries_sit_at_the_index_their_name_says(canonical_replay_pass) -> None:
    parser = canonical_replay_pass.parser
    assert parser.parse_error is None

    table = parser.string_tables.get_by_name("ActiveModifiers")
    assert table is not None
    numbered = {index: key for index, (key, _) in table.items.items() if key.isdigit()}
    misplaced = {index: key for index, key in numbered.items() if int(key) != index}

    assert len(numbered) > 1000
    assert misplaced == {}
