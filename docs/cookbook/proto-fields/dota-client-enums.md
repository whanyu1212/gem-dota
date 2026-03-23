# dota_client_enums.proto

- Module: `dota_client_enums_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **0** (top-level: 0)
- Enums: **7** (top-level: 7)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

*(No messages in this proto file.)*

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ETournamentTemplate</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ETournamentTemplate_None` | 0 |
| `k_ETournamentTemplate_AutomatedWin3` | 1 |

</details>

<details>
<summary><code>ETournamentGameState</code> — values: 10</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ETournamentGameState_Unknown` | 0 |
| `k_ETournamentGameState_Canceled` | 1 |
| `k_ETournamentGameState_Scheduled` | 2 |
| `k_ETournamentGameState_Active` | 3 |
| `k_ETournamentGameState_RadVictory` | 20 |
| `k_ETournamentGameState_DireVictory` | 21 |
| `k_ETournamentGameState_RadVictoryByForfeit` | 22 |
| `k_ETournamentGameState_DireVictoryByForfeit` | 23 |
| `k_ETournamentGameState_ServerFailure` | 40 |
| `k_ETournamentGameState_NotNeeded` | 41 |

</details>

<details>
<summary><code>ETournamentTeamState</code> — values: 21</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ETournamentTeamState_Unknown` | 0 |
| `k_ETournamentTeamState_Node1` | 1 |
| `k_ETournamentTeamState_NodeMax` | 1024 |
| `k_ETournamentTeamState_Eliminated` | 14003 |
| `k_ETournamentTeamState_Forfeited` | 14004 |
| `k_ETournamentTeamState_Finished1st` | 15001 |
| `k_ETournamentTeamState_Finished2nd` | 15002 |
| `k_ETournamentTeamState_Finished3rd` | 15003 |
| `k_ETournamentTeamState_Finished4th` | 15004 |
| `k_ETournamentTeamState_Finished5th` | 15005 |
| `k_ETournamentTeamState_Finished6th` | 15006 |
| `k_ETournamentTeamState_Finished7th` | 15007 |
| `k_ETournamentTeamState_Finished8th` | 15008 |
| `k_ETournamentTeamState_Finished9th` | 15009 |
| `k_ETournamentTeamState_Finished10th` | 15010 |
| `k_ETournamentTeamState_Finished11th` | 15011 |
| `k_ETournamentTeamState_Finished12th` | 15012 |
| `k_ETournamentTeamState_Finished13th` | 15013 |
| `k_ETournamentTeamState_Finished14th` | 15014 |
| `k_ETournamentTeamState_Finished15th` | 15015 |
| `k_ETournamentTeamState_Finished16th` | 15016 |

</details>

<details>
<summary><code>ETournamentState</code> — values: 12</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ETournamentState_Unknown` | 0 |
| `k_ETournamentState_CanceledByAdmin` | 1 |
| `k_ETournamentState_Completed` | 2 |
| `k_ETournamentState_Merged` | 3 |
| `k_ETournamentState_ServerFailure` | 4 |
| `k_ETournamentState_TeamAbandoned` | 5 |
| `k_ETournamentState_TeamTimeoutForfeit` | 6 |
| `k_ETournamentState_TeamTimeoutRefund` | 7 |
| `k_ETournamentState_ServerFailureGrantedVictory` | 8 |
| `k_ETournamentState_TeamTimeoutGrantedVictory` | 9 |
| `k_ETournamentState_InProgress` | 100 |
| `k_ETournamentState_WaitingToMerge` | 101 |

</details>

<details>
<summary><code>ETournamentNodeState</code> — values: 14</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ETournamentNodeState_Unknown` | 0 |
| `k_ETournamentNodeState_Canceled` | 1 |
| `k_ETournamentNodeState_TeamsNotYetAssigned` | 2 |
| `k_ETournamentNodeState_InBetweenGames` | 3 |
| `k_ETournamentNodeState_GameInProgress` | 4 |
| `k_ETournamentNodeState_A_Won` | 5 |
| `k_ETournamentNodeState_B_Won` | 6 |
| `k_ETournamentNodeState_A_WonByForfeit` | 7 |
| `k_ETournamentNodeState_B_WonByForfeit` | 8 |
| `k_ETournamentNodeState_A_Bye` | 9 |
| `k_ETournamentNodeState_A_Abandoned` | 10 |
| `k_ETournamentNodeState_ServerFailure` | 11 |
| `k_ETournamentNodeState_A_TimeoutForfeit` | 12 |
| `k_ETournamentNodeState_A_TimeoutRefund` | 13 |

</details>

<details>
<summary><code>EDOTAGroupMergeResult</code> — values: 10</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDOTAGroupMergeResult_OK` | 0 |
| `k_EDOTAGroupMergeResult_FAILED_GENERIC` | 1 |
| `k_EDOTAGroupMergeResult_NOT_LEADER` | 2 |
| `k_EDOTAGroupMergeResult_TOO_MANY_PLAYERS` | 3 |
| `k_EDOTAGroupMergeResult_TOO_MANY_COACHES` | 4 |
| `k_EDOTAGroupMergeResult_ENGINE_MISMATCH` | 5 |
| `k_EDOTAGroupMergeResult_NO_SUCH_GROUP` | 6 |
| `k_EDOTAGroupMergeResult_OTHER_GROUP_NOT_OPEN` | 7 |
| `k_EDOTAGroupMergeResult_ALREADY_INVITED` | 8 |
| `k_EDOTAGroupMergeResult_NOT_INVITED` | 9 |

</details>

<details>
<summary><code>EPartyBeaconType</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EPartyBeaconType_Available` | 0 |
| `k_EPartyBeaconType_Joinable` | 1 |

</details>
