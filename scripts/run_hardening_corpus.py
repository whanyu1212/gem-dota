"""Run pre-release hardening sweeps against a GCS or local Dota 2 replay corpus.

For every selected match, parses the replay once and verifies:
1. ``gem.parse()`` succeeds without unhandled errors, recording wall time and peak RSS.
2. Core structural invariants hold (players, non-negative counters, monotonic clocks).
3. Public API surfaces succeed: ``to_json``/``from_dict`` round-trip, ``analyze()``,
   and ``to_parquet``/``read_parquet_table`` with all optional table groups.
4. OpenDota field-by-field parity via :mod:`scripts.audit_opendota_parity` for
   parity-eligible matches (excluding ``smoke-only`` entries such as Turbo by default).

Optionally runs a ``parse_many_to_parquet`` batch check, compares parity against a
baseline ``parity.json`` (local path or ``gs://`` URI), and uploads run artifacts
to ``gs://<bucket>/runs/<timestamp>-<git-sha>/``.

Examples:
    export GEM_CORPUS_BUCKET=gs://my-gem-hardening
    uv run python scripts/run_hardening_corpus.py --workers 4 --upload-run
    uv run python scripts/run_hardening_corpus.py --tag ranked --examples
    uv run python scripts/run_hardening_corpus.py --compare gs://my-gem-hardening/runs/<prev>/parity.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import subprocess
import sys
import tempfile
import time
import traceback
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
for _path in (SCRIPTS_DIR, REPO_ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import audit_opendota_parity as audit  # noqa: E402
from _hardening_gcs import (  # noqa: E402
    DEFAULT_CACHE_DIR,
    CorpusEntry,
    CorpusIndex,
    GcsClient,
    GcsError,
    file_sha256,
    join_gcs_uri,
    load_corpus_index_from_gcs,
    resolve_bucket,
)

from gem.replays.fetch import _decompress_replay  # noqa: E402

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

ALL_DATAFRAME_INCLUDES: tuple[str, ...] = ("analysis", "opendota", "gold_ledger")


@dataclass(slots=True)
class MatchRunOutcome:
    """Outcome of running all hardening checks on a single corpus match."""

    match_id: int
    source: str
    tags: tuple[str, ...]
    ok: bool
    parse_seconds: float
    total_seconds: float
    peak_rss_mb: float
    parity_audited: bool
    invariants: list[str] = field(default_factory=list)
    stage_errors: dict[str, str] = field(default_factory=dict)
    parity_results: dict[str, audit.FieldResult] = field(default_factory=dict)

    def to_summary_dict(self) -> dict[str, Any]:
        """Serialize per-match telemetry and errors for ``summary.json``."""
        return {
            "match_id": self.match_id,
            "source": self.source,
            "tags": list(self.tags),
            "ok": self.ok,
            "parse_seconds": round(self.parse_seconds, 3),
            "total_seconds": round(self.total_seconds, 3),
            "peak_rss_mb": round(self.peak_rss_mb, 1),
            "parity_audited": self.parity_audited,
            "invariants": list(self.invariants),
            "stage_errors": dict(self.stage_errors),
        }


def _current_peak_rss_mb() -> float:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes; Linux reports KiB.
    if sys.platform == "darwin":
        return rss / (1024 * 1024)
    return rss / 1024


def _git_short_sha() -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        sha = proc.stdout.strip()
        if proc.returncode == 0 and sha:
            return sha
    except OSError:
        pass
    return "nogit"


def check_match_invariants(match: ParsedMatch, entry: CorpusEntry) -> list[str]:
    """Validate basic structural invariants on a parsed match.

    Args:
        match: Parsed replay output from :func:`gem.parse`.
        entry: Corpus metadata for the replay.

    Returns:
        List of human-readable invariant violations (empty when all pass).
    """
    issues: list[str] = []
    if match.match_id and match.match_id != entry.match_id:
        issues.append(f"match_id mismatch: parsed {match.match_id}, expected {entry.match_id}")
    if not match.players:
        issues.append("parsed match has no players")
        return issues

    player_ids = [p.player_id for p in match.players]
    if len(player_ids) != len(set(player_ids)):
        issues.append(f"duplicate player_ids: {player_ids}")

    non_negative_fields = (
        "kills",
        "deaths",
        "assists",
        "last_hits",
        "denies",
        "net_worth",
        "hero_damage",
        "tower_damage",
        "hero_healing",
    )
    for player in match.players:
        for attr in non_negative_fields:
            value = getattr(player, attr, 0)
            if isinstance(value, (int, float)) and value < 0:
                issues.append(f"player {player.player_id} has negative {attr}={value}")
        if player.game_times_min and player.game_times_min != sorted(player.game_times_min):
            issues.append(f"player {player.player_id} has non-monotonic game_times_min")

    if match.game_clock is not None:
        ticks = sorted(
            {
                t
                for t in (0, match.game_start_tick, match.game_end_tick)
                if isinstance(t, int) and t >= 0
            }
        )
        clock_samples = [
            secs for tick in ticks if (secs := match.game_clock.game_seconds_at(tick)) is not None
        ]
        if clock_samples != sorted(clock_samples):
            issues.append(f"game_clock regressed across ticks {ticks}: {clock_samples}")

    return issues


def _opendota_cache_valid(opendota_path: Path, entry: CorpusEntry) -> bool:
    if not opendota_path.is_file():
        return False
    if (
        entry.opendota_size_bytes is not None
        and opendota_path.stat().st_size != entry.opendota_size_bytes
    ):
        return False
    if entry.opendota_sha256 is not None:
        return file_sha256(opendota_path) == entry.opendota_sha256
    # Legacy index entries lack opendota_sha256; refresh if the index expects a
    # parsed OpenDota payload while the cached JSON is unparsed or unreadable.
    if entry.opendota_parsed:
        try:
            payload = json.loads(opendota_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False
        return isinstance(payload, dict) and bool(payload.get("radiant_gold_adv"))
    return True


def sync_corpus_entry(
    entry: CorpusEntry,
    *,
    corpus_dir: Path,
    bucket_uri: str | None,
    gcs: GcsClient | None,
) -> tuple[Path, Path]:
    """Ensure a corpus entry's compressed archive and OpenDota JSON exist locally.

    Verifies the local archive and OpenDota JSON against recorded size/SHA-256
    metadata and re-downloads from GCS when missing, stale, or corrupted.

    Args:
        entry: Corpus index record.
        corpus_dir: Local directory root mirroring ``corpus/``.
        bucket_uri: GCS bucket/prefix URI, or ``None`` for offline local mode.
        gcs: Active :class:`GcsClient`, or ``None`` for offline local mode.

    Returns:
        Tuple of ``(archive_path, opendota_json_path)``.

    Raises:
        RuntimeError: When files are missing or corrupted and cannot be fetched.
    """
    archive_path = corpus_dir / entry.archive_object
    opendota_path = corpus_dir / entry.opendota_object

    archive_valid = (
        archive_path.is_file()
        and archive_path.stat().st_size == entry.archive_size_bytes
        and file_sha256(archive_path) == entry.archive_sha256
    )
    if not archive_valid:
        if gcs is None or bucket_uri is None:
            raise RuntimeError(
                f"Match {entry.match_id}: archive missing or SHA-256 mismatch at {archive_path}"
            )
        archive_uri = join_gcs_uri(bucket_uri, "corpus", entry.archive_object)
        gcs.download(archive_uri, archive_path)
        actual_sha = file_sha256(archive_path)
        if actual_sha != entry.archive_sha256:
            raise RuntimeError(
                f"Match {entry.match_id}: downloaded archive SHA-256 mismatch "
                f"(expected {entry.archive_sha256}, got {actual_sha})"
            )

    if not _opendota_cache_valid(opendota_path, entry):
        if gcs is None or bucket_uri is None:
            raise RuntimeError(
                f"Match {entry.match_id}: OpenDota JSON missing or stale at {opendota_path}"
            )
        opendota_uri = join_gcs_uri(bucket_uri, "corpus", entry.opendota_object)
        gcs.download(opendota_uri, opendota_path)
        if entry.opendota_sha256 is not None:
            actual_od_sha = file_sha256(opendota_path)
            if actual_od_sha != entry.opendota_sha256:
                raise RuntimeError(
                    f"Match {entry.match_id}: downloaded OpenDota JSON SHA-256 mismatch "
                    f"(expected {entry.opendota_sha256}, got {actual_od_sha})"
                )

    return archive_path, opendota_path


def _ensure_dem(
    entry: CorpusEntry,
    archive_path: Path,
    *,
    scratch_dir: Path,
    keep_dem_dir: Path | None,
) -> Path:
    if keep_dem_dir is not None:
        keep_dem_dir.mkdir(parents=True, exist_ok=True)
        dem_path = keep_dem_dir / f"{entry.match_id}.dem"
        if (
            dem_path.is_file()
            and dem_path.stat().st_size == entry.dem_size_bytes
            and file_sha256(dem_path) == entry.dem_sha256
        ):
            return dem_path
    else:
        dem_path = scratch_dir / f"{entry.match_id}.dem"

    dem_bytes = _decompress_replay(archive_path.read_bytes())
    actual_sha = hashlib.sha256(dem_bytes).hexdigest()
    if actual_sha != entry.dem_sha256:
        raise RuntimeError(
            f"Decompressed SHA-256 mismatch for {entry.match_id}: "
            f"expected {entry.dem_sha256}, got {actual_sha}"
        )
    dem_path.write_bytes(dem_bytes)
    return dem_path


def _run_api_checks(match: ParsedMatch, scratch_dir: Path) -> dict[str, str]:
    import gem

    stage_errors: dict[str, str] = {}

    try:
        serialized = gem.to_json(match)
        reloaded = gem.from_dict(json.loads(serialized))
        if reloaded.match_id != match.match_id or len(reloaded.players) != len(match.players):
            stage_errors["json_roundtrip"] = (
                f"round-trip mismatch: match_id={reloaded.match_id}/{match.match_id}, "
                f"players={len(reloaded.players)}/{len(match.players)}"
            )
    except Exception:
        stage_errors["json_roundtrip"] = traceback.format_exc(limit=6).strip()

    try:
        gem.analyze(match)
    except Exception:
        stage_errors["analyze"] = traceback.format_exc(limit=6).strip()

    try:
        parquet_root = scratch_dir / "parquet"
        match_dir = parquet_root / str(match.match_id or "match")
        written = gem.to_parquet(match, match_dir, include=ALL_DATAFRAME_INCLUDES)
        if not written:
            stage_errors["parquet"] = "to_parquet wrote 0 files"
        else:
            summary_df = gem.read_parquet_table(parquet_root, "player_summary")
            if len(summary_df) != len(match.players):
                stage_errors["parquet"] = (
                    f"player_summary row count mismatch: {len(summary_df)} != {len(match.players)}"
                )
    except Exception:
        stage_errors["parquet"] = traceback.format_exc(limit=6).strip()

    return stage_errors


def evaluate_match(
    entry: CorpusEntry,
    archive_path: Path,
    opendota_path: Path,
    *,
    run_api_checks: bool = True,
    include_smoke_parity: bool = False,
    keep_dem_dir: Path | None = None,
    manifest_dir: Path | None = audit.DEFAULT_FIXTURES_DIR,
) -> MatchRunOutcome:
    """Parse one match once and run invariants, API checks, and OpenDota parity.

    Designed as a top-level function so it can run inside :class:`ProcessPoolExecutor`.

    Args:
        entry: Corpus index record for the match.
        archive_path: Local path to the compressed ``.dem.bz2`` / zstd archive.
        opendota_path: Local path to ``<match_id>.opendota.json``.
        run_api_checks: Whether to exercise JSON round-trip, ``analyze()``, and Parquet.
        include_smoke_parity: Also run OpenDota parity on ``smoke-only`` matches (e.g. Turbo).
        keep_dem_dir: Optional directory to persist decompressed ``.dem`` files.
        manifest_dir: Directory containing ``manifest.json`` for ``stale_fields`` and
            ``known_bugs`` annotations (defaults to ``tests/fixtures/opendota``).

    Returns:
        :class:`MatchRunOutcome` with timings, errors, invariants, and parity tallies.
    """
    import gem

    started = time.perf_counter()
    parse_seconds = 0.0
    stage_errors: dict[str, str] = {}
    invariants: list[str] = []
    parity_results: dict[str, audit.FieldResult] = {}
    parity_audited = False

    with tempfile.TemporaryDirectory(prefix=f"gem-harden-{entry.match_id}-") as tmp_name:
        scratch_dir = Path(tmp_name)
        try:
            dem_path = _ensure_dem(
                entry,
                archive_path,
                scratch_dir=scratch_dir,
                keep_dem_dir=keep_dem_dir,
            )
        except Exception:
            stage_errors["decompress"] = traceback.format_exc(limit=6).strip()
            return MatchRunOutcome(
                match_id=entry.match_id,
                source=entry.source,
                tags=entry.tags,
                ok=False,
                parse_seconds=0.0,
                total_seconds=time.perf_counter() - started,
                peak_rss_mb=_current_peak_rss_mb(),
                parity_audited=False,
                stage_errors=stage_errors,
            )

        parse_start = time.perf_counter()
        try:
            match = gem.parse(dem_path)
            parse_seconds = time.perf_counter() - parse_start
        except Exception:
            parse_seconds = time.perf_counter() - parse_start
            stage_errors["parse"] = traceback.format_exc(limit=8).strip()
            return MatchRunOutcome(
                match_id=entry.match_id,
                source=entry.source,
                tags=entry.tags,
                ok=False,
                parse_seconds=parse_seconds,
                total_seconds=time.perf_counter() - started,
                peak_rss_mb=_current_peak_rss_mb(),
                parity_audited=False,
                stage_errors=stage_errors,
            )

        try:
            invariants = check_match_invariants(match, entry)
        except Exception:
            stage_errors["invariants"] = traceback.format_exc(limit=6).strip()

        if run_api_checks:
            stage_errors.update(_run_api_checks(match, scratch_dir))

        should_audit = entry.parity_eligible or (include_smoke_parity and entry.opendota_parsed)
        if should_audit:
            try:
                od = json.loads(opendota_path.read_text(encoding="utf-8"))
                if od.get("radiant_gold_adv"):
                    match_key = str(entry.match_id)
                    stale = (
                        audit.stale_fields(manifest_dir, match_key)
                        if manifest_dir is not None
                        else frozenset()
                    )
                    bugs = (
                        audit.known_bugs(manifest_dir, match_key)
                        if manifest_dir is not None
                        else ()
                    )
                    audit.audit_match(match_key, match, od, parity_results, stale, bugs)
                    parity_audited = True
            except Exception:
                stage_errors["opendota_parity"] = traceback.format_exc(limit=6).strip()

    ok = not stage_errors and not invariants
    return MatchRunOutcome(
        match_id=entry.match_id,
        source=entry.source,
        tags=entry.tags,
        ok=ok,
        parse_seconds=parse_seconds,
        total_seconds=time.perf_counter() - started,
        peak_rss_mb=_current_peak_rss_mb(),
        parity_audited=parity_audited,
        invariants=invariants,
        stage_errors=stage_errors,
        parity_results=parity_results,
    )


def run_batch_parquet_check(
    entries_with_archives: Sequence[tuple[CorpusEntry, Path]],
    *,
    workers: int,
) -> tuple[bool, str]:
    """Verify ``parse_many_to_parquet`` and ``read_parquet_table`` over a batch of replays.

    Args:
        entries_with_archives: Pairs of ``(CorpusEntry, archive_path)`` to include.
        workers: Number of parallel workers for ``parse_many_to_parquet``.

    Returns:
        ``(ok, message)`` summary of the batch check.
    """
    import gem

    if not entries_with_archives:
        return True, "batch check skipped (0 matches)"

    started = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory(prefix="gem-batch-check-") as tmp_name:
            root = Path(tmp_name)
            dem_dir = root / "dems"
            out_dir = root / "parquet"
            dem_dir.mkdir()
            dem_paths: list[Path] = []
            for entry, archive_path in entries_with_archives:
                dem_path = dem_dir / f"{entry.match_id}.dem"
                dem_path.write_bytes(_decompress_replay(archive_path.read_bytes()))
                dem_paths.append(dem_path)

            written = gem.parse_many_to_parquet(
                dem_paths,
                out_dir,
                workers=min(workers, len(dem_paths)),
                progress=False,
            )
            summary_df = gem.read_parquet_table(out_dir, "player_summary")
            seen_replays = set(summary_df["replay"].unique())
            expected_replays = {str(entry.match_id) for entry, _ in entries_with_archives}
            missing = sorted(expected_replays - seen_replays)
            elapsed = time.perf_counter() - started
            if missing:
                return False, f"batch check missing replay outputs: {', '.join(missing)}"
            return (
                True,
                f"batch check OK: {len(dem_paths)} replays, {len(written)} parquet files, "
                f"{len(summary_df)} player rows in {elapsed:.1f}s",
            )
    except Exception as exc:
        elapsed = time.perf_counter() - started
        return (
            False,
            f"batch check FAILED after {elapsed:.1f}s: {type(exc).__name__}: {exc}",
        )


def format_hardening_report(
    outcomes: Sequence[MatchRunOutcome],
    merged_parity: dict[str, audit.FieldResult],
    *,
    entries: Sequence[CorpusEntry],
    baseline: dict[str, Any] | None = None,
    examples: bool = False,
    batch_note: str | None = None,
) -> str:
    """Format a triage-oriented plain-text report for a hardening sweep."""
    passed = sum(1 for o in outcomes if o.ok)
    failed = [o for o in outcomes if not o.ok]
    parity_count = sum(1 for o in outcomes if o.parity_audited)
    distinct_heroes = len({h for e in entries for h in e.hero_ids if h > 0})
    total_parse_s = sum(o.parse_seconds for o in outcomes)
    max_rss_mb = max((o.peak_rss_mb for o in outcomes), default=0.0)

    lines = [
        f"Hardening sweep: {passed}/{len(outcomes)} matches passed, "
        f"{len(failed)} failed, {parity_count} audited for OpenDota parity",
        f"Coverage: {distinct_heroes} distinct hero IDs | "
        f"Cumulative parse time: {total_parse_s:.1f}s | Peak worker RSS: {max_rss_mb:.1f} MB",
    ]
    if batch_note:
        lines.append(batch_note)

    if failed:
        lines.append("")
        lines.append("=== FAILURES ===")
        for outcome in sorted(failed, key=lambda o: o.match_id):
            lines.append(
                f"Match {outcome.match_id} ({outcome.source}, tags={','.join(outcome.tags)}):"
            )
            for issue in outcome.invariants:
                lines.append(f"  [invariant] {issue}")
            for stage, err in sorted(outcome.stage_errors.items()):
                first_line = err.splitlines()[-1] if err else "error"
                lines.append(f"  [{stage}] {first_line}")

    slowest = sorted(outcomes, key=lambda o: o.parse_seconds, reverse=True)[:5]
    if slowest:
        lines.append("")
        lines.append("=== SLOWEST MATCHES ===")
        for outcome in slowest:
            lines.append(
                f"  {outcome.match_id}  parse={outcome.parse_seconds:6.2f}s  "
                f"total={outcome.total_seconds:6.2f}s  rss={outcome.peak_rss_mb:6.1f} MB  "
                f"[{','.join(outcome.tags)}]"
            )

    if merged_parity:
        lines.append("")
        lines.append("=== OPENDOTA PARITY ===")
        lines.append(audit.format_report(merged_parity, baseline=baseline, examples=examples))

    return "\n".join(lines)


def _load_baseline(compare_arg: str, gcs: GcsClient | None) -> dict[str, Any]:
    if compare_arg.startswith("gs://"):
        client = gcs or GcsClient()
        payload = client.read_json(compare_arg)
    else:
        payload = json.loads(Path(compare_arg).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Comparison baseline must be a JSON object: {compare_arg}")
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the hardening corpus runner."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--bucket",
        help="GCS bucket or prefix URI (default: $GEM_CORPUS_BUCKET unless --local-corpus-dir is set).",
    )
    parser.add_argument(
        "--local-corpus-dir",
        type=Path,
        help="Run fully offline against a local corpus directory containing index.json and matches/.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=DEFAULT_CACHE_DIR,
        help=f"Local cache directory for synced GCS corpus files (default: {DEFAULT_CACHE_DIR}).",
    )
    parser.add_argument(
        "--keep-dem",
        action="store_true",
        help="Keep decompressed .dem files under <cache-dir>/dem/ across runs.",
    )
    parser.add_argument(
        "--tag",
        dest="tags",
        action="append",
        default=[],
        help="Include matches with at least one of these tags (repeatable).",
    )
    parser.add_argument(
        "--exclude-tag",
        dest="exclude_tags",
        action="append",
        default=[],
        help="Exclude matches with any of these tags (repeatable).",
    )
    parser.add_argument(
        "--patch",
        dest="patches",
        action="append",
        type=int,
        default=[],
        help="Filter to specific patch ID(s) (repeatable, e.g. 61).",
    )
    parser.add_argument(
        "--match",
        dest="match_ids",
        action="append",
        type=int,
        default=[],
        help="Run only these specific match ID(s) (repeatable).",
    )
    parser.add_argument("--limit", type=int, help="Maximum number of matches to run.")
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Parallel worker processes (default: 4).",
    )
    parser.add_argument(
        "--skip-api-checks",
        action="store_true",
        help="Skip JSON round-trip, analyze(), and Parquet checks (parse + invariants + parity only).",
    )
    parser.add_argument(
        "--include-smoke-parity",
        action="store_true",
        help="Also include smoke-only matches (e.g. Turbo) in OpenDota parity scoring.",
    )
    parser.add_argument(
        "--batch-check",
        type=int,
        default=0,
        help="Run parse_many_to_parquet over the first N selected matches (default: 0 = off).",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Show the first mismatch example for each non-exact parity field.",
    )
    parser.add_argument(
        "--compare",
        help="Baseline parity.json (local path or gs:// URI) to check for regressions.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Directory to write summary.json, parity.json, and report.txt.",
    )
    parser.add_argument(
        "--upload-run",
        action="store_true",
        help="Upload summary.json, parity.json, and report.txt to gs://<bucket>/runs/<run-id>/.",
    )
    return parser.parse_args(argv)


def _load_corpus_context(
    args: argparse.Namespace,
) -> tuple[Path, CorpusIndex, str | None, GcsClient | None]:
    if args.local_corpus_dir is not None:
        corpus_dir = args.local_corpus_dir
        index = CorpusIndex.from_dict(
            json.loads((corpus_dir / "index.json").read_text(encoding="utf-8"))
        )
        if not args.upload_run:
            return corpus_dir, index, None, None
        bucket_uri = resolve_bucket(args.bucket)
        gcs = GcsClient()
        gcs.check_access(bucket_uri)
        return corpus_dir, index, bucket_uri, gcs

    bucket_uri = resolve_bucket(args.bucket)
    gcs = GcsClient()
    gcs.check_access(bucket_uri)
    corpus_dir = args.cache_dir / "corpus"
    index = load_corpus_index_from_gcs(gcs, bucket_uri)
    if index.matches:
        corpus_dir.mkdir(parents=True, exist_ok=True)
        (corpus_dir / "index.json").write_text(
            json.dumps(index.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return corpus_dir, index, bucket_uri, gcs


def _evaluate_synced(
    synced: Sequence[tuple[CorpusEntry, Path, Path]],
    *,
    workers: int,
    run_api_checks: bool,
    include_smoke_parity: bool,
    keep_dem_dir: Path | None,
) -> list[MatchRunOutcome]:
    if workers == 1:
        outcomes = [
            evaluate_match(
                entry,
                archive_path,
                opendota_path,
                run_api_checks=run_api_checks,
                include_smoke_parity=include_smoke_parity,
                keep_dem_dir=keep_dem_dir,
            )
            for entry, archive_path, opendota_path in synced
        ]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [
                pool.submit(
                    evaluate_match,
                    entry,
                    archive_path,
                    opendota_path,
                    run_api_checks=run_api_checks,
                    include_smoke_parity=include_smoke_parity,
                    keep_dem_dir=keep_dem_dir,
                )
                for entry, archive_path, opendota_path in synced
            ]
            outcomes = [future.result() for future in futures]
    outcomes.sort(key=lambda o: o.match_id)
    return outcomes


def _persist_run_artifacts(
    *,
    summary_payload: dict[str, Any],
    parity_json: dict[str, Any],
    report_text: str,
    out_dir_arg: Path | None,
    upload_run: bool,
    gcs: GcsClient | None,
    bucket_uri: str | None,
) -> None:
    if out_dir_arg is None and not upload_run:
        return
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-{_git_short_sha()}"
    with tempfile.TemporaryDirectory(prefix="gem-run-out-") as tmp_out:
        out_dir = out_dir_arg if out_dir_arg is not None else Path(tmp_out)
        out_dir.mkdir(parents=True, exist_ok=True)
        summary_path = out_dir / "summary.json"
        parity_path = out_dir / "parity.json"
        report_path = out_dir / "report.txt"
        summary_path.write_text(
            json.dumps(summary_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        parity_path.write_text(
            json.dumps(parity_json, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        report_path.write_text(report_text + "\n", encoding="utf-8")

        if upload_run and gcs is not None and bucket_uri is not None:
            run_prefix = join_gcs_uri(bucket_uri, "runs", run_id)
            gcs.upload(summary_path, join_gcs_uri(run_prefix, "summary.json"))
            gcs.upload(parity_path, join_gcs_uri(run_prefix, "parity.json"))
            gcs.upload(report_path, join_gcs_uri(run_prefix, "report.txt"))
            print(f"\nUploaded run artifacts to {run_prefix}/")


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for running the hardening corpus sweep."""
    args = parse_args(argv)
    try:
        corpus_dir, index, bucket_uri, gcs = _load_corpus_context(args)
    except (ValueError, GcsError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    selected = index.filter_entries(
        tags=args.tags,
        exclude_tags=args.exclude_tags,
        patches=args.patches,
        match_ids=args.match_ids,
        limit=args.limit,
    )
    if not selected:
        print("No corpus matches matched the selection filters.", file=sys.stderr)
        return 1

    baseline: dict[str, Any] | None = None
    if args.compare:
        try:
            baseline = _load_baseline(args.compare, gcs)
        except (ValueError, GcsError, OSError, json.JSONDecodeError) as exc:
            print(f"ERROR loading --compare baseline: {exc}", file=sys.stderr)
            return 1

    synced: list[tuple[CorpusEntry, Path, Path]] = []
    print(f"Syncing {len(selected)} match(es)...", flush=True)
    for entry in selected:
        try:
            archive_path, opendota_path = sync_corpus_entry(
                entry,
                corpus_dir=corpus_dir,
                bucket_uri=bucket_uri,
                gcs=gcs,
            )
        except (RuntimeError, GcsError) as exc:
            print(f"ERROR syncing match {entry.match_id}: {exc}", file=sys.stderr)
            return 1
        synced.append((entry, archive_path, opendota_path))

    workers = max(1, min(args.workers, len(synced)))
    print(f"Evaluating {len(synced)} match(es) across {workers} worker(s)...", flush=True)
    outcomes = _evaluate_synced(
        synced,
        workers=workers,
        run_api_checks=not args.skip_api_checks,
        include_smoke_parity=args.include_smoke_parity,
        keep_dem_dir=(args.cache_dir / "dem") if args.keep_dem else None,
    )

    merged_parity: dict[str, audit.FieldResult] = {}
    for outcome in outcomes:
        audit.merge_results(merged_parity, outcome.parity_results)
    merged_parity = dict(sorted(merged_parity.items()))

    batch_ok = True
    batch_note: str | None = None
    if args.batch_check > 0:
        batch_slice = [(entry, arch) for entry, arch, _ in synced[: args.batch_check]]
        batch_ok, batch_note = run_batch_parquet_check(batch_slice, workers=workers)

    report_text = format_hardening_report(
        outcomes,
        merged_parity,
        entries=selected,
        baseline=baseline,
        examples=args.examples,
        batch_note=batch_note,
    )
    print(report_text)

    summary_payload = {
        "schema_version": 1,
        "git_sha": _git_short_sha(),
        "ran_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "matches_total": len(outcomes),
        "matches_passed": sum(1 for o in outcomes if o.ok),
        "matches_failed": sum(1 for o in outcomes if not o.ok),
        "parity_audited": sum(1 for o in outcomes if o.parity_audited),
        "distinct_heroes": len({h for e in selected for h in e.hero_ids if h > 0}),
        "batch_check_ok": batch_ok,
        "batch_check_note": batch_note,
        "outcomes": [o.to_summary_dict() for o in outcomes],
    }
    _persist_run_artifacts(
        summary_payload=summary_payload,
        parity_json=audit.results_to_json(merged_parity),
        report_text=report_text,
        out_dir_arg=args.out_dir,
        upload_run=args.upload_run,
        gcs=gcs,
        bucket_uri=bucket_uri,
    )

    has_regression = False
    if baseline is not None:
        incompatible = audit.incompatible_baseline_fields(merged_parity, baseline)
        if incompatible:
            print(
                f"Incompatible --compare baseline on: {', '.join(incompatible)}",
                file=sys.stderr,
            )
            has_regression = True
        elif audit.regressed(merged_parity, baseline):
            has_regression = True

    return 1 if (any(not o.ok for o in outcomes) or not batch_ok or has_regression) else 0


if __name__ == "__main__":
    raise SystemExit(main())
