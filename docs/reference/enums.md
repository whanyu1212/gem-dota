# Reference Values (Enums)

Some output fields are represented as integer codes for compatibility with replay/network data.
This page documents commonly used values.

> These are practical reference mappings, not strict guarantees for all historical/future patches.

---

## Team values

Used in multiple output fields (for example, attacker/target team in combat entries).

| Value | Meaning |
|---:|---|
| `2` | Radiant |
| `3` | Dire |
| `0` | Unknown / unset |

---

## Common game mode values

`ParsedMatch.game_mode` is an integer code.

| Value | Meaning |
|---:|---|
| `1` | All Pick |
| `2` | Captains Mode |
| `3` | Random Draft |
| `4` | Single Draft |
| `22` | Ranked All Pick |

---

## Common lobby type values

`ParsedMatch.lobby_type` is an integer code.

| Value | Meaning |
|---:|---|
| `0` | Public matchmaking |
| `1` | Practice |
| `7` | Ranked matchmaking |

---

## EntityOp bit flags

`EntityOp` is an `IntFlag` bitmask used in entity callbacks.

| Flag | Value | Meaning |
|---|---:|---|
| `CREATED` | `1` | Entity created this tick |
| `UPDATED` | `2` | One or more fields changed |
| `DELETED` | `4` | Entity removed |
| `ENTERED` | `8` | Entity entered PVS |
| `LEFT` | `16` | Entity left PVS |

Example:

```python
if op & EntityOp.CREATED:
    ...
if op & EntityOp.UPDATED:
    ...
```

See also: [Models](models.md), [Entities](entities.md)
