"""Audit gem's output against OpenDota's parsed match JSON, field by field.

Runs offline over the local OpenDota fixtures (``tests/fixtures/opendota``: a
``<match_id>.dem`` next to its ``<match_id>.opendota.json``). For each match
OpenDota fully parsed, it parses the replay with gem (or loads a cached
``to_json`` file), maps gem's output format onto OpenDota's, and reports how
many matches and players agree on each field.

The mapping keeps only value differences:

- Per-minute arrays use gem's ``*_min`` fields and ``game_times_min``; gem's
  ``gold_t``/``xp_t``/``lh_t``/``dn_t``/``times`` are dense samples.
- Log entries become OpenDota's ``(key, time)`` pairs. The time is the entry's
  own ``game_time_s`` when it has one (as gem's OpenDota-shaped outputs use),
  else the match's pause-aware game clock at its tick.
- ``item_uses`` keys drop the ``item_`` prefix; ``max_hero_hit`` drops
  OpenDota's ``slot``/``player_slot`` keys.
- Ward placement logs compare counts; ward-left logs compare
  ``(time, key, attackername)``.
- Chat compares ``(text, player slot)`` of ``all``/``team`` messages.
- Teamfights compare gem's OpenDota-shaped ``opendota_teamfights``; gem's own
  fight list deliberately keeps every fight.
- Objectives get odota/core's read-time ``victim_player_slot`` on first blood
  when the reference JSON predates it (see :func:`_annotated_objectives`).
- Every other field name both sides share is compared as-is.

OpenDota does not re-parse a match it has already parsed, so a fixture's JSON
keeps the rules of the odota/parser that parsed it, and of the odota/core that
served it when it was fetched. The manifest's ``opendota_json_predates`` lists
the rule changes a fixture's JSON is older than (reported as stale), and
``opendota_known_bugs`` pins verified upstream ``odota/parser`` bug events to
strip from the reference before comparing the rest normally (see
:data:`RULE_CHANGES` and :func:`known_bugs`).

Reference: odota/parser src/main/java/opendota/CreateParsedDataBlob.java
(pinned revision in CLAUDE.md) defines the OpenDota output fields.
``scripts/validate_opendota.py`` is the online, tolerance-based check of a
smaller field set; this script is the exhaustive offline one.

Usage:
    uv run python scripts/audit_opendota_parity.py
    uv run python scripts/audit_opendota_parity.py --save-gem-json tmp/gem-json
    uv run python scripts/audit_opendota_parity.py --gem-json-dir tmp/gem-json --examples
    uv run python scripts/audit_opendota_parity.py --gem-json-dir tmp/gem-json \\
        --json-out after.json --compare before.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Callable, Iterable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch, ParsedPlayer

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "opendota"

# (gem attribute, OpenDota key) for the per-minute arrays.
_MINUTE_ARRAYS = (
    ("gold_t_min", "gold_t"),
    ("xp_t_min", "xp_t"),
    ("lh_t_min", "lh_t"),
    ("dn_t_min", "dn_t"),
    ("game_times_min", "times"),
)

# odota/parser or odota/core commit -> the audited fields its rule change touches.
RULE_CHANGES = {
    # odota/parser, August 2026: an Aegis reincarnation is no longer a death.
    "efe5794b": frozenset(
        {"match.teamfights", "player.kills_log", "player.killed", "player.killed_by"}
    ),
    # odota/core, 14 October 2026: a first purchase at exactly 0:00 is kept
    # instead of being replaced by the item's next purchase.
    "7d32aef0": frozenset({"player.first_purchase_time"}),
    # odota/parser, November 2026: Lone Druid's Spirit Bear is flagged
    # target_is_hero=True in the combat log, but killing it is not a hero kill
    # on the scoreboard and is left out of kills_log.
    "8d6ea0c2": frozenset({"player.kills_log"}),
    # odota/parser, November 2026: tower/creep-finished hero kills that the
    # scoreboard credits to an enemy hero are included in kills_log.
    "a6e8dbf3": frozenset({"player.kills_log"}),
}


@dataclass(frozen=True)
class KnownOpenDotaBug:
    """One verified upstream ``odota/parser`` bug entry in a fixture manifest."""

    bug: str
    killer: str
    victim: str
    time: int


# Known upstream odota/parser bugs that can be isolated and stripped from the
# reference JSON without exempting unrelated player data.
_MEEPO_AEGIS_BUG = "meepo-aegis-reincarnation"
KNOWN_OPENDOTA_BUGS: frozenset[str] = frozenset({_MEEPO_AEGIS_BUG})

Seconds = Callable[[int], "int | None"]
PlayerCheck = Callable[["ParsedPlayer", dict[str, Any], Seconds], tuple[Any, Any]]
MatchCheck = Callable[["ParsedMatch", dict[str, Any]], tuple[Any, Any]]


def _strip_item(key: str | None) -> str | None:
    return key[5:] if key and key.startswith("item_") else key


def _left_log(entries: Iterable[dict[str, Any]]) -> list[tuple[Any, Any, Any]]:
    return [(e.get("time"), e.get("key"), e.get("attackername")) for e in entries]


def _max_hero_hit(hit: dict[str, Any] | None) -> dict[str, Any] | None:
    if not hit:
        return None
    return {k: v for k, v in hit.items() if k not in ("slot", "player_slot")}


def _minute_array(gem_attr: str, od_key: str) -> PlayerCheck:
    return lambda p, o, t: (list(getattr(p, gem_attr)), o[od_key])


def _always(_entry: Any) -> bool:
    return True


def _entry_seconds(entry: Any, seconds: Seconds) -> int | None:
    """Return an entry's time the way gem's OpenDota-shaped outputs derive it."""
    game_time_s = getattr(entry, "game_time_s", None)
    return int(game_time_s) if game_time_s is not None else seconds(entry.tick)


def _log_check(
    log_attr: str, key: Callable[[Any], Any], keep: Callable[[Any], bool] = _always
) -> PlayerCheck:
    def check(p: ParsedPlayer, o: dict[str, Any], seconds: Seconds) -> tuple[Any, Any]:
        gem = [(key(e), _entry_seconds(e, seconds)) for e in getattr(p, log_attr) if keep(e)]
        od = [(e["key"], e["time"]) for e in o[log_attr]]
        return gem, od

    return check


#: Player fields compared after mapping gem's format onto OpenDota's. Each
#: returns ``(gem value, OpenDota value)``; every other shared field is compared
#: as-is.
PLAYER_CHECKS: dict[str, PlayerCheck] = {
    **{od: _minute_array(gem, od) for gem, od in _MINUTE_ARRAYS},
    "purchase_log": _log_check("purchase_log", lambda e: _strip_item(e.value_name)),
    "runes_log": _log_check("runes_log", lambda e: str(e.rune_type)),
    "kills_log": _log_check(
        "kills_log",
        lambda e: e.target_name,
        keep=lambda e: (
            e.target_is_hero
            and not e.target_is_illusion
            and e.target_name.startswith("npc_dota_hero_")
        ),
    ),
    "buyback_log": lambda p, o, t: (
        [_entry_seconds(e, t) for e in p.buyback_log],
        [e["time"] for e in o["buyback_log"]],
    ),
    "item_uses": lambda p, o, t: (
        {_strip_item(k): v for k, v in p.item_uses.items()},
        o["item_uses"],
    ),
    "max_hero_hit": lambda p, o, t: (p.max_hero_hit or None, _max_hero_hit(o["max_hero_hit"])),
    "obs_log": lambda p, o, t: (len(p.obs_log), len(o["obs_log"])),
    "sen_log": lambda p, o, t: (len(p.sen_log), len(o["sen_log"])),
    "obs_left_log": lambda p, o, t: (_left_log(p.obs_left_log), _left_log(o["obs_left_log"])),
    "sen_left_log": lambda p, o, t: (_left_log(p.sen_left_log), _left_log(o["sen_left_log"])),
}


def _annotated_objectives(od: dict[str, Any]) -> list[dict[str, Any]]:
    """Return OpenDota's objectives with first blood's ``victim_player_slot``.

    odota/core adds it when serving a match (svc/util/compute.ts
    ``annotateFirstbloodVictim``, read at 7b4256f), so reference JSON fetched
    before that change lacks it. It is the player_slot of ``players[key]``.
    """
    players = od.get("players") or []
    objectives = [dict(o) for o in od.get("objectives") or []]
    for objective in objectives:
        if objective.get("type") != "CHAT_MESSAGE_FIRSTBLOOD" or "victim_player_slot" in objective:
            continue
        key = str(objective.get("key", ""))
        if key.isdigit() and int(key) < len(players):
            objective["victim_player_slot"] = players[int(key)]["player_slot"]
    return objectives


def _teamfights(fights: Iterable[Any]) -> list[dict[str, Any]]:
    """Normalize teamfight dicts for OpenDota comparison.

    OpenDota's Gson serializer omits ``null`` fields, so pre-horn teamfights
    without an interval sample at ``start`` or ``end`` leave out ``xp_start``
    and ``xp_end`` rather than emitting ``null``.
    """
    normalized: list[dict[str, Any]] = []
    for fight in _plain(list(fights)):
        players = [
            {
                key: value
                for key, value in player.items()
                if not (key in ("xp_start", "xp_end") and value is None)
            }
            for player in fight.get("players", [])
        ]
        normalized.append({**fight, "players": players})
    return normalized


#: Match fields compared after mapping; every other shared field is compared as-is.
MATCH_CHECKS: dict[str, MatchCheck] = {
    "chat": lambda m, od: (
        [(c.text, c.player_slot) for c in m.chat if c.channel in ("all", "team")],
        [(c["key"], c.get("slot")) for c in od.get("chat") or [] if c.get("type") == "chat"],
    ),
    "teamfights": lambda m, od: (
        _teamfights(m.opendota_teamfights),
        _teamfights(od.get("teamfights") or []),
    ),
    "objectives": lambda m, od: (_plain(m.objectives), _annotated_objectives(od)),
}


@dataclass
class FieldResult:
    """Agreement on one field across the audited matches.

    Attributes:
        matched: Items (matches or players) where gem equals OpenDota.
        total: Items compared.
        mismatches: Match id -> number of mismatched items in that match.
        example: The first mismatch as ``(match_id, gem value, OpenDota value)``.
        stale: Match id -> number of mismatched items whose OpenDota JSON
            predates a rule change touching this field; not in ``total``.
        known_bug: Match id -> sorted list of verified OpenDota parser-bug
            event identities stripped from the reference on that match.
    """

    matched: int = 0
    total: int = 0
    mismatches: dict[str, int] = field(default_factory=dict)
    example: tuple[str, Any, Any] | None = None
    stale: dict[str, int] = field(default_factory=dict)
    known_bug: dict[str, list[str]] = field(default_factory=dict)

    def record(self, match_id: str, gem: Any, od: Any, *, stale: bool = False) -> None:
        """Count one comparison; a mismatch against a ``stale`` reference counts apart."""
        if gem != od and stale:
            self.stale[match_id] = self.stale.get(match_id, 0) + 1
            return
        self.total += 1
        if gem == od:
            self.matched += 1
            return
        self.mismatches[match_id] = self.mismatches.get(match_id, 0) + 1
        if self.example is None:
            self.example = (match_id, gem, od)


def _decrement_count(counts: dict[str, int], key: str) -> None:
    remaining = counts[key] - 1
    if remaining > 0:
        counts[key] = remaining
    else:
        del counts[key]


def _strip_meepo_aegis_reincarnation(
    od: dict[str, Any],
    bugs: Iterable[KnownOpenDotaBug],
) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """Strip only the manifest-pinned Meepo Aegis reincarnation kill from ``od``.

    odota/parser's ``handleDeathCombat`` (pinned 5018d019) calls
    ``consumeReincarnationDeath`` before its suicide check, so the first
    ``meepo_divided_we_stand`` clone self-death consumes Meepo's Aegis and the
    actual ``will_reincarnate=True`` killing blow is counted as a real kill
    (contradicting the scoreboard, HY-576). Resolves player slots from
    OpenDota's own ``hero_id`` values so gem output cannot alter the reference,
    and returns ``(od, stripped_events_by_field)``.
    """
    from gem.catalog import hero_id

    od_players = {p["player_slot"]: p for p in od.get("players") or [] if "player_slot" in p}
    hero_to_slot = {
        p["hero_id"]: p["player_slot"]
        for p in od_players.values()
        if isinstance(p.get("hero_id"), int)
    }
    if not hero_to_slot or not od_players:
        return od, {}

    copied_players: dict[int, dict[str, Any]] = {}
    adjusted: dict[str, list[str]] = {}

    for bug in bugs:
        if bug.bug != _MEEPO_AEGIS_BUG:
            continue
        killer_id = hero_id(bug.killer)
        victim_id = hero_id(bug.victim)
        killer_slot = hero_to_slot.get(killer_id) if killer_id else None
        victim_slot = hero_to_slot.get(victim_id) if victim_id else None
        if killer_slot is None or killer_slot not in od_players:
            continue
        k_od = copied_players.get(killer_slot, od_players[killer_slot])
        k_log = k_od.get("kills_log")
        if not isinstance(k_log, list):
            continue
        idx = next(
            (
                i
                for i, item in enumerate(k_log)
                if isinstance(item, dict)
                and item.get("key") == bug.victim
                and item.get("time") == bug.time
            ),
            None,
        )
        if idx is None:
            continue

        event_id = f"{bug.bug}:{bug.killer}->{bug.victim}@{bug.time}"
        new_log = [dict(k) for k in k_log]
        new_log.pop(idx)
        k_updates: dict[str, Any] = {"kills_log": new_log}
        adjusted.setdefault("player.kills_log", []).append(event_id)

        k_killed = k_od.get("killed")
        if isinstance(k_killed, dict) and k_killed.get(bug.victim, 0) > 0:
            new_killed = dict(k_killed)
            _decrement_count(new_killed, bug.victim)
            k_updates["killed"] = new_killed
            adjusted.setdefault("player.killed", []).append(event_id)
        copied_players[killer_slot] = {**k_od, **k_updates}

        if victim_slot is not None and victim_slot in od_players:
            v_od = copied_players.get(victim_slot, od_players[victim_slot])
            v_killed_by = v_od.get("killed_by")
            if isinstance(v_killed_by, dict) and v_killed_by.get(bug.killer, 0) > 0:
                new_killed_by = dict(v_killed_by)
                _decrement_count(new_killed_by, bug.killer)
                copied_players[victim_slot] = {**v_od, "killed_by": new_killed_by}
                adjusted.setdefault("player.killed_by", []).append(event_id)

    if not copied_players:
        return od, {}
    new_players = [copied_players.get(p.get("player_slot"), p) for p in od.get("players") or []]
    return {**od, "players": new_players}, adjusted


def _plain(value: Any) -> Any:
    """Convert gem values (dataclasses, defaultdicts) for comparison with JSON."""
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def od_player_slot(player_id: int) -> int:
    """Map gem's player id (0-9) to OpenDota's ``player_slot`` (0-4, 128-132)."""
    return player_id if player_id < 5 else 128 + (player_id - 5)


def audit_match(
    match_id: str,
    match: ParsedMatch,
    od: dict[str, Any],
    results: dict[str, FieldResult],
    stale_fields: frozenset[str] = frozenset(),
    known_bug_entries: Iterable[KnownOpenDotaBug] = (),
) -> None:
    """Compare one match with OpenDota, adding to ``results`` in place.

    Args:
        match_id: The match id, used to label mismatches.
        match: gem's parsed match.
        od: OpenDota's parsed match JSON.
        results: Field name -> accumulated result. Match fields are keyed
            ``match.<name>``, player fields ``player.<name>``.
        stale_fields: Fields whose rules changed after OpenDota parsed this
            match (see :func:`stale_fields`).
        known_bug_entries: Pinned upstream parser-bug entries for this match
            (see :func:`known_bugs`).
    """
    from gem.state.game_clock import game_clock_for

    clock = game_clock_for(match)

    def seconds(tick: int) -> int | None:
        return clock.game_seconds_at(tick)

    od, adjusted_bugs = _strip_meepo_aegis_reincarnation(od, known_bug_entries)

    match_fields = {f.name for f in fields(match) if not f.name.startswith("_")}
    compared = (match_fields | MATCH_CHECKS.keys()) & od.keys()
    for name in sorted(compared - {"players"}):
        check = MATCH_CHECKS.get(name)
        gem, ref = check(match, od) if check else (_plain(getattr(match, name)), od[name])
        key = f"match.{name}"
        results.setdefault(key, FieldResult()).record(match_id, gem, ref, stale=key in stale_fields)

    od_players = {p["player_slot"]: p for p in od["players"]}
    for player in match.players:
        o = od_players.get(od_player_slot(player.player_id))
        if o is None:
            continue
        player_fields = {f.name for f in fields(player) if not f.name.startswith("_")}
        for name in sorted(player_fields & o.keys() | (PLAYER_CHECKS.keys() & o.keys())):
            check_p = PLAYER_CHECKS.get(name)
            gem, ref = (
                check_p(player, o, seconds) if check_p else (_plain(getattr(player, name)), o[name])
            )
            key = f"player.{name}"
            results.setdefault(key, FieldResult()).record(
                match_id, gem, ref, stale=key in stale_fields
            )

    for key, events in adjusted_bugs.items():
        results.setdefault(key, FieldResult()).known_bug.setdefault(match_id, []).extend(events)


def fixture_ids(fixtures_dir: Path) -> list[str]:
    """Return match ids with a replay and an OpenDota JSON that OpenDota parsed.

    A match counts as parsed when its JSON carries ``radiant_gold_adv``; the
    OpenDota API leaves it null for matches it only knows from Steam.
    """
    ids = []
    for dem in sorted(fixtures_dir.glob("*.dem")):
        reference = dem.with_suffix(".opendota.json")
        if reference.exists() and json.loads(reference.read_text()).get("radiant_gold_adv"):
            ids.append(dem.stem)
    return ids


def _manifest_entry(fixtures_dir: Path, match_id: str) -> dict[str, Any]:
    manifest = fixtures_dir / "manifest.json"
    if not manifest.exists():
        return {}
    entries = json.loads(manifest.read_text())["matches"]
    return next((e for e in entries if str(e["match_id"]) == match_id), {})


def stale_fields(fixtures_dir: Path, match_id: str) -> frozenset[str]:
    """Return the fields whose rules changed after OpenDota parsed ``match_id``.

    Read from the manifest's ``opendota_json_predates``; empty when the
    directory has no manifest or the match no entry.
    """
    entry = _manifest_entry(fixtures_dir, match_id)
    return frozenset().union(
        *(RULE_CHANGES[tag] for tag in entry.get("opendota_json_predates", []))
    )


def known_bugs(fixtures_dir: Path, match_id: str) -> tuple[KnownOpenDotaBug, ...]:
    """Return pinned ``odota/parser`` bug entries annotated for ``match_id``.

    Read from the manifest's ``opendota_known_bugs``; empty when the directory
    has no manifest or the match no entry.
    """
    entry = _manifest_entry(fixtures_dir, match_id)
    bugs: list[KnownOpenDotaBug] = []
    for item in entry.get("opendota_known_bugs", []):
        if isinstance(item, dict) and item.get("bug") in KNOWN_OPENDOTA_BUGS:
            raw_time = item.get("time")
            if type(raw_time) is not int:
                raise ValueError(
                    f"Invalid known-bug time {raw_time!r} for {item.get('bug')!r} "
                    f"in match {match_id}; expected int"
                )
            bugs.append(
                KnownOpenDotaBug(
                    bug=str(item["bug"]),
                    killer=str(item["killer"]),
                    victim=str(item["victim"]),
                    time=raw_time,
                )
            )
    return tuple(bugs)


def merge_results(into: dict[str, FieldResult], part: dict[str, FieldResult]) -> None:
    """Add one match's results to the running totals in place."""
    for name, result in part.items():
        total = into.setdefault(name, FieldResult())
        total.matched += result.matched
        total.total += result.total
        total.mismatches.update(result.mismatches)
        total.stale.update(result.stale)
        for mid, events in result.known_bug.items():
            total.known_bug.setdefault(mid, []).extend(events)
        if total.example is None:
            total.example = result.example


def audit_fixture(
    match_id: str,
    fixtures_dir: Path,
    gem_json_dir: Path | None = None,
    save_gem_json: Path | None = None,
) -> dict[str, FieldResult]:
    """Load (or parse) one fixture's gem output and audit it.

    Args:
        match_id: The fixture's match id.
        fixtures_dir: Directory with ``<match_id>.dem`` and ``.opendota.json``.
        gem_json_dir: Directory of cached ``<match_id>.json`` gem output. The
            replay is parsed only when no cached file exists.
        save_gem_json: Directory to write freshly parsed gem JSON to.

    Returns:
        Field name -> result for this match.
    """
    import gem

    cached = gem_json_dir / f"{match_id}.json" if gem_json_dir else None
    if cached is not None and cached.exists():
        text = cached.read_text()
    else:
        text = gem.parse_to_json(fixtures_dir / f"{match_id}.dem")
        if save_gem_json is not None:
            save_gem_json.mkdir(parents=True, exist_ok=True)
            (save_gem_json / f"{match_id}.json").write_text(text)
    match = gem.from_dict(json.loads(text))
    od = json.loads((fixtures_dir / f"{match_id}.opendota.json").read_text())
    results: dict[str, FieldResult] = {}
    audit_match(
        match_id,
        match,
        od,
        results,
        stale_fields(fixtures_dir, match_id),
        known_bugs(fixtures_dir, match_id),
    )
    return results


def run_audit(
    match_ids: list[str],
    fixtures_dir: Path,
    *,
    gem_json_dir: Path | None = None,
    save_gem_json: Path | None = None,
    workers: int = 4,
) -> dict[str, FieldResult]:
    """Audit every match, one worker process per match at a time.

    Args:
        match_ids: Matches to audit.
        fixtures_dir: Directory with the replays and OpenDota JSON.
        gem_json_dir: Directory of cached gem JSON (see :func:`audit_fixture`).
        save_gem_json: Directory to write freshly parsed gem JSON to.
        workers: Parallel worker processes.

    Returns:
        Field name -> result across all matches, sorted by name.
    """
    results: dict[str, FieldResult] = {}
    n = len(match_ids)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        parts = pool.map(
            audit_fixture,
            match_ids,
            [fixtures_dir] * n,
            [gem_json_dir] * n,
            [save_gem_json] * n,
        )
        for part in parts:
            merge_results(results, part)
    return dict(sorted(results.items()))


def results_to_json(results: dict[str, FieldResult]) -> dict[str, Any]:
    """Return the JSON-serializable summary written by ``--json-out``."""
    return {
        name: {
            "matched": r.matched,
            "total": r.total,
            "mismatches": r.mismatches,
            "stale": r.stale,
            "known_bug": {mid: sorted(events) for mid, events in sorted(r.known_bug.items())},
        }
        for name, r in results.items()
    }


def _normalized_known_bug(raw: Any) -> Any:
    if not isinstance(raw, dict):
        return raw
    return {
        str(mid): sorted(events) if isinstance(events, list) else events
        for mid, events in raw.items()
    }


def format_report(
    results: dict[str, FieldResult],
    *,
    baseline: dict[str, Any] | None = None,
    examples: bool = False,
) -> str:
    """Format the per-field table, worst agreement first.

    Args:
        results: Field name -> result.
        baseline: A previous ``--json-out`` summary to show changes against.
        examples: Whether to show the first mismatch of each field.

    Returns:
        The report text.
    """
    lines = []
    incompatible = (
        set(incompatible_baseline_fields(results, baseline)) if baseline is not None else set()
    )
    exact = sorted(name for name, r in results.items() if r.total > 0 and r.matched == r.total)
    untested = sorted(name for name, r in results.items() if r.total == 0)
    partial = sorted(
        (item for item in results.items() if item[1].matched < item[1].total),
        key=lambda item: (item[1].matched / item[1].total, item[0]),
    )
    tally: Counter[str] = Counter()
    for name, result in partial:
        change = ""
        if baseline is not None and name in baseline and name not in incompatible:
            before = baseline[name]["matched"]
            if result.matched != before:
                change = f"  ({'+' if result.matched > before else ''}{result.matched - before})"
                tally["improved" if result.matched > before else "worse"] += 1
        spread = ", ".join(f"{mid}×{n}" for mid, n in sorted(result.mismatches.items()))
        lines.append(f"{name:36s} {result.matched:4d}/{result.total:<4d}{change}  {spread}")
        if examples and result.example is not None:
            mid, gem, od = result.example
            lines.append(f"    e.g. {mid}: gem={str(gem)[:160]}  opendota={str(od)[:160]}")
    if baseline is not None:
        for name in exact:
            before = baseline.get(name)
            if (
                before is not None
                and name not in incompatible
                and before["matched"] < results[name].matched
            ):
                tally["improved"] += 1
                lines.append(f"{name:36s} now exact (was {before['matched']}/{before['total']})")
    lines.append("")
    lines.append(f"{len(exact)} of {len(results)} fields match exactly: {', '.join(exact)}")
    if untested:
        lines.append(f"Untested (0 comparisons): {', '.join(untested)}")
    for name, result in results.items():
        if result.stale:
            matches = ", ".join(f"{mid}×{n}" for mid, n in sorted(result.stale.items()))
            lines.append(f"{name}: OpenDota JSON predates a rule change on {matches}")
        if result.known_bug:
            matches = ", ".join(
                f"{mid}×{len(events)}" for mid, events in sorted(result.known_bug.items())
            )
            lines.append(f"{name}: known OpenDota parser bug on {matches}")
    if baseline is not None:
        for name in sorted(incompatible):
            lines.append(
                f"{name:36s} incompatible baseline (re-audit baseline with the current script)"
            )
        for name in missing_fields(results, baseline):
            tally["worse"] += 1
            lines.append(
                f"{name:36s} no longer audited (was {baseline[name]['matched']}/{baseline[name]['total']})"
            )
        lines.append(f"Against the baseline: {tally['improved']} improved, {tally['worse']} worse.")
    return "\n".join(lines)


def missing_fields(results: dict[str, FieldResult], baseline: dict[str, Any]) -> list[str]:
    """Return baseline fields absent from ``results`` or whose comparison count dropped to 0."""
    return sorted(
        name
        for name in baseline
        if name not in results or (baseline[name].get("total", 0) > 0 and results[name].total == 0)
    )


def incompatible_baseline_fields(
    results: dict[str, FieldResult], baseline: dict[str, Any]
) -> list[str]:
    """Return fields whose ``known_bug`` reference normalization differs from ``baseline``."""
    return sorted(
        name
        for name, result in results.items()
        if name in baseline
        and _normalized_known_bug(result.known_bug)
        != _normalized_known_bug(baseline[name].get("known_bug") or {})
    )


def regressed(results: dict[str, FieldResult], baseline: dict[str, Any]) -> bool:
    """Return whether any field got worse, vanished, or used different normalization."""
    worse = any(
        name in baseline and r.matched < baseline[name]["matched"] for name, r in results.items()
    )
    return (
        worse
        or bool(missing_fields(results, baseline))
        or bool(incompatible_baseline_fields(results, baseline))
    )


def main(argv: list[str] | None = None) -> int:
    """Run the audit from the command line.

    Args:
        argv: Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns:
        ``0`` on success, ``1`` when no fixtures were found, or when a field got
        worse, disappeared, or used an incompatible ``--compare`` baseline.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixtures-dir", type=Path, default=DEFAULT_FIXTURES_DIR)
    parser.add_argument("--match", action="append", help="Audit only this match id (repeatable).")
    parser.add_argument("--gem-json-dir", type=Path, help="Load cached gem JSON from here.")
    parser.add_argument("--save-gem-json", type=Path, help="Write parsed gem JSON here.")
    parser.add_argument("--workers", type=int, default=4, help="Parallel worker processes.")
    parser.add_argument("--examples", action="store_true", help="Show each field's first mismatch.")
    parser.add_argument("--json-out", type=Path, help="Write the summary as JSON.")
    parser.add_argument(
        "--compare",
        type=Path,
        help="A previous --json-out over the same matches to compare against.",
    )
    args = parser.parse_args(argv)

    match_ids = args.match or fixture_ids(args.fixtures_dir)
    if not match_ids:
        print(f"No OpenDota-parsed fixtures found in {args.fixtures_dir}.", file=sys.stderr)
        return 1
    results = run_audit(
        match_ids,
        args.fixtures_dir,
        gem_json_dir=args.gem_json_dir,
        save_gem_json=args.save_gem_json,
        workers=args.workers,
    )
    baseline = json.loads(args.compare.read_text()) if args.compare else None
    print(f"Audited {len(match_ids)} matches: {', '.join(match_ids)}\n")
    print(format_report(results, baseline=baseline, examples=args.examples))
    if args.json_out is not None:
        args.json_out.write_text(json.dumps(results_to_json(results), indent=2, sort_keys=True))
    if baseline is not None:
        incompatible = incompatible_baseline_fields(results, baseline)
        if incompatible:
            print(
                "Incompatible --compare baseline: known_bug normalization differs on "
                f"{', '.join(incompatible)}. Re-audit your cached baseline with the current script.",
                file=sys.stderr,
            )
            return 1
        if regressed(results, baseline):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
