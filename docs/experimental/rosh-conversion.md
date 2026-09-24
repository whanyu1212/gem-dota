# Roshan Conversion

`Roshan Conversion` is an experimental, evidence-first analysis of what changed
after each Roshan kill.

Instead of forcing every Roshan into one exclusive category, gem compares the
two teams across fights, structures, resources, territory, vision, and the
Tormentor. The HTML report keeps the underlying signed values visible and adds
non-exclusive tags only as a quick summary.

## Why this is experimental

The replay does not contain a native `rosh_conversion` field. This analysis
joins already-parsed facts:

- Roshan kills and Aegis pickup, steal, or deny events
- teamfight windows
- towers and barracks destroyed
- team gold and XP advantage curves
- sampled hero positions and observer-ward placements
- Tormentor kills and buybacks

The facts are observed replay data, but their association with one Roshan and
the thresholds used for summary tags are analytical choices. Treat the output
as an explainable comparison, not proof that Roshan caused every later event.

## Attribution and windows

An Aegis event is associated only when it occurs between the Roshan kill and the
earliest of:

- 30 seconds after the kill
- one tick before the next Roshan
- game end

For a pickup or steal, the conversion team is the holder's team. The ownership
horizon runs from pickup until the earliest of five minutes, the next Roshan,
or game end. A holder death inside that horizon is treated as an inferred Aegis
consume. `aegis_fate_source` distinguishes that inference from a denial event,
nominal expiry, game-end boundary, next-Roshan boundary, or missing event.

Item-entity deletion was investigated but is not a stronger lifecycle signal:
the entity can disappear on pickup or later removal and does not reliably
separate consumption, natural expiry, transfer/drop, and game-end cleanup. gem
therefore retains the bounded holder-death inference and states its provenance
instead of presenting it as observed fact.

The analysis window may continue for up to 120 seconds after Aegis ends so that
the immediate aftermath remains visible. If the inferred consume occurs inside
a detected fight, that whole fight is included. The result is always capped at
the next Roshan and game end, so one event cannot be credited to two Roshan
windows.

When Aegis is denied or no reliable holder is available, gem uses the immediate
three-minute post-Roshan window and marks the profile `partial` or
`unavailable`. If the Roshan killer's team can be resolved, that team remains
the comparison side; otherwise team-dependent values are unavailable rather
than reported as zero.

Team attribution prefers the Source 2 protocol `attacker_team`, then player ID,
then a unique damage-source hero, then a unique attacker hero, then an explicit
`npc_dota_goodguys_*` / `npc_dota_badguys_*` attacker allegiance for lane
creeps. The selected source is exposed as `roshan_team_source` or
`conversion_team_source`. Unknown structure and Tormentor killers remain
unattributed; they are counted in the profile and never silently credited to
the conversion team. A structure killed by its owning team is treated as a deny
and credited to neither side.

## Differential profile

Every differential is signed from the conversion team's perspective:

```text
conversion team value - opponent value
```

A positive value favors the conversion team; a negative value shows a
counter-conversion by the opponent.

### Fights

```text
fights won by conversion team - fights won by opponent
```

Drawn or unknown-winner fights are reported separately and do not change the
differential.

Fight association uses the engagement-start evidence from teamfight
positioning, rather than the padded detector window alone. `fight_evidence`
records the fight index, whether the engagement was already underway at the
Roshan boundary, engagement-start source, first-death/end ticks, winner, and
active participant IDs split by side. The report links in both directions
between Roshan timeline events and the corresponding fight card.

### Structures

Each destroyed structure contributes a transparent, tier-aware value:

| Structure | Value |
| --- | ---: |
| Tier 1 tower | 1 |
| Tier 2 tower | 2 |
| Tier 3 tower | 3 |
| Tier 4 tower | 4 |
| Barracks | 4 |

The profile reports both teams' tower and barracks counts, both weighted
values, and their signed difference. Actual structures are always shown beside
the weighted comparison.

### Net worth and XP

Gold and XP use the match-level `radiant_gold_adv` and `radiant_xp_adv` curves,
which come from total-earned team fields. Values are signed for the conversion
team and sampled immediately after the acquisition boundary so the direct
Roshan bounty does not masquerade as downstream conversion.

For each resource the profile reports:

- advantage at the start and end of the analysis window
- total swing (`end - start`)
- swing per minute

Missing or incomplete curves produce `None` / **Unavailable**, never a
fabricated zero.

### Sustained territory

Territory measures sustained forward presence, not distance travelled and not
true map control.

Hero positions are accumulated into roughly 600 × 600 world-unit cells and
30-second buckets. A cell counts as occupied in a bucket when it contains at
least 10 hero-seconds or at least two distinct allied heroes. Samples are not
interpolated across gaps longer than 10 seconds, which prevents teleports and
missing telemetry from drawing imaginary paths.

Two forward-presence measures are computed for each side:

- **coverage:** average occupied enemy-side area per bucket
- **depth:** time-weighted 90th-percentile progress toward the enemy fountain

With complete sampling, a team that never enters the enemy side has observed
depth `0.0`; unavailable depth is reserved for insufficient position evidence.

The report compares a three-minute pre-Roshan baseline with the hardened
analysis window:

```text
coverage swing =
  (conversion coverage - opponent coverage) during
  - (conversion coverage - opponent coverage) before
```

Depth swing uses the same double-differential shape. A territory window needs at
least 70% of the expected player-time for both sides; insufficient sampling is
reported as unavailable. The paired maps show sampled occupied cells, not fog,
vision, or continuous paths.

### Forward wards

```text
conversion observer wards in enemy territory
- opponent observer wards in conversion territory
```

Only observer wards with known coordinates inside the analysis window count.

### Tormentor

```text
conversion-team Tormentor kills - opponent Tormentor kills
```

Tormentor remains a separate secondary-objective dimension. It is not assigned
the same weight as towers or barracks. Events without a resolvable killer team
are excluded rather than guessed.

### Buybacks

Buybacks remain timeline context. They can help explain the cost of a push or
fight, but they are not a headline differential and do not affect any tag.

## Non-exclusive tags

Several tags can describe the same Roshan. The initial thresholds are explicit
calibration points, not universal Dota truths:

| Tag | Initial rule |
| --- | --- |
| `fight_advantage` | fight differential ≥ 2 |
| `objective_gain` | weighted structure differential ≥ 2 |
| `resource_gain` | net-worth swing ≥ 2,000 or XP swing ≥ 1,500 |
| `territorial_expansion` | coverage double-differential ≥ 8 percentage points |
| `vision_expansion` | ward differential ≥ 2, or ≥ 1 with positive coverage swing |
| `tormentor_secured` | Tormentor differential > 0 |
| `game_closing` | the conversion team wins and the game ends inside this analysis window |
| `counter_conversion` | the opponent owns the material signed evidence in the window |

The defaults live in the immutable `RoshTagThresholds` record and every profile
stores its `tag_ruleset`. Callers can pass an alternate threshold record to
`build_rosh_conversions(...)` for reproducible sensitivity analysis without
changing raw values.

The report does not show a radar chart or aggregate score. Independent metrics
have different units and meanings; keeping raw signed values visible is more
honest than making them look directly additive.

## Status and missing data

Each profile carries a status and concrete reasons:

- `complete`: the team and main evidence needed for the profile are available
- `partial`: attribution exists, but one or more evidence streams are incomplete
- `unavailable`: the conversion team cannot be established or the comparison
  cannot be made responsibly

A genuine zero means the replay contained the relevant evidence and the event
did not occur. **Unavailable** means the evidence was absent or insufficient.

## Compatibility

`conversion_label` and `conversion_score` are formally deprecated. They remain
available through the 0.9 release line for source compatibility and will not be
removed before 1.0; 1.0 may either remove them or designate them permanent
compatibility fields after downstream usage is reviewed. New consumers should
use `differential_profile`, raw values, `analysis_status`, and
`conversion_tags`. The report no longer renders either legacy field.

`build_dataframes(match, include=["analysis"])` exports:

- `roshan_conversions`: one flat row per Roshan, including provenance, raw
  differentials, evidence status, ruleset, and clearly prefixed legacy fields
- `roshan_conversion_fights`: one flat row per associated fight with engagement
  provenance, relation, and participant IDs

Direct `gem.to_dict(build_rosh_conversions(match))` serialization preserves the
nested public records and enum values as strings.

## Current limits

- Aegis consumption remains inferred from the holder's first hero death inside
  the ownership horizon; transfer/drop is not independently observable.
- Engagement start is evidence-aware but still falls back to first death when
  earlier damage evidence is unavailable.
- Forward territory is only as complete as the replay's sampled position logs.
- Map halves and depth use calibrated geometry, not lane topology or fog state.
- Tag thresholds remain `provisional-v1`; see the calibration record below.

## Related pages

1. [Reports](../reports/index.md)
2. [Roshan Conversion Calibration](./rosh-conversion-calibration.md)
3. [Farming Patterns](./farming-patterns.md)
4. [Estimate Vision](./estimate-vision.md)
5. [Vision Modifiers](./vision-modifiers.md)
