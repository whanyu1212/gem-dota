from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import networkbasetypes_pb2 as _networkbasetypes_pb2
import usercmd_pb2 as _usercmd_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class CDota2UserCmdPB(_message.Message):
    __slots__ = (
        "base",
        "spectator_query_unit_entindex",
        "crosshairtrace",
        "cameraposition_x",
        "cameraposition_y",
        "clickbehavior",
        "statspanel",
        "shoppanel",
        "stats_dropdown",
        "stats_dropdown_sort",
    )
    BASE_FIELD_NUMBER: _ClassVar[int]
    SPECTATOR_QUERY_UNIT_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    CROSSHAIRTRACE_FIELD_NUMBER: _ClassVar[int]
    CAMERAPOSITION_X_FIELD_NUMBER: _ClassVar[int]
    CAMERAPOSITION_Y_FIELD_NUMBER: _ClassVar[int]
    CLICKBEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    STATSPANEL_FIELD_NUMBER: _ClassVar[int]
    SHOPPANEL_FIELD_NUMBER: _ClassVar[int]
    STATS_DROPDOWN_FIELD_NUMBER: _ClassVar[int]
    STATS_DROPDOWN_SORT_FIELD_NUMBER: _ClassVar[int]
    base: _usercmd_pb2.CBaseUserCmdPB
    spectator_query_unit_entindex: int
    crosshairtrace: _networkbasetypes_pb2.CMsgVector
    cameraposition_x: int
    cameraposition_y: int
    clickbehavior: int
    statspanel: int
    shoppanel: int
    stats_dropdown: int
    stats_dropdown_sort: int
    def __init__(
        self,
        base: _usercmd_pb2.CBaseUserCmdPB | _Mapping | None = ...,
        spectator_query_unit_entindex: int | None = ...,
        crosshairtrace: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        cameraposition_x: int | None = ...,
        cameraposition_y: int | None = ...,
        clickbehavior: int | None = ...,
        statspanel: int | None = ...,
        shoppanel: int | None = ...,
        stats_dropdown: int | None = ...,
        stats_dropdown_sort: int | None = ...,
    ) -> None: ...
