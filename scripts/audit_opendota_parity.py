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
- Chat compares ``(text, player slot)`` of ``all``/``team`` messages;
  teamfights compare the count only.
- Every other field name both sides share is compared as-is.

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
        keep=lambda e: e.target_is_hero and not e.target_is_illusion,
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

#: Match fields compared after mapping; every other shared field is compared as-is.
MATCH_CHECKS: dict[str, MatchCheck] = {
    "chat": lambda m, od: (
        [(c.text, c.player_slot) for c in m.chat if c.channel in ("all", "team")],
        [(c["key"], c.get("slot")) for c in od.get("chat") or [] if c.get("type") == "chat"],
    ),
    "teamfights": lambda m, od: (len(m.teamfights), len(od.get("teamfights") or [])),
}


@dataclass
class FieldResult:
    """Agreement on one field across the audited matches.

    Attributes:
        matched: Items (matches or players) where gem equals OpenDota.
        total: Items compared.
        mismatches: Match id -> number of mismatched items in that match.
        example: The first mismatch as ``(match_id, gem value, OpenDota value)``.
    """

    matched: int = 0
    total: int = 0
    mismatches: dict[str, int] = field(default_factory=dict)
    example: tuple[str, Any, Any] | None = None

    def record(self, match_id: str, gem: Any, od: Any) -> None:
        """Count one comparison."""
        self.total += 1
        if gem == od:
            self.matched += 1
            return
        self.mismatches[match_id] = self.mismatches.get(match_id, 0) + 1
        if self.example is None:
            self.example = (match_id, gem, od)


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
) -> None:
    """Compare one match with OpenDota, adding to ``results`` in place.

    Args:
        match_id: The match id, used to label mismatches.
        match: gem's parsed match.
        od: OpenDota's parsed match JSON.
        results: Field name -> accumulated result. Match fields are keyed
            ``match.<name>``, player fields ``player.<name>``.
    """
    from gem.state.game_clock import game_clock_for

    clock = game_clock_for(match)

    def seconds(tick: int) -> int | None:
        return clock.game_seconds_at(tick)

    match_fields = {f.name for f in fields(match) if not f.name.startswith("_")}
    for name in sorted((match_fields & od.keys()) - {"players"}):
        check = MATCH_CHECKS.get(name)
        gem, ref = check(match, od) if check else (_plain(getattr(match, name)), od[name])
        results.setdefault(f"match.{name}", FieldResult()).record(match_id, gem, ref)

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
            results.setdefault(f"player.{name}", FieldResult()).record(match_id, gem, ref)


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


def merge_results(into: dict[str, FieldResult], part: dict[str, FieldResult]) -> None:
    """Add one match's results to the running totals in place."""
    for name, result in part.items():
        total = into.setdefault(name, FieldResult())
        total.matched += result.matched
        total.total += result.total
        total.mismatches.update(result.mismatches)
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
    audit_match(match_id, match, od, results)
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
        name: {"matched": r.matched, "total": r.total, "mismatches": r.mismatches}
        for name, r in results.items()
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
    exact = sorted(name for name, r in results.items() if r.matched == r.total)
    partial = sorted(
        (item for item in results.items() if item[1].matched < item[1].total),
        key=lambda item: (item[1].matched / item[1].total, item[0]),
    )
    tally: Counter[str] = Counter()
    for name, result in partial:
        change = ""
        if baseline is not None and name in baseline:
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
            if before is not None and before["matched"] < results[name].matched:
                tally["improved"] += 1
                lines.append(f"{name:36s} now exact (was {before['matched']}/{before['total']})")
    lines.append("")
    lines.append(f"{len(exact)} of {len(results)} fields match exactly: {', '.join(exact)}")
    if baseline is not None:
        for name in missing_fields(results, baseline):
            tally["worse"] += 1
            lines.append(
                f"{name:36s} no longer audited (was {baseline[name]['matched']}/{baseline[name]['total']})"
            )
        lines.append(f"Against the baseline: {tally['improved']} improved, {tally['worse']} worse.")
    return "\n".join(lines)


def missing_fields(results: dict[str, FieldResult], baseline: dict[str, Any]) -> list[str]:
    """Return baseline fields absent from ``results``, e.g. a removed or renamed field."""
    return sorted(baseline.keys() - results.keys())


def regressed(results: dict[str, FieldResult], baseline: dict[str, Any]) -> bool:
    """Return whether any field matches less often than in ``baseline`` or vanished."""
    worse = any(
        name in baseline and r.matched < baseline[name]["matched"] for name, r in results.items()
    )
    return worse or bool(missing_fields(results, baseline))


def main(argv: list[str] | None = None) -> int:
    """Run the audit from the command line.

    Args:
        argv: Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns:
        ``0`` on success, ``1`` when no fixtures were found, or when a field got
        worse or disappeared against ``--compare``.
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
    if baseline is not None and regressed(results, baseline):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
