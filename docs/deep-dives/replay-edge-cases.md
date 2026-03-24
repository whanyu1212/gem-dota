# Replay Edge Cases

Real replay parsing is not just "read bytes, decode protobufs, done". Source 2 replays contain duplicated entities, build-specific field changes, truncated packets, and signals that look authoritative but are only heuristics.

This page collects the cases that most often confuse parser users and library contributors.

## Why this page exists

If a parsed output looks strange, the first question should be:

1. is the replay data itself ambiguous?
2. did we choose the wrong source of truth?
3. are we inferring something that the replay never directly stores?

Those are different problems, and they need different fixes.

::: important
Many "parser bugs" are really "picked the wrong authoritative field or entity" bugs.
:::

## Canonical hero entity vs duplicate hero entities

The clean mental model is:

1. one player
2. one hero
3. one movement trail

Real replay state is messier than that.

You can have multiple live hero-class entities that all look like the same hero:

1. the real hero entity
2. illusion-like entities
3. clone/replicate-style entities
4. temporary duplicated hero representations that still expose hero fields

If you sample every `CDOTA_Unit_Hero_*` entity and then group by `player_id`, you can merge multiple physical entities into one trail.

Common symptom:

1. the same player has two coordinates at the same tick
2. rendered movement suddenly zig-zags between two distant points
3. farming or movement maps look impossible

### The correct source of truth

For movement and live hero state, the canonical choice is the player's selected hero handle:

1. `CDOTAPlayerController.m_hAssignedHero`
2. fallback: `CDOTA_PlayerResource.m_vecPlayerTeamData.%04d.m_hSelectedHero`

That handle resolves to one live entity. Sampling that entity avoids most illusion/clone contamination.

Simplified logic:

```python
handle = controller.m_hAssignedHero or player_resource.m_hSelectedHero
hero_entity = entity_manager.find_by_handle(handle)
snapshot(hero_entity)
```

### Why matching by `player_id` is not enough

`player_id` tells you ownership, not uniqueness.

Two hero-like entities can share the same player slot. That is enough to corrupt:

1. `position_log`
2. movement heatmaps
3. farming route visualizations
4. any nearest-position lookup done from the wrong hero entity

::: tip
If a movement path looks wrong, inspect for duplicate same-tick positions before changing the renderer.
:::

## Sampling inside a tick

Even when you pick the right entity, timing still matters.

Replay packets do not arrive as a perfect "end of tick snapshot". Entity updates are processed incrementally. If sampling is triggered from arbitrary entity callbacks, you can observe:

1. partially updated state within the current tick
2. one entity already updated while another is still stale
3. small jitter or timing skew in sampled series

This usually matters less than the canonical-entity problem, but it still matters for:

1. movement trails
2. fast state transitions
3. exact per-tick reconstruction

## Incomplete or truncated replays

Not every replay ends cleanly.

Common cases:

1. final compressed block is truncated
2. `CDemoFileInfo` metadata is missing or incomplete
3. some late-game state never arrives

gem intentionally falls back to live game-rule entities when possible, for example:

1. match id from `CDOTAGamerulesProxy`
2. winner from `m_nGameWinner`
3. late-game scoreboard values from authoritative player-resource fields

This is why "missing metadata" does not always mean "parse failed".

## Build-specific field and schema differences

The replay format is not stable across Dota builds.

Typical examples:

1. `m_nPlayerID` vs `m_iPlayerID`
2. renamed or moved sendtable fields
3. draft/facet field layout changes
4. different serializer behavior across builds

That is why gem patches sendtable decoding and often reads fallback fields instead of assuming one permanent schema.

If a field suddenly becomes `None` on a newer replay, treat that as a schema question first.

## Inference limits are not parser bugs

Some outputs are inferred because the replay does not directly store the desired concept.

Examples:

1. estimated ward vision impact
2. farming context labels like `safe_home_farm` or `high_risk_invade`
3. map control proxies
4. teamfight clustering windows

These are analytics heuristics, not raw replay facts.

So the right question is not:

> "Did the parser read this field wrong?"

It is:

> "Is this inference calibrated well enough for the use case?"

## Practical debugging checklist

When something looks wrong, check in this order:

1. Are there duplicate samples for the same player and tick?
2. Are we sampling the canonical entity handle, or just matching by class/player id?
3. Is the replay truncated or missing metadata?
4. Did the build move or rename the field?
5. Is this output inferred rather than directly stored?

## Related pages

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [State Reconstruction Layer](state-layer.md)
3. [Extractors Layer](extractors-layer.md)
4. [Match Assembly Layer](match-assembly-layer.md)
