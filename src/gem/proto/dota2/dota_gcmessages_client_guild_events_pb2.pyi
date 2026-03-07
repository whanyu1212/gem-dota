from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EGuildEventAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EGuildEventAuditAction_Invalid: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_DevGrant: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_CompleteContract: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_CompleteChallenge: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_CompleteMatch_Winner: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_ChallengeProgress: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_CompleteMatch_Loser: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_WeeklyLeaderboard: _ClassVar[EGuildEventAuditAction]
    k_EGuildEventAuditAction_ManualGrant: _ClassVar[EGuildEventAuditAction]

k_EGuildEventAuditAction_Invalid: EGuildEventAuditAction
k_EGuildEventAuditAction_DevGrant: EGuildEventAuditAction
k_EGuildEventAuditAction_CompleteContract: EGuildEventAuditAction
k_EGuildEventAuditAction_CompleteChallenge: EGuildEventAuditAction
k_EGuildEventAuditAction_CompleteMatch_Winner: EGuildEventAuditAction
k_EGuildEventAuditAction_ChallengeProgress: EGuildEventAuditAction
k_EGuildEventAuditAction_CompleteMatch_Loser: EGuildEventAuditAction
k_EGuildEventAuditAction_WeeklyLeaderboard: EGuildEventAuditAction
k_EGuildEventAuditAction_ManualGrant: EGuildEventAuditAction

class CMsgGuildContract(_message.Message):
    __slots__ = (
        "contract_id",
        "challenge_instance_id",
        "challenge_parameter",
        "challenge_timestamp",
        "assigned_account_id",
        "contract_flags",
    )
    CONTRACT_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    contract_id: int
    challenge_instance_id: int
    challenge_parameter: int
    challenge_timestamp: int
    assigned_account_id: int
    contract_flags: int
    def __init__(
        self,
        contract_id: int | None = ...,
        challenge_instance_id: int | None = ...,
        challenge_parameter: int | None = ...,
        challenge_timestamp: int | None = ...,
        assigned_account_id: int | None = ...,
        contract_flags: int | None = ...,
    ) -> None: ...

class CMsgGuildContractSlot(_message.Message):
    __slots__ = ("contract",)
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    contract: CMsgGuildContract
    def __init__(self, contract: CMsgGuildContract | _Mapping | None = ...) -> None: ...

class CMsgAccountGuildEventData(_message.Message):
    __slots__ = (
        "guild_points",
        "contracts_refreshed_timestamp",
        "contract_slots",
        "completed_challenge_count",
        "challenges_refresh_timestamp",
        "guild_weekly_percentile",
        "guild_weekly_last_timestamp",
        "last_weekly_claim_time",
        "guild_current_percentile",
    )
    GUILD_POINTS_FIELD_NUMBER: _ClassVar[int]
    CONTRACTS_REFRESHED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_SLOTS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_CHALLENGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    CHALLENGES_REFRESH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    GUILD_WEEKLY_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    GUILD_WEEKLY_LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_WEEKLY_CLAIM_TIME_FIELD_NUMBER: _ClassVar[int]
    GUILD_CURRENT_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    guild_points: int
    contracts_refreshed_timestamp: int
    contract_slots: _containers.RepeatedCompositeFieldContainer[CMsgGuildContractSlot]
    completed_challenge_count: int
    challenges_refresh_timestamp: int
    guild_weekly_percentile: int
    guild_weekly_last_timestamp: int
    last_weekly_claim_time: int
    guild_current_percentile: int
    def __init__(
        self,
        guild_points: int | None = ...,
        contracts_refreshed_timestamp: int | None = ...,
        contract_slots: _Iterable[CMsgGuildContractSlot | _Mapping] | None = ...,
        completed_challenge_count: int | None = ...,
        challenges_refresh_timestamp: int | None = ...,
        guild_weekly_percentile: int | None = ...,
        guild_weekly_last_timestamp: int | None = ...,
        last_weekly_claim_time: int | None = ...,
        guild_current_percentile: int | None = ...,
    ) -> None: ...

class CMsgGuildActiveContracts(_message.Message):
    __slots__ = ("contracts_refreshed_timestamp", "contracts")
    CONTRACTS_REFRESHED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    contracts_refreshed_timestamp: int
    contracts: _containers.RepeatedCompositeFieldContainer[CMsgGuildContract]
    def __init__(
        self,
        contracts_refreshed_timestamp: int | None = ...,
        contracts: _Iterable[CMsgGuildContract | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGuildChallenge(_message.Message):
    __slots__ = (
        "challenge_instance_id",
        "challenge_parameter",
        "challenge_timestamp",
        "challenge_progress",
        "challenge_flags",
    )
    CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    challenge_instance_id: int
    challenge_parameter: int
    challenge_timestamp: int
    challenge_progress: int
    challenge_flags: int
    def __init__(
        self,
        challenge_instance_id: int | None = ...,
        challenge_parameter: int | None = ...,
        challenge_timestamp: int | None = ...,
        challenge_progress: int | None = ...,
        challenge_flags: int | None = ...,
    ) -> None: ...

class CMsgGuildEventMember(_message.Message):
    __slots__ = ("account_id", "guild_points_earned")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_POINTS_EARNED_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    guild_points_earned: int
    def __init__(
        self, account_id: int | None = ..., guild_points_earned: int | None = ...
    ) -> None: ...

class CMsgClientToGCRequestAccountGuildEventData(_message.Message):
    __slots__ = ("guild_id", "event_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self, guild_id: int | None = ..., event_id: _dota_shared_enums_pb2.EEvent | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestAccountGuildEventDataResponse(_message.Message):
    __slots__ = ("result", "event_id", "event_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse]
        k_eInvalidGuildEvent: _ClassVar[
            CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eNotMember: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    k_eInvalidGuildEvent: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_DATA_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse
    event_id: _dota_shared_enums_pb2.EEvent
    event_data: CMsgAccountGuildEventData
    def __init__(
        self,
        result: CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse | str | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        event_data: CMsgAccountGuildEventData | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientAccountGuildEventDataUpdated(_message.Message):
    __slots__ = ("guild_id", "event_id", "update_flags", "guild_event_data", "contracts_updated")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    GUILD_EVENT_DATA_FIELD_NUMBER: _ClassVar[int]
    CONTRACTS_UPDATED_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    update_flags: int
    guild_event_data: CMsgAccountGuildEventData
    contracts_updated: bool
    def __init__(
        self,
        guild_id: int | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        update_flags: int | None = ...,
        guild_event_data: CMsgAccountGuildEventData | _Mapping | None = ...,
        contracts_updated: bool = ...,
    ) -> None: ...

class CMsgClientToGCRequestActiveGuildContracts(_message.Message):
    __slots__ = ("guild_id", "event_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self, guild_id: int | None = ..., event_id: _dota_shared_enums_pb2.EEvent | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestActiveGuildContractsResponse(_message.Message):
    __slots__ = ("result", "active_contracts", "active_challenges")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]
        k_eInvalidGuildEvent: _ClassVar[CMsgClientToGCRequestActiveGuildContractsResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eNotMember: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    k_eInvalidGuildEvent: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CHALLENGES_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse
    active_contracts: CMsgGuildActiveContracts
    active_challenges: CMsgGuildChallenge
    def __init__(
        self,
        result: CMsgClientToGCRequestActiveGuildContractsResponse.EResponse | str | None = ...,
        active_contracts: CMsgGuildActiveContracts | _Mapping | None = ...,
        active_challenges: CMsgGuildChallenge | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientActiveGuildContractsUpdated(_message.Message):
    __slots__ = ("guild_id", "event_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self, guild_id: int | None = ..., event_id: _dota_shared_enums_pb2.EEvent | str | None = ...
    ) -> None: ...

class CMsgClientToGCSelectGuildContract(_message.Message):
    __slots__ = ("guild_id", "event_id", "contract_id", "contract_slot")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_SLOT_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    contract_id: int
    contract_slot: int
    def __init__(
        self,
        guild_id: int | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        contract_id: int | None = ...,
        contract_slot: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSelectGuildContractResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eInvalidGuildEvent: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eInvalidContractID: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eAlreadyAssigned: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eInvalidContractSlot: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eContractSlotLockedGuild: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eContractSlotCooldown: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eContractDuplicate: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eContractSlotTimeError: _ClassVar[CMsgClientToGCSelectGuildContractResponse.EResponse]
        k_eContractSlotLockedDotaPlus: _ClassVar[
            CMsgClientToGCSelectGuildContractResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eSuccess: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eTooBusy: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eDisabled: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eTimeout: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eNotMember: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eInvalidGuildEvent: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eInvalidContractID: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eAlreadyAssigned: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eInvalidContractSlot: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eContractSlotLockedGuild: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eContractSlotCooldown: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eContractDuplicate: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eContractSlotTimeError: CMsgClientToGCSelectGuildContractResponse.EResponse
    k_eContractSlotLockedDotaPlus: CMsgClientToGCSelectGuildContractResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSelectGuildContractResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCSelectGuildContractResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestActiveGuildChallenge(_message.Message):
    __slots__ = ("guild_id", "event_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self, guild_id: int | None = ..., event_id: _dota_shared_enums_pb2.EEvent | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestActiveGuildChallengeResponse(_message.Message):
    __slots__ = ("result", "active_challenge")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]
        k_eInvalidGuildEvent: _ClassVar[CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eNotMember: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    k_eInvalidGuildEvent: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse
    active_challenge: CMsgGuildChallenge
    def __init__(
        self,
        result: CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse | str | None = ...,
        active_challenge: CMsgGuildChallenge | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientActiveGuildChallengeUpdated(_message.Message):
    __slots__ = ("guild_id", "event_id", "active_challenge")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    active_challenge: CMsgGuildChallenge
    def __init__(
        self,
        guild_id: int | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        active_challenge: CMsgGuildChallenge | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestGuildEventMembers(_message.Message):
    __slots__ = ("guild_id", "event_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self, guild_id: int | None = ..., event_id: _dota_shared_enums_pb2.EEvent | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestGuildEventMembersResponse(_message.Message):
    __slots__ = ("result", "members")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]
        k_eInvalidGuildEvent: _ClassVar[CMsgClientToGCRequestGuildEventMembersResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eNotMember: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    k_eInvalidGuildEvent: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestGuildEventMembersResponse.EResponse
    members: _containers.RepeatedCompositeFieldContainer[CMsgGuildEventMember]
    def __init__(
        self,
        result: CMsgClientToGCRequestGuildEventMembersResponse.EResponse | str | None = ...,
        members: _Iterable[CMsgGuildEventMember | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGuildLeaderboardCombinedResponse(_message.Message):
    __slots__ = (
        "event_id",
        "region",
        "last_updated",
        "guild_id",
        "rank",
        "current_percentile",
        "weekly_percentile",
        "points",
    )
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    WEEKLY_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    region: int
    last_updated: int
    guild_id: _containers.RepeatedScalarFieldContainer[int]
    rank: _containers.RepeatedScalarFieldContainer[int]
    current_percentile: _containers.RepeatedScalarFieldContainer[int]
    weekly_percentile: _containers.RepeatedScalarFieldContainer[int]
    points: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        region: int | None = ...,
        last_updated: int | None = ...,
        guild_id: _Iterable[int] | None = ...,
        rank: _Iterable[int] | None = ...,
        current_percentile: _Iterable[int] | None = ...,
        weekly_percentile: _Iterable[int] | None = ...,
        points: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCClaimLeaderboardRewards(_message.Message):
    __slots__ = ("guild_id", "event_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self, guild_id: int | None = ..., event_id: _dota_shared_enums_pb2.EEvent | str | None = ...
    ) -> None: ...

class CMsgClientToGCClaimLeaderboardRewardsResponse(_message.Message):
    __slots__ = ("result", "event_points")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eInvalidEvent: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eInvalidGuildEvent: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eDoesNotQualify: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]
        k_eAlreadyClaimed: _ClassVar[CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse]

    k_eInternalError: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eSuccess: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eTooBusy: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eDisabled: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eTimeout: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eInvalidEvent: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eNotMember: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eInvalidGuildEvent: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eDoesNotQualify: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    k_eAlreadyClaimed: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse
    event_points: int
    def __init__(
        self,
        result: CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse | str | None = ...,
        event_points: int | None = ...,
    ) -> None: ...
