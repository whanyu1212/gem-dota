from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ECraftworksAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eInvalid: _ClassVar[ECraftworksAuditAction]
    k_eRecipeCrafted: _ClassVar[ECraftworksAuditAction]
    k_eMatchRewards: _ClassVar[ECraftworksAuditAction]
    k_eMatchRewardsTurbo: _ClassVar[ECraftworksAuditAction]

k_eInvalid: ECraftworksAuditAction
k_eRecipeCrafted: ECraftworksAuditAction
k_eMatchRewards: ECraftworksAuditAction
k_eMatchRewardsTurbo: ECraftworksAuditAction

class CMsgCraftworksComponents(_message.Message):
    __slots__ = ("component_quantities",)
    class ComponentQuantitiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: int | None = ..., value: int | None = ...) -> None: ...

    COMPONENT_QUANTITIES_FIELD_NUMBER: _ClassVar[int]
    component_quantities: _containers.RepeatedCompositeFieldContainer[
        CMsgCraftworksComponents.ComponentQuantitiesEntry
    ]
    def __init__(
        self,
        component_quantities: _Iterable[
            CMsgCraftworksComponents.ComponentQuantitiesEntry | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgCraftworksQuestReward(_message.Message):
    __slots__ = ("quest_id", "reward_components", "stat_value")
    QUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    STAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    quest_id: int
    reward_components: CMsgCraftworksComponents
    stat_value: int
    def __init__(
        self,
        quest_id: int | None = ...,
        reward_components: CMsgCraftworksComponents | _Mapping | None = ...,
        stat_value: int | None = ...,
    ) -> None: ...
