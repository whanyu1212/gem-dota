"""Reproduce full-replay timing, CPU sampling, and Python allocation profiles.

Run each invocation in a fresh process, with no concurrent benchmarks. See
docs/deep-dives/parser-performance.md for the measurement protocol. This harness
does not change parsing logic (reference: manta/parser.go and field_reader.go).
"""

from __future__ import annotations

import argparse
import cProfile
import gc
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import pstats
import resource
import subprocess
import sys
import time
import tracemalloc
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
# Exact normalized public outputs validated in parser-profile-2026-09.md.
EXPECTED_OUTPUT_SHA256 = {
    8822520406: "3b0844312187a2856743092e991ab425878d64e101d91cf8f9c83bb2b3580427",
    8856501050: "1e8d1f6f172d7bc39abd6b2a338539b231395780e599b9b8fbf44068128a9e5e",
}


def _parser_commit() -> str:
    status = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all", "--", "src/gem"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    if status:
        raise RuntimeError(f"Refusing to profile dirty parser sources:\n{status}")
    return subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _checked_output(match: Any) -> dict[str, Any]:
    import gem

    expected = EXPECTED_OUTPUT_SHA256[match.match_id]
    payload = json.dumps(gem.to_dict(match), sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != expected:
        raise RuntimeError(
            f"Public output mismatch for {match.match_id}: expected {expected}, got {digest}"
        )
    return {
        "bytes": len(payload),
        "sha256": digest,
        "players": len(match.players),
        "combat_log_entries": len(match.combat_log),
        "duration": match.duration,
    }


def _command(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    return (result.stdout + result.stderr).strip()


def _path(filename: str) -> str:
    return filename.removeprefix(str(ROOT) + "/")


def _rss() -> int:
    import psutil

    return psutil.Process().memory_info().rss


def _snapshot() -> dict[str, Any]:
    current, peak = tracemalloc.get_traced_memory()
    snapshot = tracemalloc.take_snapshot()
    return {
        "current_bytes": current,
        "peak_bytes": peak,
        "tracer_metadata_bytes": tracemalloc.get_tracemalloc_memory(),
        "top_lines": [
            {
                "location": f"{_path(s.traceback[0].filename)}:{s.traceback[0].lineno}",
                "bytes": s.size,
                "blocks": s.count,
            }
            for s in snapshot.statistics("lineno")[:100]
        ],
    }


def _sample_summary(session: Any) -> dict[str, Any]:
    totals: dict[tuple[str, int, str], list[float]] = defaultdict(lambda: [0.0, 0.0])

    def visit(frame: Any, ancestors: frozenset[Any]) -> None:
        key = (_path(frame.file_path or ""), frame.line_no or 0, frame.function)
        # Count recursive inclusive time once per stack, and every exclusive frame.
        totals[key][0] += max(0.0, frame.total_self_time)
        if key not in ancestors:
            totals[key][1] += frame.time
        for child in frame.children:
            if not child.is_synthetic:
                visit(child, ancestors | {key})

    frame = session.root_frame()
    if frame is not None:
        visit(frame, frozenset())
    return {
        "duration_s": session.duration,
        "cpu_s": session.cpu_time,
        "sample_count": session.sample_count,
        "interval_s": 0.005,
        "functions": [
            {"file": k[0], "line": k[1], "function": k[2], "self_s": v[0], "inclusive_s": v[1]}
            for k, v in sorted(totals.items(), key=lambda item: -item[1][0])
        ],
    }


def _run(args: argparse.Namespace) -> dict[str, Any]:
    commit = _parser_commit()
    sys.path.insert(0, str(ROOT / "src"))
    import gem
    from gem.parser import ReplayParser

    assert Path(gem.__file__).resolve().is_relative_to(ROOT / "src")
    # Equal imports in public/core runs; do not initialize a parser for warmup.
    for module in (
        "gem.combat.aggregator",
        "gem.extractors.courier",
        "gem.extractors.draft",
        "gem.extractors.intervals",
        "gem.extractors.objectives",
        "gem.extractors.players",
        "gem.extractors.smoke_vision",
        "gem.extractors.wards",
        "gem.results.assembly",
    ):
        importlib.import_module(module)
    _rss()  # Import psutil outside the timer.
    replay = args.replay.resolve()
    manifest = json.loads((ROOT / "tests/fixtures/opendota/manifest.json").read_text())
    fixture = next(m for m in manifest["matches"] if m["dem"] == replay.name)
    if args.scenario == "public" and fixture["match_id"] not in EXPECTED_OUTPUT_SHA256:
        raise ValueError(f"No validated public output hash for {fixture['match_id']}")
    digest = hashlib.sha256()
    with replay.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    assert replay.stat().st_size == fixture["dem_size_bytes"]
    assert digest.hexdigest() == fixture["dem_sha256"]
    del chunk

    report: dict[str, Any] = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "scenario": args.scenario,
        "commit": commit,
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "gc_enabled": gc.isenabled(),
        "hash_seed": os.environ.get("PYTHONHASHSEED"),
        "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},
        "fixture": {
            k: fixture[k] for k in ("match_id", "duration", "dem_size_bytes", "dem_sha256")
        },
        "power_start": _command("pmset", "-g", "batt") if sys.platform == "darwin" else None,
    }
    original_parse = ReplayParser.parse
    parsed: dict[str, Any] = {}

    def checked_parse(parser: Any) -> None:
        original_parse(parser)
        if parser.parse_error is not None:
            raise RuntimeError(f"Incomplete replay at {parser.tick}") from parser.parse_error
        parsed.update(match_id=parser.match_id, tick=parser.tick, game_build=parser.game_build)

    ReplayParser.parse = checked_parse  # type: ignore[method-assign, assignment]
    parser = ReplayParser(replay) if args.scenario == "core" else None
    sample = None
    deterministic = None
    if args.mode == "sample":
        if args.profiler_path:
            sys.path.insert(0, str(args.profiler_path.resolve()))
        from pyinstrument import Profiler

        sample = Profiler(interval=0.005, async_mode="disabled")
        report["pyinstrument_version"] = importlib.metadata.version("pyinstrument")
    elif args.mode == "cprofile":
        deterministic = cProfile.Profile()
    elif args.mode == "memory":
        from gem.results import assembly

        original_build = assembly.build_parsed_match

        def measured_build(**kwargs: Any) -> Any:
            report["before_assembly"] = _snapshot()
            return original_build(**kwargs)

        if args.scenario == "public":
            assembly.build_parsed_match = measured_build  # type: ignore[assignment]

    gc.collect()
    report["rss_before_bytes"] = _rss()
    report["load_start"] = os.getloadavg()
    if args.mode == "memory":
        tracemalloc.start(1)
    if sample:
        sample.start()
    if deterministic:
        deterministic.enable()
    cpu_start = resource.getrusage(resource.RUSAGE_SELF)
    start = time.perf_counter()
    match = gem.parse(replay) if parser is None else parser.parse()  # type: ignore[func-returns-value]
    elapsed = time.perf_counter() - start
    cpu_end = resource.getrusage(resource.RUSAGE_SELF)
    if sample:
        sample.stop()
    if deterministic:
        deterministic.disable()
    # Capture before serialization, profile rendering, snapshots, or collection.
    report.update(
        elapsed_s=elapsed,
        user_s=cpu_end.ru_utime - cpu_start.ru_utime,
        system_s=cpu_end.ru_stime - cpu_start.ru_stime,
        peak_rss_bytes=cpu_end.ru_maxrss * (1 if sys.platform == "darwin" else 1024),
        rss_after_parse_bytes=_rss(),
        load_end=os.getloadavg(),
        parser=parsed,
    )
    if args.mode == "memory":
        report["after_parse"] = _snapshot()
    gc.collect()
    report["rss_after_gc_bytes"] = _rss()
    if args.mode == "memory":
        report["after_gc"] = _snapshot()
        tracemalloc.stop()
    report["power_end"] = _command("pmset", "-g", "batt") if sys.platform == "darwin" else None
    assert parsed["match_id"] == fixture["match_id"]
    if match is not None:
        assert match.match_id == fixture["match_id"] and len(match.players) == 10
        assert match.duration == fixture["duration"]
        # All output, without removing fields; no full JSON artifacts are needed.
        report["output"] = _checked_output(match)
    if sample:
        assert sample.last_session is not None
        report["sampling"] = _sample_summary(sample.last_session)
    if deterministic:
        stats = pstats.Stats(deterministic)
        report["cprofile"] = {
            "total_s": stats.total_tt,  # type: ignore[attr-defined]
            "functions": [
                {
                    "file": _path(k[0]),
                    "line": k[1],
                    "function": k[2],
                    "primitive_calls": v[0],
                    "calls": v[1],
                    "self_s": v[2],
                    "inclusive_s": v[3],
                }
                for k, v in sorted(stats.stats.items(), key=lambda item: -item[1][2])  # type: ignore[attr-defined]
            ],
        }
    if _parser_commit() != commit:
        raise RuntimeError("Git HEAD changed during profiling")
    return report


def main() -> None:
    """Run one fresh-process measurement and save its auditable JSON result."""
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--replay", type=Path, required=True)
    cli.add_argument("--scenario", choices=("public", "core"), required=True)
    cli.add_argument("--mode", choices=("timing", "sample", "memory", "cprofile"), default="timing")
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument(
        "--profiler-path", type=Path, help="Optional isolated pyinstrument installation"
    )
    args = cli.parse_args()
    if args.output.exists():
        cli.error(f"Refusing to overwrite {args.output}")
    report = _run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                **{
                    k: report[k]
                    for k in ("mode", "scenario", "elapsed_s", "user_s", "peak_rss_bytes")
                },
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
