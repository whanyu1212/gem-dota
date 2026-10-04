# Fight Timeline

`build_fight_timeline(match, start_tick, end_tick)` turns the combat log
between two ticks into typed records:

- each ability and item use, with the heroes it hit, the damage it did to each
  and its type;
- every bit of damage on a hero, in short bursts;
- the modifiers on each hero, from when they were added to when they were
  removed;
- each hero death, with the gold the hero lost and the damage it took first;
- the kill gold and XP each hero earned;
- buybacks and their cost.

It is the data behind a fight playback: what happened, to whom, and for how
much. It reports what the log records and adds no interpretation.

## Quick start

```python
import gem

match = gem.parse("match.dem")
fight = max(match.fights, key=lambda f: f.deaths)
timeline = gem.build_fight_timeline(match, fight.start_tick, fight.end_tick)
clock = match.game_clock

for cast in timeline.casts:
    hits = ", ".join(f"{hit.hero} {hit.damage} {hit.damage_type}" for hit in cast.hits)
    print(clock.format_tick(cast.tick), cast.caster, cast.ability, hits)

for death in timeline.deaths:
    rewards = timeline.rewards_at(death.tick)
    print(
        clock.format_tick(death.tick),
        death.victim,
        death.killer_hero,
        -death.gold_lost,
        rewards.gold if rewards else {},
    )
```

Any window works, not only a detected fight. Every record carries ticks; use
`match.game_clock` for game time, since ticks keep running through pauses.
Heroes are NPC names (`npc_dota_hero_tiny`); `timeline.player_ids` maps them to
player slots, and `gem.format_npc_name` gives a display name.

## Records

| Field | Record | What it holds |
|---|---|---|
| `casts` | `TimelineCast` | Caster, ability or item, level, the target the replay records, `hits` and `self_effect` |
| `damage` | `DamageBurst` | Attacker, the hero credited, target hero, source, damage type, damage and number of hits |
| `modifiers` | `ModifierWindow` | Target hero, modifier, source, add and remove ticks, duration, stun seconds, aura |
| `deaths` | `TimelineDeath` | Victim, killer, the hero credited, reincarnation, gold lost, damage taken in the last ten seconds |
| `rewards` | `KillRewards` | Per tick with deaths: the victims, and the hero-kill gold and XP each hero received |
| `buybacks` | `TimelineBuyback` | Hero, cost, and whether the cost was observed |

`timeline.disables` is the modifiers with a stun duration.

## How each record is read

**Casts.** One per `ABILITY` or `ITEM` entry by a hero; casts by illusions are
left out. `target` is the unit the replay records as the cast's target, which
it does only for some unit-targeted casts: 11% of hero casts in match
8856501050. It need not be a hero, or the hero the cast damaged; `hits` says
who took the damage.

**Hits are the one derived field.** A `DAMAGE` entry on a hero that the log
credits to the caster (its damage source, so it may come from a unit the hero
controls, but not from an illusion), or a `MODIFIER_ADD` the caster applied,
belongs to the caster's latest cast, at most three seconds
earlier (`hit_window_ticks`), of the same ability. For damage, that means the
entry's inflictor is the ability. For a modifier, it means the modifier's name
contains the ability's (`modifier_lion_voodoo` for `lion_voodoo`,
`modifier_sheepstick_debuff` for `item_sheepstick`; see
`modifier_matches_ability`). Each entry goes to at most one cast, so no damage
is counted twice. What the cast did to the caster itself is `self_effect`: Black
King Bar's spell immunity, for example.

A modifier named differently from its ability is not matched, and damage that
arrives after the hit window (a long damage-over-time) is left off the cast.
Both still appear in `modifiers` and `damage`.

**Damage.** Every `DAMAGE` entry on a hero, grouped by attacker, target, source
and type into bursts that start at their first entry and last half a second
(`burst_ticks`). The credited hero is the log's damage source: the owner of a
summon or an illusion, the attacker itself for a hero, and `None` for creeps,
towers and neutrals. A cast's hit damage is a subset of this list; the rest is
right-click attacks, passives and damage no cast matched.

**Modifiers.** A modifier's source is the unit that applied it: on modifier
entries the log's damage-source field names unrelated units, so it is not
read. Each `MODIFIER_ADD` on a hero is paired with the next
`MODIFIER_REMOVE` of the same modifier on the same hero. `end_tick` is `None`
when the modifier outlasted the window, and `start_tick` is `None` when it was
added before the window.

**Deaths and rewards.** Gold lost is the victim's `GOLD` entry with reason 1
(death) on the death tick. Rewards are the hero-kill `GOLD` (reason 12) and `XP`
(reason 1) entries on the same tick. The log does not say which death a bounty
pays for, so deaths on one tick share one `KillRewards`. On the two fixtures
checked, every hero-kill bounty lands on the death tick itself. A reincarnation (Aegis) is
marked with `reincarnated`; the two Aegis deaths in match 8856501050 cost no
gold and paid no bounty.

## Checks

The tests cover each rule on synthetic logs. On the canonical replay they check
that every death has a rewards record on its tick, that every hero kill paid a
bounty and cost the victim gold, that no caster is among its own hits, and that
cast damage never exceeds the total damage.

## Related

- [Fight Positioning](./fight-positioning.md): where each hero stood at four
  moments of a fight.
- [Fights](../guides/06_fights.md): how gem detects fights.
