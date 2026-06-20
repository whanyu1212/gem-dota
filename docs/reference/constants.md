# Constants

Display-name helpers and lookup tables backed by bundled dotaconstants data.

---

## Generated API

## Module `gem.constants`

Backward-compatible facade for Dota catalog lookups.

Source: [src/gem/constants.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L1)

### Top-level functions

### `hero_display`

```python
def hero_display(npc_name: str) -> str
```

Return the localized display name for an ``npc_dota_hero_*`` string.

Source: [src/gem/constants.py:69](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L69)

### `hero_short`

```python
def hero_short(npc_name: str) -> str
```

Return display name from either a full ``npc_dota_hero_*`` or a bare suffix.

Source: [src/gem/constants.py:81](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L81)

### `hero_npc_name`

```python
def hero_npc_name(name: str) -> str | None
```

Resolve a display name to its ``npc_dota_hero_*`` NPC name.

Source: [src/gem/constants.py:93](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L93)

### `hero_meta`

```python
def hero_meta(npc_name: str) -> dict[str, Any]
```

Return the full hero metadata dict, or an empty dict if not found.

Source: [src/gem/constants.py:105](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L105)

### `item_display`

```python
def item_display(internal: str) -> str
```

Return display name for an ``item_*`` prefixed internal name.

Source: [src/gem/constants.py:117](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L117)

### `item_key_by_id`

```python
def item_key_by_id(item_id: int) -> str | None
```

Return the internal item key for an item ability ID.

Source: [src/gem/constants.py:129](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L129)

### `ability_display`

```python
def ability_display(internal: str) -> str
```

Return display name for an ability or item internal name.

Source: [src/gem/constants.py:141](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L141)

### `xp_to_next_level`

```python
def xp_to_next_level(level: int, current_xp: int) -> int | None
```

Return XP needed to reach the next level, or None at max level.

Source: [src/gem/constants.py:153](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L153)

### `permanent_buff_name`

```python
def permanent_buff_name(buff_id: int) -> str
```

Return the item name for a permanent buff integer ID.

Source: [src/gem/constants.py:166](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L166)

### `league_name`

```python
def league_name(leagueid: int) -> str | None
```

Return the league name for a given league ID, or None if unknown/not found.

Source: [src/gem/constants.py:178](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L178)
