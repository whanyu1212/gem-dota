"""High-level extractors that convert raw replay data into structured records.

Each extractor attaches to a ``ReplayParser`` via its ``attach(parser)``
method, registers the necessary callbacks, and accumulates results during
``parser.parse()``.

Example:
    >>> from gem.parser import ReplayParser
    >>> from gem.extractors import ObjectivesExtractor, PlayerExtractor, WardsExtractor
    >>>
    >>> parser = ReplayParser("game.dem")
    >>> players = PlayerExtractor()
    >>> objectives = ObjectivesExtractor()
    >>> wards = WardsExtractor()
    >>>
    >>> players.attach(parser)
    >>> objectives.attach(parser)
    >>> wards.attach(parser)
    >>> parser.parse()
    >>>
    >>> print(objectives.roshan_kills)
    >>> print(wards.ward_events[:5])
    >>> print(players.time_series(player_id=0))
"""

from gem.extractors.courier import CourierExtractor, CourierSnapshot
from gem.extractors.draft import DraftEvent, DraftExtractor
from gem.extractors.objectives import BarracksKill, ObjectivesExtractor, RoshanKill, TowerKill
from gem.extractors.players import PlayerExtractor, PlayerStateSnapshot, PlayerTimeSeries
from gem.extractors.wards import WardEvent, WardsExtractor

__all__ = [
    "PlayerExtractor",
    "PlayerStateSnapshot",
    "PlayerTimeSeries",
    "ObjectivesExtractor",
    "TowerKill",
    "RoshanKill",
    "BarracksKill",
    "WardsExtractor",
    "WardEvent",
    "CourierExtractor",
    "CourierSnapshot",
    "DraftExtractor",
    "DraftEvent",
]
