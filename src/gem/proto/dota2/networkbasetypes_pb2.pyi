from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class SignonState_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIGNONSTATE_NONE: _ClassVar[SignonState_t]
    SIGNONSTATE_CHALLENGE: _ClassVar[SignonState_t]
    SIGNONSTATE_CONNECTED: _ClassVar[SignonState_t]
    SIGNONSTATE_NEW: _ClassVar[SignonState_t]
    SIGNONSTATE_PRESPAWN: _ClassVar[SignonState_t]
    SIGNONSTATE_SPAWN: _ClassVar[SignonState_t]
    SIGNONSTATE_FULL: _ClassVar[SignonState_t]
    SIGNONSTATE_CHANGELEVEL: _ClassVar[SignonState_t]

class NET_Messages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    net_NOP: _ClassVar[NET_Messages]
    net_Disconnect_Legacy: _ClassVar[NET_Messages]
    net_SplitScreenUser: _ClassVar[NET_Messages]
    net_Tick: _ClassVar[NET_Messages]
    net_StringCmd: _ClassVar[NET_Messages]
    net_SetConVar: _ClassVar[NET_Messages]
    net_SignonState: _ClassVar[NET_Messages]
    net_SpawnGroup_Load: _ClassVar[NET_Messages]
    net_SpawnGroup_ManifestUpdate: _ClassVar[NET_Messages]
    net_SpawnGroup_SetCreationTick: _ClassVar[NET_Messages]
    net_SpawnGroup_Unload: _ClassVar[NET_Messages]
    net_SpawnGroup_LoadCompleted: _ClassVar[NET_Messages]
    net_DebugOverlay: _ClassVar[NET_Messages]

class SpawnGroupFlags_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPAWN_GROUP_LOAD_ENTITIES_FROM_SAVE: _ClassVar[SpawnGroupFlags_t]
    SPAWN_GROUP_DONT_SPAWN_ENTITIES: _ClassVar[SpawnGroupFlags_t]
    SPAWN_GROUP_SYNCHRONOUS_SPAWN: _ClassVar[SpawnGroupFlags_t]
    SPAWN_GROUP_IS_INITIAL_SPAWN_GROUP: _ClassVar[SpawnGroupFlags_t]
    SPAWN_GROUP_CREATE_CLIENT_ONLY_ENTITIES: _ClassVar[SpawnGroupFlags_t]
    SPAWN_GROUP_BLOCK_UNTIL_LOADED: _ClassVar[SpawnGroupFlags_t]
    SPAWN_GROUP_LOAD_STREAMING_DATA: _ClassVar[SpawnGroupFlags_t]
    SPAWN_GROUP_CREATE_NEW_SCENE_WORLD: _ClassVar[SpawnGroupFlags_t]

SIGNONSTATE_NONE: SignonState_t
SIGNONSTATE_CHALLENGE: SignonState_t
SIGNONSTATE_CONNECTED: SignonState_t
SIGNONSTATE_NEW: SignonState_t
SIGNONSTATE_PRESPAWN: SignonState_t
SIGNONSTATE_SPAWN: SignonState_t
SIGNONSTATE_FULL: SignonState_t
SIGNONSTATE_CHANGELEVEL: SignonState_t
net_NOP: NET_Messages
net_Disconnect_Legacy: NET_Messages
net_SplitScreenUser: NET_Messages
net_Tick: NET_Messages
net_StringCmd: NET_Messages
net_SetConVar: NET_Messages
net_SignonState: NET_Messages
net_SpawnGroup_Load: NET_Messages
net_SpawnGroup_ManifestUpdate: NET_Messages
net_SpawnGroup_SetCreationTick: NET_Messages
net_SpawnGroup_Unload: NET_Messages
net_SpawnGroup_LoadCompleted: NET_Messages
net_DebugOverlay: NET_Messages
SPAWN_GROUP_LOAD_ENTITIES_FROM_SAVE: SpawnGroupFlags_t
SPAWN_GROUP_DONT_SPAWN_ENTITIES: SpawnGroupFlags_t
SPAWN_GROUP_SYNCHRONOUS_SPAWN: SpawnGroupFlags_t
SPAWN_GROUP_IS_INITIAL_SPAWN_GROUP: SpawnGroupFlags_t
SPAWN_GROUP_CREATE_CLIENT_ONLY_ENTITIES: SpawnGroupFlags_t
SPAWN_GROUP_BLOCK_UNTIL_LOADED: SpawnGroupFlags_t
SPAWN_GROUP_LOAD_STREAMING_DATA: SpawnGroupFlags_t
SPAWN_GROUP_CREATE_NEW_SCENE_WORLD: SpawnGroupFlags_t
MAXIMUM_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
maximum_size_bytes: _descriptor.FieldDescriptor

class CMsgVector(_message.Message):
    __slots__ = ("x", "y", "z", "w")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    w: float
    def __init__(
        self,
        x: float | None = ...,
        y: float | None = ...,
        z: float | None = ...,
        w: float | None = ...,
    ) -> None: ...

class CMsgVector2D(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: float | None = ..., y: float | None = ...) -> None: ...

class CMsgQAngle(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(
        self, x: float | None = ..., y: float | None = ..., z: float | None = ...
    ) -> None: ...

class CMsgQuaternion(_message.Message):
    __slots__ = ("x", "y", "z", "w")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    w: float
    def __init__(
        self,
        x: float | None = ...,
        y: float | None = ...,
        z: float | None = ...,
        w: float | None = ...,
    ) -> None: ...

class CMsgTransform(_message.Message):
    __slots__ = ("position", "scale", "orientation")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    position: CMsgVector
    scale: float
    orientation: CMsgQuaternion
    def __init__(
        self,
        position: CMsgVector | _Mapping | None = ...,
        scale: float | None = ...,
        orientation: CMsgQuaternion | _Mapping | None = ...,
    ) -> None: ...

class CMsgRGBA(_message.Message):
    __slots__ = ("r", "g", "b", "a")
    R_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    r: int
    g: int
    b: int
    a: int
    def __init__(
        self, r: int | None = ..., g: int | None = ..., b: int | None = ..., a: int | None = ...
    ) -> None: ...

class CMsgPlayerInfo(_message.Message):
    __slots__ = ("name", "xuid", "userid", "steamid", "fakeplayer", "ishltv")
    NAME_FIELD_NUMBER: _ClassVar[int]
    XUID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    FAKEPLAYER_FIELD_NUMBER: _ClassVar[int]
    ISHLTV_FIELD_NUMBER: _ClassVar[int]
    name: str
    xuid: int
    userid: int
    steamid: int
    fakeplayer: bool
    ishltv: bool
    def __init__(
        self,
        name: str | None = ...,
        xuid: int | None = ...,
        userid: int | None = ...,
        steamid: int | None = ...,
        fakeplayer: bool = ...,
        ishltv: bool = ...,
    ) -> None: ...

class CEntityMsg(_message.Message):
    __slots__ = ("target_entity",)
    TARGET_ENTITY_FIELD_NUMBER: _ClassVar[int]
    target_entity: int
    def __init__(self, target_entity: int | None = ...) -> None: ...

class CMsg_CVars(_message.Message):
    __slots__ = ("cvars",)
    class CVar(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: str | None = ..., value: str | None = ...) -> None: ...

    CVARS_FIELD_NUMBER: _ClassVar[int]
    cvars: _containers.RepeatedCompositeFieldContainer[CMsg_CVars.CVar]
    def __init__(self, cvars: _Iterable[CMsg_CVars.CVar | _Mapping] | None = ...) -> None: ...

class CNETMsg_NOP(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CNETMsg_SplitScreenUser(_message.Message):
    __slots__ = ("slot",)
    SLOT_FIELD_NUMBER: _ClassVar[int]
    slot: int
    def __init__(self, slot: int | None = ...) -> None: ...

class CNETMsg_Tick(_message.Message):
    __slots__ = (
        "tick",
        "host_computationtime",
        "host_computationtime_std_deviation",
        "legacy_host_loss",
        "host_unfiltered_frametime",
        "hltv_replay_flags",
        "expected_long_tick",
        "expected_long_tick_reason",
        "host_frame_dropped_pct_x10",
        "host_frame_irregular_arrival_pct_x10",
    )
    TICK_FIELD_NUMBER: _ClassVar[int]
    HOST_COMPUTATIONTIME_FIELD_NUMBER: _ClassVar[int]
    HOST_COMPUTATIONTIME_STD_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    LEGACY_HOST_LOSS_FIELD_NUMBER: _ClassVar[int]
    HOST_UNFILTERED_FRAMETIME_FIELD_NUMBER: _ClassVar[int]
    HLTV_REPLAY_FLAGS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_LONG_TICK_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_LONG_TICK_REASON_FIELD_NUMBER: _ClassVar[int]
    HOST_FRAME_DROPPED_PCT_X10_FIELD_NUMBER: _ClassVar[int]
    HOST_FRAME_IRREGULAR_ARRIVAL_PCT_X10_FIELD_NUMBER: _ClassVar[int]
    tick: int
    host_computationtime: int
    host_computationtime_std_deviation: int
    legacy_host_loss: int
    host_unfiltered_frametime: int
    hltv_replay_flags: int
    expected_long_tick: int
    expected_long_tick_reason: str
    host_frame_dropped_pct_x10: int
    host_frame_irregular_arrival_pct_x10: int
    def __init__(
        self,
        tick: int | None = ...,
        host_computationtime: int | None = ...,
        host_computationtime_std_deviation: int | None = ...,
        legacy_host_loss: int | None = ...,
        host_unfiltered_frametime: int | None = ...,
        hltv_replay_flags: int | None = ...,
        expected_long_tick: int | None = ...,
        expected_long_tick_reason: str | None = ...,
        host_frame_dropped_pct_x10: int | None = ...,
        host_frame_irregular_arrival_pct_x10: int | None = ...,
    ) -> None: ...

class CNETMsg_StringCmd(_message.Message):
    __slots__ = ("command", "prediction_sync")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_SYNC_FIELD_NUMBER: _ClassVar[int]
    command: str
    prediction_sync: int
    def __init__(self, command: str | None = ..., prediction_sync: int | None = ...) -> None: ...

class CNETMsg_SetConVar(_message.Message):
    __slots__ = ("convars",)
    CONVARS_FIELD_NUMBER: _ClassVar[int]
    convars: CMsg_CVars
    def __init__(self, convars: CMsg_CVars | _Mapping | None = ...) -> None: ...

class CNETMsg_SignonState(_message.Message):
    __slots__ = (
        "signon_state",
        "spawn_count",
        "num_server_players",
        "players_networkids",
        "map_name",
        "addons",
    )
    SIGNON_STATE_FIELD_NUMBER: _ClassVar[int]
    SPAWN_COUNT_FIELD_NUMBER: _ClassVar[int]
    NUM_SERVER_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_NETWORKIDS_FIELD_NUMBER: _ClassVar[int]
    MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    ADDONS_FIELD_NUMBER: _ClassVar[int]
    signon_state: SignonState_t
    spawn_count: int
    num_server_players: int
    players_networkids: _containers.RepeatedScalarFieldContainer[str]
    map_name: str
    addons: str
    def __init__(
        self,
        signon_state: SignonState_t | str | None = ...,
        spawn_count: int | None = ...,
        num_server_players: int | None = ...,
        players_networkids: _Iterable[str] | None = ...,
        map_name: str | None = ...,
        addons: str | None = ...,
    ) -> None: ...

class CSVCMsg_GameEvent(_message.Message):
    __slots__ = ("event_name", "eventid", "keys")
    class key_t(_message.Message):
        __slots__ = (
            "type",
            "val_string",
            "val_float",
            "val_long",
            "val_short",
            "val_byte",
            "val_bool",
            "val_uint64",
        )
        TYPE_FIELD_NUMBER: _ClassVar[int]
        VAL_STRING_FIELD_NUMBER: _ClassVar[int]
        VAL_FLOAT_FIELD_NUMBER: _ClassVar[int]
        VAL_LONG_FIELD_NUMBER: _ClassVar[int]
        VAL_SHORT_FIELD_NUMBER: _ClassVar[int]
        VAL_BYTE_FIELD_NUMBER: _ClassVar[int]
        VAL_BOOL_FIELD_NUMBER: _ClassVar[int]
        VAL_UINT64_FIELD_NUMBER: _ClassVar[int]
        type: int
        val_string: str
        val_float: float
        val_long: int
        val_short: int
        val_byte: int
        val_bool: bool
        val_uint64: int
        def __init__(
            self,
            type: int | None = ...,
            val_string: str | None = ...,
            val_float: float | None = ...,
            val_long: int | None = ...,
            val_short: int | None = ...,
            val_byte: int | None = ...,
            val_bool: bool = ...,
            val_uint64: int | None = ...,
        ) -> None: ...

    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    eventid: int
    keys: _containers.RepeatedCompositeFieldContainer[CSVCMsg_GameEvent.key_t]
    def __init__(
        self,
        event_name: str | None = ...,
        eventid: int | None = ...,
        keys: _Iterable[CSVCMsg_GameEvent.key_t | _Mapping] | None = ...,
    ) -> None: ...

class CSVCMsgList_GameEvents(_message.Message):
    __slots__ = ("events",)
    class event_t(_message.Message):
        __slots__ = ("tick", "event")
        TICK_FIELD_NUMBER: _ClassVar[int]
        EVENT_FIELD_NUMBER: _ClassVar[int]
        tick: int
        event: CSVCMsg_GameEvent
        def __init__(
            self, tick: int | None = ..., event: CSVCMsg_GameEvent | _Mapping | None = ...
        ) -> None: ...

    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[CSVCMsgList_GameEvents.event_t]
    def __init__(
        self, events: _Iterable[CSVCMsgList_GameEvents.event_t | _Mapping] | None = ...
    ) -> None: ...

class CNETMsg_SpawnGroup_Load(_message.Message):
    __slots__ = (
        "worldname",
        "entitylumpname",
        "entityfiltername",
        "spawngrouphandle",
        "spawngroupownerhandle",
        "world_offset_pos",
        "world_offset_angle",
        "spawngroupmanifest",
        "flags",
        "tickcount",
        "manifestincomplete",
        "localnamefixup",
        "parentnamefixup",
        "manifestloadpriority",
        "worldgroupid",
        "creationsequence",
        "savegamefilename",
        "spawngroupparenthandle",
        "leveltransition",
        "worldgroupname",
    )
    WORLDNAME_FIELD_NUMBER: _ClassVar[int]
    ENTITYLUMPNAME_FIELD_NUMBER: _ClassVar[int]
    ENTITYFILTERNAME_FIELD_NUMBER: _ClassVar[int]
    SPAWNGROUPHANDLE_FIELD_NUMBER: _ClassVar[int]
    SPAWNGROUPOWNERHANDLE_FIELD_NUMBER: _ClassVar[int]
    WORLD_OFFSET_POS_FIELD_NUMBER: _ClassVar[int]
    WORLD_OFFSET_ANGLE_FIELD_NUMBER: _ClassVar[int]
    SPAWNGROUPMANIFEST_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    TICKCOUNT_FIELD_NUMBER: _ClassVar[int]
    MANIFESTINCOMPLETE_FIELD_NUMBER: _ClassVar[int]
    LOCALNAMEFIXUP_FIELD_NUMBER: _ClassVar[int]
    PARENTNAMEFIXUP_FIELD_NUMBER: _ClassVar[int]
    MANIFESTLOADPRIORITY_FIELD_NUMBER: _ClassVar[int]
    WORLDGROUPID_FIELD_NUMBER: _ClassVar[int]
    CREATIONSEQUENCE_FIELD_NUMBER: _ClassVar[int]
    SAVEGAMEFILENAME_FIELD_NUMBER: _ClassVar[int]
    SPAWNGROUPPARENTHANDLE_FIELD_NUMBER: _ClassVar[int]
    LEVELTRANSITION_FIELD_NUMBER: _ClassVar[int]
    WORLDGROUPNAME_FIELD_NUMBER: _ClassVar[int]
    worldname: str
    entitylumpname: str
    entityfiltername: str
    spawngrouphandle: int
    spawngroupownerhandle: int
    world_offset_pos: CMsgVector
    world_offset_angle: CMsgQAngle
    spawngroupmanifest: bytes
    flags: int
    tickcount: int
    manifestincomplete: bool
    localnamefixup: str
    parentnamefixup: str
    manifestloadpriority: int
    worldgroupid: int
    creationsequence: int
    savegamefilename: str
    spawngroupparenthandle: int
    leveltransition: bool
    worldgroupname: str
    def __init__(
        self,
        worldname: str | None = ...,
        entitylumpname: str | None = ...,
        entityfiltername: str | None = ...,
        spawngrouphandle: int | None = ...,
        spawngroupownerhandle: int | None = ...,
        world_offset_pos: CMsgVector | _Mapping | None = ...,
        world_offset_angle: CMsgQAngle | _Mapping | None = ...,
        spawngroupmanifest: bytes | None = ...,
        flags: int | None = ...,
        tickcount: int | None = ...,
        manifestincomplete: bool = ...,
        localnamefixup: str | None = ...,
        parentnamefixup: str | None = ...,
        manifestloadpriority: int | None = ...,
        worldgroupid: int | None = ...,
        creationsequence: int | None = ...,
        savegamefilename: str | None = ...,
        spawngroupparenthandle: int | None = ...,
        leveltransition: bool = ...,
        worldgroupname: str | None = ...,
    ) -> None: ...

class CNETMsg_SpawnGroup_ManifestUpdate(_message.Message):
    __slots__ = ("spawngrouphandle", "spawngroupmanifest", "manifestincomplete")
    SPAWNGROUPHANDLE_FIELD_NUMBER: _ClassVar[int]
    SPAWNGROUPMANIFEST_FIELD_NUMBER: _ClassVar[int]
    MANIFESTINCOMPLETE_FIELD_NUMBER: _ClassVar[int]
    spawngrouphandle: int
    spawngroupmanifest: bytes
    manifestincomplete: bool
    def __init__(
        self,
        spawngrouphandle: int | None = ...,
        spawngroupmanifest: bytes | None = ...,
        manifestincomplete: bool = ...,
    ) -> None: ...

class CNETMsg_SpawnGroup_SetCreationTick(_message.Message):
    __slots__ = ("spawngrouphandle", "tickcount", "creationsequence")
    SPAWNGROUPHANDLE_FIELD_NUMBER: _ClassVar[int]
    TICKCOUNT_FIELD_NUMBER: _ClassVar[int]
    CREATIONSEQUENCE_FIELD_NUMBER: _ClassVar[int]
    spawngrouphandle: int
    tickcount: int
    creationsequence: int
    def __init__(
        self,
        spawngrouphandle: int | None = ...,
        tickcount: int | None = ...,
        creationsequence: int | None = ...,
    ) -> None: ...

class CNETMsg_SpawnGroup_Unload(_message.Message):
    __slots__ = ("spawngrouphandle", "flags", "tickcount")
    SPAWNGROUPHANDLE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    TICKCOUNT_FIELD_NUMBER: _ClassVar[int]
    spawngrouphandle: int
    flags: int
    tickcount: int
    def __init__(
        self,
        spawngrouphandle: int | None = ...,
        flags: int | None = ...,
        tickcount: int | None = ...,
    ) -> None: ...

class CNETMsg_SpawnGroup_LoadCompleted(_message.Message):
    __slots__ = ("spawngrouphandle",)
    SPAWNGROUPHANDLE_FIELD_NUMBER: _ClassVar[int]
    spawngrouphandle: int
    def __init__(self, spawngrouphandle: int | None = ...) -> None: ...

class CSVCMsg_GameSessionConfiguration(_message.Message):
    __slots__ = (
        "is_multiplayer",
        "is_loadsavegame",
        "is_background_map",
        "is_headless",
        "min_client_limit",
        "max_client_limit",
        "max_clients",
        "tick_interval",
        "hostname",
        "savegamename",
        "s1_mapname",
        "gamemode",
        "server_ip_address",
        "data",
        "is_localonly",
        "no_steam_server",
        "is_transition",
        "previouslevel",
        "landmarkname",
    )
    IS_MULTIPLAYER_FIELD_NUMBER: _ClassVar[int]
    IS_LOADSAVEGAME_FIELD_NUMBER: _ClassVar[int]
    IS_BACKGROUND_MAP_FIELD_NUMBER: _ClassVar[int]
    IS_HEADLESS_FIELD_NUMBER: _ClassVar[int]
    MIN_CLIENT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAX_CLIENT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAX_CLIENTS_FIELD_NUMBER: _ClassVar[int]
    TICK_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    SAVEGAMENAME_FIELD_NUMBER: _ClassVar[int]
    S1_MAPNAME_FIELD_NUMBER: _ClassVar[int]
    GAMEMODE_FIELD_NUMBER: _ClassVar[int]
    SERVER_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LOCALONLY_FIELD_NUMBER: _ClassVar[int]
    NO_STEAM_SERVER_FIELD_NUMBER: _ClassVar[int]
    IS_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    PREVIOUSLEVEL_FIELD_NUMBER: _ClassVar[int]
    LANDMARKNAME_FIELD_NUMBER: _ClassVar[int]
    is_multiplayer: bool
    is_loadsavegame: bool
    is_background_map: bool
    is_headless: bool
    min_client_limit: int
    max_client_limit: int
    max_clients: int
    tick_interval: int
    hostname: str
    savegamename: str
    s1_mapname: str
    gamemode: str
    server_ip_address: str
    data: bytes
    is_localonly: bool
    no_steam_server: bool
    is_transition: bool
    previouslevel: str
    landmarkname: str
    def __init__(
        self,
        is_multiplayer: bool = ...,
        is_loadsavegame: bool = ...,
        is_background_map: bool = ...,
        is_headless: bool = ...,
        min_client_limit: int | None = ...,
        max_client_limit: int | None = ...,
        max_clients: int | None = ...,
        tick_interval: int | None = ...,
        hostname: str | None = ...,
        savegamename: str | None = ...,
        s1_mapname: str | None = ...,
        gamemode: str | None = ...,
        server_ip_address: str | None = ...,
        data: bytes | None = ...,
        is_localonly: bool = ...,
        no_steam_server: bool = ...,
        is_transition: bool = ...,
        previouslevel: str | None = ...,
        landmarkname: str | None = ...,
    ) -> None: ...

class CNETMsg_DebugOverlay(_message.Message):
    __slots__ = ("etype", "vectors", "colors", "dimensions", "times", "bools", "uint64s", "strings")
    ETYPE_FIELD_NUMBER: _ClassVar[int]
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    COLORS_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    TIMES_FIELD_NUMBER: _ClassVar[int]
    BOOLS_FIELD_NUMBER: _ClassVar[int]
    UINT64S_FIELD_NUMBER: _ClassVar[int]
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    etype: int
    vectors: _containers.RepeatedCompositeFieldContainer[CMsgVector]
    colors: _containers.RepeatedCompositeFieldContainer[CMsgRGBA]
    dimensions: _containers.RepeatedScalarFieldContainer[float]
    times: _containers.RepeatedScalarFieldContainer[float]
    bools: _containers.RepeatedScalarFieldContainer[bool]
    uint64s: _containers.RepeatedScalarFieldContainer[int]
    strings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        etype: int | None = ...,
        vectors: _Iterable[CMsgVector | _Mapping] | None = ...,
        colors: _Iterable[CMsgRGBA | _Mapping] | None = ...,
        dimensions: _Iterable[float] | None = ...,
        times: _Iterable[float] | None = ...,
        bools: _Iterable[bool] | None = ...,
        uint64s: _Iterable[int] | None = ...,
        strings: _Iterable[str] | None = ...,
    ) -> None: ...
