# Vision Modifiers

`match.vision_modifiers` is an experimental replay-derived event stream that records reveal-style modifier windows on heroes.

This is the structure that lets gem say things like:

- "this hero was under Track during this interval"
- "this target was revealed by Corrosive Haze here"
- "a Dust / Gem-style reveal window was active on this hero at this tick"

It is also one of the core inputs used by [Estimate Vision](./estimate-vision.md).

> [!IMPORTANT]
> `match.vision_modifiers` is not a raw Valve fog-of-war feed.
>
> It is gem's reconstruction of reveal windows from combat-log modifier events for a curated set of vision-relevant modifiers.

## Why this exists

Pure geometry is not enough for visibility analysis.

A hero can be visible because:

- an allied hero is nearby
- an allied observer ward covers the area
- a reveal-style modifier is active on that hero

The third case is important because it bypasses ordinary line-of-sight logic in ways that simple radius checks do not capture well.

Without `match.vision_modifiers`, `estimate_vision` would miss some of the most analytically important visibility cases:

- Track
- Corrosive Haze
- Dust
- Gem-style reveals

So this structure exists to preserve those reveal windows as explicit replay-derived events.

## What the replay gives us

The replay gives gem combat-log entries, including modifier add/remove events.

gem watches those events during parse and reconstructs reveal windows from them.

That means the feature is:

- replay-derived
- deterministic
- tied to actual observed modifier events

But it is still experimental because gem must decide:

- which modifiers count as vision-relevant
- how to pair add/remove events
- how to handle overlapping or refreshed applications

## Data model

`ParsedMatch.vision_modifiers` is a:

```python
list[VisionModifierEvent]
```

Each `VisionModifierEvent` has:

```python
ev.tick           # int: tick when modifier was applied
ev.end_tick       # int | None: tick when removed, or None if still open at game end
ev.modifier_name  # str: internal modifier name
ev.target_name    # str: NPC hero name of the revealed target
ev.caster_name    # str: NPC hero name of the applier
ev.caster_team    # int: team of the caster (2=Radiant, 3=Dire), or 0 if unknown
```

Interpretation:

- `tick` is the open time of the reveal window
- `end_tick` is the close time if gem observed one
- `modifier_name` says what caused the reveal
- `target_name` says who was revealed
- `caster_name` / `caster_team` say who revealed them

## Current tracked modifier set

The current curated set in `src/gem/__init__.py` is:

| Modifier | Interpretation |
|---|---|
| `modifier_slardar_amplify_damage` | Slardar Corrosive Haze reveal window |
| `modifier_bounty_hunter_track` | Bounty Hunter Track reveal window |
| `modifier_item_dustofappearance` | Dust of Appearance reveal window |
| `modifier_item_gem_of_true_sight` | Gem-based reveal on target |
| `modifier_gem_active_truesight` | Gem thinker / active true sight style reveal |

This is intentionally a curated list, not a blanket "every modifier in the game" stream.

## High-level derivation

The event stream is built in five stages.

### 1. Subscribe to combat-log entries

During `gem.parse()`, gem registers a combat-log callback.

That callback inspects each `CombatLogEntry` as it is emitted during parse.

The relevant code lives in `src/gem/__init__.py`.

## 2. Filter to relevant modifier names

Only modifiers in the curated `_VISION_MODIFIER_NAMES` set are considered.

This is important because the combat log contains many modifier adds/removes that are irrelevant to visibility.

So the first gate is:

```text
entry.inflictor_name in _VISION_MODIFIER_NAMES
```

If not, the entry is ignored for this feature.

## 3. Open a reveal window on `MODIFIER_ADD`

When gem sees:

```text
entry.log_type == "MODIFIER_ADD"
```

and the modifier is in the tracked set, gem creates a new `VisionModifierEvent`:

```python
VisionModifierEvent(
    tick=entry.tick,
    end_tick=None,
    modifier_name=entry.inflictor_name,
    target_name=entry.target_name,
    caster_name=entry.attacker_name,
    caster_team=0,  # filled later
)
```

This new event is:

- appended to `vision_modifier_events`
- pushed onto an "open events" stack keyed by `(modifier_name, target_name)`

That key choice is deliberate.

## Why the key is `(modifier_name, target_name)`

The same hero can receive the same modifier more than once.

Examples:

- Dust can be refreshed
- repeated applications can overlap in replay logs
- add/remove events may not always arrive in a perfectly simple single-window pattern

So gem does **not** use a single open event slot per modifier.

Instead it keeps:

```python
_open_vision_mods[(modifier_name, target_name)] = list[VisionModifierEvent]
```

That list behaves like a stack.

This gives two practical benefits:

1. refreshed or overlapping applications do not immediately destroy earlier state
2. a later `MODIFIER_REMOVE` can close the most recent still-open application first

This is a pragmatic replay-parsing choice, not a claim about Valve internals.

## 4. Close a reveal window on `MODIFIER_REMOVE`

When gem sees:

```text
entry.log_type == "MODIFIER_REMOVE"
```

for a tracked modifier, it looks up:

```python
key = (modifier_name, target_name)
```

If an open stack exists, gem:

1. pops the most recently opened event
2. sets its `end_tick = entry.tick`

This is effectively LIFO matching.

That means:

- the newest open application closes first
- older still-open applications remain until matched or left open

This is the most defensible matching strategy once you admit that refreshes and overlaps can happen in the combat-log stream.

## 5. Back-fill `caster_team` after parse

When the modifier event is first created, gem does **not** yet assign a final team.

It initially sets:

```python
caster_team = 0
```

After parse completes, gem builds a map from hero NPC name to team using player snapshots:

```python
_team_by_npc = {snap.npc_name: snap.team for snap in player_ext.snapshots if snap.team}
```

Then it back-fills:

```python
vev.caster_team = _team_by_npc.get(vev.caster_name, 0)
```

Why this happens after parse:

- team mapping is more reliable once player extraction has finished
- the modifier event can be captured immediately, then enriched afterward

## Exact decision logic

Conceptually, the collection logic is:

```text
for each combat log entry:
    if entry is MODIFIER_ADD and modifier is tracked:
        create VisionModifierEvent(end_tick=None)
        append to global list
        push onto open stack keyed by (modifier_name, target_name)

    if entry is MODIFIER_REMOVE and modifier is tracked:
        find the open stack for (modifier_name, target_name)
        if stack exists:
            pop newest event
            set end_tick = entry.tick

after parse:
    back-fill caster_team from hero -> team mapping
```

## Why `end_tick` can be `None`

`end_tick` stays `None` when gem sees an add but never sees a matching remove.

That can happen for several reasons:

- the replay ends while the modifier is still active
- the replay is truncated
- the combat-log stream did not contain the remove event gem expected

This is not necessarily a bug. It means:

> gem observed the reveal begin, but did not observe a clean close

In downstream analysis, that should be interpreted as:

- "active until observed otherwise"
- not "guaranteed active forever"

## Why this is useful

This structure turns one-off combat-log lines into explicit visibility windows.

That unlocks queries like:

- how long was this hero under Track?
- was Corrosive Haze active at the moment of the gank?
- did Dust overlap with the initiation window?
- did the enemy team have a reveal-based reason to see this hero?

Without this structure, every one of those questions would need to be reconstructed manually from raw combat-log entries.

## Relationship to `estimate_vision`

`estimate_vision` consumes `match.vision_modifiers` later as one of its vision-source inputs.

The simplified relationship is:

1. `match.vision_modifiers` captures reveal windows
2. `estimate_vision` checks whether a reveal window is active at tick `t`
3. if it is active, the revealed hero contributes a modifier-based visibility source

So:

- `match.vision_modifiers` is the event stream
- `estimate_vision` is the visibility query layer built on top of it

## What this feature does well

It does well when the question is:

- "was a reveal-style modifier active?"
- "who was revealed?"
- "for how long?"
- "which team applied the reveal?"

Those are exactly the questions the structure is designed to answer.

## What this feature does not do

It does **not** do these things:

- reconstruct every vision-affecting mechanic in Dota
- model the exact geometry of Dust or Gem aura coverage
- guarantee that every relevant modifier in the game is tracked
- infer visibility without an observed tracked modifier event

It is intentionally narrow and explicit.

## Known limitations

Current limitations include:

- only a curated set of modifiers is tracked
- matching uses pragmatic LIFO stack logic, not engine-internal state
- `caster_team` can remain `0` if back-fill fails
- `end_tick` can remain `None`
- replay truncation can leave windows apparently open
- downstream interpretation still depends on sampled hero positions when the event stream is used inside `estimate_vision`

## Example analysis patterns

### How long was a hero under Track?

```python
for ev in match.vision_modifiers:
    if ev.modifier_name == "modifier_bounty_hunter_track":
        duration = ((ev.end_tick or match.game_end_tick) - ev.tick) / 30
        print(f"{ev.target_name} tracked for {duration:.1f}s")
```

### Which reveal windows were active at a specific tick?

```python
active = [
    ev
    for ev in match.vision_modifiers
    if ev.tick <= tick and (ev.end_tick is None or tick <= ev.end_tick)
]
```

### Which team applied the most tracked reveals?

```python
from collections import Counter

counts = Counter(ev.caster_team for ev in match.vision_modifiers)
print(counts)
```

## Thought process behind the design

The design is intentionally conservative.

Instead of claiming to solve "true Dota vision", gem splits the problem:

1. preserve replay-observed reveal windows faithfully enough
2. expose them as explicit structured events
3. let downstream helpers like `estimate_vision` consume them

That separation makes the system easier to debug and easier to refine.

If the visibility interpretation looks wrong, you can ask:

- was the raw modifier event missing?
- was the window opened or closed incorrectly?
- was the downstream geometric query too loose or too strict?

That is much better than one opaque monolithic vision heuristic.

## Code locations

If you want to inspect or tune the implementation:

- `src/gem/__init__.py`
- `src/gem/models.py`
- `src/gem/match_builder.py`
- `src/gem/analysis.py`
- `docs/reference/analysis.md`

## Related reading

1. [Estimate Vision](./estimate-vision.md)
2. [Analysis Helpers](../reference/analysis.md)
3. [Replay Edge Cases](../deep-dives/replay-edge-cases.md)
