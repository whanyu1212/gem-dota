from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ETournamentTemplate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ETournamentTemplate_None: _ClassVar[ETournamentTemplate]
    k_ETournamentTemplate_AutomatedWin3: _ClassVar[ETournamentTemplate]

class ETournamentGameState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ETournamentGameState_Unknown: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_Canceled: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_Scheduled: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_Active: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_RadVictory: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_DireVictory: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_RadVictoryByForfeit: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_DireVictoryByForfeit: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_ServerFailure: _ClassVar[ETournamentGameState]
    k_ETournamentGameState_NotNeeded: _ClassVar[ETournamentGameState]

class ETournamentTeamState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ETournamentTeamState_Unknown: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Node1: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_NodeMax: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Eliminated: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Forfeited: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished1st: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished2nd: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished3rd: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished4th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished5th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished6th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished7th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished8th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished9th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished10th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished11th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished12th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished13th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished14th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished15th: _ClassVar[ETournamentTeamState]
    k_ETournamentTeamState_Finished16th: _ClassVar[ETournamentTeamState]

class ETournamentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ETournamentState_Unknown: _ClassVar[ETournamentState]
    k_ETournamentState_CanceledByAdmin: _ClassVar[ETournamentState]
    k_ETournamentState_Completed: _ClassVar[ETournamentState]
    k_ETournamentState_Merged: _ClassVar[ETournamentState]
    k_ETournamentState_ServerFailure: _ClassVar[ETournamentState]
    k_ETournamentState_TeamAbandoned: _ClassVar[ETournamentState]
    k_ETournamentState_TeamTimeoutForfeit: _ClassVar[ETournamentState]
    k_ETournamentState_TeamTimeoutRefund: _ClassVar[ETournamentState]
    k_ETournamentState_ServerFailureGrantedVictory: _ClassVar[ETournamentState]
    k_ETournamentState_TeamTimeoutGrantedVictory: _ClassVar[ETournamentState]
    k_ETournamentState_InProgress: _ClassVar[ETournamentState]
    k_ETournamentState_WaitingToMerge: _ClassVar[ETournamentState]

class ETournamentNodeState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ETournamentNodeState_Unknown: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_Canceled: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_TeamsNotYetAssigned: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_InBetweenGames: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_GameInProgress: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_A_Won: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_B_Won: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_A_WonByForfeit: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_B_WonByForfeit: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_A_Bye: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_A_Abandoned: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_ServerFailure: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_A_TimeoutForfeit: _ClassVar[ETournamentNodeState]
    k_ETournamentNodeState_A_TimeoutRefund: _ClassVar[ETournamentNodeState]

class EDOTAGroupMergeResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTAGroupMergeResult_OK: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_FAILED_GENERIC: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_NOT_LEADER: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_TOO_MANY_PLAYERS: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_TOO_MANY_COACHES: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_ENGINE_MISMATCH: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_NO_SUCH_GROUP: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_OTHER_GROUP_NOT_OPEN: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_ALREADY_INVITED: _ClassVar[EDOTAGroupMergeResult]
    k_EDOTAGroupMergeResult_NOT_INVITED: _ClassVar[EDOTAGroupMergeResult]

class EPartyBeaconType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EPartyBeaconType_Available: _ClassVar[EPartyBeaconType]
    k_EPartyBeaconType_Joinable: _ClassVar[EPartyBeaconType]

k_ETournamentTemplate_None: ETournamentTemplate
k_ETournamentTemplate_AutomatedWin3: ETournamentTemplate
k_ETournamentGameState_Unknown: ETournamentGameState
k_ETournamentGameState_Canceled: ETournamentGameState
k_ETournamentGameState_Scheduled: ETournamentGameState
k_ETournamentGameState_Active: ETournamentGameState
k_ETournamentGameState_RadVictory: ETournamentGameState
k_ETournamentGameState_DireVictory: ETournamentGameState
k_ETournamentGameState_RadVictoryByForfeit: ETournamentGameState
k_ETournamentGameState_DireVictoryByForfeit: ETournamentGameState
k_ETournamentGameState_ServerFailure: ETournamentGameState
k_ETournamentGameState_NotNeeded: ETournamentGameState
k_ETournamentTeamState_Unknown: ETournamentTeamState
k_ETournamentTeamState_Node1: ETournamentTeamState
k_ETournamentTeamState_NodeMax: ETournamentTeamState
k_ETournamentTeamState_Eliminated: ETournamentTeamState
k_ETournamentTeamState_Forfeited: ETournamentTeamState
k_ETournamentTeamState_Finished1st: ETournamentTeamState
k_ETournamentTeamState_Finished2nd: ETournamentTeamState
k_ETournamentTeamState_Finished3rd: ETournamentTeamState
k_ETournamentTeamState_Finished4th: ETournamentTeamState
k_ETournamentTeamState_Finished5th: ETournamentTeamState
k_ETournamentTeamState_Finished6th: ETournamentTeamState
k_ETournamentTeamState_Finished7th: ETournamentTeamState
k_ETournamentTeamState_Finished8th: ETournamentTeamState
k_ETournamentTeamState_Finished9th: ETournamentTeamState
k_ETournamentTeamState_Finished10th: ETournamentTeamState
k_ETournamentTeamState_Finished11th: ETournamentTeamState
k_ETournamentTeamState_Finished12th: ETournamentTeamState
k_ETournamentTeamState_Finished13th: ETournamentTeamState
k_ETournamentTeamState_Finished14th: ETournamentTeamState
k_ETournamentTeamState_Finished15th: ETournamentTeamState
k_ETournamentTeamState_Finished16th: ETournamentTeamState
k_ETournamentState_Unknown: ETournamentState
k_ETournamentState_CanceledByAdmin: ETournamentState
k_ETournamentState_Completed: ETournamentState
k_ETournamentState_Merged: ETournamentState
k_ETournamentState_ServerFailure: ETournamentState
k_ETournamentState_TeamAbandoned: ETournamentState
k_ETournamentState_TeamTimeoutForfeit: ETournamentState
k_ETournamentState_TeamTimeoutRefund: ETournamentState
k_ETournamentState_ServerFailureGrantedVictory: ETournamentState
k_ETournamentState_TeamTimeoutGrantedVictory: ETournamentState
k_ETournamentState_InProgress: ETournamentState
k_ETournamentState_WaitingToMerge: ETournamentState
k_ETournamentNodeState_Unknown: ETournamentNodeState
k_ETournamentNodeState_Canceled: ETournamentNodeState
k_ETournamentNodeState_TeamsNotYetAssigned: ETournamentNodeState
k_ETournamentNodeState_InBetweenGames: ETournamentNodeState
k_ETournamentNodeState_GameInProgress: ETournamentNodeState
k_ETournamentNodeState_A_Won: ETournamentNodeState
k_ETournamentNodeState_B_Won: ETournamentNodeState
k_ETournamentNodeState_A_WonByForfeit: ETournamentNodeState
k_ETournamentNodeState_B_WonByForfeit: ETournamentNodeState
k_ETournamentNodeState_A_Bye: ETournamentNodeState
k_ETournamentNodeState_A_Abandoned: ETournamentNodeState
k_ETournamentNodeState_ServerFailure: ETournamentNodeState
k_ETournamentNodeState_A_TimeoutForfeit: ETournamentNodeState
k_ETournamentNodeState_A_TimeoutRefund: ETournamentNodeState
k_EDOTAGroupMergeResult_OK: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_FAILED_GENERIC: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_NOT_LEADER: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_TOO_MANY_PLAYERS: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_TOO_MANY_COACHES: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_ENGINE_MISMATCH: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_NO_SUCH_GROUP: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_OTHER_GROUP_NOT_OPEN: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_ALREADY_INVITED: EDOTAGroupMergeResult
k_EDOTAGroupMergeResult_NOT_INVITED: EDOTAGroupMergeResult
k_EPartyBeaconType_Available: EPartyBeaconType
k_EPartyBeaconType_Joinable: EPartyBeaconType
