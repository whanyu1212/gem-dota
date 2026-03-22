# Constants

Display-name helpers and lookup tables backed by bundled dotaconstants data.

---

## Generated API

## Module `gem.constants`

Dota 2 game constants — heroes, items, abilities, XP thresholds.

Source: [src/gem/constants.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L1)

### Top-level functions

### `hero_display`

```python
def hero_display(npc_name: str) -> str
```

Return the localized display name for an ``npc_dota_hero_*`` string.

Source: [src/gem/constants.py:52](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L52)

### `hero_short`

```python
def hero_short(npc_name: str) -> str
```

Return display name from either a full ``npc_dota_hero_*`` or a bare suffix.

Source: [src/gem/constants.py:67](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L67)

### `hero_npc_name`

```python
def hero_npc_name(name: str) -> str | None
```

Resolve a display name to its ``npc_dota_hero_*`` NPC name.

Source: [src/gem/constants.py:81](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L81)

### `hero_meta`

```python
def hero_meta(npc_name: str) -> dict
```

Return the full hero metadata dict, or an empty dict if not found.

Source: [src/gem/constants.py:108](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L108)

### `item_display`

```python
def item_display(internal: str) -> str
```

Return display name for an ``item_*`` prefixed internal name.

Source: [src/gem/constants.py:125](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L125)

### `ability_display`

```python
def ability_display(internal: str) -> str
```

Return display name for an ability or item internal name.

Source: [src/gem/constants.py:176](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L176)

### `xp_to_next_level`

```python
def xp_to_next_level(level: int, current_xp: int) -> int | None
```

Return XP needed to reach the next level, or None at max level.

Source: [src/gem/constants.py:202](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L202)

### `permanent_buff_name`

```python
def permanent_buff_name(buff_id: int) -> str
```

Return the item name for a permanent buff integer ID.

Source: [src/gem/constants.py:222](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L222)

### `league_name`

```python
def league_name(leagueid: int) -> str | None
```

Return the league name for a given league ID, or None if unknown/not found.

Source: [src/gem/constants.py:239](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/constants.py#L239)
