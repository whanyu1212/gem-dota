"""The rune extractor: every rune entity, matched to the rune chat events (HY-151)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import gem.extractors.runes as runes_module
from gem.extractors.runes import Rune, RuneExtractor
from gem.proto.dota_usermessages_pb2 import (
    CHAT_MESSAGE_RUNE_BOTTLE,
    CHAT_MESSAGE_RUNE_DENY,
    CHAT_MESSAGE_RUNE_PICKUP,
)
from gem.state.entities import EntityOp

CREATED, DELETED = EntityOp.CREATED, EntityOp.DELETED
REENTERED = EntityOp.UPDATED | EntityOp.ENTERED


class _Entity:
    def __init__(self, index: int, rune_type: int, pos: tuple[float, float]) -> None:
        self.index, self.rune_type, self.pos = index, rune_type, pos

    def get_index(self) -> int:
        return self.index

    def get_int32(self, name: str) -> int | None:
        return self.rune_type if name == "m_iRuneType" else None


@pytest.fixture
def run(monkeypatch: pytest.MonkeyPatch):
    """Play entity ops and chat events through a RuneExtractor, then finalize it."""
    monkeypatch.setattr(runes_module, "_pos", lambda entity: entity.pos)

    def play(steps: list[tuple]) -> list[Rune]:
        parser = SimpleNamespace(tick=0)
        extractor = RuneExtractor()
        extractor._parser = parser  # type: ignore[assignment]
        for step in sorted(steps, key=lambda s: s[0]):
            parser.tick = step[0]
            if step[1] == "entity":
                _, _, entity, op = step
                extractor._on_entity(entity, op)
            else:
                _, _, chat_type, slot, rune_type = step
                event = SimpleNamespace(type=chat_type, playerid_1=slot, value=rune_type)
                extractor._on_chat_event(event, step[0])  # type: ignore[arg-type]
        return extractor.finalize()

    return play


def test_runes_end_taken_bottled_denied_untaken_or_still_there(run) -> None:
    dd, bounty, haste, invis, shield = (
        _Entity(1, 0, (14700.0, 17500.0)),
        _Entity(2, 5, (15388.0, 20815.0)),
        _Entity(3, 1, (17600.0, 15200.0)),
        _Entity(4, 3, (14700.0, 17500.0)),
        _Entity(5, 9, (17600.0, 15200.0)),
    )
    runes = run(
        [
            (100, "entity", dd, CREATED),
            (100, "entity", bounty, CREATED),
            (100, "entity", haste, CREATED),
            (200, "entity", dd, DELETED),
            (200, "chat", CHAT_MESSAGE_RUNE_PICKUP, 3, 0),
            # The bottle event can come a tick after the rune leaves.
            (300, "entity", bounty, DELETED),
            (301, "chat", CHAT_MESSAGE_RUNE_BOTTLE, 6, 5),
            # Used later: a pickup that removes no rune of its own.
            (900, "chat", CHAT_MESSAGE_RUNE_PICKUP, 6, 5),
            # Replaced at the next spawn: removed with no chat event.
            (400, "entity", haste, DELETED),
            (450, "entity", invis, CREATED),
            (600, "entity", invis, DELETED),
            (600, "chat", CHAT_MESSAGE_RUNE_DENY, 2, 3),
            (700, "entity", shield, CREATED),
        ]
    )
    assert [(r.rune_type, r.outcome, r.player_id, r.end_tick, r.used_tick) for r in runes] == [
        (0, "picked_up", 3, 200, None),
        (5, "bottled", 6, 300, 900),
        (1, "not_taken", None, 400, None),
        (3, "denied", 2, 600, None),
        (9, "still_there", None, None, None),
    ]
    assert (runes[1].x, runes[1].y, runes[1].spawn_tick) == (15388.0, 20815.0, 100)


def test_runes_take_a_recycled_slot_and_stacked_bounties(run) -> None:
    first, again = _Entity(7, 5, (16979.0, 11724.0)), _Entity(7, 5, (16979.0, 11724.0))
    older = _Entity(8, 5, (16950.0, 11700.0))
    runes = run(
        [
            (100, "entity", first, CREATED),
            (150, "entity", first, DELETED),
            (150, "chat", CHAT_MESSAGE_RUNE_PICKUP, 0, 5),
            # The same slot comes back without CREATED.
            (200, "entity", again, REENTERED),
            (210, "entity", older, CREATED),
            # Two bounties taken together, two ticks apart: each its own rune.
            (500, "entity", again, DELETED),
            (502, "entity", older, DELETED),
            (500, "chat", CHAT_MESSAGE_RUNE_PICKUP, 4, 5),
            (502, "chat", CHAT_MESSAGE_RUNE_PICKUP, 4, 5),
        ]
    )
    assert [(r.spawn_tick, r.end_tick, r.player_id) for r in runes] == [
        (100, 150, 0),
        (200, 500, 4),
        (210, 502, 4),
    ]


def test_runes_pair_nearby_events_as_a_group(run) -> None:
    # Removals at 100 and 102, pickups at 102 and 104: nearest-first would give
    # the 102 rune to the first pickup and leave the second without one.
    first, second = _Entity(1, 5, (16979.0, 11724.0)), _Entity(2, 5, (8000.0, 8000.0))
    runes = run(
        [
            (10, "entity", first, CREATED),
            (20, "entity", second, CREATED),
            (100, "entity", first, DELETED),
            (102, "entity", second, DELETED),
            (102, "chat", CHAT_MESSAGE_RUNE_PICKUP, 1, 5),
            (104, "chat", CHAT_MESSAGE_RUNE_PICKUP, 7, 5),
        ]
    )
    assert [(r.end_tick, r.outcome, r.player_id) for r in runes] == [
        (100, "picked_up", 1),
        (102, "picked_up", 7),
    ]


def test_runes_ignore_wisdom_runes_and_other_chat_events(run) -> None:
    runes = run(
        [
            (100, "chat", CHAT_MESSAGE_RUNE_PICKUP, 1, 8),  # a wisdom rune: no entity
            (100, "chat", 0, 1, 0),
        ]
    )
    assert runes == []


@pytest.mark.integration
@pytest.mark.slow
def test_runes_account_for_every_rune_pickup_on_a_replay(canonical_parsed_match) -> None:
    match = canonical_parsed_match
    pickups = sorted(
        (e.tick, e.value)
        for e in match.combat_log
        if e.log_type == "PICKUP_RUNE" and e.rune_type != 8  # wisdom runes are no entity
    )
    # Each pickup either removed a rune (taken) or used a bottled one.
    explained = sorted(
        [(r.end_tick, r.player_id) for r in match.runes if r.outcome == "picked_up"]
        + [(r.used_tick, r.player_id) for r in match.runes if r.used_tick is not None]
    )
    assert len(explained) == len(pickups)
    assert all(
        abs(a[0] - b[0]) <= 2 and a[1] == b[1] for a, b in zip(explained, pickups, strict=True)
    )
    assert all(r.rune_type >= 0 and r.x is not None for r in match.runes)
    assert {r.outcome for r in match.runes} <= {
        "picked_up",
        "bottled",
        "denied",
        "not_taken",
        "still_there",
    }
