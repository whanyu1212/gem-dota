"""Unit tests for extractors/gold_ledger.py (BuybackSpendTracker)."""

from __future__ import annotations

from gem.extractors._snapshots import TEAM_DIRE, TEAM_RADIANT
from gem.extractors.gold_ledger import BuybackSpend, BuybackSpendTracker
from gem.state.entities import Entity, EntityOp
from tests._entities import set_fields


class _Class:
    def __init__(self, name: str) -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


class _Parser:
    """Parser double without field-gated registration (the fallback path)."""

    def __init__(self) -> None:
        self.tick = 0
        self.handlers: list = []

    def _on_entity_filtered(self, handler, **_filters) -> None:
        self.handlers.append(handler)


def _data(cls: str = "CDOTA_DataRadiant") -> Entity:
    return Entity(index=1, serial=1, cls=_Class(cls))


def _pools(entity: Entity, slot: int, spent: int, reliable: int, unreliable: int) -> Entity:
    prefix = f"m_vecDataTeam.{slot:04d}"
    set_fields(
        entity,
        {
            f"{prefix}.m_iGoldSpentOnBuybacks": spent,
            f"{prefix}.m_iReliableGold": reliable,
            f"{prefix}.m_iUnreliableGold": unreliable,
        },
    )
    return entity


def _tracker() -> tuple[BuybackSpendTracker, _Parser]:
    tracker = BuybackSpendTracker()
    parser = _Parser()
    tracker.attach(parser)  # type: ignore[arg-type]
    return tracker, parser


def _update(tracker, parser, entity, tick, op=EntityOp.UPDATED) -> None:
    parser.tick = tick
    tracker._on_entity(entity, op)


class TestBuybackSpendTracker:
    def test_records_a_rise_with_the_unreliable_first_split(self):
        tracker, parser = _tracker()
        entity = _pools(_data(), 2, 0, 1625, 211)
        _update(tracker, parser, entity, 100, EntityOp.CREATED_ENTERED)

        _update(tracker, parser, _pools(entity, 2, 1836, 0, 0), 200)

        assert tracker.spends == [
            BuybackSpend(
                tick=200,
                team=TEAM_RADIANT,
                team_slot=2,
                cost=1836,
                reliable_gold=1625,
                unreliable_gold=211,
            )
        ]

    def test_no_record_without_a_rise_and_a_drop_rebaselines(self):
        tracker, parser = _tracker()
        entity = _pools(_data(), 0, 900, 50, 50)
        _update(tracker, parser, entity, 100, EntityOp.CREATED_ENTERED)
        _update(tracker, parser, _pools(entity, 0, 900, 60, 70), 110)
        _update(tracker, parser, _pools(entity, 0, 100, 60, 70), 120)
        _update(tracker, parser, _pools(entity, 0, 400, 60, 0), 130)

        assert [(spend.tick, spend.cost) for spend in tracker.spends] == [(130, 300)]

    def test_income_on_the_same_update_keeps_the_split(self):
        # Replay 8856501050: reliable pays the whole cost while 337 unreliable
        # income lands on the same update.
        tracker, parser = _tracker()
        entity = _pools(_data(cls="CDOTA_DataDire"), 1, 2101, 4783, 0)
        _update(tracker, parser, entity, 100, EntityOp.CREATED_ENTERED)

        _update(tracker, parser, _pools(entity, 1, 5874, 1010, 337), 200)

        (spend,) = tracker.spends
        assert spend.team == TEAM_DIRE
        assert (spend.cost, spend.reliable_gold, spend.unreliable_gold) == (3773, 3773, 0)

    def test_a_purchase_on_the_same_update_drops_the_split(self):
        tracker, parser = _tracker()
        entity = _pools(_data(), 3, 0, 2000, 1500)
        _update(tracker, parser, entity, 100, EntityOp.CREATED_ENTERED)

        # 1000-gold buyback from unreliable plus a 400-gold purchase.
        _update(tracker, parser, _pools(entity, 3, 1000, 2000, 100), 200)

        (spend,) = tracker.spends
        assert spend.cost == 1000
        assert spend.reliable_gold is None
        assert spend.unreliable_gold is None

    def test_reentered_entity_rebaselines_instead_of_diffing_stale_pools(self):
        tracker, parser = _tracker()
        entity = _pools(_data(), 0, 0, 100, 100)
        _update(tracker, parser, entity, 100, EntityOp.CREATED_ENTERED)

        _update(tracker, parser, _pools(entity, 0, 700, 0, 0), 200, EntityOp.UPDATED_ENTERED)

        assert tracker.spends == []

    def test_deleted_entity_forgets_its_pools(self):
        tracker, parser = _tracker()
        entity = _pools(_data(), 0, 0, 100, 100)
        _update(tracker, parser, entity, 100, EntityOp.CREATED_ENTERED)
        _update(tracker, parser, entity, 150, EntityOp.DELETED)

        _update(tracker, parser, _pools(entity, 0, 700, 0, 0), 200)

        assert tracker.spends == []

    def test_slot_with_a_missing_field_is_skipped(self):
        tracker, parser = _tracker()
        entity = _data()
        set_fields(entity, {"m_vecDataTeam.0000.m_iGoldSpentOnBuybacks": 0})
        _update(tracker, parser, entity, 100, EntityOp.CREATED_ENTERED)
        set_fields(entity, {"m_vecDataTeam.0000.m_iGoldSpentOnBuybacks": 500})
        _update(tracker, parser, entity, 200)

        assert tracker.spends == []

    def test_attach_prefers_field_gated_registration(self):
        registrations = []

        class _GatedParser(_Parser):
            def _on_entity_fields(self, handler, *, required_fields, changed_fields) -> None:
                registrations.append((required_fields, changed_fields))

        BuybackSpendTracker().attach(_GatedParser())  # type: ignore[arg-type]

        ((required, changed),) = registrations
        assert required == ("m_vecDataTeam.0000.m_iGoldSpentOnBuybacks",)
        assert len(changed) == 15
        assert "m_vecDataTeam.0004.m_iUnreliableGold" in changed
