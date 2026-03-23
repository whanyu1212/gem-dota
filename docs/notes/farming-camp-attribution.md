# Camp Farming Attribution Plan

This note defines a concrete contract for improving farming pattern extraction (which camps each core actually farmed, in order) with lower context blindness.

## Goal

Move from radius-only camp matching to confidence-scored camp sessions that combine movement, combat, and economy signals.

## Inputs

- Camp metadata: `src/gem/data/neutral_camps.json`
- World bounds: `src/gem/data/map_constants.json`
- Replay telemetry:
  - `players[].position_log`
  - combat log (neutral interactions; location when present)
  - per-player timeseries (`gold_t`, `xp_t`, `lh_t`)
  - objectives (`towers`, `barracks`, `roshans`, `aegis_events`, `tormentors`, `shrines`)
  - wards (`match.wards`) and vision estimator (`analysis.estimate_vision`)
- Annotated reference image: `tests/fixtures/camp_annotated.png` (for zone calibration and QA)

## New Geometry File

Create `src/gem/data/camp_zones.json` with per-camp shapes.

```json
{
  "version": 1,
  "source_image": "tests/fixtures/camp_annotated.png",
  "world_bounds": { "xmin": 7563, "xmax": 25900, "ymin": 7800, "ymax": 25600 },
  "camps": [
    {
      "id": 1,
      "type": "large",
      "center": { "x": 8647, "y": 15564 },
      "zone": { "shape": "ellipse", "rx": 700, "ry": 620, "rotation_deg": 0 },
      "hysteresis": { "enter_margin": 0, "exit_margin": 120 }
    }
  ]
}
```

Notes:
- Support `ellipse` first; allow optional `polygon` later for irregular camps.
- `hysteresis` prevents flicker when heroes skim zone edges.

## Output Schema

Add a new extractor output (per player):

```text
CampVisit:
  player_id: int
  camp_id: int
  camp_type: str
  start_tick: int
  end_tick: int
  duration_s: float
  neutral_kills: int
  neutral_damage: int
  gold_gain: int
  xp_gain: int
  confidence: float       # 0.0..1.0
  confidence_label: str   # high|medium|low
  signals: list[str]      # ["zone_dwell", "neutral_kill", ...]
```

Derived summary:
- ordered route (`camp_id` sequence)
- transition counts (`camp_a -> camp_b`)
- repeat loops (triangle/ancients cycles)

## Context Model (Objective-Aware)

Add a match-level context timeline so each camp visit is interpreted relative to map state.

```text
MapContextBucket:
  start_tick: int
  end_tick: int
  tower_alive_radiant: int
  tower_alive_dire: int
  t1_mid_alive_radiant: bool
  t1_mid_alive_dire: bool
  roshan_last_kill_tick: int | None
  aegis_holder_team: int | None   # 2|3|None
  aegis_active: bool
  tormentor_last_kill_tick: int | None
  ward_count_radiant: int
  ward_count_dire: int
  enemy_presence_by_region: dict[str, float]  # decayed density score
```

Attach context to each visit:

```text
CampVisitContext:
  farm_safety_score: float      # 0..1
  pressure_score: float         # 0..1
  expected_value_score: float   # 0..1
  context_label: str            # safe_farm|contested_farm|defensive_jungle|aggressive_invade
  context_drivers: list[str]    # ["lost_t1_mid", "enemy_aegis_active", ...]
```

Recommended defaults:
- Build context buckets every 30s (`900` ticks).
- Apply decay windows:
  - enemy presence: fast (30–90s)
  - roshan/aegis pressure: medium (Aegis active window)
  - tower-state effects: persistent until state changes
- Keep confidence explicit; do not hide uncertain context as hard labels.

## Detection Logic (v1)

1. Assign each hero position sample to `camp_id`/`None` using camp zones.
2. Build contiguous in-camp segments with min dwell threshold.
3. Fuse local evidence within each segment:
   - neutral damage/kill proximity
   - short-window gold/xp delta
   - movement profile (not just pass-through)
4. Score confidence from weighted signals and mark low-confidence sessions explicitly.
5. Keep ambiguous periods as `unknown` instead of forcing camp attribution.

## Context Scoring (v1)

1. Build `MapContextBucket` timeline from objective and ward events.
2. For each `CampVisit`, join the overlapping context bucket(s).
3. Compute:
   - `farm_safety_score`: ally control proxies (alive towers, nearby allied presence, ward coverage)
   - `pressure_score`: enemy threat proxies (enemy sightings, enemy aegis, recent objective loss)
   - `expected_value_score`: local farm opportunity (camp type + available neutral evidence + continuity)
4. Assign `context_label` from thresholded score combinations.
5. Emit `context_drivers` for explainability in UI tooltips and downstream analytics.

## Implementation Sequence

1. Add `camp_zones.json` (seeded from annotated map + camp centers).
2. Implement context timeline builder (`map_context.py`) from objectives/wards/presence.
3. Implement `extractors/farming.py` producing `CampVisit` + summaries + `CampVisitContext`.
4. Wire into `ParsedPlayer`/match output behind a feature flag if needed.
5. Add fixtures/tests for:
   - transit near camps (false-positive guard)
   - nearby camp disambiguation
   - repeated triangle loops
   - confidence labeling stability
   - objective-driven route shifts (tower loss / roshan windows)
