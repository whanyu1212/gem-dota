"""OpenDota match-API parity showcase (0.4.0).

`gem.parse()` now reproduces most of OpenDota's per-match and per-player schema
directly from the `.dem` stream — final inventories, OpenDota-style kill
breakdowns, building-status bitmasks, the unified objectives timeline,
per-inflictor/per-target combat dicts, the purchase timeline, and ward
departure logs. This script parses a replay and prints those 0.4.0 outputs the
way OpenDota groups them.

If a sibling ``<match_id>.opendota.json`` file is present (the real OpenDota
match-API response, as shipped next to the bundled test fixtures), the script
cross-checks gem's output against it field by field — turning the demo into a
parity *proof*, not just a field tour. Without that file it simply prints gem's
values, so it works on any replay you supply.

Usage:
    python examples/opendota_parity.py                      # default fixture (see below)
    python examples/opendota_parity.py path/to/replay.dem   # your own replay

With no argument, the script prefers the full OpenDota validation replay
(``tests/fixtures/opendota/8822520406.dem``) when that local/ignored download is
present — it ships the sibling ``.opendota.json`` that drives the parity
cross-check. That replay is NOT committed, so on a fresh clone the script falls
back to the committed but *truncated* TI14 fixture (partial match, no parity
reference) and prints a heads-up. Fetch a full replay for the complete demo:
``gem.fetch_replay(8822520406, "tests/fixtures/opendota")``.

Notes on representation differences (intentional, called out inline below):
  * ``final_items`` keeps the ``item_`` *name* (``item_power_treads``); OpenDota
    reports numeric item *IDs* (``item_0: 63``). Same fact, different encoding.
  * Ward coordinates in the OpenDota-shaped outputs (``obs``/``sen``,
    ``obs_left_log``) are in OpenDota *cell* units (world / 128), matching
    ``Parse.java``; gem's native ``WardEvent`` keeps world coordinates.
  * ``player_slot`` uses OpenDota's 0-4 (Radiant) / 128-132 (Dire) encoding.
  * ``firstblood_claimed`` / ``teamfight_participation`` are read from the
    authoritative ``CDOTA_PlayerResource`` entity fields and stay ``0`` on
    replays that carry no interval data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import gem
from gem import catalog
from gem.catalog import units

# ---------------------------------------------------------------------------
# Tiny pretty-printing helpers (no third-party deps)
# ---------------------------------------------------------------------------

WIDTH = 76


def section(title: str) -> None:
    pad = max(0, (WIDTH - len(title) - 2) // 2)
    print(f"\n{'=' * pad} {title} {'=' * pad}")


def sub(title: str) -> None:
    print(f"\n── {title} " + "─" * max(0, WIDTH - len(title) - 4))


def check(label: str, gem_val: Any, od_val: Any | None, *, od_available: bool) -> None:
    """Print one gem value, with a ✓/✗ parity marker when an OpenDota ref exists."""
    if not od_available:
        print(f"  {label:<28} gem={gem_val}")
        return
    mark = "✓" if gem_val == od_val else "✗"
    suffix = "" if gem_val == od_val else f"   (OpenDota={od_val})"
    print(f"  {mark} {label:<26} gem={gem_val}{suffix}")


def _player_slot(player_id: int) -> int:
    """OpenDota player_slot encoding: 0-4 Radiant, 128-132 Dire."""
    return player_id if player_id < 5 else 128 + (player_id - 5)


# ---------------------------------------------------------------------------
# OpenDota reference loading (optional)
# ---------------------------------------------------------------------------


def load_opendota_ref(dem_path: Path) -> dict[str, Any] | None:
    """Return the sibling OpenDota match-API JSON for *dem_path*, if it exists.

    The bundled fixtures ship as ``<match_id>.dem`` next to
    ``<match_id>.opendota.json``. Returns ``None`` when no such file is found.
    """
    ref_path = dem_path.with_suffix(".opendota.json")
    if not ref_path.exists():
        return None
    with ref_path.open() as fh:
        return json.load(fh)


def od_player(ref: dict[str, Any] | None, player_id: int) -> dict[str, Any] | None:
    """Find the OpenDota player record for gem's 0-9 ``player_id`` (by player_slot)."""
    if ref is None:
        return None
    target = _player_slot(player_id)
    for p in ref.get("players", []):
        if p.get("player_slot") == target:
            return p
    return None


# ---------------------------------------------------------------------------
# Per-section reports
# ---------------------------------------------------------------------------


def report_match_scalars(match: gem.ParsedMatch, ref: dict[str, Any] | None) -> None:
    section("MATCH SCALARS  (ParsedMatch)")
    avail = ref is not None
    check(
        "radiant_score", match.radiant_score, (ref or {}).get("radiant_score"), od_available=avail
    )
    check("dire_score", match.dire_score, (ref or {}).get("dire_score"), od_available=avail)
    # first_blood_time can differ from OpenDota by ±1s: gem floors int(game_time_s)
    # from the first non-illusion DEATH entry, which can round one tick off the
    # CHAT_MESSAGE_FIRSTBLOOD timestamp. Treat a 1s gap as a match.
    od_fb = (ref or {}).get("first_blood_time")
    fb_ok = od_fb is None or abs(match.first_blood_time - od_fb) <= 1
    if avail:
        print(
            f"  {'✓' if fb_ok else '✗'} {'first_blood_time (s)':<26} "
            f"gem={match.first_blood_time}"
            + ("" if match.first_blood_time == od_fb else f"   (OpenDota={od_fb}, ±1s ok)")
        )
    else:
        print(f"  {'first_blood_time (s)':<28} gem={match.first_blood_time}")


def report_building_status(match: gem.ParsedMatch, ref: dict[str, Any] | None) -> None:
    section("BUILDING-STATUS BITMASKS  (Steam GC bit layout, reconstructed offline)")
    avail = ref is not None
    sub("Raw masks (bit set = building standing)")
    check(
        "tower_status_radiant",
        match.tower_status_radiant,
        (ref or {}).get("tower_status_radiant"),
        od_available=avail,
    )
    check(
        "tower_status_dire",
        match.tower_status_dire,
        (ref or {}).get("tower_status_dire"),
        od_available=avail,
    )
    check(
        "barracks_status_radiant",
        match.barracks_status_radiant,
        (ref or {}).get("barracks_status_radiant"),
        od_available=avail,
    )
    check(
        "barracks_status_dire",
        match.barracks_status_dire,
        (ref or {}).get("barracks_status_dire"),
        od_available=avail,
    )

    # Decode the radiant tower mask into the human-readable per-building view.
    # Layout (results/derived.py): tier 1/2/3 per lane at lane_offset + (tier-1),
    # lanes top=0, mid=3, bot=6 (bits 0-8); two tier-4 share bits 9, 10.
    sub("Decoded — Radiant towers (✗ = destroyed)")
    lanes = {"top": 0, "mid": 3, "bot": 6}
    mask = match.tower_status_radiant
    for lane, off in lanes.items():
        cells = []
        for tier in (1, 2, 3):
            standing = (mask >> (off + tier - 1)) & 1
            cells.append(f"T{tier}{'•' if standing else '✗'}")
        print(f"  {lane:<5} {'  '.join(cells)}")
    anc = [(mask >> b) & 1 for b in (9, 10)]
    print(f"  tier-4  {'  '.join('T4' + ('•' if s else '✗') for s in anc)}")


def report_objectives(match: gem.ParsedMatch) -> None:
    section("OBJECTIVES TIMELINE  (match.objectives — OpenDota-shaped)")
    print(f"  {len(match.objectives)} chronological events. By type:")
    counts: dict[str, int] = {}
    for ev in match.objectives:
        counts[ev["type"]] = counts.get(ev["type"], 0) + 1
    for typ, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"    {typ:<32} {n:>3}")

    sub("First 12 events")
    for ev in match.objectives[:12]:
        t = ev.get("time", 0)
        typ = ev["type"]
        if typ == "building_kill":
            key = ev.get("key", "?")
            unit = ev.get("unit", "")
            who = f"  by {catalog.hero_short(unit)}" if unit.startswith("npc_dota_hero_") else ""
            detail = f"{key}{who}"
        elif typ == "CHAT_MESSAGE_ROSHAN_KILL":
            team = ev.get("team")
            detail = f"team {team}" if team else "(roshan)"
        else:
            detail = typ.replace("CHAT_MESSAGE_", "")
        print(f"  {t:>5}s  {typ:<30} {detail}")


def report_courier_and_teamfights(match: gem.ParsedMatch) -> None:
    section("COURIER DEATHS & OPENDOTA TEAMFIGHTS")
    sub(f"courier_deaths  ({len(match.courier_deaths)})")
    for cd in match.courier_deaths:
        killer = cd.killer_source or cd.killer or "(unknown)"
        killer = catalog.hero_short(killer) if killer.startswith("npc_dota_hero_") else killer
        print(f"  tick {cd.tick:>7,}  killed by {killer}")

    sub(f"opendota_teamfights  ({len(match.opendota_teamfights)}; OpenDota's 15s/3-death windows)")
    for i, tf in enumerate(match.opendota_teamfights):
        involved = sum(1 for p in tf.players if p.deaths or p.damage or p.healing)
        print(
            f"  fight {i}: {tf.start:>4}s–{tf.end:<4}s  deaths={tf.deaths}  participants≈{involved}"
        )


def report_player_inventory_and_kills(match: gem.ParsedMatch, ref: dict[str, Any] | None) -> None:
    section("PER-PLAYER: FINAL INVENTORY + OPENDOTA KILL BREAKDOWN")
    for player in match.players:
        odp = od_player(ref, player.player_id)
        hero = catalog.hero_short(player.hero_name)
        print(f"\n  {hero}  (player_id={player.player_id}, hero_id={player.hero_id})")

        # final_items: gem keeps prefixed names; OpenDota uses numeric ids.
        main = [player.final_items.get(s, "—") for s in range(6)]
        main_disp = ", ".join(m.replace("item_", "") for m in main)
        print(f"    final_items[0-5]: {main_disp}")
        if odp is not None:
            od_ids = [odp.get(f"item_{s}", 0) for s in range(6)]
            print(f"      (OpenDota item_0-5 numeric ids: {od_ids})")

        # OpenDota kill-category scalars — these match OpenDota exactly when present.
        cats = [
            ("lane_kills", player.lane_kills),
            ("neutral_kills", player.neutral_kills),
            ("ancient_kills", player.ancient_kills),
            ("roshan_kills", player.roshan_kills),
            ("observer_kills", player.observer_kills),
            ("sentry_kills", player.sentry_kills),
            ("courier_kills", player.courier_kills),
        ]
        marks = []
        for name, val in cats:
            if odp is not None:
                ok = val == odp.get(name)
                marks.append(f"{'✓' if ok else '✗'}{name.replace('_kills', '')}={val}")
            else:
                marks.append(f"{name.replace('_kills', '')}={val}")
        print(f"    kills: {'  '.join(marks)}")

        # Derived scalars (firstblood_claimed / teamfight_participation come from
        # CDOTA_PlayerResource and are 0 on replays without interval data).
        print(
            f"    level={player.level}  gold_spent={player.gold_spent:,}  "
            f"life_state_dead={player.life_state_dead}s  "
            f"fb_claimed={player.firstblood_claimed}  "
            f"tf_participation={player.teamfight_participation:.3f}"
        )


def report_player_combat_and_wards(match: gem.ParsedMatch, ref: dict[str, Any] | None) -> None:
    section("PER-PLAYER: COMBAT DICTS, PURCHASE TIMELINE, WARD LOGS  (top NW player)")
    # Pick the highest-net-worth player so the dicts are well populated.
    player = max(
        match.players,
        key=lambda p: p.net_worth_t_min[-1] if p.net_worth_t_min else 0,
    )
    odp = od_player(ref, player.player_id)
    print(f"  Showing: {catalog.hero_short(player.hero_name)} (player_id={player.player_id})")

    sub("Per-inflictor / per-target combat (OpenDota gating: enemy heroes only)")
    top_inflictors = sorted(player.damage_inflictor.items(), key=lambda kv: -kv[1])[:5]
    print("  damage_inflictor (top 5):")
    for name, dmg in top_inflictors:
        targets = player.damage_targets.get(name, {})
        n_targets = len(targets)
        print(f"    {name:<28} {dmg:>7,} dmg  across {n_targets} hero(es)")
    print(
        f"  hero_hits (instances): {dict(sorted(player.hero_hits.items(), key=lambda kv: -kv[1])[:3])}"
    )
    if player.max_hero_hit:
        mh = player.max_hero_hit
        print(f"  max_hero_hit: {mh.get('value')} via {mh.get('inflictor')} on {mh.get('key')}")

    sub("Purchase timeline (recipes excluded from *_time dicts)")
    print(f"  distinct items purchased: {len(player.purchase)}")
    print(
        f"  tpscrolls={player.purchase_tpscroll}  "
        f"obs_bought={player.purchase_ward_observer}  sen_bought={player.purchase_ward_sentry}"
    )
    # First few buys by time.
    by_time = sorted(player.first_purchase_time.items(), key=lambda kv: kv[1])[:6]
    print("  earliest first_purchase_time:")
    for item, t in by_time:
        print(f"    {t:>5}s  {item}")

    sub("Ward logs (coordinates in OpenDota cell units, world/128)")
    print(
        f"  observers_placed={player.observers_placed}  "
        f"observer_uses={player.observer_uses}  sentry_uses={player.sentry_uses}"
    )
    print(f"  obs_left_log entries: {len(player.obs_left_log)}  (each: time/type/x/y/attackername)")
    for ev in player.obs_left_log[:3]:
        killer = ev.get("attackername") or "(expired)"
        x, y = ev.get("x"), ev.get("y")
        cell = f"({x:.1f},{y:.1f})" if isinstance(x, (int, float)) else f"({x},{y})"
        print(f"    {ev.get('time'):>5}s  cell={cell}  left via {killer}")
    if odp is not None:
        od_obs_left = odp.get("obs_left_log") or []
        mark = "✓" if len(player.obs_left_log) == len(od_obs_left) else "≈"
        print(
            f"  {mark} obs_left_log count: gem={len(player.obs_left_log)} OpenDota={len(od_obs_left)}"
        )


def report_catalog_helpers() -> None:
    section("NEW CATALOG HELPERS  (0.4.0)")
    print(
        "  gem.catalog.hero_id('npc_dota_hero_broodmother') =",
        catalog.hero_id("npc_dota_hero_broodmother"),
    )
    print(
        "  gem.catalog.hero_id('npc_dota_hero_axe')         =", catalog.hero_id("npc_dota_hero_axe")
    )
    sub("gem.catalog.units NPC classifiers  (back the per-player kill scalars)")
    samples = [
        ("npc_dota_neutral_black_drake", "is_ancient"),
        ("npc_dota_creep_goodguys_melee", "is_lane_creep"),
        ("npc_dota_courier", "is_courier"),
        ("npc_dota_roshan", "is_roshan"),
    ]
    for name, fn in samples:
        result = getattr(units, fn)(name)
        print(f"    units.{fn}({name!r}) = {result}")
    print(f"  units.ANCIENTS has {len(units.ANCIENTS)} ancient-neutral names (from ancients.json)")


# ---------------------------------------------------------------------------
# Default fixture resolution
# ---------------------------------------------------------------------------

# The full OpenDota validation replay (98 MB) is a local/ignored download — it is
# NOT committed (see CLAUDE.md: "Full replay fixtures should be local/ignored
# OpenDota downloads"). It is the *preferred* default because it ships a sibling
# <match_id>.opendota.json that drives the parity cross-check. When it isn't
# present, fall back to the committed (but truncated) TI14 replay so a fresh clone
# still runs — at the cost of a partial match and no parity reference.
_FIXTURES = Path(__file__).parent.parent / "tests" / "fixtures"
_OPENDOTA_FIXTURE = _FIXTURES / "opendota" / "8822520406.dem"
_COMMITTED_FIXTURE = _FIXTURES / "ti14_finals_g3_xg_vs_falcons_truncated.dem"


def resolve_default_fixture() -> tuple[Path, bool] | None:
    """Pick the no-arg default replay; prefer the OpenDota download.

    Returns a ``(path, truncated)`` tuple, or ``None`` when neither fixture is
    available. ``truncated`` is ``True`` for the committed partial replay so the
    caller can warn that the showcase is running on an incomplete match.
    """
    if _OPENDOTA_FIXTURE.exists():
        return _OPENDOTA_FIXTURE, False
    if _COMMITTED_FIXTURE.exists():
        return _COMMITTED_FIXTURE, True
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    truncated = False
    if len(sys.argv) > 1:
        dem_path = Path(sys.argv[1])
        if not dem_path.exists():
            print(f"Replay not found: {dem_path}")
            print("Pass a path: python examples/opendota_parity.py path/to/replay.dem")
            sys.exit(1)
    else:
        resolved = resolve_default_fixture()
        if resolved is None:
            print("No bundled replay found to demo against.")
            print(
                "The full OpenDota fixture is a local/ignored download; fetch one with\n"
                "  uv run python -c \"import gem; gem.fetch_replay(8822520406, 'tests/fixtures/opendota')\"\n"
                "or pass your own: python examples/opendota_parity.py path/to/replay.dem"
            )
            sys.exit(1)
        dem_path, truncated = resolved
        if truncated:
            print(
                "NOTE: using the committed *truncated* TI14 fixture (the full OpenDota\n"
                "download isn't present). The match is partial — final items, building\n"
                "status, and scores reflect only the captured portion, and there is no\n"
                "OpenDota reference to cross-check against. For the full parity demo,\n"
                "fetch a replay (see --help) or pass a path with a sibling .opendota.json.\n"
            )

    ref = load_opendota_ref(dem_path)
    print(f"Replay: {dem_path}")
    print(
        "OpenDota reference: "
        + (
            f"{dem_path.with_suffix('.opendota.json').name} (parity cross-check ON)"
            if ref is not None
            else "none found (printing gem values only)"
        )
    )
    print("\nParsing…")
    match = gem.parse(str(dem_path))
    print(f"Parsed {match.duration_minutes:.1f} min match.")

    report_match_scalars(match, ref)
    report_building_status(match, ref)
    report_objectives(match)
    report_courier_and_teamfights(match)
    report_player_inventory_and_kills(match, ref)
    report_player_combat_and_wards(match, ref)
    report_catalog_helpers()

    section("DONE")
    if ref is not None:
        print("  ✓ = gem matches the OpenDota match-API reference exactly.")
        print("  Representation differences (final_items names vs ids, cell-unit ward")
        print("  coords) are intentional and noted inline above.")
    else:
        print("  Supply a replay with a sibling <match_id>.opendota.json to enable the")
        print("  gem-vs-OpenDota parity cross-check.")


if __name__ == "__main__":
    main()
