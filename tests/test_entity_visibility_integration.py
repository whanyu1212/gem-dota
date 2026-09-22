"""Offline replay coverage for the all-NPC visibility timeline."""

from __future__ import annotations

import pytest

from gem.results.models import ParsedMatch, VisibilityState


@pytest.mark.integration
@pytest.mark.slow
def test_canonical_replay_emits_identity_aware_npc_visibility(
    canonical_parsed_match: ParsedMatch,
) -> None:
    events = canonical_parsed_match.entity_visibility_events

    assert events
    assert [event.tick for event in events] == sorted(event.tick for event in events)
    assert any(event.active and "Hero" not in event.class_name for event in events)
    assert any(
        event.active
        and (
            event.radiant_state is not VisibilityState.UNKNOWN
            or event.dire_state is not VisibilityState.UNKNOWN
        )
        for event in events
    )

    terminals = [event for event in events if not event.active]
    assert terminals
    assert all(
        event.radiant_state is VisibilityState.UNKNOWN
        and event.dire_state is VisibilityState.UNKNOWN
        for event in terminals
    )
