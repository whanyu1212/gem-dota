from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CInButtonStatePB(_message.Message):
    __slots__ = ("buttonstate1", "buttonstate2", "buttonstate3")
    BUTTONSTATE1_FIELD_NUMBER: _ClassVar[int]
    BUTTONSTATE2_FIELD_NUMBER: _ClassVar[int]
    BUTTONSTATE3_FIELD_NUMBER: _ClassVar[int]
    buttonstate1: int
    buttonstate2: int
    buttonstate3: int
    def __init__(
        self,
        buttonstate1: int | None = ...,
        buttonstate2: int | None = ...,
        buttonstate3: int | None = ...,
    ) -> None: ...

class CSubtickMoveStep(_message.Message):
    __slots__ = (
        "button",
        "pressed",
        "when",
        "analog_forward_delta",
        "analog_left_delta",
        "pitch_delta",
        "yaw_delta",
    )
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
    def __init__(
        self,
        button: int | None = ...,
        pressed: bool = ...,
        when: float | None = ...,
        analog_forward_delta: float | None = ...,
        analog_left_delta: float | None = ...,
        pitch_delta: float | None = ...,
        yaw_delta: float | None = ...,
    ) -> None: ...

class CBaseUserCmdExecutionNotes(_message.Message):
    __slots__ = ("ignored_reason",)
    IGNORED_REASON_FIELD_NUMBER: _ClassVar[int]
    ignored_reason: str
    def __init__(self, ignored_reason: str | None = ...) -> None: ...

class CBaseUserCmdPB(_message.Message):
    __slots__ = (
        "legacy_command_number",
        "client_tick",
        "prediction_offset_ticks_x256",
        "buttons_pb",
        "viewangles",
        "forwardmove",
        "leftmove",
        "upmove",
        "impulse",
        "weaponselect",
        "random_seed",
        "mousedx",
        "mousedy",
        "pawn_entity_handle",
        "subtick_moves",
        "move_crc",
        "consumed_server_angle_changes",
        "cmd_flags",
        "execution_notes",
    )
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
    def __init__(
        self,
        legacy_command_number: int | None = ...,
        client_tick: int | None = ...,
        prediction_offset_ticks_x256: int | None = ...,
        buttons_pb: CInButtonStatePB | _Mapping | None = ...,
        viewangles: _networkbasetypes_pb2.CMsgQAngle | _Mapping | None = ...,
        forwardmove: float | None = ...,
        leftmove: float | None = ...,
        upmove: float | None = ...,
        impulse: int | None = ...,
        weaponselect: int | None = ...,
        random_seed: int | None = ...,
        mousedx: int | None = ...,
        mousedy: int | None = ...,
        pawn_entity_handle: int | None = ...,
        subtick_moves: _Iterable[CSubtickMoveStep | _Mapping] | None = ...,
        move_crc: bytes | None = ...,
        consumed_server_angle_changes: int | None = ...,
        cmd_flags: int | None = ...,
        execution_notes: CBaseUserCmdExecutionNotes | _Mapping | None = ...,
    ) -> None: ...

class CUserCmdBasePB(_message.Message):
    __slots__ = ("base",)
    BASE_FIELD_NUMBER: _ClassVar[int]
    base: CBaseUserCmdPB
    def __init__(self, base: CBaseUserCmdPB | _Mapping | None = ...) -> None: ...
