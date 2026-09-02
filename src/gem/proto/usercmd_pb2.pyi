from . import valveextensions_pb2 as _valveextensions_pb2
from . import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CInButtonStatePB(_message.Message):
    __slots__ = ("buttonstate1", "buttonstate2", "buttonstate3")
    BUTTONSTATE1_FIELD_NUMBER: _ClassVar[int]
    BUTTONSTATE2_FIELD_NUMBER: _ClassVar[int]
    BUTTONSTATE3_FIELD_NUMBER: _ClassVar[int]
    buttonstate1: int
    buttonstate2: int
    buttonstate3: int
    def __init__(self, buttonstate1: _Optional[int] = ..., buttonstate2: _Optional[int] = ..., buttonstate3: _Optional[int] = ...) -> None: ...

class CSubtickMoveStep(_message.Message):
    __slots__ = ("button", "pressed", "when", "analog_forward_delta", "analog_left_delta", "pitch_delta", "yaw_delta")
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    PRESSED_FIELD_NUMBER: _ClassVar[int]
    WHEN_FIELD_NUMBER: _ClassVar[int]
    ANALOG_FORWARD_DELTA_FIELD_NUMBER: _ClassVar[int]
    ANALOG_LEFT_DELTA_FIELD_NUMBER: _ClassVar[int]
    PITCH_DELTA_FIELD_NUMBER: _ClassVar[int]
    YAW_DELTA_FIELD_NUMBER: _ClassVar[int]
    button: int
    pressed: bool
    when: float
    analog_forward_delta: float
    analog_left_delta: float
    pitch_delta: float
    yaw_delta: float
    def __init__(self, button: _Optional[int] = ..., pressed: bool = ..., when: _Optional[float] = ..., analog_forward_delta: _Optional[float] = ..., analog_left_delta: _Optional[float] = ..., pitch_delta: _Optional[float] = ..., yaw_delta: _Optional[float] = ...) -> None: ...

class CBaseUserCmdExecutionNotes(_message.Message):
    __slots__ = ("ignored_reason",)
    IGNORED_REASON_FIELD_NUMBER: _ClassVar[int]
    ignored_reason: str
    def __init__(self, ignored_reason: _Optional[str] = ...) -> None: ...

class CBaseUserCmdPB(_message.Message):
    __slots__ = ("legacy_command_number", "client_tick", "prediction_offset_ticks_x256", "buttons_pb", "viewangles", "forwardmove", "leftmove", "upmove", "impulse", "weaponselect", "random_seed", "mousedx", "mousedy", "pawn_entity_handle", "subtick_moves", "move_crc", "consumed_server_angle_changes", "cmd_flags", "execution_notes")
    LEGACY_COMMAND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TICK_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OFFSET_TICKS_X256_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_PB_FIELD_NUMBER: _ClassVar[int]
    VIEWANGLES_FIELD_NUMBER: _ClassVar[int]
    FORWARDMOVE_FIELD_NUMBER: _ClassVar[int]
    LEFTMOVE_FIELD_NUMBER: _ClassVar[int]
    UPMOVE_FIELD_NUMBER: _ClassVar[int]
    IMPULSE_FIELD_NUMBER: _ClassVar[int]
    WEAPONSELECT_FIELD_NUMBER: _ClassVar[int]
    RANDOM_SEED_FIELD_NUMBER: _ClassVar[int]
    MOUSEDX_FIELD_NUMBER: _ClassVar[int]
    MOUSEDY_FIELD_NUMBER: _ClassVar[int]
    PAWN_ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
    SUBTICK_MOVES_FIELD_NUMBER: _ClassVar[int]
    MOVE_CRC_FIELD_NUMBER: _ClassVar[int]
    CONSUMED_SERVER_ANGLE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    CMD_FLAGS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_NOTES_FIELD_NUMBER: _ClassVar[int]
    legacy_command_number: int
    client_tick: int
    prediction_offset_ticks_x256: int
    buttons_pb: CInButtonStatePB
    viewangles: _networkbasetypes_pb2.CMsgQAngle
    forwardmove: float
    leftmove: float
    upmove: float
    impulse: int
    weaponselect: int
    random_seed: int
    mousedx: int
    mousedy: int
    pawn_entity_handle: int
    subtick_moves: _containers.RepeatedCompositeFieldContainer[CSubtickMoveStep]
    move_crc: bytes
    consumed_server_angle_changes: int
    cmd_flags: int
    execution_notes: CBaseUserCmdExecutionNotes
    def __init__(self, legacy_command_number: _Optional[int] = ..., client_tick: _Optional[int] = ..., prediction_offset_ticks_x256: _Optional[int] = ..., buttons_pb: _Optional[_Union[CInButtonStatePB, _Mapping]] = ..., viewangles: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ..., forwardmove: _Optional[float] = ..., leftmove: _Optional[float] = ..., upmove: _Optional[float] = ..., impulse: _Optional[int] = ..., weaponselect: _Optional[int] = ..., random_seed: _Optional[int] = ..., mousedx: _Optional[int] = ..., mousedy: _Optional[int] = ..., pawn_entity_handle: _Optional[int] = ..., subtick_moves: _Optional[_Iterable[_Union[CSubtickMoveStep, _Mapping]]] = ..., move_crc: _Optional[bytes] = ..., consumed_server_angle_changes: _Optional[int] = ..., cmd_flags: _Optional[int] = ..., execution_notes: _Optional[_Union[CBaseUserCmdExecutionNotes, _Mapping]] = ...) -> None: ...

class CUserCmdBasePB(_message.Message):
    __slots__ = ("base",)
    BASE_FIELD_NUMBER: _ClassVar[int]
    base: CBaseUserCmdPB
    def __init__(self, base: _Optional[_Union[CBaseUserCmdPB, _Mapping]] = ...) -> None: ...
