# Roshan Conversion Calibration

This page records the reproducible validation work behind the
`provisional-v1` Roshan conversion ruleset. It separates replay facts from tag
observations: the corpus asserts attribution, lifecycle, boundaries, fight
association, and missing-data state, but never declares a Roshan strategically
“good” or “bad.”

## Reproduce the corpus

The committed factual expectations live in
`tests/fixtures/opendota/roshan_conversion_corpus.json`. Full `.dem` files stay
gitignored and are synchronized from `tests/fixtures/opendota/manifest.json`.

```bash
uv run python scripts/sync_opendota_fixtures.py --all-active
uv run python scripts/audit_roshan_conversion_corpus.py --check
```

The audit parses the replay stream with gem. It does not substitute the
OpenDota JSON snapshot for gem's protocol and entity evidence.

## Real-match coverage

The September 2026 audit parsed eight existing local fixtures plus the dedicated
Aegis-denial fixture, spanning 31 Roshan conversions and one short match with no
Roshan. The committed check selects representative facts from six matches:

| Match | Factual role |
| --- | --- |
| `8868259993` | Short game with no Roshan |
| `8860187335` | Three bounded windows and one in-game pause; natural expiry, inferred consumption, and a stolen pickup still held when the Ancient fell |
| `8855188139` | Multiple inferred consumptions and a late window that closes the game |
| `8856501050` | Seven Roshans across three pauses, including an expired window with no associated fight and a final window cut short by the game ending |
| `8822593932` | A fight already underway at acquisition and a final window without economy series |
| `8974053011` | Observed Aegis denial followed by a later normal pickup and inferred consumption |

The local replay set did not contain every rare failure mode. Missing pickup,
unresolved killers, unknown structure/Tormentor attribution, allied structure
denies, summon/source fallback, and threshold edges therefore have targeted
deterministic unit tests. This distinction is explicit
in the corpus metadata rather than representing synthetic cases as real-match
facts.

## Attribution and lifecycle findings

- Source 2 `attacker_team` was present for every audited Roshan kill and is now
  the preferred source. Player and unique roster-name fallbacks remain for
  older or incomplete data.
- The real denial fixture produces `aegis_fate_source="denial_event"`; its later
  holder death produces `holder_death_inference`. Natural five-minute endings
  produce `nominal_expiry`; an Aegis still held when the Ancient falls produces
  `game_end_boundary`.
- Item-entity deletion cannot reliably distinguish pickup, consumption, expiry,
  transfer/drop, and cleanup. It is not used to overrule the bounded death
  inference.
- All audited objective and Tormentor events with known protocol/team evidence
  remained attributed; unknown targeted cases remain counted and uncredited.
- Each conversion ends no later than one tick before the next Roshan. Claimed
  fight indexes are unique across consecutive windows.

## Tag observations

The 31 audited conversions produced these default-tag frequencies:

| Tag | Observed count |
| --- | ---: |
| `fight_advantage` | 8 |
| `objective_gain` | 21 |
| `resource_gain` | 20 |
| `territorial_expansion` | 0 |
| `vision_expansion` | 15 |
| `tormentor_secured` | 6 |
| `game_closing` | 5 |
| `counter_conversion` | 7 |
| no tag | 0 |

These counts were re-audited after the game-clock correction. The first audit
ended every window at the last recorded tick, which can run many minutes past the
Ancient falling, so `game_closing` could never fire on a real replay (0 hits) and
final windows reported missing late evidence. It also mapped minute-level net
worth/XP samples to ticks without subtracting pauses, which shifted resource
windows after any pause. Correcting both moved `game_closing` from 0 to 5,
`counter_conversion` from 3 to 7, `resource_gain` from 22 to 20, and no-tag
windows from 2 to 0. The thresholds themselves are unchanged.

These are sensitivity observations, not precision/recall labels. There is no
defensible subjective ground truth in the fixture, so the audit cannot claim a
false-positive rate by treating analyst opinion as fact. The defaults are
therefore unchanged and remain explicitly `provisional-v1`. In particular, the
zero hits for territorial expansion are recorded for future review rather than
“fixed” by lowering thresholds against this small sample.

`RoshTagThresholds` makes every boundary inspectable. Unit tests exercise exact
threshold transitions and counter-conversion's two-dimension minimum. Raw
values remain the preferred interface regardless of which tags fire.

## Territory sensitivity

`RoshTerritoryConfig` makes cell size, bucket width, maximum sample gap,
occupancy requirements, player-time completeness, and depth percentile
reproducible inputs.

The validation suite establishes:

- 70% player-time completeness is inclusive; 69.99% remains unavailable.
- stationary occupancy is invariant when the bucket width changes from 30 to
  60 seconds.
- changing cell size changes the absolute sampled area, as expected, which is
  why coverage remains a raw geometric measure rather than “true control.”
- weighted p90 depth ignores a small deep-position outlier that a maximum would
  promote.
- gaps longer than ten seconds are not interpolated.

The default remains 600-unit cells, 30-second buckets, a ten-second maximum
sample gap, 70% completeness, and weighted p90 depth. Lane or objective
topology was not added because this corpus does not demonstrate that the added
interpretation would be more reliable than the current transparent geometry.

## Review policy

A future threshold change should update the ruleset name, the boundary tests,
this page, and the corpus observations in the same pull request. A larger
human-reviewed study may add strategic labels separately, but must not replace
the factual replay expectations used for regression testing.
