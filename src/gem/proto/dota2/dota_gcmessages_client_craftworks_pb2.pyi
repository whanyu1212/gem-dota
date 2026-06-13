import steammessages_pb2 as _steammessages_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_gcmessages_webapi_pb2 as _dota_gcmessages_webapi_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
import base_gcmessages_pb2 as _base_gcmessages_pb2
import econ_gcmessages_pb2 as _econ_gcmessages_pb2
import dota_gcmessages_client_pb2 as _dota_gcmessages_client_pb2
import valveextensions_pb2 as _valveextensions_pb2
import dota_gcmessages_common_craftworks_pb2 as _dota_gcmessages_common_craftworks_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgCraftworksUserData(_message.Message):
    __slots__ = ("component_inventory",)
    COMPONENT_INVENTORY_FIELD_NUMBER: _ClassVar[int]
    component_inventory: _dota_gcmessages_common_craftworks_pb2.CMsgCraftworksComponents
    def __init__(self, component_inventory: _Optional[_Union[_dota_gcmessages_common_craftworks_pb2.CMsgCraftworksComponents, _Mapping]] = ...) -> None: ...

class CMsgClientToGCCraftworksGetUserData(_message.Message):
    __slots__ = ("craftworks_id",)
    CRAFTWORKS_ID_FIELD_NUMBER: _ClassVar[int]
    craftworks_id: int
    def __init__(self, craftworks_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCCraftworksGetUserDataResponse(_message.Message):
    __slots__ = ("response", "user_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCraftworksGetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCraftworksGetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCraftworksGetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCraftworksGetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCraftworksGetUserDataResponse.EResponse]
        k_eInvalidCraftworks: _ClassVar[CMsgClientToGCCraftworksGetUserDataResponse.EResponse]
        k_eExpiredCraftworks: _ClassVar[CMsgClientToGCCraftworksGetUserDataResponse.EResponse]
    k_eInternalError: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    k_eInvalidCraftworks: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    k_eExpiredCraftworks: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCraftworksGetUserDataResponse.EResponse
    user_data: CMsgCraftworksUserData
    def __init__(self, response: _Optional[_Union[CMsgClientToGCCraftworksGetUserDataResponse.EResponse, str]] = ..., user_data: _Optional[_Union[CMsgCraftworksUserData, _Mapping]] = ...) -> None: ...

class CMsgGCToClientCraftworksUserDataUpdated(_message.Message):
    __slots__ = ("craftworks_id", "user_data")
    CRAFTWORKS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    craftworks_id: int
    user_data: CMsgCraftworksUserData
    def __init__(self, craftworks_id: _Optional[int] = ..., user_data: _Optional[_Union[CMsgCraftworksUserData, _Mapping]] = ...) -> None: ...

class CMsgClientToGCCraftworksCraftRecipe(_message.Message):
    __slots__ = ("craftworks_id", "recipe_id")
    CRAFTWORKS_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPE_ID_FIELD_NUMBER: _ClassVar[int]
    craftworks_id: int
    recipe_id: int
    def __init__(self, craftworks_id: _Optional[int] = ..., recipe_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCCraftworksCraftRecipeResponse(_message.Message):
    __slots__ = ("response", "claim_response")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eInvalidCraftworks: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eExpiredCraftworks: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eNotEnoughComponents: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eInvalidRecipe: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eRecipeTierLocked: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
        k_eAlreadyCraftedMaxAmount: _ClassVar[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse]
    k_eInternalError: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eSuccess: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eTooBusy: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eDisabled: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eTimeout: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eInvalidCraftworks: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eExpiredCraftworks: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eNotEnoughComponents: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eInvalidRecipe: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eRecipeTierLocked: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    k_eAlreadyCraftedMaxAmount: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCraftworksCraftRecipeResponse.EResponse
    claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCCraftworksCraftRecipeResponse.EResponse, str]] = ..., claim_response: _Optional[_Union[_dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse, _Mapping]] = ...) -> None: ...

class CMsgClientToGCCraftworksDevModifyComponents(_message.Message):
    __slots__ = ("craftworks_id", "components", "operation")
    class EOperation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eAddComponents: _ClassVar[CMsgClientToGCCraftworksDevModifyComponents.EOperation]
        k_eSubtractComponents: _ClassVar[CMsgClientToGCCraftworksDevModifyComponents.EOperation]
    k_eAddComponents: CMsgClientToGCCraftworksDevModifyComponents.EOperation
    k_eSubtractComponents: CMsgClientToGCCraftworksDevModifyComponents.EOperation
    CRAFTWORKS_ID_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    craftworks_id: int
    components: _dota_gcmessages_common_craftworks_pb2.CMsgCraftworksComponents
    operation: CMsgClientToGCCraftworksDevModifyComponents.EOperation
    def __init__(self, craftworks_id: _Optional[int] = ..., components: _Optional[_Union[_dota_gcmessages_common_craftworks_pb2.CMsgCraftworksComponents, _Mapping]] = ..., operation: _Optional[_Union[CMsgClientToGCCraftworksDevModifyComponents.EOperation, str]] = ...) -> None: ...

class CMsgClientToGCCraftworksDevModifyComponentsResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse]
        k_eInvalidCraftworks: _ClassVar[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse]
    k_eInternalError: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    k_eSuccess: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    k_eTooBusy: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    k_eDisabled: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    k_eTimeout: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    k_eInvalidCraftworks: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse, str]] = ...) -> None: ...
