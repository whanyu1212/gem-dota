# Roshan Conversion Calibration

This page records the reproducible validation behind the Roshan records. The
corpus asserts attribution, Aegis lifecycle, window boundaries, fight
association and missing-data state, and never declares a Roshan strategically
“good” or “bad.” gem 0.12's tags and territory windows, and their observations
on this page, were removed in 0.13.

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

The November 2026 audit parsed the eight local fixtures (seven on patch 7.42 and
one on 7.41), spanning 16 Roshan conversions. The committed check records facts
from all eight:

| Match | Factual role |
| --- | --- |
| `9097870389` | Short game with one Roshan; the Aegis is still held when the Ancient falls, so the window closes the game |
| `9101190574` | Two bounded windows, both ending in inferred consumption |
| `9101299342` | Four Roshans in a 73-minute game: inferred consumptions and a natural expiry |
| `9098298585` | An inferred consumption, then an Aegis still held at the game's end |
| `9097868416` | One Roshan with an inferred consumption |
| `9101479361` | A natural expiry followed by an inferred consumption |
| `9098373280` | A normal pickup, then a stolen one during a fight already underway at acquisition |
| `8974053011` | Observed Aegis denial followed by a later normal pickup and inferred consumption (patch 7.41) |

No local fixture has a short match without a Roshan, or a window without economy
series; the corpus metadata lists both as not observed.

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

## Review policy

A change to the attribution, lifecycle or window rules should update the
boundary tests, this page and the corpus expectations in the same pull request.
A human-reviewed study may add strategic labels outside gem, but must not
replace the factual replay expectations used for regression testing.
