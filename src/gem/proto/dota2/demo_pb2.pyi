from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EDemoCommands(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEM_Error: _ClassVar[EDemoCommands]
    DEM_Stop: _ClassVar[EDemoCommands]
    DEM_FileHeader: _ClassVar[EDemoCommands]
    DEM_FileInfo: _ClassVar[EDemoCommands]
    DEM_SyncTick: _ClassVar[EDemoCommands]
    DEM_SendTables: _ClassVar[EDemoCommands]
    DEM_ClassInfo: _ClassVar[EDemoCommands]
    DEM_StringTables: _ClassVar[EDemoCommands]
    DEM_Packet: _ClassVar[EDemoCommands]
    DEM_SignonPacket: _ClassVar[EDemoCommands]
    DEM_ConsoleCmd: _ClassVar[EDemoCommands]
    DEM_CustomData: _ClassVar[EDemoCommands]
    DEM_CustomDataCallbacks: _ClassVar[EDemoCommands]
    DEM_UserCmd: _ClassVar[EDemoCommands]
    DEM_FullPacket: _ClassVar[EDemoCommands]
    DEM_SaveGame: _ClassVar[EDemoCommands]
    DEM_SpawnGroups: _ClassVar[EDemoCommands]
    DEM_AnimationData: _ClassVar[EDemoCommands]
    DEM_AnimationHeader: _ClassVar[EDemoCommands]
    DEM_Recovery: _ClassVar[EDemoCommands]
    DEM_Max: _ClassVar[EDemoCommands]
    DEM_IsCompressed: _ClassVar[EDemoCommands]

DEM_Error: EDemoCommands
DEM_Stop: EDemoCommands
DEM_FileHeader: EDemoCommands
DEM_FileInfo: EDemoCommands
DEM_SyncTick: EDemoCommands
DEM_SendTables: EDemoCommands
DEM_ClassInfo: EDemoCommands
DEM_StringTables: EDemoCommands
DEM_Packet: EDemoCommands
DEM_SignonPacket: EDemoCommands
DEM_ConsoleCmd: EDemoCommands
DEM_CustomData: EDemoCommands
DEM_CustomDataCallbacks: EDemoCommands
DEM_UserCmd: EDemoCommands
DEM_FullPacket: EDemoCommands
DEM_SaveGame: EDemoCommands
DEM_SpawnGroups: EDemoCommands
DEM_AnimationData: EDemoCommands
DEM_AnimationHeader: EDemoCommands
DEM_Recovery: EDemoCommands
DEM_Max: EDemoCommands
DEM_IsCompressed: EDemoCommands

class CDemoFileHeader(_message.Message):
    __slots__ = (
        "demo_file_stamp",
        "patch_version",
        "server_name",
        "client_name",
        "map_name",
        "game_directory",
        "fullpackets_version",
        "allow_clientside_entities",
        "allow_clientside_particles",
        "addons",
        "demo_version_name",
        "demo_version_guid",
        "build_num",
        "game",
        "server_start_tick",
    )
    DEMO_FILE_STAMP_FIELD_NUMBER: _ClassVar[int]
    PATCH_VERSION_FIELD_NUMBER: _ClassVar[int]
    SERVER_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    GAME_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    FULLPACKETS_VERSION_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CLIENTSIDE_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CLIENTSIDE_PARTICLES_FIELD_NUMBER: _ClassVar[int]
    ADDONS_FIELD_NUMBER: _ClassVar[int]
    DEMO_VERSION_NAME_FIELD_NUMBER: _ClassVar[int]
    DEMO_VERSION_GUID_FIELD_NUMBER: _ClassVar[int]
    BUILD_NUM_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_START_TICK_FIELD_NUMBER: _ClassVar[int]
    demo_file_stamp: str
    patch_version: int
    server_name: str
    client_name: str
    map_name: str
    game_directory: str
    fullpackets_version: int
    allow_clientside_entities: bool
    allow_clientside_particles: bool
    addons: str
    demo_version_name: str
    demo_version_guid: str
    build_num: int
    game: str
    server_start_tick: int
    def __init__(
        self,
        demo_file_stamp: str | None = ...,
        patch_version: int | None = ...,
        server_name: str | None = ...,
        client_name: str | None = ...,
        map_name: str | None = ...,
        game_directory: str | None = ...,
        fullpackets_version: int | None = ...,
        allow_clientside_entities: bool = ...,
        allow_clientside_particles: bool = ...,
        addons: str | None = ...,
        demo_version_name: str | None = ...,
        demo_version_guid: str | None = ...,
        build_num: int | None = ...,
        game: str | None = ...,
        server_start_tick: int | None = ...,
    ) -> None: ...

class CGameInfo(_message.Message):
    __slots__ = ("dota", "cs")
    class CDotaGameInfo(_message.Message):
        __slots__ = (
            "match_id",
            "game_mode",
            "game_winner",
            "player_info",
            "leagueid",
            "picks_bans",
            "radiant_team_id",
            "dire_team_id",
            "radiant_team_tag",
            "dire_team_tag",
            "end_time",
        )
        class CPlayerInfo(_message.Message):
            __slots__ = ("hero_name", "player_name", "is_fake_client", "steamid", "game_team")
            HERO_NAME_FIELD_NUMBER: _ClassVar[int]
            PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
            IS_FAKE_CLIENT_FIELD_NUMBER: _ClassVar[int]
            STEAMID_FIELD_NUMBER: _ClassVar[int]
            GAME_TEAM_FIELD_NUMBER: _ClassVar[int]
            hero_name: str
            player_name: str
            is_fake_client: bool
            steamid: int
            game_team: int
            def __init__(
                self,
                hero_name: str | None = ...,
                player_name: str | None = ...,
                is_fake_client: bool = ...,
                steamid: int | None = ...,
                game_team: int | None = ...,
            ) -> None: ...

        class CHeroSelectEvent(_message.Message):
            __slots__ = ("is_pick", "team", "hero_id")
            IS_PICK_FIELD_NUMBER: _ClassVar[int]
            TEAM_FIELD_NUMBER: _ClassVar[int]
            HERO_ID_FIELD_NUMBER: _ClassVar[int]
            is_pick: bool
            team: int
            hero_id: int
            def __init__(
                self, is_pick: bool = ..., team: int | None = ..., hero_id: int | None = ...
            ) -> None: ...

        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        GAME_MODE_FIELD_NUMBER: _ClassVar[int]
        GAME_WINNER_FIELD_NUMBER: _ClassVar[int]
        PLAYER_INFO_FIELD_NUMBER: _ClassVar[int]
        LEAGUEID_FIELD_NUMBER: _ClassVar[int]
        PICKS_BANS_FIELD_NUMBER: _ClassVar[int]
        RADIANT_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        DIRE_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        RADIANT_TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
        DIRE_TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        game_mode: int
        game_winner: int
        player_info: _containers.RepeatedCompositeFieldContainer[
            CGameInfo.CDotaGameInfo.CPlayerInfo
        ]
        leagueid: int
        picks_bans: _containers.RepeatedCompositeFieldContainer[
            CGameInfo.CDotaGameInfo.CHeroSelectEvent
        ]
        radiant_team_id: int
        dire_team_id: int
        radiant_team_tag: str
        dire_team_tag: str
        end_time: int
        def __init__(
            self,
            match_id: int | None = ...,
            game_mode: int | None = ...,
            game_winner: int | None = ...,
            player_info: _Iterable[CGameInfo.CDotaGameInfo.CPlayerInfo | _Mapping] | None = ...,
            leagueid: int | None = ...,
            picks_bans: _Iterable[CGameInfo.CDotaGameInfo.CHeroSelectEvent | _Mapping] | None = ...,
            radiant_team_id: int | None = ...,
            dire_team_id: int | None = ...,
            radiant_team_tag: str | None = ...,
            dire_team_tag: str | None = ...,
            end_time: int | None = ...,
        ) -> None: ...

    class CCSGameInfo(_message.Message):
        __slots__ = ("round_start_ticks",)
        ROUND_START_TICKS_FIELD_NUMBER: _ClassVar[int]
        round_start_ticks: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, round_start_ticks: _Iterable[int] | None = ...) -> None: ...

    DOTA_FIELD_NUMBER: _ClassVar[int]
    CS_FIELD_NUMBER: _ClassVar[int]
    dota: CGameInfo.CDotaGameInfo
    cs: CGameInfo.CCSGameInfo
    def __init__(
        self,
        dota: CGameInfo.CDotaGameInfo | _Mapping | None = ...,
        cs: CGameInfo.CCSGameInfo | _Mapping | None = ...,
    ) -> None: ...

class CDemoFileInfo(_message.Message):
    __slots__ = ("playback_time", "playback_ticks", "playback_frames", "game_info")
    PLAYBACK_TIME_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_TICKS_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_FRAMES_FIELD_NUMBER: _ClassVar[int]
    GAME_INFO_FIELD_NUMBER: _ClassVar[int]
    playback_time: float
    playback_ticks: int
    playback_frames: int
    game_info: CGameInfo
    def __init__(
        self,
        playback_time: float | None = ...,
        playback_ticks: int | None = ...,
        playback_frames: int | None = ...,
        game_info: CGameInfo | _Mapping | None = ...,
    ) -> None: ...

class CDemoPacket(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: bytes | None = ...) -> None: ...

class CDemoFullPacket(_message.Message):
    __slots__ = ("string_table", "packet")
    STRING_TABLE_FIELD_NUMBER: _ClassVar[int]
    PACKET_FIELD_NUMBER: _ClassVar[int]
    string_table: CDemoStringTables
    packet: CDemoPacket
    def __init__(
        self,
        string_table: CDemoStringTables | _Mapping | None = ...,
        packet: CDemoPacket | _Mapping | None = ...,
    ) -> None: ...

class CDemoSaveGame(_message.Message):
    __slots__ = ("data", "steam_id", "signature", "version")
    DATA_FIELD_NUMBER: _ClassVar[int]
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    steam_id: int
    signature: int
    version: int
    def __init__(
        self,
        data: bytes | None = ...,
        steam_id: int | None = ...,
        signature: int | None = ...,
        version: int | None = ...,
    ) -> None: ...

class CDemoSyncTick(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDemoConsoleCmd(_message.Message):
    __slots__ = ("cmdstring",)
    CMDSTRING_FIELD_NUMBER: _ClassVar[int]
    cmdstring: str
    def __init__(self, cmdstring: str | None = ...) -> None: ...

class CDemoSendTables(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: bytes | None = ...) -> None: ...

class CDemoClassInfo(_message.Message):
    __slots__ = ("classes",)
    class class_t(_message.Message):
        __slots__ = ("class_id", "network_name", "table_name")
        CLASS_ID_FIELD_NUMBER: _ClassVar[int]
        NETWORK_NAME_FIELD_NUMBER: _ClassVar[int]
        TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
        class_id: int
        network_name: str
        table_name: str
        def __init__(
            self,
            class_id: int | None = ...,
            network_name: str | None = ...,
            table_name: str | None = ...,
        ) -> None: ...

    CLASSES_FIELD_NUMBER: _ClassVar[int]
    classes: _containers.RepeatedCompositeFieldContainer[CDemoClassInfo.class_t]
    def __init__(
        self, classes: _Iterable[CDemoClassInfo.class_t | _Mapping] | None = ...
    ) -> None: ...

class CDemoCustomData(_message.Message):
    __slots__ = ("callback_index", "data")
    CALLBACK_INDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    callback_index: int
    data: bytes
    def __init__(self, callback_index: int | None = ..., data: bytes | None = ...) -> None: ...

class CDemoCustomDataCallbacks(_message.Message):
    __slots__ = ("save_id",)
    SAVE_ID_FIELD_NUMBER: _ClassVar[int]
    save_id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, save_id: _Iterable[str] | None = ...) -> None: ...

class CDemoAnimationHeader(_message.Message):
    __slots__ = ("entity_id", "tick", "data")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    TICK_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    entity_id: int
    tick: int
    data: bytes
    def __init__(
        self, entity_id: int | None = ..., tick: int | None = ..., data: bytes | None = ...
    ) -> None: ...

class CDemoAnimationData(_message.Message):
    __slots__ = ("entity_id", "start_tick", "end_tick", "data", "data_checksum")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    START_TICK_FIELD_NUMBER: _ClassVar[int]
    END_TICK_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    entity_id: int
    start_tick: int
    end_tick: int
    data: bytes
    data_checksum: int
    def __init__(
        self,
        entity_id: int | None = ...,
        start_tick: int | None = ...,
        end_tick: int | None = ...,
        data: bytes | None = ...,
        data_checksum: int | None = ...,
    ) -> None: ...

class CDemoStringTables(_message.Message):
    __slots__ = ("tables",)
    class items_t(_message.Message):
        __slots__ = ("str", "data")
        STR_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        str: str
        data: bytes
        def __init__(self, str: str | None = ..., data: bytes | None = ...) -> None: ...

    class table_t(_message.Message):
        __slots__ = ("table_name", "items", "items_clientside", "table_flags")
        TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        ITEMS_CLIENTSIDE_FIELD_NUMBER: _ClassVar[int]
        TABLE_FLAGS_FIELD_NUMBER: _ClassVar[int]
        table_name: str
        items: _containers.RepeatedCompositeFieldContainer[CDemoStringTables.items_t]
        items_clientside: _containers.RepeatedCompositeFieldContainer[CDemoStringTables.items_t]
        table_flags: int
        def __init__(
            self,
            table_name: str | None = ...,
            items: _Iterable[CDemoStringTables.items_t | _Mapping] | None = ...,
            items_clientside: _Iterable[CDemoStringTables.items_t | _Mapping] | None = ...,
            table_flags: int | None = ...,
        ) -> None: ...

    TABLES_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.RepeatedCompositeFieldContainer[CDemoStringTables.table_t]
    def __init__(
        self, tables: _Iterable[CDemoStringTables.table_t | _Mapping] | None = ...
    ) -> None: ...

class CDemoStop(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDemoUserCmd(_message.Message):
    __slots__ = ("cmd_number", "data")
    CMD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    cmd_number: int
    data: bytes
    def __init__(self, cmd_number: int | None = ..., data: bytes | None = ...) -> None: ...

class CDemoSpawnGroups(_message.Message):
    __slots__ = ("msgs",)
    MSGS_FIELD_NUMBER: _ClassVar[int]
    msgs: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, msgs: _Iterable[bytes] | None = ...) -> None: ...

class CDemoRecovery(_message.Message):
    __slots__ = ("initial_spawn_group", "spawn_group_message")
    class DemoInitialSpawnGroupEntry(_message.Message):
        __slots__ = ("spawngrouphandle", "was_created")
        SPAWNGROUPHANDLE_FIELD_NUMBER: _ClassVar[int]
        WAS_CREATED_FIELD_NUMBER: _ClassVar[int]
        spawngrouphandle: int
        was_created: bool
        def __init__(self, spawngrouphandle: int | None = ..., was_created: bool = ...) -> None: ...

    INITIAL_SPAWN_GROUP_FIELD_NUMBER: _ClassVar[int]
    SPAWN_GROUP_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    initial_spawn_group: CDemoRecovery.DemoInitialSpawnGroupEntry
    spawn_group_message: bytes
    def __init__(
        self,
        initial_spawn_group: CDemoRecovery.DemoInitialSpawnGroupEntry | _Mapping | None = ...,
        spawn_group_message: bytes | None = ...,
    ) -> None: ...
