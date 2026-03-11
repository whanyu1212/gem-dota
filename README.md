# gem

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?logo=opensourceinitiative&logoColor=white)
![Phase](https://img.shields.io/badge/phase-10%20of%2012-blue)
![Coverage](https://img.shields.io/badge/coverage-77%25-green)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

**Gem of True Sight** — a Python Dota 2 replay parser.

Reads Source 2 `.dem` binary replay files and exposes structured output: per-tick hero state, combat events, ward placements, smoke usage, Roshan kills, gold/XP timelines, draft picks/bans, courier state, ability levels, and more.

---

## Why gem?

Existing parsers (Clarity, Manta, OpenDota/parser) are built for backend services in Java or Go. `gem` brings that to Python without touching JVM toolchains — with a clean API designed for data science and ML workflows.

```python
import gem

match = gem.parse("my_replay.dem")

# Draft — who was picked and banned?
for event in match.draft:
    action = "PICK" if event.is_pick else "BAN"
    print(f"{action}: {gem.constants.hero_display(event.hero_name)}")

# Per-player summary
for player in match.players:
    print(
        f"{player.player_name} ({gem.constants.hero_display(player.hero_name)}): "
        f"{player.kills}/{player.deaths}/{player.assists}  "
        f"{player.net_worth:,} NW  {player.stuns_dealt:.1f}s stuns"
    )
```

```python
# Gold/XP timeline as DataFrames
dfs = gem.parse_to_dataframe("my_replay.dem")
snapshots = dfs["snapshots"]   # one row per player per sample tick
combat    = dfs["combat_log"]  # all combat log entries
```

---

## Implementation Status

| Phase | Scope | Status |
|---|---|---|
| 1 | `BitReader`, `DemoStream` — binary frame iteration | ✅ Complete |
| 2 | `sendtable`, `field_decoder`, `field_path` — schema layer | ✅ Complete |
| 3 | String tables, entity lifecycle, game events, combat log | ✅ Complete |
| 4 | `gem.constants` — bundled hero/item/ability display names | ✅ Complete |
| 5 | Extractors — player timelines, objectives, ward coordinates | ✅ Complete |
| 6 | `gem.parse()` — `ParsedMatch`/`ParsedPlayer`, DataFrame export, CLI | ✅ Complete |
| 7 | Rune pickups, buybacks, aegis, lane heatmaps, chat, purchase log, movement heatmap | ✅ Complete |
| 8 | Ability levels, courier state, draft extraction, stun duration | ✅ Complete |
| 9 | Teamfight detection — per-player breakdown, minimap report | ✅ Complete |
| 10 | Validation against OpenDota API, fuzz tests, gold/XP advantage curves | ✅ Complete |
| 11 | Performance — benchmark tooling, Python optimisations, Rust extension (PyO3) | 🚧 Planned |
| 12 | Distribution — PyPI packaging, CI/CD | 🚧 Planned |

---

## What you can extract

| Data | Field / Source |
|---|---|
| Hero picks and bans with timestamps | `ParsedMatch.draft` |
| Courier state snapshots per team | `ParsedMatch.courier_snapshots` |
| Ability levels per hero per tick | `PlayerStateSnapshot.ability_levels` |
| Stun seconds dealt per player | `ParsedPlayer.stuns_dealt` |
| Damage, heals, kills, assists, deaths | `ParsedPlayer.damage` etc. |
| Gold and net worth over time | `ParsedPlayer.snapshots` |
| Ward placements with exact coordinates | `ParsedMatch.wards` |
| Smoke of Deceit activations + groups | `ParsedMatch.wards` (smoke entries) |
| Roshan kills + aegis events | `ParsedMatch.roshans`, `.aegis_events` |
| Rune pickups per player | `ParsedPlayer.runes_log` |
| Buybacks per player | `ParsedPlayer.buyback_log` |
| Tower and barracks kills | `ParsedMatch.towers`, `.barracks` |
| Lane position heatmaps | `ParsedPlayer.lane_pos` |
| Chat messages | `ParsedMatch.chat` |
| Purchase log per player | `ParsedPlayer.purchase_log` |
| Hero display names, item/ability names | `gem.constants` |
| Teamfights with per-player stats (damage, deaths, buybacks, XP) | `ParsedMatch.teamfights` |
| Teamfight minimap report with hero icons and live filters | `examples/teamfight_report.py` |
| Radiant gold / XP advantage curves (per-minute) | `ParsedMatch.radiant_gold_adv`, `.radiant_xp_adv` |
| Match info from Steam API (K/D/A, GPM, XPM, hero damage) | `examples/steam_match_info.py` |

---

## Installation

Requires Python 3.10+. Uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

```bash
git clone https://github.com/whanyu1212/gem
cd gem
uv sync
```

---

## Quick start

```bash
# Full replay summary — combat log + entity snapshots
python examples/extraction_demo.py path/to/your.dem

# Ward placements, smoke groups, Roshan kills
python examples/ward_smoke_rosh.py path/to/your.dem

# Interactive movement heatmap (Plotly)
python examples/movement_heatmap.py path/to/your.dem

# HTML draft summary with hero icons
python scripts/fetch_hero_icons.py          # one-time icon download
python examples/draft_summary.py path/to/your.dem

# HTML teamfight report — minimap, hero icons, live filters
python examples/teamfight_report.py path/to/your.dem

# Match info from Steam API (requires STEAM_API_KEY env var)
python examples/steam_match_info.py <match_id>
```

---

## Documentation

Full concepts, tutorials, and API reference at the project docs site (built with MkDocs Material):

```bash
uv run mkdocs serve
```

Topics covered: DEM binary format, varint encoding, Protocol Buffers, the entity delta system, combat log ingestion, and known data limitations.

---

## Known limitations

- **Roshan drops** — Aegis, Cheese, Refresher Shard, and Aghanim's Blessing pickups are not in the combat log. Roshan kills are tracked, but the specific drop items are not.
- **Smoke empty groups** — if a smoke breaks instantly on activation (hero inside sentry truesight), the group list will be empty. This is correct game behaviour, not a parsing gap.
- **Hero icons** — not bundled in the package. Run `python scripts/fetch_hero_icons.py` to download them locally before using `examples/draft_summary.py` or `examples/teamfight_report.py`.
