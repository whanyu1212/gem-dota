"""Tests for gem.combat.aggregator.

Covers _ParsedPlayerAgg structure and _CombatAggregator routing/accumulation.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import fields
from types import SimpleNamespace
from unittest.mock import MagicMock

from gem.combat.aggregator import _CombatAggregator, _ParsedPlayerAgg
from gem.state.entities import Entity

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


def _hero_entity(player_id_raw: int) -> Entity:
    """Return a real entity with a flat player-ID overlay."""
    entity = Entity(
        index=0,
        serial=0,
        cls=SimpleNamespace(name="CDOTA_Unit_Hero", class_id=0, serializer=None),
    )
    entity._state["m_nPlayerID"] = player_id_raw
    return entity


def _make_agg(player_id_raw: int = 0) -> tuple[_CombatAggregator, Entity]:
    """Return a _CombatAggregator wired to a single fake hero entity."""
    player_ext = MagicMock()
    # No entity manager in unit tests -> the summon->owner resolution path no-ops
    # cleanly (it returns None when ``_parser`` is None) instead of dereferencing
    # auto-generated MagicMock attributes.
    player_ext._parser = None
    hero_entity = _hero_entity(player_id_raw)
    player_ext._heroes_by_npc = {"npc_dota_hero_axe": hero_entity}
    return _CombatAggregator(player_ext), hero_entity


def _entry(**kwargs) -> MagicMock:
    defaults = {
        "log_type": "DAMAGE",
        "attacker_name": "npc_dota_hero_axe",
        # Default the damage source to the attacker (the common auto-attack case);
        # tests that exercise summon/spell attribution override it explicitly.
        "damage_source_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_mirana",
        "attacker_is_hero": True,
        "target_is_hero": False,
        "attacker_is_illusion": False,
        "target_is_illusion": False,
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

    def test_unknown_log_type_does_not_accumulate_damage(self):
        # Proto types the parser does not model arrive as UNKNOWN (not DAMAGE),
        # so the match statement falls through and they never inflate the damage
        # aggregates. Guards against the CRITICAL_DAMAGE/MODIFIER_STACK_EVENT
        # double-counting regression. (A DAMAGE entry with the same fields would
        # have populated agg.players[0].damage; UNKNOWN must not.)
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(log_type="UNKNOWN", target_is_hero=True, value=500))
        if 0 in agg.players:
            assert agg.players[0].damage["npc_dota_hero_mirana"] == 0
            assert agg.players[0].hero_damage == 0

        # Control: the identical entry as DAMAGE *does* accumulate, proving the
        # UNKNOWN no-op above is the label's doing, not an unrelated filter.
        agg2, _ = _make_agg(0)
        agg2.on_entry(_entry(log_type="DAMAGE", target_is_hero=True, value=500))
        assert agg2.players[0].damage["npc_dota_hero_mirana"] == 500

    def test_damage_taken_on_target(self):
        player_ext = MagicMock()
        # attacker = axe (pid 0), target = mirana (pid 1)
        axe_entity = _hero_entity(0)
        mirana_entity = _hero_entity(2)  # slot 1
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
        axe_entity = _hero_entity(0)
        mirana_entity = _hero_entity(2)  # slot 1
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


class TestCombatAggregatorCombatScalars:
    """OpenDota-style hero_damage / tower_damage / hero_healing reconstruction."""

    def test_hero_damage_counts_hero_target(self):
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(target_is_hero=True, value=200))
        assert agg.players[0].hero_damage == 200

    def test_hero_damage_excludes_illusion_target(self):
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(target_is_hero=True, target_is_illusion=True, value=200))
        assert agg.players[0].hero_damage == 0

    def test_hero_damage_counts_all_damage_types(self):
        # OpenDota's per-target damage dict (and thus the parse-only scalar) applies
        # no damage_type filter; crediting the source already keeps absorbed/return
        # ("others") instances from inflating a hero's total, so they are counted
        # like any other source-attributed hero damage. Verified against fixtures.
        agg, _ = _make_agg(0)
        agg.on_entry(_entry(target_is_hero=True, damage_type="others", value=120))
        assert agg.players[0].hero_damage == 120

    def test_hero_damage_excludes_non_hero_target(self):
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(target_is_hero=False, target_name="npc_dota_creep_badguys_melee", value=50)
        )
        assert agg.players[0].hero_damage == 0

    def test_tower_damage_counts_structures(self):
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(target_is_hero=False, target_name="npc_dota_badguys_tower1_mid", value=100)
        )
        agg.on_entry(
            _entry(target_is_hero=False, target_name="npc_dota_badguys_melee_rax_mid", value=80)
        )
        agg.on_entry(_entry(target_is_hero=False, target_name="npc_dota_badguys_fort", value=60))
        assert agg.players[0].tower_damage == 240

    def test_tower_damage_ignores_creeps(self):
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(target_is_hero=False, target_name="npc_dota_creep_goodguys_ranged", value=40)
        )
        assert agg.players[0].tower_damage == 0

    def test_hero_healing_excludes_self(self):
        agg, _ = _make_agg(0)
        # heal an ally hero -> counts; heal self -> excluded.
        agg.on_entry(
            _entry(
                log_type="HEAL",
                target_is_hero=True,
                target_name="npc_dota_hero_mirana",
                value=300,
            )
        )
        agg.on_entry(
            _entry(
                log_type="HEAL",
                target_is_hero=True,
                target_name="npc_dota_hero_axe",  # self (source is axe)
                value=500,
            )
        )
        assert agg.players[0].hero_healing == 300


class TestCombatAggregatorSourceAttribution:
    """Damage/heal is credited to ``damage_source_name``, not ``attacker_name``.

    Mirrors OpenDota's ``handleDamageCombat`` (``unit = e.sourcename``): summon /
    spell / projectile damage lands on the owning hero even when the combat-log
    attacker is the summon. This is what closes the tower_damage residual
    (87% -> ~exact) and aligns gem's per-target dicts with OpenDota's.
    """

    def test_damage_credited_to_source_not_attacker(self):
        # attacker is a non-hero summon; source is the owning hero (axe).
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(
                attacker_name="npc_dota_lone_druid_bear",
                attacker_is_hero=False,
                damage_source_name="npc_dota_hero_axe",
                target_is_hero=True,
                target_name="npc_dota_hero_mirana",
                value=200,
            )
        )
        assert agg.players[0].damage["npc_dota_hero_mirana"] == 200
        assert agg.players[0].hero_damage == 200

    def test_tower_damage_credited_to_source(self):
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(
                attacker_name="npc_dota_lone_druid_bear",
                attacker_is_hero=False,
                damage_source_name="npc_dota_hero_axe",
                target_is_hero=False,
                target_name="npc_dota_badguys_tower1_mid",
                value=150,
            )
        )
        assert agg.players[0].tower_damage == 150

    def test_damage_taken_keyed_by_source(self):
        player_ext = MagicMock()
        player_ext._parser = None
        axe_entity = _hero_entity(0)
        mirana_entity = _hero_entity(2)  # slot 1
        player_ext._heroes_by_npc = {
            "npc_dota_hero_axe": axe_entity,
            "npc_dota_hero_mirana": mirana_entity,
        }
        agg = _CombatAggregator(player_ext)
        agg.on_entry(
            _entry(
                attacker_name="npc_dota_lone_druid_bear",
                attacker_is_hero=False,
                damage_source_name="npc_dota_hero_axe",
                target_is_hero=True,
                target_name="npc_dota_hero_mirana",
                value=90,
            )
        )
        # damage_taken is keyed by the source unit (axe), not the projectile/summon.
        assert agg.players[1].damage_taken["npc_dota_hero_axe"] == 90

    def test_falls_back_to_attacker_when_source_empty(self):
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(
                attacker_name="npc_dota_hero_axe",
                damage_source_name="",  # unset source -> fall back to attacker
                target_is_hero=True,
                target_name="npc_dota_hero_mirana",
                value=75,
            )
        )
        assert agg.players[0].hero_damage == 75

    def test_illusion_target_keyed_separately(self):
        # An illusion target is keyed "illusion_<hero>" (OpenDota computeIllusionString),
        # so the real hero's damage key is not inflated by illusion damage.
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(
                target_is_hero=True,
                target_is_illusion=True,
                target_name="npc_dota_hero_mirana",
                value=120,
            )
        )
        assert agg.players[0].damage["illusion_npc_dota_hero_mirana"] == 120
        assert agg.players[0].damage["npc_dota_hero_mirana"] == 0
        # illusion targets are excluded from the hero_damage scalar.
        assert agg.players[0].hero_damage == 0

    def test_non_unit_target_excluded_from_damage_dict(self):
        # Valve logs some absorb/redirect interactions against an ability/modifier
        # name rather than a unit; OpenDota's damage dict excludes these.
        agg, _ = _make_agg(0)
        agg.on_entry(
            _entry(
                target_is_hero=False,
                target_name="nevermore_necromastery",
                value=10,
            )
        )
        # The entry is skipped entirely — no damage recorded under the junk key
        # (and no aggregate need have been created for the player at all).
        player = agg.players.get(0)
        assert player is None or "nevermore_necromastery" not in player.damage


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
        axe_entity = _hero_entity(0)
        mirana_entity = _hero_entity(2)  # slot 1
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


class TestSummonKillAttribution:
    """DEATH kills by summons credit the owner; ward self-expiry does not."""

    def _agg_with_summon_owner(self, summon_name: str, owner_slot_raw: int = 0):
        """Wire an aggregator whose entity manager resolves ``summon_name`` to an
        owner hero at player slot ``owner_slot_raw // 2``.
        """
        player_ext = MagicMock()
        parser = MagicMock()
        em = MagicMock()
        summon_entity = MagicMock()
        summon_entity.get_uint32.return_value = 12345  # owner handle
        owner_entity = _hero_entity(owner_slot_raw)

        def _find_by_npc_name(name):
            return summon_entity if name == summon_name else None

        em.find_by_npc_name.side_effect = _find_by_npc_name
        em.find_by_handle.return_value = owner_entity
        parser.entity_manager = em
        player_ext._parser = parser
        player_ext._heroes_by_npc = {}
        return _CombatAggregator(player_ext)

    def _death(self, attacker, target):
        return _entry(
            log_type="DEATH",
            attacker_name=attacker,
            attacker_is_hero=False,
            damage_source_name="",
            target_name=target,
            target_is_hero=False,
            value=0,
        )

    def test_summon_kill_credited_to_owner(self):
        agg = self._agg_with_summon_owner("npc_dota_lone_druid_bear", owner_slot_raw=0)
        agg.on_entry(self._death("npc_dota_lone_druid_bear", "npc_dota_creep_badguys_melee"))
        assert len(agg.players[0].kills_log) == 1
        assert agg.players[0].kills_log[0].target_name == "npc_dota_creep_badguys_melee"

    def test_summon_death_prefers_damage_source_hero(self):
        agg, _ = _make_agg(player_id_raw=0)
        agg.on_entry(self._death("npc_dota_beastmaster_boar", "npc_dota_creep_badguys_melee"))
        assert agg.players.get(0) is None

        agg.on_entry(
            _entry(
                log_type="DEATH",
                attacker_name="npc_dota_beastmaster_boar",
                attacker_is_hero=False,
                damage_source_name="npc_dota_hero_axe",
                target_name="npc_dota_creep_badguys_melee",
                target_is_hero=False,
                value=0,
            )
        )

        assert len(agg.players[0].kills_log) == 1
        assert agg.players[0].kills_log[0].target_name == "npc_dota_creep_badguys_melee"

    def test_self_death_with_source_hero_not_credited(self):
        agg, _ = _make_agg(player_id_raw=0)
        agg.on_entry(
            _entry(
                log_type="DEATH",
                attacker_name="npc_dota_sentry_wards",
                attacker_is_hero=False,
                damage_source_name="npc_dota_hero_axe",
                target_name="npc_dota_sentry_wards",
                target_is_hero=False,
                value=0,
            )
        )

        assert agg.players.get(0) is None

    def test_ward_self_expiry_not_credited_to_placer(self):
        # A ward expiring is a DEATH whose attacker is the ward itself. Even if the
        # ward would resolve to a placer, it must NOT be appended to kills_log.
        agg = self._agg_with_summon_owner("npc_dota_observer_wards", owner_slot_raw=0)
        agg.on_entry(self._death("npc_dota_observer_wards", "npc_dota_observer_wards"))
        # The expiry was not attributed to any player, so no agg/kills_log exists.
        assert agg.players.get(0) is None or agg.players[0].kills_log == []


# ---------------------------------------------------------------------------
# Per-inflictor / per-target attribution (OpenDota parity)
# ---------------------------------------------------------------------------


def _two_hero_agg() -> _CombatAggregator:
    """Aggregator with axe (pid 0) and mirana (pid 1) as resolvable heroes."""
    player_ext = MagicMock()
    player_ext._parser = None
    axe = _hero_entity(0)  # raw // 2 -> slot 0
    mirana = _hero_entity(2)  # raw // 2 -> slot 1
    player_ext._heroes_by_npc = {
        "npc_dota_hero_axe": axe,
        "npc_dota_hero_mirana": mirana,
    }
    return _CombatAggregator(player_ext)


def _hero_dmg(**kwargs) -> MagicMock:
    """A DAMAGE entry from axe (source hero) onto mirana (enemy hero)."""
    defaults = {
        "log_type": "DAMAGE",
        "attacker_name": "npc_dota_hero_axe",
        "damage_source_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_mirana",
        "attacker_is_hero": True,
        "target_is_hero": True,
        "attacker_is_illusion": False,
        "target_is_illusion": False,
        "inflictor_name": "axe_culling_blade",
        "value": 100,
        "gold_reason": 0,
        "xp_reason": 0,
        "damage_type": "",
        "stun_duration": 0.0,
        "game_time_s": 60,
        "timestamp_s": 60.0,
    }
    defaults.update(kwargs)
    return MagicMock(**defaults)


class TestInflictorDicts:
    def test_damage_inflictor_and_targets_and_hits(self):
        agg = _two_hero_agg()
        agg.on_entry(_hero_dmg(value=100))
        agg.on_entry(_hero_dmg(value=50))
        p = agg.players[0]
        assert p.damage_inflictor["axe_culling_blade"] == 150
        assert p.damage_targets["axe_culling_blade"]["npc_dota_hero_mirana"] == 150
        assert p.hero_hits["axe_culling_blade"] == 2  # counts instances, not damage

    def test_item_prefix_stripped_in_inflictor_key(self):
        agg = _two_hero_agg()
        agg.on_entry(_hero_dmg(inflictor_name="item_dagon", value=400))
        assert agg.players[0].damage_inflictor["dagon"] == 400  # item_ stripped

    def test_auto_attack_keyed_null(self):
        # Empty inflictor (auto-attack) is keyed "null" to match OpenDota's JSON.
        agg = _two_hero_agg()
        agg.on_entry(_hero_dmg(inflictor_name="", value=70))
        assert agg.players[0].damage_inflictor["null"] == 70
        assert agg.players[0].hero_hits["null"] == 1

    def test_dota_unknown_inflictor_dropped(self):
        agg = _two_hero_agg()
        agg.on_entry(_hero_dmg(inflictor_name="dota_unknown", value=70))
        # dota_unknown is dropped entirely (no key), matching OpenDota's translate.
        assert "dota_unknown" not in agg.players[0].damage_inflictor
        assert agg.players[0].damage_inflictor.get(None) is None

    def test_max_hero_hit_tracks_largest(self):
        agg = _two_hero_agg()
        agg.on_entry(_hero_dmg(value=100, game_time_s=10))
        agg.on_entry(_hero_dmg(value=350, game_time_s=20, inflictor_name="axe_battle_hunger"))
        agg.on_entry(_hero_dmg(value=80, game_time_s=30))
        mhh = agg.players[0].max_hero_hit
        assert mhh is not None
        assert mhh["value"] == 350
        assert mhh["inflictor"] == "axe_battle_hunger"
        assert mhh["unit"] == "npc_dota_hero_axe"
        assert mhh["key"] == "npc_dota_hero_mirana"
        assert mhh["time"] == 20

    def test_non_hero_target_excluded(self):
        # Damage to a creep must NOT populate the inflictor breakdowns.
        agg = _two_hero_agg()
        agg.on_entry(
            _hero_dmg(target_name="npc_dota_creep_badguys_melee", target_is_hero=False, value=50)
        )
        assert agg.players.get(0) is None or agg.players[0].damage_inflictor == {}

    def test_illusion_target_excluded_from_inflictor(self):
        # Damage to an illusion is excluded from the inflictor breakdowns
        # (OpenDota gates on !targetillusion).
        agg = _two_hero_agg()
        agg.on_entry(_hero_dmg(target_is_illusion=True, value=50))
        assert agg.players.get(0) is None or agg.players[0].damage_inflictor == {}

    def test_self_damage_excluded_from_inflictor(self):
        # Self-inflicted damage (target == source) is excluded from
        # damage_inflictor / max_hero_hit (OpenDota's !key.equals(unit)) but still
        # counts toward damage_targets / hero_hits.
        agg = _two_hero_agg()
        agg.on_entry(
            _hero_dmg(target_name="npc_dota_hero_axe", inflictor_name="axe_berserkers_call")
        )
        p = agg.players[0]
        assert p.damage_inflictor == {}  # self-damage excluded
        assert p.max_hero_hit is None
        assert p.hero_hits["axe_berserkers_call"] == 1  # but hits still counted

    def test_damage_inflictor_received_only_from_enemy_hero(self):
        # The victim records damage_inflictor_received keyed by the enemy's
        # inflictor, only when the source is a hero.
        agg = _two_hero_agg()
        agg.on_entry(_hero_dmg(value=120, inflictor_name="axe_culling_blade"))
        assert agg.players[1].damage_inflictor_received["axe_culling_blade"] == 120

    def test_ability_targets_nested(self):
        agg = _two_hero_agg()
        agg.on_entry(
            _hero_dmg(
                log_type="ABILITY",
                inflictor_name="axe_battle_hunger",
                target_name="npc_dota_hero_mirana",
                target_is_hero=True,
            )
        )
        p = agg.players[0]
        assert p.ability_uses["axe_battle_hunger"] == 1
        assert p.ability_targets["axe_battle_hunger"]["npc_dota_hero_mirana"] == 1
