"""Utilities for downloading and decompressing Dota 2 replay files.

Fetches replay URLs from the OpenDota API and downloads ``.dem.bz2`` files
from the Valve CDN, decompressing them to ``.dem`` files ready for parsing.

Example::

    from gem.replay_fetch import fetch_replay

    dem_path = fetch_replay(8734577999, out_dir="replays/")
    match = gem.parse(str(dem_path))
"""

from __future__ import annotations

import bz2
import json
import ssl
import urllib.request
from pathlib import Path

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
        ValueError: If OpenDota returns no replay URL for the match.
        urllib.error.URLError: If the API request fails.
    """
    url = f"{OPENDOTA_API}/{match_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "gem/1.0"})
    with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=20) as resp:
        data = json.loads(resp.read())

    replay_url = data.get("replay_url")
    if not replay_url:
        raise ValueError(
            f"OpenDota returned no replay_url for match {match_id}. "
            "The match may not have been ingested yet. "
            f"Force a parse with: curl -X POST {OPENDOTA_API.replace('/matches', '')}/request/{match_id}"
        )
    return replay_url


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
    with urllib.request.urlopen(req, context=_SSL_CONTEXT) as resp:
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
