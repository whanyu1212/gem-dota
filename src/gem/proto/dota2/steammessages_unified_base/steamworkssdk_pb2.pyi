from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EProtoExecutionSite(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EProtoExecutionSiteUnknown: _ClassVar[EProtoExecutionSite]
    k_EProtoExecutionSiteSteamClient: _ClassVar[EProtoExecutionSite]

k_EProtoExecutionSiteUnknown: EProtoExecutionSite
k_EProtoExecutionSiteSteamClient: EProtoExecutionSite
DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
description: _descriptor.FieldDescriptor
SERVICE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
service_description: _descriptor.FieldDescriptor
SERVICE_EXECUTION_SITE_FIELD_NUMBER: _ClassVar[int]
service_execution_site: _descriptor.FieldDescriptor
METHOD_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
method_description: _descriptor.FieldDescriptor
ENUM_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
enum_description: _descriptor.FieldDescriptor
ENUM_VALUE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
enum_value_description: _descriptor.FieldDescriptor
