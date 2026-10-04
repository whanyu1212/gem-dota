"""Tests for gem.analysis.fight_timeline.

Unit tests build synthetic combat logs; the integration test reads a real fixture.
"""

from __future__ import annotations

import bisect

import pytest

from gem.analysis.fight_timeline import (
    CastHit,
    KillRewards,
    build_fight_timeline,
    modifier_matches_ability,
)
from gem.combat.log import CombatLogEntry
from gem.results.models import BuybackEvent, ParsedMatch, ParsedPlayer

TINY = "npc_dota_hero_tiny"
LION = "npc_dota_hero_lion"
AXE = "npc_dota_hero_axe"
SF = "npc_dota_hero_nevermore"
GOLEM = "npc_dota_necronomicon_warrior_3"


def _match(log: list[CombatLogEntry], **buybacks: list[BuybackEvent]) -> ParsedMatch:
    players = [
        ParsedPlayer(player_id=slot, hero_name=hero, team=2 if slot < 5 else 3)
        for slot, hero in enumerate((TINY, LION, "", "", "", AXE, SF, "", "", ""))
    ]
    for player in players:
        player.buybacks = buybacks.get(player.hero_name.removeprefix("npc_dota_hero_"), [])
    return ParsedMatch(players=players, combat_log=sorted(log, key=lambda e: e.tick))


def _entry(
    log_type: str, tick: int, attacker: str = "", target: str = "", **fields
) -> CombatLogEntry:
    return CombatLogEntry(
        tick=tick,
        log_type=log_type,
        attacker_name=attacker,
        damage_source_name=fields.pop("source", attacker),
        target_name=target,
        **fields,
    )


def _cast(tick: int, caster: str, ability: str, target: str = "", **fields) -> CombatLogEntry:
    log_type = "ITEM" if ability.startswith("item_") else "ABILITY"
    return _entry(log_type, tick, caster, target, inflictor_name=ability, **fields)


def _damage(tick: int, attacker: str, target: str, value: int, ability: str = "", **fields):
    fields.setdefault("damage_type", "magical" if ability else "physical")
    return _entry("DAMAGE", tick, attacker, target, inflictor_name=ability, value=value, **fields)


def _modifier(log_type: str, tick: int, attacker: str, target: str, name: str, **fields):
    return _entry(log_type, tick, attacker, target, inflictor_name=name, **fields)


class TestModifierMatchesAbility:
    @pytest.mark.parametrize(
        ("modifier", "ability"),
        [
            ("modifier_lion_voodoo", "lion_voodoo"),
            ("modifier_sheepstick_debuff", "item_sheepstick"),
            ("modifier_black_king_bar_immune", "item_black_king_bar"),
            ("tiny_avalanche", "tiny_avalanche"),
        ],
    )
    def test_matches(self, modifier, ability):
        assert modifier_matches_ability(modifier, ability)

    @pytest.mark.parametrize(
        ("modifier", "ability"),
        [
            ("modifier_stunned", "tiny_avalanche"),
            ("lion_voodoo_extra", "lion_voodoo"),
            ("", "lion_voodoo"),
            ("modifier_lion_voodoo", ""),
        ],
    )
    def test_does_not_match(self, modifier, ability):
        assert not modifier_matches_ability(modifier, ability)


class TestCasts:
    def test_hits_carry_damage_and_debuffs_per_hero(self):
        log = [
            _cast(100, TINY, "tiny_avalanche"),
            _damage(110, TINY, AXE, 300, "tiny_avalanche"),
            _damage(112, TINY, AXE, 50, "tiny_avalanche"),
            _modifier(
                "MODIFIER_ADD", 110, TINY, SF, "modifier_tiny_avalanche_stun", stun_duration=1.2
            ),
            _damage(115, TINY, SF, 80),  # an attack: not part of the cast
        ]

        (cast,) = build_fight_timeline(_match(log), 0, 1000).casts

        assert cast.caster == TINY and cast.ability == "tiny_avalanche" and not cast.is_item
        assert cast.hits == (
            CastHit(AXE, 350, "magical"),
            CastHit(SF, 0, "", 1.2, ("modifier_tiny_avalanche_stun",)),
        )
        assert cast.damage == 350
        assert cast.target is None and cast.self_effect is None

    def test_self_buff_is_the_self_effect_not_a_hit(self):
        log = [
            _cast(100, SF, "item_black_king_bar"),
            _modifier("MODIFIER_ADD", 101, SF, SF, "modifier_black_king_bar_immune"),
        ]

        (cast,) = build_fight_timeline(_match(log), 0, 1000).casts

        assert cast.is_item
        assert cast.hits == ()
        assert cast.self_effect == CastHit(SF, modifiers=("modifier_black_king_bar_immune",))

    def test_recorded_target_is_kept_even_when_it_is_not_a_hero(self):
        log = [
            _cast(100, LION, "lion_voodoo", AXE, target_is_hero=True),
            _cast(200, TINY, "tiny_toss", "npc_dota_creep_badguys_melee"),
        ]

        hex_cast, toss = build_fight_timeline(_match(log), 0, 1000).casts

        assert (hex_cast.target, hex_cast.target_is_hero) == (AXE, True)
        assert (toss.target, toss.target_is_hero) == ("npc_dota_creep_badguys_melee", False)

    def test_each_hit_goes_to_the_latest_cast_of_its_ability(self):
        log = [
            _cast(100, SF, "nevermore_shadowraze1"),
            _damage(105, SF, AXE, 200, "nevermore_shadowraze1"),
            _cast(130, SF, "nevermore_shadowraze1"),
            _damage(135, SF, AXE, 220, "nevermore_shadowraze1"),
        ]

        first, second = build_fight_timeline(_match(log), 0, 1000).casts

        assert first.hits == (CastHit(AXE, 200, "magical"),)
        assert second.hits == (CastHit(AXE, 220, "magical"),)

    def test_damage_after_the_hit_window_is_only_in_the_damage_list(self):
        log = [
            _cast(100, AXE, "axe_battle_hunger"),
            _damage(150, AXE, TINY, 40, "axe_battle_hunger"),
            _damage(400, AXE, TINY, 40, "axe_battle_hunger"),
        ]

        timeline = build_fight_timeline(_match(log), 0, 1000)

        assert timeline.casts[0].hits == (CastHit(TINY, 40, "magical"),)
        assert sum(burst.damage for burst in timeline.damage) == 80

    def test_hits_from_a_unit_the_hero_controls_count_for_its_cast(self):
        remnant = "npc_dota_ember_spirit_remnant"
        log = [
            _cast(100, SF, "ember_spirit_activate_fire_remnant"),
            _damage(120, remnant, AXE, 180, "ember_spirit_activate_fire_remnant", source=SF),
            _damage(
                125, SF, TINY, 90, "ember_spirit_activate_fire_remnant", attacker_is_illusion=True
            ),
        ]

        (cast,) = build_fight_timeline(_match(log), 0, 1000).casts

        assert cast.hits == (CastHit(AXE, 180, "magical"),)

    def test_illusion_casts_are_left_out(self):
        log = [_cast(100, TINY, "tiny_avalanche", attacker_is_illusion=True)]

        assert build_fight_timeline(_match(log), 0, 1000).casts == ()


class TestDamage:
    def test_bursts_group_per_attacker_target_source_and_type(self):
        log = [
            _damage(100, TINY, AXE, 100),
            _damage(105, TINY, AXE, 120),
            _damage(110, TINY, AXE, 300, "tiny_avalanche"),
            _damage(130, TINY, AXE, 90),  # next half-second bucket
            _damage(100, "npc_dota_badguys_tower2_mid", TINY, 150),
        ]

        bursts = build_fight_timeline(_match(log), 0, 1000).damage

        attacks = [b for b in bursts if b.attacker == TINY and b.source == ""]
        assert [(b.start_tick, b.end_tick, b.damage, b.hits) for b in attacks] == [
            (100, 105, 220, 2),
            (130, 130, 90, 1),
        ]
        tower = next(b for b in bursts if b.target == TINY)
        assert tower.attacker_hero is None

    def test_summon_and_illusion_damage_is_credited_to_the_owner(self):
        log = [
            _damage(100, GOLEM, AXE, 60, source=TINY),
            _damage(100, TINY, AXE, 30, attacker_is_illusion=True),
        ]

        bursts = build_fight_timeline(_match(log), 0, 1000).damage

        assert {(b.attacker, b.attacker_is_illusion, b.attacker_hero) for b in bursts} == {
            (GOLEM, False, TINY),
            (TINY, True, TINY),
        }

    def test_damage_to_illusions_is_left_out(self):
        log = [_damage(100, TINY, AXE, 60, target_is_illusion=True)]

        assert build_fight_timeline(_match(log), 0, 1000).damage == ()


class TestModifiers:
    def test_adds_pair_with_the_next_remove_of_the_same_modifier(self):
        log = [
            _modifier("MODIFIER_REMOVE", 50, AXE, AXE, "modifier_axe_berserkers_call_armor"),
            _modifier(
                "MODIFIER_ADD",
                100,
                LION,
                AXE,
                "modifier_lion_voodoo",
                stun_duration=3.0,
                modifier_duration_s=3.0,
            ),
            _modifier("MODIFIER_ADD", 120, SF, SF, "modifier_black_king_bar_immune"),
            _modifier("MODIFIER_REMOVE", 190, LION, AXE, "modifier_lion_voodoo"),
        ]

        timeline = build_fight_timeline(_match(log), 0, 1000)
        windows = {w.modifier: w for w in timeline.modifiers}

        assert (
            windows["modifier_axe_berserkers_call_armor"].start_tick,
            windows["modifier_axe_berserkers_call_armor"].end_tick,
        ) == (None, 50)
        hexed = windows["modifier_lion_voodoo"]
        assert (hexed.start_tick, hexed.end_tick, hexed.stun_s, hexed.duration_s) == (
            100,
            190,
            3.0,
            3.0,
        )
        assert (hexed.source, hexed.source_hero) == (LION, LION)
        assert windows["modifier_black_king_bar_immune"].end_tick is None
        assert timeline.disables == (hexed,)


class TestDeaths:
    def test_death_reads_gold_lost_rewards_and_recent_damage(self):
        log = [
            _damage(50, SF, LION, 400),  # before the window, inside the recap
            _damage(130, SF, LION, 300, "nevermore_requiem"),
            _entry("DEATH", 140, SF, LION, target_is_hero=True),
            _entry("GOLD", 140, target=LION, value=-210, gold_reason=1),
            _entry("GOLD", 140, target=SF, value=326, gold_reason=12),
            _entry("GOLD", 140, target=AXE, value=81, gold_reason=12),
            _entry("GOLD", 140, target=SF, value=50, gold_reason=13),  # a creep: not a reward
            _entry("XP", 140, target=SF, value=468, xp_reason=1),
            _entry("XP", 140, target=AXE, value=468, xp_reason=1),
        ]

        timeline = build_fight_timeline(_match(log), 100, 1000)

        (death,) = timeline.deaths
        assert (death.victim, death.killer, death.killer_hero) == (LION, SF, SF)
        assert death.gold_lost == 210 and not death.reincarnated
        assert [(d.source, d.damage) for d in death.recent_damage] == [
            ("", 400),
            ("nevermore_requiem", 300),
        ]
        assert timeline.rewards == (
            KillRewards(140, (LION,), {SF: 326, AXE: 81}, {SF: 468, AXE: 468}),
        )
        assert timeline.rewards_at(140) is timeline.rewards[0]
        assert timeline.rewards_at(141) is None

    def test_a_summon_kill_is_credited_to_the_owner(self):
        log = [_entry("DEATH", 100, GOLEM, LION, source=TINY)]

        (death,) = build_fight_timeline(_match(log), 0, 1000).deaths

        assert (death.killer, death.killer_hero) == (GOLEM, TINY)

    def test_a_tower_kill_has_no_killer_hero(self):
        log = [_entry("DEATH", 100, "npc_dota_goodguys_tower1_mid", SF)]

        (death,) = build_fight_timeline(_match(log), 0, 1000).deaths

        assert death.killer_hero is None

    def test_deaths_on_one_tick_share_one_rewards_record(self):
        log = [
            _entry("DEATH", 100, TINY, AXE),
            _entry("DEATH", 100, TINY, SF),
            _entry("GOLD", 100, target=TINY, value=700, gold_reason=12),
        ]

        timeline = build_fight_timeline(_match(log), 0, 1000)

        assert [d.victim for d in timeline.deaths] == [AXE, SF]
        assert timeline.rewards == (KillRewards(100, (AXE, SF), {TINY: 700}, {}),)

    def test_aegis_death_is_marked_and_illusion_deaths_are_left_out(self):
        log = [
            _entry("DEATH", 100, TINY, SF, will_reincarnate=True),
            _entry("DEATH", 110, TINY, AXE, target_is_illusion=True),
        ]

        (death,) = build_fight_timeline(_match(log), 0, 1000).deaths

        assert death.victim == SF and death.reincarnated and death.gold_lost == 0


class TestWindow:
    def test_only_entries_and_buybacks_inside_the_window(self):
        early = BuybackEvent(tick=50, player_slot=1, cost=500, net_worth=6000)
        inside = BuybackEvent(tick=150, player_slot=1, cost=831, net_worth=8000, cost_exact=True)
        log = [_cast(50, TINY, "tiny_toss"), _cast(150, TINY, "tiny_avalanche")]

        timeline = build_fight_timeline(_match(log, lion=[early, inside]), 100, 200)

        assert [c.ability for c in timeline.casts] == ["tiny_avalanche"]
        assert [(b.hero, b.cost, b.cost_exact) for b in timeline.buybacks] == [(LION, 831, True)]
        assert timeline.player_ids == {TINY: 0, LION: 1, AXE: 5, SF: 6}

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"start_tick": 200, "end_tick": 100},
            {"start_tick": 0, "end_tick": 10, "hit_window_ticks": -1},
            {"start_tick": 0, "end_tick": 10, "burst_ticks": 0},
        ],
    )
    def test_rejects_bad_bounds(self, kwargs):
        with pytest.raises(ValueError):
            build_fight_timeline(_match([]), **kwargs)


@pytest.mark.slow
@pytest.mark.integration
def test_fixture_fights_have_their_rewards_on_the_death_tick(canonical_parsed_match):
    """Every hero death has a rewards record on its tick, with gold for hero kills."""
    match = canonical_parsed_match
    assert match.fights
    ticks = [entry.tick for entry in match.combat_log]
    for fight in match.fights:
        timeline = build_fight_timeline(match, fight.start_tick, fight.end_tick)
        assert len(timeline.deaths) >= fight.deaths
        for death in timeline.deaths:
            rewards = timeline.rewards_at(death.tick)
            assert rewards is not None and death.victim in rewards.victims
            if death.killer_hero and not death.reincarnated:
                assert rewards.gold, (death.tick, death.victim)
                assert death.gold_lost > 0, (death.tick, death.victim)
        for cast in timeline.casts:
            assert cast.caster not in {hit.hero for hit in cast.hits}
        cast_damage = sum(cast.damage for cast in timeline.casts)
        assert cast_damage <= sum(burst.damage for burst in timeline.damage)
        # Every hero-kill bounty and XP in the window is paid on a death tick.
        reward_ticks = {rewards.tick for rewards in timeline.rewards}
        lo = bisect.bisect_left(ticks, fight.start_tick)
        hi = bisect.bisect_right(ticks, fight.end_tick)
        for entry in match.combat_log[lo:hi]:
            if (entry.log_type == "GOLD" and entry.gold_reason == 12) or (
                entry.log_type == "XP" and entry.xp_reason == 1
            ):
                assert entry.tick in reward_ticks, (entry.tick, entry.target_name)
