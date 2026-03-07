"""
Tests for gem.entities — entity lifecycle, state, and typed accessors.

Reference: manta/entity.go
"""

import pytest


@pytest.fixture
def entity_cls():
    from gem.entities import Entity

    return Entity


@pytest.fixture
def entity_op():
    from gem.entities import EntityOp

    return EntityOp


class TestEntityOp:
    def test_flag_check(self, entity_op):
        op = entity_op.CREATED | entity_op.ENTERED
        assert op.has(entity_op.CREATED)
        assert op.has(entity_op.ENTERED)
        assert not op.has(entity_op.DELETED)

    def test_created_entered_composite(self, entity_op):
        op = entity_op.CREATED_ENTERED
        assert op.has(entity_op.CREATED)
        assert op.has(entity_op.ENTERED)

    def test_deleted_left_composite(self, entity_op):
        op = entity_op.DELETED_LEFT
        assert op.has(entity_op.DELETED)
        assert op.has(entity_op.LEFT)


class TestEntityState:
    def _make_entity(self, entity_cls, class_name="CDOTAPlayer"):
        class FakeClass:
            name = class_name
            class_id = 1
            serializer = None

        return entity_cls(index=0, serial=0, cls=FakeClass())

    def test_get_missing_returns_none(self, entity_cls):
        e = self._make_entity(entity_cls)
        assert e.get("nonexistent") is None

    def test_set_and_get(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_iHealth"] = 500
        assert e.get("m_iHealth") == 500

    def test_exists_true(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_iHealth"] = 500
        assert e.exists("m_iHealth") is True

    def test_exists_false(self, entity_cls):
        e = self._make_entity(entity_cls)
        assert e.exists("m_iHealth") is False

    def test_get_int32(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_iHealth"] = 200
        val, ok = e.get_int32("m_iHealth")
        assert ok is True
        assert val == 200

    def test_get_int32_missing(self, entity_cls):
        e = self._make_entity(entity_cls)
        val, ok = e.get_int32("m_iHealth")
        assert ok is False
        assert val == 0

    def test_get_float32(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_flMoveSpeed"] = 300.0
        val, ok = e.get_float32("m_flMoveSpeed")
        assert ok is True
        assert val == pytest.approx(300.0)

    def test_get_string(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_iName"] = "npc_dota_hero_axe"
        val, ok = e.get_string("m_iName")
        assert ok is True
        assert val == "npc_dota_hero_axe"

    def test_get_bool(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_bIsWaitingForChampionSelect"] = True
        val, ok = e.get_bool("m_bIsWaitingForChampionSelect")
        assert ok is True
        assert val is True

    def test_get_uint32_from_uint64(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_nHandle"] = 0xDEADBEEF
        val, ok = e.get_uint32("m_nHandle")
        assert ok is True
        assert val == 0xDEADBEEF

    def test_map_returns_all_fields(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["a"] = 1
        e._state["b"] = 2
        m = e.to_map()
        assert m["a"] == 1
        assert m["b"] == 2

    def test_get_class_name(self, entity_cls):
        e = self._make_entity(entity_cls, class_name="CDOTAGamerulesProxy")
        assert e.get_class_name() == "CDOTAGamerulesProxy"

    def test_get_index(self, entity_cls):
        class FakeClass:
            name = "test"
            class_id = 5
            serializer = None

        e = entity_cls(index=42, serial=7, cls=FakeClass())
        assert e.get_index() == 42
        assert e.get_serial() == 7
        assert e.get_class_id() == 5


class TestEntityHandlers:
    def test_on_entity_called(self):
        from gem.entities import EntityOp, EntityTracker

        tracker = EntityTracker()
        received = []

        def handler(entity, op):
            received.append((entity, op))

        tracker.on_entity(handler)

        class FakeClass:
            name = "test"
            class_id = 1
            serializer = None

        from gem.entities import Entity

        e = Entity(index=0, serial=0, cls=FakeClass())
        tracker._dispatch(e, EntityOp.CREATED_ENTERED)

        assert len(received) == 1
        assert received[0][1].has(EntityOp.CREATED)
