"""Exact buyback costs from the team data's gold-spent-on-buybacks counters.

Internal extractor: ``BuybackSpendTracker`` is wired up by :func:`gem.api.parse`
and consumed by :mod:`gem.results.assembly`; it is not part of the public API.

``CDOTA_DataRadiant``/``CDOTA_DataDire`` keep, per team slot, the running total
of gold spent on buybacks (``m_vecDataTeam.NNNN.m_iGoldSpentOnBuybacks``). It
rises on the same tick as the player's BUYBACK combat-log entry, by exactly the
buyback's cost, so each rise is one buyback's cost.

Reference: none of the pinned upstream parsers reads this counter —
odota/parser src/main/java/opendota/Parse.java records only the BUYBACK entry's
time and slot, and dotabuff/manta / skadistats/clarity expose it only as a raw
entity field. Its meaning is established against the BUYBACK entries (same
tick, same player) on the local OpenDota replay fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.extractors._snapshots import TEAM_DIRE, TEAM_RADIANT, team_data_prefix
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

_DATA_CLASSES = ("CDOTA_DataRadiant", "CDOTADataRadiant", "CDOTA_DataDire", "CDOTADataDire")
# Per slot: gold spent on buybacks, then the reliable and unreliable gold pools.
_SLOT_FIELDS = FieldAccessPlan(
    tuple(
        f"{team_data_prefix(team_slot)}.{field_name}"
        for team_slot in range(5)
        for field_name in ("m_iGoldSpentOnBuybacks", "m_iReliableGold", "m_iUnreliableGold")
    )
)
# How far a pool may drop beyond what the split estimate says was paid from it.
# Income landing in the same update only makes a pool drop less; a purchase in
# the same update makes it drop more.
_SPLIT_TOLERANCE = 5

__all__ = ["BuybackSpend", "BuybackSpendTracker"]


@dataclass(frozen=True, slots=True)
class BuybackSpend:
    """One observed rise in a team slot's gold spent on buybacks.

    Attributes:
        tick: Replay tick of the update that carried the rise.
        team: ``TEAM_RADIANT`` or ``TEAM_DIRE``.
        team_slot: The ``m_vecDataTeam`` row, 0-4.
        cost: The rise, i.e. the buyback's cost in gold.
        reliable_gold: Estimated part paid from reliable gold, or ``None``.
        unreliable_gold: Estimated part paid from unreliable gold, or ``None``.
    """

    tick: int
    team: int
    team_slot: int
    cost: int
    reliable_gold: int | None
    unreliable_gold: int | None


class BuybackSpendTracker:
    """Record each rise in the team data's gold spent on buybacks.

    Attributes:
        spends: Observed rises, in replay order.
    """

    def __init__(self) -> None:
        """Initialise an empty tracker."""
        self.spends: list[BuybackSpend] = []
        self._parser: ReplayParser | None = None
        # (team, team_slot) -> (spent on buybacks, reliable, unreliable) as of the
        # last update that carried all three.
        self._pools: dict[tuple[int, int], tuple[int, int, int]] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register for changes to the buyback counters and gold pools.

        The pools must be tracked on every change, not only on buybacks: the
        split estimate needs each pool as it was just before the buyback.

        Args:
            parser: The replay parser to attach to.
        """
        self._parser = parser
        if hasattr(parser, "_on_entity_fields"):
            parser._on_entity_fields(
                self._on_entity,
                required_fields=(_SLOT_FIELDS.names[0],),
                changed_fields=_SLOT_FIELDS.names,
            )
        else:
            # Lightweight parser doubles do not expose field-gated registration.
            parser._on_entity_filtered(self._on_entity, class_names=_DATA_CLASSES)

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        team = TEAM_RADIANT if "Radiant" in entity.get_class_name() else TEAM_DIRE
        if op.has(EntityOp.DELETED):
            for team_slot in range(5):
                self._pools.pop((team, team_slot), None)
            return
        fresh = op.has(EntityOp.CREATED_ENTERED)
        tick = self._parser.tick if self._parser is not None else 0
        fields = entity._resolve_fields(_SLOT_FIELDS)
        for team_slot in range(5):
            key = (team, team_slot)
            spent, reliable, unreliable = (
                entity._get_int32_resolved(fields[team_slot * 3 + i]) for i in range(3)
            )
            if spent is None or reliable is None or unreliable is None:
                self._pools.pop(key, None)
                continue
            before = None if fresh else self._pools.get(key)
            self._pools[key] = (spent, reliable, unreliable)
            # No baseline yet, or the counter did not rise (a drop re-baselines).
            if before is None or spent <= before[0]:
                continue
            self.spends.append(
                _buyback_spend(
                    tick, team, team_slot, before, spent - before[0], reliable, unreliable
                )
            )


def _buyback_spend(
    tick: int,
    team: int,
    team_slot: int,
    before: tuple[int, int, int],
    cost: int,
    reliable: int,
    unreliable: int,
) -> BuybackSpend:
    """Build one rise's record, estimating how it was paid.

    Dota spends unreliable gold first, so the estimate takes
    ``min(cost, unreliable gold before)`` from the unreliable pool and the rest
    from the reliable pool. It is dropped (both parts ``None``) when either pool
    fell by more than the estimate says was paid from it, which means something
    else, such as a purchase, spent gold on the same update. Income on the same
    update makes a pool fall less and is not a contradiction, but if it arrived
    before the buyback it can shift the true split by that income.
    """
    _, reliable_before, unreliable_before = before
    unreliable_gold = min(cost, unreliable_before)
    reliable_gold = cost - unreliable_gold
    agrees = (
        unreliable_before - unreliable <= unreliable_gold + _SPLIT_TOLERANCE
        and reliable_before - reliable <= reliable_gold + _SPLIT_TOLERANCE
    )
    return BuybackSpend(
        tick=tick,
        team=team,
        team_slot=team_slot,
        cost=cost,
        reliable_gold=reliable_gold if agrees else None,
        unreliable_gold=unreliable_gold if agrees else None,
    )
