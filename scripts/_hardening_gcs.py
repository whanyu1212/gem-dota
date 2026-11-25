"""Shared GCS storage and corpus-index helpers for pre-release hardening scripts.

Wraps the ``gcloud storage`` CLI via subprocess argument lists so no extra cloud
SDK dependency is required in ``gem``'s runtime or dev dependencies.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from sync_opendota_fixtures import file_sha256 as file_sha256  # noqa: E402

CORPUS_BUCKET_ENV = "GEM_CORPUS_BUCKET"
CORPUS_INDEX_SCHEMA_VERSION = 1
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "gem-corpus"


class GcsError(RuntimeError):
    """Raised when a ``gcloud storage`` command fails."""


class CorpusIndexError(ValueError):
    """Raised when a corpus index payload is invalid or incompatible."""


def normalize_bucket_uri(bucket: str) -> str:
    """Validate and normalize a GCS bucket or prefix URI to ``gs://...``.

    Args:
        bucket: Bucket name (``my-bucket``) or ``gs://`` URI with optional prefix.

    Returns:
        Normalized ``gs://bucket`` or ``gs://bucket/prefix`` URI with no trailing slash.

    Raises:
        ValueError: If ``bucket`` is empty, contains whitespace, or uses a non-GCS scheme.
    """
    cleaned = bucket.strip()
    if not cleaned:
        raise ValueError("GCS bucket URI must not be empty")
    if any(ch.isspace() for ch in cleaned):
        raise ValueError(f"GCS bucket URI must not contain whitespace: {bucket!r}")
    if "://" in cleaned:
        if not cleaned.startswith("gs://"):
            raise ValueError(f"Expected a gs:// URI, got: {bucket!r}")
        remainder = cleaned[len("gs://") :].rstrip("/")
    elif ":" in cleaned:
        raise ValueError(f"Invalid GCS bucket URI: {bucket!r}")
    else:
        remainder = cleaned.rstrip("/")
    bucket_name = remainder.split("/", 1)[0]
    if not bucket_name:
        raise ValueError(f"Missing bucket name in GCS URI: {bucket!r}")
    return f"gs://{remainder}"


def bucket_root_uri(bucket_uri: str) -> str:
    """Return the ``gs://<bucket>`` root for a normalized bucket or prefix URI.

    Args:
        bucket_uri: Bucket name or ``gs://`` URI with optional object prefix.

    Returns:
        The ``gs://<bucket>`` root URI without any object path.
    """
    normalized = normalize_bucket_uri(bucket_uri)
    bucket_name = normalized[len("gs://") :].split("/", 1)[0]
    return f"gs://{bucket_name}"


def resolve_bucket(bucket: str | None) -> str:
    """Resolve the GCS bucket URI from an explicit CLI argument or environment variable.

    Args:
        bucket: Explicit ``--bucket`` argument value, or ``None`` to read
            :data:`CORPUS_BUCKET_ENV`.

    Returns:
        Normalized ``gs://...`` URI.

    Raises:
        ValueError: If neither ``bucket`` nor ``GEM_CORPUS_BUCKET`` is provided.
    """
    raw = bucket or os.environ.get(CORPUS_BUCKET_ENV)
    if not raw:
        raise ValueError(f"GCS bucket not configured; pass --bucket or set {CORPUS_BUCKET_ENV}")
    return normalize_bucket_uri(raw)


def join_gcs_uri(base: str, *parts: str) -> str:
    """Join relative path segments onto a normalized ``gs://`` URI.

    Args:
        base: Base ``gs://`` URI.
        *parts: Relative path segments to append.

    Returns:
        Combined ``gs://`` URI.
    """
    root = normalize_bucket_uri(base)
    cleaned = [part.strip("/") for part in parts if part and part.strip("/")]
    return "/".join([root, *cleaned])


class GcsClient:
    """Minimal GCS client backed by the ``gcloud storage`` CLI."""

    def __init__(self, gcloud_bin: str = "gcloud", *, timeout: int = 300) -> None:
        self.gcloud_bin = gcloud_bin
        self.timeout = timeout

    def _run(self, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
        cmd = [self.gcloud_bin, *args]
        env = dict(os.environ)
        # Keep uploads atomic: avoid orphaned gcloud/tmp/parallel_composite_uploads/ chunks on interrupt.
        env.setdefault("CLOUDSDK_STORAGE_PARALLEL_COMPOSITE_UPLOAD_ENABLED", "False")
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
                env=env,
            )
        except FileNotFoundError as exc:
            raise GcsError(
                f"gcloud CLI not found ({self.gcloud_bin!r}); install Google Cloud SDK first"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise GcsError(
                f"gcloud command timed out after {self.timeout}s: {' '.join(cmd)}"
            ) from exc
        if check and proc.returncode != 0:
            detail = proc.stderr.strip() or proc.stdout.strip() or f"exit code {proc.returncode}"
            raise GcsError(f"gcloud command failed ({' '.join(cmd)}): {detail}")
        return proc

    def check_access(self, bucket_uri: str) -> dict[str, Any]:
        """Verify that the active gcloud credentials can describe ``bucket_uri``.

        Args:
            bucket_uri: Target bucket or prefix URI.

        Returns:
            Parsed bucket metadata dictionary from ``gcloud storage buckets describe``.
        """
        root = bucket_root_uri(bucket_uri)
        proc = self._run(["storage", "buckets", "describe", root, "--format=json"])
        payload = json.loads(proc.stdout or "{}")
        if not isinstance(payload, dict):
            raise GcsError(f"Unexpected bucket describe payload for {root}")
        return payload

    def exists(self, uri: str) -> bool:
        """Return whether an object exists at ``uri``.

        Args:
            uri: Full ``gs://`` object URI.

        Returns:
            ``True`` when the object exists, ``False`` when absent.

        Raises:
            GcsError: If ``gcloud`` fails for a reason other than missing object.
        """
        proc = self._run(["storage", "ls", uri], check=False)
        if proc.returncode == 0:
            return True
        stderr_lower = proc.stderr.lower()
        if "matched no objects" in stderr_lower or "not found" in stderr_lower:
            return False
        detail = proc.stderr.strip() or proc.stdout.strip() or f"exit code {proc.returncode}"
        raise GcsError(f"gcloud storage ls failed for {uri}: {detail}")

    def download(self, uri: str, dest: Path) -> Path:
        """Atomically download a GCS object to ``dest``.

        Args:
            uri: Source ``gs://`` object URI.
            dest: Local destination file path.

        Returns:
            ``dest`` after atomic replacement.
        """
        dest.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=f".{dest.name}.", dir=dest.parent)
        os.close(fd)
        tmp_path = Path(tmp_name)
        try:
            self._run(["storage", "cp", uri, str(tmp_path)])
            tmp_path.replace(dest)
        except Exception:
            tmp_path.unlink(missing_ok=True)
            raise
        return dest

    def upload(self, src: Path, uri: str) -> None:
        """Upload a local file to ``uri``.

        Args:
            src: Local source file path.
            uri: Destination ``gs://`` object URI.
        """
        self._run(["storage", "cp", str(src), uri])

    def read_json(self, uri: str) -> Any:
        """Read and decode a JSON object directly from GCS.

        Args:
            uri: Source ``gs://`` object URI.

        Returns:
            Decoded JSON value.
        """
        proc = self._run(["storage", "cat", uri])
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise GcsError(f"Invalid JSON at {uri}: {exc}") from exc

    def write_json(self, uri: str, payload: Any) -> None:
        """Serialize ``payload`` as indented JSON and upload it to ``uri``.

        Args:
            uri: Destination ``gs://`` object URI.
            payload: JSON-serializable object.
        """
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        with tempfile.TemporaryDirectory(prefix="gem-gcs-json-") as tmpdir:
            local = Path(tmpdir) / "payload.json"
            local.write_text(text, encoding="utf-8")
            self.upload(local, uri)


@dataclass(frozen=True, slots=True)
class CorpusEntry:
    """Metadata record for one match stored in a GCS hardening corpus."""

    match_id: int
    source: str
    tags: tuple[str, ...]
    patch: int | None
    lobby_type: int | None
    game_mode: int | None
    duration: int | None
    has_abandon: bool
    hero_ids: tuple[int, ...]
    archive_object: str
    opendota_object: str
    archive_size_bytes: int
    archive_sha256: str
    dem_size_bytes: int
    dem_sha256: str
    opendota_parsed: bool
    fetched_at: str
    note: str | None = None

    @property
    def parity_eligible(self) -> bool:
        """Return whether this match should participate in OpenDota parity scoring."""
        return self.opendota_parsed and "smoke-only" not in self.tags

    def to_dict(self) -> dict[str, Any]:
        """Convert the entry into a JSON-serializable dictionary."""
        return {
            "match_id": self.match_id,
            "source": self.source,
            "tags": list(self.tags),
            "patch": self.patch,
            "lobby_type": self.lobby_type,
            "game_mode": self.game_mode,
            "duration": self.duration,
            "has_abandon": self.has_abandon,
            "hero_ids": list(self.hero_ids),
            "archive_object": self.archive_object,
            "opendota_object": self.opendota_object,
            "archive_size_bytes": self.archive_size_bytes,
            "archive_sha256": self.archive_sha256,
            "dem_size_bytes": self.dem_size_bytes,
            "dem_sha256": self.dem_sha256,
            "opendota_parsed": self.opendota_parsed,
            "fetched_at": self.fetched_at,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, raw: object) -> CorpusEntry:
        """Parse and validate a :class:`CorpusEntry` from a raw JSON dict.

        Args:
            raw: Decoded JSON object.

        Returns:
            Validated :class:`CorpusEntry`.

        Raises:
            CorpusIndexError: When required fields are missing or malformed.
        """
        if not isinstance(raw, dict):
            raise CorpusIndexError("Corpus entry must be a JSON object")
        match_id = raw.get("match_id")
        if not isinstance(match_id, int) or isinstance(match_id, bool) or match_id <= 0:
            raise CorpusIndexError(f"Invalid match_id in corpus entry: {match_id!r}")
        raw_tags = raw.get("tags", [])
        if not isinstance(raw_tags, list) or not all(isinstance(t, str) and t for t in raw_tags):
            raise CorpusIndexError(f"Match {match_id}: tags must be a list of non-empty strings")
        raw_heroes = raw.get("hero_ids", [])
        if not isinstance(raw_heroes, list) or not all(
            isinstance(h, int) and not isinstance(h, bool) for h in raw_heroes
        ):
            raise CorpusIndexError(f"Match {match_id}: hero_ids must be a list of integers")
        for key in (
            "source",
            "archive_object",
            "opendota_object",
            "archive_sha256",
            "dem_sha256",
            "fetched_at",
        ):
            value = raw.get(key)
            if not isinstance(value, str) or not value:
                raise CorpusIndexError(f"Match {match_id}: {key} must be a non-empty string")
        for key in ("archive_size_bytes", "dem_size_bytes"):
            value = raw.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise CorpusIndexError(f"Match {match_id}: {key} must be a positive integer")
        return cls(
            match_id=match_id,
            source=raw["source"],
            tags=tuple(sorted(set(raw_tags))),
            patch=raw.get("patch"),
            lobby_type=raw.get("lobby_type"),
            game_mode=raw.get("game_mode"),
            duration=raw.get("duration"),
            has_abandon=bool(raw.get("has_abandon", False)),
            hero_ids=tuple(raw_heroes),
            archive_object=raw["archive_object"],
            opendota_object=raw["opendota_object"],
            archive_size_bytes=raw["archive_size_bytes"],
            archive_sha256=raw["archive_sha256"],
            dem_size_bytes=raw["dem_size_bytes"],
            dem_sha256=raw["dem_sha256"],
            opendota_parsed=bool(raw.get("opendota_parsed", False)),
            fetched_at=raw["fetched_at"],
            note=raw.get("note"),
        )


@dataclass(frozen=True, slots=True)
class CorpusIndex:
    """Top-level manifest for ``gs://<bucket>/corpus/index.json``."""

    matches: tuple[CorpusEntry, ...] = ()
    schema_version: int = CORPUS_INDEX_SCHEMA_VERSION

    @property
    def by_match_id(self) -> dict[int, CorpusEntry]:
        """Return entries indexed by ``match_id``."""
        return {entry.match_id: entry for entry in self.matches}

    def covered_hero_ids(self) -> set[int]:
        """Return all non-zero hero IDs represented across the corpus."""
        return {hero_id for entry in self.matches for hero_id in entry.hero_ids if hero_id > 0}

    def upsert(self, entry: CorpusEntry) -> CorpusIndex:
        """Return a new index with ``entry`` inserted or replaced, sorted by ``match_id``."""
        updated = self.by_match_id
        updated[entry.match_id] = entry
        ordered = tuple(updated[mid] for mid in sorted(updated))
        return CorpusIndex(matches=ordered, schema_version=self.schema_version)

    def filter_entries(
        self,
        *,
        tags: Iterable[str] = (),
        exclude_tags: Iterable[str] = (),
        patches: Iterable[int] = (),
        match_ids: Iterable[int] = (),
        limit: int | None = None,
    ) -> list[CorpusEntry]:
        """Filter corpus entries deterministically by tags, patch, match IDs, and limit.

        Args:
            tags: If non-empty, an entry must carry at least one of these tags.
            exclude_tags: Entries carrying any of these tags are excluded.
            patches: If non-empty, keep only entries whose ``patch`` is in this set.
            match_ids: If non-empty, keep only entries with these exact match IDs.
            limit: Optional cap on returned entries.

        Returns:
            Filtered entries in ascending ``match_id`` order.
        """
        tag_set = set(tags)
        exclude_set = set(exclude_tags)
        patch_set = set(patches)
        id_set = set(match_ids)

        selected: list[CorpusEntry] = []
        for entry in self.matches:
            if id_set and entry.match_id not in id_set:
                continue
            if tag_set and not (tag_set & set(entry.tags)):
                continue
            if exclude_set and (exclude_set & set(entry.tags)):
                continue
            if patch_set and entry.patch not in patch_set:
                continue
            selected.append(entry)
        if limit is not None:
            return selected[:limit]
        return selected

    def to_dict(self) -> dict[str, Any]:
        """Convert the index to a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "matches": [entry.to_dict() for entry in self.matches],
        }

    @classmethod
    def from_dict(cls, raw: object) -> CorpusIndex:
        """Parse and validate a :class:`CorpusIndex` from decoded JSON.

        Args:
            raw: Decoded JSON object.

        Returns:
            Validated :class:`CorpusIndex`.

        Raises:
            CorpusIndexError: If schema version or match entries are invalid.
        """
        if not isinstance(raw, dict):
            raise CorpusIndexError("Corpus index root must be a JSON object")
        version = raw.get("schema_version")
        if version != CORPUS_INDEX_SCHEMA_VERSION:
            raise CorpusIndexError(
                f"Unsupported corpus index schema_version {version!r}; "
                f"expected {CORPUS_INDEX_SCHEMA_VERSION}"
            )
        raw_matches = raw.get("matches")
        if not isinstance(raw_matches, list):
            raise CorpusIndexError("Corpus index 'matches' must be a list")
        entries = [CorpusEntry.from_dict(item) for item in raw_matches]
        ids = [entry.match_id for entry in entries]
        if len(ids) != len(set(ids)):
            raise CorpusIndexError("Corpus index contains duplicate match_id values")
        ordered = tuple(sorted(entries, key=lambda entry: entry.match_id))
        return cls(matches=ordered, schema_version=CORPUS_INDEX_SCHEMA_VERSION)


def load_corpus_index_from_gcs(client: GcsClient, bucket_uri: str) -> CorpusIndex:
    """Load ``corpus/index.json`` from GCS, returning an empty index when absent.

    Args:
        client: Active :class:`GcsClient`.
        bucket_uri: Normalized bucket or prefix URI.

    Returns:
        Existing :class:`CorpusIndex`, or an empty index when not yet initialized.
    """
    index_uri = join_gcs_uri(bucket_uri, "corpus", "index.json")
    if not client.exists(index_uri):
        return CorpusIndex()
    return CorpusIndex.from_dict(client.read_json(index_uri))
