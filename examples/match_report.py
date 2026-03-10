"""Phase 6 showcase — full match report using the gem public API.

Demonstrates everything extractable after Phase 6, structured to mirror
what Dotabuff (TrueSight), Stratz, and OpenDota show on their match pages:

  Section 1 — Scoreboard          (OpenDota overview / Dotabuff summary)
  Section 2 — Gold advantage graph (OpenDota gold graph / Stratz net worth)
  Section 3 — Objectives timeline  (Stratz objectives / OpenDota log)
  Section 4 — Ward map summary     (Dotabuff Vision tab / Stratz vision)
  Section 5 — Damage breakdown     (Dotabuff Combat tab / OpenDota abilities)
  Section 6 — Kill feed            (OpenDota kills log)
  Section 7 — Purchase timeline    (OpenDota items tab / Dotabuff items)

Built entirely on top of ``gem.parse()`` — no internal imports required.

Usage:
    python examples/match_report.py <path/to/replay.dem>

Or without arguments to use the bundled fixture:
    python examples/match_report.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich import box
from rich.console import Console
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

import gem
from gem.constants import ability_display, hero_short, item_display

console = Console()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TEAM_COLOR = {2: "green", 3: "red"}
TEAM_NAMES = {2: "Radiant", 3: "Dire"}
TICKS_PER_SEC = 30
TICKS_PER_MIN = TICKS_PER_SEC * 60
_MAP_MID = 8192.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fmt_tick(tick: int) -> str:
    """Format a game tick as MM:SS."""
    secs = tick // TICKS_PER_SEC
    return f"{secs // 60:02d}:{secs % 60:02d}"


def _team_name(team: int) -> str:
    return TEAM_NAMES.get(team, f"Team{team}")


def _team_text(team: int) -> Text:
    color = TEAM_COLOR.get(team, "white")
    return Text(_team_name(team), style=f"bold {color}")


def _hero(npc_name: str) -> str:
    return hero_short(npc_name) if npc_name else "?"


def _ward_zone(x: float, y: float) -> str:
    top = y > _MAP_MID
    right = x > _MAP_MID
    if top and not right:
        return "Radiant jungle / top"
    if top and right:
        return "Dire jungle / top"
    if not top and not right:
        return "Radiant jungle / bot"
    return "Dire jungle / bot"


def _sparkline(values: list[int] | list[float], width: int = 40) -> str:
    """Render a list of floats as a compact Unicode sparkline."""
    if not values:
        return ""
    bars = " ▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    span = hi - lo or 1
    step = max(1, len(values) // width)
    sampled = values[::step][:width]
    return "".join(bars[min(8, int((v - lo) / span * 8))] for v in sampled)


def _bar(value: int, max_value: int, width: int = 20) -> str:
    if max_value == 0:
        return ""
    filled = min(width, int(value / max_value * width))
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------------------
# Section 1 — Scoreboard
# ---------------------------------------------------------------------------


def report_scoreboard(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]SCOREBOARD[/bold cyan]"))

    # Build K/D/A from combat log
    hero_kills: Counter[str] = Counter()
    hero_deaths: Counter[str] = Counter()
    hero_assists: Counter[str] = Counter()
    hero_death_ticks: dict[str, list[int]] = {}

    for entry in match.combat_log:
        if entry.log_type != "DEATH" or not entry.target_is_hero:
            continue
        if entry.attacker_is_hero and entry.attacker_name:
            hero_kills[entry.attacker_name] += 1
        if entry.target_name:
            hero_deaths[entry.target_name] += 1
            hero_death_ticks.setdefault(entry.target_name, []).append(entry.tick)

    _DMG_WINDOW = 15 * TICKS_PER_SEC
    damage_at: dict[tuple[str, int], set[str]] = {}
    for entry in match.combat_log:
        if entry.log_type != "DAMAGE" or not entry.attacker_is_hero:
            continue
        for t in hero_death_ticks.get(entry.target_name, []):
            if 0 <= t - entry.tick <= _DMG_WINDOW:
                damage_at.setdefault((entry.target_name, t), set()).add(entry.attacker_name)

    for (_target, _death_tick), attackers in damage_at.items():
        for a in attackers:
            if a != _target:
                hero_assists[a] += 1

    for entry in match.combat_log:
        if (
            entry.log_type == "DEATH"
            and entry.target_is_hero
            and entry.attacker_is_hero
            and entry.attacker_name in hero_assists
        ):
            hero_assists[entry.attacker_name] -= 1

    for team in (2, 3):
        color = TEAM_COLOR[team]
        team_players = [p for p in match.players if p.team == team and p.hero_name]
        if not team_players:
            continue

        console.print()
        console.print(f"  [{color}]{_team_name(team).upper()}[/{color}]")

        tbl = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style=f"bold {color}",
            pad_edge=False,
        )
        tbl.add_column("Hero", min_width=22)
        tbl.add_column("K", justify="right", min_width=4)
        tbl.add_column("D", justify="right", min_width=4)
        tbl.add_column("A", justify="right", min_width=4)
        tbl.add_column("LH", justify="right", min_width=5)
        tbl.add_column("DN", justify="right", min_width=4)
        tbl.add_column("Gold", justify="right", min_width=7)
        tbl.add_column("Dmg", justify="right", min_width=8)
        tbl.add_column("Heal", justify="right", min_width=7)
        tbl.add_column("Obs", justify="right", min_width=4)
        tbl.add_column("Sen", justify="right", min_width=4)

        for pp in team_players:
            npc = pp.hero_name
            k = hero_kills.get(npc, 0)
            d = hero_deaths.get(npc, 0)
            assists: int = max(0, hero_assists.get(npc, 0))
            final_gold = pp.gold_t[-1] if pp.gold_t else 0
            final_lh = pp.lh_t[-1] if pp.lh_t else 0
            final_dn = pp.dn_t[-1] if pp.dn_t else 0
            total_dmg = sum(pp.damage.values())
            total_heal = sum(pp.healing.values())
            obs = len(pp.obs_log)
            sen = len(pp.sen_log)
            tbl.add_row(
                _hero(npc),
                str(k),
                str(d),
                str(assists),
                str(final_lh),
                str(final_dn),
                f"{final_gold:,}",
                f"{total_dmg:,}",
                f"{total_heal:,}",
                str(obs),
                str(sen),
            )
        console.print(tbl)


# ---------------------------------------------------------------------------
# Section 2 — Gold advantage graph
# ---------------------------------------------------------------------------


def report_gold_advantage(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]GOLD & XP ADVANTAGE  (Radiant − Dire)[/bold cyan]"))

    radiant = [p for p in match.players if p.team == 2 and p.gold_t]
    dire = [p for p in match.players if p.team == 3 and p.gold_t]

    if not radiant or not dire:
        console.print("  [dim](not enough time-series data)[/dim]")
        return

    all_ticks = sorted({t for p in match.players for t in p.times})
    if not all_ticks:
        return

    def _gold_at(players: list, tick: int) -> int:
        total = 0
        for p in players:
            if tick in p.times:
                idx = p.times.index(tick)
                total += p.gold_t[idx]
        return total

    adv_gold: list[int] = []
    adv_xp: list[int] = []
    ticks_used: list[int] = []

    for tick in all_ticks:
        rg = _gold_at(radiant, tick)
        dg = _gold_at(dire, tick)
        rx = sum(p.xp_t[p.times.index(tick)] for p in radiant if tick in p.times)
        dx = sum(p.xp_t[p.times.index(tick)] for p in dire if tick in p.times)
        if rg == 0 and dg == 0:
            continue
        adv_gold.append(rg - dg)
        adv_xp.append(rx - dx)
        ticks_used.append(tick)

    if not adv_gold:
        console.print("  [dim](no data)[/dim]")
        return

    tbl = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl.add_column("Time", min_width=7)
    tbl.add_column("Gold adv", justify="right", min_width=10)
    tbl.add_column("XP adv", justify="right", min_width=10)
    tbl.add_column("Leader", min_width=10)

    step = max(1, len(ticks_used) // 20)
    for i in range(0, len(ticks_used), step):
        tick = ticks_used[i]
        ga = adv_gold[i]
        xa = adv_xp[i]
        if ga > 0:
            leader = Text("▲ Radiant", style="bold green")
            ga_str = Text(f"+{ga:,}", style="green")
        elif ga < 0:
            leader = Text("▼ Dire", style="bold red")
            ga_str = Text(f"{ga:,}", style="red")
        else:
            leader = Text("─ Even", style="dim")
            ga_str = Text("0", style="dim")

        xa_str = Text(f"+{xa:,}" if xa >= 0 else f"{xa:,}", style="green" if xa >= 0 else "red")
        tbl.add_row(_fmt_tick(tick), ga_str, xa_str, leader)

    console.print(tbl)

    peak_r = max(adv_gold)
    peak_d = min(adv_gold)
    final = adv_gold[-1]
    console.print(f"  Peak [green]Radiant[/green] lead : [green]+{peak_r:,}[/green] gold")
    console.print(f"  Peak [red]Dire[/red] lead    : [red]+{abs(peak_d):,}[/red] gold")
    color = "green" if final > 0 else ("red" if final < 0 else "dim")
    side = "Radiant" if final > 0 else ("Dire" if final < 0 else "even")
    console.print(f"  Final advantage   : [{color}]{final:+,}[/{color}] gold ({side})")

    console.print()
    console.print("  [dim]Gold advantage sparkline (Radiant positive ↑)[/dim]")
    console.print(f"  {_sparkline(adv_gold, width=60)}")


# ---------------------------------------------------------------------------
# Section 3 — Objectives timeline
# ---------------------------------------------------------------------------


def report_objectives(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]OBJECTIVES TIMELINE[/bold cyan]"))

    events: list[tuple[int, str, str, str]] = []  # tick, type, team_color, desc

    for t in match.towers:
        color = TEAM_COLOR.get(t.team, "white")
        name = t.tower_name.replace("npc_dota_", "").replace("_", " ")
        killer = _hero(t.killer) if t.killer.startswith("npc_dota_hero_") else t.killer
        events.append(
            (
                t.tick,
                "Tower",
                color,
                f"[{color}]{_team_name(t.team)}[/{color}] {name} — killed by {killer}",
            )
        )

    for b in match.barracks:
        color = TEAM_COLOR.get(b.team, "white")
        name = b.barracks_name.replace("npc_dota_", "").replace("_", " ")
        killer = _hero(b.killer) if b.killer.startswith("npc_dota_hero_") else b.killer
        events.append(
            (
                b.tick,
                "Barracks",
                color,
                f"[{color}]{_team_name(b.team)}[/{color}] {name} — killed by {killer}",
            )
        )

    for n, r in enumerate(match.roshans, 1):
        killer = _hero(r.killer) if r.killer else "?"
        respawn_min = _fmt_tick(r.tick + 8 * TICKS_PER_MIN)
        respawn_max = _fmt_tick(r.tick + 11 * TICKS_PER_MIN)
        events.append(
            (
                r.tick,
                f"Roshan #{n}",
                "yellow",
                f"[yellow]Roshan #{n}[/yellow] killed by {killer} — respawns {respawn_min}–{respawn_max}",
            )
        )

    if not events:
        console.print("  [dim](no objective events recorded)[/dim]")
        return

    events.sort(key=lambda e: e[0])

    tbl = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl.add_column("Time", min_width=7)
    tbl.add_column("Type", min_width=10)
    tbl.add_column("Event")

    for tick, etype, color, desc in events:
        tbl.add_row(_fmt_tick(tick), Text(etype, style=f"bold {color}"), Text.from_markup(desc))

    console.print(tbl)
    console.print(
        f"  Towers: [bold]{len(match.towers)}[/bold]  |  "
        f"Barracks: [bold]{len(match.barracks)}[/bold]  |  "
        f"Roshans: [bold]{len(match.roshans)}[/bold]"
    )


# ---------------------------------------------------------------------------
# Section 4 — Ward map summary
# ---------------------------------------------------------------------------


def report_wards(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]WARD MAP[/bold cyan]"))

    obs = [w for w in match.wards if w.ward_type == "observer"]
    sen = [w for w in match.wards if w.ward_type == "sentry"]

    for label, wards, color in (("OBSERVER", obs, "cyan"), ("SENTRY", sen, "magenta")):
        console.print()
        console.print(f"  [{color}]{label} WARDS ({len(wards)} total)[/{color}]")

        with_coords = [w for w in wards if w.x is not None]
        killed = [w for w in wards if w.killed_tick is not None]
        expired = [w for w in wards if w.expires_tick is not None]
        console.print(f"  Coordinates resolved: {len(with_coords)}/{len(wards)}")
        console.print(f"  Destroyed by enemy  : {len(killed)}")
        console.print(f"  Expired naturally   : {len(expired)}")

        if not wards:
            continue

        tbl = Table(box=box.SIMPLE, show_header=True, header_style=f"bold {color}", pad_edge=False)
        tbl.add_column("Time", min_width=7)
        tbl.add_column("Hero", min_width=20)
        tbl.add_column("Team", min_width=8)
        tbl.add_column("Coords", min_width=22)
        tbl.add_column("Fate", min_width=24)
        tbl.add_column("Zone")

        for w in wards:
            coord_str = f"({w.x:>8.0f},{w.y:>8.0f})" if w.x is not None else "(no coords)"
            zone = _ward_zone(float(w.x), float(w.y)) if w.x is not None and w.y is not None else ""
            team_color = TEAM_COLOR.get(w.team, "white")

            if w.killed_tick is not None:
                killer = _hero(w.killer) if w.killer else "?"
                fate = Text(f"killed {_fmt_tick(w.killed_tick)} by {killer}", style="red")
            elif w.expires_tick is not None:
                fate = Text(f"expired {_fmt_tick(w.expires_tick)}", style="dim")
            else:
                fate = Text("active/unknown", style="yellow")

            tbl.add_row(
                _fmt_tick(w.tick),
                _hero(w.placer),
                Text(_team_name(w.team), style=f"bold {team_color}"),
                coord_str,
                fate,
                zone,
            )
        console.print(tbl)

    console.print()
    console.print("  [bold]Wards placed per player[/bold]")
    tbl = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl.add_column("Hero", min_width=22)
    tbl.add_column("Team", min_width=8)
    tbl.add_column("Obs", justify="right", min_width=4)
    tbl.add_column("Sen", justify="right", min_width=4)
    tbl.add_column("Total", justify="right", min_width=6)

    for pp in sorted(match.players, key=lambda p: p.team):
        if not pp.hero_name:
            continue
        o, s = len(pp.obs_log), len(pp.sen_log)
        if o + s == 0:
            continue
        team_color = TEAM_COLOR.get(pp.team, "white")
        tbl.add_row(
            _hero(pp.hero_name),
            Text(_team_name(pp.team), style=f"bold {team_color}"),
            str(o),
            str(s),
            str(o + s),
        )
    console.print(tbl)


# ---------------------------------------------------------------------------
# Section 5 — Damage breakdown
# ---------------------------------------------------------------------------


def report_damage(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]DAMAGE BREAKDOWN[/bold cyan]"))

    for team in (2, 3):
        color = TEAM_COLOR[team]
        team_players = [p for p in match.players if p.team == team and p.hero_name]
        console.print()
        console.print(f"  [{color}]{_team_name(team).upper()}[/{color}]")

        tbl = Table(box=box.SIMPLE, show_header=True, header_style=f"bold {color}", pad_edge=False)
        tbl.add_column("Hero", min_width=22)
        tbl.add_column("Hero Dmg", justify="right", min_width=9)
        tbl.add_column("Top Ability", min_width=32)
        tbl.add_column("Healing", justify="right", min_width=8)

        for pp in team_players:
            total_dmg = sum(pp.damage.values())
            total_heal = sum(pp.healing.values())
            top_ability = ""
            if pp.ability_uses:
                top_ab = max(pp.ability_uses, key=pp.ability_uses.get)  # type: ignore[arg-type]
                top_ability = f"{ability_display(top_ab)} ({pp.ability_uses[top_ab]}x)"
            tbl.add_row(_hero(pp.hero_name), f"{total_dmg:,}", top_ability, f"{total_heal:,}")

        console.print(tbl)

    # Top 5 damage dealers
    console.print()
    console.print("  [bold]Top 5 Damage Dealers[/bold]")
    ranked = sorted(
        [(p, sum(p.damage.values())) for p in match.players if p.hero_name],
        key=lambda x: -x[1],
    )
    max_dmg = ranked[0][1] if ranked else 1

    tbl = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    tbl.add_column("#", min_width=3)
    tbl.add_column("Hero", min_width=22)
    tbl.add_column("Damage", justify="right", min_width=9)
    tbl.add_column("Bar", min_width=22)

    for rank, (pp, dmg) in enumerate(ranked[:5], 1):
        color = TEAM_COLOR.get(pp.team, "white")
        bar = Text(_bar(dmg, max_dmg, 20), style=color)
        tbl.add_row(str(rank), _hero(pp.hero_name), f"{dmg:,}", bar)
    console.print(tbl)

    console.print("  [bold]Top 5 Damage Sponges (received)[/bold]")
    taken_ranked = sorted(
        [(p, sum(p.damage_taken.values())) for p in match.players if p.hero_name],
        key=lambda x: -x[1],
    )
    max_taken = taken_ranked[0][1] if taken_ranked else 1

    tbl2 = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    tbl2.add_column("#", min_width=3)
    tbl2.add_column("Hero", min_width=22)
    tbl2.add_column("Taken", justify="right", min_width=9)
    tbl2.add_column("Bar", min_width=22)

    for rank, (pp, dmg) in enumerate(taken_ranked[:5], 1):
        color = TEAM_COLOR.get(pp.team, "white")
        bar = Text(_bar(dmg, max_taken, 20), style=color)
        tbl2.add_row(str(rank), _hero(pp.hero_name), f"{dmg:,}", bar)
    console.print(tbl2)


# ---------------------------------------------------------------------------
# Section 6 — Kill feed
# ---------------------------------------------------------------------------


def report_kill_feed(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]KILL FEED[/bold cyan]"))

    hvh = [
        e
        for e in match.combat_log
        if e.log_type == "DEATH" and e.attacker_is_hero and e.target_is_hero
    ]

    if not hvh:
        console.print("  [dim](no hero-vs-hero kills recorded)[/dim]")
        return

    console.print(f"  Total hero kills: [bold]{len(hvh)}[/bold]")
    console.print()

    tbl = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl.add_column("Time", min_width=7)
    tbl.add_column("Killer", min_width=22)
    tbl.add_column("Victim", min_width=22)
    tbl.add_column("Via")

    for entry in hvh:
        via = ability_display(entry.inflictor_name) if entry.inflictor_name else "auto-attack"
        tbl.add_row(
            _fmt_tick(entry.tick),
            _hero(entry.attacker_name),
            _hero(entry.target_name),
            via,
        )
    console.print(tbl)

    console.print("  [bold]Kill count per hero[/bold]")
    kill_counts = Counter(e.attacker_name for e in hvh)
    death_counts = Counter(e.target_name for e in hvh)

    tbl2 = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl2.add_column("Hero", min_width=22)
    tbl2.add_column("Team", min_width=8)
    tbl2.add_column("Kills", justify="right", min_width=6)
    tbl2.add_column("Deaths", justify="right", min_width=7)

    for pp in sorted(match.players, key=lambda p: -kill_counts.get(p.hero_name, 0)):
        if not pp.hero_name:
            continue
        k = kill_counts.get(pp.hero_name, 0)
        d = death_counts.get(pp.hero_name, 0)
        if k == 0 and d == 0:
            continue
        color = TEAM_COLOR.get(pp.team, "white")
        tbl2.add_row(
            _hero(pp.hero_name),
            Text(_team_name(pp.team), style=f"bold {color}"),
            str(k),
            str(d),
        )
    console.print(tbl2)


# ---------------------------------------------------------------------------
# Section 7 — Purchase timeline
# ---------------------------------------------------------------------------


def report_purchases(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]PURCHASE TIMELINE[/bold cyan]"))

    total_purchases = sum(len(p.purchase_log) for p in match.players)
    if total_purchases == 0:
        console.print(
            "  [dim](No purchase data available — HLTV/spectator replays may not carry\n"
            "   hero-attributed PURCHASE events in the S2 combat log path.)[/dim]"
        )
        return

    for team in (2, 3):
        color = TEAM_COLOR[team]
        team_players = [p for p in match.players if p.team == team and p.hero_name]
        console.print()
        console.print(f"  [{color}]{_team_name(team).upper()}[/{color}]")

        for pp in team_players:
            if not pp.purchase_log:
                continue
            console.print(f"\n  [bold]{_hero(pp.hero_name)}[/bold]")
            purchases = sorted(pp.purchase_log, key=lambda e: e.tick)[:12]

            tbl = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
            tbl.add_column("Time", min_width=7)
            tbl.add_column("Item")

            for entry in purchases:
                item_name = item_display(entry.value_name) if entry.value_name else entry.value_name
                tbl.add_row(_fmt_tick(entry.tick), item_name)
            console.print(tbl)


# ---------------------------------------------------------------------------
# Section 8 — Buybacks
# ---------------------------------------------------------------------------


def report_buybacks(match: gem.ParsedMatch) -> None:
    total = sum(len(p.buyback_log) for p in match.players)
    console.print()
    console.print(Rule("[bold cyan]BUYBACKS[/bold cyan]"))

    if total == 0:
        console.print("  [dim](no buybacks recorded)[/dim]")
        return

    tbl = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl.add_column("Time", min_width=7)
    tbl.add_column("Hero", min_width=22)
    tbl.add_column("Team", min_width=8)

    for pp in sorted(match.players, key=lambda p: p.team):
        if not pp.buyback_log:
            continue
        color = TEAM_COLOR.get(pp.team, "white")
        for entry in sorted(pp.buyback_log, key=lambda e: e.tick):
            tbl.add_row(
                _fmt_tick(entry.tick),
                _hero(pp.hero_name),
                Text(_team_name(pp.team), style=f"bold {color}"),
            )
    console.print(tbl)
    console.print(f"  Total buybacks: [bold]{total}[/bold]")


# ---------------------------------------------------------------------------
# Section 9 — Rune pickups
# ---------------------------------------------------------------------------


def report_runes(match: gem.ParsedMatch) -> None:
    total = sum(len(p.runes_log) for p in match.players)
    console.print()
    console.print(Rule("[bold cyan]RUNE PICKUPS[/bold cyan]"))

    if total == 0:
        console.print("  [dim](no rune pickups recorded)[/dim]")
        return

    from gem.constants import item_display as _item_disp

    tbl = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl.add_column("Time", min_width=7)
    tbl.add_column("Hero", min_width=22)
    tbl.add_column("Team", min_width=8)
    tbl.add_column("Rune")

    for pp in sorted(match.players, key=lambda p: p.team):
        if not pp.runes_log:
            continue
        color = TEAM_COLOR.get(pp.team, "white")
        for entry in sorted(pp.runes_log, key=lambda e: e.tick):
            tbl.add_row(
                _fmt_tick(entry.tick),
                _hero(pp.hero_name),
                Text(_team_name(pp.team), style=f"bold {color}"),
                _item_disp(entry.inflictor_name),
            )
    console.print(tbl)

    # Per-player summary
    tbl2 = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl2.add_column("Hero", min_width=22)
    tbl2.add_column("Team", min_width=8)
    tbl2.add_column("Runes", justify="right", min_width=6)
    for pp in sorted(match.players, key=lambda p: (-len(p.runes_log), p.team)):
        if not pp.runes_log:
            continue
        color = TEAM_COLOR.get(pp.team, "white")
        tbl2.add_row(
            _hero(pp.hero_name),
            Text(_team_name(pp.team), style=f"bold {color}"),
            str(len(pp.runes_log)),
        )
    console.print(tbl2)


# ---------------------------------------------------------------------------
# Section 10 — Chat log
# ---------------------------------------------------------------------------


def report_chat(match: gem.ParsedMatch) -> None:
    console.print()
    console.print(Rule("[bold cyan]CHAT LOG[/bold cyan]"))

    if not match.chat:
        console.print("  [dim](no chat messages recorded)[/dim]")
        return

    # Build player_slot → hero name map
    slot_to_hero: dict[int, tuple[str, int]] = {}
    for pp in match.players:
        if pp.hero_name:
            slot_to_hero[pp.player_id] = (pp.hero_name, pp.team)

    tbl = Table(box=box.SIMPLE, show_header=True, header_style="bold", pad_edge=False)
    tbl.add_column("Time", min_width=7)
    tbl.add_column("Hero", min_width=22)
    tbl.add_column("Ch", min_width=4)
    tbl.add_column("Message")

    for msg in match.chat:
        hero_name, team = slot_to_hero.get(msg.player_slot, ("?", 0))
        color = TEAM_COLOR.get(team, "white")
        ch_text = Text(
            "ALL" if msg.channel == "all" else "TM",
            style="bold yellow" if msg.channel == "all" else f"bold {color}",
        )
        tbl.add_row(
            _fmt_tick(msg.tick),
            Text(_hero(hero_name), style=color),
            ch_text,
            msg.text,
        )
    console.print(tbl)
    console.print(f"  Total messages: [bold]{len(match.chat)}[/bold]")


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

    console.print(f"Replay : [dim]{dem_path}[/dim]")
    console.print("Parsing with [bold]gem.parse()[/bold] ...")

    match = gem.parse(dem_path)

    last_tick = max((max(p.times) for p in match.players if p.times), default=0)
    duration = _fmt_tick(last_tick)

    console.print(f"Done    : [bold]{duration}[/bold]  ({last_tick:,} ticks)")
    console.print(f"Players : {sum(1 for p in match.players if p.hero_name)}")
    console.print(f"Combat log entries: {len(match.combat_log):,}")

    report_scoreboard(match)
    report_gold_advantage(match)
    report_objectives(match)
    report_wards(match)
    report_damage(match)
    report_kill_feed(match)
    report_purchases(match)
    report_buybacks(match)
    report_runes(match)
    report_chat(match)

    console.print()
    console.print(Rule())
    hvh_kills = sum(
        1
        for e in match.combat_log
        if e.log_type == "DEATH" and e.attacker_is_hero and e.target_is_hero
    )
    total_buybacks = sum(len(p.buyback_log) for p in match.players)
    total_runes = sum(len(p.runes_log) for p in match.players)
    console.print(
        f"[bold]Summary:[/bold] {hvh_kills} hero kills  |  "
        f"{len(match.towers)} towers  |  {len(match.barracks)} barracks  |  "
        f"{len(match.roshans)} Roshan kill(s)  |  "
        f"{len(match.wards)} wards  |  {total_buybacks} buybacks  |  "
        f"{total_runes} runes  |  {len(match.chat)} chat msgs  |  "
        f"duration [bold]{duration}[/bold]"
    )


if __name__ == "__main__":
    main()
