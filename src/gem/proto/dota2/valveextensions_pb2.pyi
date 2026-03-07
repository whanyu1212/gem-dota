from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EProtoDebugVisiblity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EProtoDebugVisibility_Always: _ClassVar[EProtoDebugVisiblity]
    k_EProtoDebugVisibility_Server: _ClassVar[EProtoDebugVisiblity]
    k_EProtoDebugVisibility_ValveServer: _ClassVar[EProtoDebugVisiblity]
    k_EProtoDebugVisibility_GC: _ClassVar[EProtoDebugVisiblity]
    k_EProtoDebugVisibility_Never: _ClassVar[EProtoDebugVisiblity]

k_EProtoDebugVisibility_Always: EProtoDebugVisiblity
k_EProtoDebugVisibility_Server: EProtoDebugVisiblity
k_EProtoDebugVisibility_ValveServer: EProtoDebugVisiblity
k_EProtoDebugVisibility_GC: EProtoDebugVisiblity
k_EProtoDebugVisibility_Never: EProtoDebugVisiblity
VALVE_MAP_FIELD_FIELD_NUMBER: _ClassVar[int]
valve_map_field: _descriptor.FieldDescriptor
VALVE_MAP_KEY_FIELD_NUMBER: _ClassVar[int]
valve_map_key: _descriptor.FieldDescriptor
DIFF_ENCODE_FIELD_FIELD_NUMBER: _ClassVar[int]
diff_encode_field: _descriptor.FieldDescriptor
DELTA_IGNORE_FIELD_NUMBER: _ClassVar[int]
delta_ignore: _descriptor.FieldDescriptor
STEAMML_MAX_ENTRIES_FIELD_NUMBER: _ClassVar[int]
steamml_max_entries: _descriptor.FieldDescriptor
STEAMML_IS_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
steamml_is_timestamp: _descriptor.FieldDescriptor
STEAMLEARN_COUNT_FIELD_NUMBER: _ClassVar[int]
steamlearn_count: _descriptor.FieldDescriptor
DEBUGPRINT_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
debugprint_visibility: _descriptor.FieldDescriptor
SCHEMA_FRIENDLY_NAME_FIELD_NUMBER: _ClassVar[int]
schema_friendly_name: _descriptor.FieldDescriptor
SCHEMA_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
schema_description: _descriptor.FieldDescriptor
SCHEMA_SUPPRESS_ENUMERATOR_FIELD_NUMBER: _ClassVar[int]
schema_suppress_enumerator: _descriptor.FieldDescriptor
