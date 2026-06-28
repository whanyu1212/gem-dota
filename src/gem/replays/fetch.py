"""Utilities for downloading and decompressing Dota 2 replay files.

Fetches replay URLs from the OpenDota API and downloads ``.dem.bz2`` files
from the Valve CDN, decompressing them to ``.dem`` files ready for parsing.

Example::

    from gem.replays.fetch import fetch_replay

    dem_path = fetch_replay(8734577999, out_dir="replays/")
    match = gem.parse(str(dem_path))
"""

from __future__ import annotations

import bz2
import json
import ssl
import urllib.parse
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

OPENDOTA_API = "https://api.opendota.com/api/matches"

# Use the platform trust store and hostname verification for OpenDota/CDN HTTPS.
_SSL_CONTEXT = ssl.create_default_context()


def _normalize_replay_url(replay_url: str) -> str:
    """Return an HTTPS replay URL, upgrading known Valve replay hosts."""
    parsed = urllib.parse.urlsplit(replay_url)
    scheme = parsed.scheme.lower()
    if scheme == "https":
        return replay_url

    host = (parsed.hostname or "").lower()
    if scheme == "http" and host.startswith("replay") and host.endswith(".valve.net"):
        return urllib.parse.urlunsplit(
            ("https", parsed.netloc, parsed.path, parsed.query, parsed.fragment)
        )

    raise ValueError(f"Replay download URL must use HTTPS: {replay_url}")


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
    if not isinstance(replay_url, str):
        raise ValueError(f"OpenDota returned a non-string replay_url for match {match_id}")
    return _normalize_replay_url(replay_url)


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

    replay_url = _normalize_replay_url(replay_url)
    req = urllib.request.Request(replay_url, headers={"User-Agent": "Mozilla/5.0"})
    # Larger timeout than the JSON API calls: a full replay is 100-300 MB.
    with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=120) as resp:
        bz2_path.write_bytes(resp.read())

    dem_path.write_bytes(bz2.decompress(bz2_path.read_bytes()))
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
    """Populate API-sourced per-minute rates and totals on a parsed match.

    ``gold_per_min``/``xp_per_min`` are not present in the replay — they come from
    the Steam GC match summary (also exposed by the OpenDota match API). This
    helper maps those per-player rates onto :class:`~gem.results.models.ParsedPlayer`
    and derives ``total_gold``/``total_xp`` with OpenDota's exact formula
    ``floor(rate * duration / 60)``. The pure mapping is kept separate from the
    network call so it can be tested against fixtures offline.

    Players are matched by OpenDota ``player_slot`` (Radiant 0-4, Dire 128-132).
    Missing rates leave the corresponding fields at ``0``.

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
    """Fetch OpenDota match rates and apply them to a parsed match.

    Opt-in enrichment for the API-only fields (``gold_per_min``, ``xp_per_min``,
    ``total_gold``, ``total_xp``). ``gem.parse`` never makes network calls and
    leaves these at ``0``; call this afterwards to fill them from the OpenDota
    match API (keyless). Thin wrapper over :func:`fetch_opendota_match` plus
    :func:`apply_api_rates`.

    Args:
        match: A parsed match to enrich in place.
        match_id: Steam match ID to fetch rates for.

    Returns:
        The same ``match`` instance, enriched.

    Raises:
        urllib.error.URLError: If the API request fails.
    """
    return apply_api_rates(match, fetch_opendota_match(match_id))
