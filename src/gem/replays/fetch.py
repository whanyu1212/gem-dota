"""Utilities for downloading and decompressing Dota 2 replay files.

Fetches replay URLs from the OpenDota API and downloads ``.dem.bz2`` files
from the Valve CDN, decompressing them to ``.dem`` files ready for parsing.
Valve serves both bzip2 and Zstandard archives under the ``.bz2`` extension,
so the format is detected from the payload's magic bytes rather than the name.

Example::

    from gem.replays.fetch import fetch_replay

    dem_path = fetch_replay(8734577999, out_dir="replays/")
    match = gem.parse(str(dem_path))
"""

from __future__ import annotations

import bz2
import io
import json
import ssl
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

OPENDOTA_API = "https://api.opendota.com/api/matches"

# Relax SSL verification for CDN hosts that occasionally present cert issues.
_SSL_CONTEXT = ssl.create_default_context()
_SSL_CONTEXT.check_hostname = False
_SSL_CONTEXT.verify_mode = ssl.CERT_NONE


def fetch_replay_url(match_id: int) -> str:
    """Fetch the replay download URL for a match from the OpenDota API.

    Args:
        match_id: Steam match ID.

    Returns:
        The ``replay_url`` string from the OpenDota API response.

    Raises:
        ValueError: If OpenDota returns no replay URL or a non-JSON response.
        urllib.error.URLError: If the API request fails.
    """
    url = f"{OPENDOTA_API}/{match_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "gem/1.0"})
    with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=20) as resp:
        raw = resp.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"OpenDota returned a non-JSON response for match {match_id} ({url})"
        ) from exc

    replay_url = data.get("replay_url")
    if not replay_url:
        raise ValueError(
            f"OpenDota returned no replay_url for match {match_id}. "
            "The match may not have been ingested yet. "
            f"Force a parse with: curl -X POST {OPENDOTA_API.replace('/matches', '')}/request/{match_id}"
        )
    return replay_url


# Valve serves both formats under the same ``.dem.bz2`` URL (the switch to
# Zstandard landed mid-2026), so the extension does not identify the archive.
_BZIP2_MAGIC = b"BZh"
_ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"


def _decompress_replay(payload: bytes) -> bytes:
    """Decompress a downloaded replay archive, detecting its format.

    Args:
        payload: Raw bytes of the downloaded ``.dem.bz2`` archive, which may be
            either a bzip2 or a Zstandard stream.

    Returns:
        The decompressed ``.dem`` bytes.

    Raises:
        RuntimeError: If the payload is Zstandard but the ``zstandard`` package
            is unavailable, or if the payload is in neither known format.
    """
    if payload.startswith(_BZIP2_MAGIC):
        return bz2.decompress(payload)
    if payload.startswith(_ZSTD_MAGIC):
        try:
            import zstandard
        except ImportError as exc:  # pragma: no cover - depends on install extras
            raise RuntimeError(
                "Replay archive is Zstandard-compressed but the 'zstandard' package "
                "is not installed. Install it with: pip install zstandard"
            ) from exc
        # stream_reader avoids the one-shot decompress() size cap: replay frames
        # do not carry a content-size header.
        with zstandard.ZstdDecompressor().stream_reader(io.BytesIO(payload)) as reader:
            return reader.read()
    raise RuntimeError(
        f"Replay archive is neither bzip2 nor Zstandard (magic bytes: {payload[:4].hex(' ')})"
    )


def download_and_decompress(match_id: int, replay_url: str, out_dir: Path | str = ".") -> Path:
    """Download and decompress a replay .dem.bz2 to out_dir/<match_id>.dem.

    Args:
        match_id: Steam match ID (used for the output filename).
        replay_url: Direct URL to the ``.dem.bz2`` file.
        out_dir: Directory to write the decompressed ``.dem`` file into.
            Defaults to the current working directory.

    Returns:
        Path to the decompressed ``.dem`` file.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dem_path = out_dir / f"{match_id}.dem"
    bz2_path = out_dir / f"{match_id}.dem.bz2"

    req = urllib.request.Request(replay_url, headers={"User-Agent": "Mozilla/5.0"})
    # Larger timeout than the JSON API calls: a full replay is 100-300 MB.
    with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=120) as resp:
        bz2_path.write_bytes(resp.read())

    dem_path.write_bytes(_decompress_replay(bz2_path.read_bytes()))
    bz2_path.unlink()

    return dem_path


def fetch_replay(match_id: int, out_dir: Path | str = ".") -> Path:
    """Fetch, download, and decompress a replay in one call.

    Convenience wrapper that calls :func:`fetch_replay_url` then
    :func:`download_and_decompress`. Skips the download if the ``.dem``
    file already exists.

    Args:
        match_id: Steam match ID.
        out_dir: Directory to save the ``.dem`` file. Defaults to ``"."``.

    Returns:
        Path to the decompressed ``.dem`` file.
    """
    out_dir = Path(out_dir)
    dem_path = out_dir / f"{match_id}.dem"

    if dem_path.exists():
        return dem_path

    replay_url = fetch_replay_url(match_id)
    return download_and_decompress(match_id, replay_url, out_dir)


def _opendota_slot_to_player_id(player_slot: int) -> int:
    """Map an OpenDota ``player_slot`` (Radiant 0-4, Dire 128-132) to id 0-9."""
    return player_slot if player_slot < 128 else (player_slot - 128) + 5


def apply_api_rates(match: ParsedMatch, opendota_match: dict) -> ParsedMatch:
    """Apply API-sourced rates, totals, and combat scalars to a parsed match.

    Complete replays already expose these Game Coordinator values through their
    embedded ``CMsgDOTAMatch`` postgame summary. This helper remains useful as an
    explicit override or as a fallback for older/truncated replays: it maps
    per-player rates and combat scalars from an OpenDota/Steam response and
    derives ``total_gold``/``total_xp`` with OpenDota's exact formula
    ``floor(rate * duration / 60)``. The pure mapping stays separate from the
    network call so it can be tested against fixtures offline.

    Players are matched by OpenDota ``player_slot`` (Radiant 0-4, Dire 128-132).
    Missing API fields leave the corresponding parsed values unchanged.

    Args:
        match: A :class:`~gem.results.models.ParsedMatch` to enrich in place.
        opendota_match: A decoded OpenDota ``/matches/{id}`` JSON object (or a
            Steam ``GetMatchDetails`` ``result`` with the same per-player fields).

    Returns:
        The same ``match`` instance, enriched.
    """
    duration = opendota_match.get("duration") or match.duration or 0
    by_id = {pp.player_id: pp for pp in match.players}
    for od_player in opendota_match.get("players") or []:
        slot = od_player.get("player_slot")
        if slot is None:
            continue
        pp = by_id.get(_opendota_slot_to_player_id(slot))
        if pp is None:
            continue
        gpm = od_player.get("gold_per_min")
        xpm = od_player.get("xp_per_min")
        if gpm is not None:
            pp.gold_per_min = int(gpm)
            pp.total_gold = (pp.gold_per_min * duration) // 60
        if xpm is not None:
            pp.xp_per_min = int(xpm)
            pp.total_xp = (pp.xp_per_min * duration) // 60
        # Exact combat scalars overwrite gem's combat-log reconstruction.
        for attr in ("hero_damage", "tower_damage", "hero_healing"):
            value = od_player.get(attr)
            if value is not None:
                setattr(pp, attr, int(value))
    return match


def fetch_opendota_match(match_id: int) -> dict:
    """Fetch the full OpenDota ``/matches/{id}`` JSON for a match.

    Args:
        match_id: Steam match ID.

    Returns:
        The decoded OpenDota match JSON object.

    Raises:
        ValueError: If OpenDota returns a non-JSON response.
        urllib.error.URLError: If the API request fails.
    """
    url = f"{OPENDOTA_API}/{match_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "gem/1.0"})
    with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=20) as resp:
        raw = resp.read()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"OpenDota returned a non-JSON response for match {match_id} ({url})"
        ) from exc


def enrich_with_api_rates(match: ParsedMatch, match_id: int) -> ParsedMatch:
    """Fetch OpenDota match scalars and apply them to a parsed match.

    Opt-in API override/fallback for ``gold_per_min``, ``xp_per_min``, derived
    totals, and headline combat scalars. ``gem.parse`` never makes network calls;
    on complete current replays it normally obtains the same values from the
    embedded postgame summary. This is a thin wrapper over
    :func:`fetch_opendota_match` plus :func:`apply_api_rates`.

    Args:
        match: A parsed match to enrich in place.
        match_id: Steam match ID to fetch rates for.

    Returns:
        The same ``match`` instance, enriched.

    Raises:
        urllib.error.URLError: If the API request fails.
    """
    return apply_api_rates(match, fetch_opendota_match(match_id))
