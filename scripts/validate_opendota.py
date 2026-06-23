"""Validate gem parser output against OpenDota API reference data.

For each configured replay, parses the .dem file with gem, fetches match data
from the OpenDota API, and diffs key fields: total kills, per-player net_worth,
last_hits, denies, hero deaths, tower kills, and teamfight count.

Notes on expected discrepancies
--------------------------------
OpenDota's scalar per-player stats (``kills``, ``deaths``, ``last_hits``,
``net_worth``) are sourced from the Steam API ``GetMatchDetails`` endpoint,
which records the final game-state snapshot taken by the server at game-end.
gem's ``_t`` arrays are sampled from entity state at 30-tick (≈1 s) intervals
and the ``_min`` arrays at exact 60-second game-time boundaries.  A small
residual difference is therefore expected and acceptable. ``net_worth`` is the
least stable scalar here: the replay-exposed ``m_iNetWorth`` /
``m_vecDataTeam.*.m_iNetWorth`` values can diverge slightly from Steam's final
server scalar, so the validator uses a looser tolerance for that field than it
does for kills / last hits / denies.

OpenDota data availability
--------------------------
OpenDota has two data sources:

1. **Steam API** (``GetMatchDetails``) — always available for any pub match.
   Provides end-of-game scalars: kills, deaths, assists, net_worth, last_hits,
   denies.  ``radiant_score`` / ``dire_score`` also come from here but can
   disagree with the sum of per-player kills by ±1 (known API quirk); the
   validator uses ``sum(player["kills"])`` instead.

2. **OpenDota replay parser** — only runs when someone explicitly requests a
   parse (POST ``/api/request/{match_id}`` or via the website).  Produces the
   richer derived fields: ``radiant_gold_adv``, ``radiant_xp_adv``, teamfight
   windows, ward placements, etc.  High-profile matches (e.g. TI finals) are
   auto-parsed; ordinary pub matches are not.

Consequence: for unanalysed pub replays the gold/XP advantage curve fields
return ``null`` from the API.  The validator skips those comparisons rather
than failing — this is an OpenDota data-availability limitation, not a gem
bug.  To force a parse: ``curl -X POST https://api.opendota.com/api/request/{match_id}``
then wait a few minutes and re-run.

Usage:
    uv run python scripts/validate_opendota.py
    uv run python scripts/validate_opendota.py --match 8461735141
    uv run python scripts/validate_opendota.py --verbose
    uv run python scripts/validate_opendota.py --json   # machine-readable
"""

import argparse
import json
import math
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request as urlreq
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    pass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
OPENDOTA_FIXTURES_DIR = FIXTURES_DIR / "opendota"
DEFAULT_FETCH_DIR = REPO_ROOT / "tmp" / "opendota-validation"
OPENDOTA_BASE = "https://api.opendota.com/api"
OPENDOTA_MATCHES = f"{OPENDOTA_BASE}/matches"
OPENDOTA_REQUEST = f"{OPENDOTA_BASE}/request"
MATCH_SOURCE_ENDPOINTS: dict[str, str] = {
    "public": f"{OPENDOTA_BASE}/publicMatches",
    "pro": f"{OPENDOTA_BASE}/proMatches",
}


# hero_id → npc_name, built once from gem constants
def _build_hero_id_map() -> dict[int, str]:
    from gem.constants import HEROES

    return {v["id"]: npc for npc, v in HEROES.items()}


# ---------------------------------------------------------------------------
# Configured replays: (match_id, fixture_path)
# match_id is the real 64-bit Steam match ID used for OpenDota API lookups.
# It is NOT derived from the replay — gem's match_id field truncates to 32 bits.
# ---------------------------------------------------------------------------

# Keep the default gate small and stable. Larger/edge replay fixtures are kept
# in tests/fixtures/opendota/manifest.json and can be run explicitly with --match.
REPLAYS: list[tuple[int, Path]] = [
    (8822520406, OPENDOTA_FIXTURES_DIR / "8822520406.dem"),
    (8822593932, OPENDOTA_FIXTURES_DIR / "8822593932.dem"),
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class FieldResult:
    name: str
    gem_value: object
    ref_value: object
    tolerance: float = 0.0  # relative tolerance; 0 = exact
    note: str = ""  # optional explanatory note shown in verbose mode
    skip: bool = False  # True = known limitation, exclude from pass/fail count
    ok_override: bool | None = None  # if set, overrides ok computation

    @property
    def diff(self) -> float | None:
        if self.ref_value in (None, 0):
            return None
        if isinstance(self.gem_value, (int, float)) and isinstance(self.ref_value, (int, float)):
            return abs(self.gem_value - self.ref_value) / abs(self.ref_value)
        return None

    @property
    def ok(self) -> bool:
        if self.skip:
            return True
        if self.ok_override is not None:
            return self.ok_override
        d = self.diff
        if d is None:
            return self.gem_value == self.ref_value
        return d <= self.tolerance


@dataclass
class MatchResult:
    match_id: int
    fixture: Path
    source: str = "fixtures"
    mode: str = "full"
    match_fields: list[FieldResult] = field(default_factory=list)
    player_fields: list[list[FieldResult]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def all_fields(self) -> list[FieldResult]:
        out = list(self.match_fields)
        for pf in self.player_fields:
            out.extend(pf)
        return out

    @property
    def passed(self) -> int:
        return sum(1 for f in self.all_fields if f.ok)

    @property
    def failed(self) -> int:
        return sum(1 for f in self.all_fields if not f.ok)


@dataclass
class ReplaySpec:
    match_id: int
    fixture: Path
    od: dict[str, Any] | None = None
    source: str = "fixtures"
    replay_url: str | None = None
    duration: int | None = None
    game_mode: int | None = None
    lobby_type: int | None = None
    parsed_available: bool = False


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------


def _fetch_json(url: str, *, method: str = "GET") -> Any:
    req = urlreq.Request(url, headers={"User-Agent": "gem-validator/1.0"})
    req.method = method
    with urlreq.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def fetch_opendota(match_id: int) -> dict[str, Any]:
    url = f"{OPENDOTA_MATCHES}/{match_id}"
    print(f"  Fetching {url} ...")
    return _fetch_json(url)


def request_opendota_parse(match_id: int) -> dict[str, Any]:
    url = f"{OPENDOTA_REQUEST}/{match_id}"
    print(f"  Requesting OpenDota parse: {url} ...")
    return _fetch_json(url, method="POST")


def _opendota_has_parsed_data(od: dict[str, Any]) -> bool:
    if od.get("version") not in (None, 0):
        return True
    for key in ("radiant_gold_adv", "radiant_xp_adv", "teamfights"):
        value = od.get(key)
        if value not in (None, []):
            return True
    return False


def wait_for_opendota_parse(
    match_id: int,
    *,
    timeout_s: int,
    poll_interval_s: int,
) -> dict[str, Any]:
    deadline = time.time() + timeout_s
    last = fetch_opendota(match_id)
    while time.time() <= deadline:
        if _opendota_has_parsed_data(last):
            return last
        print(
            f"  Waiting for OpenDota parse for {match_id} "
            f"({poll_interval_s}s poll interval, {int(max(deadline - time.time(), 0))}s left) ..."
        )
        time.sleep(poll_interval_s)
        last = fetch_opendota(match_id)
    return last


def fetch_match_feed(
    source: Literal["public", "pro"],
    *,
    less_than_match_id: int | None = None,
) -> list[dict[str, Any]]:
    endpoint = MATCH_SOURCE_ENDPOINTS[source]
    params: dict[str, Any] = {}
    if less_than_match_id is not None:
        params["less_than_match_id"] = less_than_match_id
    url = endpoint
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    print(f"  Fetching candidate feed: {url} ...")
    data = _fetch_json(url)
    return data if isinstance(data, list) else []


def fetch_candidate_match_ids(
    source: Literal["public", "pro"],
    *,
    pool_size: int,
) -> list[int]:
    ids: list[int] = []
    seen: set[int] = set()
    cursor: int | None = None

    while len(ids) < pool_size:
        rows = fetch_match_feed(source, less_than_match_id=cursor)
        if not rows:
            break
        page_ids = [int(row["match_id"]) for row in rows if row.get("match_id")]
        for match_id in page_ids:
            if match_id not in seen:
                ids.append(match_id)
                seen.add(match_id)
            if len(ids) >= pool_size:
                break
        last_id = page_ids[-1] if page_ids else None
        if last_id is None or last_id == cursor:
            break
        cursor = last_id

    return ids


def ensure_replay(
    match_id: int,
    out_dir: Path,
    *,
    replay_url: str | None = None,
    force: bool = False,
) -> Path:
    from gem.replays.fetch import download_and_decompress, fetch_replay_url

    out_dir.mkdir(parents=True, exist_ok=True)
    dem_path = out_dir / f"{match_id}.dem"
    if dem_path.exists() and not force:
        return dem_path
    final_url = replay_url or fetch_replay_url(match_id)
    return download_and_decompress(match_id, final_url, out_dir)


def _match_qualifies_for_sampling(
    od: dict[str, Any],
    *,
    min_duration_seconds: int,
) -> tuple[bool, str]:
    replay_url = od.get("replay_url")
    if not replay_url:
        return False, "missing replay_url"
    duration = int(od.get("duration") or 0)
    if duration < min_duration_seconds:
        return False, f"duration<{min_duration_seconds}s"
    players = od.get("players") or []
    if len(players) != 10:
        return False, "player_count!=10"
    if any(player.get("hero_id") in (None, 0) for player in players):
        return False, "missing hero_id"
    return True, ""


def sample_replays(
    *,
    source: Literal["public", "pro"],
    sample_size: int,
    seed: int,
    pool_size: int,
    min_duration_seconds: int,
    fetch_dir: Path,
) -> list[ReplaySpec]:
    if pool_size < sample_size:
        raise ValueError(f"pool_size must be >= sample_size (got {pool_size} < {sample_size})")

    candidate_ids = fetch_candidate_match_ids(source, pool_size=pool_size)
    if not candidate_ids:
        raise RuntimeError(f"No candidate match IDs returned for source={source!r}")

    rng = random.Random(seed)
    rng.shuffle(candidate_ids)

    selected: list[ReplaySpec] = []
    rejected: list[str] = []

    for match_id in candidate_ids:
        if len(selected) >= sample_size:
            break
        try:
            od = fetch_opendota(match_id)
        except Exception as exc:
            rejected.append(f"{match_id}: fetch failed ({exc})")
            continue

        ok, reason = _match_qualifies_for_sampling(od, min_duration_seconds=min_duration_seconds)
        if not ok:
            rejected.append(f"{match_id}: {reason}")
            continue

        selected.append(
            ReplaySpec(
                match_id=match_id,
                fixture=fetch_dir / f"{match_id}.dem",
                od=od,
                source=source,
                replay_url=od.get("replay_url"),
                duration=int(od.get("duration") or 0),
                game_mode=od.get("game_mode"),
                lobby_type=od.get("lobby_type"),
                parsed_available=_opendota_has_parsed_data(od),
            )
        )

    if len(selected) < sample_size:
        detail = "\n".join(f"    - {line}" for line in rejected[:15])
        raise RuntimeError(
            f"Only sampled {len(selected)} qualifying match(es) from {len(candidate_ids)} candidates "
            f"for source={source!r}; requested {sample_size}. "
            "Try --source pro or increase --pool-size when recent public matches lack replay_url.\n"
            f"{detail}"
        )

    return selected


# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------


# OpenDota player_slot → gem player_id mapping:
# slots 0-4 = Radiant (gem team=2), slots 128-132 = Dire (gem team=3)
# gem player_id = slot for Radiant, slot-128+5 for Dire
def _od_slot_to_gem_id(slot: int) -> int:
    return slot if slot < 128 else slot - 128 + 5


def _opendota_teamfights_from_combat_log(combat_log: list[Any]) -> list[dict[str, int]]:
    """Project gem combat log deaths into OpenDota-compatible teamfight windows.

    OpenDota's parser builds teamfights from combat-log game seconds, opens a
    window at ``first_death_time - 15``, closes once 15 seconds pass without a
    new hero death, then filters to windows with at least three deaths. This is
    intentionally separate from gem's richer spatial teamfight detector.
    """
    from gem.extractors.teamfights import detect_opendota_teamfights

    return [
        {
            "start": fight.start,
            "end": fight.end,
            "last_death": fight.last_death,
            "deaths": fight.deaths,
        }
        for fight in detect_opendota_teamfights(combat_log)
    ]


# ---------------------------------------------------------------------------
# Core validation
# ---------------------------------------------------------------------------

_SAMPLE_NOTE = (
    "gem samples entity state at 30-tick (≈1 s) intervals; "
    "OpenDota uses the server's final game-end snapshot. "
    "Small residual differences are expected; net worth can drift a bit more "
    "than kills / last hits because Steam final scalars and replay-exposed "
    "m_iNetWorth values are not always identical."
)

_NET_WORTH_TOLERANCE = 0.08
# Advantage and player minute curves: gem samples interval boundaries on the
# combat-log timestamp axis OpenDota uses (parser.combat_log_time_s) AND reads
# the team-data frame observed one entity tick before the boundary crossing
# (the boundary-nudge fix), matching OpenDota's effective read instant. The
# curves now coincide with OpenDota almost exactly. Observed max element-wise
# error across the five validation fixtures (tournament + ranked pub), measured
# 2026-06-18: gold_t <=0.65%, xp_t <=0.40%, gold_adv <=0.88%, xp_adv <=0.47%,
# with every advantage final matching to within 1 unit. Tolerances sit a few
# multiples above that worst case: tight enough that reverting the nudge or the
# clock/source alignment (which pushes errors back to ~10%) fails the gate,
# loose enough that an unseen fixture's sub-second end-game wiggle still passes.
_GOLD_ADV_TOLERANCE = 0.02
_GOLD_ADV_CURVE_TOLERANCE_PCT = 3.0
_XP_ADV_TOLERANCE = 0.02
_XP_ADV_CURVE_TOLERANCE_PCT = 2.5
_PLAYER_GOLD_T_CURVE_TOLERANCE_PCT = 3.0
_PLAYER_XP_T_CURVE_TOLERANCE_PCT = 3.0
_PLAYER_LH_T_ABS_TOLERANCE = 5
_PLAYER_LH_T_REL_TOLERANCE = 0.02
_PLAYER_DN_T_ABS_TOLERANCE = 2
_GOLD_ADV_NOTE = (
    "gem builds gold_adv from m_iTotalEarnedGold sampled on the combat-log "
    "timestamp axis (the same axis OpenDota uses for its interval boundaries), "
    "so the curves match OpenDota almost exactly. Any residual is sub-second "
    "end-game wiggle at the final minute boundary."
)
_PLAYER_MINUTE_ARRAY_NOTE = (
    "OpenDota player minute arrays come from its interval parser pipeline. "
    "Compare by array index; residual drift is tracked before changing parser behavior."
)
_MINUTE_SAMPLE_NOTE = (
    "This is the last whole-minute snapshot before game end, compared against "
    "a final server scalar. It is informational only and is excluded from "
    "pass/fail counts because up to 59 seconds of gameplay can elapse after "
    "the final minute boundary."
)


def _max_curve_error_pct(gem_values: list[int], ref_values: list[int]) -> float:
    """Return max element-wise absolute error as percent of max reference magnitude."""
    max_abs_ref = max(abs(value) for value in ref_values) or 1
    max_abs_error = max(abs(gem - ref) for gem, ref in zip(gem_values, ref_values, strict=True))
    return round(max_abs_error / max_abs_ref * 100, 2)


def _max_abs_error(gem_values: list[int], ref_values: list[int]) -> int:
    """Return max element-wise absolute error for same-length integer arrays."""
    return max(abs(gem - ref) for gem, ref in zip(gem_values, ref_values, strict=True))


def _allowed_abs_error(
    ref_values: list[int],
    absolute_floor: int,
    relative_tolerance: float | None,
) -> int:
    """Return absolute counter tolerance, optionally scaled by reference size."""
    if relative_tolerance is None or not ref_values:
        return absolute_floor
    max_abs_ref = max(abs(value) for value in ref_values)
    return max(absolute_floor, math.ceil(max_abs_ref * relative_tolerance))


def _compare_opendota_player_array(
    label: str,
    name: str,
    gem_values: list[int],
    ref_values: list[int],
    *,
    max_curve_error_pct: float | None = None,
    max_abs_error: int | None = None,
    max_abs_error_pct: float | None = None,
) -> list[FieldResult]:
    """Compare one gem player minute array against one OpenDota player array."""
    missing_ref = not ref_values
    missing_note = f"OpenDota did not expose player {name} for this match."
    note = missing_note if missing_ref else _PLAYER_MINUTE_ARRAY_NOTE
    fields = [
        FieldResult(
            f"{label}/{name}/length",
            len(gem_values),
            len(ref_values),
            skip=missing_ref,
            note=note if missing_ref else "",
        )
    ]

    gem_final = gem_values[-1] if gem_values else None
    ref_final = ref_values[-1] if ref_values else None
    if max_curve_error_pct is not None:
        fields.append(
            FieldResult(
                f"{label}/{name}/final",
                gem_final,
                ref_final,
                tolerance=max_curve_error_pct / 100,
                skip=missing_ref,
                note=note,
            )
        )
        if gem_values and ref_values and len(gem_values) == len(ref_values):
            err_pct = _max_curve_error_pct(gem_values, ref_values)
            fields.append(
                FieldResult(
                    f"{label}/{name}/max_curve_err%",
                    err_pct,
                    max_curve_error_pct,
                    ok_override=err_pct <= max_curve_error_pct,
                    note=note,
                )
            )
        elif missing_ref:
            fields.append(
                FieldResult(
                    f"{label}/{name}/max_curve_err%",
                    None,
                    max_curve_error_pct,
                    skip=True,
                    note=note,
                )
            )
        return fields

    if max_abs_error is None:
        raise ValueError("Either max_curve_error_pct or max_abs_error must be provided")

    allowed_abs_error = _allowed_abs_error(ref_values, max_abs_error, max_abs_error_pct)
    final_abs_error = (
        abs(gem_final - ref_final)
        if isinstance(gem_final, int) and isinstance(ref_final, int)
        else None
    )
    fields.append(
        FieldResult(
            f"{label}/{name}/final_abs_err",
            final_abs_error,
            allowed_abs_error,
            skip=missing_ref,
            ok_override=final_abs_error is not None and final_abs_error <= allowed_abs_error,
            note=note,
        )
    )
    if gem_values and ref_values and len(gem_values) == len(ref_values):
        err = _max_abs_error(gem_values, ref_values)
        fields.append(
            FieldResult(
                f"{label}/{name}/max_abs_err",
                err,
                allowed_abs_error,
                ok_override=err <= allowed_abs_error,
                note=note,
            )
        )
    elif missing_ref:
        fields.append(
            FieldResult(
                f"{label}/{name}/max_abs_err",
                None,
                allowed_abs_error,
                skip=True,
                note=note,
            )
        )
    return fields


def validate_match(
    match_id: int,
    fixture: Path,
    *,
    od: dict[str, Any] | None = None,
    source: str = "fixtures",
    mode: Literal["scalar", "parsed", "full"] = "full",
) -> MatchResult:
    result = MatchResult(match_id=match_id, fixture=fixture, source=source, mode=mode)

    if not fixture.exists():
        result.errors.append(f"Fixture not found: {fixture}")
        return result

    # --- Parse with gem ---
    print(f"  Parsing {fixture.name} ...")
    try:
        import gem

        m = gem.parse(str(fixture))
    except Exception as exc:
        result.errors.append(f"gem.parse failed: {exc}")
        return result

    # --- Fetch OpenDota ---
    if od is None:
        try:
            od = fetch_opendota(match_id)
        except Exception as exc:
            result.errors.append(f"OpenDota fetch failed: {exc}")
            return result

    hero_id_map = _build_hero_id_map()

    # -----------------------------------------------------------------------
    # Match-level fields
    # -----------------------------------------------------------------------

    # Use sum of per-player kills rather than radiant_score+dire_score — OpenDota's
    # team scores can disagree with their own per-player kills by ±1 (known API quirk).
    od_total_kills = sum(p["kills"] for p in od["players"])
    gem_total_kills = sum(p.kills for p in m.players)
    result.match_fields.append(FieldResult("total_kills", gem_total_kills, od_total_kills))

    # radiant_win is None for HLTV/tournament replays where CDemoFileInfo,
    # entity state, and combat log all omit the winner. Mark as SKIP rather
    # than FAIL — this is a known replay format limitation, not a parser bug.
    result.match_fields.append(
        FieldResult(
            "radiant_win",
            m.radiant_win,
            od["radiant_win"],
            skip=m.radiant_win is None,
            note="HLTV replays omit game_winner in CDemoFileInfo and entity state.",
        )
    )

    gem_tower_kills = len(m.towers)
    od_rad_status = od.get("tower_status_radiant", 0x7FF)
    od_dir_status = od.get("tower_status_dire", 0x7FF)
    od_tower_kills = bin(0x7FF ^ od_rad_status).count("1") + bin(0x7FF ^ od_dir_status).count("1")
    result.match_fields.append(FieldResult("tower_kills", gem_tower_kills, od_tower_kills))

    if mode in {"parsed", "full"}:
        # Teamfight detection — compare against an OpenDota-compatible projection
        # built from combat-log game time. gem's public teamfight objects keep
        # raw ticks and include extra spatial clustering, so they are not the
        # right comparison surface for OpenDota's filtered parser output.
        od_teamfights = od.get("teamfights") or []
        gem_teamfights = _opendota_teamfights_from_combat_log(m.combat_log or [])
        MATCH_WINDOW_S = 30  # ±30 s is sufficient for timing alignment

        result.match_fields.append(
            FieldResult(
                "teamfights/total_count",
                len(gem_teamfights),
                len(od_teamfights),
                skip=True,  # death annotation details can still differ by parser pipeline
                note=(
                    "OpenDota applies deaths>=3 filtering over its expanded event pipeline. "
                    "Count comparison is informational only."
                ),
            )
        )

        for i, od_tf in enumerate(od_teamfights):
            od_start_s = od_tf.get("start", 0)
            # Find nearest gem fight by start time
            best_gem = None
            best_delta = float("inf")
            for tf in gem_teamfights:
                delta = abs(tf["start"] - od_start_s)
                if delta < best_delta:
                    best_delta = delta
                    best_gem = tf

            gem_start_s = best_gem["start"] if best_gem else None

            result.match_fields.append(
                FieldResult(
                    f"teamfights[{i}]/start_s(nearest)",
                    gem_start_s,
                    od_start_s,
                    ok_override=best_delta <= MATCH_WINDOW_S,
                    note=(
                        f"Nearest gem fight matched within {best_delta}s. "
                        "OpenDota end may differ due to additional death annotations."
                    ),
                )
            )

    if mode in {"parsed", "full"}:
        # radiant_gold_adv / radiant_xp_adv — per-minute curves
        # Compare array length and last value (full curve comparison via max element-wise diff)
        od_gold_adv = od.get("radiant_gold_adv") or []
        od_xp_adv = od.get("radiant_xp_adv") or []
        gem_gold_adv = m.radiant_gold_adv or []
        gem_xp_adv = m.radiant_xp_adv or []

        od_adv_missing = not od_gold_adv and not od_xp_adv
        result.match_fields.append(
            FieldResult(
                "radiant_gold_adv/length",
                len(gem_gold_adv),
                len(od_gold_adv),
                skip=od_adv_missing,
                note="OpenDota did not compute gold/XP advantage curves for this match."
                if od_adv_missing
                else "",
            )
        )
        result.match_fields.append(
            FieldResult(
                "radiant_xp_adv/length",
                len(gem_xp_adv),
                len(od_xp_adv),
                skip=od_adv_missing,
                note="OpenDota did not compute gold/XP advantage curves for this match."
                if od_adv_missing
                else "",
            )
        )

        # Final value comparison (last minute — most meaningful single scalar)
        gem_gold_final = gem_gold_adv[-1] if gem_gold_adv else None
        od_gold_final = od_gold_adv[-1] if od_gold_adv else None
        result.match_fields.append(
            FieldResult(
                "radiant_gold_adv/final",
                gem_gold_final,
                od_gold_final,
                tolerance=_GOLD_ADV_TOLERANCE,
                skip=od_adv_missing,
                note="OpenDota did not compute gold/XP advantage curves for this match."
                if od_adv_missing
                else _GOLD_ADV_NOTE,
            )
        )
        gem_xp_final = gem_xp_adv[-1] if gem_xp_adv else None
        od_xp_final = od_xp_adv[-1] if od_xp_adv else None
        result.match_fields.append(
            FieldResult(
                "radiant_xp_adv/final",
                gem_xp_final,
                od_xp_final,
                tolerance=_XP_ADV_TOLERANCE,
                skip=od_adv_missing,
                note="OpenDota did not compute gold/XP advantage curves for this match."
                if od_adv_missing
                else "",
            )
        )

        # Max element-wise relative error across the curve (gem=actual %, ref=5% threshold).
        if gem_gold_adv and od_gold_adv and len(gem_gold_adv) == len(od_gold_adv):
            max_abs = max(abs(v) for v in od_gold_adv) or 1
            err_pct = round(
                max(abs(g - o) for g, o in zip(gem_gold_adv, od_gold_adv, strict=True))
                / max_abs
                * 100,
                2,
            )
            result.match_fields.append(
                FieldResult(
                    "radiant_gold_adv/max_curve_err%",
                    err_pct,
                    _GOLD_ADV_CURVE_TOLERANCE_PCT,
                    ok_override=err_pct <= _GOLD_ADV_CURVE_TOLERANCE_PCT,
                    note=_GOLD_ADV_NOTE,
                )
            )
        if gem_xp_adv and od_xp_adv and len(gem_xp_adv) == len(od_xp_adv):
            max_abs = max(abs(v) for v in od_xp_adv) or 1
            err_pct = round(
                max(abs(g - o) for g, o in zip(gem_xp_adv, od_xp_adv, strict=True)) / max_abs * 100,
                2,
            )
            result.match_fields.append(
                FieldResult(
                    "radiant_xp_adv/max_curve_err%",
                    err_pct,
                    _XP_ADV_CURVE_TOLERANCE_PCT,
                    ok_override=err_pct <= _XP_ADV_CURVE_TOLERANCE_PCT,
                )
            )

    # -----------------------------------------------------------------------
    # Player-level fields
    # -----------------------------------------------------------------------

    gem_by_hero = {p.hero_name: p for p in m.players}

    for od_player in od["players"]:
        od_slot = od_player["player_slot"]
        od_hero_id = od_player["hero_id"]
        od_hero_npc = hero_id_map.get(od_hero_id)
        gem_id = _od_slot_to_gem_id(od_slot)

        gp = gem_by_hero.get(od_hero_npc) if od_hero_npc else None
        if gp is None:
            gp = next((p for p in m.players if p.player_id == gem_id), None)

        label = od_hero_npc or f"hero_id={od_hero_id}"
        fields: list[FieldResult] = []

        if gp is None:
            fields.append(FieldResult(f"{label}/found", False, True))
            result.player_fields.append(fields)
            continue

        # --- 30-tick sampler (last sample, ≈1 s resolution) ---
        gem_nw = gp.net_worth_t[-1] if gp.net_worth_t else None
        fields.append(
            FieldResult(
                f"{label}/net_worth[30t]",
                gem_nw,
                od_player["net_worth"],
                tolerance=_NET_WORTH_TOLERANCE,
                note=_SAMPLE_NOTE,
            )
        )
        gem_lh = gp.lh_t[-1] if gp.lh_t else None
        fields.append(
            FieldResult(
                f"{label}/last_hits[30t]",
                gem_lh,
                od_player["last_hits"],
                tolerance=0.01,
                note=_SAMPLE_NOTE,
            )
        )
        gem_dn = gp.dn_t[-1] if gp.dn_t else None
        fields.append(FieldResult(f"{label}/denies[30t]", gem_dn, od_player["denies"]))

        # --- per-minute sampler (last whole-minute snapshot, OpenDota-aligned) ---
        gem_nw_min = gp.net_worth_t_min[-1] if gp.net_worth_t_min else None
        fields.append(
            FieldResult(
                f"{label}/net_worth[min]",
                gem_nw_min,
                od_player["net_worth"],
                tolerance=_NET_WORTH_TOLERANCE,
                note=_MINUTE_SAMPLE_NOTE,
                skip=True,
            )
        )
        gem_lh_min = gp.lh_t_min[-1] if gp.lh_t_min else None
        fields.append(
            FieldResult(
                f"{label}/last_hits[min]",
                gem_lh_min,
                od_player["last_hits"],
                tolerance=0.01,
                note=_MINUTE_SAMPLE_NOTE,
                skip=True,
            )
        )
        gem_dn_min = gp.dn_t_min[-1] if gp.dn_t_min else None
        fields.append(
            FieldResult(
                f"{label}/denies[min]",
                gem_dn_min,
                od_player["denies"],
                note=_MINUTE_SAMPLE_NOTE,
                skip=True,
            )
        )

        if mode in {"parsed", "full"}:
            fields.extend(
                _compare_opendota_player_array(
                    label,
                    "gold_t",
                    list(gp.gold_t_min),
                    list(od_player.get("gold_t") or []),
                    max_curve_error_pct=_PLAYER_GOLD_T_CURVE_TOLERANCE_PCT,
                )
            )
            fields.extend(
                _compare_opendota_player_array(
                    label,
                    "xp_t",
                    list(gp.xp_t_min),
                    list(od_player.get("xp_t") or []),
                    max_curve_error_pct=_PLAYER_XP_T_CURVE_TOLERANCE_PCT,
                )
            )
            fields.extend(
                _compare_opendota_player_array(
                    label,
                    "lh_t",
                    list(gp.lh_t_min),
                    list(od_player.get("lh_t") or []),
                    max_abs_error=_PLAYER_LH_T_ABS_TOLERANCE,
                    max_abs_error_pct=_PLAYER_LH_T_REL_TOLERANCE,
                )
            )
            fields.extend(
                _compare_opendota_player_array(
                    label,
                    "dn_t",
                    list(gp.dn_t_min),
                    list(od_player.get("dn_t") or []),
                    max_abs_error=_PLAYER_DN_T_ABS_TOLERANCE,
                )
            )

        # kills / deaths from server scoreboard (CDOTAPlayerResource)
        fields.append(FieldResult(f"{label}/kills", gp.kills, od_player["kills"]))
        fields.append(FieldResult(f"{label}/deaths", gp.deaths, od_player["deaths"]))

        result.player_fields.append(fields)

    return result


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _diff_str(f: FieldResult) -> str:
    d = f.diff
    if d is None:
        return ""
    return f"{d * 100:+.1f}%"


def _status_style(f: FieldResult) -> tuple[str, str]:
    """Return (status_text, rich_style) for a field result."""
    if f.skip:
        return ("SKIP", "yellow")
    return ("OK", "green") if f.ok else ("FAIL", "bold red")


def print_result(r: MatchResult, verbose: bool = False) -> None:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()

    title = (
        f"Match [bold cyan]{r.match_id}[/]  "
        f"[[dim]{r.fixture.name}[/]]  "
        f"[dim](source={r.source}, mode={r.mode})[/]"
    )
    console.print()

    if r.errors:
        for e in r.errors:
            console.print(f"  [bold red]ERROR:[/] {e}")
        console.print(Panel(title, style="red"))
        return

    console.print(Panel(title, style="cyan"))

    # --- Match-level table ---
    mtable = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold")
    mtable.add_column("Field", style="dim")
    mtable.add_column("gem", justify="right")
    mtable.add_column("ref", justify="right")
    mtable.add_column("diff", justify="right")
    mtable.add_column("status", justify="center")

    for f in r.match_fields:
        status_text, style = _status_style(f)
        mtable.add_row(
            f.name,
            str(f.gem_value),
            str(f.ref_value),
            _diff_str(f),
            f"[{style}]{status_text}[/]",
        )

    console.print("[bold]Match-level[/]")
    console.print(mtable)

    # --- Per-player table ---
    failures = [f for pf in r.player_fields for f in pf if not f.ok]
    shown_fields = [f for pf in r.player_fields for f in pf] if verbose else failures

    if shown_fields:
        ptable = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold")
        ptable.add_column("Field", style="dim", no_wrap=False)
        ptable.add_column("gem", justify="right")
        ptable.add_column("ref", justify="right")
        ptable.add_column("diff", justify="right")
        ptable.add_column("status", justify="center")

        for f in shown_fields:
            status_text, style = _status_style(f)
            ptable.add_row(
                f.name,
                str(f.gem_value),
                str(f.ref_value),
                _diff_str(f),
                f"[{style}]{status_text}[/]",
            )

        console.print(
            "[bold]Per-player[/]"
            + ("" if verbose else " [dim](failures only — use --verbose for all)[/]")
        )
        console.print(ptable)

        if failures and verbose:
            console.print(f"  [dim]{_SAMPLE_NOTE}[/]")
    else:
        console.print("[bold]Per-player[/]")
        console.print("  [green]All player fields OK[/] [dim](use --verbose to show all)[/]")

    style = "green" if r.failed == 0 else "bold red"
    console.print(f"  Result: [{style}]{r.passed} passed, {r.failed} failed[/]\n")


def results_to_jsonable(results: list[MatchResult]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for r in results:
        out.append(
            {
                "match_id": r.match_id,
                "fixture": str(r.fixture),
                "source": r.source,
                "mode": r.mode,
                "errors": r.errors,
                "passed": r.passed,
                "failed": r.failed,
                "fields": [
                    {
                        "name": f.name,
                        "gem": f.gem_value,
                        "ref": f.ref_value,
                        "ok": f.ok,
                        "diff_pct": round(f.diff * 100, 2) if f.diff is not None else None,
                        "note": f.note or None,
                    }
                    for f in r.all_fields
                ],
            }
        )
    return out


def print_json(results: list[MatchResult]) -> None:
    print(json.dumps(results_to_jsonable(results), indent=2))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_manifest(
    specs: list[ReplaySpec],
    *,
    source: str,
    mode: str,
    seed: int | None,
    request_parse_enabled: bool,
) -> dict[str, Any]:
    return {
        "source": source,
        "mode": mode,
        "seed": seed,
        "request_parse": request_parse_enabled,
        "count": len(specs),
        "matches": [
            {
                "match_id": spec.match_id,
                "fixture": str(spec.fixture),
                "source": spec.source,
                "duration": spec.duration,
                "game_mode": spec.game_mode,
                "lobby_type": spec.lobby_type,
                "replay_url": spec.replay_url,
                "parsed_available": spec.parsed_available,
            }
            for spec in specs
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def resolve_replay_specs(args: argparse.Namespace) -> list[ReplaySpec]:
    if args.sample:
        fetch_dir = args.fetch_dir or DEFAULT_FETCH_DIR
        return sample_replays(
            source=args.source,
            sample_size=args.sample,
            seed=args.seed,
            pool_size=args.pool_size,
            min_duration_seconds=args.min_duration_seconds,
            fetch_dir=fetch_dir,
        )

    if args.match:
        known = dict(REPLAYS)
        fixture = known.get(args.match, OPENDOTA_FIXTURES_DIR / f"{args.match}.dem")
        return [ReplaySpec(match_id=args.match, fixture=fixture, source="match")]

    return [
        ReplaySpec(match_id=match_id, fixture=fixture, source="fixtures")
        for match_id, fixture in REPLAYS
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate gem output against OpenDota API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:")[1] if "Usage:" in __doc__ else "",
    )
    parser.add_argument("--match", type=int, help="Validate a single match ID.")
    parser.add_argument(
        "--mode",
        choices=("scalar", "parsed", "full"),
        default="full",
        help=(
            "Validation mode: scalar=end-state scoreboard parity only; "
            "parsed=scalar plus OpenDota replay-parser fields; full=current alias for parsed."
        ),
    )
    parser.add_argument(
        "--source",
        choices=("public", "pro"),
        default="pro",
        help="Random sampling source for --sample (default: pro).",
    )
    parser.add_argument(
        "--sample",
        type=int,
        help="Randomly sample N match IDs from OpenDota feeds and validate them.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Deterministic RNG seed used for --sample (default: 42).",
    )
    parser.add_argument(
        "--pool-size",
        type=int,
        default=200,
        help="Candidate pool size to pull from OpenDota before random sampling (default: 200).",
    )
    parser.add_argument(
        "--min-duration-seconds",
        type=int,
        default=900,
        help="Minimum match duration for sampled matches (default: 900).",
    )
    parser.add_argument(
        "--fetch-dir",
        type=Path,
        default=None,
        help=(
            "Directory for downloaded sampled replays. "
            f"Defaults to {DEFAULT_FETCH_DIR} when --sample is used."
        ),
    )
    parser.add_argument(
        "--force-fetch",
        action="store_true",
        help="Re-download sampled/missing replays even if the .dem file already exists.",
    )
    parser.add_argument(
        "--fetch-missing",
        action="store_true",
        help="For --match or fixture validation, download the replay if the local .dem is missing.",
    )
    parser.add_argument(
        "--request-parse",
        action="store_true",
        help=(
            "If OpenDota replay-parser fields are missing in parsed/full mode, "
            "POST /request/{match_id} and poll for completion."
        ),
    )
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=0,
        help="Maximum seconds to poll after --request-parse (default: 0 = do not wait).",
    )
    parser.add_argument(
        "--poll-interval-seconds",
        type=int,
        default=30,
        help="Polling interval used with --request-parse (default: 30).",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON.")
    parser.add_argument(
        "--out",
        type=Path,
        help="Write JSON validation results to this path.",
    )
    parser.add_argument(
        "--manifest-out",
        type=Path,
        help="Write sampled match metadata to this path.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show all fields, not just failures."
    )
    args = parser.parse_args()

    if args.sample and args.match:
        parser.error("--sample cannot be combined with --match")
    if args.sample and args.pool_size < args.sample:
        parser.error("--pool-size must be >= --sample")
    if args.request_parse and args.mode == "scalar":
        parser.error("--request-parse only makes sense in parsed/full mode")

    specs = resolve_replay_specs(args)
    if args.manifest_out:
        write_json(
            args.manifest_out,
            build_manifest(
                specs,
                source=args.source if args.sample else "fixtures",
                mode=args.mode,
                seed=args.seed if args.sample else None,
                request_parse_enabled=args.request_parse,
            ),
        )

    results = []
    for spec in specs:
        print(f"\nValidating match {spec.match_id} ...")

        od = spec.od
        if od is None:
            try:
                od = fetch_opendota(spec.match_id)
            except Exception as exc:
                results.append(
                    MatchResult(
                        match_id=spec.match_id,
                        fixture=spec.fixture,
                        source=spec.source,
                        mode=args.mode,
                        errors=[f"OpenDota fetch failed: {exc}"],
                    )
                )
                continue

        spec.replay_url = od.get("replay_url") or spec.replay_url
        spec.duration = int(od.get("duration") or 0) if spec.duration is None else spec.duration
        spec.game_mode = od.get("game_mode") if spec.game_mode is None else spec.game_mode
        spec.lobby_type = od.get("lobby_type") if spec.lobby_type is None else spec.lobby_type
        spec.parsed_available = _opendota_has_parsed_data(od)

        if args.mode in {"parsed", "full"} and not spec.parsed_available and args.request_parse:
            try:
                request_opendota_parse(spec.match_id)
                if args.wait_seconds > 0:
                    od = wait_for_opendota_parse(
                        spec.match_id,
                        timeout_s=args.wait_seconds,
                        poll_interval_s=args.poll_interval_seconds,
                    )
                    spec.parsed_available = _opendota_has_parsed_data(od)
            except Exception as exc:
                print(f"  Parse request/poll failed for {spec.match_id}: {exc}")

        should_fetch = args.sample or (
            not spec.fixture.exists() and (args.fetch_missing or args.force_fetch)
        )

        if should_fetch:
            try:
                fetch_dir = args.fetch_dir or DEFAULT_FETCH_DIR
                spec.fixture = ensure_replay(
                    spec.match_id,
                    fetch_dir,
                    replay_url=spec.replay_url,
                    force=args.force_fetch,
                )
            except Exception as exc:
                results.append(
                    MatchResult(
                        match_id=spec.match_id,
                        fixture=spec.fixture,
                        source=spec.source,
                        mode=args.mode,
                        errors=[f"Replay fetch failed: {exc}"],
                    )
                )
                continue

        r = validate_match(
            spec.match_id,
            spec.fixture,
            od=od,
            source=spec.source,
            mode=args.mode,
        )
        results.append(r)

    if args.out:
        write_json(args.out, results_to_jsonable(results))

    if args.json:
        print_json(results)
    else:
        from rich.console import Console
        from rich.rule import Rule

        console = Console()
        for r in results:
            print_result(r, verbose=args.verbose)

        total_failed = sum(r.failed for r in results)
        total_errors = sum(len(r.errors) for r in results)
        console.print(Rule())
        style = "green" if total_failed == 0 and total_errors == 0 else "bold red"
        console.print(
            f"[{style}]Summary: {len(results)} match(es), "
            f"{total_failed} field failures, {total_errors} errors[/]"
        )

    total_failed = sum(r.failed for r in results)
    total_errors = sum(len(r.errors) for r in results)
    if total_failed > 0 or total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
