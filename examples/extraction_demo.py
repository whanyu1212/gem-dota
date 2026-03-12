"""Comprehensive extraction demo for Dota 2 replay data.

Demonstrates combat log extraction and entity state polling using ReplayParser.
Parses the full replay and prints structured summaries of what was observed.
Enriches output using gem.constants for display names, XP thresholds, etc.

Usage:
    python examples/extraction_demo.py <path/to/replay.dem>

Or without arguments to use the bundled fixture:
    python examples/extraction_demo.py
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from collections.abc import Callable
from pathlib import Path

# Allow running from repo root without installing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gem.combatlog import CombatLogEntry
from gem.constants import (
    ABILITIES,
    HEROES,
    ITEMS,
    ability_display,
    hero_display,
    hero_short,
    item_display,
    xp_to_next_level,
)
from gem.entities import Entity, EntityOp
from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Entity helpers
# ---------------------------------------------------------------------------

TEAM_RADIANT = 2
TEAM_DIRE = 3
TEAM_NAMES = {TEAM_RADIANT: "Radiant", TEAM_DIRE: "Dire"}
DEAD = 2  # m_lifeState: 0=alive, 1=dying, 2=dead

_CELL_SIZE = 128  # Source 2 world units per cell


def _team(entity: Entity) -> str:
    team = entity.get_int32("m_iTeamNum")
    return TEAM_NAMES.get(team, f"Team{team}") if team is not None else "?"


def _hp(entity: Entity) -> tuple[int, int]:
    hp = entity.get_int32("m_iHealth") or 0
    max_hp = entity.get_int32("m_iMaxHealth") or 0
    return hp, max_hp


def _mana(entity: Entity) -> tuple[float, float]:
    mp = entity.get_float32("m_flMana") or 0.0
    max_mp = entity.get_float32("m_flMaxMana") or 0.0
    return mp, max_mp


def _is_alive(entity: Entity) -> bool:
    life = entity.get_int32("m_lifeState")
    return life is None or life != DEAD


def _player_id(entity: Entity) -> int:
    return entity.get_int32("m_nPlayerOwnerID") or 0


def _pos(entity: Entity) -> tuple[float, float] | None:
    """Return (x, y) world coordinates, or None if not available.

    Source 2 stores position as a cell index (uint16) plus a quantized float
    offset within that cell:  world_coord = cell * 128 + vec.
    """
    cell_x = entity.get_int32("CBodyComponent.m_cellX")
    cell_y = entity.get_int32("CBodyComponent.m_cellY")
    vec_x = entity.get_float32("CBodyComponent.m_vecX")
    vec_y = entity.get_float32("CBodyComponent.m_vecY")
    if cell_x is None or cell_y is None or vec_x is None or vec_y is None:
        return None
    return (cell_x * _CELL_SIZE + vec_x, cell_y * _CELL_SIZE + vec_y)


# ---------------------------------------------------------------------------
# Data collectors
# ---------------------------------------------------------------------------

_WARD_ITEMS = frozenset({"item_ward_observer", "item_ward_sentry", "item_ward_dispenser"})
_SMOKE_MODIFIER = "modifier_smoke_of_deceit"
_SMOKE_ITEM = "item_smoke_of_deceit"

# item_ward_dispenser plants an observer ward; item_ward_sentry plants a sentry.
_ITEM_TO_WARD_TYPE = {
    "item_ward_observer": "observer",
    "item_ward_dispenser": "observer",
    "item_ward_sentry": "sentry",
}


class SmokeEvent:
    """One smoke-of-deceit activation: who used it and which heroes were smoked."""

    def __init__(self, tick: int, activator: str) -> None:
        self.tick = tick
        self.activator = activator
        self.smoked: list[str] = []  # heroes that received the modifier
        self.dispelled: list[str] = []  # heroes whose smoke was removed


class CombatLogCollector:
    """Accumulates combat log entries and derives summary structures."""

    def __init__(
        self, hero_pos_lookup: Callable[[str], tuple[float, float] | None] | None = None
    ) -> None:
        self.entries: list[CombatLogEntry] = []
        self.damage_by_attacker: dict[str, int] = defaultdict(int)
        self.heal_by_source: dict[str, int] = defaultdict(int)
        self.kills: list[CombatLogEntry] = []
        self.gold_events: list[CombatLogEntry] = []
        self.xp_events: list[CombatLogEntry] = []

        # Ward placements from combat log: (tick, npc_hero_name, ward_type, hero_pos_or_None)
        # ward_type is "observer" or "sentry" (dispenser → observer)
        # hero_pos is the placer's position at placement time — used as fallback when the
        # entity stream has no CREATED event (recycled slot).
        self.ward_placements: list[tuple[int, str, str, tuple[float, float] | None]] = []
        self._hero_pos_lookup = hero_pos_lookup

        # Smoke tracking
        self.smoke_events: list[SmokeEvent] = []
        self._active_smokes: dict[str, SmokeEvent] = {}

    def __call__(self, entry: CombatLogEntry) -> None:
        self.entries.append(entry)

        if entry.log_type == "DAMAGE" and entry.attacker_is_hero:
            self.damage_by_attacker[entry.attacker_name] += entry.value

        elif entry.log_type == "HEAL" and entry.value > 0:
            self.heal_by_source[entry.inflictor_name or entry.attacker_name] += entry.value

        elif entry.log_type == "DEATH":
            self.kills.append(entry)

        elif entry.log_type == "GOLD":
            self.gold_events.append(entry)

        elif entry.log_type == "XP":
            self.xp_events.append(entry)

        elif entry.log_type == "ITEM" and entry.inflictor_name in _WARD_ITEMS:
            ward_type = _ITEM_TO_WARD_TYPE[entry.inflictor_name]
            hero_pos = self._hero_pos_lookup(entry.attacker_name) if self._hero_pos_lookup else None
            self.ward_placements.append((entry.tick, entry.attacker_name, ward_type, hero_pos))

        elif entry.log_type == "ITEM" and entry.inflictor_name == _SMOKE_ITEM:
            smoke = SmokeEvent(tick=entry.tick, activator=entry.attacker_name)
            self._active_smokes[entry.attacker_name] = smoke
            self.smoke_events.append(smoke)

        elif entry.log_type == "MODIFIER_ADD" and entry.inflictor_name == _SMOKE_MODIFIER:
            active = self._active_smokes.get(entry.attacker_name)
            if active is not None:
                active.smoked.append(entry.target_name)

        elif entry.log_type == "MODIFIER_REMOVE" and entry.inflictor_name == _SMOKE_MODIFIER:
            active = self._active_smokes.get(entry.attacker_name)
            if active is not None:  # noqa: SIM102
                active.dispelled.append(entry.target_name)
                if len(active.dispelled) >= len(active.smoked):
                    self._active_smokes.pop(entry.attacker_name, None)


class EntityStatePoller:
    """Polls hero, tower, and ward entity state; records snapshots at intervals."""

    def __init__(self, sample_every_n_ticks: int = 1800) -> None:
        self._sample_every = sample_every_n_ticks
        self._last_sample = -sample_every_n_ticks
        self.current_tick: int = 0

        self.heroes: dict[int, Entity] = {}
        self._heroes_by_npc: dict[str, Entity] = {}  # npc_dota_hero_* -> entity
        self.towers: dict[int, Entity] = {}

        self.hero_snapshots: list[dict] = []
        self.tower_snapshots: list[dict] = []

        # Ward entity log: every ward entity event with valid coordinates.
        # Each entry: (tick, ward_type, team, x, y)
        # Includes UPDATED events on recycled slots — the matcher allows reuse
        # of the same slot across multiple placements at different ticks.
        self.ward_entity_log: list[tuple[int, str, str, float, float]] = []

    def on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls.startswith("CDOTA_Unit_Hero_"):
            npc = cls.replace("CDOTA_Unit_Hero_", "npc_dota_hero_").lower()
            if op & EntityOp.DELETED:
                self.heroes.pop(entity.get_index(), None)
                self._heroes_by_npc.pop(npc, None)
            else:
                self.heroes[entity.get_index()] = entity
                self._heroes_by_npc[npc] = entity

        elif cls == "CDOTA_BaseNPC_Tower":
            if op & EntityOp.DELETED:
                self.towers.pop(entity.get_index(), None)
            else:
                self.towers[entity.get_index()] = entity

        elif cls in ("CDOTA_NPC_Observer_Ward", "CDOTA_NPC_Observer_Ward_TrueSight"):
            ward_type = "sentry" if "TrueSight" in cls else "observer"
            pos = _pos(entity)
            if pos is not None and not (op & EntityOp.DELETED):
                self.ward_entity_log.append(
                    (self.current_tick, ward_type, _team(entity), pos[0], pos[1])
                )

    def hero_pos(self, npc_name: str) -> tuple[float, float] | None:
        """Return the current world position of the named hero entity, or None."""
        entity = self._heroes_by_npc.get(npc_name.lower())
        return _pos(entity) if entity is not None else None

    def maybe_sample(self, tick: int) -> None:
        if tick - self._last_sample < self._sample_every:
            return
        self._last_sample = tick

        for entity in self.heroes.values():
            hp, max_hp = _hp(entity)
            mp, max_mp = _mana(entity)
            level = entity.get_int32("m_iCurrentLevel") or 0
            xp = entity.get_int32("m_iCurrentXP") or 0
            xp_next = xp_to_next_level(level, xp)
            dmg_min = entity.get_int32("m_iDamageMin") or 0
            dmg_max = entity.get_int32("m_iDamageMax") or 0
            move = entity.get_int32("m_iMoveSpeed") or 0
            str_total = entity.get_float32("m_flStrengthTotal") or 0.0
            agi_total = entity.get_float32("m_flAgilityTotal") or 0.0
            int_total = entity.get_float32("m_flIntellectTotal") or 0.0
            npc_name = entity.get_class_name().replace("CDOTA_Unit_Hero_", "npc_dota_hero_").lower()

            self.hero_snapshots.append(
                {
                    "tick": tick,
                    "npc_name": npc_name,
                    "hero": hero_display(npc_name),
                    "team": _team(entity),
                    "player_id": _player_id(entity),
                    "level": level,
                    "hp": hp,
                    "max_hp": max_hp,
                    "hp_pct": round(hp / max_hp * 100, 1) if max_hp else 0,
                    "mp": round(mp, 1),
                    "max_mp": round(max_mp, 1),
                    "xp": xp,
                    "xp_next": xp_next,
                    "dmg_min": dmg_min,
                    "dmg_max": dmg_max,
                    "move_speed": move,
                    "strength": round(str_total, 1),
                    "agility": round(agi_total, 1),
                    "intellect": round(int_total, 1),
                    "alive": _is_alive(entity),
                    "pos": _pos(entity),
                }
            )

        for entity in self.towers.values():
            hp, max_hp = _hp(entity)
            self.tower_snapshots.append(
                {
                    "tick": tick,
                    "team": _team(entity),
                    "hp": hp,
                    "max_hp": max_hp,
                    "hp_pct": round(hp / max_hp * 100, 1) if max_hp else 0,
                    "alive": _is_alive(entity),
                }
            )


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def print_separator(title: str = "") -> None:
    width = 72
    if title:
        pad = (width - len(title) - 2) // 2
        print(f"\n{'=' * pad} {title} {'=' * pad}")
    else:
        print("\n" + "=" * width)


# ---------------------------------------------------------------------------
# Report: combat log summary
# ---------------------------------------------------------------------------


def report_combat_log(collector: CombatLogCollector, last_tick: int) -> None:
    entries = collector.entries
    print_separator("COMBAT LOG SUMMARY")
    print(f"Total entries (ticks 0 – {last_tick:,}): {len(entries):,}")

    type_counts = Counter(e.log_type for e in entries)
    print("\nEvent type breakdown:")
    for t, n in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t:<20s} {n:>6,}")

    print("\nHero damage dealt (top 10):")
    for npc, dmg in sorted(collector.damage_by_attacker.items(), key=lambda x: -x[1])[:10]:
        print(f"  {hero_short(npc):<28s} {dmg:>8,} dmg")

    if collector.heal_by_source:
        print("\nHeal sources (top 5):")
        for src, total in sorted(collector.heal_by_source.items(), key=lambda x: -x[1])[:5]:
            if not src:
                name = "(unknown)"
            elif src.startswith("item_"):
                name = item_display(src)
            elif src.startswith("npc_dota_hero_"):
                name = hero_short(src)
            else:
                name = ability_display(src)
            print(f"  {name:<28s} {total:>6,} hp healed")

    # Hero-vs-hero kills only (both attacker and target are heroes)
    hvh_kills = [k for k in collector.kills if k.attacker_is_hero and k.target_is_hero]
    print(f"\nHero kill log ({len(hvh_kills)} hero kills, {len(collector.kills):,} total deaths):")
    for k in hvh_kills:
        attacker = hero_short(k.attacker_name) if k.attacker_name else "?"
        target = hero_short(k.target_name) if k.target_name else "?"
        via = ability_display(k.inflictor_name) if k.inflictor_name else "auto-attack"
        print(f"  tick {k.tick:>7,}  {attacker:<22s}  →  {target:<22s}  [{via}]")

    if collector.gold_events:
        total_gold = sum(e.value for e in collector.gold_events)
        gold_by_reason = Counter(e.gold_reason for e in collector.gold_events)
        print(f"\nGold events: {len(collector.gold_events):,} events, {total_gold:,} total gold")
        print("  By reason code:", dict(gold_by_reason.most_common(5)))

    if collector.xp_events:
        total_xp = sum(e.value for e in collector.xp_events)
        print(f"\nXP events: {len(collector.xp_events):,} events, {total_xp:,} total XP")

    add_count = type_counts.get("MODIFIER_ADD", 0)
    rem_count = type_counts.get("MODIFIER_REMOVE", 0)
    print(f"\nBuff/debuff activity: {add_count:,} applied, {rem_count:,} removed")

    ability_entries = [e for e in entries if e.log_type == "ABILITY"]
    if ability_entries:
        ability_counts = Counter(e.inflictor_name for e in ability_entries)
        print(f"\nAbilities cast ({len(ability_entries)} total, top 10):")
        for internal, n in ability_counts.most_common(10):
            display = ability_display(internal) if internal else "(unknown)"
            print(f"  {display:<40s} {n:>4}x")


# ---------------------------------------------------------------------------
# Report: wards and smokes
# ---------------------------------------------------------------------------


def report_wards_and_smokes(collector: CombatLogCollector, poller: EntityStatePoller) -> None:
    print_separator("WARD PLACEMENTS & SMOKE USAGE")

    # --- Ward placements from combat log (who placed, when, hero pos at that tick) ---
    obs_cl = [(t, h, hp) for t, h, wt, hp in collector.ward_placements if wt == "observer"]
    sen_cl = [(t, h, hp) for t, h, wt, hp in collector.ward_placements if wt == "sentry"]

    # --- Ward entity log (authoritative coordinates from CREATED events) ---
    obs_ent = sorted(
        [(t, x, y, team) for t, wt, team, x, y in poller.ward_entity_log if wt == "observer"],
        key=lambda e: e[0],
    )
    sen_ent = sorted(
        [(t, x, y, team) for t, wt, team, x, y in poller.ward_entity_log if wt == "sentry"],
        key=lambda e: e[0],
    )

    def _match_coords(
        placements: list[tuple[int, str, tuple | None]],
        entities: list[tuple],
        window: int = 60,
    ) -> list[tuple[int, str, float | None, float | None, str | None]]:
        """Match each placement to its nearest entity event within *window* ticks.

        Entity slots are reused, so the same slot may match multiple placements.
        Each placement independently picks the closest entity event by tick delta.

        Returns list of (tick, hero_npc, x, y, coord_source) where coord_source is
        'entity' (accurate ward position), 'hero' (placer position fallback), or None.
        """
        result: list[tuple[int, str, float | None, float | None, str | None]] = []
        for ptick, hero, hero_pos in placements:
            best_pos, best_dt = None, window + 1
            for et, ex, ey, _team in entities:
                if et < ptick - window:
                    continue
                if et > ptick + window:
                    break
                dt = abs(et - ptick)
                if dt < best_dt:
                    best_pos, best_dt = (ex, ey), dt
            if best_pos is not None:
                result.append((ptick, hero, best_pos[0], best_pos[1], "entity"))
            elif hero_pos is not None:
                result.append((ptick, hero, hero_pos[0], hero_pos[1], "hero"))
            else:
                result.append((ptick, hero, None, None, None))
        return result

    obs_matched = _match_coords(obs_cl, obs_ent)
    sen_matched = _match_coords(sen_cl, sen_ent)

    def _fmt_coords(x: float | None, y: float | None, source: str | None) -> str:
        if x is None:
            return "  (no coords)"
        marker = " " if source == "entity" else "~"  # ~ = hero position approximation
        return f"{marker}({x:>9.1f}, {y:>9.1f})"

    # Observer wards
    n_entity = sum(1 for *_, s in obs_matched if s == "entity")
    n_hero = sum(1 for *_, s in obs_matched if s == "hero")
    print(
        f"Observer wards placed: {len(obs_matched)}  "
        f"({n_entity} exact coords, {n_hero} approx from hero pos)"
    )
    for tick, npc, x, y, source in obs_matched:
        print(f"  tick {tick:>7,}  {hero_short(npc):<22}  {_fmt_coords(x, y, source)}")

    # Sentry wards
    n_entity = sum(1 for *_, s in sen_matched if s == "entity")
    n_hero = sum(1 for *_, s in sen_matched if s == "hero")
    print(
        f"\nSentry wards placed: {len(sen_matched)}  "
        f"({n_entity} exact coords, {n_hero} approx from hero pos)"
    )
    for tick, npc, x, y, source in sen_matched:
        print(f"  tick {tick:>7,}  {hero_short(npc):<22}  {_fmt_coords(x, y, source)}")

    # Smoke events
    print(f"\nSmoke of Deceit usages: {len(collector.smoke_events)}")
    for smoke in collector.smoke_events:
        activator = hero_short(smoke.activator)
        group = (
            ", ".join(hero_short(h) for h in smoke.smoked) if smoke.smoked else "(none resolved)"
        )
        note = (
            "still active"
            if smoke.smoked and len(smoke.dispelled) < len(smoke.smoked)
            else "broken/expired"
        )
        print(f"  tick {smoke.tick:>7,}  {activator:<22}  group: {group}  [{note}]")


# ---------------------------------------------------------------------------
# Report: entity state snapshots
# ---------------------------------------------------------------------------


def report_entity_state(poller: EntityStatePoller, sample_ticks: list[int]) -> None:
    print_separator("ENTITY STATE SNAPSHOTS")

    for tick in sample_ticks:
        snaps = [s for s in poller.hero_snapshots if s["tick"] == tick]
        if not snaps:
            continue

        print(f"\n--- Tick {tick:,} ---")
        hdr = (
            f"  {'Hero':<22} {'Team':<9} {'Lvl':>3} {'HP':>10} {'HP%':>6}"
            f" {'MP':>10} {'XP':>7} {'→Nxt':>6} {'Spd':>4}"
            f" {'STR':>5} {'AGI':>5} {'INT':>5}  {'Pos (x,y)':>20}  Alive"
        )
        print(hdr)
        print(f"  {'-' * (len(hdr) - 2)}")

        radiant = sorted([s for s in snaps if s["team"] == "Radiant"], key=lambda x: x["player_id"])
        dire = sorted([s for s in snaps if s["team"] == "Dire"], key=lambda x: x["player_id"])

        for team_snaps in (radiant, dire):
            for s in team_snaps:
                hp_str = f"{s['hp']}/{s['max_hp']}"
                mp_str = f"{s['mp']:.0f}/{s['max_mp']:.0f}"
                alive_str = "alive" if s["alive"] else "DEAD"
                pos_str = (
                    f"({s['pos'][0]:>7.1f},{s['pos'][1]:>7.1f})" if s["pos"] else "           n/a"
                )
                xp_next_str = f"{s['xp_next']:,}" if s["xp_next"] is not None else "max"
                print(
                    f"  {s['hero']:<22} {s['team']:<9} {s['level']:>3}"
                    f" {hp_str:>10} {s['hp_pct']:>5.1f}%"
                    f" {mp_str:>10} {s['xp']:>7,} {xp_next_str:>6}"
                    f" {s['move_speed']:>4}"
                    f" {s['strength']:>5.1f} {s['agility']:>5.1f} {s['intellect']:>5.1f}"
                    f"  {pos_str}  {alive_str}"
                )

        tower_snaps = [s for s in poller.tower_snapshots if s["tick"] == tick]
        if tower_snaps:
            alive = {
                t: sum(1 for s in tower_snaps if s["team"] == t and s["alive"])
                for t in ("Radiant", "Dire")
            }
            print(f"\n  Towers alive — Radiant: {alive['Radiant']}, Dire: {alive['Dire']}")


# ---------------------------------------------------------------------------
# Report: hero progression
# ---------------------------------------------------------------------------


def report_hero_progression(poller: EntityStatePoller) -> None:
    print_separator("HERO LEVEL & XP PROGRESSION")

    by_hero: dict[str, list[dict]] = defaultdict(list)
    for s in poller.hero_snapshots:
        by_hero[s["hero"]].append(s)

    # Get hero metadata for attr/role annotation
    # Build localized_name -> hero dict for quick lookup
    _by_display = {h.get("localized_name", ""): h for h in HEROES.values()}

    def _meta(hero_display_name: str) -> str:
        h = _by_display.get(hero_display_name)
        if not h:
            return ""
        attr = h.get("primary_attr", "?")
        roles = "/".join(h.get("roles", [])[:2])
        return f"{attr:<3}  {roles}"

    print(
        f"  {'Hero':<22} {'Team':<9} {'Attr/Roles':<22} "
        f"{'Level':<14} {'XP start':>8} {'XP end':>8} {'XP gain':>8}"
    )
    print(f"  {'-' * 100}")

    for hero_name, snaps in sorted(by_hero.items()):
        snaps_sorted = sorted(snaps, key=lambda x: x["tick"])
        first, last = snaps_sorted[0], snaps_sorted[-1]
        lvl_gain = last["level"] - first["level"]
        xp_gain = last["xp"] - first["xp"]
        meta = _meta(hero_name)
        lvl_str = f"{first['level']} → {last['level']} (+{lvl_gain})"
        print(
            f"  {hero_name:<22} {last['team']:<9} {meta:<22}"
            f" {lvl_str:<14} {first['xp']:>8,} {last['xp']:>8,} {xp_gain:>+8,}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    if len(sys.argv) > 1:
        dem_path = sys.argv[1]
    else:
        dem_path = str(
            Path(__file__).parent.parent / "tests" / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"
        )

    print(f"Replay: {dem_path}")
    print(
        f"gem.constants loaded: {len(HEROES)} heroes, {len(ITEMS)} items, "
        f"{len(ABILITIES)} abilities"
    )

    print("\nParsing full replay...")

    poller = EntityStatePoller(sample_every_n_ticks=1800)  # ~1 min at 30 tps
    combat = CombatLogCollector(hero_pos_lookup=poller.hero_pos)

    parser = ReplayParser(dem_path)
    parser.on_combat_log_entry(combat)

    def _entity_handler(entity: Entity, op: EntityOp) -> None:
        poller.current_tick = parser.tick
        poller.on_entity(entity, op)
        poller.maybe_sample(parser.tick)

    parser.on_entity(_entity_handler)
    parser.parse()
    last_tick = parser.tick

    sample_ticks = sorted({s["tick"] for s in poller.hero_snapshots})

    report_combat_log(combat, last_tick)
    report_wards_and_smokes(combat, poller)
    report_entity_state(poller, sample_ticks)
    report_hero_progression(poller)

    print_separator()
    print(
        f"Done. Parsed {last_tick:,} ticks  |  {len(combat.entries):,} combat log entries  |  "
        f"{len(poller.hero_snapshots)} hero snapshots across {len(sample_ticks)} sample ticks."
    )


if __name__ == "__main__":
    main()
