"""Export the data behind the docs site's home page figures.

The home page (``site/src/pages/index.astro``) shows real gem output: Table 1 is
the winning team's players, Figure 1 is gem's map model over the 7.41 map,
Figure 2 is every ward placed in the match, and Figure 3 is the match's biggest
fight with a narration of its events. This script writes them to a committed
snapshot, so building the site never parses a replay:

- ``site/src/data/home.json``: the match and its players; the map overlay (half
  line, river, lotus pools, every neutral camp); the wards; and the fight's
  hero paths, deaths and events. Map positions are in the coordinates of a
  1000-unit square;
- ``site/src/data/fight.json``: the fight's playback, loaded when Figure 3 comes
  into view: each hero's sampled position, HP and mana, and the fight's casts
  (with the heroes each hit and the damage it did), damage, disables, buffs,
  deaths with their gold and XP, and buybacks, from ``gem.build_fight_timeline``;
- ``site/src/assets/home-map.jpg``: the plain map square the overlays sit on;
- ``site/src/assets/home-fight.jpg``: a sharper crop of the map around the fight;
- ``site/src/assets/icons/``: the observer and sentry icons, the fight's hero
  icons (``heroes/<name>.png``) and the items used in it (``items/<name>.png``),
  copied from the icons that
  ``scripts/fetch_item_icons.py`` and ``scripts/fetch_hero_icons.py`` download.

Hero paths, death spots, HP and mana are sampled (about one per second); ward
positions and the combat log are exact.

The overlay comes from ``map_constants.json`` and ``camp_zones.json`` and is
placed with the report maps' calibrated window (``MAP_XMIN``…``MAP_YMAX``), the
same projection as ``scripts/render_readme_banner.py``.

Usage (defaults to the TI2026 fixture 8856501050, the committed snapshot)::

    uv run python scripts/export_site_home_data.py [replay.dem]
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from collections.abc import Callable, Iterable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import gem  # noqa: E402
from gem.analysis.fight_timeline import FightTimeline, build_fight_timeline  # noqa: E402
from gem.catalog.abilities import ABILITIES, ability_display  # noqa: E402
from gem.catalog.items import ITEMS, item_display  # noqa: E402
from gem.catalog.map import load_camp_zones, load_map_constants  # noqa: E402
from gem.constants import hero_display  # noqa: E402
from gem.extractors.fights import Fight  # noqa: E402
from gem.extractors.wards import WardEvent  # noqa: E402
from gem.reports._formatting import MAP_XMAX, MAP_XMIN, MAP_YMAX, MAP_YMIN  # noqa: E402
from gem.results.models import ParsedMatch, ParsedPlayer  # noqa: E402

# TI2026 match 8856501050 (93 minutes, 221 wards, a 10-death fight at 42:34).
# The committed snapshot is this match.
DEFAULT_REPLAY = REPO_ROOT / "tests" / "fixtures" / "opendota" / "8856501050.dem"
DEFAULT_DATA = REPO_ROOT / "site" / "src" / "data" / "home.json"
DEFAULT_FIGHT_DATA = REPO_ROOT / "site" / "src" / "data" / "fight.json"
DEFAULT_MAP_IMAGE = REPO_ROOT / "site" / "src" / "assets" / "home-map.jpg"
DEFAULT_FIGHT_IMAGE = REPO_ROOT / "site" / "src" / "assets" / "home-fight.jpg"
DEFAULT_ICONS = REPO_ROOT / "site" / "src" / "assets" / "icons"
SOURCE_MAP = REPO_ROOT / "assets" / "maps" / "Game_map_7.41.jpg"
ITEM_ICONS = REPO_ROOT / "src" / "gem" / "data" / "item_icons"
HERO_ICONS = REPO_ROOT / "src" / "gem" / "data" / "hero_icons"

#: The overlay's coordinate square, and the map image's size in pixels.
SIZE = 1000
IMAGE_PX = 1200
#: World units around the fight's centroid whose hero paths frame the fight crop.
FIGHT_RADIUS = 2600
#: A sampled jump longer than this (world units) is a teleport or respawn, not a path.
PATH_JUMP = 900
TICKS_PER_SECOND = 30
#: Observer ward vision radius, as in gem's point-vision model (analysis/vision.py).
OBSERVER_VISION = 1600
TEAMS = {2: "radiant", 3: "dire"}
#: The playback runs on this long after the last death, for an instant buyback
#: and the last death's gold.
PLAYBACK_TAIL_TICKS = 2 * TICKS_PER_SECOND
#: Buffs the playback draws as a ring around the hero (the site's choice of what
#: to show; every modifier is in the timeline).
BUFF_RINGS = {
    "modifier_black_king_bar_immune": "bkb",
    "modifier_minotaur_horn_immune": "bkb",
    "modifier_ghost_state": "ghost",
    "modifier_item_blade_mail_reflect": "blade_mail",
    "modifier_item_lotus_orb_active": "lotus",
    "modifier_item_satanic_unholy": "satanic",
    "modifier_item_aeon_disk_buff": "aeon_disk",
}
#: Names for disables whose modifier doesn't name its ability.
DISABLE_NAMES = {
    "modifier_stunned": "Stun",
    "modifier_bashed": "Bash",
    "modifier_knockback": "Knockback",
    "modifier_ancientapparition_coldfeet_freeze": "Cold Feet",
}


def _project(x: float, y: float) -> list[float]:
    fx = (x - MAP_XMIN) / (MAP_XMAX - MAP_XMIN)
    fy = 1.0 - (y - MAP_YMIN) / (MAP_YMAX - MAP_YMIN)
    return [round(fx * SIZE, 1), round(fy * SIZE, 1)]


def map_overlay() -> dict:
    """gem's regions and camps, projected onto the map square."""
    regions = load_map_constants()["regions"]
    camps = load_camp_zones()["camps"]
    return {
        "size": SIZE,
        "half_line": [_project(*point) for point in regions["half_line"]],
        "river": [_project(*point) for point in regions["river_outline"]],
        "lotus_radius": round(regions["lotus_radius"] / (MAP_XMAX - MAP_XMIN) * SIZE, 1),
        "lotus_pools": [_project(pool["x"], pool["y"]) for pool in regions["lotus_pools"].values()],
        "camps": [
            {"type": camp["type"], "at": _project(camp["center"]["x"], camp["center"]["y"])}
            for camp in camps
        ],
    }


def write_map_image(path: Path, box: list[float] | None = None) -> None:
    """The map square (the report maps' window), or a ``[x, y, size]`` crop of it, as a JPEG."""
    from PIL import Image

    x, y, size = box or [0.0, 0.0, float(SIZE)]
    with Image.open(SOURCE_MAP) as image:
        side = image.height
        left = (image.width - side) // 2
        scale = side / SIZE
        region = (
            round(left + x * scale),
            round(y * scale),
            round(left + (x + size) * scale),
            round((y + size) * scale),
        )
        square = image.convert("RGB").crop(region)
        square = square.resize((IMAGE_PX, IMAGE_PX), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    square.save(path, "JPEG", quality=85, optimize=True, progressive=True)


def load_match(replay: Path) -> ParsedMatch:
    """Parse the replay (kept separate so tests can supply a match)."""
    return gem.parse(replay)


def _unit_name(npc_name: str) -> str:
    """A readable name for a hero, or a tidied NPC name for anything else."""
    if npc_name.startswith("npc_dota_hero_"):
        return hero_display(npc_name)
    name = npc_name.removeprefix("npc_dota_")
    name = name.replace("goodguys", "radiant").replace("badguys", "dire")
    return name.replace("_", " ").strip().capitalize() or "Unknown"


def _clock(match: ParsedMatch, tick: int) -> str:
    clock = match.game_clock
    return clock.format_tick(tick) if clock is not None else f"tick {tick}"


def wards_snapshot(match: ParsedMatch, tick: int | None) -> dict:
    """The wards up at ``tick`` (the fight's first death), and whole-match counts by region.

    A ward is up from its placement tick until it was killed or expired. Each
    observer carries its vision radius (1600, the radius gem's point-vision
    model uses); sentries reveal invisible units and get no map-vision circle.
    """
    wards = [ward for ward in match.wards if ward.x is not None and ward.y is not None]
    by_region: dict[str, dict[str, int]] = {}
    for ward in wards:
        region = gem.region_of(ward.x, ward.y)  # type: ignore[arg-type]
        counts = by_region.setdefault(ward.ward_type, {})
        counts[region] = counts.get(region, 0) + 1

    def is_up(ward: WardEvent) -> bool:
        gone = [t for t in (ward.killed_tick, ward.expires_tick) if t is not None]
        return tick is not None and ward.tick <= tick < min(gone, default=tick + 1)

    radius = round(OBSERVER_VISION / (MAP_XMAX - MAP_XMIN) * SIZE, 1)
    return {
        "totals": {kind: sum(counts.values()) for kind, counts in by_region.items()},
        "by_region": {
            kind: dict(sorted(counts.items(), key=lambda item: -item[1]))
            for kind, counts in by_region.items()
        },
        "up": [
            {
                "type": ward.ward_type,
                "team": TEAMS.get(ward.team, "unknown"),
                "at": _project(ward.x, ward.y),  # type: ignore[arg-type]
                **({"vision_radius": radius} if ward.ward_type == "observer" else {}),
            }
            for ward in wards
            if is_up(ward)
        ],
    }


Point = tuple[float, float]
Sample = tuple[float, float, int]  # world x, world y, replay tick


def _paths(player: ParsedPlayer, start: int, end: int) -> list[list[Sample]]:
    """The player's sampled path in [start, end], split at teleports and respawns."""
    runs: list[list[Sample]] = []
    last: Point | None = None
    for tick, x, y in player.position_log:
        if not start <= tick <= end:
            continue
        if last is None or math.dist(last, (x, y)) > PATH_JUMP:
            runs.append([])
        runs[-1].append((x, y, tick))
        last = (x, y)
    return runs


def _crop(points: list[Point]) -> list[float]:
    """A square ``[x, y, size]`` in map-square units around the points, kept on the map."""
    projected = [_project(*point) for point in points]
    x0, x1 = min(p[0] for p in projected), max(p[0] for p in projected)
    y0, y1 = min(p[1] for p in projected), max(p[1] for p in projected)
    size = min(float(SIZE), max(x1 - x0, y1 - y0, 160.0) + 80.0)
    left = min(max((x0 + x1 - size) / 2, 0.0), SIZE - size)
    top = min(max((y0 + y1 - size) / 2, 0.0), SIZE - size)
    return [round(left, 1), round(top, 1), round(size, 1)]


def biggest_fight(match: ParsedMatch) -> Fight | None:
    """The fight with the most deaths (the earliest of equals), or ``None``."""
    return max(match.fights, key=lambda f: (f.deaths, -f.start_tick), default=None)


def _seconds_since(match: ParsedMatch, start_tick: int) -> Callable[[int], float]:
    """In-game seconds since ``start_tick``, for the playback.

    Pause-aware, like the clock times the narration shows; raw replay ticks only
    when the replay has no game clock.
    """
    clock = match.game_clock
    start_s = clock.game_time_at(start_tick) if clock is not None else None

    def since(tick: int) -> float:
        now_s = clock.game_time_at(tick) if clock is not None else None
        if now_s is not None and start_s is not None:
            return round(now_s - start_s, 1)
        return round((tick - start_tick) / TICKS_PER_SECOND, 1)

    return since


def fight_snapshot(match: ParsedMatch) -> dict | None:
    """The match's biggest fight: hero paths, death spots, events and team totals."""
    fight = biggest_fight(match)
    if fight is None:
        return None
    by_slot = {player.player_id: player for player in match.players}
    by_hero = {player.hero_name: player for player in match.players}

    def side(player: ParsedPlayer | None) -> str:
        return TEAMS.get(player.team, "unknown") if player else "unknown"

    events: list[tuple[int, str, str]] = []  # (tick, team colour, text)
    deaths: list[tuple[str, str, Point, int]] = []  # (hero, team, world spot, tick)
    for smoke in gem.build_smoke_analysis(match):
        if smoke.first_fight is fight:
            count = len(smoke.members)
            team = TEAMS.get(smoke.team, "unknown")
            heroes = "hero" if count == 1 else "heroes"
            events.append(
                (smoke.activation_tick, team, f"{team.capitalize()} smoked {count} {heroes}")
            )
    for entry in match.combat_log:
        if not fight.start_tick <= entry.tick <= fight.end_tick:
            continue
        kind = str(entry.log_type)
        victim = by_hero.get(entry.target_name)
        # Aegis and Reincarnation triggers are not deaths, as in detect_fights().
        if (
            kind == "DEATH"
            and entry.target_is_hero
            and not entry.target_is_illusion
            and not entry.will_reincarnate
            and victim
        ):
            killer = by_hero.get(entry.attacker_name)
            text = f"{_unit_name(entry.attacker_name)} killed {hero_display(victim.hero_name)}"
            events.append((entry.tick, side(killer), text))
            spot = gem.position_at_tick(victim, entry.tick)
            if spot is not None:
                deaths.append((hero_display(victim.hero_name), side(victim), spot, entry.tick))
        elif kind == "BUYBACK" and entry.value in by_slot:
            buyer = by_slot[entry.value]
            events.append((entry.tick, side(buyer), f"{hero_display(buyer.hero_name)} bought back"))
    events.sort(key=lambda event: event[0])

    # Paths run from the window's start to the last death: the walk away afterwards
    # would only clutter the figure.
    last_death = fight.last_death_tick or fight.end_tick
    paths = [
        (player, run)
        for player in match.players
        for run in _paths(player, fight.start_tick, last_death)
    ]
    # Keep the paths near the fight: heroes elsewhere (or walking back from the
    # fountain) would stretch the crop to the whole map.
    points = [(x, y) for _, run in paths for x, y, _tick in run]
    if fight.centroid_x is not None and fight.centroid_y is not None:
        centre: Point = (fight.centroid_x, fight.centroid_y)
    elif points:
        centre = (sum(p[0] for p in points) / len(points), sum(p[1] for p in points) / len(points))
    else:
        return None
    near = [
        (player, run)
        for player, run in paths
        if any(math.dist((x, y), centre) <= FIGHT_RADIUS for x, y, _tick in run)
    ]
    framed = [
        (x, y)
        for _, run in near
        for x, y, _tick in run
        if math.dist((x, y), centre) <= FIGHT_RADIUS
    ] + [spot for _, _, spot, _ in deaths] or [centre]

    since = _seconds_since(match, fight.start_tick)

    totals = {"radiant": {"gold": 0, "xp": 0}, "dire": {"gold": 0, "xp": 0}}
    for row in fight.players:
        team = side(by_slot.get(row.player_id))
        if team in totals:
            totals[team]["gold"] += row.gold_delta
            totals[team]["xp"] += row.xp_delta

    return {
        "first_death_tick": fight.first_death_tick,
        "first_death": _clock(match, fight.first_death_tick) if fight.first_death_tick else None,
        "duration_s": since(last_death),
        "start": _clock(match, fight.start_tick),
        "end": _clock(match, fight.end_tick),
        "deaths": fight.deaths,
        "radiant_kills": fight.radiant_kills,
        "dire_kills": fight.dire_kills,
        "winner": fight.winner,
        "totals": totals,
        "box": _crop(framed),
        "paths": [
            {
                "hero": hero_display(player.hero_name),
                "icon": player.hero_name.removeprefix("npc_dota_hero_"),
                "team": side(player),
                # [x, y, seconds since the window's start], for the playback.
                "points": [[*_project(x, y), since(tick)] for x, y, tick in run],
            }
            for player, run in near
        ],
        "deaths_at": [
            {"hero": hero, "team": team, "at": _project(*spot), "t": since(tick)}
            for hero, team, spot, tick in deaths
        ],
        "events": [
            {"time": _clock(match, tick), "t": since(tick), "team": team, "text": text}
            for tick, team, text in events
        ],
    }


def _ability_name(name: str) -> str:
    """The display name of an ability or item (``Avalanche``, ``Black King Bar``)."""
    return item_display(name) if name.startswith("item_") else ability_display(name)


def _source_name(source: str) -> str:
    """A damage source's display name; ``"Attack"`` for a right-click."""
    return _ability_name(source) if source not in ("", "dota_unknown") else "Attack"


def _disable_name(modifier: str) -> str:
    """A display name for a disabling modifier, from the ability it names."""
    if modifier in DISABLE_NAMES:
        return DISABLE_NAMES[modifier]
    name = modifier.removeprefix("modifier_")
    for suffix in ("_stunned", "_stun", "_debuff", "_freeze", "_fear", "_slow"):
        name = name.removesuffix(suffix)
    if name in ITEMS:
        return item_display(name)
    if name in ABILITIES:
        return ABILITIES[name]
    return ability_display(name)


def _hero_runs(
    player: ParsedPlayer, start: int, end: int, since: Callable[[int], float]
) -> list[list[list[float]]]:
    """The hero's samples in [start, end] as runs split at teleports and respawns.

    Each sample is ``[t, x, y, hp, max_hp, mana, max_mana]``: seconds since the
    window's start, the map-square position, and the hero's HP and mana at the
    same tick.
    """
    state = {
        tick: (hp, top, mana, top_mana)
        for tick, hp, top, mana, top_mana in zip(
            player.times,
            player.hp_t,
            player.max_hp_t,
            player.mana_t,
            player.max_mana_t,
            strict=False,
        )
    }
    runs = []
    for run in _paths(player, start, end):
        samples = []
        for x, y, tick in run:
            hp, top, mana, top_mana = state.get(tick, (0, 0, 0.0, 0.0))
            samples.append([since(tick), *_project(x, y), hp, top, round(mana), round(top_mana)])
        runs.append(samples)
    return runs


def fight_playback(match: ParsedMatch) -> dict | None:
    """The biggest fight's playback: hero state and the fight's timeline.

    Heroes are referred to by their index in ``heroes``. Every ``t`` is seconds
    since the fight window's start (the same origin as ``home.json``'s fight).
    """
    fight = biggest_fight(match)
    if fight is None:
        return None
    start = fight.start_tick
    end = (fight.last_death_tick or fight.end_tick) + PLAYBACK_TAIL_TICKS
    since = _seconds_since(match, start)
    timeline: FightTimeline = build_fight_timeline(match, start, end)
    players = sorted(match.players, key=lambda p: p.player_id)
    index = {player.hero_name: i for i, player in enumerate(players)}

    def hero(name: str | None) -> int | None:
        return index.get(name) if name else None

    casts = []
    for cast in timeline.casts:
        row: dict = {
            "t": since(cast.tick),
            "by": index[cast.caster],
            "what": _ability_name(cast.ability),
            "hits": [
                [index[hit.hero], hit.damage, hit.damage_type, round(hit.stun_s, 1)]
                for hit in cast.hits
            ],
        }
        if cast.is_item:
            row["item"] = cast.ability.removeprefix("item_")
        if cast.target is not None and cast.target != cast.caster:
            if cast.target_is_hero:
                row["target"] = index[cast.target]
            else:
                row["unit"] = _unit_name(cast.target)
        if cast.self_effect is not None or cast.target == cast.caster:
            row["self"] = True
        casts.append(row)

    team_of = {i: TEAMS.get(player.team, "unknown") for i, player in enumerate(players)}
    deaths = []
    for death in timeline.deaths:
        rewards = timeline.rewards_at(death.tick)
        deaths.append(
            {
                "t": since(death.tick),
                "victim": index[death.victim],
                "killer": hero(death.killer_hero),
                "killer_name": _unit_name(death.killer),
                "aegis": death.reincarnated,
                "gold_lost": death.gold_lost,
                "gold": [
                    [index[h], g]
                    for h, g in (rewards.gold if rewards else {}).items()
                    if h in index
                ],
                "xp": [
                    [index[h], x] for h, x in (rewards.xp if rewards else {}).items() if h in index
                ],
                "recent": [
                    [
                        _unit_name(taken.attacker_hero or taken.attacker),
                        _source_name(taken.source),
                        taken.damage_type,
                        taken.damage,
                    ]
                    for taken in death.recent_damage[:6]
                ],
            }
        )
    return {
        "start": _clock(match, start),
        "duration": since(end),
        "heroes": [
            {
                "hero": hero_display(player.hero_name),
                "icon": player.hero_name.removeprefix("npc_dota_hero_"),
                "team": team_of[i],
                "runs": _hero_runs(player, start, end, since),
            }
            for i, player in enumerate(players)
        ],
        "casts": casts,
        # [t, attacker, target, damage, type, by the hero itself (not a summon or
        # illusion), source ("Attack" for a right-click)]
        "damage": [
            [
                since(burst.start_tick),
                index[burst.attacker_hero],
                index[burst.target],
                burst.damage,
                burst.damage_type,
                int(burst.attacker == burst.attacker_hero and not burst.attacker_is_illusion),
                _source_name(burst.source),
            ]
            for burst in timeline.damage
            if burst.attacker_hero in index and burst.target in index
        ],
        # [t, target, source hero or null, name, seconds]
        "disables": [
            [
                since(window.start_tick),
                index[window.target],
                hero(window.source_hero),
                _disable_name(window.modifier),
                round(window.stun_s, 1),
            ]
            for window in timeline.disables
            if window.start_tick is not None
        ],
        # [t, until, hero, kind]. A buff still on at the window's end runs to the
        # end; one added before the window is left out, since when it started
        # isn't in the window.
        "buffs": [
            [
                since(window.start_tick),
                since(window.end_tick) if window.end_tick is not None else since(end),
                index[window.target],
                BUFF_RINGS[window.modifier],
            ]
            for window in timeline.modifiers
            if window.modifier in BUFF_RINGS and window.start_tick is not None
        ],
        "deaths": deaths,
        # [t, hero, cost]
        "buybacks": [[since(b.tick), index[b.hero], b.cost] for b in timeline.buybacks],
    }


def write_icons(icons_dir: Path, heroes: set[str], items: Iterable[str] = ()) -> None:
    """Copy the ward icons, and the given heroes' and items' icons, into the site.

    Hero and ward icons are required. An item without a downloaded icon is
    skipped: the playback shows its name instead.

    Raises:
        SystemExit: When an icon hasn't been downloaded yet.
    """
    copies = [
        (ITEM_ICONS / f"{kind}.png", icons_dir / f"{kind}.png")
        for kind in ("ward_observer", "ward_sentry")
    ]
    copies += [
        (HERO_ICONS / f"{hero}.png", icons_dir / "heroes" / f"{hero}.png")
        for hero in sorted(heroes)
    ]
    missing = [str(source) for source, _ in copies if not source.is_file()]
    if missing:
        raise SystemExit(
            "Missing icons; run scripts/fetch_item_icons.py and scripts/fetch_hero_icons.py first:\n  "
            + "\n  ".join(missing)
        )
    copies += [
        (ITEM_ICONS / f"{item}.png", icons_dir / "items" / f"{item}.png")
        for item in sorted(items)
        if (ITEM_ICONS / f"{item}.png").is_file()
    ]
    for folder in ("heroes", "items"):
        if (icons_dir / folder).is_dir():
            shutil.rmtree(icons_dir / folder)  # drop icons from an earlier match
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def match_snapshot(match: ParsedMatch) -> dict:
    """The match facts the home page shows."""
    return {
        "match_id": match.match_id,
        "radiant_team": match.radiant_team_name,
        "dire_team": match.dire_team_name,
        "radiant_win": match.radiant_win,
        "radiant_score": match.radiant_score,
        "dire_score": match.dire_score,
        "duration_s": match.duration,
        "players": [
            {
                "hero": hero_display(player.hero_name),
                "team": "radiant" if player.team == 2 else "dire",
                "kills": player.kills,
                "deaths": player.deaths,
                "assists": player.assists,
                "net_worth": player.net_worth,
                "gold_per_min": player.gold_per_min,
            }
            for player in match.players
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("replay", nargs="?", type=Path, default=DEFAULT_REPLAY)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--fight-data", type=Path, default=DEFAULT_FIGHT_DATA)
    parser.add_argument("--map-image", type=Path, default=DEFAULT_MAP_IMAGE)
    parser.add_argument("--fight-image", type=Path, default=DEFAULT_FIGHT_IMAGE)
    parser.add_argument("--icons-dir", type=Path, default=DEFAULT_ICONS)
    args = parser.parse_args(argv)

    match = load_match(args.replay)
    fight = fight_snapshot(match)
    data = {
        "match": match_snapshot(match),
        "map": map_overlay(),
        "wards": wards_snapshot(match, fight["first_death_tick"] if fight else None),
        "fight": fight,
    }
    args.data.parent.mkdir(parents=True, exist_ok=True)
    args.data.write_text(json.dumps(data, indent=1) + "\n")
    playback = fight_playback(match)
    args.fight_data.parent.mkdir(parents=True, exist_ok=True)
    # Compact: the playback is loaded by the browser, so every byte counts.
    args.fight_data.write_text(json.dumps(playback, separators=(",", ":")) + "\n")
    write_map_image(args.map_image)
    written = [args.data, args.fight_data, args.map_image]
    if fight is not None:
        write_map_image(args.fight_image, fight["box"])
        written.append(args.fight_image)
    heroes = {hero["icon"] for hero in playback["heroes"]} if playback else set()
    items = {cast["item"] for cast in playback["casts"] if "item" in cast} if playback else set()
    write_icons(args.icons_dir, heroes, items)
    written.append(args.icons_dir)
    print("Wrote " + ", ".join(str(path) for path in written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
