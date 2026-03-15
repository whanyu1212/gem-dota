# Models

Output dataclasses produced by `gem.parse()`.

See also: [Full Match Data](../guides/04_match_data.md), [Quickstart](../guides/01_quickstart.md)

## Notable recent fields

- `ParsedMatch.tormentors`: `list[TormentorKill]` — chronological Tormentor kill events.
- `ParsedMatch.shrines`: `list[ShrineKill]` — chronological Shrine of Wisdom destruction events.
- `ParsedPlayer.damage_by_type`: `dict[str, int]` — total damage dealt by damage type (`physical`, `magical`, `pure`).
- `ParsedPlayer.damage_taken_by_type`: `dict[str, int]` — total damage taken by damage type.
- `ParsedPlayer.buyback_log`: `list[CombatLogEntry]` — buyback events attributed to the player.
- `ParsedPlayer.lane_efficiency_pct`: `int` — lane efficiency percentage derived from lane gold.

## TormentorKill

- `tick`: game tick of the kill.
- `killer`: NPC name of the killing unit.
- `killer_player_id`: player slot (`0-9`) of the killer when resolved, else `-1`.
- `kill_number`: sequential Tormentor kill number in the match.

::: gem.models