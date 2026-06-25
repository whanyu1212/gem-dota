"""Player-name helpers for report rendering."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from gem.results.models import ParsedMatch, ParsedPlayer


def is_displayable_player_name(name: str | None) -> bool:
    """Return whether a replay/API player name is suitable for report display."""
    if not name:
        return False
    stripped = name.strip()
    if not stripped or "\ufffd" in stripped:
        return False
    return stripped.isprintable()


def display_player_name(player: ParsedPlayer | None) -> str:
    """Return the player name to show in reports, or ``""`` when unavailable."""
    if player is None or not is_displayable_player_name(player.player_name):
        return ""
    return player.player_name.strip()


def apply_opendota_player_names(
    match: ParsedMatch,
    opendota_match: Mapping[str, Any],
    *,
    overwrite: bool = True,
) -> ParsedMatch:
    """Apply clean OpenDota player display names to a parsed match.

    Replay ``CDOTA_PlayerResource`` names can occasionally contain binary-looking
    payloads. OpenDota match JSON carries the public ``personaname`` for the same
    player slots, so reports can use that sidecar data when callers have it.
    """
    players_by_id = {player.player_id: player for player in match.players}
    for od_player in opendota_match.get("players") or []:
        if not isinstance(od_player, Mapping):
            continue
        player_slot = od_player.get("player_slot")
        if not isinstance(player_slot, int):
            continue
        player = players_by_id.get(_opendota_slot_to_player_id(player_slot))
        if player is None:
            continue
        name = od_player.get("personaname") or od_player.get("name")
        if not isinstance(name, str) or not is_displayable_player_name(name):
            continue
        if overwrite or not display_player_name(player):
            player.player_name = name.strip()
    return match


def apply_opendota_player_names_from_path(
    match: ParsedMatch,
    path: str | Path,
    *,
    overwrite: bool = True,
) -> ParsedMatch:
    """Load OpenDota match JSON from *path* and apply its player names."""
    with Path(path).open(encoding="utf-8") as fh:
        opendota_match = json.load(fh)
    return apply_opendota_player_names(match, opendota_match, overwrite=overwrite)


def _opendota_slot_to_player_id(player_slot: int) -> int:
    return player_slot if player_slot < 128 else (player_slot - 128) + 5
