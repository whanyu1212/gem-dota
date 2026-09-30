"""Deprecated module: moved to :mod:`gem.analysis.fight_positioning`.

Importing it warns once. ``TeamfightPositioning`` and
``build_teamfight_positioning`` are the old names of ``FightPositioning`` and
``build_fight_positioning``.

Reference: see :mod:`gem.analysis.fight_positioning`.
"""

from __future__ import annotations

from gem._deprecation import warn_renamed
from gem.analysis.fight_positioning import *  # noqa: F403
from gem.analysis.fight_positioning import FightPositioning, build_fight_positioning

warn_renamed("gem.analysis.teamfight_positioning", "gem.analysis.fight_positioning", stacklevel=2)

TeamfightPositioning = FightPositioning
build_teamfight_positioning = build_fight_positioning
