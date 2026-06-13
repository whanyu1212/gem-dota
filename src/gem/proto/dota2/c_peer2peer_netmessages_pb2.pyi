import netmessages_pb2 as _netmessages_pb2
import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class P2P_Messages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    p2p_TextMessage: _ClassVar[P2P_Messages]
    p2p_Voice: _ClassVar[P2P_Messages]
    p2p_Ping: _ClassVar[P2P_Messages]
    p2p_VRAvatarPosition: _ClassVar[P2P_Messages]
    p2p_WatchSynchronization: _ClassVar[P2P_Messages]
    p2p_FightingGame_GameData: _ClassVar[P2P_Messages]
    p2p_FightingGame_Connection: _ClassVar[P2P_Messages]
p2p_TextMessage: P2P_Messages
p2p_Voice: P2P_Messages
p2p_Ping: P2P_Messages
p2p_VRAvatarPosition: P2P_Messages
p2p_WatchSynchronization: P2P_Messages
p2p_FightingGame_GameData: P2P_Messages
p2p_FightingGame_Connection: P2P_Messages

class CP2P_TextMessage(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: bytes
    def __init__(self, text: _Optional[bytes] = ...) -> None: ...

class CSteam_Voice_Encoding(_message.Message):
    __slots__ = ("voice_data",)
    VOICE_DATA_FIELD_NUMBER: _ClassVar[int]
    voice_data: bytes
    def __init__(self, voice_data: _Optional[bytes] = ...) -> None: ...

class CP2P_Voice(_message.Message):
    __slots__ = ("audio", "broadcast_group")
    class Handler_Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Played_Audio: _ClassVar[CP2P_Voice.Handler_Flags]
    Played_Audio: CP2P_Voice.Handler_Flags
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_GROUP_FIELD_NUMBER: _ClassVar[int]
    audio: _netmessages_pb2.CMsgVoiceAudio
    broadcast_group: int
    def __init__(self, audio: _Optional[_Union[_netmessages_pb2.CMsgVoiceAudio, _Mapping]] = ..., broadcast_group: _Optional[int] = ...) -> None: ...

class CP2P_Ping(_message.Message):
    __slots__ = ("send_time", "is_reply")
    SEND_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_REPLY_FIELD_NUMBER: _ClassVar[int]
    send_time: int
    is_reply: bool
    def __init__(self, send_time: _Optional[int] = ..., is_reply: bool = ...) -> None: ...

class CP2P_VRAvatarPosition(_message.Message):
    __slots__ = ("body_parts", "hat_id", "scene_id", "world_scale")
    class COrientation(_message.Message):
        __slots__ = ("pos", "ang")
        POS_FIELD_NUMBER: _ClassVar[int]
        ANG_FIELD_NUMBER: _ClassVar[int]
        pos: _networkbasetypes_pb2.CMsgVector
        ang: _networkbasetypes_pb2.CMsgQAngle
        def __init__(self, pos: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., ang: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ...) -> None: ...
    BODY_PARTS_FIELD_NUMBER: _ClassVar[int]
    HAT_ID_FIELD_NUMBER: _ClassVar[int]
    SCENE_ID_FIELD_NUMBER: _ClassVar[int]
    WORLD_SCALE_FIELD_NUMBER: _ClassVar[int]
    body_parts: _containers.RepeatedCompositeFieldContainer[CP2P_VRAvatarPosition.COrientation]
    hat_id: int
    scene_id: int
    world_scale: int
    def __init__(self, body_parts: _Optional[_Iterable[_Union[CP2P_VRAvatarPosition.COrientation, _Mapping]]] = ..., hat_id: _Optional[int] = ..., scene_id: _Optional[int] = ..., world_scale: _Optional[int] = ...) -> None: ...

class CP2P_WatchSynchronization(_message.Message):
    __slots__ = ("demo_tick", "paused", "tv_listen_voice_indices", "dota_spectator_mode", "dota_spectator_watching_broadcaster", "dota_spectator_hero_index", "dota_spectator_autospeed", "dota_replay_speed")
    DEMO_TICK_FIELD_NUMBER: _ClassVar[int]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    TV_LISTEN_VOICE_INDICES_FIELD_NUMBER: _ClassVar[int]
    DOTA_SPECTATOR_MODE_FIELD_NUMBER: _ClassVar[int]
    DOTA_SPECTATOR_WATCHING_BROADCASTER_FIELD_NUMBER: _ClassVar[int]
    DOTA_SPECTATOR_HERO_INDEX_FIELD_NUMBER: _ClassVar[int]
    DOTA_SPECTATOR_AUTOSPEED_FIELD_NUMBER: _ClassVar[int]
    DOTA_REPLAY_SPEED_FIELD_NUMBER: _ClassVar[int]
    demo_tick: int
    paused: bool
    tv_listen_voice_indices: int
    dota_spectator_mode: int
    dota_spectator_watching_broadcaster: bool
    dota_spectator_hero_index: int
    dota_spectator_autospeed: int
    dota_replay_speed: int
    def __init__(self, demo_tick: _Optional[int] = ..., paused: bool = ..., tv_listen_voice_indices: _Optional[int] = ..., dota_spectator_mode: _Optional[int] = ..., dota_spectator_watching_broadcaster: bool = ..., dota_spectator_hero_index: _Optional[int] = ..., dota_spectator_autospeed: _Optional[int] = ..., dota_replay_speed: _Optional[int] = ...) -> None: ...
