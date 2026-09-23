# Smoke/Fight Insights

`build_smoke_fight_insights(match)` composes smoke lifecycles, detected fights,
sampled positioning, authoritative hero visibility, and bounded reveal evidence
into reusable observations. It is a post-parse analysis: it reads a completed
`ParsedMatch`, does not rerun extractors, and does not mutate the match.

```python
import gem

match = gem.parse("match.dem")

for insight in gem.build_smoke_fight_insights(match):
    print(
        insight.smoke_index,
        insight.fight_index,
        insight.status.value,
        insight.active_smoked_player_ids,
    )
```

The builder deliberately reports evidence, not a smoke grade. It does not call
a smoke successful or failed, infer why a modifier ended, or attribute a fight
result to one positional measurement.

## Association contract

By default, a detected fight is a post-activation candidate when its bounded
engagement tick falls in the inclusive 1,800-tick window beginning at smoke
activation. A fight whose bounded engagement tick has already been reached at
activation is reported as pre-existing, not as a post-smoke engagement. The
detector's earlier padded fight-window start does not trigger this state.

The link requires at least one resolved smoked member who is also an active
fight participant under gem's direct-combat definition. Spatial proximity is
retained as context and never substitutes for participation.

The builder emits one `SmokeFightInsight` for each smoke/fight association. A
smoke with no bounded fight receives one record whose `fight_index` is `None`.
Each record has one of these states:

| State | Meaning |
|---|---|
| `linked` | Exactly one smoke has active-member support for the fight |
| `temporal_only` | The fight is inside the time window, but no smoked member has supported active participation |
| `ambiguous` | More than one smoke has active-member support; none receives exclusive credit |
| `preexisting` | The bounded engagement tick was at or before smoke activation while the fight had not ended |
| `no_candidate` | No bounded fight record was observed |

One smoke may link to multiple fights. A fight receives at most one unique
smoke link. These rules prevent later objectives or ward placements from being
silently credited to multiple activations.

## Exact events and sampled context

The exact event sequence can include activation, first member removal, first
authoritative visible observation, first opposing direct reveal, first logged
member action, first valid fight death, and fight end. Exact source ticks remain
separate; a missing event stays missing.

Formation evidence is different. It uses fresh position samples for resolved
smoke members and retains the requested tick, each source sample tick and age,
positioned and missing member IDs, centroid, RMS spread, maximum pairwise
distance, and completeness. The near-fight spread value is explicitly a
sampled observation; it is not a claim about physical arrival time.

Visibility remains authoritative and tri-state (`visible`, `hidden`, or
`unknown`). Point-vision geometry and direct-target reveal records are exposed
as separate supporting evidence. Smoke removal is never used as proof of enemy
vision or of a particular revealing source.

## Follow-up evidence

For a unique link, the follow-up window begins at fight end and is bounded by
the earliest of 1,800 ticks, game end, or the next same-team smoke activation.
The upper bound is exclusive. Tower and barracks kills, Roshan and Tormentor
kills, and observer placements retain direct actor/team attribution when it can
be resolved. Unresolved actors remain explicit with unknown attribution; gem
does not infer ownership from the destroyed structure or objective.

Ambiguous and temporal-only candidates receive no exclusive follow-up credit.
Raw event ticks are globally allocated to at most one preceding unique link.
When unique follow-up windows overlap, the event goes to the link with the
latest fight-end tick; equal starts use stable smoke/fight source order.

## Exports and report UI

`gem.to_dict(...)` serializes the public dataclasses and enum values. DataFrame
exports provide flat insight, member, and follow-up tables with stable empty
schemas.

The HTML report renders concise evidence in **Smoke Operations** and links a
unique association to the matching **Fights** positioning card. The jump opens
the relevant tab and snapshot; both views consume the same analysis records.

## Limits

- Fight windows and engagement-start evidence inherit the documented
  teamfight detector fallbacks.
- Hero positions are sampled and can be partial, stale, or missing.
- Authoritative visibility can remain unknown when the replay has no usable
  observation.
- Combat logs do not establish every action's intent or every objective's
  ownership.
- The output is an analyst aid, not proof of decision quality or causality.
