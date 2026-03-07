from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgFightingGame_GameData_Fighting(_message.Message):
    __slots__ = (
        "last_acked_frame",
        "player_id",
        "last_crc_frame",
        "last_crc_value",
        "now",
        "peer_ack_time",
        "input_start_frame",
        "input_sample",
    )
    class InputSample(_message.Message):
        __slots__ = ("button_mask",)
        BUTTON_MASK_FIELD_NUMBER: _ClassVar[int]
        button_mask: int
        def __init__(self, button_mask: int | None = ...) -> None: ...

    LAST_ACKED_FRAME_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_CRC_FRAME_FIELD_NUMBER: _ClassVar[int]
    LAST_CRC_VALUE_FIELD_NUMBER: _ClassVar[int]
    NOW_FIELD_NUMBER: _ClassVar[int]
    PEER_ACK_TIME_FIELD_NUMBER: _ClassVar[int]
    INPUT_START_FRAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    last_acked_frame: int
    player_id: int
    last_crc_frame: int
    last_crc_value: int
    now: float
    peer_ack_time: float
    input_start_frame: int
    input_sample: _containers.RepeatedCompositeFieldContainer[
        CMsgFightingGame_GameData_Fighting.InputSample
    ]
    def __init__(
        self,
        last_acked_frame: int | None = ...,
        player_id: int | None = ...,
        last_crc_frame: int | None = ...,
        last_crc_value: int | None = ...,
        now: float | None = ...,
        peer_ack_time: float | None = ...,
        input_start_frame: int | None = ...,
        input_sample: _Iterable[CMsgFightingGame_GameData_Fighting.InputSample | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgFightingGame_GameData_CharacterSelect(_message.Message):
    __slots__ = (
        "cursor_index",
        "selected_hero_id",
        "selected_style",
        "econ_item_refs",
        "message_ack",
        "confirmed_style",
    )
    class Item(_message.Message):
        __slots__ = ("item_def", "style_index")
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        STYLE_INDEX_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        style_index: int
        def __init__(self, item_def: int | None = ..., style_index: int | None = ...) -> None: ...

    CURSOR_INDEX_FIELD_NUMBER: _ClassVar[int]
    SELECTED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTED_STYLE_FIELD_NUMBER: _ClassVar[int]
    ECON_ITEM_REFS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ACK_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED_STYLE_FIELD_NUMBER: _ClassVar[int]
    cursor_index: int
    selected_hero_id: int
    selected_style: int
    econ_item_refs: _containers.RepeatedCompositeFieldContainer[
        CMsgFightingGame_GameData_CharacterSelect.Item
    ]
    message_ack: int
    confirmed_style: bool
    def __init__(
        self,
        cursor_index: int | None = ...,
        selected_hero_id: int | None = ...,
        selected_style: int | None = ...,
        econ_item_refs: _Iterable[CMsgFightingGame_GameData_CharacterSelect.Item | _Mapping]
        | None = ...,
        message_ack: int | None = ...,
        confirmed_style: bool = ...,
    ) -> None: ...

class CMsgFightingGame_GameData_Loaded(_message.Message):
    __slots__ = ("now", "peer_ack_time", "proposed_start_time", "accepted_start_time")
    NOW_FIELD_NUMBER: _ClassVar[int]
    PEER_ACK_TIME_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_START_TIME_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_START_TIME_FIELD_NUMBER: _ClassVar[int]
    now: float
    peer_ack_time: float
    proposed_start_time: float
    accepted_start_time: float
    def __init__(
        self,
        now: float | None = ...,
        peer_ack_time: float | None = ...,
        proposed_start_time: float | None = ...,
        accepted_start_time: float | None = ...,
    ) -> None: ...

class CP2P_FightingGame_GameData(_message.Message):
    __slots__ = ("state", "fight", "character_select", "loaded")
    class EState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_ChoosingCharacter: _ClassVar[CP2P_FightingGame_GameData.EState]
        k_Loaded: _ClassVar[CP2P_FightingGame_GameData.EState]
        k_Fighting: _ClassVar[CP2P_FightingGame_GameData.EState]

    k_ChoosingCharacter: CP2P_FightingGame_GameData.EState
    k_Loaded: CP2P_FightingGame_GameData.EState
    k_Fighting: CP2P_FightingGame_GameData.EState
    STATE_FIELD_NUMBER: _ClassVar[int]
    FIGHT_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_SELECT_FIELD_NUMBER: _ClassVar[int]
    LOADED_FIELD_NUMBER: _ClassVar[int]
    state: CP2P_FightingGame_GameData.EState
    fight: CMsgFightingGame_GameData_Fighting
    character_select: CMsgFightingGame_GameData_CharacterSelect
    loaded: CMsgFightingGame_GameData_Loaded
    def __init__(
        self,
        state: CP2P_FightingGame_GameData.EState | str | None = ...,
        fight: CMsgFightingGame_GameData_Fighting | _Mapping | None = ...,
        character_select: CMsgFightingGame_GameData_CharacterSelect | _Mapping | None = ...,
        loaded: CMsgFightingGame_GameData_Loaded | _Mapping | None = ...,
    ) -> None: ...
