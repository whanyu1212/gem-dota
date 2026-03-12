"""Tests for gem.combat_aggregator.

Covers _ParsedPlayerAgg structure and _CombatAggregator routing/accumulation.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import fields
from unittest.mock import MagicMock

from gem.combat_aggregator import _CombatAggregator, _ParsedPlayerAgg

# ---------------------------------------------------------------------------
# _ParsedPlayerAgg
# ---------------------------------------------------------------------------


class TestParsedPlayerAgg:
    def test_counter_fields_are_defaultdict(self):
        agg = _ParsedPlayerAgg()
        for attr in (
            "damage",
            "damage_taken",
            "healing",
            "ability_uses",
            "item_uses",
            "gold_reasons",
            "xp_reasons",
        ):
            assert isinstance(getattr(agg, attr), defaultdict), f"{attr} should be defaultdict"

    def test_missing_key_returns_zero(self):
        agg = _ParsedPlayerAgg()
        assert agg.damage["unknown_hero"] == 0

    def test_increment_without_prior_set(self):
        agg = _ParsedPlayerAgg()
        agg.ability_uses["spell"] += 1
        agg.ability_uses["spell"] += 1
        assert agg.ability_uses["spell"] == 2

    def test_log_fields_are_lists(self):
        agg = _ParsedPlayerAgg()
        for attr in ("kills_log", "purchase_log", "runes_log", "buyback_log"):
            assert isinstance(getattr(agg, attr), list), f"{attr} should be list"

    def test_stuns_dealt_starts_zero(self):
        assert _ParsedPlayerAgg().stuns_dealt == 0.0

    def test_is_dataclass_with_slots(self):
        assert hasattr(_ParsedPlayerAgg, "__slots__")
        assert len(fields(_ParsedPlayerAgg)) > 0

    def test_independent_instances_do_not_share_state(self):
        a, b = _ParsedPlayerAgg(), _ParsedPlayerAgg()
        a.damage["hero"] += 999
        assert b.damage["hero"] == 0


# ---------------------------------------------------------------------------
# _CombatAggregator
# ---------------------------------------------------------------------------


def _make_agg(player_id_raw: int = 0) -> tuple[_CombatAggregator, MagicMock]:
    """Return a _CombatAggregator wired to a single fake hero entity."""
    player_ext = MagicMock()
    hero_entity = MagicMock()
    hero_entity.get_int32.return_value = (player_id_raw, True)
    player_ext._heroes_by_npc = {"npc_dota_hero_axe": hero_entity}
    return _CombatAggregator(player_ext), hero_entity


def _entry(**kwargs) -> MagicMock:
    defaults = {
        "log_type": "DAMAGE",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_mirana",
        "attacker_is_hero": True,
        "target_is_hero": False,
        "inflictor_name": "",
        "value": 100,
        "gold_reason": 0,
        "xp_reason": 0,
        "stun_duration": 0.0,
    }
    defaults.update(kwargs)
    return MagicMock(**defaults)


class TestCombatAggregatorDamage:
    def test_damage_accumulates(self):
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(value=200))
        agg.on_entry(_entry(value=150))
        assert agg.players[0].damage["npc_dota_hero_mirana"] == 350

    def test_first_entry_no_keyerror(self):
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(value=999))  # must not raise
        assert agg.players[0].damage["npc_dota_hero_mirana"] == 999

    def test_damage_taken_on_target(self):
        player_ext = MagicMock()
        # attacker = axe (pid 0), target = mirana (pid 1)
        axe_entity = MagicMock()
        axe_entity.get_int32.return_value = (0, True)
        mirana_entity = MagicMock()
        mirana_entity.get_int32.return_value = (2, True)  # slot 1
        player_ext._heroes_by_npc = {
            "npc_dota_hero_axe": axe_entity,
            "npc_dota_hero_mirana": mirana_entity,
        }
        agg = _CombatAggregator(player_ext)
        e = _entry(attacker_is_hero=True, target_is_hero=True, value=100)
        agg.on_entry(e)
        assert agg.players[1].damage_taken["npc_dota_hero_axe"] == 100


class TestCombatAggregatorAbilityItem:
    def test_ability_uses_accumulate(self):
        agg, _ = _make_agg(0)
        for _ in range(3):
            agg.on_entry(_entry(log_type="ABILITY", inflictor_name="axe_berserkers_call"))
        assert agg.players[0].ability_uses["axe_berserkers_call"] == 3

    def test_item_uses_accumulate(self):
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(log_type="ITEM", inflictor_name="item_blink"))
        agg.on_entry(_entry(log_type="ITEM", inflictor_name="item_blink"))
        assert agg.players[0].item_uses["item_blink"] == 2


class TestCombatAggregatorGoldXP:
    def test_gold_reasons_accumulate(self):
        agg, _ = _make_agg(0)
        e = _entry(
            log_type="GOLD",
            attacker_is_hero=False,
            target_is_hero=False,
            target_name="npc_dota_hero_axe",
            gold_reason=6,
            value=50,
        )
        agg.on_entry(e)
        agg.on_entry(e)
        assert agg.players[0].gold_reasons["6"] == 100

    def test_xp_reasons_accumulate(self):
        agg, _ = _make_agg(0)
        e = _entry(
            log_type="XP",
            attacker_is_hero=False,
            target_is_hero=False,
            target_name="npc_dota_hero_axe",
            xp_reason=0,
            value=200,
        )
        agg.on_entry(e)
        assert agg.players[0].xp_reasons["0"] == 200


class TestCombatAggregatorRunes:
    def test_rune_pickup_goes_to_correct_slot(self):
        agg, _ = _make_agg(0)
        e = _entry(log_type="PICKUP_RUNE", attacker_is_hero=False, value=4)
        agg.on_entry(e)
        assert len(agg.players[4].runes_log) == 1

    def test_rune_out_of_range_ignored(self):
        agg, _ = _make_agg(0)
        e = _entry(log_type="PICKUP_RUNE", attacker_is_hero=False, value=10)
        agg.on_entry(e)
        assert 10 not in agg.players
