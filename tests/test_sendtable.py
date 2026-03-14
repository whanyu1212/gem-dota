"""
Tests for gem.sendtable — send table parsing, FieldType, Field, Serializer.

Reference: manta/sendtable.go, manta/field.go, manta/field_type.go
"""

import pytest

# ---------------------------------------------------------------------------
# FieldType parsing
# ---------------------------------------------------------------------------


class TestFieldTypeParsing:
    @pytest.fixture
    def parse(self):
        from gem.sendtable import _parse_field_type

        return _parse_field_type

    def test_simple_type(self, parse):
        ft = parse("uint32")
        assert ft.base_type == "uint32"
        assert ft.generic_type is None
        assert not ft.pointer
        assert ft.count == 0

    def test_fixed_array_numeric_count(self, parse):
        ft = parse("CHandle[24]")
        assert ft.base_type == "CHandle"
        assert ft.count == 24

    def test_fixed_array_named_count(self, parse):
        ft = parse("CHandle[MAX_ITEM_STOCKS]")
        assert ft.base_type == "CHandle"
        assert ft.count == 8

    def test_pointer_type(self, parse):
        ft = parse("CBodyComponent*")
        assert ft.base_type == "CBodyComponent"
        assert ft.pointer is True

    def test_generic_type(self, parse):
        ft = parse("CUtlVector< int32 >")
        assert ft.base_type == "CUtlVector"
        assert ft.generic_type is not None
        assert ft.generic_type.base_type == "int32"

    def test_str_roundtrip_simple(self, parse):
        assert str(parse("uint32")) == "uint32"

    def test_str_roundtrip_array(self, parse):
        ft = parse("CHandle[24]")
        assert "CHandle" in str(ft)
        assert "24" in str(ft)

    def test_unknown_named_count_defaults_to_1024(self, parse):
        ft = parse("SomeType[SOME_UNKNOWN_CONSTANT]")
        assert ft.count == 1024


# ---------------------------------------------------------------------------
# Field model determination
# ---------------------------------------------------------------------------


class TestFieldModel:
    @pytest.fixture
    def field_cls(self):
        from gem.sendtable import Field, FieldType

        return Field, FieldType

    def test_simple_model(self, field_cls):
        Field, FieldType = field_cls
        from gem.sendtable import FIELD_MODEL_SIMPLE

        f = Field(
            var_name="m_iHealth",
            var_type="uint32",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        f.field_type = FieldType("uint32")
        f.set_model(FIELD_MODEL_SIMPLE)
        assert f.model_name() == "simple"
        assert f.decoder is not None

    def test_fixed_array_model(self, field_cls):
        Field, FieldType = field_cls
        from gem.sendtable import FIELD_MODEL_FIXED_ARRAY

        f = Field(
            var_name="m_hAbilities",
            var_type="CHandle[24]",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        f.field_type = FieldType("CHandle", count=24)
        f.set_model(FIELD_MODEL_FIXED_ARRAY)
        assert f.model_name() == "fixed-array"
        assert f.decoder is not None

    def test_variable_array_model(self, field_cls):
        Field, FieldType = field_cls
        from gem.sendtable import FIELD_MODEL_VARIABLE_ARRAY

        f = Field(
            var_name="m_vecItems",
            var_type="CUtlVector< uint32 >",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        inner = FieldType("uint32")
        f.field_type = FieldType("CUtlVector", generic_type=inner)
        f.set_model(FIELD_MODEL_VARIABLE_ARRAY)
        assert f.model_name() == "variable-array"
        assert f.base_decoder is not None
        assert f.child_decoder is not None

    def test_fixed_table_model(self, field_cls):
        Field, FieldType = field_cls
        from gem.sendtable import FIELD_MODEL_FIXED_TABLE

        f = Field(
            var_name="m_pEntity",
            var_type="CEntityIdentity",
            send_node="",
            serializer_name="CEntityIdentity",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        f.field_type = FieldType("CEntityIdentity", pointer=True)
        f.set_model(FIELD_MODEL_FIXED_TABLE)
        assert f.model_name() == "fixed-table"
        assert f.base_decoder is not None


# ---------------------------------------------------------------------------
# Field patches
# ---------------------------------------------------------------------------


class TestFieldPatches:
    @pytest.fixture
    def patch_list(self):
        from gem.sendtable import _FIELD_PATCHES

        return _FIELD_PATCHES

    def test_always_on_patch_applies_at_any_build(self, patch_list):
        always_on = [p for p in patch_list if p.min_build == 0 and p.max_build == 0]
        assert len(always_on) > 0
        for p in always_on:
            assert p.should_apply(0)
            assert p.should_apply(9999)

    def test_range_patch_applies_within_range(self, patch_list):
        ranged = [p for p in patch_list if p.max_build > 0]
        assert len(ranged) > 0
        for p in ranged:
            assert p.should_apply(p.min_build)
            assert p.should_apply(p.max_build)
            assert not p.should_apply(p.max_build + 1)

    def test_simtime_patch_sets_encoder(self, patch_list):
        from gem.sendtable import Field, FieldType

        always_on = next(p for p in patch_list if p.min_build == 0 and p.max_build == 0)
        f = Field(
            var_name="m_flSimulationTime",
            var_type="float32",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        f.field_type = FieldType("float32")
        always_on.patch(f)
        assert f.encoder == "simtime"


# ---------------------------------------------------------------------------
# parse_send_tables — integration against a real truncated fixture
# ---------------------------------------------------------------------------


class TestParseSendTables:
    @pytest.fixture
    def sendtable_data(self):
        """Extract CDemoSendTables payload from the truncated fixture."""
        from pathlib import Path

        from gem.proto.dota2 import (
            network_connection_pb2,  # noqa: F401
            networkbasetypes_pb2,  # noqa: F401
        )
        from gem.stream import DemoStream

        fixture = Path(__file__).parent / "fixtures"
        dem_files = list(fixture.glob("*_truncated.dem"))
        if not dem_files:
            pytest.skip("No truncated fixture found")

        # EDemoCommands.DEM_SendTables = 4
        DEM_SEND_TABLES = 4
        with DemoStream(dem_files[0]) as stream:
            for _tick, msg_type, data in stream:
                if (msg_type & ~0x40) == DEM_SEND_TABLES:
                    return data

        pytest.skip("CDemoSendTables not found in truncated fixture")

    def test_returns_nonempty_dict(self, sendtable_data):
        from gem.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        assert isinstance(serializers, dict)
        assert len(serializers) > 0

    def test_known_entity_classes_present(self, sendtable_data):
        from gem.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        # These classes appear in every Dota 2 replay
        for name in ("CDOTAGamerulesProxy", "CDOTA_BaseNPC", "CWorld"):
            assert name in serializers, f"Missing expected serializer: {name}"

    def test_fields_have_decoders(self, sendtable_data):
        from gem.sendtable import FIELD_MODEL_SIMPLE, parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        errors = []
        for s in list(serializers.values())[:20]:  # spot-check first 20
            for f in s.fields:
                if f.model == FIELD_MODEL_SIMPLE and f.decoder is None:
                    errors.append(f"{s.name}.{f.var_name}")
        assert not errors, f"Fields with no decoder: {errors[:5]}"

    def test_field_types_parsed(self, sendtable_data):
        from gem.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        for s in list(serializers.values())[:10]:
            for f in s.fields:
                assert f.field_type.base_type, f"Empty base_type for {s.name}.{f.var_name}"

    def test_serializer_repr(self, sendtable_data):
        from gem.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        s = next(iter(serializers.values()))
        r = repr(s)
        assert "Serializer(" in r
        assert "fields" in r
