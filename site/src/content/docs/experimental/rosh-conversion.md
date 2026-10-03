# Roshan Conversion

`gem.build_rosh_conversions(match)` returns one record per Roshan kill: who
killed it, what happened to the Aegis, and what happened in the window that
followed. It compares the two teams across fights, structures, resources,
forward wards, the Tormentor and buybacks, and keeps the signed values visible.

It reports what happened, not whether the Roshan "converted". gem 0.12's tags
(`conversion_tags`, `RoshTagThresholds`), verdicts (`conversion_score`,
`conversion_label`, `aegis_outcome`, `drivers`), territory windows and
`enemy_half_farm_share_*` were removed in 0.13. For where a team was, use
`gem.region_of` with the players' `position_log`; for an example of answering a
question from these facts, see the [Roshan recipe](../cookbook/roshan-next-fight.md).

## Why this is experimental

The replay does not contain a native `rosh_conversion` field. This analysis
joins already-parsed facts:

- Roshan kills and Aegis pickup, steal, or deny events
- fight windows
- towers and barracks destroyed
- team gold and XP advantage curves
- sampled hero positions and observer-ward placements
- Tormentor kills and buybacks

The facts are observed replay data, but their association with one Roshan (the
window boundaries) is an analytical choice. Treat the output as an explainable
comparison, not proof that Roshan caused every later event.

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

A positive value means the conversion team had more; a negative value means the
opponent had more.

### Fights

```text
fights won by conversion team - fights won by opponent
```

Drawn or unknown-winner fights are reported separately and do not change the
differential.

Fight association uses the engagement-start evidence from fight
positioning, rather than the padded detector window alone. `fight_evidence`
records the fight index, whether the engagement was already underway at the
Roshan boundary, engagement-start source, first-death/end ticks, winner, and
active participant IDs split by side.

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

### Forward wards

```text
conversion observer wards in the enemy half
- opponent observer wards in the conversion team's half
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

Buybacks are listed on the timeline. They are not a differential.

The HTML report's `Roshan` tab shows only the kill and Aegis lifecycle facts
from these records (see [Match Reports](../reports/index.md)). The differential
profile is available in Python and the DataFrame exports.

## Status and missing data

Each profile carries a status and concrete reasons:

- `complete`: the team and main evidence needed for the profile are available
- `partial`: attribution exists, but one or more evidence streams are incomplete
- `unavailable`: the conversion team cannot be established or the comparison
  cannot be made responsibly

A genuine zero means the replay contained the relevant evidence and the event
did not occur. **Unavailable** means the evidence was absent or insufficient.

## Exports

`build_dataframes(match, include=["analysis"])` exports:

- `roshan_conversions`: one flat row per Roshan, including provenance, raw
  differentials and evidence status
- `roshan_conversion_fights`: one flat row per associated fight with engagement
  provenance, relation, and participant IDs

Direct `gem.to_dict(build_rosh_conversions(match))` serialization preserves the
nested public records and enum values as strings.

## Current limits

- Aegis consumption remains inferred from the holder's first hero death inside
  the ownership horizon; transfer/drop is not independently observable.
- Engagement start is evidence-aware but still falls back to first death when
  earlier damage evidence is unavailable.
- Forward wards are counted by map half (`gem.region_of`), not by lane topology
  or fog state.

## Related pages

1. [Reports](../reports/index.md)
2. [Roshan Conversion Calibration](./rosh-conversion-calibration.md)
3. [Farming Patterns](./farming-patterns.md)
4. [Point-Vision Evidence](./estimate-vision.md)
5. [Vision Modifiers](./vision-modifiers.md)
