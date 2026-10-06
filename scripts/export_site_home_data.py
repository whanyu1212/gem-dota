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
  into view: each hero's position, HP and mana on every replay packet, and the fight's casts
  (with the heroes each hit and the damage it did), damage, disables, buffs,
  deaths with their gold and XP, and buybacks, from ``gem.build_fight_timeline``;
- ``site/src/assets/home-map.jpg``: the plain map square the overlays sit on;
- ``site/src/assets/home-fight.jpg``: a sharper crop of the map around the fight;
- ``site/src/assets/icons/``: the observer and sentry icons, the fight's hero
  icons (``heroes/<name>.png``) and the items used in it (``items/<name>.png``),
  copied from the icons that
  ``scripts/fetch_item_icons.py`` and ``scripts/fetch_hero_icons.py`` download.

Figure 3's static hero paths and death spots are sampled (about one per second).
The playback reads every hero again on each replay packet in its window (every
other tick: the replay's own resolution), at the end of the packet, so a hit's
HP drop and a Blink's move land on the tick of their combat-log entry. Ward
positions and the combat log are exact.

The overlay comes from ``map_constants.json`` and ``camp_zones.json`` and is
placed with the map calibration (``gem.catalog.map``: ``MAP_XMIN``…``MAP_YMAX``), the
same projection as ``scripts/render_readme_banner.py``.

Usage (defaults to the TI2026 fixture 8856501050, the committed snapshot)::

    uv run python scripts/export_site_home_data.py [replay.dem]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import shutil
import sys
from collections import defaultdict
from collections.abc import Callable, Iterable
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import pandas as pd  # noqa: E402

import gem  # noqa: E402
from gem.analysis.fight_timeline import (  # noqa: E402
    FightTimeline,
    ModifierWindow,
    build_fight_timeline,
)
from gem.analysis.smoke import SmokeAnalysis  # noqa: E402
from gem.analysis.vision import OBSERVER_VISION_RADIUS  # noqa: E402
from gem.catalog.abilities import ABILITIES, ability_display  # noqa: E402
from gem.catalog.items import ITEMS, item_display  # noqa: E402
from gem.catalog.map import (  # noqa: E402
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    load_camp_zones,
    load_map_constants,
)
from gem.constants import hero_display  # noqa: E402
from gem.extractors.fights import Fight  # noqa: E402
from gem.extractors.wards import WardEvent  # noqa: E402
from gem.results.models import ParsedMatch, ParsedPlayer  # noqa: E402

# TI2026 match 8856501050 (93 minutes, 221 wards, a 10-death fight at 42:34).
# The committed snapshot is this match.
DEFAULT_REPLAY = REPO_ROOT / "tests" / "fixtures" / "opendota" / "8856501050.dem"
DEFAULT_DATA = REPO_ROOT / "site" / "src" / "data" / "home.json"
DEFAULT_FIGHT_DATA = REPO_ROOT / "site" / "src" / "data" / "fight.json"
DEFAULT_WARDS_DATA = REPO_ROOT / "site" / "src" / "data" / "wards.json"
#: The fights recipe's figure: an index and one file per fight.
DEFAULT_FIGHTS_DATA = REPO_ROOT / "site" / "src" / "data" / "fights"
COOKBOOK = REPO_ROOT / "examples" / "cookbook"
DEFAULT_OBJECTIVES_DATA = REPO_ROOT / "site" / "src" / "data" / "objectives.json"
DEFAULT_LEAD_DATA = REPO_ROOT / "site" / "src" / "data" / "lead.json"
DEFAULT_LANES_DATA = REPO_ROOT / "site" / "src" / "data" / "lanes.json"
DEFAULT_RUNES_DATA = REPO_ROOT / "site" / "src" / "data" / "runes.json"
DEFAULT_MAP_IMAGE = REPO_ROOT / "site" / "src" / "assets" / "home-map.jpg"
DEFAULT_FIGHT_IMAGE = REPO_ROOT / "site" / "src" / "assets" / "home-fight.jpg"
DEFAULT_ICONS = REPO_ROOT / "site" / "src" / "assets" / "icons"
#: Images the recipe figures use: Markdown pages can't go through Astro's image
#: pipeline, so these are served as they are.
DEFAULT_PUBLIC_FIGURES = REPO_ROOT / "site" / "public" / "figures"
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
#: Playback sample tolerances: a sample is dropped only when the straight line
#: between its neighbours puts the hero within this of it (map-square units for
#: the position, whole points for HP and mana), so the playback draws what the
#: replay says to well under a pixel.
POSITION_TOLERANCE = 0.1
POINTS_TOLERANCE = 0.49
TICKS_PER_SECOND = 30
#: Observer ward vision radius: gem's point-vision model (analysis/vision.py).
OBSERVER_VISION = OBSERVER_VISION_RADIUS
TEAMS = {2: "radiant", 3: "dire"}
#: The playback runs on this long after the last death, for an instant buyback
#: and the last death's gold.
PLAYBACK_TAIL_TICKS = 2 * TICKS_PER_SECOND
#: A smoked hero counts as seen when the enemy saw it within this long of the break.
SEEN_AFTER_BREAK_S = 1.0
#: Hidden spans shorter than this (fog flickering at the edge of vision) are left
#: out, so the badges don't flicker.
MIN_HIDDEN_S = 0.5
#: A smoke that led into the fight starts the playback when it came at most this
#: many game seconds before the fight window, so the playback shows the smoked walk-in.
SMOKE_LEAD_S = 60.0
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
#: How many damage sources a death's recap lists (its total covers them all).
RECAP_ROWS = 6
#: Names for modifiers that don't name their ability.
MODIFIER_NAMES = {
    "modifier_stunned": "Stun",
    "modifier_bashed": "Bash",
    "modifier_knockback": "Knockback",
    "modifier_ancientapparition_coldfeet_freeze": "Cold Feet",
}
#: Name fragments of disables that carry no stun time: hexes, silences, disarms,
#: roots and the like (a modifier with a stun time is a disable anyway).
DISABLE_FRAGMENTS = (
    "voodoo",
    "sheepstick",
    "hex",
    "silence",
    "disarm",
    "root",
    "taunt",
    "fear",
    "sleep",
    "cyclone",
    "stunned",
    "bashed",
    "knockback",
)
#: A hero's own modifier shorter than this (a dash, a cast's short state) is left
#: out of the feed: the cast row already says it.
MIN_SELF_BUFF_S = 1.5
#: Words dropped from a modifier name that names no ability or item.
GENERIC_WORDS = {"modifier", "item", "debuff", "buff", "active", "effect", "super", "slow"}
#: Name fragments of modifiers the feed leaves out: internal timers, cooldowns and
#: bookkeeping, not effects a viewer would read as a buff or a debuff.
NOISE_FRAGMENTS = (
    "_timer",
    "_internal_cd",
    "cooldown",
    "teleporting",
    "regeneration",
    "phase_boots",
    "respawn",
    "thinker",
    "_counter",
    "_charge",
)


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


def write_map_image(
    path: Path, box: list[float] | None = None, *, px: int = IMAGE_PX, webp: bool = False
) -> None:
    """The map square (the report maps' window), or a ``[x, y, size]`` crop of it, as a JPEG (or WebP)."""
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
        square = square.resize((px, px), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    if webp:
        square.save(path, "WEBP", quality=80, method=6)
    else:
        square.save(path, "JPEG", quality=85, optimize=True, progressive=True)


def write_public_figures(folder: Path, icons_dir: Path) -> None:
    """The map and the ward icons the recipe figures draw with, served from ``site/public``."""
    write_map_image(folder / "map.webp", px=1000, webp=True)
    for kind in ("ward_observer", "ward_sentry"):
        shutil.copyfile(icons_dir / f"{kind}.png", folder / f"{kind}.png")


def load_match(replay: Path) -> ParsedMatch:
    """Parse the replay (kept separate so tests can supply a match)."""
    return gem.parse(replay)


#: One hero reading: replay tick, world x and y, HP, max HP, mana, max mana and
#: life state (0 alive, 1 dying, 2 dead).
HeroState = tuple[int, float, float, int, int, float, float, int]


def load_hero_states(
    replay: Path, windows: Iterable[tuple[int, int]]
) -> dict[int, list[HeroState]]:
    """Every hero's state at the end of each replay packet in the windows, by player ID.

    A second parse, stopped after the last window. The replay sends entity updates once a
    packet (every other tick); reading at the packet's end means the state
    includes everything the packet's combat-log entries describe. Heroes are
    resolved the way ``PlayerExtractor`` resolves them, so illusions are skipped.
    Kept separate so tests can supply states.
    """
    from gem.extractors.players import PlayerExtractor, _build_hero_snapshot
    from gem.parser import ReplayParser

    spans = sorted(windows)
    parser = ReplayParser(replay)
    # Only for its hero resolution: one sample at the first tick, no minute marks.
    players = PlayerExtractor(sample_interval=sys.maxsize, minute_snapshots=False)
    players.attach(parser)
    states: dict[int, dict[int, HeroState]] = defaultdict(dict)

    def read(tick: int) -> None:
        if not any(start <= tick <= end for start, end in spans):
            return
        for player_id, entity in players._select_heroes().items():
            snap = _build_hero_snapshot(entity, tick, player_id)
            if snap.x is None or snap.y is None:
                continue
            # A tick's later packet overwrites its earlier one.
            states[player_id][tick] = (
                tick,
                snap.x,
                snap.y,
                snap.hp,
                snap.max_hp,
                snap.mana,
                snap.max_mana,
                snap.life_state,
            )

    # The completed-packet boundary: every delta and combat-log entry of the
    # packet has been applied (the parser's internal hook for a stable view).
    parser._on_packet_end(read)
    parser.stop_after_tick(max((end for _, end in spans), default=0))
    parser.parse()
    return {
        player_id: [by_tick[t] for t in sorted(by_tick)] for player_id, by_tick in states.items()
    }


#: Building, Roshan and Tormentor classes, for their places on the map.
_BUILDING_CLASSES = ("CDOTA_BaseNPC_Tower", "CDOTA_BaseNPC_Barracks", "CDOTA_BaseNPC_Fort")
_MOVING_CLASSES = {"CDOTA_Unit_Roshan": "roshan", "CDOTA_Unit_Miniboss": "tormentor"}
#: The wisdom-rune shrines: one in each side's jungle. The runes themselves are
#: no entity of their own in the replay.
_SHRINE_CLASS = "CDOTA_BaseNPC_XP_Fountain"


def _building_key(entity_name: str) -> str:
    """A building's EntityNames name as the combat log spells it (no npc_dota_ prefix).

    ``dota_goodguys_tower1_bot`` is ``goodguys_tower1_bot``; barracks differ:
    ``good_rax_melee_top`` is ``goodguys_melee_rax_top``. The two tier-4 towers
    keep their ``_bot``/``_top`` (the combat log names both ``tower4``).
    """
    if rax := re.fullmatch(r"(good|bad)_rax_(melee|range)_(\w+)", entity_name):
        return f"{rax.group(1)}guys_{rax.group(2)}_rax_{rax.group(3)}"
    return entity_name.removeprefix("dota_")


def load_map_places(replay: Path, until: int) -> dict:
    """Where the buildings stand, and where Roshan and the Tormentors were, from the replay.

    A pass over the replay's entities up to ``until``: every tower, barracks and
    Ancient by its combat-log name, with its world position; every position
    update of Roshan and the Tormentors, as ``(tick, x, y)``; and the two
    wisdom-rune shrines (``wisdom``). Kept separate so tests can supply places.
    """
    from gem.extractors._snapshots import _ENTITY_NAME_FIELDS, _pos
    from gem.parser import ReplayParser

    parser = ReplayParser(replay)
    buildings: dict[str, tuple[float, float]] = {}
    moving: dict[str, list[tuple[int, float, float]]] = {"roshan": [], "tormentor": []}
    shrines: list[tuple[float, float]] = []

    def on_entity(entity, _op) -> None:  # type: ignore[no-untyped-def]
        cls = entity.get_class_name()
        if cls == _SHRINE_CLASS:
            pos = _pos(entity)
            if pos and pos not in shrines:
                shrines.append(pos)
            return
        if cls in _MOVING_CLASSES:
            pos = _pos(entity)
            if pos:
                moving[_MOVING_CLASSES[cls]].append((parser.tick, pos[0], pos[1]))
            return
        if cls not in _BUILDING_CLASSES:
            return
        tables = parser.string_tables
        names = tables.get_by_name("EntityNames") if tables is not None else None
        index = entity._get_int32_resolved(entity._resolve_fields(_ENTITY_NAME_FIELDS)[0])
        item = names.items.get(index) if names is not None and index is not None else None
        pos = _pos(entity)
        if item and pos:
            buildings.setdefault(_building_key(item[0]), pos)

    parser.on_entity(on_entity)
    parser.stop_after_tick(until)
    parser.parse()
    return {"buildings": buildings, **moving, "wisdom": shrines}


def match_hero_states(match: ParsedMatch) -> dict[int, list[HeroState]]:
    """The match's own once-a-second hero samples, for a match without its replay."""
    states: dict[int, list[HeroState]] = {}
    for player in match.players:
        series = {
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
        states[player.player_id] = [
            (tick, x, y, *series.get(tick, (0, 0, 0.0, 0.0)), 0)
            for tick, x, y in player.position_log
        ]
    return states


def _unit_name(npc_name: str) -> str:
    """A readable name for a hero, or a tidied NPC name for anything else."""
    if npc_name.startswith("npc_dota_hero_"):
        return hero_display(npc_name)
    name = npc_name.removeprefix("npc_dota_")
    name = name.replace("goodguys", "radiant").replace("badguys", "dire")
    return name.replace("_", " ").strip().capitalize() or "Unknown"


def _ward_killer(npc_name: str) -> str:
    """Who killed a ward, for a reader: a hero, "a Radiant creep", or a tidied unit name."""
    for side, team in (("goodguys", "Radiant"), ("badguys", "Dire")):
        if npc_name.startswith(f"npc_dota_creep_{side}"):
            return f"a {team} creep"
    return _unit_name(npc_name) if npc_name else "unknown"


#: Fights with this many deaths or more get a playback (hero states and the
#: map) in the fights recipe; every fight gets its breakdown (the timeline).
PLAYBACK_MIN_DEATHS = 3


def _cookbook(name: str) -> ModuleType:  # a recipe, so a figure shows what it computes
    spec = importlib.util.spec_from_file_location(f"cookbook_{name}", COOKBOOK / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_LANES = {"top": "top", "mid": "middle", "bot": "bottom"}


def _objective_name(what: str) -> str:
    """A building or Roshan, for a reader: "Radiant tier 1 bottom tower", "Dire top ranged barracks"."""
    if what == "roshan":
        return "Roshan"
    side, _, rest = what.partition("_")
    team = {"goodguys": "Radiant", "badguys": "Dire"}.get(side, side.capitalize())
    if tower := re.fullmatch(r"tower(\d)(?:_(\w+))?", rest):
        lane = _LANES.get(tower.group(2) or "", "")
        return f"{team} tier {tower.group(1)}{f' {lane}' if lane else ''} tower"
    if rax := re.fullmatch(r"(melee|range)_rax_(\w+)", rest):
        kind = "melee" if rax.group(1) == "melee" else "ranged"
        return f"{team} {_LANES.get(rax.group(2), rax.group(2))} {kind} barracks"
    return f"{team} {'Ancient' if rest == 'fort' else rest.replace('_', ' ')}"


def fight_box(match: ParsedMatch, fight: Fight, states: dict[int, list[HeroState]]) -> list[float]:
    """The map crop for a fight's playback: the heroes' readings near the fight, and its deaths' centre."""
    start, end = playback_window(match, fight)
    readings = [
        (x, y) for runs in states.values() for tick, x, y, *_ in runs if start <= tick <= end
    ]
    if fight.centroid_x is not None and fight.centroid_y is not None:
        centre: Point = (fight.centroid_x, fight.centroid_y)
    elif readings:
        centre = (
            sum(p[0] for p in readings) / len(readings),
            sum(p[1] for p in readings) / len(readings),
        )
    else:
        return [0.0, 0.0, float(SIZE)]
    return _crop([p for p in readings if math.dist(p, centre) <= FIGHT_RADIUS] + [centre])


def fights_recipe(
    match: ParsedMatch, files: dict[int, str], boxes: dict[int, list[float]]
) -> list[dict]:
    """Every fight for the fights recipe's figure, from the recipe itself (``fight_table``).

    ``files`` names each fight's data file by fight number (``fights/7.json``, or
    ``fight.json`` for Figure 3's); ``boxes`` holds the map crop of each fight
    with a playback.
    """
    table = _cookbook("fights").fight_table(match)
    by_number = dict(enumerate(sorted(match.fights, key=lambda f: f.start_tick), start=1))
    fights = []
    for row in table.itertuples(index=False):
        fight = by_number[row.fight]
        at = (
            _project(fight.centroid_x, fight.centroid_y)
            if fight.centroid_x is not None and fight.centroid_y is not None
            else None
        )
        entry: dict = {
            "n": row.fight,
            "file": files[row.fight],
            "start": row.start,
            "start_s": round(row.start_s, 2),
            "duration": round(row.duration_s, 1),
            "deaths": row.deaths,
            "kills": [row.radiant_kills, row.dire_kills],
            "more": {"radiant": "r", "dire": "d"}.get(row.more_kills, "x"),
            "at": at,
            "gold": [int(row.radiant_gold), int(row.dire_gold)],
            "next": (
                [
                    _objective_name(row.next),
                    {"radiant": "r", "dire": "d"}.get(row.next_for, ""),
                    int(row.next_after_s),
                ]
                if isinstance(row.next, str)
                else None
            ),
        }
        if row.fight in boxes:
            entry["box"] = boxes[row.fight]
        fights.append(entry)
    return fights


def _killer_name(npc_name: str) -> str:
    """Who took an objective, for a reader: a hero, "a Radiant creep", "Dire siege"."""
    if npc_name.startswith("npc_dota_creep_"):
        return _ward_killer(npc_name)
    return _unit_name(npc_name) if npc_name else "unknown"


def objectives_recipe(match: ParsedMatch, places: dict) -> dict:
    """Every objective and each team's edges for the objectives recipe's figure.

    From the recipe itself (``examples/cookbook/objectives.py``), with places
    from the replay (``load_map_places``): every building at its position (the
    ones still standing too), Roshan where it was at each kill, each Tormentor
    at the spawn nearest its killer, and each wisdom rune at its side's shrine. A tier-4 tower is matched to the
    one of its side's two nearest the last hit's hero. Positions are in the
    map square; ``r``/``d`` is the side, ``c``/``o``/``n`` an edge's outcome
    (converted, other side first, nothing). ``wisdom`` has each spawn's two
    runes: who took each (``o`` its own side, ``x`` the other side, ``n`` nobody
    before the next spawn, ``e`` nobody before the game ended).
    """
    recipe = _cookbook("objectives")
    table = recipe.objective_table(match)
    damage = recipe.building_damage(match)
    edge_rows = recipe.edges(match, table)
    side = {"radiant": "r", "dire": "d"}
    heroes = {player.hero_name: player for player in match.players}
    world = places.get("buildings", {})
    standing = [
        {
            "key": key,
            "kind": "tower" if "tower" in key else "barracks" if "rax" in key else "ancient",
            "side": "r" if key.startswith("goodguys") else "d",
            "at": _project(*xy),
        }
        for key, xy in sorted(world.items())
    ]
    spawns: list[Point] = []
    for _tick, x, y in places.get("tormentor", []):
        if all(math.dist((x, y), s) > 500 for s in spawns):
            spawns.append((x, y))
    roshan = sorted(places.get("roshan", []))
    # Each wisdom shrine by the half of the map it stands in.
    shrines = {
        side[half.removesuffix("_half")]: xy
        for xy in places.get("wisdom", [])
        if (half := gem.region_of(*xy)) in ("radiant_half", "dire_half")
    }
    # Both sides can take their runes on the same tick: key by tick and hero.
    pickups = {(w["tick"], w["hero"]): w for w in recipe.wisdom_pickups(match)}

    def hero_at(name: str, tick: int) -> Point | None:
        player = heroes.get(name)
        return gem.position_at_tick(player, tick) if player is not None else None

    taken4: set[str] = set()
    objectives = []
    for row in table.itertuples(index=False):
        at: list[float] | None = None
        if row.kind in ("tower", "barracks"):
            key = row.name
            if key.endswith("tower4"):
                pair = [k for k in (f"{key}_bot", f"{key}_top") if k in world and k not in taken4]
                hero_spot = hero_at(row.last_hit, row.tick)
                if hero_spot is not None:
                    spot4: Point = hero_spot
                    pair.sort(key=lambda k: math.dist(world[k], spot4))
                key = pair[0] if pair else key
                taken4.add(key)
            at = _project(*world[key]) if key in world else None
        elif row.kind == "roshan" and roshan:
            before = [r for r in roshan if r[0] <= row.tick] or roshan[:1]
            at = _project(before[-1][1], before[-1][2])
        elif row.kind == "tormentor" and spawns:
            near = hero_at(row.last_hit, row.tick)
            spot = min(spawns, key=lambda s: math.dist(s, near)) if near is not None else spawns[0]
            at = _project(*spot)
        elif row.kind == "wisdom_rune":
            shrine = shrines.get(side.get(row.name.removesuffix("_wisdom_rune"), ""))
            at = _project(*shrine) if shrine else None
        hits = damage[(damage["name"] == row.name) & (damage["time_s"] == row.time_s)]
        objectives.append(
            {
                "kind": row.kind,
                "name": _objective_name(row.name)
                if row.kind in ("tower", "barracks")
                else "Wisdom rune"
                if row.kind == "wisdom_rune"
                else row.kind.capitalize(),
                "for": side.get(row.for_side or "", ""),
                "time_s": round(row.time_s, 1),
                "time": row.time,
                "at": at,
                "last_hit": _killer_name(row.last_hit),
                "damage": [
                    [hero_display(h.attacker) if h.attacker in heroes else "Creeps", int(h.damage)]
                    for h in hits.sort_values("damage", ascending=False).itertuples()
                ],
                "shared": bool(hits["shared"].any()) if len(hits) else False,
                "after": (
                    [int(row.after_fight), int(row.after_fight_s)]
                    if not pd.isna(row.after_fight)
                    else None
                ),
            }
        )
        pickup = pickups.get((row.tick, row.last_hit)) if row.kind == "wisdom_rune" else None
        if pickup is not None:
            # The shrine it was taken at, and the XP the picker's team got.
            objectives[-1]["spot"] = side.get(pickup["spot"], "")
            objectives[-1]["xp"] = int(pickup["xp"])
    fights = sorted(match.fights, key=lambda f: f.start_tick)
    edges = []
    for row in edge_rows.itertuples(index=False):
        took = [
            "Roshan" if name == "roshan" else _objective_name(name)
            for name in (row.took.split("; ") if isinstance(row.took, str) else [])
        ]
        entry: dict = {
            "team": side[row.team],
            "edge": row.edge,
            "number": int(row.number),
            "time": _clock(match, int(row.tick)),
            "outcome": {"converted": "c", "other side first": "o", "nothing": "n"}[row.outcome],
            "took": took,
            "after_s": None if pd.isna(row.after_s) else int(row.after_s),
        }
        if row.edge == "fight":
            fight = fights[int(row.number) - 1]
            entry["kills"] = [fight.radiant_kills, fight.dire_kills]
            # Who the first objective counted for, when it was the other side's.
            if row.outcome == "other side first":
                entry["by"] = "d" if row.team == "radiant" else "r"
        edges.append(entry)
    end_tick = match.post_game_tick or match.game_end_tick or 0
    return {
        "start_s": -90.0,
        "end_s": round(_game_seconds(match, end_tick), 1),
        "buildings": standing,
        "tormentor_spawns": [_project(*s) for s in spawns],
        "wisdom_spots": {key: _project(*xy) for key, xy in shrines.items()},
        "objectives": objectives,
        "edges": edges,
        "wisdom": [
            [
                int(w.spawn_s),
                side[w.spot],
                side.get(w.taken_by or "", ""),
                hero_display(w.hero) if isinstance(w.hero, str) else None,
                None if pd.isna(w.after_s) else int(w.after_s),
                {"own side": "o", "other side": "x", "not taken": "n", "game ended": "e"}[
                    w.outcome
                ],
            ]
            for w in recipe.wisdom_runes(match).itertuples(index=False)
        ],
    }


def lead_recipe(match: ParsedMatch) -> dict:
    """The gold and XP lead by source for the lead recipe's figure.

    From the recipe itself (``examples/cookbook/lead.py``): the game seconds of
    every reading (each minute and the end of the game), and for gold and XP the
    lead and each source's share of it (Radiant minus Dire, running totals, so a
    stretch's change is one reading minus another). Each hero's running gold in
    three groups (hero kills, lane and neutral creeps, everything else) and XP;
    the fights (number, start and end seconds, deaths, the side with more kills)
    and the objectives (kind, the side it counted for, seconds) for the strip.
    """
    recipe = _cookbook("lead")
    side = {"radiant": "r", "dire": "d"}

    def split(sources: pd.DataFrame) -> dict:
        frame = recipe.lead_by_source(sources).sort_values("time_s")
        names = [c for c in frame.columns if c not in ("match_id", "tick", "time_s", "lead")]
        return {
            "lead": [int(v) for v in frame["lead"]],
            "sources": [[name, [int(v) for v in frame[name]]] for name in names],
        }

    gold, xp = recipe.gold_sources(match), recipe.xp_sources(match)
    times = sorted(set(gold["time_s"]))
    heroes = []
    for player in sorted(match.players, key=lambda p: (p.team, p.player_id)):
        mine = gold[gold["player_id"] == player.player_id].sort_values("time_s")
        creeps = mine["lane_creeps"] + mine["neutral_creeps"]
        heroes.append(
            {
                "name": hero_display(player.hero_name),
                "side": side.get(TEAMS.get(player.team, ""), ""),
                "gold": [
                    [int(v) for v in mine["hero_kills"]],
                    [int(v) for v in creeps],
                    [int(v) for v in mine["total"] - mine["hero_kills"] - creeps],
                ],
                "xp": [
                    int(v)
                    for v in xp[xp["player_id"] == player.player_id].sort_values("time_s")["total"]
                ],
            }
        )
    fights = []
    for number, fight in enumerate(sorted(match.fights, key=lambda f: f.start_tick), start=1):
        r, d = fight.radiant_kills, fight.dire_kills
        more = "r" if r > d else "d" if d > r else ""
        start_s = _game_seconds(match, fight.start_tick)
        fights.append([number, start_s, _game_seconds(match, fight.end_tick), fight.deaths, more])
    table = _cookbook("objectives").objective_table(match)
    return {
        "times": [round(float(t), 1) for t in times],
        "gold": split(gold),
        "xp": split(xp),
        "heroes": heroes,
        "fights": fights,
        "objectives": [
            [row.kind, side.get(row.for_side or "", ""), round(float(row.time_s), 1)]
            for row in table.itertuples(index=False)
        ],
    }


def lanes_recipe(match: ParsedMatch) -> dict:
    """Each lane's heroes, numbers and events for the lanes recipe's figure.

    From the recipe itself (``examples/cookbook/lanes.py``): the readings (game
    seconds), and for each lane each side's heroes (with the share of the
    laning stage each spent there) and, at each reading, its net worth, XP,
    last hits, denies and gold from lane creeps, hero kills, neutrals and the
    rest. Then every event up to the last reading, ``jungle`` and ``""`` lanes
    included (the figure lists those apart), and the heroes whose OpenDota
    ``lane`` (over 10 minutes) is another.
    """
    recipe = _cookbook("lanes")
    lanes = recipe.hero_lanes(match)
    table = recipe.lane_table(match, lanes)
    events = recipe.lane_events(match, lanes)
    side = {"radiant": "r", "dire": "d"}
    share = dict(zip(lanes["hero"], lanes["share"], strict=True))
    numbers = [
        "net_worth", "xp", "last_hits", "denies",
        "lane_creep_gold", "hero_kill_gold", "neutral_gold", "other_gold",
    ]  # fmt: skip
    out_lanes = []
    for lane in ("top", "mid", "bot"):
        rows = table[table["lane"] == lane]
        sides = {}
        for name, key in side.items():
            mine = rows[rows["side"] == name]
            heroes = [h for h in (mine["heroes"].iloc[0].split(", ") if len(mine) else []) if h]
            sides[key] = {
                "heroes": [[hero_display(h), float(share[h])] for h in heroes],
                "at": {
                    str(int(row.reading_s)): [int(getattr(row, n)) for n in numbers]
                    for row in mine.itertuples(index=False)
                },
            }
        out_lanes.append({"lane": lane, "sides": sides})
    # OpenDota's lane ids; 0 (no lane) is left out.
    lane_names = {1: "bot", 2: "mid", 3: "top", 4: "jungle", 5: "jungle"}
    home = dict(zip(lanes["hero"], lanes["lane"], strict=True))
    return {
        "readings": [recipe.LANE_S, recipe.COMPARE_S],
        "min_visit_s": recipe.MIN_VISIT_S,
        "lanes": out_lanes,
        "events": [
            [
                int(e.time_s),
                None if pd.isna(e.end_s) else int(e.end_s),
                e.kind,
                e.lane,
                hero_display(e.hero),
                side.get(e.side or "", ""),
                _killer_name(e.by) if isinstance(e.by, str) and e.by else None,
                e.from_lane if isinstance(e.from_lane, str) and e.from_lane else None,
            ]
            for e in events.itertuples(index=False)
        ],
        "opendota": [
            [hero_display(p.hero_name), lane_names[p.lane], home[p.hero_name]]
            for p in match.players
            if p.lane in lane_names and lane_names[p.lane] != home.get(p.hero_name)
        ],
    }


def _rune_objective(name: str) -> str:
    """An objective a power rune's window was followed by, for a reader."""
    return "Tormentor" if name == "tormentor" else _objective_name(name)


def runes_recipe(match: ParsedMatch) -> dict:
    """Every rune, the 0:00 bounties and the power runes' windows for the runes recipe's figure.

    From the recipe itself (``examples/cookbook/runes.py``). Each rune is
    ``[time_s, rune, spot, outcome, hero, side, whose, used_s]``: the game
    second it left the map (its spawn's for a rune still there), its name, its
    spot, how it ended, the taker's hero and side (``r``/``d``), a bounty's
    ``river``/``own``/``other``, and a bottled rune's use. Each spot is placed
    on the map square at the mean of its runes' positions. Each window is
    ``[start_s, end_s, rune, hero, side, from_bottle, died, killed, roshan
    damage, building damage, [[objective, seconds after start_s], ...]]``.
    """
    recipe = _cookbook("runes")
    table = recipe.rune_table(match)
    side = {"radiant": "r", "dire": "d"}

    def hero(name: object) -> str | None:
        return hero_display(name) if isinstance(name, str) and name else None

    # Down to the tenth, so a time reads on the figure's clock as it does in the recipe's.
    def number(value: object) -> float | None:
        if value is None or pd.isna(value):
            return None
        return math.floor(float(value) * 10) / 10  # type: ignore[arg-type]

    spots = {
        spot: _project(float(rows["x"].mean()), float(rows["y"].mean()))
        for spot, rows in table.groupby("spot")
    }
    runes = [
        [
            number(r.time_s if r.time_s is not None and not pd.isna(r.time_s) else r.spawn_s),
            r.rune,
            r.spot,
            r.outcome,
            hero(r.hero),
            side.get(r.side or "", ""),
            r.whose if isinstance(r.whose, str) else None,
            number(r.used_s),
        ]
        for r in table.itertuples(index=False)
    ]
    openers = recipe.opening_bounties(match, table)
    deaths = recipe.opening_deaths(match)
    windows = recipe.rune_windows(match)
    end_tick = match.post_game_tick or match.game_end_tick or 0
    return {
        "start_s": 0.0,
        "end_s": round(_game_seconds(match, end_tick), 1) if end_tick else 0.0,
        "stages": [[name, start, end] for name, start, end in recipe.STAGES],
        "near": recipe.NEAR,
        "opening_s": recipe.OPENING_S,
        "after_s": recipe.AFTER_S,
        "spots": spots,
        "runes": runes,
        "openers": [
            [
                o.spot,
                hero(o.hero),
                side.get(o.side or "", ""),
                o.whose,
                number(o.after_horn_s),
                [hero_display(h) for h in o.enemies_near.split(", ") if h],
            ]
            for o in openers.itertuples(index=False)
        ],
        "deaths": [
            [number(d.time_s), hero(d.hero), side.get(d.side or "", ""), _killer_name(d.by)]
            for d in deaths.itertuples(index=False)
        ],
        "windows": [
            [
                number(w.start_s),
                number(w.end_s),
                w.rune,
                hero(w.hero),
                side.get(w.side or "", ""),
                bool(w.from_bottle),
                bool(w.died),
                [hero_display(h) for h in w.killed.split(", ") if h],
                int(w.roshan_damage),
                int(w.building_damage),
                [
                    [_rune_objective(name), int(after)]
                    for name, after in zip(
                        [n for n in w.took.split(", ") if n],
                        [a for a in w.took_s.split(", ") if a],
                        strict=True,
                    )
                ],
            ]
            for w in windows.itertuples(index=False)
        ],
    }


#: The wards recipe's figure opens on Figure 3's fight, with this much on each
#: side (whole minutes).
WARD_RANGE_PAD_S = 120


def wards_recipe(match: ParsedMatch) -> dict:
    """Every ward for the wards recipe's figure (``site/src/data/wards.json``).

    Each ward is ``[team, type, x, y, placed_s, ended_s, how, placer, killer,
    placed, ended]``: ``r``/``d``, ``o``/``s``, the map-square position, the
    in-game seconds it went up and ended (pauses excluded), ``k`` killed, ``e``
    expired or ``u`` up when the recording ended, the placer's hero (joined on
    the player slot), who killed it, and gem's clock (``format_tick``) for the
    two times. A ward is up from ``placed_s`` until ``ended_s`` (half open).
    """
    clock = match.game_clock
    heroes = {player.player_id: player.hero_name for player in match.players}
    end_tick = match.post_game_tick or match.game_end_tick or 0

    def seconds(tick: int) -> float:
        return round(_game_seconds(match, tick), 1)

    wards: list[list] = []
    placed: list[float] = []
    for ward in sorted(match.wards, key=lambda w: w.tick):
        if ward.x is None or ward.y is None or ward.team not in TEAMS:
            continue
        if ward.killed_tick is not None:
            ended, how = ward.killed_tick, "k"
        elif ward.expires_tick is not None:
            ended, how = ward.expires_tick, "e"
        else:
            ended, how = end_tick, "u"
        placer = heroes.get(ward.player_id) or ward.placer
        placed.append(seconds(ward.tick))
        wards.append(
            [
                TEAMS[ward.team][0],
                ward.ward_type[0],
                *_project(ward.x, ward.y),
                seconds(ward.tick),
                seconds(ended),
                how,
                hero_display(placer) if placer else "unknown",
                _ward_killer(ward.killer) if how == "k" else "",
                _clock(match, ward.tick),
                _clock(match, ended),
            ]
        )
    fight = biggest_fight(match)
    default = None
    if fight is not None and clock is not None:
        start, end = playback_window(match, fight)
        default = [
            math.floor((_game_seconds(match, start) - WARD_RANGE_PAD_S) / 60) * 60,
            math.ceil((_game_seconds(match, end) + WARD_RANGE_PAD_S) / 60) * 60,
        ]
    return {
        "start_s": min([-90.0, *placed]),
        "end_s": seconds(end_tick),
        "radius": round(OBSERVER_VISION / (MAP_XMAX - MAP_XMIN) * SIZE, 1),
        "range": default,
        "wards": wards,
    }


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


def _game_seconds(match: ParsedMatch, tick: int) -> float:
    """The game clock at ``tick`` in seconds (pause-aware); raw ticks without a clock."""
    clock = match.game_clock
    now = clock.game_time_at(tick) if clock is not None else None
    return round(now if now is not None else tick / TICKS_PER_SECOND, 1)


def _clock_base(match: ParsedMatch, start: int, end: int) -> float:
    """The playback clock's reading at ``start``: ``floor(base + t)`` is gem's clock.

    gem shows OpenDota's whole seconds (``game_seconds_at``), which round the raw
    seconds and the game start separately, so a second doesn't turn over where the
    exact game time crosses a whole number. The offset between the two is fixed
    for a match: this finds it from every tick in the window, checks one offset
    fits them all, and adds half a tick so rounding ``t`` to the hundredth can't
    tip a second.
    """
    clock = match.game_clock
    exact = clock.game_time_at(start) if clock is not None else None
    if clock is None or exact is None:
        return _game_seconds(match, start)
    low, high = -math.inf, math.inf
    for tick in range(start, end + 1):
        now, shown = clock.game_time_at(tick), clock.game_seconds_at(tick)
        if now is None or shown is None:
            continue
        low, high = max(low, shown - now), min(high, shown + 1 - now)
    half_tick = 0.5 / TICKS_PER_SECOND
    if not low + half_tick + 0.005 < high:
        raise ValueError(f"no single clock offset fits ticks {start}-{end}")
    return round(exact + low + half_tick, 4)


def _seconds_since(match: ParsedMatch, start_tick: int, places: int = 1) -> Callable[[int], float]:
    """In-game seconds since ``start_tick``, rounded to ``places`` decimals.

    Pause-aware, like the clock times the narration shows; raw replay ticks only
    when the replay has no game clock. Two places keep every tick distinct (a
    tick is 1/30 s).
    """
    clock = match.game_clock
    start_s = clock.game_time_at(start_tick) if clock is not None else None

    def since(tick: int) -> float:
        now_s = clock.game_time_at(tick) if clock is not None else None
        if now_s is not None and start_s is not None:
            return round(now_s - start_s, places)
        return round((tick - start_tick) / TICKS_PER_SECOND, places)

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


def _modifier_name(modifier: str) -> str:
    """A display name for a modifier, from the ability or item its name starts with.

    ``modifier_lion_voodoo`` is Hex, ``modifier_item_shivas_guard_blast`` Shiva's
    Guard: trailing words are dropped until the rest names an item or an ability.
    """
    if modifier in MODIFIER_NAMES:
        return MODIFIER_NAMES[modifier]
    words = modifier.removeprefix("modifier_").removeprefix("item_").split("_")
    for n in range(len(words), 0, -1):
        name = "_".join(words[:n])
        if name in ITEMS:
            return item_display(name)
        if name in ABILITIES:
            return ABILITIES[name]
    # No ability or item by that name: tidy the words (dropping a hero prefix).
    kept = [w for w in words if w not in GENERIC_WORDS] or words
    return ability_display("_".join(kept))


def _applied_seconds(window: ModifierWindow) -> float:
    """The duration a modifier was applied with: its stun time, or the log's duration.

    ``0.0`` when the log gives none: a missing duration, or its ``-1`` sentinel.
    """
    if window.stun_s > 0:
        return window.stun_s
    return window.duration_s if window.duration_s is not None and window.duration_s > 0 else 0.0


def _modifier_kind(window: ModifierWindow, team_of: dict[str, int]) -> str | None:
    """``disable``, ``debuff`` or ``buff`` for the feed, or ``None`` to leave it out."""
    name = window.modifier
    if window.aura or window.start_tick is None or any(f in name for f in NOISE_FRAGMENTS):
        return None
    stun = window.stun_s > 0
    enemy = team_of.get(window.source_hero or "") != team_of.get(window.target)
    # A name fragment marks a disable only on an enemy (Eul's on yourself is a save).
    if stun or (enemy and window.source_hero and any(f in name for f in DISABLE_FRAGMENTS)):
        return "disable"  # kept even without a duration: the feed shows how long it lasted
    if _applied_seconds(window) <= 0:
        return None  # passives, auras and -1 ("no duration") the log gives no time for
    if window.source_hero is None:
        return None
    if window.source_hero == window.target and _applied_seconds(window) < MIN_SELF_BUFF_S:
        return None  # a dash or a cast's own short state: the cast row says it
    return "buff" if team_of.get(window.source_hero) == team_of.get(window.target) else "debuff"


def _hero_runs(
    states: list[HeroState], start: int, end: int, since: Callable[[int], float]
) -> list[list[list[float]]]:
    """The hero's samples in [start, end] as runs split at teleports, deaths and respawns.

    Each sample is ``[t, x, y, hp, max_hp, mana, max_mana]``: seconds since the
    window's start, the map-square position, and the hero's HP and mana at the
    same tick. Only living heroes have samples. A lone jump longer than ``PATH_JUMP``
    is a teleport (a Blink, a respawn), so the run breaks there; a run of long
    jumps is fast movement (a dash) and stays one path. Samples the client's
    straight-line interpolation already reproduces are dropped (``_thin``).
    """
    alive: list[list[HeroState]] = [[]]
    for state in states:
        if not start <= state[0] <= end:
            continue
        # Dying or dead: the playback hides a hero from its death, and the next
        # sample is a respawn, a buyback or an Aegis.
        if state[7] != 0:
            if alive[-1]:
                alive.append([])
            continue
        alive[-1].append(state)
    runs: list[list[HeroState]] = []
    for stretch in alive:
        jumps = [
            math.dist(a[1:3], b[1:3]) > PATH_JUMP
            for a, b in zip(stretch, stretch[1:], strict=False)
        ]
        run: list[HeroState] = []
        for i, state in enumerate(stretch):
            # jumps[i - 1] is the step into this sample; a teleport is one alone.
            if (
                i
                and jumps[i - 1]
                and not (i >= 2 and jumps[i - 2])
                and not (i < len(jumps) and jumps[i])
            ):
                runs.append(run)
                run = []
            run.append(state)
        if run:
            runs.append(run)
    return [
        _thin(
            [
                [since(tick), *_project(x, y), hp, top, round(mana), round(top_mana)]
                for tick, x, y, hp, top, mana, top_mana, _ in run
            ]
        )
        for run in runs
    ]


def _thin(samples: list[list[float]]) -> list[list[float]]:
    """Drop the samples that straight lines between the kept ones reproduce.

    Greedy: from each kept sample, reach as far as a straight line still passes
    within the tolerances of every sample it skips. Both ends of a flat stretch
    stay, so a step in HP stays a one-packet step.
    """
    tolerances = (
        0.0,
        POSITION_TOLERANCE,
        POSITION_TOLERANCE,
        POINTS_TOLERANCE,
        POINTS_TOLERANCE,
        POINTS_TOLERANCE,
        POINTS_TOLERANCE,
    )

    def reproduces(a: list[float], b: list[float], skipped: list[list[float]]) -> bool:
        for sample in skipped:
            # Two samples at one time (a pause): the line holds its start, as drawn.
            k = 0.0 if b[0] == a[0] else (sample[0] - a[0]) / (b[0] - a[0])
            for j in range(1, len(sample)):
                if abs(a[j] + (b[j] - a[j]) * k - sample[j]) > tolerances[j]:
                    return False
        return True

    if len(samples) <= 2:
        return samples
    kept = [samples[0]]
    anchor = 0
    for i in range(2, len(samples)):
        if not reproduces(samples[anchor], samples[i], samples[anchor + 1 : i]):
            anchor = i - 1
            kept.append(samples[anchor])
    kept.append(samples[-1])
    return kept


def playback_window(
    match: ParsedMatch, fight: Fight, smokes: list[SmokeAnalysis] | None = None
) -> tuple[int, int]:
    """The playback's first and last tick: the fight, from the smoke that led into it."""
    if smokes is None:
        smokes = gem.build_smoke_analysis(match)
    start = min(
        [fight.start_tick]
        + [
            smoke.activation_tick
            for smoke in smokes
            if smoke.first_fight is fight
            # Game time, not ticks, so a pause between the two doesn't count.
            and _game_seconds(match, fight.start_tick) - _game_seconds(match, smoke.activation_tick)
            <= SMOKE_LEAD_S
        ]
    )
    return start, (fight.last_death_tick or fight.end_tick) + PLAYBACK_TAIL_TICKS


def fight_playback(
    match: ParsedMatch,
    states: dict[int, list[HeroState]] | None = None,
    fight: Fight | None = None,
) -> dict | None:
    """A fight's playback (the biggest by default): hero state and the fight's timeline.

    Heroes are referred to by their index in ``heroes``. Every ``t`` is seconds
    since the playback's ``start`` (the fight window's start, or the smoke that
    led into the fight when it came shortly before), to the hundredth so every
    tick is distinct. ``states`` are the heroes' readings by player ID
    (``load_hero_states``). An empty dict gives a breakdown with no hero states
    (no map); ``None`` falls back to the match's once-a-second samples, for tests.
    """
    fight = fight or biggest_fight(match)
    if fight is None:
        return None
    smokes = gem.build_smoke_analysis(match)
    start, end = playback_window(match, fight, smokes)
    if states is None:
        states = match_hero_states(match)
    since = _seconds_since(match, start, places=2)
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
    hero_team = {player.hero_name: player.team for player in players}
    hidden = _hidden(match, players, start, end, since)
    deaths = []
    for death in timeline.deaths:
        rewards = timeline.rewards_at(death.tick)
        # The log can't say which of several same-tick deaths a bounty paid for, so
        # the shared rewards go on the tick's first death only, and every death on
        # the tick lists the tick's victims.
        first_on_tick = rewards is None or rewards.victims[0] == death.victim
        entry: dict = {
            "t": since(death.tick),
            "victim": index[death.victim],
            "killer": hero(death.killer_hero),
            "killer_name": _unit_name(death.killer),
            "aegis": death.reincarnated,
            "gold_lost": death.gold_lost,
            "gold": [[index[h], g] for h, g in rewards.gold.items() if h in index]
            if rewards and first_on_tick
            else [],
            "xp": [[index[h], x] for h, x in rewards.xp.items() if h in index]
            if rewards and first_on_tick
            else [],
            # The largest sources (the recap's rows), and the total over all of them.
            "recent": [
                [
                    _unit_name(taken.attacker_hero or taken.attacker),
                    _source_name(taken.source),
                    taken.damage_type,
                    taken.damage,
                ]
                for taken in death.recent_damage[:RECAP_ROWS]
            ],
            "recent_total": sum(taken.damage for taken in death.recent_damage),
        }
        if rewards and len(rewards.victims) > 1:
            entry["tick_victims"] = [index[v] for v in rewards.victims if v in index]
        deaths.append(entry)
    return {
        "start": _clock(match, start),
        # The clock at the start, in seconds: the playback shows floor(start_s + t),
        # which is gem's clock at every tick (``start`` is whole seconds).
        "start_s": _clock_base(match, start, end),
        "duration": since(end),
        "heroes": [
            {
                "hero": hero_display(player.hero_name),
                "icon": player.hero_name.removeprefix("npc_dota_hero_"),
                "team": team_of[i],
                "runs": _hero_runs(states.get(player.player_id, []), start, end, since),
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
        # [t, until, target, source hero or null, name, kind, ring, seconds]:
        # disables, debuffs and buffs on heroes. ``until`` is the removal (the
        # playback's end when it outlasted it); ``ring`` names a buff drawn as a
        # ring; ``seconds`` is the duration it was applied with (the stun time,
        # or the log's duration), which a death or dispel can cut short.
        "modifiers": [
            [
                since(window.start_tick),
                since(window.end_tick) if window.end_tick is not None else since(end),
                index[window.target],
                hero(window.source_hero),
                _modifier_name(window.modifier),
                kind,
                BUFF_RINGS.get(window.modifier),
                round(_applied_seconds(window), 1),
            ]
            for window in timeline.modifiers
            if window.start_tick is not None
            and (kind := _modifier_kind(window, hero_team)) is not None
        ],
        "deaths": deaths,
        # [t, hero, cost]
        "buybacks": [[since(b.tick), index[b.hero], b.cost] for b in timeline.buybacks],
        # [team, t of the smoke's use or null before the window, members]; each
        # member [hero, smoked from, smoke broke or null, seen by the enemy within
        # a second of the break or null], clipped to the window.
        "smokes": _smokes(smokes, start, end, index, since, hidden),
        # [hero, from, to]: while the enemy team couldn't see the hero.
        "hidden": hidden,
    }


def _smokes(
    smokes: list,
    start: int,
    end: int,
    index: dict[str, int],
    since: Callable[[int], float],
    hidden: list[list[float]],
) -> list:
    """The smokes on any hero during [start, end], with each member's smoked span.

    A member counts as seen by the enemy when its hidden span ends within a second
    of the smoke breaking (the replay's visibility, not the smoke's own record).
    """

    def seen(hero: int, broke: float | None) -> float | None:
        if broke is None:
            return None
        ends = [to for h, _, to in hidden if h == hero and 0 <= to - broke <= SEEN_AFTER_BREAK_S]
        return min(ends, default=None)

    out = []
    for smoke in smokes:
        members = [
            [
                index[member.hero_name],
                since(max(member.applied_tick, start)),
                # A break after the playback's end is "still smoked at the end".
                broke := since(member.removed_tick)
                if member.removed_tick is not None and member.removed_tick <= end
                else None,
                seen(index[member.hero_name], broke),
            ]
            for member in smoke.members
            if member.hero_name in index
            and member.applied_tick <= end
            and (member.removed_tick is None or member.removed_tick >= start)
        ]
        if members:
            used = since(smoke.activation_tick) if smoke.activation_tick >= start else None
            out.append([TEAMS.get(smoke.team, "unknown"), used, members])
    return out


def _hidden(
    match: ParsedMatch,
    players: list[ParsedPlayer],
    start: int,
    end: int,
    since: Callable[[int], float],
) -> list[list[float]]:
    """Spans of [start, end] when the enemy team couldn't see each hero.

    From the replay's per-team hero visibility (``match.hero_visibility_events``);
    only ``hidden`` counts, not ``unknown``.
    """
    out: list[list[float]] = []
    for i, player in enumerate(players):
        # What the enemy team saw: Dire's view of a Radiant hero, and the reverse.
        seen_by_dire = player.team == 2
        # By tick only: the sort is stable, so same-tick transitions keep the
        # extractor's order (a terminal state, then the replacement's).
        states = sorted(
            (
                (e.tick, str(e.dire_state if seen_by_dire else e.radiant_state))
                for e in match.hero_visibility_events
                if e.player_id == player.player_id
            ),
            key=lambda state: state[0],
        )
        before = [seen for tick, seen in states if tick <= start]
        hidden_since = start if before and before[-1] == "hidden" else None
        for tick, seen in states:
            if not start < tick <= end:
                continue
            if seen == "hidden" and hidden_since is None:
                hidden_since = tick
            elif seen != "hidden" and hidden_since is not None:
                if since(tick) - since(hidden_since) >= MIN_HIDDEN_S:
                    out.append([i, since(hidden_since), since(tick)])
                hidden_since = None
        if hidden_since is not None:
            out.append([i, since(hidden_since), since(end)])
    return out


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
    parser.add_argument("--wards-data", type=Path, default=DEFAULT_WARDS_DATA)
    parser.add_argument("--fights-data", type=Path, default=DEFAULT_FIGHTS_DATA)
    parser.add_argument("--objectives-data", type=Path, default=DEFAULT_OBJECTIVES_DATA)
    parser.add_argument("--lead-data", type=Path, default=DEFAULT_LEAD_DATA)
    parser.add_argument("--lanes-data", type=Path, default=DEFAULT_LANES_DATA)
    parser.add_argument("--runes-data", type=Path, default=DEFAULT_RUNES_DATA)
    parser.add_argument("--map-image", type=Path, default=DEFAULT_MAP_IMAGE)
    parser.add_argument("--fight-image", type=Path, default=DEFAULT_FIGHT_IMAGE)
    parser.add_argument("--icons-dir", type=Path, default=DEFAULT_ICONS)
    parser.add_argument("--public-figures", type=Path, default=DEFAULT_PUBLIC_FIGURES)
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
    # Figure 3's fight, and every fight big enough for a playback in the fights
    # recipe: one more pass over the replay reads every hero in all their windows.
    home_fight = biggest_fight(match)
    in_order = sorted(match.fights, key=lambda f: f.start_tick)
    played = [f for f in in_order if f.deaths >= PLAYBACK_MIN_DEATHS or f is home_fight]
    windows = [playback_window(match, f) for f in played]
    states = load_hero_states(args.replay, windows) if windows else {}
    for start, end in windows:
        missing = [
            p.hero_name
            for p in match.players
            if not any(start <= reading[0] <= end for reading in states.get(p.player_id, []))
        ]
        if missing:
            raise SystemExit(f"no hero readings in the playback window for {', '.join(missing)}")
    playback = fight_playback(match, states, home_fight) if home_fight else None
    args.fight_data.parent.mkdir(parents=True, exist_ok=True)
    # Compact: the playback is loaded by the browser, so every byte counts.
    args.fight_data.write_text(json.dumps(playback, separators=(",", ":")) + "\n")
    # The fights recipe: one file per fight (Figure 3's is fight.json). A fight
    # with a playback gets the hero states and a map crop; the rest get an
    # empty dict, so their breakdown has no map (never the once-a-second samples).
    shutil.rmtree(args.fights_data, ignore_errors=True)
    args.fights_data.mkdir(parents=True)
    crops = args.public_figures / "fights"
    shutil.rmtree(crops, ignore_errors=True)
    files: dict[int, str] = {}
    boxes: dict[int, list[float]] = {}
    items: set[str] = set()
    for number, each in enumerate(in_order, start=1):
        has_playback = any(each is f for f in played)
        if has_playback:
            boxes[number] = fight_box(match, each, states)
            write_map_image(crops / f"{number}.webp", boxes[number], px=800, webp=True)
        if each is home_fight:
            files[number] = "fight.json"
            continue
        data_file = fight_playback(match, states if has_playback else {}, each)
        # Named from src/data, as the index and fight.json are.
        files[number] = f"fights/{number}.json"
        (args.fights_data / f"{number}.json").write_text(
            json.dumps(data_file, separators=(",", ":")) + "\n"
        )
        items |= (
            {cast["item"] for cast in data_file["casts"] if "item" in cast} if data_file else set()
        )
    # The timeline spans the match, as the wards figure's does.
    end_tick = match.post_game_tick or match.game_end_tick or 0
    index = {
        "start_s": -90.0,
        "end_s": round(_game_seconds(match, end_tick), 1),
        "fights": fights_recipe(match, files, boxes),
    }
    (args.fights_data / "index.json").write_text(json.dumps(index, separators=(",", ":")) + "\n")
    # The objectives recipe: where the buildings stand and the bosses were,
    # from one more pass over the replay's entities (up to the last objective).
    last = max(
        [t.tick for t in match.towers]
        + [b.tick for b in match.barracks]
        + [r.tick for r in match.roshans]
        + [t.tick for t in match.tormentors],
        default=None,
    )
    places = load_map_places(args.replay, last + 30) if last is not None else {}
    args.objectives_data.parent.mkdir(parents=True, exist_ok=True)
    args.objectives_data.write_text(
        json.dumps(objectives_recipe(match, places), separators=(",", ":")) + "\n"
    )
    args.wards_data.parent.mkdir(parents=True, exist_ok=True)
    args.wards_data.write_text(json.dumps(wards_recipe(match), separators=(",", ":")) + "\n")
    args.lead_data.parent.mkdir(parents=True, exist_ok=True)
    args.lead_data.write_text(json.dumps(lead_recipe(match), separators=(",", ":")) + "\n")
    args.lanes_data.parent.mkdir(parents=True, exist_ok=True)
    args.lanes_data.write_text(json.dumps(lanes_recipe(match), separators=(",", ":")) + "\n")
    args.runes_data.parent.mkdir(parents=True, exist_ok=True)
    args.runes_data.write_text(json.dumps(runes_recipe(match), separators=(",", ":")) + "\n")
    write_map_image(args.map_image)
    written = [args.data, args.fight_data, args.wards_data, args.fights_data, args.objectives_data]
    written += [args.lead_data, args.lanes_data, args.runes_data]
    written.append(args.map_image)
    if fight is not None:
        write_map_image(args.fight_image, fight["box"])
        written.append(args.fight_image)
    heroes = {hero["icon"] for hero in playback["heroes"]} if playback else set()
    items |= {cast["item"] for cast in playback["casts"] if "item" in cast} if playback else set()
    write_icons(args.icons_dir, heroes, items)
    written.append(args.icons_dir)
    write_public_figures(args.public_figures, args.icons_dir)
    written.append(args.public_figures)
    print("Wrote " + ", ".join(str(path) for path in written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
