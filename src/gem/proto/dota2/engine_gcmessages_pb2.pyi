from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class CEngineGotvSyncPacket(_message.Message):
    __slots__ = (
        "match_id",
        "instance_id",
        "signupfragment",
        "currentfragment",
        "tickrate",
        "tick",
        "rtdelay",
        "rcvage",
        "keyframe_interval",
        "cdndelay",
    )
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNUPFRAGMENT_FIELD_NUMBER: _ClassVar[int]
    CURRENTFRAGMENT_FIELD_NUMBER: _ClassVar[int]
    TICKRATE_FIELD_NUMBER: _ClassVar[int]
    TICK_FIELD_NUMBER: _ClassVar[int]
    RTDELAY_FIELD_NUMBER: _ClassVar[int]
    RCVAGE_FIELD_NUMBER: _ClassVar[int]
    KEYFRAME_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    CDNDELAY_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    instance_id: int
    signupfragment: int
    currentfragment: int
    tickrate: float
    tick: int
    rtdelay: float
    rcvage: float
    keyframe_interval: float
    cdndelay: int
    def __init__(
        self,
        match_id: int | None = ...,
        instance_id: int | None = ...,
        signupfragment: int | None = ...,
        currentfragment: int | None = ...,
        tickrate: float | None = ...,
        tick: int | None = ...,
        rtdelay: float | None = ...,
        rcvage: float | None = ...,
        keyframe_interval: float | None = ...,
        cdndelay: int | None = ...,
    ) -> None: ...
