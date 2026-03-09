"""Detailed ward placements, smoke usage, and Roshan events demo.

Tracks three high-value vision/objective events from a Dota 2 replay:
  - Observer and sentry ward placements (with coordinates where available)
  - Smoke of Deceit activations and which heroes were grouped
  - Roshan kills with attacker, respawn windows, and XP granted

Ward coordinates come from two sources:
  - Entity CREATED events (exact position) — available for ~35% of placements
  - Hero position at placement tick (approximate) — fallback for the rest;
    heroes stand where they drop wards, so this is a good approximation.

Usage:
    python examples/ward_smoke_rosh.py <path/to/replay.dem>

Or without arguments to use the bundled fixture:
    python examples/ward_smoke_rosh.py
"""

from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gem.combatlog import CombatLogEntry
from gem.constants import hero_short
from gem.entities import Entity, EntityOp
from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Game constants
# ---------------------------------------------------------------------------

TEAM_RADIANT = 2
TEAM_DIRE = 3
TEAM_NAMES = {TEAM_RADIANT: "Radiant", TEAM_DIRE: "Dire"}

_CELL_SIZE = 128  # Source 2 world units per cell

_WARD_ITEMS = frozenset({"item_ward_observer", "item_ward_sentry", "item_ward_dispenser"})
_ITEM_TO_WARD_TYPE = {
    "item_ward_observer": "observer",
    "item_ward_dispenser": "observer",  # dispenser item plants an observer ward
    "item_ward_sentry": "sentry",
}

_SMOKE_ITEM = "item_smoke_of_deceit"
_SMOKE_MODIFIER = "modifier_smoke_of_deceit"

_WARD_OBSERVER_CLASSES = frozenset(
    {
        "CDOTA_NPC_Observer_Ward",
        "CDOTA_NPC_Observer_Ward_TrueSight",
    }
)

# Roshan respawn window bounds (in ticks at ~30 ticks/sec)
_ROSH_RESPAWN_MIN_TICKS = 8 * 60 * 30
_ROSH_RESPAWN_MAX_TICKS = 11 * 60 * 30


# ---------------------------------------------------------------------------
# Entity helpers
# ---------------------------------------------------------------------------


def _team(entity: Entity) -> str:
    team, ok = entity.get_int32("m_iTeamNum")
    return TEAM_NAMES.get(team, f"Team{team}") if ok else "?"


def _pos(entity: Entity) -> tuple[float, float] | None:
    """Return world (x, y) from cell+vec encoding, or None."""
    cell_x, ok_cx = entity.get_int32("CBodyComponent.m_cellX")
    cell_y, ok_cy = entity.get_int32("CBodyComponent.m_cellY")
    vec_x, ok_vx = entity.get_float32("CBodyComponent.m_vecX")
    vec_y, ok_vy = entity.get_float32("CBodyComponent.m_vecY")
    if not (ok_cx and ok_cy and ok_vx and ok_vy):
        return None
    return (cell_x * _CELL_SIZE + vec_x, cell_y * _CELL_SIZE + vec_y)


def _fmt_tick(tick: int) -> str:
    """Format a tick as MM:SS (assumes ~30 ticks/second)."""
    secs = tick // 30
    return f"{secs // 60:02d}:{secs % 60:02d}"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


class WardPlacement:
    """One ward placed: from combat log (who/when) + optional entity coordinates."""

    __slots__ = ("tick", "placer", "ward_type", "hero_pos", "entity_pos")

    def __init__(
        self, tick: int, placer: str, ward_type: str, hero_pos: tuple[float, float] | None
    ) -> None:
        self.tick = tick
        self.placer = placer
        self.ward_type = ward_type
        self.hero_pos = hero_pos  # placer position at tick
        self.entity_pos: tuple[float, float] | None = None  # filled from entity stream


class SmokeEvent:
    """One Smoke of Deceit activation."""

    __slots__ = ("tick", "activator", "smoked", "dispelled")

    def __init__(self, tick: int, activator: str) -> None:
        self.tick = tick
        self.activator = activator
        self.smoked: list[str] = []  # heroes that received the modifier
        self.dispelled: list[str] = []  # heroes whose smoke was removed

    @property
    def still_active(self) -> bool:
        return bool(self.smoked) and len(self.dispelled) < len(self.smoked)


class RoshanKill:
    """One confirmed Roshan death from the combat log."""

    __slots__ = ("tick", "killer", "xp_total")

    def __init__(self, tick: int, killer: str, xp_total: int) -> None:
        self.tick = tick
        self.killer = killer
        self.xp_total = xp_total  # sum of XP events at same tick (kill reward)


# ---------------------------------------------------------------------------
# Collectors
# ---------------------------------------------------------------------------


class WardSmokeCollector:
    """Collects ward placements and smoke events from the combat log."""

    def __init__(
        self,
        hero_pos_lookup: Callable[[str], tuple[float, float] | None] | None = None,
    ) -> None:
        self._hero_pos_lookup = hero_pos_lookup
        self.ward_placements: list[WardPlacement] = []
        self.smoke_events: list[SmokeEvent] = []
        self._active_smokes: dict[str, SmokeEvent] = {}

    def __call__(self, entry: CombatLogEntry) -> None:
        if entry.log_type == "ITEM" and entry.inflictor_name in _WARD_ITEMS:
            ward_type = _ITEM_TO_WARD_TYPE[entry.inflictor_name]
            hero_pos = self._hero_pos_lookup(entry.attacker_name) if self._hero_pos_lookup else None
            self.ward_placements.append(
                WardPlacement(entry.tick, entry.attacker_name, ward_type, hero_pos)
            )

        elif entry.log_type == "ITEM" and entry.inflictor_name == _SMOKE_ITEM:
            smoke = SmokeEvent(entry.tick, entry.attacker_name)
            self._active_smokes[entry.attacker_name] = smoke
            self.smoke_events.append(smoke)

        elif (
            entry.log_type == "MODIFIER_ADD"
            and entry.inflictor_name == _SMOKE_MODIFIER
            and entry.target_is_hero
        ):  # exclude summons/illusions
            active = self._active_smokes.get(entry.attacker_name)
            if active is not None:
                active.smoked.append(entry.target_name)

        elif (
            entry.log_type == "MODIFIER_REMOVE"
            and entry.inflictor_name == _SMOKE_MODIFIER
            and entry.target_is_hero
        ):
            active = self._active_smokes.get(entry.attacker_name)
            if active is not None:
                active.dispelled.append(entry.target_name)
                if len(active.dispelled) >= len(active.smoked):
                    self._active_smokes.pop(entry.attacker_name, None)


class RoshanCollector:
    """Tracks Roshan kill events and XP rewards from the combat log."""

    def __init__(self) -> None:
        self.kills: list[RoshanKill] = []
        self._pending_xp: dict[int, int] = {}  # tick -> total XP at that tick

    def __call__(self, entry: CombatLogEntry) -> None:
        if entry.log_type == "DEATH" and entry.target_name == "npc_dota_roshan":
            kill = RoshanKill(
                tick=entry.tick,
                killer=entry.attacker_name,
                xp_total=self._pending_xp.get(entry.tick, 0),
            )
            self.kills.append(kill)

        elif entry.log_type == "XP":
            # Accumulate XP events at the same tick — Roshan kill grants a burst
            self._pending_xp[entry.tick] = self._pending_xp.get(entry.tick, 0) + entry.value


class EntityTracker:
    """Tracks ward entity spawns (for coordinates) and hero positions."""

    def __init__(self) -> None:
        self.current_tick: int = 0
        # Ward entity spawn log: (tick, ward_type, team, x, y)
        self.ward_spawns: list[tuple[int, str, str, float, float]] = []
        # Hero position lookup by npc name
        self._heroes_by_npc: dict[str, Entity] = {}

    def on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls.startswith("CDOTA_Unit_Hero_"):
            npc = cls.replace("CDOTA_Unit_Hero_", "npc_dota_hero_").lower()
            if op & EntityOp.DELETED:
                self._heroes_by_npc.pop(npc, None)
            else:
                self._heroes_by_npc[npc] = entity

        elif cls in _WARD_OBSERVER_CLASSES:
            # Record every entity event that carries a valid position — including
            # UPDATED events on recycled slots. The matcher allows the same entity
            # slot to be matched to multiple placements at different ticks.
            ward_type = "sentry" if "TrueSight" in cls else "observer"
            pos = _pos(entity)
            if pos is not None and not (op & EntityOp.DELETED):
                self.ward_spawns.append(
                    (self.current_tick, ward_type, _team(entity), pos[0], pos[1])
                )

    def hero_pos(self, npc_name: str) -> tuple[float, float] | None:
        """Return current world position of the named hero, or None."""
        entity = self._heroes_by_npc.get(npc_name.lower())
        return _pos(entity) if entity is not None else None


# ---------------------------------------------------------------------------
# Coordinate matching
# ---------------------------------------------------------------------------


def match_ward_coords(
    placements: list[WardPlacement],
    spawns: list[tuple[int, str, str, float, float]],
    ward_type: str,
    window: int = 60,
) -> None:
    """Match WardPlacements to entity spawn records; fill entity_pos in place.

    Entity slots are reused across the game, so the same (index, pos) pair may
    appear many times. We allow the same spawn record to match multiple placements
    — each placement is matched to the nearest entity event within ``window`` ticks.

    Args:
        placements: WardPlacement objects of the given ward_type.
        spawns: All (tick, ward_type, team, x, y) entity spawn records.
        ward_type: ``"observer"`` or ``"sentry"``.
        window: Max tick delta to consider a match.
    """
    relevant = sorted(
        [(t, x, y) for t, wt, _tm, x, y in spawns if wt == ward_type],
        key=lambda e: e[0],
    )
    for wp in placements:
        best_pos, best_dt = None, window + 1
        for et, ex, ey in relevant:
            if et < wp.tick - window:
                continue
            if et > wp.tick + window:
                break
            dt = abs(et - wp.tick)
            if dt < best_dt:
                best_pos, best_dt = (ex, ey), dt
        if best_pos is not None:
            wp.entity_pos = best_pos


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _sep(title: str = "") -> None:
    width = 76
    if title:
        pad = (width - len(title) - 2) // 2
        print(f"\n{'─' * pad} {title} {'─' * pad}")
    else:
        print("\n" + "─" * width)


def report_wards(placements: list[WardPlacement]) -> None:
    obs = [w for w in placements if w.ward_type == "observer"]
    sen = [w for w in placements if w.ward_type == "sentry"]

    for label, wards in (("Observer", obs), ("Sentry", sen)):
        n_exact = sum(1 for w in wards if w.entity_pos is not None)
        n_approx = sum(1 for w in wards if w.entity_pos is None and w.hero_pos is not None)
        n_none = len(wards) - n_exact - n_approx

        _sep(f"{label.upper()} WARDS  ({len(wards)} total)")
        print(f"  Coords: {n_exact} exact  |  {n_approx} approx (hero pos)  |  {n_none} missing")
        print()
        print(f"  {'Time':<7} {'Hero':<24} {'Coordinates':<28}  Source")
        print(f"  {'─' * 7} {'─' * 24} {'─' * 28}  {'─' * 15}")

        by_hero: dict[str, int] = defaultdict(int)
        for w in wards:
            if (pos := w.entity_pos) is not None:
                coord_str = f" ({pos[0]:>8.1f}, {pos[1]:>8.1f})"
                source = "exact"
            elif (pos := w.hero_pos) is not None:
                coord_str = f"~({pos[0]:>8.1f}, {pos[1]:>8.1f})"
                source = "hero pos approx"
            else:
                coord_str = "            (no pos)"
                source = ""
            name = hero_short(w.placer)
            print(f"  {_fmt_tick(w.tick):<7} {name:<24} {coord_str:<28}  {source}")
            by_hero[name] += 1

        print("\n  Per-hero summary:")
        for name, count in sorted(by_hero.items(), key=lambda x: -x[1]):
            print(f"    {name:<26} {count:>3}  {label.lower()} ward{'s' if count != 1 else ''}")


def report_smokes(smoke_events: list[SmokeEvent]) -> None:
    _sep(f"SMOKE OF DECEIT  ({len(smoke_events)} usages)")
    if not smoke_events:
        print("  (none recorded)")
        return

    sizes = [len(s.smoked) for s in smoke_events if s.smoked]

    print(f"  {'Time':<7} {'Activator':<24}  Group (heroes only)")
    print(f"  {'─' * 7} {'─' * 24}  {'─' * 44}")

    by_activator: dict[str, int] = defaultdict(int)
    for smoke in smoke_events:
        activator = hero_short(smoke.activator)
        group = (
            ", ".join(hero_short(h) for h in smoke.smoked)
            if smoke.smoked
            else "(no heroes resolved)"
        )
        status = "ACTIVE" if smoke.still_active else "expired/broken"
        print(f"  {_fmt_tick(smoke.tick):<7} {activator:<24}  {group}  [{status}]")
        by_activator[activator] += 1

    print("\n  Initiator breakdown:")
    for name, count in sorted(by_activator.items(), key=lambda x: -x[1]):
        print(f"    {name:<26} {count}x")

    if sizes:
        avg = sum(sizes) / len(sizes)
        print(f"\n  Avg group size: {avg:.1f}  (min {min(sizes)}, max {max(sizes)})")


def report_roshan(kills: list[RoshanKill]) -> None:
    _sep(f"ROSHAN  ({len(kills)} kill(s))")
    if not kills:
        print("  Roshan was not killed in this replay.")
        return

    print(f"  {'#':<3} {'Time':<7} {'Last hit by':<24}  Respawn window")
    print(f"  {'─' * 3} {'─' * 7} {'─' * 24}  {'─' * 22}")

    for n, kill in enumerate(kills, start=1):
        killer = hero_short(kill.killer) if kill.killer else "(unknown)"
        rmin = _fmt_tick(kill.tick + _ROSH_RESPAWN_MIN_TICKS)
        rmax = _fmt_tick(kill.tick + _ROSH_RESPAWN_MAX_TICKS)
        print(f"  {n:<3} {_fmt_tick(kill.tick):<7} {killer:<24}  {rmin} – {rmax}")

    print()
    print("  Note: Aegis/Cheese pickup is not recorded in the combat log.")
    print("        Track item entities or CDOTAUserMsg_ItemPurchased for drop details.")


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
    print("Parsing...")

    tracker = EntityTracker()
    ward_smoke = WardSmokeCollector(hero_pos_lookup=tracker.hero_pos)
    rosh = RoshanCollector()

    parser = ReplayParser(dem_path)
    parser.on_combat_log_entry(ward_smoke)
    parser.on_combat_log_entry(rosh)

    def _on_entity(entity: Entity, op: EntityOp) -> None:
        tracker.current_tick = parser.tick
        tracker.on_entity(entity, op)

    parser.on_entity(_on_entity)
    parser.parse()

    last_tick = parser.tick
    print(f"Done. Duration: {_fmt_tick(last_tick)}  (tick {last_tick:,})\n")

    # Match ward placement records to entity spawn coordinates
    obs = [w for w in ward_smoke.ward_placements if w.ward_type == "observer"]
    sen = [w for w in ward_smoke.ward_placements if w.ward_type == "sentry"]
    match_ward_coords(obs, tracker.ward_spawns, "observer")
    match_ward_coords(sen, tracker.ward_spawns, "sentry")

    report_wards(ward_smoke.ward_placements)
    report_smokes(ward_smoke.smoke_events)
    report_roshan(rosh.kills)

    _sep()
    print(
        f"Summary: {len(obs)} observer wards  |  {len(sen)} sentry wards  |  "
        f"{len(ward_smoke.smoke_events)} smokes  |  {len(rosh.kills)} Roshan kill(s)"
    )


if __name__ == "__main__":
    main()
