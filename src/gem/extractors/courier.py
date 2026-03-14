"""Courier state extractor for Dota 2 replays.

Tracks ``CDOTA_Unit_Courier`` entities and snapshots their position and state
at configurable tick intervals.

Reference: refs/parser/src/main/java/opendota/Parse.java (entity polling pattern)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.entities import Entity, EntityOp
from gem.extractors.players import _pos

if TYPE_CHECKING:
    from gem.parser import ReplayParser


@dataclass
class CourierSnapshot:
    """A single courier state sample at one tick.

    Attributes:
        tick: Game tick of this sample.
        team: Team number (2=Radiant, 3=Dire).
        state: ``m_iCourierState`` integer value (0 = idle, varies by version).
        flying: True if the courier is in flying form.
        x: World x coordinate, or ``None`` if unavailable.
        y: World y coordinate, or ``None`` if unavailable.
    """

    tick: int
    team: int
    state: int
    flying: bool
    x: float | None
    y: float | None


class CourierExtractor:
    """Polls courier entity state and accumulates snapshots.

    Attach to a ``ReplayParser`` before calling ``parse()``:

    Example:
        >>> extractor = CourierExtractor()
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> print(extractor.snapshots[:3])

    Attributes:
        snapshots: All collected ``CourierSnapshot`` objects in chronological order.
    """

    snapshots: list[CourierSnapshot]

    def __init__(self, sample_interval: int = 150) -> None:
        """Initialise the extractor.

        Args:
            sample_interval: Minimum tick gap between successive snapshots.
                Default 150 ticks ≈ 5 seconds at 30 ticks/sec.
        """
        self._sample_interval = sample_interval
        self._parser: ReplayParser | None = None
        self._last_sample: int = -sample_interval
        self._couriers: dict[int, Entity] = {}
        self.snapshots = []

    def attach(self, parser: ReplayParser) -> None:
        """Register callbacks with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_entity(self._on_entity)

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()
        if not cls.startswith("CDOTA_Unit_Courier"):
            return
        idx = entity.get_index()
        if op.has(EntityOp.DELETED):
            self._couriers.pop(idx, None)
        else:
            self._couriers[idx] = entity
            self._maybe_sample()

    def _maybe_sample(self) -> None:
        if self._parser is None:
            return
        tick = self._parser.tick
        if tick - self._last_sample < self._sample_interval:
            return
        self._last_sample = tick
        self._sample(tick)

    def _sample(self, tick: int) -> None:
        for entity in self._couriers.values():
            team = entity.get_int32("m_iTeamNum") or 0
            state = entity.get_int32("m_iCourierState") or 0
            flying = entity.get_bool("m_bFlyingCourier") or False
            pos = _pos(entity)
            self.snapshots.append(
                CourierSnapshot(
                    tick=tick,
                    team=team,
                    state=state,
                    flying=flying,
                    x=pos[0] if pos else None,
                    y=pos[1] if pos else None,
                )
            )
