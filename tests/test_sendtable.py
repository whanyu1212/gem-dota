"""
Tests for gem.schema.sendtable — send table parsing, FieldType, Field, Serializer.

Reference: manta/sendtable.go, manta/field.go, manta/field_type.go
"""

import pytest


def _pack_varuint32(value: int) -> bytes:
    out = bytearray()
    while value >= 0x80:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def _wrap_flattened_serializer(flattened: object) -> bytes:
    from gem.proto.demo_pb2 import CDemoSendTables

    payload = flattened.SerializeToString()
    return CDemoSendTables(data=_pack_varuint32(len(payload)) + payload).SerializeToString()


# ---------------------------------------------------------------------------
# FieldType parsing
# ---------------------------------------------------------------------------


class TestFieldTypeParsing:
    @pytest.fixture
    def parse(self):
        from gem.schema.sendtable import _parse_field_type

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

    def test_str_roundtrip_generic_and_pointer(self, parse):
        assert str(parse("CUtlVector< int32 >")) == "CUtlVector<int32>"
        assert str(parse("CBodyComponent*")) == "CBodyComponent*"

    def test_unknown_named_count_defaults_to_1024(self, parse):
        ft = parse("SomeType[SOME_UNKNOWN_CONSTANT]")
        assert ft.count == 1024

    def test_invalid_type_raises_value_error(self, parse):
        with pytest.raises(ValueError, match="Cannot parse field type"):
            parse("")


# ---------------------------------------------------------------------------
# Field model determination
# ---------------------------------------------------------------------------


class TestFieldModel:
    @pytest.fixture
    def field_cls(self):
        from gem.schema.sendtable import Field, FieldType

        return Field, FieldType

    def test_simple_model(self, field_cls):
        Field, FieldType = field_cls
        from gem.schema.sendtable import FIELD_MODEL_SIMPLE

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
        from gem.schema.sendtable import FIELD_MODEL_FIXED_ARRAY

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
        from gem.schema.sendtable import FIELD_MODEL_VARIABLE_ARRAY

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
        from gem.schema.sendtable import FIELD_MODEL_FIXED_TABLE

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

    def test_variable_array_without_generic_raises(self, field_cls):
        Field, FieldType = field_cls
        from gem.schema.sendtable import FIELD_MODEL_VARIABLE_ARRAY

        f = Field(
            var_name="m_vecItems",
            var_type="CUtlVector",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        f.field_type = FieldType("CUtlVector")

        with pytest.raises(ValueError, match="has no generic type"):
            f.set_model(FIELD_MODEL_VARIABLE_ARRAY)

    def test_unknown_model_raises(self, field_cls):
        Field, FieldType = field_cls

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

        with pytest.raises(ValueError, match="unknown field model 999"):
            f.set_model(999)


# ---------------------------------------------------------------------------
# Field patches
# ---------------------------------------------------------------------------


class TestFieldPatches:
    @pytest.fixture
    def patch_list(self):
        from gem.schema.sendtable import _FIELD_PATCHES

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
        from gem.schema.sendtable import Field, FieldType

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

    def test_pre991_patch_sets_normal_encoder(self, patch_list):
        from gem.schema.sendtable import Field, FieldType

        pre991 = next(p for p in patch_list if p.min_build == 0 and p.max_build == 990)
        f = Field(
            var_name="m_vecLadderNormal",
            var_type="Vector",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        f.field_type = FieldType("Vector")

        pre991.patch(f)

        assert f.encoder == "normal"

    def test_1016_1027_patch_sets_fixed64_encoder(self, patch_list):
        from gem.schema.sendtable import Field, FieldType

        patch = next(p for p in patch_list if p.min_build == 1016 and p.max_build == 1027)
        f = Field(
            var_name="m_iPlayerSteamID",
            var_type="uint64",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        f.field_type = FieldType("uint64")

        patch.patch(f)

        assert f.encoder == "fixed64"


# ---------------------------------------------------------------------------
# parse_send_tables — integration against a real truncated fixture
# ---------------------------------------------------------------------------


class TestParseSendTables:
    def test_symbol_none_returns_empty_string(self):
        from gem.schema.sendtable.parser import _symbol

        assert _symbol(["Serializer"], None, "optional") == ""

    def test_empty_inner_payload_raises_buffer_read_error(self):
        from gem.binary.reader import BufferReadError
        from gem.proto.demo_pb2 import CDemoSendTables
        from gem.schema.sendtable import parse_send_tables

        payload = CDemoSendTables(data=b"").SerializeToString()

        with pytest.raises(BufferReadError):
            parse_send_tables(payload)

    def test_declared_inner_payload_size_larger_than_buffer_raises(self):
        from gem.binary.reader import BufferReadError
        from gem.proto.demo_pb2 import CDemoSendTables
        from gem.schema.sendtable import parse_send_tables

        payload = CDemoSendTables(data=_pack_varuint32(4) + b"\x00").SerializeToString()

        with pytest.raises(BufferReadError):
            parse_send_tables(payload)

    def test_invalid_outer_protobuf_raises_value_error(self):
        from gem.schema.sendtable import parse_send_tables

        with pytest.raises(ValueError, match="invalid CDemoSendTables payload"):
            parse_send_tables(b"\xff")

    def test_invalid_inner_protobuf_raises_value_error(self):
        from gem.proto.demo_pb2 import CDemoSendTables
        from gem.schema.sendtable import parse_send_tables

        payload = CDemoSendTables(data=_pack_varuint32(1) + b"\xff").SerializeToString()

        with pytest.raises(ValueError, match="invalid CSVCMsg_FlattenedSerializer payload"):
            parse_send_tables(payload)

    def test_invalid_serializer_symbol_index_raises_value_error(self):
        from gem.proto.netmessages_pb2 import CSVCMsg_FlattenedSerializer
        from gem.schema.sendtable import parse_send_tables

        flattened = CSVCMsg_FlattenedSerializer(
            symbols=["OnlySymbol"],
            serializers=[{"serializer_name_sym": 3, "serializer_version": 1}],
        )

        with pytest.raises(ValueError, match="invalid symbol index 3"):
            parse_send_tables(_wrap_flattened_serializer(flattened))

    def test_invalid_field_index_raises_value_error(self):
        from gem.proto.netmessages_pb2 import CSVCMsg_FlattenedSerializer
        from gem.schema.sendtable import parse_send_tables

        flattened = CSVCMsg_FlattenedSerializer(
            symbols=["Serializer"],
            serializers=[{"serializer_name_sym": 0, "serializer_version": 1, "fields_index": [0]}],
        )

        with pytest.raises(ValueError, match="invalid field index 0"):
            parse_send_tables(_wrap_flattened_serializer(flattened))

    def test_unresolved_serializer_reference_raises_value_error(self):
        from gem.proto.netmessages_pb2 import CSVCMsg_FlattenedSerializer
        from gem.schema.sendtable import parse_send_tables

        flattened = CSVCMsg_FlattenedSerializer(
            symbols=["Serializer", "Missing", "Missing*", "m_missing"],
            serializers=[{"serializer_name_sym": 0, "serializer_version": 1, "fields_index": [0]}],
            fields=[
                {
                    "var_type_sym": 2,
                    "var_name_sym": 3,
                    "field_serializer_name_sym": 1,
                    "field_serializer_version": 1,
                }
            ],
        )

        with pytest.raises(ValueError, match="unresolved serializer reference 'Missing'"):
            parse_send_tables(_wrap_flattened_serializer(flattened))

    def test_variable_array_without_generic_raises_value_error(self):
        from gem.proto.netmessages_pb2 import CSVCMsg_FlattenedSerializer
        from gem.schema.sendtable import parse_send_tables

        flattened = CSVCMsg_FlattenedSerializer(
            symbols=["Serializer", "CUtlVector", "m_vecItems"],
            serializers=[{"serializer_name_sym": 0, "serializer_version": 1, "fields_index": [0]}],
            fields=[{"var_type_sym": 1, "var_name_sym": 2}],
        )

        with pytest.raises(ValueError, match="has no generic type"):
            parse_send_tables(_wrap_flattened_serializer(flattened))

    def test_forward_serializer_reference_resolves(self):
        from gem.proto.netmessages_pb2 import CSVCMsg_FlattenedSerializer
        from gem.schema.sendtable import FIELD_MODEL_FIXED_TABLE, parse_send_tables

        flattened = CSVCMsg_FlattenedSerializer(
            symbols=["Parent", "Child", "Child*", "m_child", "uint32", "m_value"],
            serializers=[
                {"serializer_name_sym": 0, "serializer_version": 1, "fields_index": [0]},
                {"serializer_name_sym": 1, "serializer_version": 1, "fields_index": [1]},
            ],
            fields=[
                {
                    "var_type_sym": 2,
                    "var_name_sym": 3,
                    "field_serializer_name_sym": 1,
                    "field_serializer_version": 1,
                },
                {"var_type_sym": 4, "var_name_sym": 5},
            ],
        )

        serializers = parse_send_tables(_wrap_flattened_serializer(flattened))

        child = serializers["Child"]
        parent_field = serializers["Parent"].fields[0]
        assert parent_field.serializer is child
        assert parent_field.model == FIELD_MODEL_FIXED_TABLE

    def test_root_send_node_normalized_to_empty_string(self):
        from gem.proto.netmessages_pb2 import CSVCMsg_FlattenedSerializer
        from gem.schema.sendtable import parse_send_tables

        flattened = CSVCMsg_FlattenedSerializer(
            symbols=["Serializer", "uint32", "m_value", "(root)"],
            serializers=[{"serializer_name_sym": 0, "serializer_version": 1, "fields_index": [0]}],
            fields=[{"var_type_sym": 1, "var_name_sym": 2, "send_node_sym": 3}],
        )

        serializers = parse_send_tables(_wrap_flattened_serializer(flattened))

        assert serializers["Serializer"].fields[0].send_node == ""

    @pytest.fixture
    def sendtable_data(self):
        """Extract CDemoSendTables payload from the truncated fixture."""
        from pathlib import Path

        from gem.binary.stream import DemoStream
        from gem.proto import (
            network_connection_pb2,  # noqa: F401
            networkbasetypes_pb2,  # noqa: F401
        )

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
        from gem.schema.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        assert isinstance(serializers, dict)
        assert len(serializers) > 0

    def test_known_entity_classes_present(self, sendtable_data):
        from gem.schema.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        # These classes appear in every Dota 2 replay
        for name in ("CDOTAGamerulesProxy", "CDOTA_BaseNPC", "CWorld"):
            assert name in serializers, f"Missing expected serializer: {name}"

    def test_fields_have_decoders(self, sendtable_data):
        from gem.schema.sendtable import (
            FIELD_MODEL_FIXED_ARRAY,
            FIELD_MODEL_SIMPLE,
            parse_send_tables,
        )

        serializers = parse_send_tables(sendtable_data)
        errors = []
        for s in serializers.values():
            for f in s.fields:
                if f.model in (FIELD_MODEL_SIMPLE, FIELD_MODEL_FIXED_ARRAY) and f.decoder is None:
                    errors.append(f"{s.name}.{f.var_name}")
        assert not errors, f"Fields with no decoder: {errors[:5]}"

    def test_field_types_parsed(self, sendtable_data):
        from gem.schema.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        for s in serializers.values():
            for f in s.fields:
                assert f.field_type.base_type, f"Empty base_type for {s.name}.{f.var_name}"

    def test_serializer_references_are_resolved(self, sendtable_data):
        from gem.schema.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        errors = []
        for s in serializers.values():
            for f in s.fields:
                if f.serializer_name and f.serializer is None:
                    errors.append(f"{s.name}.{f.var_name}->{f.serializer_name}")
        assert not errors, f"Unresolved serializer references: {errors[:5]}"

    def test_variable_arrays_have_generic_type_and_child_decoder(self, sendtable_data):
        from gem.schema.sendtable import FIELD_MODEL_VARIABLE_ARRAY, parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        errors = []
        for s in serializers.values():
            for f in s.fields:
                if f.model == FIELD_MODEL_VARIABLE_ARRAY and (
                    f.field_type.generic_type is None or f.child_decoder is None
                ):
                    errors.append(f"{s.name}.{f.var_name}:{f.var_type}")
        assert not errors, f"Invalid variable-array fields: {errors[:5]}"

    def test_serializer_repr(self, sendtable_data):
        from gem.schema.sendtable import parse_send_tables

        serializers = parse_send_tables(sendtable_data)
        s = next(iter(serializers.values()))
        r = repr(s)
        assert "Serializer(" in r
        assert "fields" in r
