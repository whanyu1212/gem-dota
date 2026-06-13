from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EDotaBroadcastMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_BM_LANLobbyRequest: _ClassVar[EDotaBroadcastMessages]
    DOTA_BM_LANLobbyReply: _ClassVar[EDotaBroadcastMessages]
DOTA_BM_LANLobbyRequest: EDotaBroadcastMessages
DOTA_BM_LANLobbyReply: EDotaBroadcastMessages

class CDOTABroadcastMsg(_message.Message):
    __slots__ = ("type", "msg")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    type: EDotaBroadcastMessages
    msg: bytes
    def __init__(self, type: _Optional[_Union[EDotaBroadcastMessages, str]] = ..., msg: _Optional[bytes] = ...) -> None: ...

class CDOTABroadcastMsg_LANLobbyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTABroadcastMsg_LANLobbyReply(_message.Message):
    __slots__ = ("id", "tournament_id", "tournament_game_id", "members", "requires_pass_key", "leader_account_id", "game_mode", "name", "players")
    class CLobbyMember(_message.Message):
        __slots__ = ("account_id", "player_name")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        player_name: str
        def __init__(self, account_id: _Optional[int] = ..., player_name: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    LEADER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    id: int
    tournament_id: int
    tournament_game_id: int
    members: _containers.RepeatedCompositeFieldContainer[CDOTABroadcastMsg_LANLobbyReply.CLobbyMember]
    requires_pass_key: bool
    leader_account_id: int
    game_mode: int
    name: str
    players: int
    def __init__(self, id: _Optional[int] = ..., tournament_id: _Optional[int] = ..., tournament_game_id: _Optional[int] = ..., members: _Optional[_Iterable[_Union[CDOTABroadcastMsg_LANLobbyReply.CLobbyMember, _Mapping]]] = ..., requires_pass_key: bool = ..., leader_account_id: _Optional[int] = ..., game_mode: _Optional[int] = ..., name: _Optional[str] = ..., players: _Optional[int] = ...) -> None: ...
