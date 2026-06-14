"""Deprecated compatibility shim for :mod:`gem.results.models`."""

import warnings

warnings.warn(
    "gem.models is deprecated; import from gem.results.models instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.results.models import (  # noqa: E402
    AegisEvent,
    BarracksKill,
    ChatEntry,
    CombatLogEntry,
    CourierSnapshot,
    DraftEvent,
    NeutralItemFoundEvent,
    ParsedMatch,
    ParsedPlayer,
    RoshanKill,
    ShrineKill,
    SmokeEvent,
    Teamfight,
    TormentorKill,
    TowerKill,
    VisionModifierEvent,
    WardEvent,
    dataclass,
    defaultdict,
    field,
)

__all__ = [
    "AegisEvent",
    "BarracksKill",
    "ChatEntry",
    "CombatLogEntry",
    "CourierSnapshot",
    "DraftEvent",
    "NeutralItemFoundEvent",
    "ParsedMatch",
    "ParsedPlayer",
    "RoshanKill",
    "ShrineKill",
    "SmokeEvent",
    "Teamfight",
    "TormentorKill",
    "TowerKill",
    "VisionModifierEvent",
    "WardEvent",
    "dataclass",
    "defaultdict",
    "field",
]
