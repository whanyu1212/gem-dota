"""Deprecated module: gem's fight detection moved to :mod:`gem.extractors.fights`.

Importing it warns once. ``Teamfight``, ``TeamfightPlayer`` and
``detect_teamfights`` are the old names of ``Fight``, ``FightPlayer`` and
``detect_fights``; the OpenDota-compatible names are unchanged.

Reference: odota/parser src/main/java/opendota/CreateParsedDataBlob.java
``processTeamfights`` (pinned in CLAUDE.md), via :mod:`gem.extractors.fights`.
"""

from __future__ import annotations

from gem._deprecation import warn_renamed
from gem.extractors.fights import (
    FIGHT_RADIUS,
    FIGHT_WINDOW_S,
    Fight,
    FightPlayer,
    OpenDotaTeamfight,
    OpenDotaTeamfightPlayer,
    detect_fights,
    detect_opendota_teamfights,
)

warn_renamed("gem.extractors.teamfights", "gem.extractors.fights", stacklevel=2)

Teamfight = Fight
TeamfightPlayer = FightPlayer
detect_teamfights = detect_fights

__all__ = [
    "FIGHT_RADIUS",
    "FIGHT_WINDOW_S",
    "Fight",
    "FightPlayer",
    "OpenDotaTeamfight",
    "OpenDotaTeamfightPlayer",
    "Teamfight",
    "TeamfightPlayer",
    "detect_fights",
    "detect_opendota_teamfights",
    "detect_teamfights",
]
