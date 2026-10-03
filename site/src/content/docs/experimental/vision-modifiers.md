# Vision Modifiers

`match.vision_modifiers` is an experimental, evidence-preserving stream of
vision-relevant modifier **applications**. It is broader than a list of direct
hero reveals: non-hero targets, aura carriers, and reveal auras remain in the
stream so downstream analysis can distinguish them instead of silently treating
every modifier as Track or Corrosive Haze.

> [!IMPORTANT]
> This is combat-log evidence, not Valve's fog-of-war feed. Use
> `hero_visibility_at(...)` when authoritative hero visibility bits answer the
> question directly.

## Semantics

Each modifier is described by a typed registry:

| Modifier | `semantic` |
|---|---|
| `modifier_slardar_amplify_damage` | `direct_target_reveal` |
| `modifier_bounty_hunter_track` | `direct_target_reveal` |
| `modifier_item_dustofappearance` | `direct_target_reveal` |
| `modifier_item_gem_of_true_sight` | `aura_carrier` |
| `modifier_gem_active_truesight` | `reveal_aura` |

This registry was audited against the repository's modern Source 2 fixtures for
OpenDota patch id 60, including match `8822520406` (Corrosive Haze) and match
`8868259993` (Gem carrier). Modifier names and behavior are patch-sensitive;
new supported patches must be re-audited rather than inheriting these meanings
silently.

Gem's carrier modifier is commonly self-applied and same-team. It is retained as
carrier evidence; it is not a direct reveal of the carrier. Non-hero applications
are also retained with `target_is_hero=False`.

## Lifecycle evidence

The original first six `VisionModifierEvent` fields remain in their historical
order: `tick`, `end_tick`, `modifier_name`, `target_name`, `caster_name`, and
`caster_team`. New fields append semantic, identity, team-provenance, duration,
aura/purge, pairing, and lifecycle evidence.

- `end_tick` is set only from an observed `MODIFIER_REMOVE`. gem never invents
  an exact tick from a duration.
- `lifecycle_status` is `removed`, `expired`, `open`, or `incomplete`.
- `close_evidence` distinguishes `observed`, `duration_inferred`, `unobserved`,
  and `ambiguous` closes.
- Application and removal durations, elapsed duration, pause-aware game times,
  sources, protocol teams, aura flags, and purge evidence remain separate.
- Hero/illusion values retain explicit presence flags; absent optional fields are
  not silently treated as authoritative `False` during pairing.
- Protocol team 2/3 wins; player snapshots are used only as a recorded,
  consensus-only fallback. Conflicting snapshot teams remain unknown.

An unobserved application may be classified `expired` once the pause-aware final
game time passes its reported duration, but its `end_tick` stays `None`. A
plausibly live near-end application is `open`; `None` does **not** mean "active
until game end."

## Pairing adds and removes

Relevant observations are resolved after parsing in tick and ingestion order.
For a removal, gem requires any explicit caster and hero/illusion identity to be
compatible, then uses pause-aware elapsed-time evidence, then a single remaining
candidate. Intended duration is retained but is not mistaken for elapsed age.
Pending ambiguity is revisited when a later exact match eliminates a candidate.
Gem does not use LIFO when multiple applications remain plausible.

Ambiguous candidates become `incomplete`. Ambiguous and orphan removals are
preserved separately in:

```python
match.vision_modifier_pairing_issues  # list[VisionModifierPairingIssue]
```

Pairing issues include their reason, removal tick and identity, combat-log
source, candidate add ticks, and key duration/team evidence. They do not create
fake application rows.

## Conservative consumers

`assess_point_vision(..., target_player_id=...)` and fight reveal badges consume
only direct-target, non-illusion hero, non-ambiguous evidence with an observed
`end_tick`. The point assessment keeps that target evidence separate from
hero/observer map geometry. Duration-only expiry is pause-aware evidence but
cannot provide an exact replay-tick interval, so consumers do not synthesize
one. Gem carrier/aura events and incomplete or unobserved-close events are not
reported as direct target reveals.

For tabular workflows, `build_dataframes(...)` always provides the flat
`vision_modifiers` and `vision_modifier_pairing_issues` tables, with declared
columns even when empty. List fields (`evidence_gaps`, `candidate_add_ticks`) are
exported as `";"`-joined strings.
