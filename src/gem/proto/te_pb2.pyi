from . import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ETEProtobufIds(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TE_EffectDispatchId: _ClassVar[ETEProtobufIds]
    TE_ArmorRicochetId: _ClassVar[ETEProtobufIds]
    TE_BeamEntPointId: _ClassVar[ETEProtobufIds]
    TE_BeamEntsId: _ClassVar[ETEProtobufIds]
    TE_BeamPointsId: _ClassVar[ETEProtobufIds]
    TE_BeamRingId: _ClassVar[ETEProtobufIds]
    TE_BubblesId: _ClassVar[ETEProtobufIds]
    TE_BubbleTrailId: _ClassVar[ETEProtobufIds]
    TE_DecalId: _ClassVar[ETEProtobufIds]
    TE_WorldDecalId: _ClassVar[ETEProtobufIds]
    TE_EnergySplashId: _ClassVar[ETEProtobufIds]
    TE_FizzId: _ClassVar[ETEProtobufIds]
    TE_ShatterSurfaceId: _ClassVar[ETEProtobufIds]
    TE_GlowSpriteId: _ClassVar[ETEProtobufIds]
    TE_ImpactId: _ClassVar[ETEProtobufIds]
    TE_MuzzleFlashId: _ClassVar[ETEProtobufIds]
    TE_BloodStreamId: _ClassVar[ETEProtobufIds]
    TE_ExplosionId: _ClassVar[ETEProtobufIds]
    TE_DustId: _ClassVar[ETEProtobufIds]
    TE_LargeFunnelId: _ClassVar[ETEProtobufIds]
    TE_SparksId: _ClassVar[ETEProtobufIds]
    TE_PhysicsPropId: _ClassVar[ETEProtobufIds]
    TE_SmokeId: _ClassVar[ETEProtobufIds]
TE_EffectDispatchId: ETEProtobufIds
TE_ArmorRicochetId: ETEProtobufIds
TE_BeamEntPointId: ETEProtobufIds
TE_BeamEntsId: ETEProtobufIds
TE_BeamPointsId: ETEProtobufIds
TE_BeamRingId: ETEProtobufIds
TE_BubblesId: ETEProtobufIds
TE_BubbleTrailId: ETEProtobufIds
TE_DecalId: ETEProtobufIds
TE_WorldDecalId: ETEProtobufIds
TE_EnergySplashId: ETEProtobufIds
TE_FizzId: ETEProtobufIds
TE_ShatterSurfaceId: ETEProtobufIds
TE_GlowSpriteId: ETEProtobufIds
TE_ImpactId: ETEProtobufIds
TE_MuzzleFlashId: ETEProtobufIds
TE_BloodStreamId: ETEProtobufIds
TE_ExplosionId: ETEProtobufIds
TE_DustId: ETEProtobufIds
TE_LargeFunnelId: ETEProtobufIds
TE_SparksId: ETEProtobufIds
TE_PhysicsPropId: ETEProtobufIds
TE_SmokeId: ETEProtobufIds

class CMsgTEArmorRicochet(_message.Message):
    __slots__ = ("pos", "dir")
    POS_FIELD_NUMBER: _ClassVar[int]
    DIR_FIELD_NUMBER: _ClassVar[int]
    pos: _networkbasetypes_pb2.CMsgVector
    dir: _networkbasetypes_pb2.CMsgVector
    def __init__(self, pos: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., dir: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...

class CMsgTEBaseBeam(_message.Message):
    __slots__ = ("modelindex", "haloindex", "startframe", "framerate", "life", "width", "endwidth", "fadelength", "amplitude", "color", "speed", "flags")
    MODELINDEX_FIELD_NUMBER: _ClassVar[int]
    HALOINDEX_FIELD_NUMBER: _ClassVar[int]
    STARTFRAME_FIELD_NUMBER: _ClassVar[int]
    FRAMERATE_FIELD_NUMBER: _ClassVar[int]
    LIFE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    ENDWIDTH_FIELD_NUMBER: _ClassVar[int]
    FADELENGTH_FIELD_NUMBER: _ClassVar[int]
    AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    modelindex: int
    haloindex: int
    startframe: int
    framerate: int
    life: float
    width: float
    endwidth: float
    fadelength: int
    amplitude: float
    color: int
    speed: int
    flags: int
    def __init__(self, modelindex: _Optional[int] = ..., haloindex: _Optional[int] = ..., startframe: _Optional[int] = ..., framerate: _Optional[int] = ..., life: _Optional[float] = ..., width: _Optional[float] = ..., endwidth: _Optional[float] = ..., fadelength: _Optional[int] = ..., amplitude: _Optional[float] = ..., color: _Optional[int] = ..., speed: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...

class CMsgTEBeamEntPoint(_message.Message):
    __slots__ = ("base", "startentity", "endentity", "start", "end")
    BASE_FIELD_NUMBER: _ClassVar[int]
    STARTENTITY_FIELD_NUMBER: _ClassVar[int]
    ENDENTITY_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    base: CMsgTEBaseBeam
    startentity: int
    endentity: int
    start: _networkbasetypes_pb2.CMsgVector
    end: _networkbasetypes_pb2.CMsgVector
    def __init__(self, base: _Optional[_Union[CMsgTEBaseBeam, _Mapping]] = ..., startentity: _Optional[int] = ..., endentity: _Optional[int] = ..., start: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., end: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...

class CMsgTEBeamEnts(_message.Message):
    __slots__ = ("base", "startentity", "endentity")
    BASE_FIELD_NUMBER: _ClassVar[int]
    STARTENTITY_FIELD_NUMBER: _ClassVar[int]
    ENDENTITY_FIELD_NUMBER: _ClassVar[int]
    base: CMsgTEBaseBeam
    startentity: int
    endentity: int
    def __init__(self, base: _Optional[_Union[CMsgTEBaseBeam, _Mapping]] = ..., startentity: _Optional[int] = ..., endentity: _Optional[int] = ...) -> None: ...

class CMsgTEBeamPoints(_message.Message):
    __slots__ = ("base", "start", "end")
    BASE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    base: CMsgTEBaseBeam
    start: _networkbasetypes_pb2.CMsgVector
    end: _networkbasetypes_pb2.CMsgVector
    def __init__(self, base: _Optional[_Union[CMsgTEBaseBeam, _Mapping]] = ..., start: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., end: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...

class CMsgTEBeamRing(_message.Message):
    __slots__ = ("base", "startentity", "endentity")
    BASE_FIELD_NUMBER: _ClassVar[int]
    STARTENTITY_FIELD_NUMBER: _ClassVar[int]
    ENDENTITY_FIELD_NUMBER: _ClassVar[int]
    base: CMsgTEBaseBeam
    startentity: int
    endentity: int
    def __init__(self, base: _Optional[_Union[CMsgTEBaseBeam, _Mapping]] = ..., startentity: _Optional[int] = ..., endentity: _Optional[int] = ...) -> None: ...

class CMsgTEBubbles(_message.Message):
    __slots__ = ("mins", "maxs", "height", "count", "speed")
    MINS_FIELD_NUMBER: _ClassVar[int]
    MAXS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    mins: _networkbasetypes_pb2.CMsgVector
    maxs: _networkbasetypes_pb2.CMsgVector
    height: float
    count: int
    speed: float
    def __init__(self, mins: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., maxs: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., height: _Optional[float] = ..., count: _Optional[int] = ..., speed: _Optional[float] = ...) -> None: ...

class CMsgTEBubbleTrail(_message.Message):
    __slots__ = ("mins", "maxs", "waterz", "count", "speed")
    MINS_FIELD_NUMBER: _ClassVar[int]
    MAXS_FIELD_NUMBER: _ClassVar[int]
    WATERZ_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    mins: _networkbasetypes_pb2.CMsgVector
    maxs: _networkbasetypes_pb2.CMsgVector
    waterz: float
    count: int
    speed: float
    def __init__(self, mins: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., maxs: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., waterz: _Optional[float] = ..., count: _Optional[int] = ..., speed: _Optional[float] = ...) -> None: ...

class CMsgTEDecal(_message.Message):
    __slots__ = ("origin", "start", "entity", "hitbox", "index")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    HITBOX_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    start: _networkbasetypes_pb2.CMsgVector
    entity: int
    hitbox: int
    index: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., start: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., entity: _Optional[int] = ..., hitbox: _Optional[int] = ..., index: _Optional[int] = ...) -> None: ...

class CMsgEffectData(_message.Message):
    __slots__ = ("origin", "start", "normal", "angles", "entity", "otherentity", "scale", "magnitude", "radius", "surfaceprop", "effectindex", "damagetype", "material", "hitbox", "color", "flags", "attachmentindex", "effectname", "attachmentname")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    ANGLES_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    OTHERENTITY_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    SURFACEPROP_FIELD_NUMBER: _ClassVar[int]
    EFFECTINDEX_FIELD_NUMBER: _ClassVar[int]
    DAMAGETYPE_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    HITBOX_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTINDEX_FIELD_NUMBER: _ClassVar[int]
    EFFECTNAME_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTNAME_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    start: _networkbasetypes_pb2.CMsgVector
    normal: _networkbasetypes_pb2.CMsgVector
    angles: _networkbasetypes_pb2.CMsgQAngle
    entity: int
    otherentity: int
    scale: float
    magnitude: float
    radius: float
    surfaceprop: int
    effectindex: int
    damagetype: int
    material: int
    hitbox: int
    color: int
    flags: int
    attachmentindex: int
    effectname: int
    attachmentname: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., start: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., normal: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., angles: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ..., entity: _Optional[int] = ..., otherentity: _Optional[int] = ..., scale: _Optional[float] = ..., magnitude: _Optional[float] = ..., radius: _Optional[float] = ..., surfaceprop: _Optional[int] = ..., effectindex: _Optional[int] = ..., damagetype: _Optional[int] = ..., material: _Optional[int] = ..., hitbox: _Optional[int] = ..., color: _Optional[int] = ..., flags: _Optional[int] = ..., attachmentindex: _Optional[int] = ..., effectname: _Optional[int] = ..., attachmentname: _Optional[int] = ...) -> None: ...

class CMsgTEEffectDispatch(_message.Message):
    __slots__ = ("effectdata",)
    EFFECTDATA_FIELD_NUMBER: _ClassVar[int]
    effectdata: CMsgEffectData
    def __init__(self, effectdata: _Optional[_Union[CMsgEffectData, _Mapping]] = ...) -> None: ...

class CMsgTEEnergySplash(_message.Message):
    __slots__ = ("pos", "dir", "explosive")
    POS_FIELD_NUMBER: _ClassVar[int]
    DIR_FIELD_NUMBER: _ClassVar[int]
    EXPLOSIVE_FIELD_NUMBER: _ClassVar[int]
    pos: _networkbasetypes_pb2.CMsgVector
    dir: _networkbasetypes_pb2.CMsgVector
    explosive: bool
    def __init__(self, pos: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., dir: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., explosive: bool = ...) -> None: ...

class CMsgTEFizz(_message.Message):
    __slots__ = ("entity", "density", "current")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    DENSITY_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    entity: int
    density: int
    current: int
    def __init__(self, entity: _Optional[int] = ..., density: _Optional[int] = ..., current: _Optional[int] = ...) -> None: ...

class CMsgTEShatterSurface(_message.Message):
    __slots__ = ("origin", "angles", "force", "forcepos", "width", "height", "shardsize", "surfacetype", "frontcolor", "backcolor")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ANGLES_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCEPOS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SHARDSIZE_FIELD_NUMBER: _ClassVar[int]
    SURFACETYPE_FIELD_NUMBER: _ClassVar[int]
    FRONTCOLOR_FIELD_NUMBER: _ClassVar[int]
    BACKCOLOR_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    angles: _networkbasetypes_pb2.CMsgQAngle
    force: _networkbasetypes_pb2.CMsgVector
    forcepos: _networkbasetypes_pb2.CMsgVector
    width: float
    height: float
    shardsize: float
    surfacetype: int
    frontcolor: int
    backcolor: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., angles: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ..., force: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., forcepos: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., shardsize: _Optional[float] = ..., surfacetype: _Optional[int] = ..., frontcolor: _Optional[int] = ..., backcolor: _Optional[int] = ...) -> None: ...

class CMsgTEGlowSprite(_message.Message):
    __slots__ = ("origin", "scale", "life", "brightness")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    LIFE_FIELD_NUMBER: _ClassVar[int]
    BRIGHTNESS_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    scale: float
    life: float
    brightness: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., scale: _Optional[float] = ..., life: _Optional[float] = ..., brightness: _Optional[int] = ...) -> None: ...

class CMsgTEImpact(_message.Message):
    __slots__ = ("origin", "normal", "type")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    normal: _networkbasetypes_pb2.CMsgVector
    type: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., normal: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...

class CMsgTEMuzzleFlash(_message.Message):
    __slots__ = ("origin", "angles", "scale", "type")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ANGLES_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    angles: _networkbasetypes_pb2.CMsgQAngle
    scale: float
    type: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., angles: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ..., scale: _Optional[float] = ..., type: _Optional[int] = ...) -> None: ...

class CMsgTEBloodStream(_message.Message):
    __slots__ = ("origin", "direction", "color", "amount")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    direction: _networkbasetypes_pb2.CMsgVector
    color: int
    amount: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., direction: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., color: _Optional[int] = ..., amount: _Optional[int] = ...) -> None: ...

class CMsgTEExplosion(_message.Message):
    __slots__ = ("origin", "flags", "normal", "radius", "magnitude", "affect_ragdolls", "sound_name", "explosion_type", "explosion_type_name", "create_debris", "debris_origin", "debris_surfaceprop")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    AFFECT_RAGDOLLS_FIELD_NUMBER: _ClassVar[int]
    SOUND_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPLOSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPLOSION_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATE_DEBRIS_FIELD_NUMBER: _ClassVar[int]
    DEBRIS_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DEBRIS_SURFACEPROP_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    flags: int
    normal: _networkbasetypes_pb2.CMsgVector
    radius: int
    magnitude: int
    affect_ragdolls: bool
    sound_name: str
    explosion_type: int
    explosion_type_name: int
    create_debris: bool
    debris_origin: _networkbasetypes_pb2.CMsgVector
    debris_surfaceprop: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., flags: _Optional[int] = ..., normal: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., radius: _Optional[int] = ..., magnitude: _Optional[int] = ..., affect_ragdolls: bool = ..., sound_name: _Optional[str] = ..., explosion_type: _Optional[int] = ..., explosion_type_name: _Optional[int] = ..., create_debris: bool = ..., debris_origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., debris_surfaceprop: _Optional[int] = ...) -> None: ...

class CMsgTEDust(_message.Message):
    __slots__ = ("origin", "size", "speed", "direction")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    size: float
    speed: float
    direction: _networkbasetypes_pb2.CMsgVector
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., size: _Optional[float] = ..., speed: _Optional[float] = ..., direction: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...

class CMsgTELargeFunnel(_message.Message):
    __slots__ = ("origin", "reversed")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    REVERSED_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    reversed: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., reversed: _Optional[int] = ...) -> None: ...

class CMsgTESparks(_message.Message):
    __slots__ = ("origin", "magnitude", "length", "direction")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    magnitude: int
    length: int
    direction: _networkbasetypes_pb2.CMsgVector
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., magnitude: _Optional[int] = ..., length: _Optional[int] = ..., direction: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...

class CMsgTEPhysicsProp(_message.Message):
    __slots__ = ("origin", "velocity", "angles", "skin", "flags", "effects", "color", "modelindex", "unused_breakmodelsnottomake", "scale", "dmgpos", "dmgdir", "dmgtype")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGLES_FIELD_NUMBER: _ClassVar[int]
    SKIN_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    EFFECTS_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    MODELINDEX_FIELD_NUMBER: _ClassVar[int]
    UNUSED_BREAKMODELSNOTTOMAKE_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    DMGPOS_FIELD_NUMBER: _ClassVar[int]
    DMGDIR_FIELD_NUMBER: _ClassVar[int]
    DMGTYPE_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    velocity: _networkbasetypes_pb2.CMsgVector
    angles: _networkbasetypes_pb2.CMsgQAngle
    skin: int
    flags: int
    effects: int
    color: int
    modelindex: int
    unused_breakmodelsnottomake: int
    scale: float
    dmgpos: _networkbasetypes_pb2.CMsgVector
    dmgdir: _networkbasetypes_pb2.CMsgVector
    dmgtype: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., velocity: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., angles: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ..., skin: _Optional[int] = ..., flags: _Optional[int] = ..., effects: _Optional[int] = ..., color: _Optional[int] = ..., modelindex: _Optional[int] = ..., unused_breakmodelsnottomake: _Optional[int] = ..., scale: _Optional[float] = ..., dmgpos: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., dmgdir: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., dmgtype: _Optional[int] = ...) -> None: ...

class CMsgTESmoke(_message.Message):
    __slots__ = ("origin", "scale")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    scale: float
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., scale: _Optional[float] = ...) -> None: ...

class CMsgTEWorldDecal(_message.Message):
    __slots__ = ("origin", "normal", "index")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    normal: _networkbasetypes_pb2.CMsgVector
    index: int
    def __init__(self, origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., normal: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., index: _Optional[int] = ...) -> None: ...
