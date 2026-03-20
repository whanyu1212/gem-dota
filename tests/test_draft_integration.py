"""Integration tests: draft extraction vs OpenDota API reference.

For each configured captains-mode match:
1. Fetch match metadata + picks_bans from OpenDota API.
2. Download and decompress the replay from the CDN URL in ``replay_url``.
3. Parse with gem, call ``DraftExtractor.finalize()``.
4. Compare gem's draft (hero NPC names) against OpenDota's ``picks_bans``
   (resolved via ``/api/heroes`` id → npc_name map).
   - Bans: verified via picks_bans (hero_id → npc_name).
   - Picks: verified via picks_bans AND cross-checked against npc_dota_hero_*
     names that appear in the OD match response (combat stats keys), since
     picks appear as hero NPC name keys in fields like ``killed``, ``ability_uses``.
5. Delete the ``.dem`` file immediately to save disk space.

Run with::

    pytest tests/test_draft_integration.py -m integration -v

Requires network access and ~500 MB of free disk space per match (temporary).
"""

from __future__ import annotations

import bz2
import json
import ssl
import tempfile
import urllib.request
from pathlib import Path

import pytest

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

OPENDOTA_API = "https://api.opendota.com/api/matches"

# Five recent captains-mode pro matches with known replay URLs.
MATCH_IDS = [
    8735903160,
    8735881600,
    8735854783,
    8735821683,
    8735819319,
]


# ---------------------------------------------------------------------------
# Helpers (mirrors scripts/fetch_replays.py + scripts/fetch_hero_npc_names.py)
# ---------------------------------------------------------------------------


def _fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "gem/1.0"})
    with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=30) as resp:
        return json.loads(resp.read())


def _build_od_hero_id_map() -> dict[int, str]:
    """Return OpenDota hero_id → npc_name from /api/heroes."""
    heroes = _fetch_json("https://api.opendota.com/api/heroes")
    return {h["id"]: h["name"] for h in heroes}


def _download_and_decompress(replay_url: str, dest: Path) -> None:
    req = urllib.request.Request(replay_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=120) as resp:
        compressed = resp.read()
    dest.write_bytes(bz2.decompress(compressed))


def _scan_npc_heroes(obj: object, found: set[str]) -> None:
    """Recursively collect npc_dota_hero_* keys/values from a JSON object.

    Picks appear as NPC name keys in per-player combat stat fields like
    ``killed``, ``ability_uses``, ``item_uses`` in the OD match response.
    Bans never appear here — they must be verified via picks_bans + hero ID map.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.startswith("npc_dota_hero_"):
                found.add(k)
            _scan_npc_heroes(v, found)
    elif isinstance(obj, list):
        for item in obj:
            _scan_npc_heroes(item, found)
    elif isinstance(obj, str) and obj.startswith("npc_dota_hero_"):
        found.add(obj)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def od_hero_id_map() -> dict[int, str]:
    """OpenDota hero_id → npc_name, fetched once per test module."""
    return _build_od_hero_id_map()


# ---------------------------------------------------------------------------
# Parametrized integration test
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize("match_id", MATCH_IDS)
def test_draft_matches_opendota(match_id: int, od_hero_id_map: dict[int, str]) -> None:
    """gem draft picks/bans must match OpenDota picks_bans for a captains-mode match."""
    from gem.extractors.draft import DraftExtractor
    from gem.parser import ReplayParser

    # --- Fetch OpenDota match data ---
    od = _fetch_json(f"{OPENDOTA_API}/{match_id}")

    assert od.get("game_mode") == 2, (
        f"Match {match_id} is not captains mode (game_mode={od.get('game_mode')})"
    )

    replay_url = od.get("replay_url")
    assert replay_url, f"Match {match_id} has no replay_url — may not be ingested yet"

    picks_bans = od.get("picks_bans") or []
    assert len(picks_bans) == 24, f"Expected 24 draft actions, got {len(picks_bans)}"

    # Resolve picks and bans from picks_bans via hero ID map.
    # Both picks and bans are verified this way — bans have no NPC name presence
    # in the OD response outside of picks_bans.
    od_picks = {od_hero_id_map[pb["hero_id"]] for pb in picks_bans if pb["is_pick"]}
    od_bans = {od_hero_id_map[pb["hero_id"]] for pb in picks_bans if not pb["is_pick"]}

    # Cross-check: collect npc_dota_hero_* names that appear in OD combat stats.
    # These are picks only (played heroes show up as keys in killed/ability_uses/etc).
    # gem picks must be a subset of these — if a gem pick is absent here it means
    # gem resolved the wrong hero.
    od_npc_in_response: set[str] = set()
    _scan_npc_heroes(od, od_npc_in_response)

    # --- Download, decompress, parse, delete ---
    with tempfile.TemporaryDirectory() as tmpdir:
        dem_path = Path(tmpdir) / f"{match_id}.dem"

        _download_and_decompress(replay_url, dem_path)
        assert dem_path.exists(), "Failed to create .dem file"

        p = ReplayParser(str(dem_path))
        draft_ext = DraftExtractor()
        draft_ext.attach(p)
        p.parse()
        draft_ext.finalize()

        # dem_path is deleted automatically when tmpdir context exits

    # --- Compare ---
    events = sorted(draft_ext.draft_events, key=lambda e: e.tick)
    assert len(events) == 24, f"Match {match_id}: expected 24 draft events, got {len(events)}"

    gem_picks = {e.hero_name for e in events if e.is_pick}
    gem_bans = {e.hero_name for e in events if not e.is_pick}

    missing_picks = od_picks - gem_picks
    extra_picks = gem_picks - od_picks
    missing_bans = od_bans - gem_bans
    extra_bans = gem_bans - od_bans

    assert not missing_picks, f"Match {match_id}: gem missing picks: {missing_picks}"
    assert not extra_picks, f"Match {match_id}: gem has extra picks: {extra_picks}"
    assert not missing_bans, f"Match {match_id}: gem missing bans: {missing_bans}"
    assert not extra_bans, f"Match {match_id}: gem has extra bans: {extra_bans}"

    # Cross-check: every gem pick must appear in OD combat stats as an NPC name key.
    # Bans are excluded here — they have no in-game entity so no combat stat keys.
    picks_not_in_response = gem_picks - od_npc_in_response
    assert not picks_not_in_response, (
        f"Match {match_id}: gem picks not found in OD combat stats "
        f"(wrong hero resolved?): {picks_not_in_response}"
    )
