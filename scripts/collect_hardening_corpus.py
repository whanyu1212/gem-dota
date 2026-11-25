"""Discover, verify, and upload a diverse Dota 2 replay corpus to GCS.

Collects pro tournament matches (via OpenDota Explorer), freshly parsed ranked
and Turbo pubs (via ``/api/parsedMatches`` + ``public_matches``), and explicit
match IDs. Uses greedy hero-coverage selection so a modest corpus exercises as
much of the hero pool and lobby/duration spectrum as possible.

Also mirrors active curated fixtures from ``tests/fixtures/opendota/manifest.json``
into ``gs://<bucket>/fixtures/`` so Valve CDN expiry never breaks them.

Examples:
    export GEM_CORPUS_BUCKET=gs://my-gem-hardening
    uv run python scripts/collect_hardening_corpus.py --check-bucket
    uv run python scripts/collect_hardening_corpus.py --league 20208 --league-limit 35 \\
        --ranked-count 35 --turbo-count 3 --dry-run
    uv run python scripts/collect_hardening_corpus.py --mirror-manifest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
for _path in (SCRIPTS_DIR, REPO_ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from _hardening_gcs import (  # noqa: E402
    CorpusEntry,
    CorpusIndex,
    GcsClient,
    GcsError,
    join_gcs_uri,
    load_corpus_index_from_gcs,
    resolve_bucket,
)
from sync_opendota_fixtures import (  # noqa: E402
    DEFAULT_MANIFEST,
    FixtureSpec,
    load_fixture_manifest,
)

from gem.replays.fetch import _SSL_CONTEXT, _decompress_replay  # noqa: E402

OPENDOTA_BASE = "https://api.opendota.com/api"
USER_AGENT = "gem-hardening-collector/1.0"
SHORT_DURATION_S = 1500
LONG_DURATION_S = 3600


class OpenDotaApiError(RuntimeError):
    """Raised when an OpenDota API request fails."""


@dataclass(frozen=True, slots=True)
class CandidateMatch:
    """Lightweight match candidate returned by discovery queries."""

    match_id: int
    source: str
    tags: tuple[str, ...]
    duration: int | None
    lobby_type: int | None
    game_mode: int | None
    hero_ids: tuple[int, ...]
    has_abandon: bool = False
    opendota_parsed: bool = True


@dataclass(frozen=True, slots=True)
class CollectionOutcome:
    """Result of attempting to ingest one candidate match into GCS."""

    match_id: int
    status: str  # "uploaded", "skipped", "failed"
    detail: str
    entry: CorpusEntry | None = None


def utc_now_iso() -> str:
    """Return the current UTC timestamp formatted as ``YYYY-MM-DDTHH:MM:SSZ``."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def derive_match_tags(
    payload: dict[str, Any],
    *,
    extra_tags: Sequence[str] = (),
) -> tuple[str, ...]:
    """Derive standardized corpus tags from an OpenDota ``/matches/{id}`` payload.

    Args:
        payload: OpenDota match JSON payload.
        extra_tags: Additional caller-supplied tags to include.

    Returns:
        Sorted tuple of unique tags.
    """
    tags = {tag.strip() for tag in extra_tags if tag and tag.strip()}

    lobby_type = payload.get("lobby_type")
    if lobby_type == 1:
        tags.add("pro")
    elif lobby_type == 7:
        tags.add("ranked")
    elif lobby_type == 0:
        tags.add("unranked")

    game_mode = payload.get("game_mode")
    if game_mode == 2:
        tags.add("cm")
    elif game_mode == 22:
        tags.add("ap")
    elif game_mode == 23:
        tags.add("turbo")
        tags.add("smoke-only")

    patch = payload.get("patch")
    if isinstance(patch, int) and not isinstance(patch, bool):
        tags.add(f"patch-{patch}")

    duration = payload.get("duration")
    if isinstance(duration, int) and not isinstance(duration, bool):
        if duration < SHORT_DURATION_S:
            tags.add("short")
        elif duration >= LONG_DURATION_S:
            tags.add("long")

    if payload_has_abandon(payload):
        tags.add("abandon")

    return tuple(sorted(tags))


def payload_hero_ids(payload: dict[str, Any]) -> tuple[int, ...]:
    """Extract ordered non-zero hero IDs from an OpenDota match payload."""
    players = payload.get("players") or []
    ordered = sorted(
        (p for p in players if isinstance(p, dict)),
        key=lambda p: p.get("player_slot", 0),
    )
    heroes: list[int] = []
    for player in ordered:
        hero_id = player.get("hero_id")
        if isinstance(hero_id, int) and not isinstance(hero_id, bool) and hero_id > 0:
            heroes.append(hero_id)
    return tuple(heroes)


def payload_has_abandon(payload: dict[str, Any]) -> bool:
    """Return whether any player in an OpenDota match payload abandoned (``leaver_status >= 2``)."""
    for player in payload.get("players") or []:
        if not isinstance(player, dict):
            continue
        leaver = player.get("leaver_status")
        if isinstance(leaver, int) and not isinstance(leaver, bool) and leaver >= 2:
            return True
    return False


def payload_is_parsed(payload: dict[str, Any]) -> bool:
    """Return whether OpenDota fully parsed the match (matches ``audit_opendota_parity``)."""
    return bool(payload.get("radiant_gold_adv"))


class OpenDotaClient:
    """Rate-limit-aware OpenDota HTTP client using stdlib ``urllib``."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        request_delay: float = 1.1,
        max_retries: int = 3,
        timeout: int = 30,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self._api_key = api_key
        self._request_delay = max(0.0, request_delay)
        self._max_retries = max_retries
        self._timeout = timeout
        self._sleep = sleep_fn
        self._last_request_at = 0.0

    def _with_api_key(self, url: str) -> str:
        if not self._api_key:
            return url
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}api_key={urllib.parse.quote(self._api_key, safe='')}"

    def _pace(self) -> None:
        if self._request_delay <= 0 or self._last_request_at == 0.0:
            return
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._request_delay:
            self._sleep(self._request_delay - elapsed)

    def get_json(self, url: str) -> Any:
        """Fetch and decode JSON from OpenDota with retry on 429 and transient 5xx.

        Args:
            url: Full OpenDota API URL without ``api_key``.

        Returns:
            Decoded JSON payload.

        Raises:
            OpenDotaApiError: If all retry attempts fail.
        """
        full_url = self._with_api_key(url)
        for attempt in range(self._max_retries + 1):
            self._pace()
            self._last_request_at = time.monotonic()
            req = urllib.request.Request(full_url, headers={"User-Agent": USER_AGENT})
            try:
                with urllib.request.urlopen(
                    req, context=_SSL_CONTEXT, timeout=self._timeout
                ) as resp:
                    return json.loads(resp.read())
            except urllib.error.HTTPError as exc:
                retryable = exc.code == 429 or 500 <= exc.code < 600
                if retryable and attempt < self._max_retries:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    backoff = (
                        float(retry_after)
                        if retry_after and retry_after.isdigit()
                        else (2.0 ** (attempt + 1))
                    )
                    self._sleep(backoff)
                    continue
                # Never include full_url (which may hold api_key) in error messages.
                raise OpenDotaApiError(f"OpenDota HTTP {exc.code} for {url}") from exc
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt < self._max_retries:
                    self._sleep(2.0 ** (attempt + 1))
                    continue
                raise OpenDotaApiError(f"OpenDota request failed for {url}: {exc}") from exc
        raise OpenDotaApiError(f"OpenDota request exhausted retries for {url}")

    def explorer_query(self, sql: str) -> list[dict[str, Any]]:
        """Execute a read-only SQL query via ``/api/explorer``.

        Args:
            sql: PostgreSQL query string.

        Returns:
            List of row dicts returned by OpenDota.
        """
        url = f"{OPENDOTA_BASE}/explorer?sql={urllib.parse.quote(sql)}"
        payload = self.get_json(url)
        if not isinstance(payload, dict):
            raise OpenDotaApiError("OpenDota explorer returned a non-object response")
        if payload.get("err"):
            raise OpenDotaApiError(f"OpenDota explorer SQL error: {payload['err']}")
        rows = payload.get("rows")
        if not isinstance(rows, list):
            return []
        return [row for row in rows if isinstance(row, dict)]

    def fetch_match(self, match_id: int) -> dict[str, Any]:
        """Fetch full match JSON from ``/api/matches/{match_id}``."""
        payload = self.get_json(f"{OPENDOTA_BASE}/matches/{int(match_id)}")
        if not isinstance(payload, dict):
            raise OpenDotaApiError(f"OpenDota returned non-object payload for match {match_id}")
        return payload

    def discover_league_matches(self, league_id: int, *, limit: int = 200) -> list[CandidateMatch]:
        """Discover parsed matches in an OpenDota league with hero rosters.

        Args:
            league_id: OpenDota / Steam league ID (e.g. ``20208`` for BLAST SLAM IX).
            limit: Maximum number of candidate rows to fetch.

        Returns:
            List of :class:`CandidateMatch` records ordered newest first.
        """
        sql = (
            "SELECT m.match_id, m.duration, m.game_mode, m.lobby_type, m.version, "
            "array_agg(pm.hero_id ORDER BY pm.player_slot) AS hero_ids, "
            "bool_or(COALESCE(pm.leaver_status, 0) >= 2) AS has_abandon "
            "FROM matches m "
            "JOIN player_matches pm ON pm.match_id = m.match_id "
            f"WHERE m.leagueid = {int(league_id)} AND m.version IS NOT NULL "
            "GROUP BY m.match_id, m.duration, m.game_mode, m.lobby_type, m.version, m.start_time "
            f"ORDER BY m.start_time DESC LIMIT {int(limit)}"
        )
        rows = self.explorer_query(sql)
        candidates: list[CandidateMatch] = []
        for row in rows:
            match_id = row.get("match_id")
            if not isinstance(match_id, int):
                continue
            heroes = tuple(
                int(h) for h in (row.get("hero_ids") or []) if isinstance(h, int) and h > 0
            )
            candidates.append(
                CandidateMatch(
                    match_id=match_id,
                    source=f"league-{int(league_id)}",
                    tags=("pro", "cm") if row.get("game_mode") == 2 else ("pro",),
                    duration=row.get("duration"),
                    lobby_type=row.get("lobby_type"),
                    game_mode=row.get("game_mode"),
                    hero_ids=heroes,
                    has_abandon=bool(row.get("has_abandon", False)),
                    opendota_parsed=True,
                )
            )
        return candidates

    def _fetch_parsed_match_ids(self, pages: int) -> list[int]:
        match_ids: list[int] = []
        seen: set[int] = set()
        cursor: int | None = None
        for _ in range(max(1, pages)):
            url = f"{OPENDOTA_BASE}/parsedMatches"
            if cursor is not None:
                url = f"{url}?less_than_match_id={cursor}"
            batch = self.get_json(url)
            if not isinstance(batch, list) or not batch:
                break
            batch_ids = [
                int(row["match_id"])
                for row in batch
                if isinstance(row, dict) and isinstance(row.get("match_id"), int)
            ]
            if not batch_ids:
                break
            for mid in batch_ids:
                if mid not in seen:
                    seen.add(mid)
                    match_ids.append(mid)
            cursor = min(batch_ids)
        return match_ids

    @staticmethod
    def _candidate_from_public_row(row: dict[str, Any]) -> CandidateMatch | None:
        match_id = row.get("match_id")
        if not isinstance(match_id, int):
            return None
        lobby_type = row.get("lobby_type")
        game_mode = row.get("game_mode")
        if lobby_type == 7 and game_mode == 22:
            source, tags = "ranked-ap", ("ranked", "ap")
        elif game_mode == 23:
            source, tags = "turbo", ("turbo", "smoke-only")
        else:
            return None
        radiant = row.get("radiant_team") or []
        dire = row.get("dire_team") or []
        heroes = tuple(int(h) for h in (*radiant, *dire) if isinstance(h, int) and h > 0)
        return CandidateMatch(
            match_id=match_id,
            source=source,
            tags=tags,
            duration=row.get("duration"),
            lobby_type=lobby_type,
            game_mode=game_mode,
            hero_ids=heroes,
            has_abandon=False,
            opendota_parsed=True,
        )

    def discover_parsed_public_matches(
        self,
        *,
        pages: int = 4,
        min_duration: int = 600,
    ) -> list[CandidateMatch]:
        """Discover recently parsed public matches (Ranked AP + Turbo) with hero rosters.

        Uses ``/api/parsedMatches`` (paginated via ``less_than_match_id``) followed
        by a batched ``public_matches`` lookup in ``/api/explorer`` so every returned
        match is both fresh (live Valve CDN replay) and already parsed by OpenDota.

        Args:
            pages: Number of 100-match pages to scan from ``/api/parsedMatches``.
            min_duration: Minimum match duration in seconds.

        Returns:
            List of :class:`CandidateMatch` records covering Ranked AP and Turbo matches.
        """
        match_ids = self._fetch_parsed_match_ids(pages)
        if not match_ids:
            return []

        candidates: list[CandidateMatch] = []
        chunk_size = 100
        for offset in range(0, len(match_ids), chunk_size):
            chunk = match_ids[offset : offset + chunk_size]
            id_csv = ",".join(str(mid) for mid in chunk)
            sql = (
                "SELECT match_id, duration, game_mode, lobby_type, start_time, "
                "radiant_team, dire_team "
                f"FROM public_matches WHERE match_id IN ({id_csv}) "
                f"AND duration >= {int(min_duration)} "
                "ORDER BY match_id DESC"
            )
            for row in self.explorer_query(sql):
                candidate = self._candidate_from_public_row(row)
                if candidate is not None:
                    candidates.append(candidate)
        return candidates


def select_diverse_candidates(
    candidates: Sequence[CandidateMatch],
    *,
    limit: int,
    existing_match_ids: set[int] | frozenset[int] = frozenset(),
    covered_heroes: set[int] | frozenset[int] = frozenset(),
    include_extremes: bool = True,
) -> list[CandidateMatch]:
    """Select up to ``limit`` candidates maximizing distinct hero and edge-case coverage.

    Args:
        candidates: Candidate pool to select from.
        limit: Maximum number of matches to return.
        existing_match_ids: Match IDs already present in the corpus (skipped).
        covered_heroes: Hero IDs already covered by existing corpus matches.
        include_extremes: When ``True`` and ``limit >= 3``, reserve initial slots for
            one shortest match, one longest match, and one abandon match when present.

    Returns:
        Selected :class:`CandidateMatch` items in selection order.
    """
    if limit <= 0:
        return []

    deduped: dict[int, CandidateMatch] = {}
    for candidate in candidates:
        if candidate.match_id in existing_match_ids:
            continue
        deduped.setdefault(candidate.match_id, candidate)

    remaining = list(deduped.values())
    if not remaining:
        return []

    chosen: list[CandidateMatch] = []
    seen_heroes = set(covered_heroes)

    def take(item: CandidateMatch) -> None:
        chosen.append(item)
        remaining.remove(item)
        seen_heroes.update(h for h in item.hero_ids if h > 0)

    if include_extremes and limit >= 3:
        dated = [c for c in remaining if c.duration is not None]
        if dated:
            take(min(dated, key=lambda c: (c.duration or 0, c.match_id)))
        dated = [c for c in remaining if c.duration is not None]
        if dated and len(chosen) < limit:
            take(max(dated, key=lambda c: (c.duration or 0, -c.match_id)))
        abandons = [c for c in remaining if c.has_abandon]
        if abandons and len(chosen) < limit:
            take(
                max(
                    abandons,
                    key=lambda c: (
                        len({h for h in c.hero_ids if h > 0} - seen_heroes),
                        c.duration or 0,
                        -c.match_id,
                    ),
                )
            )

    while remaining and len(chosen) < limit:
        best = max(
            remaining,
            key=lambda c: (
                len({h for h in c.hero_ids if h > 0} - seen_heroes),
                -(c.duration if c.duration is not None else 10**9),
                -c.match_id,
            ),
        )
        take(best)

    return chosen


def download_raw_archive(replay_url: str, *, timeout: int = 120) -> bytes:
    """Download the raw compressed replay archive from ``replay_url``.

    Args:
        replay_url: Valve CDN or mirror URL.
        timeout: Socket read timeout in seconds.

    Returns:
        Raw compressed archive bytes (bzip2 or Zstandard).
    """
    req = urllib.request.Request(replay_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=timeout) as resp:
        return resp.read()


def collect_match(
    candidate: CandidateMatch,
    *,
    bucket_uri: str,
    gcs: GcsClient,
    opendota: OpenDotaClient,
    existing_index: CorpusIndex,
    force: bool = False,
    note: str | None = None,
    archive_downloader: Callable[[str], bytes] = download_raw_archive,
) -> CollectionOutcome:
    """Fetch, verify, and upload one match archive + OpenDota JSON into GCS.

    Args:
        candidate: Match candidate metadata.
        bucket_uri: Normalized target bucket/prefix URI.
        gcs: Active :class:`GcsClient`.
        opendota: Active :class:`OpenDotaClient`.
        existing_index: Current corpus index (used to skip duplicates unless ``force``).
        force: Re-fetch and overwrite an existing corpus match when ``True``.
        note: Optional free-text note attached to the corpus entry.
        archive_downloader: Injectable download callable for testing.

    Returns:
        :class:`CollectionOutcome` describing whether the match was uploaded, skipped,
        or failed.
    """
    match_id = candidate.match_id
    if not force and match_id in existing_index.by_match_id:
        return CollectionOutcome(match_id, "skipped", "already in corpus/index.json")

    try:
        payload = opendota.fetch_match(match_id)
    except OpenDotaApiError as exc:
        return CollectionOutcome(match_id, "failed", str(exc))

    replay_url = payload.get("replay_url")
    if not isinstance(replay_url, str) or not replay_url:
        return CollectionOutcome(match_id, "failed", "OpenDota payload has no replay_url")

    try:
        archive_bytes = archive_downloader(replay_url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return CollectionOutcome(
            match_id, "failed", f"replay download failed ({replay_url}): {exc}"
        )

    try:
        dem_bytes = _decompress_replay(archive_bytes)
    except Exception as exc:
        return CollectionOutcome(match_id, "failed", f"replay decompression failed: {exc}")

    archive_sha256 = hashlib.sha256(archive_bytes).hexdigest()
    dem_sha256 = hashlib.sha256(dem_bytes).hexdigest()
    archive_object = f"matches/{match_id}.dem.bz2"
    opendota_object = f"matches/{match_id}.opendota.json"

    archive_uri = join_gcs_uri(bucket_uri, "corpus", archive_object)
    opendota_uri = join_gcs_uri(bucket_uri, "corpus", opendota_object)

    with tempfile.TemporaryDirectory(prefix="gem-collect-") as tmpdir:
        tmp_archive = Path(tmpdir) / f"{match_id}.dem.bz2"
        tmp_json = Path(tmpdir) / f"{match_id}.opendota.json"
        tmp_archive.write_bytes(archive_bytes)
        tmp_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        try:
            gcs.upload(tmp_archive, archive_uri)
            gcs.upload(tmp_json, opendota_uri)
        except GcsError as exc:
            return CollectionOutcome(match_id, "failed", f"GCS upload failed: {exc}")

    entry = CorpusEntry(
        match_id=match_id,
        source=candidate.source,
        tags=derive_match_tags(payload, extra_tags=candidate.tags),
        patch=payload.get("patch") if isinstance(payload.get("patch"), int) else None,
        lobby_type=payload.get("lobby_type")
        if isinstance(payload.get("lobby_type"), int)
        else None,
        game_mode=payload.get("game_mode") if isinstance(payload.get("game_mode"), int) else None,
        duration=payload.get("duration") if isinstance(payload.get("duration"), int) else None,
        has_abandon=payload_has_abandon(payload),
        hero_ids=payload_hero_ids(payload) or candidate.hero_ids,
        archive_object=archive_object,
        opendota_object=opendota_object,
        archive_size_bytes=len(archive_bytes),
        archive_sha256=archive_sha256,
        dem_size_bytes=len(dem_bytes),
        dem_sha256=dem_sha256,
        opendota_parsed=payload_is_parsed(payload),
        fetched_at=utc_now_iso(),
        note=note,
    )
    return CollectionOutcome(
        match_id,
        "uploaded",
        f"{len(archive_bytes) / (1024 * 1024):.1f} MB archive, tags={','.join(entry.tags)}",
        entry=entry,
    )


def mirror_manifest_fixtures(
    *,
    bucket_uri: str,
    gcs: GcsClient,
    manifest_path: Path = DEFAULT_MANIFEST,
    force: bool = False,
    dry_run: bool = False,
    archive_downloader: Callable[[str], bytes] = download_raw_archive,
) -> list[CollectionOutcome]:
    """Mirror active fixtures from ``manifest.json`` into ``gs://<bucket>/fixtures/``.

    Verifies each downloaded replay against the manifest's recorded decompressed
    size and SHA-256 before uploading the raw compressed archive.

    Args:
        bucket_uri: Normalized target bucket/prefix URI.
        gcs: Active :class:`GcsClient`.
        manifest_path: Path to ``tests/fixtures/opendota/manifest.json``.
        force: Re-upload fixtures that already exist in GCS when ``True``.
        dry_run: Report planned uploads without downloading or uploading.
        archive_downloader: Injectable download callable for testing.

    Returns:
        List of :class:`CollectionOutcome` records, one per active fixture.
    """
    specs: list[FixtureSpec] = [
        spec for spec in load_fixture_manifest(manifest_path) if spec.status == "active"
    ]
    outcomes: list[CollectionOutcome] = []
    for spec in specs:
        uri = join_gcs_uri(bucket_uri, "fixtures", f"{spec.match_id}.dem.bz2")
        if not force and gcs.exists(uri):
            outcomes.append(CollectionOutcome(spec.match_id, "skipped", f"already exists: {uri}"))
            continue
        if dry_run:
            outcomes.append(
                CollectionOutcome(spec.match_id, "skipped", f"dry-run: would upload {uri}")
            )
            continue
        if spec.source_url is None:
            outcomes.append(
                CollectionOutcome(spec.match_id, "failed", "manifest entry has no source_url")
            )
            continue
        try:
            archive_bytes = archive_downloader(spec.source_url)
            dem_bytes = _decompress_replay(archive_bytes)
        except Exception as exc:
            outcomes.append(
                CollectionOutcome(spec.match_id, "failed", f"download/decompress failed: {exc}")
            )
            continue
        if spec.dem_size_bytes is not None and len(dem_bytes) != spec.dem_size_bytes:
            outcomes.append(
                CollectionOutcome(
                    spec.match_id,
                    "failed",
                    f"decompressed size mismatch: expected {spec.dem_size_bytes}, got {len(dem_bytes)}",
                )
            )
            continue
        actual_sha = hashlib.sha256(dem_bytes).hexdigest()
        if spec.dem_sha256 is not None and actual_sha != spec.dem_sha256:
            outcomes.append(
                CollectionOutcome(
                    spec.match_id,
                    "failed",
                    f"decompressed SHA-256 mismatch: expected {spec.dem_sha256}, got {actual_sha}",
                )
            )
            continue
        with tempfile.TemporaryDirectory(prefix="gem-mirror-") as tmpdir:
            tmp_archive = Path(tmpdir) / f"{spec.match_id}.dem.bz2"
            tmp_archive.write_bytes(archive_bytes)
            try:
                gcs.upload(tmp_archive, uri)
            except GcsError as exc:
                outcomes.append(
                    CollectionOutcome(spec.match_id, "failed", f"GCS upload failed: {exc}")
                )
                continue
        outcomes.append(
            CollectionOutcome(
                spec.match_id,
                "uploaded",
                f"{len(archive_bytes) / (1024 * 1024):.1f} MB -> {uri}",
            )
        )
    return outcomes


def _format_plan(
    selected: Sequence[CandidateMatch],
    *,
    existing_heroes: set[int],
) -> str:
    added_heroes = {h for item in selected for h in item.hero_ids if h > 0} - existing_heroes
    by_source: dict[str, int] = {}
    for item in selected:
        by_source[item.source] = by_source.get(item.source, 0) + 1
    source_summary = ", ".join(f"{src}={count}" for src, count in sorted(by_source.items()))
    lines = [
        f"Selected {len(selected)} match(es) ({source_summary or 'none'})",
        f"Hero coverage: {len(existing_heroes)} existing -> "
        f"{len(existing_heroes | added_heroes)} (+{len(added_heroes)} new)",
    ]
    for item in selected:
        dur = f"{item.duration // 60}m" if item.duration is not None else "?m"
        tags = ",".join(item.tags)
        lines.append(f"  {item.match_id}  {item.source:14s}  {dur:>4s}  [{tags}]")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the corpus collector."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--bucket",
        help="GCS bucket or prefix URI (default: $GEM_CORPUS_BUCKET).",
    )
    parser.add_argument(
        "--check-bucket",
        action="store_true",
        help="Verify gcloud CLI auth and bucket access, then exit.",
    )
    parser.add_argument(
        "--league",
        dest="league_ids",
        action="append",
        type=int,
        default=[],
        help="OpenDota league ID to sample (repeatable, e.g. 20208 for BLAST SLAM IX).",
    )
    parser.add_argument(
        "--league-limit",
        type=int,
        default=35,
        help="Max matches to select per --league (default: 35).",
    )
    parser.add_argument(
        "--ranked-count",
        type=int,
        default=0,
        help="Number of parsed Ranked All Pick matches to select (default: 0).",
    )
    parser.add_argument(
        "--turbo-count",
        type=int,
        default=0,
        help="Number of parsed Turbo matches to select as smoke-only (default: 0).",
    )
    parser.add_argument(
        "--parsed-pages",
        type=int,
        default=4,
        help="Pages of 100 matches to scan from /api/parsedMatches (default: 4).",
    )
    parser.add_argument(
        "--ranked-min-duration",
        type=int,
        default=600,
        help="Minimum pub duration in seconds (default: 600).",
    )
    parser.add_argument(
        "--match",
        dest="match_ids",
        action="append",
        type=int,
        default=[],
        help="Explicit match ID to add (repeatable).",
    )
    parser.add_argument(
        "--tag",
        dest="extra_tags",
        action="append",
        default=[],
        help="Extra tag to apply to manual --match entries (repeatable).",
    )
    parser.add_argument("--note", help="Optional note attached to newly added corpus entries.")
    parser.add_argument(
        "--mirror-manifest",
        action="store_true",
        help="Mirror active tests/fixtures/opendota/manifest.json replays to gs://<bucket>/fixtures/.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Fixture manifest path used with --mirror-manifest.",
    )
    parser.add_argument(
        "--request-delay",
        type=float,
        default=1.1,
        help="Seconds between OpenDota API calls (default: 1.1).",
    )
    parser.add_argument(
        "--opendota-api-key",
        default=os.environ.get("OPENDOTA_API_KEY"),
        help="Optional OpenDota API key (default: $OPENDOTA_API_KEY).",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite matches already in GCS.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run discovery and selection without downloading replays or uploading.",
    )
    return parser.parse_args(argv)


def _select_requested_candidates(
    args: argparse.Namespace,
    *,
    opendota: OpenDotaClient,
    index: CorpusIndex,
) -> list[CandidateMatch]:
    existing_ids = set() if args.force else set(index.by_match_id)
    covered_heroes = index.covered_hero_ids()
    selected: list[CandidateMatch] = []

    def extend_from(
        pool: Sequence[CandidateMatch], *, limit: int, include_extremes: bool = True
    ) -> None:
        picked = select_diverse_candidates(
            pool,
            limit=limit,
            existing_match_ids=existing_ids | {c.match_id for c in selected},
            covered_heroes=covered_heroes,
            include_extremes=include_extremes,
        )
        selected.extend(picked)
        covered_heroes.update(h for c in picked for h in c.hero_ids if h > 0)

    for league_id in args.league_ids:
        extend_from(opendota.discover_league_matches(league_id), limit=args.league_limit)

    if args.ranked_count > 0 or args.turbo_count > 0:
        pub_pool = opendota.discover_parsed_public_matches(
            pages=args.parsed_pages,
            min_duration=args.ranked_min_duration,
        )
        if args.ranked_count > 0:
            extend_from([c for c in pub_pool if c.source == "ranked-ap"], limit=args.ranked_count)
        if args.turbo_count > 0:
            extend_from(
                [c for c in pub_pool if c.source == "turbo"],
                limit=args.turbo_count,
                include_extremes=False,
            )

    chosen_ids = existing_ids | {c.match_id for c in selected}
    for match_id in args.match_ids:
        if match_id in chosen_ids:
            continue
        chosen_ids.add(match_id)
        selected.append(
            CandidateMatch(
                match_id=match_id,
                source="manual",
                tags=tuple(args.extra_tags),
                duration=None,
                lobby_type=None,
                game_mode=None,
                hero_ids=(),
            )
        )
    return selected


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for collecting and mirroring GCS hardening replays."""
    args = parse_args(argv)
    try:
        bucket_uri = resolve_bucket(args.bucket)
        gcs = GcsClient()
        bucket_info = gcs.check_access(bucket_uri)
    except (ValueError, GcsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    location = bucket_info.get("location", "unknown")
    storage_class = (
        bucket_info.get("default_storage_class") or bucket_info.get("storage_class") or "unknown"
    )
    print(f"GCS OK: {bucket_uri} (location={location}, class={storage_class})", flush=True)
    if args.check_bucket:
        return 0

    exit_code = 0

    if args.mirror_manifest:
        mirror_outcomes = mirror_manifest_fixtures(
            bucket_uri=bucket_uri,
            gcs=gcs,
            manifest_path=args.manifest,
            force=args.force,
            dry_run=args.dry_run,
        )
        for outcome in mirror_outcomes:
            print(
                f"MIRROR [{outcome.status.upper()}] {outcome.match_id}: {outcome.detail}",
                flush=True,
            )
        if any(o.status == "failed" for o in mirror_outcomes):
            exit_code = 1

    wants_corpus = bool(
        args.league_ids or args.ranked_count > 0 or args.turbo_count > 0 or args.match_ids
    )
    if not wants_corpus:
        if not args.mirror_manifest:
            print(
                "Nothing to collect. Pass --league, --ranked-count, --turbo-count, "
                "--match, --mirror-manifest, or --check-bucket.",
                file=sys.stderr,
            )
            return 1
        return exit_code

    try:
        index = load_corpus_index_from_gcs(gcs, bucket_uri)
        opendota = OpenDotaClient(
            api_key=args.opendota_api_key,
            request_delay=args.request_delay,
        )
        selected = _select_requested_candidates(args, opendota=opendota, index=index)
    except (GcsError, ValueError, OpenDotaApiError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(_format_plan(selected, existing_heroes=index.covered_hero_ids()), flush=True)
    if args.dry_run:
        return exit_code

    index_uri = join_gcs_uri(bucket_uri, "corpus", "index.json")
    uploaded = 0
    failed = 0
    for candidate in selected:
        outcome = collect_match(
            candidate,
            bucket_uri=bucket_uri,
            gcs=gcs,
            opendota=opendota,
            existing_index=index,
            force=args.force,
            note=args.note,
        )
        print(f"CORPUS [{outcome.status.upper()}] {outcome.match_id}: {outcome.detail}", flush=True)
        if outcome.status == "uploaded" and outcome.entry is not None:
            index = index.upsert(outcome.entry)
            gcs.write_json(index_uri, index.to_dict())
            uploaded += 1
        elif outcome.status == "failed":
            failed += 1

    print(
        f"Done: {uploaded} uploaded, {failed} failed, "
        f"{len(index.matches)} total matches in {index_uri} "
        f"({len(index.covered_hero_ids())} distinct heroes)."
    )
    return 1 if failed > 0 else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
