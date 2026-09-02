from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EBaseClientMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CM_CustomGameEvent: _ClassVar[EBaseClientMessages]
    CM_CustomGameEventBounce: _ClassVar[EBaseClientMessages]
    CM_ClientUIEvent: _ClassVar[EBaseClientMessages]
    CM_DevPaletteVisibilityChanged: _ClassVar[EBaseClientMessages]
    CM_WorldUIControllerHasPanelChanged: _ClassVar[EBaseClientMessages]
    CM_RotateAnchor: _ClassVar[EBaseClientMessages]
    CM_MAX_BASE: _ClassVar[EBaseClientMessages]

class EClientUIEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EClientUIEvent_Invalid: _ClassVar[EClientUIEvent]
    EClientUIEvent_DialogFinished: _ClassVar[EClientUIEvent]
    EClientUIEvent_FireOutput: _ClassVar[EClientUIEvent]
CM_CustomGameEvent: EBaseClientMessages
CM_CustomGameEventBounce: EBaseClientMessages
CM_ClientUIEvent: EBaseClientMessages
CM_DevPaletteVisibilityChanged: EBaseClientMessages
CM_WorldUIControllerHasPanelChanged: EBaseClientMessages
CM_RotateAnchor: EBaseClientMessages
CM_MAX_BASE: EBaseClientMessages
EClientUIEvent_Invalid: EClientUIEvent
EClientUIEvent_DialogFinished: EClientUIEvent
EClientUIEvent_FireOutput: EClientUIEvent

class CClientMsg_CustomGameEvent(_message.Message):
    __slots__ = ("event_name", "data")
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    data: bytes
    def __init__(self, event_name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class CClientMsg_CustomGameEventBounce(_message.Message):
    __slots__ = ("event_name", "data", "player_slot")
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    data: bytes
    player_slot: int
    def __init__(self, event_name: _Optional[str] = ..., data: _Optional[bytes] = ..., player_slot: _Optional[int] = ...) -> None: ...

class CClientMsg_ClientUIEvent(_message.Message):
    __slots__ = ("event", "ent_ehandle", "client_ehandle", "data1", "data2")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    ENT_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    DATA1_FIELD_NUMBER: _ClassVar[int]
    DATA2_FIELD_NUMBER: _ClassVar[int]
    event: EClientUIEvent
    ent_ehandle: int
    client_ehandle: int
    data1: str
    data2: str
    def __init__(self, event: _Optional[_Union[EClientUIEvent, str]] = ..., ent_ehandle: _Optional[int] = ..., client_ehandle: _Optional[int] = ..., data1: _Optional[str] = ..., data2: _Optional[str] = ...) -> None: ...

class CClientMsg_DevPaletteVisibilityChangedEvent(_message.Message):
    __slots__ = ("visible",)
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    visible: bool
    def __init__(self, visible: bool = ...) -> None: ...

class CClientMsg_WorldUIControllerHasPanelChangedEvent(_message.Message):
    __slots__ = ("has_panel", "client_ehandle", "literal_hand_type")
    HAS_PANEL_FIELD_NUMBER: _ClassVar[int]
    CLIENT_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    LITERAL_HAND_TYPE_FIELD_NUMBER: _ClassVar[int]
    has_panel: bool
    client_ehandle: int
    literal_hand_type: int
    def __init__(self, has_panel: bool = ..., client_ehandle: _Optional[int] = ..., literal_hand_type: _Optional[int] = ...) -> None: ...

class CClientMsg_RotateAnchor(_message.Message):
    __slots__ = ("angle",)
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    angle: float
    def __init__(self, angle: _Optional[float] = ...) -> None: ...
