# Catalog

Grouped accessors for bundled Dota metadata and static map data.

`gem.constants` remains available as a compatibility facade; new code can use
`gem.catalog` or the more specific `gem.catalog.*` modules.

---

## Generated API

## Module `gem.catalog.heroes`

Hero catalog lookups backed by bundled dotaconstants data.

Source: [src/gem/catalog/heroes.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/heroes.py#L1)

### Top-level functions

### `hero_display`

```python
def hero_display(npc_name: str) -> str
```

Return the localized display name for an ``npc_dota_hero_*`` string.

Source: [src/gem/catalog/heroes.py:16](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/heroes.py#L16)

### `hero_short`

```python
def hero_short(npc_name: str) -> str
```

Return display name from either a full ``npc_dota_hero_*`` or a bare suffix.

Source: [src/gem/catalog/heroes.py:31](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/heroes.py#L31)

### `hero_npc_name`

```python
def hero_npc_name(name: str) -> str | None
```

Resolve a display name to its ``npc_dota_hero_*`` NPC name.

Source: [src/gem/catalog/heroes.py:45](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/heroes.py#L45)

### `hero_meta`

```python
def hero_meta(npc_name: str) -> dict[str, Any]
```

Return the full hero metadata dict, or an empty dict if not found.

Source: [src/gem/catalog/heroes.py:71](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/heroes.py#L71)

## Module `gem.catalog.items`

Item and permanent-buff catalog lookups.

Source: [src/gem/catalog/items.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/items.py#L1)

### Top-level functions

### `item_display`

```python
def item_display(internal: str) -> str
```

Return display name for an ``item_*`` prefixed internal name.

Source: [src/gem/catalog/items.py:24](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/items.py#L24)

### `item_key_by_id`

```python
def item_key_by_id(item_id: int) -> str | None
```

Return the internal item key for an item ability ID.

Source: [src/gem/catalog/items.py:38](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/items.py#L38)

### `permanent_buff_name`

```python
def permanent_buff_name(buff_id: int) -> str
```

Return the item name for a permanent buff integer ID.

Source: [src/gem/catalog/items.py:50](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/items.py#L50)

## Module `gem.catalog.abilities`

Ability catalog lookups backed by bundled dotaconstants data.

Source: [src/gem/catalog/abilities.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/abilities.py#L1)

### Top-level functions

### `ability_display`

```python
def ability_display(internal: str) -> str
```

Return display name for an ability or item internal name.

Source: [src/gem/catalog/abilities.py:44](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/abilities.py#L44)

## Module `gem.catalog.xp`

Hero experience threshold catalog.

Source: [src/gem/catalog/xp.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/xp.py#L1)

### Top-level functions

### `xp_to_next_level`

```python
def xp_to_next_level(level: int, current_xp: int) -> int | None
```

Return XP needed to reach the next level, or None at max level.

Source: [src/gem/catalog/xp.py:14](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/xp.py#L14)

## Module `gem.catalog.leagues`

League catalog lookups.

Source: [src/gem/catalog/leagues.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/leagues.py#L1)

### Top-level functions

### `league_name`

```python
def league_name(leagueid: int) -> str | None
```

Return the league name for a given league ID, or None if unknown/not found.

Source: [src/gem/catalog/leagues.py:14](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/leagues.py#L14)

## Module `gem.catalog.map`

Map catalog lookups for static map and neutral-camp data.

Source: [src/gem/catalog/map.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/map.py#L1)

### Top-level functions

### `load_camp_zones`

```python
def load_camp_zones() -> dict[str, Any]
```

Load calibrated neutral-camp zone geometry.

Source: [src/gem/catalog/map.py:13](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/map.py#L13)

### `load_map_constants`

```python
def load_map_constants() -> dict[str, Any]
```

Load static map calibration constants.

Source: [src/gem/catalog/map.py:22](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/map.py#L22)

### `load_neutral_camps`

```python
def load_neutral_camps() -> list[dict[str, Any]]
```

Load static neutral-camp center data.

Source: [src/gem/catalog/map.py:31](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/map.py#L31)

### `load_neutral_camp_centers`

```python
def load_neutral_camp_centers() -> dict[int, tuple[float, float]]
```

Load neutral camp IDs mapped to world-coordinate centers.

Source: [src/gem/catalog/map.py:40](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/map.py#L40)

## Module `gem.catalog.resources`

Bundled catalog resource loading.

Source: [src/gem/catalog/resources.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/resources.py#L1)

### Top-level functions

### `load_data_text`

```python
def load_data_text(name: str) -> str
```

Load a bundled data file as text.

Source: [src/gem/catalog/resources.py:16](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/resources.py#L16)

### `load_data_json`

```python
def load_data_json(name: str) -> Any
```

Load a bundled JSON data file.

Source: [src/gem/catalog/resources.py:28](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/catalog/resources.py#L28)
