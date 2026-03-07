from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf.internal import python_message as _python_message

DESCRIPTOR: _descriptor.FileDescriptor

class EBaseUserMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UM_AchievementEvent: _ClassVar[EBaseUserMessages]
    UM_CloseCaption: _ClassVar[EBaseUserMessages]
    UM_CloseCaptionDirect: _ClassVar[EBaseUserMessages]
    UM_CurrentTimescale: _ClassVar[EBaseUserMessages]
    UM_DesiredTimescale: _ClassVar[EBaseUserMessages]
    UM_Fade: _ClassVar[EBaseUserMessages]
    UM_GameTitle: _ClassVar[EBaseUserMessages]
    UM_HudMsg: _ClassVar[EBaseUserMessages]
    UM_HudText: _ClassVar[EBaseUserMessages]
    UM_ColoredText: _ClassVar[EBaseUserMessages]
    UM_RequestState: _ClassVar[EBaseUserMessages]
    UM_ResetHUD: _ClassVar[EBaseUserMessages]
    UM_Rumble: _ClassVar[EBaseUserMessages]
    UM_SayText: _ClassVar[EBaseUserMessages]
    UM_SayText2: _ClassVar[EBaseUserMessages]
    UM_SayTextChannel: _ClassVar[EBaseUserMessages]
    UM_Shake: _ClassVar[EBaseUserMessages]
    UM_ShakeDir: _ClassVar[EBaseUserMessages]
    UM_WaterShake: _ClassVar[EBaseUserMessages]
    UM_TextMsg: _ClassVar[EBaseUserMessages]
    UM_ScreenTilt: _ClassVar[EBaseUserMessages]
    UM_VoiceMask: _ClassVar[EBaseUserMessages]
    UM_SendAudio: _ClassVar[EBaseUserMessages]
    UM_ItemPickup: _ClassVar[EBaseUserMessages]
    UM_AmmoDenied: _ClassVar[EBaseUserMessages]
    UM_ShowMenu: _ClassVar[EBaseUserMessages]
    UM_CreditsMsg: _ClassVar[EBaseUserMessages]
    UM_CloseCaptionPlaceholder: _ClassVar[EBaseUserMessages]
    UM_CameraTransition: _ClassVar[EBaseUserMessages]
    UM_AudioParameter: _ClassVar[EBaseUserMessages]
    UM_ParticleManager: _ClassVar[EBaseUserMessages]
    UM_HudError: _ClassVar[EBaseUserMessages]
    UM_CustomGameEvent: _ClassVar[EBaseUserMessages]
    UM_AnimGraphUpdate: _ClassVar[EBaseUserMessages]
    UM_HapticsManagerPulse: _ClassVar[EBaseUserMessages]
    UM_HapticsManagerEffect: _ClassVar[EBaseUserMessages]
    UM_UpdateCssClasses: _ClassVar[EBaseUserMessages]
    UM_ServerFrameTime: _ClassVar[EBaseUserMessages]
    UM_LagCompensationError: _ClassVar[EBaseUserMessages]
    UM_RequestDllStatus: _ClassVar[EBaseUserMessages]
    UM_RequestUtilAction: _ClassVar[EBaseUserMessages]
    UM_UtilActionResponse: _ClassVar[EBaseUserMessages]
    UM_DllStatusResponse: _ClassVar[EBaseUserMessages]
    UM_RequestInventory: _ClassVar[EBaseUserMessages]
    UM_InventoryResponse: _ClassVar[EBaseUserMessages]
    UM_RequestDiagnostic: _ClassVar[EBaseUserMessages]
    UM_DiagnosticResponse: _ClassVar[EBaseUserMessages]
    UM_ExtraUserData: _ClassVar[EBaseUserMessages]
    UM_NotifyResponseFound: _ClassVar[EBaseUserMessages]
    UM_PlayResponseConditional: _ClassVar[EBaseUserMessages]
    UM_MAX_BASE: _ClassVar[EBaseUserMessages]

class EBaseEntityMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EM_PlayJingle: _ClassVar[EBaseEntityMessages]
    EM_ScreenOverlay: _ClassVar[EBaseEntityMessages]
    EM_RemoveAllDecals: _ClassVar[EBaseEntityMessages]
    EM_PropagateForce: _ClassVar[EBaseEntityMessages]
    EM_DoSpark: _ClassVar[EBaseEntityMessages]
    EM_FixAngle: _ClassVar[EBaseEntityMessages]

class eRollType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLL_NONE: _ClassVar[eRollType]
    ROLL_STATS: _ClassVar[eRollType]
    ROLL_CREDITS: _ClassVar[eRollType]
    ROLL_LATE_JOIN_LOGO: _ClassVar[eRollType]
    ROLL_OUTTRO: _ClassVar[eRollType]

class PARTICLE_MESSAGE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GAME_PARTICLE_MANAGER_EVENT_CREATE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_FORWARD: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_ORIENTATION: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_FALLBACK: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_ENT: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_OFFSET: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_DESTROY: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_DESTROY_INVOLVING: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_RELEASE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_LATENCY: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SHOULD_DRAW: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_FROZEN: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_CHANGE_CONTROL_POINT_ATTACHMENT: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_ENTITY_POSITION: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_FOW_PROPERTIES: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_TEXT: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_SHOULD_CHECK_FOW: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_CONTROL_POINT_MODEL: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_CONTROL_POINT_SNAPSHOT: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_TEXTURE_ATTRIBUTE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_SCENE_OBJECT_GENERIC_FLAG: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_SCENE_OBJECT_TINT_AND_DESAT: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_DESTROY_NAMED: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SKIP_TO_TIME: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_CAN_FREEZE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_NAMED_VALUE_CONTEXT: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_TRANSFORM: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_FREEZE_TRANSITION_OVERRIDE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_FREEZE_INVOLVING: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_ADD_MODELLIST_OVERRIDE_ELEMENT: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_CLEAR_MODELLIST_OVERRIDE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_CREATE_PHYSICS_SIM: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_DESTROY_PHYSICS_SIM: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_VDATA: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_MATERIAL_OVERRIDE: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_ADD_FAN: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_UPDATE_FAN: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_SET_CLUSTER_GROWTH: _ClassVar[PARTICLE_MESSAGE]
    GAME_PARTICLE_MANAGER_EVENT_REMOVE_FAN: _ClassVar[PARTICLE_MESSAGE]

class EHapticPulseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VR_HAND_HAPTIC_PULSE_LIGHT: _ClassVar[EHapticPulseType]
    VR_HAND_HAPTIC_PULSE_MEDIUM: _ClassVar[EHapticPulseType]
    VR_HAND_HAPTIC_PULSE_STRONG: _ClassVar[EHapticPulseType]

UM_AchievementEvent: EBaseUserMessages
UM_CloseCaption: EBaseUserMessages
UM_CloseCaptionDirect: EBaseUserMessages
UM_CurrentTimescale: EBaseUserMessages
UM_DesiredTimescale: EBaseUserMessages
UM_Fade: EBaseUserMessages
UM_GameTitle: EBaseUserMessages
UM_HudMsg: EBaseUserMessages
UM_HudText: EBaseUserMessages
UM_ColoredText: EBaseUserMessages
UM_RequestState: EBaseUserMessages
UM_ResetHUD: EBaseUserMessages
UM_Rumble: EBaseUserMessages
UM_SayText: EBaseUserMessages
UM_SayText2: EBaseUserMessages
UM_SayTextChannel: EBaseUserMessages
UM_Shake: EBaseUserMessages
UM_ShakeDir: EBaseUserMessages
UM_WaterShake: EBaseUserMessages
UM_TextMsg: EBaseUserMessages
UM_ScreenTilt: EBaseUserMessages
UM_VoiceMask: EBaseUserMessages
UM_SendAudio: EBaseUserMessages
UM_ItemPickup: EBaseUserMessages
UM_AmmoDenied: EBaseUserMessages
UM_ShowMenu: EBaseUserMessages
UM_CreditsMsg: EBaseUserMessages
UM_CloseCaptionPlaceholder: EBaseUserMessages
UM_CameraTransition: EBaseUserMessages
UM_AudioParameter: EBaseUserMessages
UM_ParticleManager: EBaseUserMessages
UM_HudError: EBaseUserMessages
UM_CustomGameEvent: EBaseUserMessages
UM_AnimGraphUpdate: EBaseUserMessages
UM_HapticsManagerPulse: EBaseUserMessages
UM_HapticsManagerEffect: EBaseUserMessages
UM_UpdateCssClasses: EBaseUserMessages
UM_ServerFrameTime: EBaseUserMessages
UM_LagCompensationError: EBaseUserMessages
UM_RequestDllStatus: EBaseUserMessages
UM_RequestUtilAction: EBaseUserMessages
UM_UtilActionResponse: EBaseUserMessages
UM_DllStatusResponse: EBaseUserMessages
UM_RequestInventory: EBaseUserMessages
UM_InventoryResponse: EBaseUserMessages
UM_RequestDiagnostic: EBaseUserMessages
UM_DiagnosticResponse: EBaseUserMessages
UM_ExtraUserData: EBaseUserMessages
UM_NotifyResponseFound: EBaseUserMessages
UM_PlayResponseConditional: EBaseUserMessages
UM_MAX_BASE: EBaseUserMessages
EM_PlayJingle: EBaseEntityMessages
EM_ScreenOverlay: EBaseEntityMessages
EM_RemoveAllDecals: EBaseEntityMessages
EM_PropagateForce: EBaseEntityMessages
EM_DoSpark: EBaseEntityMessages
EM_FixAngle: EBaseEntityMessages
ROLL_NONE: eRollType
ROLL_STATS: eRollType
ROLL_CREDITS: eRollType
ROLL_LATE_JOIN_LOGO: eRollType
ROLL_OUTTRO: eRollType
GAME_PARTICLE_MANAGER_EVENT_CREATE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_FORWARD: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_ORIENTATION: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_FALLBACK: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_ENT: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_OFFSET: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_DESTROY: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_DESTROY_INVOLVING: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_RELEASE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_LATENCY: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SHOULD_DRAW: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_FROZEN: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_CHANGE_CONTROL_POINT_ATTACHMENT: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_ENTITY_POSITION: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_FOW_PROPERTIES: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_TEXT: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_SHOULD_CHECK_FOW: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_CONTROL_POINT_MODEL: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_CONTROL_POINT_SNAPSHOT: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_TEXTURE_ATTRIBUTE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_SCENE_OBJECT_GENERIC_FLAG: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_SCENE_OBJECT_TINT_AND_DESAT: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_DESTROY_NAMED: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SKIP_TO_TIME: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_CAN_FREEZE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_NAMED_VALUE_CONTEXT: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_TRANSFORM: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_FREEZE_TRANSITION_OVERRIDE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_FREEZE_INVOLVING: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_ADD_MODELLIST_OVERRIDE_ELEMENT: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_CLEAR_MODELLIST_OVERRIDE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_CREATE_PHYSICS_SIM: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_DESTROY_PHYSICS_SIM: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_VDATA: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_MATERIAL_OVERRIDE: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_ADD_FAN: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_UPDATE_FAN: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_SET_CLUSTER_GROWTH: PARTICLE_MESSAGE
GAME_PARTICLE_MANAGER_EVENT_REMOVE_FAN: PARTICLE_MESSAGE
VR_HAND_HAPTIC_PULSE_LIGHT: EHapticPulseType
VR_HAND_HAPTIC_PULSE_MEDIUM: EHapticPulseType
VR_HAND_HAPTIC_PULSE_STRONG: EHapticPulseType

class CUserMessageAchievementEvent(_message.Message):
    __slots__ = ("achievement",)
    ACHIEVEMENT_FIELD_NUMBER: _ClassVar[int]
    achievement: int
    def __init__(self, achievement: int | None = ...) -> None: ...

class CUserMessageCloseCaption(_message.Message):
    __slots__ = ("hash", "duration", "from_player", "ent_index")
    HASH_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FROM_PLAYER_FIELD_NUMBER: _ClassVar[int]
    ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    hash: int
    duration: float
    from_player: bool
    ent_index: int
    def __init__(
        self,
        hash: int | None = ...,
        duration: float | None = ...,
        from_player: bool = ...,
        ent_index: int | None = ...,
    ) -> None: ...

class CUserMessageCloseCaptionDirect(_message.Message):
    __slots__ = ("hash", "duration", "from_player", "ent_index")
    HASH_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FROM_PLAYER_FIELD_NUMBER: _ClassVar[int]
    ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    hash: int
    duration: float
    from_player: bool
    ent_index: int
    def __init__(
        self,
        hash: int | None = ...,
        duration: float | None = ...,
        from_player: bool = ...,
        ent_index: int | None = ...,
    ) -> None: ...

class CUserMessageCloseCaptionPlaceholder(_message.Message):
    __slots__ = ("string", "duration", "from_player", "ent_index")
    STRING_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FROM_PLAYER_FIELD_NUMBER: _ClassVar[int]
    ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    string: str
    duration: float
    from_player: bool
    ent_index: int
    def __init__(
        self,
        string: str | None = ...,
        duration: float | None = ...,
        from_player: bool = ...,
        ent_index: int | None = ...,
    ) -> None: ...

class CUserMessageCurrentTimescale(_message.Message):
    __slots__ = ("current",)
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    current: float
    def __init__(self, current: float | None = ...) -> None: ...

class CUserMessageDesiredTimescale(_message.Message):
    __slots__ = ("desired", "acceleration", "minblendrate", "blenddeltamultiplier")
    DESIRED_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    MINBLENDRATE_FIELD_NUMBER: _ClassVar[int]
    BLENDDELTAMULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    desired: float
    acceleration: float
    minblendrate: float
    blenddeltamultiplier: float
    def __init__(
        self,
        desired: float | None = ...,
        acceleration: float | None = ...,
        minblendrate: float | None = ...,
        blenddeltamultiplier: float | None = ...,
    ) -> None: ...

class CUserMessageFade(_message.Message):
    __slots__ = ("duration", "hold_time", "flags", "color")
    DURATION_FIELD_NUMBER: _ClassVar[int]
    HOLD_TIME_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    duration: int
    hold_time: int
    flags: int
    color: int
    def __init__(
        self,
        duration: int | None = ...,
        hold_time: int | None = ...,
        flags: int | None = ...,
        color: int | None = ...,
    ) -> None: ...

class CUserMessageShake(_message.Message):
    __slots__ = ("command", "amplitude", "frequency", "duration")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    command: int
    amplitude: float
    frequency: float
    duration: float
    def __init__(
        self,
        command: int | None = ...,
        amplitude: float | None = ...,
        frequency: float | None = ...,
        duration: float | None = ...,
    ) -> None: ...

class CUserMessageShakeDir(_message.Message):
    __slots__ = ("shake", "direction")
    SHAKE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    shake: CUserMessageShake
    direction: _networkbasetypes_pb2.CMsgVector
    def __init__(
        self,
        shake: CUserMessageShake | _Mapping | None = ...,
        direction: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
    ) -> None: ...

class CUserMessageWaterShake(_message.Message):
    __slots__ = ("command", "amplitude", "frequency", "duration")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    command: int
    amplitude: float
    frequency: float
    duration: float
    def __init__(
        self,
        command: int | None = ...,
        amplitude: float | None = ...,
        frequency: float | None = ...,
        duration: float | None = ...,
    ) -> None: ...

class CUserMessageScreenTilt(_message.Message):
    __slots__ = ("command", "ease_in_out", "angle", "duration", "time")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    EASE_IN_OUT_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    command: int
    ease_in_out: bool
    angle: _networkbasetypes_pb2.CMsgVector
    duration: float
    time: float
    def __init__(
        self,
        command: int | None = ...,
        ease_in_out: bool = ...,
        angle: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        duration: float | None = ...,
        time: float | None = ...,
    ) -> None: ...

class CUserMessageSayText(_message.Message):
    __slots__ = ("playerindex", "text", "chat")
    PLAYERINDEX_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    playerindex: int
    text: str
    chat: bool
    def __init__(
        self, playerindex: int | None = ..., text: str | None = ..., chat: bool = ...
    ) -> None: ...

class CUserMessageSayText2(_message.Message):
    __slots__ = ("entityindex", "chat", "messagename", "param1", "param2", "param3", "param4")
    ENTITYINDEX_FIELD_NUMBER: _ClassVar[int]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    MESSAGENAME_FIELD_NUMBER: _ClassVar[int]
    PARAM1_FIELD_NUMBER: _ClassVar[int]
    PARAM2_FIELD_NUMBER: _ClassVar[int]
    PARAM3_FIELD_NUMBER: _ClassVar[int]
    PARAM4_FIELD_NUMBER: _ClassVar[int]
    entityindex: int
    chat: bool
    messagename: str
    param1: str
    param2: str
    param3: str
    param4: str
    def __init__(
        self,
        entityindex: int | None = ...,
        chat: bool = ...,
        messagename: str | None = ...,
        param1: str | None = ...,
        param2: str | None = ...,
        param3: str | None = ...,
        param4: str | None = ...,
    ) -> None: ...

class CUserMessageHudMsg(_message.Message):
    __slots__ = ("channel", "x", "y", "color1", "color2", "effect", "message")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    COLOR1_FIELD_NUMBER: _ClassVar[int]
    COLOR2_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    channel: int
    x: float
    y: float
    color1: int
    color2: int
    effect: int
    message: str
    def __init__(
        self,
        channel: int | None = ...,
        x: float | None = ...,
        y: float | None = ...,
        color1: int | None = ...,
        color2: int | None = ...,
        effect: int | None = ...,
        message: str | None = ...,
    ) -> None: ...

class CUserMessageHudText(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: str | None = ...) -> None: ...

class CUserMessageTextMsg(_message.Message):
    __slots__ = ("dest", "param")
    DEST_FIELD_NUMBER: _ClassVar[int]
    PARAM_FIELD_NUMBER: _ClassVar[int]
    dest: int
    param: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dest: int | None = ..., param: _Iterable[str] | None = ...) -> None: ...

class CUserMessageGameTitle(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CUserMessageResetHUD(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CUserMessageSendAudio(_message.Message):
    __slots__ = ("soundname", "stop")
    SOUNDNAME_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    soundname: str
    stop: bool
    def __init__(self, soundname: str | None = ..., stop: bool = ...) -> None: ...

class CUserMessageAudioParameter(_message.Message):
    __slots__ = ("parameter_type", "name_hash_code", "value", "int_value")
    PARAMETER_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_HASH_CODE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    parameter_type: int
    name_hash_code: int
    value: float
    int_value: int
    def __init__(
        self,
        parameter_type: int | None = ...,
        name_hash_code: int | None = ...,
        value: float | None = ...,
        int_value: int | None = ...,
    ) -> None: ...

class CUserMessageVoiceMask(_message.Message):
    __slots__ = ("gamerules_masks", "ban_masks", "mod_enable")
    GAMERULES_MASKS_FIELD_NUMBER: _ClassVar[int]
    BAN_MASKS_FIELD_NUMBER: _ClassVar[int]
    MOD_ENABLE_FIELD_NUMBER: _ClassVar[int]
    gamerules_masks: _containers.RepeatedScalarFieldContainer[int]
    ban_masks: _containers.RepeatedScalarFieldContainer[int]
    mod_enable: bool
    def __init__(
        self,
        gamerules_masks: _Iterable[int] | None = ...,
        ban_masks: _Iterable[int] | None = ...,
        mod_enable: bool = ...,
    ) -> None: ...

class CUserMessageRequestState(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CUserMessageRumble(_message.Message):
    __slots__ = ("index", "data", "flags")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    index: int
    data: int
    flags: int
    def __init__(
        self, index: int | None = ..., data: int | None = ..., flags: int | None = ...
    ) -> None: ...

class CUserMessageSayTextChannel(_message.Message):
    __slots__ = ("player", "channel", "text")
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    player: int
    channel: int
    text: str
    def __init__(
        self, player: int | None = ..., channel: int | None = ..., text: str | None = ...
    ) -> None: ...

class CUserMessageColoredText(_message.Message):
    __slots__ = (
        "color",
        "text",
        "reset",
        "context_player_slot",
        "context_value",
        "context_team_id",
    )
    COLOR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    RESET_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_VALUE_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    color: int
    text: str
    reset: bool
    context_player_slot: int
    context_value: int
    context_team_id: int
    def __init__(
        self,
        color: int | None = ...,
        text: str | None = ...,
        reset: bool = ...,
        context_player_slot: int | None = ...,
        context_value: int | None = ...,
        context_team_id: int | None = ...,
    ) -> None: ...

class CUserMessageItemPickup(_message.Message):
    __slots__ = ("itemname",)
    ITEMNAME_FIELD_NUMBER: _ClassVar[int]
    itemname: str
    def __init__(self, itemname: str | None = ...) -> None: ...

class CUserMessageAmmoDenied(_message.Message):
    __slots__ = ("ammo_id",)
    AMMO_ID_FIELD_NUMBER: _ClassVar[int]
    ammo_id: int
    def __init__(self, ammo_id: int | None = ...) -> None: ...

class CUserMessageShowMenu(_message.Message):
    __slots__ = ("validslots", "displaytime", "needmore", "menustring")
    VALIDSLOTS_FIELD_NUMBER: _ClassVar[int]
    DISPLAYTIME_FIELD_NUMBER: _ClassVar[int]
    NEEDMORE_FIELD_NUMBER: _ClassVar[int]
    MENUSTRING_FIELD_NUMBER: _ClassVar[int]
    validslots: int
    displaytime: int
    needmore: bool
    menustring: str
    def __init__(
        self,
        validslots: int | None = ...,
        displaytime: int | None = ...,
        needmore: bool = ...,
        menustring: str | None = ...,
    ) -> None: ...

class CUserMessageCreditsMsg(_message.Message):
    __slots__ = ("rolltype", "logo_length")
    ROLLTYPE_FIELD_NUMBER: _ClassVar[int]
    LOGO_LENGTH_FIELD_NUMBER: _ClassVar[int]
    rolltype: eRollType
    logo_length: float
    def __init__(
        self, rolltype: eRollType | str | None = ..., logo_length: float | None = ...
    ) -> None: ...

class CEntityMessagePlayJingle(_message.Message):
    __slots__ = ("entity_msg",)
    ENTITY_MSG_FIELD_NUMBER: _ClassVar[int]
    entity_msg: _networkbasetypes_pb2.CEntityMsg
    def __init__(
        self, entity_msg: _networkbasetypes_pb2.CEntityMsg | _Mapping | None = ...
    ) -> None: ...

class CEntityMessageScreenOverlay(_message.Message):
    __slots__ = ("start_effect", "entity_msg")
    START_EFFECT_FIELD_NUMBER: _ClassVar[int]
    ENTITY_MSG_FIELD_NUMBER: _ClassVar[int]
    start_effect: bool
    entity_msg: _networkbasetypes_pb2.CEntityMsg
    def __init__(
        self,
        start_effect: bool = ...,
        entity_msg: _networkbasetypes_pb2.CEntityMsg | _Mapping | None = ...,
    ) -> None: ...

class CEntityMessageRemoveAllDecals(_message.Message):
    __slots__ = ("remove_decals", "entity_msg")
    REMOVE_DECALS_FIELD_NUMBER: _ClassVar[int]
    ENTITY_MSG_FIELD_NUMBER: _ClassVar[int]
    remove_decals: bool
    entity_msg: _networkbasetypes_pb2.CEntityMsg
    def __init__(
        self,
        remove_decals: bool = ...,
        entity_msg: _networkbasetypes_pb2.CEntityMsg | _Mapping | None = ...,
    ) -> None: ...

class CEntityMessagePropagateForce(_message.Message):
    __slots__ = ("impulse", "entity_msg")
    IMPULSE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_MSG_FIELD_NUMBER: _ClassVar[int]
    impulse: _networkbasetypes_pb2.CMsgVector
    entity_msg: _networkbasetypes_pb2.CEntityMsg
    def __init__(
        self,
        impulse: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        entity_msg: _networkbasetypes_pb2.CEntityMsg | _Mapping | None = ...,
    ) -> None: ...

class CEntityMessageDoSpark(_message.Message):
    __slots__ = (
        "origin",
        "entityindex",
        "radius",
        "color",
        "beams",
        "thick",
        "duration",
        "entity_msg",
    )
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ENTITYINDEX_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    BEAMS_FIELD_NUMBER: _ClassVar[int]
    THICK_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    ENTITY_MSG_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    entityindex: int
    radius: float
    color: int
    beams: int
    thick: float
    duration: float
    entity_msg: _networkbasetypes_pb2.CEntityMsg
    def __init__(
        self,
        origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        entityindex: int | None = ...,
        radius: float | None = ...,
        color: int | None = ...,
        beams: int | None = ...,
        thick: float | None = ...,
        duration: float | None = ...,
        entity_msg: _networkbasetypes_pb2.CEntityMsg | _Mapping | None = ...,
    ) -> None: ...

class CEntityMessageFixAngle(_message.Message):
    __slots__ = ("relative", "angle", "entity_msg")
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_MSG_FIELD_NUMBER: _ClassVar[int]
    relative: bool
    angle: _networkbasetypes_pb2.CMsgQAngle
    entity_msg: _networkbasetypes_pb2.CEntityMsg
    def __init__(
        self,
        relative: bool = ...,
        angle: _networkbasetypes_pb2.CMsgQAngle | _Mapping | None = ...,
        entity_msg: _networkbasetypes_pb2.CEntityMsg | _Mapping | None = ...,
    ) -> None: ...

class CUserMessageCameraTransition(_message.Message):
    __slots__ = ("camera_type", "duration", "params_data_driven")
    class Transition_DataDriven(_message.Message):
        __slots__ = ("filename", "attach_ent_index", "duration")
        FILENAME_FIELD_NUMBER: _ClassVar[int]
        ATTACH_ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        filename: str
        attach_ent_index: int
        duration: float
        def __init__(
            self,
            filename: str | None = ...,
            attach_ent_index: int | None = ...,
            duration: float | None = ...,
        ) -> None: ...

    CAMERA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_DATA_DRIVEN_FIELD_NUMBER: _ClassVar[int]
    camera_type: int
    duration: float
    params_data_driven: CUserMessageCameraTransition.Transition_DataDriven
    def __init__(
        self,
        camera_type: int | None = ...,
        duration: float | None = ...,
        params_data_driven: CUserMessageCameraTransition.Transition_DataDriven
        | _Mapping
        | None = ...,
    ) -> None: ...

class CUserMsg_ParticleManager(_message.Message):
    __slots__ = (
        "type",
        "index",
        "release_particle_index",
        "create_particle",
        "destroy_particle",
        "destroy_particle_involving",
        "update_particle",
        "update_particle_fwd",
        "update_particle_orient",
        "update_particle_fallback",
        "update_particle_offset",
        "update_particle_ent",
        "update_particle_should_draw",
        "update_particle_set_frozen",
        "change_control_point_attachment",
        "update_entity_position",
        "set_particle_fow_properties",
        "set_particle_text",
        "set_particle_should_check_fow",
        "set_control_point_model",
        "set_control_point_snapshot",
        "set_texture_attribute",
        "set_scene_object_generic_flag",
        "set_scene_object_tint_and_desat",
        "destroy_particle_named",
        "particle_skip_to_time",
        "particle_can_freeze",
        "set_named_value_context",
        "update_particle_transform",
        "particle_freeze_transition_override",
        "freeze_particle_involving",
        "add_modellist_override_element",
        "clear_modellist_override",
        "create_physics_sim",
        "destroy_physics_sim",
        "set_vdata",
        "set_material_override",
        "add_fan",
        "update_fan",
        "set_particle_cluster_growth",
        "remove_fan",
    )
    Extensions: _python_message._ExtensionDict
    class ReleaseParticleIndex(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class CreateParticle(_message.Message):
        __slots__ = (
            "particle_name_index",
            "attach_type",
            "entity_handle",
            "entity_handle_for_modifiers",
            "apply_voice_ban_rules",
            "team_behavior",
            "control_point_configuration",
            "cluster",
            "endcap_time",
            "aggregation_position",
        )
        PARTICLE_NAME_INDEX_FIELD_NUMBER: _ClassVar[int]
        ATTACH_TYPE_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FOR_MODIFIERS_FIELD_NUMBER: _ClassVar[int]
        APPLY_VOICE_BAN_RULES_FIELD_NUMBER: _ClassVar[int]
        TEAM_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
        CONTROL_POINT_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
        CLUSTER_FIELD_NUMBER: _ClassVar[int]
        ENDCAP_TIME_FIELD_NUMBER: _ClassVar[int]
        AGGREGATION_POSITION_FIELD_NUMBER: _ClassVar[int]
        particle_name_index: int
        attach_type: int
        entity_handle: int
        entity_handle_for_modifiers: int
        apply_voice_ban_rules: bool
        team_behavior: int
        control_point_configuration: str
        cluster: bool
        endcap_time: float
        aggregation_position: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            particle_name_index: int | None = ...,
            attach_type: int | None = ...,
            entity_handle: int | None = ...,
            entity_handle_for_modifiers: int | None = ...,
            apply_voice_ban_rules: bool = ...,
            team_behavior: int | None = ...,
            control_point_configuration: str | None = ...,
            cluster: bool = ...,
            endcap_time: float | None = ...,
            aggregation_position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    class DestroyParticle(_message.Message):
        __slots__ = ("destroy_immediately",)
        DESTROY_IMMEDIATELY_FIELD_NUMBER: _ClassVar[int]
        destroy_immediately: bool
        def __init__(self, destroy_immediately: bool = ...) -> None: ...

    class DestroyParticleInvolving(_message.Message):
        __slots__ = ("destroy_immediately", "entity_handle")
        DESTROY_IMMEDIATELY_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        destroy_immediately: bool
        entity_handle: int
        def __init__(
            self, destroy_immediately: bool = ..., entity_handle: int | None = ...
        ) -> None: ...

    class DestroyParticleNamed(_message.Message):
        __slots__ = ("particle_name_index", "entity_handle", "destroy_immediately", "play_endcap")
        PARTICLE_NAME_INDEX_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        DESTROY_IMMEDIATELY_FIELD_NUMBER: _ClassVar[int]
        PLAY_ENDCAP_FIELD_NUMBER: _ClassVar[int]
        particle_name_index: int
        entity_handle: int
        destroy_immediately: bool
        play_endcap: bool
        def __init__(
            self,
            particle_name_index: int | None = ...,
            entity_handle: int | None = ...,
            destroy_immediately: bool = ...,
            play_endcap: bool = ...,
        ) -> None: ...

    class UpdateParticle_OBSOLETE(_message.Message):
        __slots__ = ("control_point", "position")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        position: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            control_point: int | None = ...,
            position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    class UpdateParticleFwd_OBSOLETE(_message.Message):
        __slots__ = ("control_point", "forward")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        FORWARD_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        forward: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            control_point: int | None = ...,
            forward: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    class UpdateParticleOrient_OBSOLETE(_message.Message):
        __slots__ = ("control_point", "forward", "deprecated_right", "up", "left")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        FORWARD_FIELD_NUMBER: _ClassVar[int]
        DEPRECATED_RIGHT_FIELD_NUMBER: _ClassVar[int]
        UP_FIELD_NUMBER: _ClassVar[int]
        LEFT_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        forward: _networkbasetypes_pb2.CMsgVector
        deprecated_right: _networkbasetypes_pb2.CMsgVector
        up: _networkbasetypes_pb2.CMsgVector
        left: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            control_point: int | None = ...,
            forward: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            deprecated_right: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            up: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            left: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    class UpdateParticleTransform(_message.Message):
        __slots__ = ("control_point", "position", "orientation", "interpolation_interval")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        ORIENTATION_FIELD_NUMBER: _ClassVar[int]
        INTERPOLATION_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        position: _networkbasetypes_pb2.CMsgVector
        orientation: _networkbasetypes_pb2.CMsgQuaternion
        interpolation_interval: float
        def __init__(
            self,
            control_point: int | None = ...,
            position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            orientation: _networkbasetypes_pb2.CMsgQuaternion | _Mapping | None = ...,
            interpolation_interval: float | None = ...,
        ) -> None: ...

    class UpdateParticleFallback(_message.Message):
        __slots__ = ("control_point", "position")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        position: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            control_point: int | None = ...,
            position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    class UpdateParticleOffset(_message.Message):
        __slots__ = ("control_point", "origin_offset", "angle_offset")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_OFFSET_FIELD_NUMBER: _ClassVar[int]
        ANGLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        origin_offset: _networkbasetypes_pb2.CMsgVector
        angle_offset: _networkbasetypes_pb2.CMsgQAngle
        def __init__(
            self,
            control_point: int | None = ...,
            origin_offset: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            angle_offset: _networkbasetypes_pb2.CMsgQAngle | _Mapping | None = ...,
        ) -> None: ...

    class UpdateParticleEnt(_message.Message):
        __slots__ = (
            "control_point",
            "entity_handle",
            "attach_type",
            "attachment",
            "fallback_position",
            "include_wearables",
            "offset_position",
            "offset_angles",
        )
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ATTACH_TYPE_FIELD_NUMBER: _ClassVar[int]
        ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
        FALLBACK_POSITION_FIELD_NUMBER: _ClassVar[int]
        INCLUDE_WEARABLES_FIELD_NUMBER: _ClassVar[int]
        OFFSET_POSITION_FIELD_NUMBER: _ClassVar[int]
        OFFSET_ANGLES_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        entity_handle: int
        attach_type: int
        attachment: int
        fallback_position: _networkbasetypes_pb2.CMsgVector
        include_wearables: bool
        offset_position: _networkbasetypes_pb2.CMsgVector
        offset_angles: _networkbasetypes_pb2.CMsgQAngle
        def __init__(
            self,
            control_point: int | None = ...,
            entity_handle: int | None = ...,
            attach_type: int | None = ...,
            attachment: int | None = ...,
            fallback_position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            include_wearables: bool = ...,
            offset_position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            offset_angles: _networkbasetypes_pb2.CMsgQAngle | _Mapping | None = ...,
        ) -> None: ...

    class UpdateParticleSetFrozen(_message.Message):
        __slots__ = ("set_frozen", "transition_duration")
        SET_FROZEN_FIELD_NUMBER: _ClassVar[int]
        TRANSITION_DURATION_FIELD_NUMBER: _ClassVar[int]
        set_frozen: bool
        transition_duration: float
        def __init__(
            self, set_frozen: bool = ..., transition_duration: float | None = ...
        ) -> None: ...

    class UpdateParticleShouldDraw(_message.Message):
        __slots__ = ("should_draw",)
        SHOULD_DRAW_FIELD_NUMBER: _ClassVar[int]
        should_draw: bool
        def __init__(self, should_draw: bool = ...) -> None: ...

    class ChangeControlPointAttachment(_message.Message):
        __slots__ = ("attachment_old", "attachment_new", "entity_handle")
        ATTACHMENT_OLD_FIELD_NUMBER: _ClassVar[int]
        ATTACHMENT_NEW_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        attachment_old: int
        attachment_new: int
        entity_handle: int
        def __init__(
            self,
            attachment_old: int | None = ...,
            attachment_new: int | None = ...,
            entity_handle: int | None = ...,
        ) -> None: ...

    class UpdateEntityPosition(_message.Message):
        __slots__ = ("entity_handle", "position")
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        entity_handle: int
        position: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            entity_handle: int | None = ...,
            position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    class SetParticleFoWProperties(_message.Message):
        __slots__ = ("fow_control_point", "fow_control_point2", "fow_radius")
        FOW_CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        FOW_CONTROL_POINT2_FIELD_NUMBER: _ClassVar[int]
        FOW_RADIUS_FIELD_NUMBER: _ClassVar[int]
        fow_control_point: int
        fow_control_point2: int
        fow_radius: float
        def __init__(
            self,
            fow_control_point: int | None = ...,
            fow_control_point2: int | None = ...,
            fow_radius: float | None = ...,
        ) -> None: ...

    class SetParticleShouldCheckFoW(_message.Message):
        __slots__ = ("check_fow",)
        CHECK_FOW_FIELD_NUMBER: _ClassVar[int]
        check_fow: bool
        def __init__(self, check_fow: bool = ...) -> None: ...

    class SetControlPointModel(_message.Message):
        __slots__ = ("control_point", "model_name")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        model_name: str
        def __init__(
            self, control_point: int | None = ..., model_name: str | None = ...
        ) -> None: ...

    class SetControlPointSnapshot(_message.Message):
        __slots__ = ("control_point", "snapshot_name")
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        SNAPSHOT_NAME_FIELD_NUMBER: _ClassVar[int]
        control_point: int
        snapshot_name: str
        def __init__(
            self, control_point: int | None = ..., snapshot_name: str | None = ...
        ) -> None: ...

    class SetParticleText(_message.Message):
        __slots__ = ("text",)
        TEXT_FIELD_NUMBER: _ClassVar[int]
        text: str
        def __init__(self, text: str | None = ...) -> None: ...

    class SetTextureAttribute(_message.Message):
        __slots__ = ("attribute_name", "texture_name")
        ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
        TEXTURE_NAME_FIELD_NUMBER: _ClassVar[int]
        attribute_name: str
        texture_name: str
        def __init__(
            self, attribute_name: str | None = ..., texture_name: str | None = ...
        ) -> None: ...

    class SetSceneObjectGenericFlag(_message.Message):
        __slots__ = ("flag_value",)
        FLAG_VALUE_FIELD_NUMBER: _ClassVar[int]
        flag_value: bool
        def __init__(self, flag_value: bool = ...) -> None: ...

    class SetSceneObjectTintAndDesat(_message.Message):
        __slots__ = ("tint", "desat")
        TINT_FIELD_NUMBER: _ClassVar[int]
        DESAT_FIELD_NUMBER: _ClassVar[int]
        tint: int
        desat: float
        def __init__(self, tint: int | None = ..., desat: float | None = ...) -> None: ...

    class ParticleSkipToTime(_message.Message):
        __slots__ = ("skip_to_time",)
        SKIP_TO_TIME_FIELD_NUMBER: _ClassVar[int]
        skip_to_time: float
        def __init__(self, skip_to_time: float | None = ...) -> None: ...

    class ParticleCanFreeze(_message.Message):
        __slots__ = ("can_freeze",)
        CAN_FREEZE_FIELD_NUMBER: _ClassVar[int]
        can_freeze: bool
        def __init__(self, can_freeze: bool = ...) -> None: ...

    class ParticleFreezeTransitionOverride(_message.Message):
        __slots__ = ("freeze_transition_override",)
        FREEZE_TRANSITION_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
        freeze_transition_override: float
        def __init__(self, freeze_transition_override: float | None = ...) -> None: ...

    class FreezeParticleInvolving(_message.Message):
        __slots__ = ("set_frozen", "transition_duration", "entity_handle")
        SET_FROZEN_FIELD_NUMBER: _ClassVar[int]
        TRANSITION_DURATION_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        set_frozen: bool
        transition_duration: float
        entity_handle: int
        def __init__(
            self,
            set_frozen: bool = ...,
            transition_duration: float | None = ...,
            entity_handle: int | None = ...,
        ) -> None: ...

    class AddModellistOverrideElement(_message.Message):
        __slots__ = ("model_name", "spawn_probability", "groupid")
        MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
        SPAWN_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
        GROUPID_FIELD_NUMBER: _ClassVar[int]
        model_name: str
        spawn_probability: float
        groupid: int
        def __init__(
            self,
            model_name: str | None = ...,
            spawn_probability: float | None = ...,
            groupid: int | None = ...,
        ) -> None: ...

    class ClearModellistOverride(_message.Message):
        __slots__ = ("groupid",)
        GROUPID_FIELD_NUMBER: _ClassVar[int]
        groupid: int
        def __init__(self, groupid: int | None = ...) -> None: ...

    class SetParticleNamedValueContext(_message.Message):
        __slots__ = ("float_values", "vector_values", "transform_values", "ehandle_values")
        class FloatContextValue(_message.Message):
            __slots__ = ("value_name_hash", "value")
            VALUE_NAME_HASH_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value_name_hash: int
            value: float
            def __init__(
                self, value_name_hash: int | None = ..., value: float | None = ...
            ) -> None: ...

        class VectorContextValue(_message.Message):
            __slots__ = ("value_name_hash", "value")
            VALUE_NAME_HASH_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value_name_hash: int
            value: _networkbasetypes_pb2.CMsgVector
            def __init__(
                self,
                value_name_hash: int | None = ...,
                value: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            ) -> None: ...

        class TransformContextValue(_message.Message):
            __slots__ = ("value_name_hash", "angles", "translation")
            VALUE_NAME_HASH_FIELD_NUMBER: _ClassVar[int]
            ANGLES_FIELD_NUMBER: _ClassVar[int]
            TRANSLATION_FIELD_NUMBER: _ClassVar[int]
            value_name_hash: int
            angles: _networkbasetypes_pb2.CMsgQAngle
            translation: _networkbasetypes_pb2.CMsgVector
            def __init__(
                self,
                value_name_hash: int | None = ...,
                angles: _networkbasetypes_pb2.CMsgQAngle | _Mapping | None = ...,
                translation: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            ) -> None: ...

        class EHandleContext(_message.Message):
            __slots__ = ("value_name_hash", "ent_index")
            VALUE_NAME_HASH_FIELD_NUMBER: _ClassVar[int]
            ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
            value_name_hash: int
            ent_index: int
            def __init__(
                self, value_name_hash: int | None = ..., ent_index: int | None = ...
            ) -> None: ...

        FLOAT_VALUES_FIELD_NUMBER: _ClassVar[int]
        VECTOR_VALUES_FIELD_NUMBER: _ClassVar[int]
        TRANSFORM_VALUES_FIELD_NUMBER: _ClassVar[int]
        EHANDLE_VALUES_FIELD_NUMBER: _ClassVar[int]
        float_values: _containers.RepeatedCompositeFieldContainer[
            CUserMsg_ParticleManager.SetParticleNamedValueContext.FloatContextValue
        ]
        vector_values: _containers.RepeatedCompositeFieldContainer[
            CUserMsg_ParticleManager.SetParticleNamedValueContext.VectorContextValue
        ]
        transform_values: _containers.RepeatedCompositeFieldContainer[
            CUserMsg_ParticleManager.SetParticleNamedValueContext.TransformContextValue
        ]
        ehandle_values: _containers.RepeatedCompositeFieldContainer[
            CUserMsg_ParticleManager.SetParticleNamedValueContext.EHandleContext
        ]
        def __init__(
            self,
            float_values: _Iterable[
                CUserMsg_ParticleManager.SetParticleNamedValueContext.FloatContextValue | _Mapping
            ]
            | None = ...,
            vector_values: _Iterable[
                CUserMsg_ParticleManager.SetParticleNamedValueContext.VectorContextValue | _Mapping
            ]
            | None = ...,
            transform_values: _Iterable[
                CUserMsg_ParticleManager.SetParticleNamedValueContext.TransformContextValue
                | _Mapping
            ]
            | None = ...,
            ehandle_values: _Iterable[
                CUserMsg_ParticleManager.SetParticleNamedValueContext.EHandleContext | _Mapping
            ]
            | None = ...,
        ) -> None: ...

    class CreatePhysicsSim(_message.Message):
        __slots__ = ("prop_group_name", "use_high_quality_simulation", "max_particle_count")
        PROP_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
        USE_HIGH_QUALITY_SIMULATION_FIELD_NUMBER: _ClassVar[int]
        MAX_PARTICLE_COUNT_FIELD_NUMBER: _ClassVar[int]
        prop_group_name: str
        use_high_quality_simulation: bool
        max_particle_count: int
        def __init__(
            self,
            prop_group_name: str | None = ...,
            use_high_quality_simulation: bool = ...,
            max_particle_count: int | None = ...,
        ) -> None: ...

    class DestroyPhysicsSim(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class SetVData(_message.Message):
        __slots__ = ("vdata_name",)
        VDATA_NAME_FIELD_NUMBER: _ClassVar[int]
        vdata_name: str
        def __init__(self, vdata_name: str | None = ...) -> None: ...

    class SetMaterialOverride(_message.Message):
        __slots__ = ("material_name", "include_children")
        MATERIAL_NAME_FIELD_NUMBER: _ClassVar[int]
        INCLUDE_CHILDREN_FIELD_NUMBER: _ClassVar[int]
        material_name: str
        include_children: bool
        def __init__(
            self, material_name: str | None = ..., include_children: bool = ...
        ) -> None: ...

    class AddFan(_message.Message):
        __slots__ = (
            "active",
            "bounds_mins",
            "bounds_maxs",
            "fan_origin",
            "fan_origin_offset",
            "fan_direction",
            "force",
            "fan_force_curve",
            "falloff",
            "pull_towards_point",
            "curve_min_dist",
            "curve_max_dist",
            "fan_type",
            "cone_start_radius",
            "cone_end_radius",
            "cone_length",
            "entity_handle",
            "attachment_name",
        )
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        BOUNDS_MINS_FIELD_NUMBER: _ClassVar[int]
        BOUNDS_MAXS_FIELD_NUMBER: _ClassVar[int]
        FAN_ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FAN_ORIGIN_OFFSET_FIELD_NUMBER: _ClassVar[int]
        FAN_DIRECTION_FIELD_NUMBER: _ClassVar[int]
        FORCE_FIELD_NUMBER: _ClassVar[int]
        FAN_FORCE_CURVE_FIELD_NUMBER: _ClassVar[int]
        FALLOFF_FIELD_NUMBER: _ClassVar[int]
        PULL_TOWARDS_POINT_FIELD_NUMBER: _ClassVar[int]
        CURVE_MIN_DIST_FIELD_NUMBER: _ClassVar[int]
        CURVE_MAX_DIST_FIELD_NUMBER: _ClassVar[int]
        FAN_TYPE_FIELD_NUMBER: _ClassVar[int]
        CONE_START_RADIUS_FIELD_NUMBER: _ClassVar[int]
        CONE_END_RADIUS_FIELD_NUMBER: _ClassVar[int]
        CONE_LENGTH_FIELD_NUMBER: _ClassVar[int]
        ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ATTACHMENT_NAME_FIELD_NUMBER: _ClassVar[int]
        active: bool
        bounds_mins: _networkbasetypes_pb2.CMsgVector
        bounds_maxs: _networkbasetypes_pb2.CMsgVector
        fan_origin: _networkbasetypes_pb2.CMsgVector
        fan_origin_offset: _networkbasetypes_pb2.CMsgVector
        fan_direction: _networkbasetypes_pb2.CMsgVector
        force: float
        fan_force_curve: str
        falloff: bool
        pull_towards_point: bool
        curve_min_dist: float
        curve_max_dist: float
        fan_type: int
        cone_start_radius: float
        cone_end_radius: float
        cone_length: float
        entity_handle: int
        attachment_name: str
        def __init__(
            self,
            active: bool = ...,
            bounds_mins: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            bounds_maxs: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            fan_origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            fan_origin_offset: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            fan_direction: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            force: float | None = ...,
            fan_force_curve: str | None = ...,
            falloff: bool = ...,
            pull_towards_point: bool = ...,
            curve_min_dist: float | None = ...,
            curve_max_dist: float | None = ...,
            fan_type: int | None = ...,
            cone_start_radius: float | None = ...,
            cone_end_radius: float | None = ...,
            cone_length: float | None = ...,
            entity_handle: int | None = ...,
            attachment_name: str | None = ...,
        ) -> None: ...

    class UpdateFan(_message.Message):
        __slots__ = (
            "active",
            "fan_origin",
            "fan_origin_offset",
            "fan_direction",
            "fan_ramp_ratio",
            "bounds_mins",
            "bounds_maxs",
        )
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        FAN_ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FAN_ORIGIN_OFFSET_FIELD_NUMBER: _ClassVar[int]
        FAN_DIRECTION_FIELD_NUMBER: _ClassVar[int]
        FAN_RAMP_RATIO_FIELD_NUMBER: _ClassVar[int]
        BOUNDS_MINS_FIELD_NUMBER: _ClassVar[int]
        BOUNDS_MAXS_FIELD_NUMBER: _ClassVar[int]
        active: bool
        fan_origin: _networkbasetypes_pb2.CMsgVector
        fan_origin_offset: _networkbasetypes_pb2.CMsgVector
        fan_direction: _networkbasetypes_pb2.CMsgVector
        fan_ramp_ratio: float
        bounds_mins: _networkbasetypes_pb2.CMsgVector
        bounds_maxs: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            active: bool = ...,
            fan_origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            fan_origin_offset: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            fan_direction: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            fan_ramp_ratio: float | None = ...,
            bounds_mins: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
            bounds_maxs: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    class RemoveFan(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    class SetParticleClusterGrowth(_message.Message):
        __slots__ = ("duration", "origin")
        DURATION_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        duration: float
        origin: _networkbasetypes_pb2.CMsgVector
        def __init__(
            self,
            duration: float | None = ...,
            origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        ) -> None: ...

    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    RELEASE_PARTICLE_INDEX_FIELD_NUMBER: _ClassVar[int]
    CREATE_PARTICLE_FIELD_NUMBER: _ClassVar[int]
    DESTROY_PARTICLE_FIELD_NUMBER: _ClassVar[int]
    DESTROY_PARTICLE_INVOLVING_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_FWD_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_ORIENT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_ENT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_SHOULD_DRAW_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_SET_FROZEN_FIELD_NUMBER: _ClassVar[int]
    CHANGE_CONTROL_POINT_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_ENTITY_POSITION_FIELD_NUMBER: _ClassVar[int]
    SET_PARTICLE_FOW_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SET_PARTICLE_TEXT_FIELD_NUMBER: _ClassVar[int]
    SET_PARTICLE_SHOULD_CHECK_FOW_FIELD_NUMBER: _ClassVar[int]
    SET_CONTROL_POINT_MODEL_FIELD_NUMBER: _ClassVar[int]
    SET_CONTROL_POINT_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    SET_TEXTURE_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    SET_SCENE_OBJECT_GENERIC_FLAG_FIELD_NUMBER: _ClassVar[int]
    SET_SCENE_OBJECT_TINT_AND_DESAT_FIELD_NUMBER: _ClassVar[int]
    DESTROY_PARTICLE_NAMED_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_SKIP_TO_TIME_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_CAN_FREEZE_FIELD_NUMBER: _ClassVar[int]
    SET_NAMED_VALUE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PARTICLE_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_FREEZE_TRANSITION_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    FREEZE_PARTICLE_INVOLVING_FIELD_NUMBER: _ClassVar[int]
    ADD_MODELLIST_OVERRIDE_ELEMENT_FIELD_NUMBER: _ClassVar[int]
    CLEAR_MODELLIST_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    CREATE_PHYSICS_SIM_FIELD_NUMBER: _ClassVar[int]
    DESTROY_PHYSICS_SIM_FIELD_NUMBER: _ClassVar[int]
    SET_VDATA_FIELD_NUMBER: _ClassVar[int]
    SET_MATERIAL_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ADD_FAN_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FAN_FIELD_NUMBER: _ClassVar[int]
    SET_PARTICLE_CLUSTER_GROWTH_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FAN_FIELD_NUMBER: _ClassVar[int]
    type: PARTICLE_MESSAGE
    index: int
    release_particle_index: CUserMsg_ParticleManager.ReleaseParticleIndex
    create_particle: CUserMsg_ParticleManager.CreateParticle
    destroy_particle: CUserMsg_ParticleManager.DestroyParticle
    destroy_particle_involving: CUserMsg_ParticleManager.DestroyParticleInvolving
    update_particle: CUserMsg_ParticleManager.UpdateParticle_OBSOLETE
    update_particle_fwd: CUserMsg_ParticleManager.UpdateParticleFwd_OBSOLETE
    update_particle_orient: CUserMsg_ParticleManager.UpdateParticleOrient_OBSOLETE
    update_particle_fallback: CUserMsg_ParticleManager.UpdateParticleFallback
    update_particle_offset: CUserMsg_ParticleManager.UpdateParticleOffset
    update_particle_ent: CUserMsg_ParticleManager.UpdateParticleEnt
    update_particle_should_draw: CUserMsg_ParticleManager.UpdateParticleShouldDraw
    update_particle_set_frozen: CUserMsg_ParticleManager.UpdateParticleSetFrozen
    change_control_point_attachment: CUserMsg_ParticleManager.ChangeControlPointAttachment
    update_entity_position: CUserMsg_ParticleManager.UpdateEntityPosition
    set_particle_fow_properties: CUserMsg_ParticleManager.SetParticleFoWProperties
    set_particle_text: CUserMsg_ParticleManager.SetParticleText
    set_particle_should_check_fow: CUserMsg_ParticleManager.SetParticleShouldCheckFoW
    set_control_point_model: CUserMsg_ParticleManager.SetControlPointModel
    set_control_point_snapshot: CUserMsg_ParticleManager.SetControlPointSnapshot
    set_texture_attribute: CUserMsg_ParticleManager.SetTextureAttribute
    set_scene_object_generic_flag: CUserMsg_ParticleManager.SetSceneObjectGenericFlag
    set_scene_object_tint_and_desat: CUserMsg_ParticleManager.SetSceneObjectTintAndDesat
    destroy_particle_named: CUserMsg_ParticleManager.DestroyParticleNamed
    particle_skip_to_time: CUserMsg_ParticleManager.ParticleSkipToTime
    particle_can_freeze: CUserMsg_ParticleManager.ParticleCanFreeze
    set_named_value_context: CUserMsg_ParticleManager.SetParticleNamedValueContext
    update_particle_transform: CUserMsg_ParticleManager.UpdateParticleTransform
    particle_freeze_transition_override: CUserMsg_ParticleManager.ParticleFreezeTransitionOverride
    freeze_particle_involving: CUserMsg_ParticleManager.FreezeParticleInvolving
    add_modellist_override_element: CUserMsg_ParticleManager.AddModellistOverrideElement
    clear_modellist_override: CUserMsg_ParticleManager.ClearModellistOverride
    create_physics_sim: CUserMsg_ParticleManager.CreatePhysicsSim
    destroy_physics_sim: CUserMsg_ParticleManager.DestroyPhysicsSim
    set_vdata: CUserMsg_ParticleManager.SetVData
    set_material_override: CUserMsg_ParticleManager.SetMaterialOverride
    add_fan: CUserMsg_ParticleManager.AddFan
    update_fan: CUserMsg_ParticleManager.UpdateFan
    set_particle_cluster_growth: CUserMsg_ParticleManager.SetParticleClusterGrowth
    remove_fan: CUserMsg_ParticleManager.RemoveFan
    def __init__(
        self,
        type: PARTICLE_MESSAGE | str | None = ...,
        index: int | None = ...,
        release_particle_index: CUserMsg_ParticleManager.ReleaseParticleIndex
        | _Mapping
        | None = ...,
        create_particle: CUserMsg_ParticleManager.CreateParticle | _Mapping | None = ...,
        destroy_particle: CUserMsg_ParticleManager.DestroyParticle | _Mapping | None = ...,
        destroy_particle_involving: CUserMsg_ParticleManager.DestroyParticleInvolving
        | _Mapping
        | None = ...,
        update_particle: CUserMsg_ParticleManager.UpdateParticle_OBSOLETE | _Mapping | None = ...,
        update_particle_fwd: CUserMsg_ParticleManager.UpdateParticleFwd_OBSOLETE
        | _Mapping
        | None = ...,
        update_particle_orient: CUserMsg_ParticleManager.UpdateParticleOrient_OBSOLETE
        | _Mapping
        | None = ...,
        update_particle_fallback: CUserMsg_ParticleManager.UpdateParticleFallback
        | _Mapping
        | None = ...,
        update_particle_offset: CUserMsg_ParticleManager.UpdateParticleOffset
        | _Mapping
        | None = ...,
        update_particle_ent: CUserMsg_ParticleManager.UpdateParticleEnt | _Mapping | None = ...,
        update_particle_should_draw: CUserMsg_ParticleManager.UpdateParticleShouldDraw
        | _Mapping
        | None = ...,
        update_particle_set_frozen: CUserMsg_ParticleManager.UpdateParticleSetFrozen
        | _Mapping
        | None = ...,
        change_control_point_attachment: CUserMsg_ParticleManager.ChangeControlPointAttachment
        | _Mapping
        | None = ...,
        update_entity_position: CUserMsg_ParticleManager.UpdateEntityPosition
        | _Mapping
        | None = ...,
        set_particle_fow_properties: CUserMsg_ParticleManager.SetParticleFoWProperties
        | _Mapping
        | None = ...,
        set_particle_text: CUserMsg_ParticleManager.SetParticleText | _Mapping | None = ...,
        set_particle_should_check_fow: CUserMsg_ParticleManager.SetParticleShouldCheckFoW
        | _Mapping
        | None = ...,
        set_control_point_model: CUserMsg_ParticleManager.SetControlPointModel
        | _Mapping
        | None = ...,
        set_control_point_snapshot: CUserMsg_ParticleManager.SetControlPointSnapshot
        | _Mapping
        | None = ...,
        set_texture_attribute: CUserMsg_ParticleManager.SetTextureAttribute | _Mapping | None = ...,
        set_scene_object_generic_flag: CUserMsg_ParticleManager.SetSceneObjectGenericFlag
        | _Mapping
        | None = ...,
        set_scene_object_tint_and_desat: CUserMsg_ParticleManager.SetSceneObjectTintAndDesat
        | _Mapping
        | None = ...,
        destroy_particle_named: CUserMsg_ParticleManager.DestroyParticleNamed
        | _Mapping
        | None = ...,
        particle_skip_to_time: CUserMsg_ParticleManager.ParticleSkipToTime | _Mapping | None = ...,
        particle_can_freeze: CUserMsg_ParticleManager.ParticleCanFreeze | _Mapping | None = ...,
        set_named_value_context: CUserMsg_ParticleManager.SetParticleNamedValueContext
        | _Mapping
        | None = ...,
        update_particle_transform: CUserMsg_ParticleManager.UpdateParticleTransform
        | _Mapping
        | None = ...,
        particle_freeze_transition_override: CUserMsg_ParticleManager.ParticleFreezeTransitionOverride
        | _Mapping
        | None = ...,
        freeze_particle_involving: CUserMsg_ParticleManager.FreezeParticleInvolving
        | _Mapping
        | None = ...,
        add_modellist_override_element: CUserMsg_ParticleManager.AddModellistOverrideElement
        | _Mapping
        | None = ...,
        clear_modellist_override: CUserMsg_ParticleManager.ClearModellistOverride
        | _Mapping
        | None = ...,
        create_physics_sim: CUserMsg_ParticleManager.CreatePhysicsSim | _Mapping | None = ...,
        destroy_physics_sim: CUserMsg_ParticleManager.DestroyPhysicsSim | _Mapping | None = ...,
        set_vdata: CUserMsg_ParticleManager.SetVData | _Mapping | None = ...,
        set_material_override: CUserMsg_ParticleManager.SetMaterialOverride | _Mapping | None = ...,
        add_fan: CUserMsg_ParticleManager.AddFan | _Mapping | None = ...,
        update_fan: CUserMsg_ParticleManager.UpdateFan | _Mapping | None = ...,
        set_particle_cluster_growth: CUserMsg_ParticleManager.SetParticleClusterGrowth
        | _Mapping
        | None = ...,
        remove_fan: CUserMsg_ParticleManager.RemoveFan | _Mapping | None = ...,
    ) -> None: ...

class CUserMsg_HudError(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    def __init__(self, order_id: int | None = ...) -> None: ...

class CUserMsg_CustomGameEvent(_message.Message):
    __slots__ = ("event_name", "data")
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    data: bytes
    def __init__(self, event_name: str | None = ..., data: bytes | None = ...) -> None: ...

class CUserMessageHapticsManagerPulse(_message.Message):
    __slots__ = ("hand_id", "effect_amplitude", "effect_frequency", "effect_duration")
    HAND_ID_FIELD_NUMBER: _ClassVar[int]
    EFFECT_AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    EFFECT_DURATION_FIELD_NUMBER: _ClassVar[int]
    hand_id: int
    effect_amplitude: float
    effect_frequency: float
    effect_duration: float
    def __init__(
        self,
        hand_id: int | None = ...,
        effect_amplitude: float | None = ...,
        effect_frequency: float | None = ...,
        effect_duration: float | None = ...,
    ) -> None: ...

class CUserMessageHapticsManagerEffect(_message.Message):
    __slots__ = ("hand_id", "effect_name_hash_code", "effect_scale")
    HAND_ID_FIELD_NUMBER: _ClassVar[int]
    EFFECT_NAME_HASH_CODE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_SCALE_FIELD_NUMBER: _ClassVar[int]
    hand_id: int
    effect_name_hash_code: int
    effect_scale: float
    def __init__(
        self,
        hand_id: int | None = ...,
        effect_name_hash_code: int | None = ...,
        effect_scale: float | None = ...,
    ) -> None: ...

class CUserMessageAnimStateGraphState(_message.Message):
    __slots__ = ("entity_index", "data")
    ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    entity_index: int
    data: bytes
    def __init__(self, entity_index: int | None = ..., data: bytes | None = ...) -> None: ...

class CUserMessageUpdateCssClasses(_message.Message):
    __slots__ = ("target_world_panel", "css_classes", "is_add")
    TARGET_WORLD_PANEL_FIELD_NUMBER: _ClassVar[int]
    CSS_CLASSES_FIELD_NUMBER: _ClassVar[int]
    IS_ADD_FIELD_NUMBER: _ClassVar[int]
    target_world_panel: int
    css_classes: str
    is_add: bool
    def __init__(
        self,
        target_world_panel: int | None = ...,
        css_classes: str | None = ...,
        is_add: bool = ...,
    ) -> None: ...

class CUserMessageServerFrameTime(_message.Message):
    __slots__ = ("frame_time",)
    FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    frame_time: float
    def __init__(self, frame_time: float | None = ...) -> None: ...

class CUserMessageLagCompensationError(_message.Message):
    __slots__ = ("distance",)
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    distance: float
    def __init__(self, distance: float | None = ...) -> None: ...

class CUserMessageRequestDllStatus(_message.Message):
    __slots__ = ("dll_action", "full_report")
    DLL_ACTION_FIELD_NUMBER: _ClassVar[int]
    FULL_REPORT_FIELD_NUMBER: _ClassVar[int]
    dll_action: str
    full_report: bool
    def __init__(self, dll_action: str | None = ..., full_report: bool = ...) -> None: ...

class CUserMessageRequestUtilAction(_message.Message):
    __slots__ = ("util1", "util2", "util3", "util4", "util5")
    UTIL1_FIELD_NUMBER: _ClassVar[int]
    UTIL2_FIELD_NUMBER: _ClassVar[int]
    UTIL3_FIELD_NUMBER: _ClassVar[int]
    UTIL4_FIELD_NUMBER: _ClassVar[int]
    UTIL5_FIELD_NUMBER: _ClassVar[int]
    util1: int
    util2: int
    util3: int
    util4: int
    util5: int
    def __init__(
        self,
        util1: int | None = ...,
        util2: int | None = ...,
        util3: int | None = ...,
        util4: int | None = ...,
        util5: int | None = ...,
    ) -> None: ...

class CUserMessage_UtilMsg_Response(_message.Message):
    __slots__ = (
        "crc",
        "item_count",
        "crc2",
        "item_count2",
        "crc_part",
        "crc_part2",
        "client_timestamp",
        "platform",
        "itemdetails",
        "itemgroup",
        "total_count",
        "total_count2",
    )
    class ItemDetail(_message.Message):
        __slots__ = ("index", "hash", "crc", "name")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        HASH_FIELD_NUMBER: _ClassVar[int]
        CRC_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        index: int
        hash: int
        crc: int
        name: str
        def __init__(
            self,
            index: int | None = ...,
            hash: int | None = ...,
            crc: int | None = ...,
            name: str | None = ...,
        ) -> None: ...

    CRC_FIELD_NUMBER: _ClassVar[int]
    ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    CRC2_FIELD_NUMBER: _ClassVar[int]
    ITEM_COUNT2_FIELD_NUMBER: _ClassVar[int]
    CRC_PART_FIELD_NUMBER: _ClassVar[int]
    CRC_PART2_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    ITEMDETAILS_FIELD_NUMBER: _ClassVar[int]
    ITEMGROUP_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT2_FIELD_NUMBER: _ClassVar[int]
    crc: int
    item_count: int
    crc2: int
    item_count2: int
    crc_part: _containers.RepeatedScalarFieldContainer[int]
    crc_part2: _containers.RepeatedScalarFieldContainer[int]
    client_timestamp: int
    platform: int
    itemdetails: _containers.RepeatedCompositeFieldContainer[
        CUserMessage_UtilMsg_Response.ItemDetail
    ]
    itemgroup: int
    total_count: int
    total_count2: int
    def __init__(
        self,
        crc: int | None = ...,
        item_count: int | None = ...,
        crc2: int | None = ...,
        item_count2: int | None = ...,
        crc_part: _Iterable[int] | None = ...,
        crc_part2: _Iterable[int] | None = ...,
        client_timestamp: int | None = ...,
        platform: int | None = ...,
        itemdetails: _Iterable[CUserMessage_UtilMsg_Response.ItemDetail | _Mapping] | None = ...,
        itemgroup: int | None = ...,
        total_count: int | None = ...,
        total_count2: int | None = ...,
    ) -> None: ...

class CUserMessage_DllStatus(_message.Message):
    __slots__ = (
        "file_report",
        "command_line",
        "total_files",
        "process_id",
        "osversion",
        "client_time",
        "diagnostics",
        "modules",
    )
    class CVDiagnostic(_message.Message):
        __slots__ = ("id", "extended", "value", "string_value")
        ID_FIELD_NUMBER: _ClassVar[int]
        EXTENDED_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
        id: int
        extended: int
        value: int
        string_value: str
        def __init__(
            self,
            id: int | None = ...,
            extended: int | None = ...,
            value: int | None = ...,
            string_value: str | None = ...,
        ) -> None: ...

    class CModule(_message.Message):
        __slots__ = ("base_addr", "name", "size", "timestamp")
        BASE_ADDR_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        base_addr: int
        name: str
        size: int
        timestamp: int
        def __init__(
            self,
            base_addr: int | None = ...,
            name: str | None = ...,
            size: int | None = ...,
            timestamp: int | None = ...,
        ) -> None: ...

    FILE_REPORT_FIELD_NUMBER: _ClassVar[int]
    COMMAND_LINE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FILES_FIELD_NUMBER: _ClassVar[int]
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    OSVERSION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TIME_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    MODULES_FIELD_NUMBER: _ClassVar[int]
    file_report: str
    command_line: str
    total_files: int
    process_id: int
    osversion: int
    client_time: int
    diagnostics: _containers.RepeatedCompositeFieldContainer[CUserMessage_DllStatus.CVDiagnostic]
    modules: _containers.RepeatedCompositeFieldContainer[CUserMessage_DllStatus.CModule]
    def __init__(
        self,
        file_report: str | None = ...,
        command_line: str | None = ...,
        total_files: int | None = ...,
        process_id: int | None = ...,
        osversion: int | None = ...,
        client_time: int | None = ...,
        diagnostics: _Iterable[CUserMessage_DllStatus.CVDiagnostic | _Mapping] | None = ...,
        modules: _Iterable[CUserMessage_DllStatus.CModule | _Mapping] | None = ...,
    ) -> None: ...

class CUserMessageRequestInventory(_message.Message):
    __slots__ = ("inventory", "offset", "options")
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    inventory: int
    offset: int
    options: int
    def __init__(
        self, inventory: int | None = ..., offset: int | None = ..., options: int | None = ...
    ) -> None: ...

class CUserMessage_Inventory_Response(_message.Message):
    __slots__ = (
        "crc",
        "item_count",
        "osversion",
        "perf_time",
        "client_timestamp",
        "platform",
        "inventories",
        "inventories2",
        "inventories3",
        "inv_type",
        "build_version",
        "instance",
        "start_time",
    )
    class InventoryDetail(_message.Message):
        __slots__ = (
            "index",
            "primary",
            "offset",
            "first",
            "base",
            "name",
            "base_name",
            "base_detail",
            "base_time",
            "base_hash",
        )
        INDEX_FIELD_NUMBER: _ClassVar[int]
        PRIMARY_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        FIRST_FIELD_NUMBER: _ClassVar[int]
        BASE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        BASE_NAME_FIELD_NUMBER: _ClassVar[int]
        BASE_DETAIL_FIELD_NUMBER: _ClassVar[int]
        BASE_TIME_FIELD_NUMBER: _ClassVar[int]
        BASE_HASH_FIELD_NUMBER: _ClassVar[int]
        index: int
        primary: int
        offset: int
        first: int
        base: int
        name: str
        base_name: str
        base_detail: int
        base_time: int
        base_hash: int
        def __init__(
            self,
            index: int | None = ...,
            primary: int | None = ...,
            offset: int | None = ...,
            first: int | None = ...,
            base: int | None = ...,
            name: str | None = ...,
            base_name: str | None = ...,
            base_detail: int | None = ...,
            base_time: int | None = ...,
            base_hash: int | None = ...,
        ) -> None: ...

    CRC_FIELD_NUMBER: _ClassVar[int]
    ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    OSVERSION_FIELD_NUMBER: _ClassVar[int]
    PERF_TIME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    INVENTORIES_FIELD_NUMBER: _ClassVar[int]
    INVENTORIES2_FIELD_NUMBER: _ClassVar[int]
    INVENTORIES3_FIELD_NUMBER: _ClassVar[int]
    INV_TYPE_FIELD_NUMBER: _ClassVar[int]
    BUILD_VERSION_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    crc: int
    item_count: int
    osversion: int
    perf_time: int
    client_timestamp: int
    platform: int
    inventories: _containers.RepeatedCompositeFieldContainer[
        CUserMessage_Inventory_Response.InventoryDetail
    ]
    inventories2: _containers.RepeatedCompositeFieldContainer[
        CUserMessage_Inventory_Response.InventoryDetail
    ]
    inventories3: _containers.RepeatedCompositeFieldContainer[
        CUserMessage_Inventory_Response.InventoryDetail
    ]
    inv_type: int
    build_version: int
    instance: int
    start_time: int
    def __init__(
        self,
        crc: int | None = ...,
        item_count: int | None = ...,
        osversion: int | None = ...,
        perf_time: int | None = ...,
        client_timestamp: int | None = ...,
        platform: int | None = ...,
        inventories: _Iterable[CUserMessage_Inventory_Response.InventoryDetail | _Mapping]
        | None = ...,
        inventories2: _Iterable[CUserMessage_Inventory_Response.InventoryDetail | _Mapping]
        | None = ...,
        inventories3: _Iterable[CUserMessage_Inventory_Response.InventoryDetail | _Mapping]
        | None = ...,
        inv_type: int | None = ...,
        build_version: int | None = ...,
        instance: int | None = ...,
        start_time: int | None = ...,
    ) -> None: ...

class CUserMessageRequestDiagnostic(_message.Message):
    __slots__ = ("diagnostics",)
    class Diagnostic(_message.Message):
        __slots__ = (
            "index",
            "offset",
            "param",
            "length",
            "type",
            "base",
            "range",
            "extent",
            "detail",
            "name",
            "alias",
            "vardetail",
            "context",
        )
        INDEX_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        PARAM_FIELD_NUMBER: _ClassVar[int]
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        BASE_FIELD_NUMBER: _ClassVar[int]
        RANGE_FIELD_NUMBER: _ClassVar[int]
        EXTENT_FIELD_NUMBER: _ClassVar[int]
        DETAIL_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ALIAS_FIELD_NUMBER: _ClassVar[int]
        VARDETAIL_FIELD_NUMBER: _ClassVar[int]
        CONTEXT_FIELD_NUMBER: _ClassVar[int]
        index: int
        offset: int
        param: int
        length: int
        type: int
        base: int
        range: int
        extent: int
        detail: int
        name: str
        alias: str
        vardetail: bytes
        context: int
        def __init__(
            self,
            index: int | None = ...,
            offset: int | None = ...,
            param: int | None = ...,
            length: int | None = ...,
            type: int | None = ...,
            base: int | None = ...,
            range: int | None = ...,
            extent: int | None = ...,
            detail: int | None = ...,
            name: str | None = ...,
            alias: str | None = ...,
            vardetail: bytes | None = ...,
            context: int | None = ...,
        ) -> None: ...

    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    diagnostics: _containers.RepeatedCompositeFieldContainer[
        CUserMessageRequestDiagnostic.Diagnostic
    ]
    def __init__(
        self,
        diagnostics: _Iterable[CUserMessageRequestDiagnostic.Diagnostic | _Mapping] | None = ...,
    ) -> None: ...

class CUserMessage_Diagnostic_Response(_message.Message):
    __slots__ = ("diagnostics", "build_version", "instance", "start_time", "osversion", "platform")
    class Diagnostic(_message.Message):
        __slots__ = (
            "index",
            "offset",
            "param",
            "length",
            "detail",
            "base",
            "range",
            "type",
            "name",
            "alias",
            "backup",
            "context",
            "control",
            "augment",
            "placebo",
        )
        INDEX_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        PARAM_FIELD_NUMBER: _ClassVar[int]
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        DETAIL_FIELD_NUMBER: _ClassVar[int]
        BASE_FIELD_NUMBER: _ClassVar[int]
        RANGE_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ALIAS_FIELD_NUMBER: _ClassVar[int]
        BACKUP_FIELD_NUMBER: _ClassVar[int]
        CONTEXT_FIELD_NUMBER: _ClassVar[int]
        CONTROL_FIELD_NUMBER: _ClassVar[int]
        AUGMENT_FIELD_NUMBER: _ClassVar[int]
        PLACEBO_FIELD_NUMBER: _ClassVar[int]
        index: int
        offset: int
        param: int
        length: int
        detail: bytes
        base: int
        range: int
        type: int
        name: str
        alias: str
        backup: bytes
        context: int
        control: int
        augment: int
        placebo: int
        def __init__(
            self,
            index: int | None = ...,
            offset: int | None = ...,
            param: int | None = ...,
            length: int | None = ...,
            detail: bytes | None = ...,
            base: int | None = ...,
            range: int | None = ...,
            type: int | None = ...,
            name: str | None = ...,
            alias: str | None = ...,
            backup: bytes | None = ...,
            context: int | None = ...,
            control: int | None = ...,
            augment: int | None = ...,
            placebo: int | None = ...,
        ) -> None: ...

    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    BUILD_VERSION_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    OSVERSION_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    diagnostics: _containers.RepeatedCompositeFieldContainer[
        CUserMessage_Diagnostic_Response.Diagnostic
    ]
    build_version: int
    instance: int
    start_time: int
    osversion: int
    platform: int
    def __init__(
        self,
        diagnostics: _Iterable[CUserMessage_Diagnostic_Response.Diagnostic | _Mapping] | None = ...,
        build_version: int | None = ...,
        instance: int | None = ...,
        start_time: int | None = ...,
        osversion: int | None = ...,
        platform: int | None = ...,
    ) -> None: ...

class CUserMessage_ExtraUserData(_message.Message):
    __slots__ = ("item", "value1", "value2", "detail1", "detail2")
    ITEM_FIELD_NUMBER: _ClassVar[int]
    VALUE1_FIELD_NUMBER: _ClassVar[int]
    VALUE2_FIELD_NUMBER: _ClassVar[int]
    DETAIL1_FIELD_NUMBER: _ClassVar[int]
    DETAIL2_FIELD_NUMBER: _ClassVar[int]
    item: int
    value1: int
    value2: int
    detail1: _containers.RepeatedScalarFieldContainer[bytes]
    detail2: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(
        self,
        item: int | None = ...,
        value1: int | None = ...,
        value2: int | None = ...,
        detail1: _Iterable[bytes] | None = ...,
        detail2: _Iterable[bytes] | None = ...,
    ) -> None: ...

class CUserMessage_NotifyResponseFound(_message.Message):
    __slots__ = (
        "ent_index",
        "rule_name",
        "response_value",
        "response_concept",
        "criteria",
        "int_criteria_names",
        "int_criteria_values",
        "float_criteria_names",
        "float_criteria_values",
        "symbol_criteria_names",
        "symbol_criteria_values",
        "speak_result",
    )
    class Criteria(_message.Message):
        __slots__ = ("name_symbol", "value")
        NAME_SYMBOL_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name_symbol: int
        value: str
        def __init__(self, name_symbol: int | None = ..., value: str | None = ...) -> None: ...

    ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    RULE_NAME_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_VALUE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CONCEPT_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_FIELD_NUMBER: _ClassVar[int]
    INT_CRITERIA_NAMES_FIELD_NUMBER: _ClassVar[int]
    INT_CRITERIA_VALUES_FIELD_NUMBER: _ClassVar[int]
    FLOAT_CRITERIA_NAMES_FIELD_NUMBER: _ClassVar[int]
    FLOAT_CRITERIA_VALUES_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_CRITERIA_NAMES_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_CRITERIA_VALUES_FIELD_NUMBER: _ClassVar[int]
    SPEAK_RESULT_FIELD_NUMBER: _ClassVar[int]
    ent_index: int
    rule_name: str
    response_value: str
    response_concept: str
    criteria: _containers.RepeatedCompositeFieldContainer[CUserMessage_NotifyResponseFound.Criteria]
    int_criteria_names: _containers.RepeatedScalarFieldContainer[int]
    int_criteria_values: _containers.RepeatedScalarFieldContainer[int]
    float_criteria_names: _containers.RepeatedScalarFieldContainer[int]
    float_criteria_values: _containers.RepeatedScalarFieldContainer[float]
    symbol_criteria_names: _containers.RepeatedScalarFieldContainer[int]
    symbol_criteria_values: _containers.RepeatedScalarFieldContainer[int]
    speak_result: int
    def __init__(
        self,
        ent_index: int | None = ...,
        rule_name: str | None = ...,
        response_value: str | None = ...,
        response_concept: str | None = ...,
        criteria: _Iterable[CUserMessage_NotifyResponseFound.Criteria | _Mapping] | None = ...,
        int_criteria_names: _Iterable[int] | None = ...,
        int_criteria_values: _Iterable[int] | None = ...,
        float_criteria_names: _Iterable[int] | None = ...,
        float_criteria_values: _Iterable[float] | None = ...,
        symbol_criteria_names: _Iterable[int] | None = ...,
        symbol_criteria_values: _Iterable[int] | None = ...,
        speak_result: int | None = ...,
    ) -> None: ...

class CUserMessage_PlayResponseConditional(_message.Message):
    __slots__ = ("ent_index", "player_slots", "response", "ent_origin", "pre_delay", "mix_priority")
    ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOTS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ENT_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    PRE_DELAY_FIELD_NUMBER: _ClassVar[int]
    MIX_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    ent_index: int
    player_slots: _containers.RepeatedScalarFieldContainer[int]
    response: str
    ent_origin: _networkbasetypes_pb2.CMsgVector
    pre_delay: float
    mix_priority: int
    def __init__(
        self,
        ent_index: int | None = ...,
        player_slots: _Iterable[int] | None = ...,
        response: str | None = ...,
        ent_origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        pre_delay: float | None = ...,
        mix_priority: int | None = ...,
    ) -> None: ...
