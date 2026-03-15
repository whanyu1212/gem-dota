"""Tests for gem.combat_aggregator.

Covers _ParsedPlayerAgg structure, _CombatAggregator routing/accumulation,
and _dedup_purchase_log deduplication logic.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import fields
from unittest.mock import MagicMock

from gem.combat_aggregator import _CombatAggregator, _dedup_purchase_log, _ParsedPlayerAgg
from gem.combatlog import CombatLogEntry

# ---------------------------------------------------------------------------
# _ParsedPlayerAgg
# ---------------------------------------------------------------------------


class TestParsedPlayerAgg:
    def test_counter_fields_are_defaultdict(self):
        agg = _ParsedPlayerAgg()
        for attr in (
            "damage",
            "damage_taken",
            "damage_by_type",
            "damage_taken_by_type",
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
    hero_entity.get_int32.return_value = player_id_raw
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
        "damage_type": "",
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
        axe_entity.get_int32.return_value = 0
        mirana_entity = MagicMock()
        mirana_entity.get_int32.return_value = 2  # slot 1
        player_ext._heroes_by_npc = {
            "npc_dota_hero_axe": axe_entity,
            "npc_dota_hero_mirana": mirana_entity,
        }
        agg = _CombatAggregator(player_ext)
        e = _entry(attacker_is_hero=True, target_is_hero=True, value=100)
        agg.on_entry(e)
        assert agg.players[1].damage_taken["npc_dota_hero_axe"] == 100

    def test_damage_by_type_accumulates_for_attacker(self):
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(value=120, damage_type="physical"))
        agg.on_entry(_entry(value=80, damage_type="magical"))
        agg.on_entry(_entry(value=30, damage_type="physical"))
        assert agg.players[0].damage_by_type["physical"] == 150
        assert agg.players[0].damage_by_type["magical"] == 80

    def test_damage_taken_by_type_accumulates_for_target(self):
        player_ext = MagicMock()
        axe_entity = MagicMock()
        axe_entity.get_int32.return_value = 0
        mirana_entity = MagicMock()
        mirana_entity.get_int32.return_value = 2  # slot 1
        player_ext._heroes_by_npc = {
            "npc_dota_hero_axe": axe_entity,
            "npc_dota_hero_mirana": mirana_entity,
        }
        agg = _CombatAggregator(player_ext)
        agg.on_entry(
            _entry(
                attacker_is_hero=True,
                target_is_hero=True,
                value=90,
                damage_type="pure",
            )
        )
        assert agg.players[1].damage_taken_by_type["pure"] == 90


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


class TestDamageTypeConsistency:
    """Verify damage_by_type sum tallies with total accumulated damage."""

    def test_damage_by_type_sums_to_total_damage(self):
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(value=120, damage_type="physical"))
        agg.on_entry(_entry(value=80, damage_type="magical"))
        agg.on_entry(_entry(value=50, damage_type="pure"))
        player = agg.players[0]
        total_damage = sum(player.damage.values())
        total_by_type = sum(player.damage_by_type.values())
        assert total_by_type == total_damage, (
            f"damage_by_type sum ({total_by_type}) != total damage ({total_damage})"
        )

    def test_empty_damage_type_excluded_from_by_type(self):
        """Entries with no damage_type (empty string) don't pollute damage_by_type."""
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(value=100, damage_type="physical"))
        agg.on_entry(_entry(value=200, damage_type=""))  # untyped entry
        player = agg.players[0]
        total_damage = sum(player.damage.values())
        total_by_type = sum(player.damage_by_type.values())
        assert total_damage == 300
        assert total_by_type == 100  # only the typed entry counted
        assert "" not in player.damage_by_type

    def test_damage_taken_by_type_sums_to_total_taken(self):
        player_ext = MagicMock()
        axe_entity = MagicMock()
        axe_entity.get_int32.return_value = 0
        mirana_entity = MagicMock()
        mirana_entity.get_int32.return_value = 2  # slot 1
        player_ext._heroes_by_npc = {
            "npc_dota_hero_axe": axe_entity,
            "npc_dota_hero_mirana": mirana_entity,
        }
        agg = _CombatAggregator(player_ext)
        for dmg_type, val in [("physical", 200), ("magical", 150), ("pure", 50)]:
            agg.on_entry(
                _entry(attacker_is_hero=True, target_is_hero=True, value=val, damage_type=dmg_type)
            )
        target = agg.players[1]
        assert sum(target.damage_taken.values()) == sum(target.damage_taken_by_type.values())


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


# ---------------------------------------------------------------------------
# _dedup_purchase_log
# ---------------------------------------------------------------------------


def _purchase(tick: int, item: str) -> CombatLogEntry:
    return CombatLogEntry(tick=tick, log_type="PURCHASE", value_name=item)


class TestDedupPurchaseLog:
    def test_no_first_snap_returns_sorted(self):
        entries = [_purchase(300, "item_branches"), _purchase(100, "item_tango")]
        result = _dedup_purchase_log(entries, first_snap_tick=None, sample_interval=150)
        assert [e.tick for e in result] == [100, 300]

    def test_duplicate_within_window_removed(self):
        # first_snap_tick=100, sample_interval=150 → cutoff=250
        entries = [
            _purchase(100, "item_branches"),
            _purchase(100, "item_branches"),  # duplicate at same tick+item
        ]
        result = _dedup_purchase_log(entries, first_snap_tick=100, sample_interval=150)
        assert len(result) == 1

    def test_duplicate_outside_window_kept(self):
        # cutoff = 100 + 150 = 250; tick 300 > 250 → both entries kept
        entries = [
            _purchase(100, "item_branches"),
            _purchase(300, "item_branches"),  # same item but beyond cutoff
        ]
        result = _dedup_purchase_log(entries, first_snap_tick=100, sample_interval=150)
        assert len(result) == 2

    def test_different_items_at_same_tick_both_kept(self):
        entries = [
            _purchase(100, "item_tango"),
            _purchase(100, "item_branches"),
        ]
        result = _dedup_purchase_log(entries, first_snap_tick=100, sample_interval=150)
        assert len(result) == 2

    def test_empty_list_returns_empty(self):
        assert _dedup_purchase_log([], first_snap_tick=100, sample_interval=150) == []

    def test_result_sorted_by_tick(self):
        entries = [_purchase(500, "item_tango"), _purchase(200, "item_branches")]
        result = _dedup_purchase_log(entries, first_snap_tick=100, sample_interval=150)
        assert result[0].tick == 200
        assert result[1].tick == 500

    def test_cutoff_boundary_entry_is_deduplicated(self):
        # Entry at exactly cutoff tick (100+150=250) is still inside window
        entries = [
            _purchase(250, "item_tango"),
            _purchase(250, "item_tango"),
        ]
        result = _dedup_purchase_log(entries, first_snap_tick=100, sample_interval=150)
        assert len(result) == 1

    def test_entry_just_beyond_cutoff_is_kept(self):
        # Entry at 251 > cutoff=250 → not deduplicated
        entries = [
            _purchase(250, "item_tango"),
            _purchase(251, "item_tango"),
        ]
        result = _dedup_purchase_log(entries, first_snap_tick=100, sample_interval=150)
        assert len(result) == 2
