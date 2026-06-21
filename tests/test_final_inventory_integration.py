"""Integration test: end-of-game final inventory matches OpenDota.

Parses one full OpenDota fixture and checks that each player's
``ParsedPlayer.final_items`` (slots 0-5, the main inventory read from the hero
entity at the game-end tick) matches OpenDota's ``item_0``-``item_5`` for the
same hero. gem stores ``item_``-prefixed names; OpenDota stores numeric item
IDs, so the comparison maps OpenDota IDs to internal keys via
``catalog.item_key_by_id``.

Marked ``slow`` + ``integration`` — needs a real ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import gem
from gem.catalog.heroes import HEROES
from gem.catalog.items import item_key_by_id

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
_MATCH_ID = 8855188139

_NAME_TO_HERO_ID = {name: meta["id"] for name, meta in HEROES.items()}


def _od_main_inventory_keys(od_player: dict) -> list[str | None]:
    """Return slots 0-5 of an OpenDota player as internal item keys (or None)."""
    keys: list[str | None] = []
    for slot in range(6):
        item_id = od_player.get(f"item_{slot}")
        keys.append(item_key_by_id(item_id) if item_id else None)
    return keys


def _gem_main_inventory_keys(player: gem.ParsedPlayer) -> list[str | None]:
    """Return slots 0-5 of a ParsedPlayer as internal item keys (or None)."""
    keys: list[str | None] = []
    for slot in range(6):
        name = player.final_items.get(slot)
        keys.append(name.removeprefix("item_") if name else None)
    return keys


@pytest.mark.slow
@pytest.mark.integration
class TestFinalInventoryMatchesOpenDota:
    @pytest.fixture(scope="class")
    def comparison(self):
        """Parse the fixture once and pair each player with OpenDota by hero.

        Returns:
            List of ``(hero_name, gem_keys, od_keys)`` tuples for slots 0-5.
        """
        dem = FIXTURES_DIR / f"{_MATCH_ID}.dem"
        od_path = FIXTURES_DIR / f"{_MATCH_ID}.opendota.json"
        if not dem.exists() or not od_path.exists():
            pytest.skip(f"OpenDota fixture {_MATCH_ID} (.dem + .opendota.json) not available")

        match = gem.parse(str(dem))
        with open(od_path) as fh:
            od = json.load(fh)
        od_by_hero = {p["hero_id"]: p for p in od.get("players") or []}

        rows: list[tuple[str, list[str | None], list[str | None]]] = []
        for player in match.players:
            hero_id = _NAME_TO_HERO_ID.get(player.hero_name)
            od_player = od_by_hero.get(hero_id)
            if od_player is None:
                continue
            rows.append(
                (
                    player.hero_name,
                    _gem_main_inventory_keys(player),
                    _od_main_inventory_keys(od_player),
                )
            )
        return rows

    def test_all_players_paired(self, comparison):
        assert len(comparison) == 10

    def test_final_inventory_matches_opendota(self, comparison):
        mismatches = [
            (hero, gem_keys, od_keys)
            for hero, gem_keys, od_keys in comparison
            if gem_keys != od_keys
        ]
        assert not mismatches, f"final inventory diverged from OpenDota: {mismatches}"

    def test_inventory_is_non_empty(self, comparison):
        # Guards against the silent name-index regression (empty inventory for
        # everyone): every player in a finished pro game holds at least one item.
        assert all(any(gem_keys) for _, gem_keys, _ in comparison)
