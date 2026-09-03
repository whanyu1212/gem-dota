"""
Tests for gem.state.entities — entity lifecycle, state, and typed accessors.

Reference: manta/entity.go
"""

from __future__ import annotations

import pytest

from gem.schema.field_path import FieldPath
from gem.state.entities import (
    ClassInfo,
    Entity,
    EntityManager,
    EntityOp,
    EntityTracker,
    FieldState,
    _find_field_path,
)
from gem.state.string_table import StringTable, StringTables


@pytest.fixture
def entity_cls():
    from gem.state.entities import Entity

    return Entity


@pytest.fixture
def entity_op():
    from gem.state.entities import EntityOp

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
        val = e.get_int32("m_iHealth")
        assert val == 200

    def test_get_int32_missing(self, entity_cls):
        e = self._make_entity(entity_cls)
        val = e.get_int32("m_iHealth")
        assert val is None

    def test_get_float32(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_flMoveSpeed"] = 300.0
        val = e.get_float32("m_flMoveSpeed")
        assert val == pytest.approx(300.0)

    def test_get_string(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_iName"] = "npc_dota_hero_axe"
        val = e.get_string("m_iName")
        assert val == "npc_dota_hero_axe"

    def test_get_bool(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_bIsWaitingForChampionSelect"] = True
        val = e.get_bool("m_bIsWaitingForChampionSelect")
        assert val is True

    def test_get_uint32_from_uint64(self, entity_cls):
        e = self._make_entity(entity_cls)
        e._state["m_nHandle"] = 0xDEADBEEF
        val = e.get_uint32("m_nHandle")
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
        from gem.state.entities import EntityOp, EntityTracker

        tracker = EntityTracker()
        received = []

        def handler(entity, op):
            received.append((entity, op))

        tracker.on_entity(handler)

        class FakeClass:
            name = "test"
            class_id = 1
            serializer = None

        from gem.state.entities import Entity

        e = Entity(index=0, serial=0, cls=FakeClass())
        tracker._dispatch(e, EntityOp.CREATED_ENTERED)

        assert len(received) == 1
        assert received[0][1].has(EntityOp.CREATED)


# ---------------------------------------------------------------------------
# ClassInfo — @dataclass(slots=True)
# ---------------------------------------------------------------------------


class TestClassInfo:
    def test_is_dataclass(self):
        from dataclasses import is_dataclass

        assert is_dataclass(ClassInfo)

    def test_has_slots(self):

        assert hasattr(ClassInfo, "__slots__")

    def test_construction(self):

        ci = ClassInfo(class_id=42, name="CDOTA_Unit_Hero_Axe", serializer=None)
        assert ci.class_id == 42
        assert ci.name == "CDOTA_Unit_Hero_Axe"
        assert ci.serializer is None

    def test_field_names(self):
        from dataclasses import fields

        assert {f.name for f in fields(ClassInfo)} == {"class_id", "name", "serializer"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class FakeClass:
    def __init__(self, name: str = "TestClass", class_id: int = 1) -> None:
        self.name = name
        self.class_id = class_id
        self.serializer = None


def _entity(
    name: str = "TestClass",
    index: int = 0,
    serial: int = 0,
    class_id: int = 1,
) -> Entity:
    return Entity(index=index, serial=serial, cls=FakeClass(name, class_id))


def _fp(*path: int) -> FieldPath:
    fp = FieldPath()
    for i, v in enumerate(path):
        fp.path[i] = v
    fp.last = len(path) - 1
    return fp


# ---------------------------------------------------------------------------
# FieldState
# ---------------------------------------------------------------------------


class TestFieldState:
    def test_get_missing_returns_none(self):
        fs = FieldState()
        assert fs.get(_fp(0)) is None

    def test_set_and_get_depth1(self):
        fs = FieldState()
        fs.set(_fp(0), 42)
        assert fs.get(_fp(0)) == 42

    def test_set_and_get_depth2(self):
        fs = FieldState()
        fs.set(_fp(0, 1), "hello")
        assert fs.get(_fp(0, 1)) == "hello"

    def test_set_and_get_depth3(self):
        fs = FieldState()
        fs.set(_fp(0, 1, 2), 3.14)
        assert fs.get(_fp(0, 1, 2)) == pytest.approx(3.14)

    def test_multiple_slots_independent(self):
        fs = FieldState()
        fs.set(_fp(0), 1)
        fs.set(_fp(1), 2)
        assert fs.get(_fp(0)) == 1
        assert fs.get(_fp(1)) == 2

    def test_overwrite_value(self):
        fs = FieldState()
        fs.set(_fp(0), 10)
        fs.set(_fp(0), 20)
        assert fs.get(_fp(0)) == 20

    def test_grow_past_initial_capacity(self):
        fs = FieldState()
        # Initial capacity is 8; write beyond that
        fs.set(_fp(15), 99)
        assert fs.get(_fp(15)) == 99

    def test_get_path_too_short_returns_none(self):
        # Set a value at depth 2; reading at depth 1 finds a FieldState child, not a value
        fs = FieldState()
        fs.set(_fp(0, 0), 7)
        # depth-1 path: the slot holds a FieldState, not 7
        result = fs.get(_fp(0))
        assert result is None or isinstance(result, FieldState)

    def test_get_beyond_array_length_returns_none(self):
        fs = FieldState()
        assert fs.get(_fp(100)) is None

    def test_set_does_not_overwrite_fieldstate_child_with_leaf(self):
        # Writing a leaf at the same index where a child FieldState already exists
        # should be a no-op (the set() implementation guards on isinstance check)
        fs = FieldState()
        fs.set(_fp(0, 0), 5)  # creates child FieldState at slot 0
        fs.set(_fp(0), 999)  # tries to write leaf where child FieldState lives
        # Child must still be accessible
        assert fs.get(_fp(0, 0)) == 5


# ---------------------------------------------------------------------------
# Entity typed getters — edge cases
# ---------------------------------------------------------------------------


class TestEntityTypedGetters:
    def test_get_int32_from_float_returns_none(self):
        e = _entity()
        e._state["x"] = 1.5
        val = e.get_int32("x")
        assert val is None

    def test_get_float32_from_int_succeeds(self):
        e = _entity()
        e._state["x"] = 5
        val = e.get_float32("x")
        assert val == pytest.approx(5.0)

    def test_get_string_from_int_returns_none(self):
        e = _entity()
        e._state["x"] = 42
        val = e.get_string("x")
        assert val is None

    def test_get_bool_from_zero_is_false(self):
        e = _entity()
        e._state["x"] = 0
        val = e.get_bool("x")
        assert val is False

    def test_get_bool_from_nonzero_is_true(self):
        e = _entity()
        e._state["x"] = 1
        val = e.get_bool("x")
        assert val is True

    def test_get_bool_from_string_returns_none(self):
        e = _entity()
        e._state["x"] = "yes"
        val = e.get_bool("x")
        assert val is None

    def test_get_uint32_truncates_high_bits(self):
        e = _entity()
        e._state["h"] = 0x1_DEAD_BEEF
        val = e.get_uint32("h")
        assert val == 0xDEAD_BEEF

    def test_get_uint64_returns_full_value(self):
        e = _entity()
        e._state["h"] = 0xDEAD_BEEF_CAFE_1234
        val = e.get_uint64("h")
        assert val == 0xDEAD_BEEF_CAFE_1234

    def test_get_uint64_missing_returns_none(self):
        e = _entity()
        val = e.get_uint64("missing")
        assert val is None

    def test_repr(self):
        e = _entity("MyClass", index=7)
        assert "7" in repr(e)
        assert "MyClass" in repr(e)

    def test_active_default_true(self):
        e = _entity()
        assert e.active is True


# ---------------------------------------------------------------------------
# Entity.get() via FieldState + _find_field_path
# ---------------------------------------------------------------------------


class TestEntityGetViaFieldState:
    """Tests for the slow path: serializer → FieldPath → FieldState."""

    def _make_simple_serializer(self):
        """Build a minimal serializer with one simple field."""
        from gem.schema.sendtable import FIELD_MODEL_SIMPLE, Field, Serializer

        decoder = lambda r: 777  # noqa: E731

        f = Field.__new__(Field)
        f.var_name = "m_iHealth"
        f.model = FIELD_MODEL_SIMPLE
        f.decoder = decoder
        f.base_decoder = None
        f.child_decoder = None
        f.serializer = None

        ser = Serializer(name="TestSer", version=0)
        ser.fields = [f]
        return ser

    def _make_array_serializer(self):
        """Build a minimal serializer with one fixed-array field."""
        from gem.schema.sendtable import FIELD_MODEL_FIXED_ARRAY, Field, Serializer

        f = Field.__new__(Field)
        f.var_name = "m_Arr"
        f.model = FIELD_MODEL_FIXED_ARRAY
        f.decoder = lambda r: 0
        f.base_decoder = None
        f.child_decoder = None
        f.serializer = None

        ser = Serializer(name="ArrSer", version=0)
        ser.fields = [f]
        return ser

    def test_get_via_serializer_hit(self):
        ser = self._make_simple_serializer()
        cls = FakeClass("T")
        cls.serializer = ser
        e = Entity(index=0, serial=0, cls=cls)
        # Manually place value in FieldState at path [0]
        e._field_state.set(_fp(0), 42)
        assert e.get("m_iHealth") == 42

    def test_get_via_serializer_noop_cached(self):
        ser = self._make_simple_serializer()
        cls = FakeClass("T")
        cls.serializer = ser
        e = Entity(index=0, serial=0, cls=cls)
        # First call records an explicit shared serializer miss.
        assert e.get("nonexistent") is None
        assert e.get("nonexistent") is None
        assert ser._resolved_fields["nonexistent"].path is None

    def test_get_cache_hit_on_second_call(self):
        ser = self._make_simple_serializer()
        cls = FakeClass("T")
        cls.serializer = ser
        e = Entity(index=0, serial=0, cls=cls)
        e._field_state.set(_fp(0), 99)
        e.get("m_iHealth")
        assert ser._resolved_fields["m_iHealth"].path == (0,)
        assert e.get("m_iHealth") == 99  # hits cache

    def test_entities_share_positive_and_negative_resolutions(self):
        ser = self._make_simple_serializer()
        cls = FakeClass("T")
        cls.serializer = ser
        first = Entity(index=0, serial=0, cls=cls)
        second = Entity(index=1, serial=0, cls=cls)
        first._field_state.set(_fp(0), 10)
        second._field_state.set(_fp(0), 20)

        assert first.get("m_iHealth") == 10
        hit = ser._resolved_fields["m_iHealth"]
        assert second.get("m_iHealth") == 20
        assert ser._resolved_fields["m_iHealth"] is hit

        assert first.get("missing") is None
        miss = ser._resolved_fields["missing"]
        assert miss.path is None
        assert second.get("missing") is None
        assert ser._resolved_fields["missing"] is miss

    def test_distinct_serializers_do_not_share_resolution_state(self):
        first_ser = self._make_simple_serializer()
        second_ser = self._make_simple_serializer()
        second_ser.version = 1

        first_hit = first_ser._resolve_field("m_iHealth")
        second_hit = second_ser._resolve_field("m_iHealth")

        assert first_hit is not second_hit
        assert first_ser._resolved_fields is not second_ser._resolved_fields

    def test_resolved_access_preserves_overlay_precedence(self):
        from gem.schema.sendtable.models import FieldAccessPlan

        ser = self._make_simple_serializer()
        cls = FakeClass("T")
        cls.serializer = ser
        e = Entity(index=0, serial=0, cls=cls)
        e._field_state.set(_fp(0), 99)
        plan = FieldAccessPlan(("m_iHealth", "missing"))
        health, missing = e._resolve_fields(plan)

        assert e._get_int32_resolved(health) == 99
        e._state["m_iHealth"] = None
        e._state["missing"] = 42
        assert e._get_int32_resolved(health) is None
        assert e._get_int32_resolved(missing) == 42

    def test_field_plan_tuple_is_reused_by_serializer(self):
        from gem.schema.sendtable.models import FieldAccessPlan

        ser = self._make_simple_serializer()
        plan = FieldAccessPlan(("m_iHealth", "missing"))

        first = ser._resolve_plan(plan)
        second = ser._resolve_plan(plan)

        assert second is first
        assert first[0].path is not None
        assert first[1].path is None

    def test_entity_does_not_allocate_field_resolution_caches(self):
        ser = self._make_simple_serializer()
        cls = FakeClass("T")
        cls.serializer = ser
        entity = Entity(index=0, serial=0, cls=cls)

        assert not hasattr(entity, "_fp_cache")
        assert not hasattr(entity, "_fp_noop")

    def test_get_array_field_by_index(self):
        ser = self._make_array_serializer()
        cls = FakeClass("T")
        cls.serializer = ser
        e = Entity(index=0, serial=0, cls=cls)
        # Array element at path [0][3]
        e._field_state.set(_fp(0, 3), 55)
        assert e.get("m_Arr.0003") == 55


# ---------------------------------------------------------------------------
# _find_field_path — direct tests
# ---------------------------------------------------------------------------


class TestFindFieldPath:
    def _ser_with_fields(self, *var_names):
        from gem.schema.sendtable import FIELD_MODEL_SIMPLE, Field, Serializer

        fields = []
        for name in var_names:
            f = Field.__new__(Field)
            f.var_name = name
            f.model = FIELD_MODEL_SIMPLE
            f.decoder = None
            f.base_decoder = None
            f.child_decoder = None
            f.serializer = None
            fields.append(f)

        ser = Serializer(name="S", version=0)
        ser.fields = fields
        return ser

    def test_simple_field_found(self):
        ser = self._ser_with_fields("m_iHealth", "m_flSpeed")
        fp = _find_field_path(ser, "m_iHealth")
        assert fp is not None
        assert fp.path[0] == 0
        assert fp.last == 0

    def test_second_field_found(self):
        ser = self._ser_with_fields("m_iHealth", "m_flSpeed")
        fp = _find_field_path(ser, "m_flSpeed")
        assert fp is not None
        assert fp.path[0] == 1

    def test_unknown_field_returns_none(self):
        ser = self._ser_with_fields("m_iHealth")
        assert _find_field_path(ser, "m_flSpeed") is None

    def test_nested_fixed_table(self):
        from gem.schema.sendtable import FIELD_MODEL_FIXED_TABLE, Field, Serializer

        inner = self._ser_with_fields("m_x")

        f = Field.__new__(Field)
        f.var_name = "m_nested"
        f.model = FIELD_MODEL_FIXED_TABLE
        f.decoder = None
        f.base_decoder = None
        f.child_decoder = None
        f.serializer = inner

        ser = Serializer(name="S", version=0)
        ser.fields = [f]

        fp = _find_field_path(ser, "m_nested.m_x")
        assert fp is not None
        assert fp.path[0] == 0
        assert fp.path[1] == 0
        assert fp.last == 1

    def test_fixed_array_index(self):
        from gem.schema.sendtable import FIELD_MODEL_FIXED_ARRAY, Field, Serializer

        f = Field.__new__(Field)
        f.var_name = "m_Items"
        f.model = FIELD_MODEL_FIXED_ARRAY
        f.decoder = None
        f.base_decoder = None
        f.child_decoder = None
        f.serializer = None

        ser = Serializer(name="S", version=0)
        ser.fields = [f]

        fp = _find_field_path(ser, "m_Items.0002")
        assert fp is not None
        assert fp.path[0] == 0
        assert fp.path[1] == 2
        assert fp.last == 1

    def test_variable_array_index(self):
        from gem.schema.sendtable import FIELD_MODEL_VARIABLE_ARRAY, Field, Serializer

        f = Field.__new__(Field)
        f.var_name = "m_Vec"
        f.model = FIELD_MODEL_VARIABLE_ARRAY
        f.decoder = None
        f.base_decoder = None
        f.child_decoder = None
        f.serializer = None

        ser = Serializer(name="S", version=0)
        ser.fields = [f]

        fp = _find_field_path(ser, "m_Vec.0007")
        assert fp is not None
        assert fp.path[1] == 7

    def test_variable_table_nested(self):
        from gem.schema.sendtable import FIELD_MODEL_VARIABLE_TABLE, Field, Serializer

        inner = self._ser_with_fields("m_val")

        f = Field.__new__(Field)
        f.var_name = "m_tbl"
        f.model = FIELD_MODEL_VARIABLE_TABLE
        f.decoder = None
        f.base_decoder = None
        f.child_decoder = None
        f.serializer = inner

        ser = Serializer(name="S", version=0)
        ser.fields = [f]

        fp = _find_field_path(ser, "m_tbl.0001.m_val")
        assert fp is not None
        assert fp.path[0] == 0
        assert fp.path[1] == 1
        assert fp.path[2] == 0
        assert fp.last == 2


# ---------------------------------------------------------------------------
# EntityTracker — multi-handler dispatch
# ---------------------------------------------------------------------------


class TestEntityTrackerMultiHandler:
    def test_multiple_handlers_all_called(self):
        tracker = EntityTracker()
        log = []
        tracker.on_entity(lambda e, op: log.append(("a", op)))
        tracker.on_entity(lambda e, op: log.append(("b", op)))
        e = _entity()
        tracker._dispatch(e, EntityOp.CREATED)
        assert log == [("a", EntityOp.CREATED), ("b", EntityOp.CREATED)]

    def test_no_handlers_no_error(self):
        tracker = EntityTracker()
        tracker._dispatch(_entity(), EntityOp.DELETED)  # should not raise

    def test_handler_receives_correct_entity(self):
        tracker = EntityTracker()
        received = []
        tracker.on_entity(lambda e, op: received.append(e))
        e = _entity("MyHero", index=5)
        tracker._dispatch(e, EntityOp.UPDATED)
        assert received[0] is e

    @pytest.mark.parametrize(
        "op",
        [
            EntityOp.CREATED,
            EntityOp.UPDATED,
            EntityOp.ENTERED,
            EntityOp.LEFT,
            EntityOp.DELETED,
            EntityOp.CREATED_ENTERED,
            EntityOp.UPDATED_ENTERED,
            EntityOp.DELETED_LEFT,
        ],
    )
    def test_generic_and_filtered_handlers_receive_every_operation(self, op):
        tracker = EntityTracker()
        received = []
        tracker.on_entity(lambda _e, value: received.append(("generic", value)))
        tracker._on_entity_filtered(
            lambda _e, value: received.append(("filtered", value)),
            class_names=("ExactClass",),
        )
        tracker._on_class_info([ClassInfo(7, "ExactClass", None)])

        tracker._dispatch(_entity("ExactClass", class_id=7), op)

        assert received == [("generic", op), ("filtered", op)]

    def test_exact_and_prefix_filters_ignore_nonmatching_classes(self):
        tracker = EntityTracker()
        received = []
        tracker._on_entity_filtered(
            lambda entity, _op: received.append(("exact", entity.get_class_name())),
            class_names=("ExactClass",),
        )
        tracker._on_entity_filtered(
            lambda entity, _op: received.append(("prefix", entity.get_class_name())),
            class_prefixes=("Hero_",),
        )
        tracker._on_class_info(
            [
                ClassInfo(1, "ExactClass", None),
                ClassInfo(2, "Hero_Axe", None),
                ClassInfo(3, "OtherClass", None),
            ]
        )

        tracker._dispatch(_entity("ExactClass", class_id=1), EntityOp.UPDATED)
        tracker._dispatch(_entity("Hero_Axe", class_id=2), EntityOp.UPDATED)
        tracker._dispatch(_entity("OtherClass", class_id=3), EntityOp.UPDATED)

        assert received == [("exact", "ExactClass"), ("prefix", "Hero_Axe")]

    def test_registration_order_is_preserved_before_and_after_class_info(self):
        tracker = EntityTracker()
        received = []
        tracker.on_entity(lambda _e, _op: received.append("generic-before"))
        tracker._on_entity_filtered(
            lambda _e, _op: received.append("filtered-before"),
            class_prefixes=("Hero_",),
        )
        tracker._on_class_info([ClassInfo(4, "Hero_Axe", None)])
        tracker._on_entity_filtered(
            lambda _e, _op: received.append("filtered-after"),
            class_names=("Hero_Axe",),
        )
        tracker.on_entity(lambda _e, _op: received.append("generic-after"))

        tracker._dispatch(_entity("Hero_Axe", class_id=4), EntityOp.CREATED_ENTERED)

        assert received == [
            "generic-before",
            "filtered-before",
            "filtered-after",
            "generic-after",
        ]

    def test_overlapping_filters_and_recompile_do_not_duplicate_handler(self):
        tracker = EntityTracker()
        received = []
        tracker._on_entity_filtered(
            lambda _e, _op: received.append("matched"),
            class_names=("Hero_Axe",),
            class_prefixes=("Hero_",),
        )
        classes = [ClassInfo(5, "Hero_Axe", None)]
        tracker._on_class_info(classes)
        tracker._on_class_info(classes)

        tracker._dispatch(_entity("Hero_Axe", class_id=5), EntityOp.UPDATED)

        assert received == ["matched"]

    def test_filtered_handler_matches_before_class_info_for_direct_dispatch(self):
        tracker = EntityTracker()
        received = []
        tracker._on_entity_filtered(
            lambda entity, _op: received.append(entity.get_class_name()),
            class_prefixes=("Hero_",),
        )

        tracker._dispatch(_entity("Hero_Axe"), EntityOp.UPDATED)
        tracker._dispatch(_entity("OtherClass"), EntityOp.UPDATED)

        assert received == ["Hero_Axe"]

    def test_filtered_handler_requires_a_nonempty_filter(self):
        tracker = EntityTracker()

        with pytest.raises(ValueError, match="require a class name or prefix"):
            tracker._on_entity_filtered(lambda _e, _op: None)


# ---------------------------------------------------------------------------
# ClassInfo
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# EntityManager — on_server_info
# ---------------------------------------------------------------------------


class TestEntityManagerServerInfo:
    def _make_em(self):
        return EntityManager(serializers={}, string_tables=StringTables())

    def test_class_id_size_set(self):
        em = self._make_em()

        class Msg:
            max_classes = 512
            game_dir = "/dota_v1234/dota"

        em.on_server_info(Msg())
        assert em.class_id_size == 10  # log2(512) + 1
        assert em.game_build == 1234

    def test_entities_list_sized(self):
        em = self._make_em()

        class Msg:
            max_classes = 256
            game_dir = ""

        em.on_server_info(Msg())
        assert len(em.entities) == 1 << 14  # full Source 2 entity pool, not max_classes

    def test_game_build_zero_when_no_match(self):
        em = self._make_em()

        class Msg:
            max_classes = 256
            game_dir = "/some/other/path"

        em.on_server_info(Msg())
        assert em.game_build == 0


# ---------------------------------------------------------------------------
# EntityManager — on_class_info
# ---------------------------------------------------------------------------


class TestEntityManagerClassInfo:
    def _make_em(self):
        return EntityManager(serializers={}, string_tables=StringTables())

    def test_classes_populated(self):
        em = self._make_em()

        class FakeClassEntry:
            class_id = 3
            network_name = "CDOTA_Unit_Hero_Axe"

        class Msg:
            classes = [FakeClassEntry()]

        em.on_class_info(Msg())
        assert 3 in em.classes_by_id
        assert "CDOTA_Unit_Hero_Axe" in em.classes_by_name

    def test_serializer_linked_when_present(self):
        from gem.schema.sendtable import Serializer

        ser = Serializer(name="CDOTA_Unit_Hero_Axe", version=0)

        em = EntityManager(serializers={"CDOTA_Unit_Hero_Axe": ser}, string_tables=StringTables())

        class FakeClassEntry:
            class_id = 1
            network_name = "CDOTA_Unit_Hero_Axe"

        class Msg:
            classes = [FakeClassEntry()]

        em.on_class_info(Msg())
        ci = em.classes_by_id[1]
        assert ci.serializer is ser

    def test_class_info_ready_flag(self):
        em = self._make_em()
        assert em._class_info_ready is False

        class Msg:
            classes = []

        em.on_class_info(Msg())
        assert em._class_info_ready is True

    def test_class_info_compiles_filtered_handlers(self):
        em = self._make_em()
        received = []
        em._on_entity_filtered(
            lambda entity, _op: received.append(entity.get_class_name()),
            class_prefixes=("CDOTA_Unit_Hero_",),
        )

        class HeroClass:
            class_id = 1
            network_name = "CDOTA_Unit_Hero_Axe"

        class OtherClass:
            class_id = 2
            network_name = "CDOTA_BaseNPC"

        class Msg:
            classes = [HeroClass(), OtherClass()]

        em.on_class_info(Msg())
        em.tracker._dispatch(
            Entity(index=0, serial=0, cls=em.classes_by_id[1]),
            EntityOp.CREATED_ENTERED,
        )
        em.tracker._dispatch(
            Entity(index=1, serial=0, cls=em.classes_by_id[2]),
            EntityOp.CREATED_ENTERED,
        )

        assert received == ["CDOTA_Unit_Hero_Axe"]


# ---------------------------------------------------------------------------
# EntityManager — on_baseline_updated / _update_baselines
# ---------------------------------------------------------------------------


class TestEntityManagerBaselines:
    def test_baseline_not_applied_before_class_info(self):
        em = EntityManager(serializers={}, string_tables=StringTables())
        # Add a string table entry before class info
        st = StringTable(index=0, name="instancebaseline")
        st.items[0] = ("3", b"\x00")
        em.string_tables.add(st)
        em.on_baseline_updated()
        # Class info not ready yet → no baselines
        assert em.class_baselines == {}

    def test_baseline_applied_after_class_info(self):
        em = EntityManager(serializers={}, string_tables=StringTables())
        st = StringTable(index=0, name="instancebaseline")
        st.items[0] = ("5", b"\xab\xcd")
        em.string_tables.add(st)

        class Msg:
            classes = []

        em.on_class_info(Msg())  # sets _class_info_ready + calls _update_baselines
        assert em.class_baselines.get(5) == b"\xab\xcd"

    def test_non_int_key_skipped(self):
        em = EntityManager(serializers={}, string_tables=StringTables())
        st = StringTable(index=0, name="instancebaseline")
        st.items[0] = ("not_an_int", b"\x00")
        em.string_tables.add(st)

        class Msg:
            classes = []

        em.on_class_info(Msg())
        assert em.class_baselines == {}


# ---------------------------------------------------------------------------
# EntityManager — find / find_by_handle / filter / find_by_class_name / all_active
# ---------------------------------------------------------------------------


class TestEntityManagerQueryHelpers:
    def _make_em_with_entity(self, index=0, serial=0, name="Hero"):
        em = EntityManager(serializers={}, string_tables=StringTables())
        em.entities = [None] * 10
        e = _entity(name, index=index, serial=serial)
        em.entities[index] = e
        return em, e

    def test_find_returns_entity(self):
        em, e = self._make_em_with_entity(index=3)
        assert em.find(3) is e

    def test_find_returns_none_for_empty_slot(self):
        em, _ = self._make_em_with_entity(index=3)
        assert em.find(0) is None

    def test_find_out_of_range_returns_none(self):
        em, _ = self._make_em_with_entity()
        assert em.find(999) is None

    def test_find_by_handle_success(self):
        em, e = self._make_em_with_entity(index=2, serial=7)
        handle = (7 << 14) | 2
        assert em.find_by_handle(handle) is e

    def test_find_by_handle_wrong_serial(self):
        em, _ = self._make_em_with_entity(index=2, serial=7)
        handle = (99 << 14) | 2  # wrong serial
        assert em.find_by_handle(handle) is None

    def test_find_by_handle_empty_slot(self):
        em, _ = self._make_em_with_entity(index=2, serial=7)
        handle = (7 << 14) | 5  # slot 5 is empty
        assert em.find_by_handle(handle) is None

    def test_filter_returns_matching(self):
        em, e = self._make_em_with_entity(index=0, name="Hero")
        e2 = _entity("Tower", index=1)
        em.entities[1] = e2
        heroes = em.filter(lambda x: x.get_class_name() == "Hero")
        assert heroes == [e]

    def test_filter_empty_result(self):
        em, _ = self._make_em_with_entity(name="Hero")
        result = em.filter(lambda x: x.get_class_name() == "NoSuchClass")
        assert result == []

    def test_find_by_class_name_found(self):
        em, e = self._make_em_with_entity(name="CDOTAGamerulesProxy")
        assert em.find_by_class_name("CDOTAGamerulesProxy") is e

    def test_find_by_class_name_not_found(self):
        em, _ = self._make_em_with_entity(name="Hero")
        assert em.find_by_class_name("NoSuchClass") is None

    def test_find_by_class_name_inactive_skipped(self):
        em, e = self._make_em_with_entity(name="Hero")
        e.active = False
        assert em.find_by_class_name("Hero") is None

    def test_all_active_returns_active_only(self):
        em = EntityManager(serializers={}, string_tables=StringTables())
        em.entities = [None] * 4
        e1 = _entity("A", index=0)
        e2 = _entity("B", index=1)
        e2.active = False
        em.entities[0] = e1
        em.entities[1] = e2
        result = em.all_active()
        assert e1 in result
        assert e2 not in result

    def test_all_active_empty(self):
        em = EntityManager(serializers={}, string_tables=StringTables())
        em.entities = [None] * 4
        assert em.all_active() == []


# ---------------------------------------------------------------------------
# EntityManager — on_packet_entities (synthetic bit stream)
# ---------------------------------------------------------------------------


def _build_packet(updates: list[tuple]) -> bytes:
    """Build a minimal CSVCMsg_PacketEntities-style payload.

    Each update tuple: (delta_index, cmd_bits, extra_bits_bytes)
    Returns raw bytes. Not a real protobuf — we drive on_packet_entities
    through a fake message object instead.
    """

    return b""  # placeholder — see tests below for direct approach


class TestEntityManagerPacketEntities:
    """Tests for on_packet_entities using fake messages with synthetic bit data."""

    def _make_em(self, max_classes=256, game_dir=""):
        em = EntityManager(serializers={}, string_tables=StringTables())

        class ServerInfo:
            max_classes = 256
            game_dir = ""

        em.on_server_info(ServerInfo())
        return em

    def _write_bits(self, *args) -> bytes:
        """Write a sequence of (value, nbits) pairs into a byte buffer LSB-first."""
        bits = []
        for value, nbits in args:
            for i in range(nbits):
                bits.append((value >> i) & 1)
        # Pad to byte boundary
        while len(bits) % 8:
            bits.append(0)
        result = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte |= bits[i + j] << j
            result.append(byte)
        return bytes(result)

    def _write_ubit_var(self, value: int) -> list[tuple[int, int]]:
        """Encode value as ubit_var: 6 bits + 2-bit selector = 0."""
        # Use small form: selector=0 (2 bits = 0b00), then 4 more bits → 6-bit total
        # ubit_var: read 6 bits, then 2-bit selector; if selector==0 return low 4 bits
        # Actually: read low 6 bits, read 2 more → 8 bits total; selector = high 2
        # Form: selector bits = bits[4:6]; value in bits[0:4] if selector==0
        # Simplest: value < 16 → selector=00, write low 4 bits then 00
        assert value < 16, "use small values for simplicity"
        return [(value & 0xF, 4), (0, 2)]  # 6 bits total

    def test_full_packet_second_call_returns_empty(self):
        em = self._make_em()

        class Msg:
            legacy_is_delta = False
            updated_entries = 0
            entity_data = b""

        em.on_packet_entities(Msg())  # first full packet
        result = em.on_packet_entities(Msg())  # second full packet ignored
        assert result == []

    def test_delta_packet_always_processed(self):
        em = self._make_em()

        class Msg:
            legacy_is_delta = True
            updated_entries = 0
            entity_data = b""

        result = em.on_packet_entities(Msg())
        assert result == []  # 0 updates → empty result, but no early return

    def test_leave_without_delete(self):
        """cmd=0b01 → LEFT only (entity goes inactive)."""
        em = self._make_em()
        # Place an entity at index 0
        e = _entity("Hero", index=0, serial=0)
        em.entities[0] = e

        # Build: delta=0 (stays at index 0), cmd=0b01 (leave, no delete)
        # ubit_var delta: value=0 → write as (0, 4), (0, 2)
        # But index = -1 + delta + 1, so delta=0 → index=0
        # cmd = 01 binary → bits: 1, 0
        bits = []
        # ubit_var(0): 4 low bits = 0000, selector = 00 → 6 bits total: 000000
        for _ in range(4):
            bits.append(0)
        bits.append(0)
        bits.append(0)
        # cmd = 0b01: bit0=1, bit1=0
        bits.append(1)
        bits.append(0)
        # Pad to byte boundary
        while len(bits) % 8:
            bits.append(0)
        bytes(int("".join(str(b) for b in bits[:: -1 * 0 or 1]), 2) for _ in [0])

        # Simpler approach: just build bytes directly
        # ubit_var(0) = read 6 bits then 2-bit group → use the 6-bit form
        # Actually let's just build the raw bits manually
        raw_bits = [
            0,
            0,
            0,
            0,
            0,
            0,  # ubit_var(0): result=0, selector=00
            1,
            0,
        ]  # cmd = 01 (binary LSB first: bit0=1, bit1=0)
        while len(raw_bits) % 8:
            raw_bits.append(0)
        data = bytearray()
        for i in range(0, len(raw_bits), 8):
            byte = 0
            for j in range(8):
                byte |= raw_bits[i + j] << j
            data.append(byte)

        class Msg:
            legacy_is_delta = True
            updated_entries = 1
            entity_data = bytes(data)

        results = em.on_packet_entities(Msg())
        assert len(results) == 1
        entity_out, op = results[0]
        assert entity_out is e
        assert op.has(EntityOp.LEFT)
        assert not op.has(EntityOp.DELETED)
        assert e.active is False

    def test_leave_with_delete(self):
        """cmd=0b11 → LEFT | DELETED (entity removed from slot)."""
        em = self._make_em()
        e = _entity("Hero", index=0, serial=0)
        em.entities[0] = e

        raw_bits = [
            0,
            0,
            0,
            0,
            0,
            0,  # ubit_var(0)
            1,
            1,
        ]  # cmd = 11 (DELETED | LEFT)
        while len(raw_bits) % 8:
            raw_bits.append(0)
        data = bytearray()
        for i in range(0, len(raw_bits), 8):
            byte = sum(raw_bits[i + j] << j for j in range(8))
            data.append(byte)

        class Msg:
            legacy_is_delta = True
            updated_entries = 1
            entity_data = bytes(data)

        results = em.on_packet_entities(Msg())
        entity_out, op = results[0]
        assert op.has(EntityOp.DELETED)
        assert op.has(EntityOp.LEFT)
        assert em.entities[0] is None

    def test_on_entity_handler_called_on_packet(self):
        """EntityTracker._dispatch is called for each entity in packet."""
        em = self._make_em()
        e = _entity("Hero", index=0, serial=0)
        em.entities[0] = e
        dispatched = []
        em.on_entity(lambda ent, op: dispatched.append((ent, op)))

        raw_bits = [0, 0, 0, 0, 0, 0, 1, 0]  # ubit_var(0), cmd=01 (leave)
        while len(raw_bits) % 8:
            raw_bits.append(0)
        data = bytearray(
            sum(raw_bits[i + j] << j for j in range(8)) for i in range(0, len(raw_bits), 8)
        )

        class Msg:
            legacy_is_delta = True
            updated_entries = 1
            entity_data = bytes(data)

        em.on_packet_entities(Msg())
        assert len(dispatched) == 1
        assert dispatched[0][0] is e

    def test_internal_packet_path_dispatches_without_results(self):
        """The parser-only path applies updates without building result tuples."""
        em = self._make_em()
        e = _entity("Hero", index=0, serial=0)
        em.entities[0] = e
        dispatched = []
        em.on_entity(lambda ent, op: dispatched.append((ent, op)))

        data = self._pack_bits([0, 0, 0, 0, 0, 0, 1, 0])

        class Msg:
            legacy_is_delta = True
            updated_entries = 1
            entity_data = data

        result = em._on_packet_entities(Msg())

        assert result is None
        assert len(dispatched) == 1
        assert dispatched[0][0] is e
        assert e.active is False

    @staticmethod
    def _pack_bits(raw_bits: list[int]) -> bytes:
        while len(raw_bits) % 8:
            raw_bits.append(0)
        return bytes(
            sum(raw_bits[i + j] << j for j in range(8)) for i in range(0, len(raw_bits), 8)
        )

    def test_leave_on_inactive_entity_raises(self):
        """A LEAVE for an already-inactive entity is rejected (B9 — manta panics)."""
        em = self._make_em()
        e = _entity("Hero", index=0, serial=0)
        e.active = False  # already inactive
        em.entities[0] = e

        # ubit_var(0) + cmd=0b01 (leave, no delete)
        data = self._pack_bits([0, 0, 0, 0, 0, 0, 1, 0])

        class Msg:
            legacy_is_delta = True
            updated_entries = 1
            entity_data = data

        with pytest.raises(RuntimeError, match="already inactive"):
            em.on_packet_entities(Msg())

    def test_create_without_baseline_raises(self):
        """A CREATE for a class with no registered baseline is rejected (B8)."""
        em = self._make_em()

        # Register class id 3 so classes_by_id resolves, but DO NOT add a baseline.
        class FakeClassEntry:
            class_id = 3
            network_name = "CDOTA_Unit_Hero_Axe"

        class ClassMsg:
            classes = [FakeClassEntry()]

        em.on_class_info(ClassMsg())
        assert 3 not in em.class_baselines

        # Build a CREATE: ubit_var(0) + cmd=0b10 + class_id=3 (9 bits) +
        # serial=0 (17 bits) + varuint32(0) (8 bits).
        bits: list[int] = []
        bits += [0, 0, 0, 0, 0, 0]  # ubit_var(0)
        bits += [0, 1]  # cmd=0b10 (create): bit0=0, bit1=1
        for i in range(em.class_id_size):  # class_id=3, LSB-first
            bits.append((3 >> i) & 1)
        bits += [0] * 17  # serial=0
        bits += [0] * 8  # varuint32(0)
        data = self._pack_bits(bits)

        class Msg:
            legacy_is_delta = True
            updated_entries = 1
            entity_data = data

        with pytest.raises(RuntimeError, match="baseline"):
            em.on_packet_entities(Msg())
