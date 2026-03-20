# Models

Output dataclasses produced by `gem.parse()`.

See also: [Full Match Data](../guides/04_match_data.md), [Quickstart](../guides/01_quickstart.md)

## Notable recent fields

- `ParsedMatch.radiant_team_id` / `dire_team_id`: `int` — tournament team ID (matches OpenDota `/teams/{id}` URL). `0` for pub games.
- `ParsedMatch.radiant_team_name` / `dire_team_name`: `str` — team name (e.g. `"Xtreme Gaming"`). Empty string for pub games.
- `ParsedMatch.radiant_team_tag` / `dire_team_tag`: `str` — team tag (e.g. `"XG"`). Empty string for pub games.
- `ParsedPlayer.steam_id`: `int` — 64-bit Steam ID. `0` if unavailable.
- `ParsedPlayer.account_id`: `int` — 32-bit account ID (the ID in OpenDota/Dotabuff player URLs). `0` if unavailable.
- `ParsedMatch.vision_modifiers`: `list[VisionModifierEvent]` *(experimental)* — every application of a vision-granting modifier (Slardar Corrosive Haze, BH Track, Dust of Appearance, Gem of True Sight). See [`estimate_vision`](analysis.md) for how these integrate with the vision API.
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