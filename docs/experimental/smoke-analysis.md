# Smoke Analysis

`build_smoke_analysis(match)` reconstructs each Smoke of Deceit activation as a
set of per-hero modifier lifecycles. It keeps the observed replay facts separate:

- the item activation tick
- each hero's modifier application and removal ticks
- natural expiry versus an earlier removal
- authoritative enemy visibility at those ticks
- sampled enemy proximity and same-tick combat evidence
- the first teamfight whose first death follows the activation within 60 seconds

The helper does **not** produce a smoke success score or claim why the modifier
ended. A hero can lose smoke while still hidden from the opposing team, and a
natural expiry can still create useful map position.

## Quick start

```python
import gem

match = gem.parse("match.dem")

for smoke in gem.build_smoke_analysis(match):
    print(smoke.activation_tick, smoke.status.value)
    for member in smoke.members:
        print(
            member.hero_name,
            member.applied_tick,
            member.removed_tick,
            member.lifecycle_status.value,
            member.visibility_at_remove.value,
        )
```

Ticks are the canonical timing values. Convert them to display seconds only at
the presentation boundary. Raw smoke and member records also retain optional
pause-aware `*_game_time_s` values when the replay exposes them; otherwise gem
uses the exact replay tick and does not invent a game-time value.

## Lifecycle status

For each member, `lifecycle_status` is:

| Status | Meaning |
|---|---|
| `expired` | The reported modifier elapsed duration reached its expected duration within a small tolerance |
| `early` | A removal was observed before the expected duration |
| `unobserved` | No removal, or insufficient duration evidence, was available |

The group status summarizes only those member lifecycles:

- `no_members_observed`
- `early_removal`
- `expired`
- `incomplete`

An activation with no observed members is deliberately not labelled “wasted.”
It may be a real empty activation, but the replay evidence is not strong enough
to turn that into a causal conclusion.

## Visibility and proximity

`visibility_at_apply`, `visibility_at_remove`, and `first_visible_tick` use the
authoritative hero-entity visibility timeline exposed by
`hero_visibility_at(...)`. Each state remains tri-state: `visible`, `hidden`, or
`unknown`.

`nearest_enemy_distance` is different. Hero positions are sampled roughly once
per second, so the nearest enemy name and distance are useful context rather
than exact break attribution. Same-tick action and death lists are likewise
correlations, not proof of cause.

## Raw lifecycle data

The parse result retains the underlying records in `match.smoke_events`:

```python
event.tick                    # item activation tick
event.activation_game_time_s # pause-aware time when available
event.activation_x            # sampled activator position
event.participants[0].applied_tick
event.participants[0].removed_tick
event.participants[0].applied_game_time_s
event.participants[0].removed_game_time_s
event.participants[0].modifier_duration_s
event.participants[0].modifier_elapsed_duration_s
```

The legacy `event.smoked`, `event.x`, and `event.y` fields remain available.
`x/y` are the member centroid captured around modifier application, not the
activator's item-use position.

DataFrame exports include both `smoke_events` (with `smoked` as a `";"`-joined
hero list) and a flat `smoke_members` table.
The HTML report presents the same evidence in the **Smoke Operations** card.
For bounded smoke-to-fight composition, participant overlap, formation context,
and follow-up evidence, use
[Smoke/Fight Insights](./smoke-fight-insights.md).

## Known limitations

- Source 1 combat logs do not expose modifier duration or elapsed duration.
- Positions and distances use sampled player timelines and are less precise than
  combat-log ticks.
- Unresolved combat-log names or missing modifier events remain incomplete;
  gem does not currently use the `ActiveModifiers` string table as a fallback.
- The analysis cannot identify the exact unit, ward, terrain edge, or player
  action that caused an early removal.
