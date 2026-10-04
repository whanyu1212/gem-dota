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

## Review policy

A change to the attribution, lifecycle or window rules should update the
boundary tests, this page and the corpus expectations in the same pull request.
A human-reviewed study may add strategic labels outside gem, but must not
replace the factual replay expectations used for regression testing.
