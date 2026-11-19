from . import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from . import events_pb2 as _events_pb2
from . import event_gcmessages_common_pb2 as _event_gcmessages_common_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EGCEventClientMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMsgClientToGCGetEventPoints: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCGetEventPointsResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgGCToClientEventPointsUpdated: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevGrantEventPoints: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevGrantEventPointsResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevReloadEventSchema: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevReloadEventSchemaResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevResetEventState: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevResetEventStateResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevGrantEventAction: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevGrantEventActionResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevResetEventActions: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCDevResetEventActionsResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCClaimEventAction: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCClaimEventActionResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCGetPeriodicResource: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCGetPeriodicResourceResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgGCToClientPeriodicResourceUpdated: _ClassVar[EGCEventClientMessages]
k_EMsgClientToGCGetEventPoints: EGCEventClientMessages
k_EMsgClientToGCGetEventPointsResponse: EGCEventClientMessages
k_EMsgGCToClientEventPointsUpdated: EGCEventClientMessages
k_EMsgClientToGCDevGrantEventPoints: EGCEventClientMessages
k_EMsgClientToGCDevGrantEventPointsResponse: EGCEventClientMessages
k_EMsgClientToGCDevReloadEventSchema: EGCEventClientMessages
k_EMsgClientToGCDevReloadEventSchemaResponse: EGCEventClientMessages
k_EMsgClientToGCDevResetEventState: EGCEventClientMessages
k_EMsgClientToGCDevResetEventStateResponse: EGCEventClientMessages
k_EMsgClientToGCDevGrantEventAction: EGCEventClientMessages
k_EMsgClientToGCDevGrantEventActionResponse: EGCEventClientMessages
k_EMsgClientToGCDevResetEventActions: EGCEventClientMessages
k_EMsgClientToGCDevResetEventActionsResponse: EGCEventClientMessages
k_EMsgClientToGCClaimEventAction: EGCEventClientMessages
k_EMsgClientToGCClaimEventActionResponse: EGCEventClientMessages
k_EMsgClientToGCGetPeriodicResource: EGCEventClientMessages
k_EMsgClientToGCGetPeriodicResourceResponse: EGCEventClientMessages
k_EMsgGCToClientPeriodicResourceUpdated: EGCEventClientMessages

class CMsgClientToGCGetEventPoints(_message.Message):
    __slots__ = ("event_id", "account_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    account_id: int
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., account_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCGetEventPointsResponse(_message.Message):
    __slots__ = ("result", "event_points")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
    k_eInternalError: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eSuccess: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eDisabled: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eTimeout: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCGetEventPointsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetEventPointsResponse.EResponse
    event_points: _event_gcmessages_common_pb2.CMsgUserEventPoints
    def __init__(self, result: _Optional[_Union[CMsgClientToGCGetEventPointsResponse.EResponse, str]] = ..., event_points: _Optional[_Union[_event_gcmessages_common_pb2.CMsgUserEventPoints, _Mapping]] = ...) -> None: ...

class CMsgGCToClientEventPointsUpdated(_message.Message):
    __slots__ = ("event_id", "event_points", "audit_action")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    event_points: _event_gcmessages_common_pb2.CMsgUserEventPoints
    audit_action: int
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., event_points: _Optional[_Union[_event_gcmessages_common_pb2.CMsgUserEventPoints, _Mapping]] = ..., audit_action: _Optional[int] = ...) -> None: ...

class CMsgClientToGCGetPeriodicResource(_message.Message):
    __slots__ = ("account_id", "periodic_resource_id", "timestamp")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    periodic_resource_id: int
    timestamp: int
    def __init__(self, account_id: _Optional[int] = ..., periodic_resource_id: _Optional[int] = ..., timestamp: _Optional[int] = ...) -> None: ...

class CMsgClientToGCGetPeriodicResourceResponse(_message.Message):
    __slots__ = ("result", "periodic_resource_value")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetPeriodicResourceResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetPeriodicResourceResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetPeriodicResourceResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetPeriodicResourceResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetPeriodicResourceResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCGetPeriodicResourceResponse.EResponse]
    k_eInternalError: CMsgClientToGCGetPeriodicResourceResponse.EResponse
    k_eSuccess: CMsgClientToGCGetPeriodicResourceResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetPeriodicResourceResponse.EResponse
    k_eDisabled: CMsgClientToGCGetPeriodicResourceResponse.EResponse
    k_eTimeout: CMsgClientToGCGetPeriodicResourceResponse.EResponse
    k_eNotAllowed: CMsgClientToGCGetPeriodicResourceResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetPeriodicResourceResponse.EResponse
    periodic_resource_value: _event_gcmessages_common_pb2.CMsgPeriodicResourceValue
    def __init__(self, result: _Optional[_Union[CMsgClientToGCGetPeriodicResourceResponse.EResponse, str]] = ..., periodic_resource_value: _Optional[_Union[_event_gcmessages_common_pb2.CMsgPeriodicResourceValue, _Mapping]] = ...) -> None: ...

class CMsgGCToClientPeriodicResourceUpdated(_message.Message):
    __slots__ = ("periodic_resource_key", "periodic_resource_value")
    PERIODIC_RESOURCE_KEY_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    periodic_resource_key: _event_gcmessages_common_pb2.CMsgPeriodicResourceKey
    periodic_resource_value: _event_gcmessages_common_pb2.CMsgPeriodicResourceValue
    def __init__(self, periodic_resource_key: _Optional[_Union[_event_gcmessages_common_pb2.CMsgPeriodicResourceKey, _Mapping]] = ..., periodic_resource_value: _Optional[_Union[_event_gcmessages_common_pb2.CMsgPeriodicResourceValue, _Mapping]] = ...) -> None: ...

class CMsgClientToGCDevGrantEventPoints(_message.Message):
    __slots__ = ("event_id", "event_points", "premium_points")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    event_points: int
    premium_points: int
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., event_points: _Optional[int] = ..., premium_points: _Optional[int] = ...) -> None: ...

class CMsgClientToGCDevGrantEventPointsResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
        k_eInvalidPoints: _ClassVar[CMsgClientToGCDevGrantEventPointsResponse.EResponse]
    k_eInternalError: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    k_eSuccess: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    k_eTooBusy: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    k_eDisabled: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    k_eTimeout: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    k_eInvalidPoints: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCDevGrantEventPointsResponse.EResponse
    def __init__(self, result: _Optional[_Union[CMsgClientToGCDevGrantEventPointsResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCDevReloadEventSchema(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCDevReloadEventSchemaResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDevReloadEventSchemaResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDevReloadEventSchemaResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDevReloadEventSchemaResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCDevReloadEventSchemaResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDevReloadEventSchemaResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCDevReloadEventSchemaResponse.EResponse]
    k_eInternalError: CMsgClientToGCDevReloadEventSchemaResponse.EResponse
    k_eSuccess: CMsgClientToGCDevReloadEventSchemaResponse.EResponse
    k_eTooBusy: CMsgClientToGCDevReloadEventSchemaResponse.EResponse
    k_eDisabled: CMsgClientToGCDevReloadEventSchemaResponse.EResponse
    k_eTimeout: CMsgClientToGCDevReloadEventSchemaResponse.EResponse
    k_eNotAllowed: CMsgClientToGCDevReloadEventSchemaResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCDevReloadEventSchemaResponse.EResponse
    def __init__(self, result: _Optional[_Union[CMsgClientToGCDevReloadEventSchemaResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCDevResetEventState(_message.Message):
    __slots__ = ("event_id", "remove_audit")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    REMOVE_AUDIT_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    remove_audit: bool
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., remove_audit: bool = ...) -> None: ...

class CMsgClientToGCDevResetEventStateResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDevResetEventStateResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDevResetEventStateResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDevResetEventStateResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCDevResetEventStateResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDevResetEventStateResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCDevResetEventStateResponse.EResponse]
    k_eInternalError: CMsgClientToGCDevResetEventStateResponse.EResponse
    k_eSuccess: CMsgClientToGCDevResetEventStateResponse.EResponse
    k_eTooBusy: CMsgClientToGCDevResetEventStateResponse.EResponse
    k_eDisabled: CMsgClientToGCDevResetEventStateResponse.EResponse
    k_eTimeout: CMsgClientToGCDevResetEventStateResponse.EResponse
    k_eNotAllowed: CMsgClientToGCDevResetEventStateResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCDevResetEventStateResponse.EResponse
    def __init__(self, result: _Optional[_Union[CMsgClientToGCDevResetEventStateResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCDevGrantEventAction(_message.Message):
    __slots__ = ("event_id", "action_id", "action_score")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_SCORE_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    action_id: int
    action_score: int
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., action_id: _Optional[int] = ..., action_score: _Optional[int] = ...) -> None: ...

class CMsgClientToGCDevGrantEventActionResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eInvalidAccount: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eGrantFailed: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
        k_eNotGranted: _ClassVar[CMsgClientToGCDevGrantEventActionResponse.EResponse]
    k_eInternalError: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eSuccess: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eTooBusy: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eDisabled: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eTimeout: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eNotAllowed: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eInvalidAccount: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eGrantFailed: CMsgClientToGCDevGrantEventActionResponse.EResponse
    k_eNotGranted: CMsgClientToGCDevGrantEventActionResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCDevGrantEventActionResponse.EResponse
    def __init__(self, result: _Optional[_Union[CMsgClientToGCDevGrantEventActionResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCDevResetEventActions(_message.Message):
    __slots__ = ("event_id", "start_action_id", "end_action_id", "remove_audit")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    START_ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    END_ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    REMOVE_AUDIT_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    start_action_id: int
    end_action_id: int
    remove_audit: bool
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., start_action_id: _Optional[int] = ..., end_action_id: _Optional[int] = ..., remove_audit: bool = ...) -> None: ...

class CMsgClientToGCDevResetEventActionsResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
        k_eInvalidAccount: _ClassVar[CMsgClientToGCDevResetEventActionsResponse.EResponse]
    k_eInternalError: CMsgClientToGCDevResetEventActionsResponse.EResponse
    k_eSuccess: CMsgClientToGCDevResetEventActionsResponse.EResponse
    k_eTooBusy: CMsgClientToGCDevResetEventActionsResponse.EResponse
    k_eDisabled: CMsgClientToGCDevResetEventActionsResponse.EResponse
    k_eTimeout: CMsgClientToGCDevResetEventActionsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCDevResetEventActionsResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCDevResetEventActionsResponse.EResponse
    k_eInvalidAccount: CMsgClientToGCDevResetEventActionsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCDevResetEventActionsResponse.EResponse
    def __init__(self, result: _Optional[_Union[CMsgClientToGCDevResetEventActionsResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCClaimEventAction(_message.Message):
    __slots__ = ("event_id", "action_id", "quantity", "score_mode", "suppress_rewards", "claim_data", "consume_item_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SCORE_MODE_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_REWARDS_FIELD_NUMBER: _ClassVar[int]
    CLAIM_DATA_FIELD_NUMBER: _ClassVar[int]
    CONSUME_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    action_id: int
    quantity: int
    score_mode: _event_gcmessages_common_pb2.EEventActionScoreMode
    suppress_rewards: bool
    claim_data: bytes
    consume_item_id: int
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., action_id: _Optional[int] = ..., quantity: _Optional[int] = ..., score_mode: _Optional[_Union[_event_gcmessages_common_pb2.EEventActionScoreMode, str]] = ..., suppress_rewards: bool = ..., claim_data: _Optional[bytes] = ..., consume_item_id: _Optional[int] = ...) -> None: ...

class CMsgEventActionGrantLootListRewardData(_message.Message):
    __slots__ = ("item_def",)
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    item_def: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item_def: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgEventActionGrantResult(_message.Message):
    __slots__ = ("action_id", "grant_index", "score_index", "reward_index", "grant_data")
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    GRANT_INDEX_FIELD_NUMBER: _ClassVar[int]
    SCORE_INDEX_FIELD_NUMBER: _ClassVar[int]
    REWARD_INDEX_FIELD_NUMBER: _ClassVar[int]
    GRANT_DATA_FIELD_NUMBER: _ClassVar[int]
    action_id: int
    grant_index: int
    score_index: int
    reward_index: int
    grant_data: bytes
    def __init__(self, action_id: _Optional[int] = ..., grant_index: _Optional[int] = ..., score_index: _Optional[int] = ..., reward_index: _Optional[int] = ..., grant_data: _Optional[bytes] = ...) -> None: ...

class CMsgClientToGCClaimEventActionResponse(_message.Message):
    __slots__ = ("result", "grant_results")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eInvalidAction: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eEventNotActive: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eEventNotOwned: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eInsufficientLevel: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eInsufficientPoints: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eAlreadyClaimed: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eInvalidScoreMode: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eRequiresSubscription: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
        k_eInvalidItem: _ClassVar[CMsgClientToGCClaimEventActionResponse.EResponse]
    k_eInternalError: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eSuccess: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eTooBusy: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eDisabled: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eTimeout: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eNotAllowed: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eInvalidAction: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eEventNotActive: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eEventNotOwned: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eInsufficientLevel: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eInsufficientPoints: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eAlreadyClaimed: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eInvalidScoreMode: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eRequiresSubscription: CMsgClientToGCClaimEventActionResponse.EResponse
    k_eInvalidItem: CMsgClientToGCClaimEventActionResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    GRANT_RESULTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCClaimEventActionResponse.EResponse
    grant_results: _containers.RepeatedCompositeFieldContainer[CMsgEventActionGrantResult]
    def __init__(self, result: _Optional[_Union[CMsgClientToGCClaimEventActionResponse.EResponse, str]] = ..., grant_results: _Optional[_Iterable[_Union[CMsgEventActionGrantResult, _Mapping]]] = ...) -> None: ...
