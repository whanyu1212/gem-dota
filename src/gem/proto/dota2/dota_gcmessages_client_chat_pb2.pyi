from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgClientToGCPrivateChatInvite(_message.Message):
    __slots__ = ("private_chat_channel_name", "invited_account_id")
    PRIVATE_CHAT_CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    INVITED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    private_chat_channel_name: str
    invited_account_id: int
    def __init__(
        self, private_chat_channel_name: str | None = ..., invited_account_id: int | None = ...
    ) -> None: ...

class CMsgClientToGCPrivateChatKick(_message.Message):
    __slots__ = ("private_chat_channel_name", "kick_account_id")
    PRIVATE_CHAT_CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    KICK_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    private_chat_channel_name: str
    kick_account_id: int
    def __init__(
        self, private_chat_channel_name: str | None = ..., kick_account_id: int | None = ...
    ) -> None: ...

class CMsgClientToGCPrivateChatPromote(_message.Message):
    __slots__ = ("private_chat_channel_name", "promote_account_id")
    PRIVATE_CHAT_CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    PROMOTE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    private_chat_channel_name: str
    promote_account_id: int
    def __init__(
        self, private_chat_channel_name: str | None = ..., promote_account_id: int | None = ...
    ) -> None: ...

class CMsgClientToGCPrivateChatDemote(_message.Message):
    __slots__ = ("private_chat_channel_name", "demote_account_id")
    PRIVATE_CHAT_CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DEMOTE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    private_chat_channel_name: str
    demote_account_id: int
    def __init__(
        self, private_chat_channel_name: str | None = ..., demote_account_id: int | None = ...
    ) -> None: ...

class CMsgGCToClientPrivateChatResponse(_message.Message):
    __slots__ = ("private_chat_channel_name", "result", "username")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_CREATION_LOCK: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_SQL_TRANSACTION: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_SDO_LOAD: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_NO_PERMISSION: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_ALREADY_MEMBER: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_NOT_A_MEMBER: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_NO_REMAINING_ADMINS: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_NO_ROOM: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_CREATION_RATE_LIMITED: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_UNKNOWN_CHANNEL_NAME: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_UNKNOWN_USER: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_UNKNOWN_ERROR: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_CANNOT_KICK_ADMIN: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]
        FAILURE_ALREADY_ADMIN: _ClassVar[CMsgGCToClientPrivateChatResponse.Result]

    SUCCESS: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_CREATION_LOCK: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_SQL_TRANSACTION: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_SDO_LOAD: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_NO_PERMISSION: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_ALREADY_MEMBER: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_NOT_A_MEMBER: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_NO_REMAINING_ADMINS: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_NO_ROOM: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_CREATION_RATE_LIMITED: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_UNKNOWN_CHANNEL_NAME: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_UNKNOWN_USER: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_UNKNOWN_ERROR: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_CANNOT_KICK_ADMIN: CMsgGCToClientPrivateChatResponse.Result
    FAILURE_ALREADY_ADMIN: CMsgGCToClientPrivateChatResponse.Result
    PRIVATE_CHAT_CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    private_chat_channel_name: str
    result: CMsgGCToClientPrivateChatResponse.Result
    username: str
    def __init__(
        self,
        private_chat_channel_name: str | None = ...,
        result: CMsgGCToClientPrivateChatResponse.Result | str | None = ...,
        username: str | None = ...,
    ) -> None: ...

class CMsgDOTAJoinChatChannel(_message.Message):
    __slots__ = ("channel_name", "channel_type", "silent_rejection")
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SILENT_REJECTION_FIELD_NUMBER: _ClassVar[int]
    channel_name: str
    channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t
    silent_rejection: bool
    def __init__(
        self,
        channel_name: str | None = ...,
        channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t | str | None = ...,
        silent_rejection: bool = ...,
    ) -> None: ...

class CMsgDOTALeaveChatChannel(_message.Message):
    __slots__ = ("channel_id",)
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    def __init__(self, channel_id: int | None = ...) -> None: ...

class CMsgGCChatReportPublicSpam(_message.Message):
    __slots__ = ("channel_id", "channel_user_id")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    channel_user_id: int
    def __init__(self, channel_id: int | None = ..., channel_user_id: int | None = ...) -> None: ...

class CMsgDOTAChatModeratorBan(_message.Message):
    __slots__ = ("channel_id", "account_id", "duration")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    account_id: int
    duration: int
    def __init__(
        self, channel_id: int | None = ..., account_id: int | None = ..., duration: int | None = ...
    ) -> None: ...

class CMsgDOTAChatMessage(_message.Message):
    __slots__ = (
        "account_id",
        "channel_id",
        "persona_name",
        "text",
        "timestamp",
        "suggest_invite_account_id",
        "suggest_invite_name",
        "fantasy_draft_owner_account_id",
        "fantasy_draft_player_account_id",
        "event_id",
        "suggest_invite_to_lobby",
        "coin_flip",
        "player_id",
        "share_profile_account_id",
        "channel_user_id",
        "dice_roll",
        "share_party_id",
        "share_lobby_id",
        "share_lobby_custom_game_id",
        "share_lobby_passkey",
        "private_chat_channel_id",
        "status",
        "legacy_battle_cup_victory",
        "battle_cup_streak",
        "badge_level",
        "suggest_pick_hero_id",
        "suggest_pick_hero_role",
        "suggest_ban_hero_id",
        "trivia_answer",
        "requested_ability_id",
        "chat_flags",
        "started_finding_match",
        "ctrl_is_down",
        "favorite_team_id",
        "favorite_team_quality",
        "suggest_player_draft_pick",
        "player_draft_pick",
        "chat_wheel_message",
        "event_level",
        "suggest_pick_hero_facet",
        "requested_hero_id",
        "requested_hero_facet_key",
    )
    class DiceRoll(_message.Message):
        __slots__ = ("roll_min", "roll_max", "result")
        ROLL_MIN_FIELD_NUMBER: _ClassVar[int]
        ROLL_MAX_FIELD_NUMBER: _ClassVar[int]
        RESULT_FIELD_NUMBER: _ClassVar[int]
        roll_min: int
        roll_max: int
        result: int
        def __init__(
            self, roll_min: int | None = ..., roll_max: int | None = ..., result: int | None = ...
        ) -> None: ...

    class TriviaAnswered(_message.Message):
        __slots__ = (
            "question_id",
            "answer_index",
            "party_questions_correct",
            "party_questions_viewed",
            "party_trivia_points",
        )
        QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
        ANSWER_INDEX_FIELD_NUMBER: _ClassVar[int]
        PARTY_QUESTIONS_CORRECT_FIELD_NUMBER: _ClassVar[int]
        PARTY_QUESTIONS_VIEWED_FIELD_NUMBER: _ClassVar[int]
        PARTY_TRIVIA_POINTS_FIELD_NUMBER: _ClassVar[int]
        question_id: int
        answer_index: int
        party_questions_correct: int
        party_questions_viewed: int
        party_trivia_points: int
        def __init__(
            self,
            question_id: int | None = ...,
            answer_index: int | None = ...,
            party_questions_correct: int | None = ...,
            party_questions_viewed: int | None = ...,
            party_trivia_points: int | None = ...,
        ) -> None: ...

    class PlayerDraftPick(_message.Message):
        __slots__ = ("player_id", "team")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        team: int
        def __init__(self, player_id: int | None = ..., team: int | None = ...) -> None: ...

    class ChatWheelMessage(_message.Message):
        __slots__ = ("message_id", "emoticon_id", "message_text", "hero_badge_tier")
        MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
        EMOTICON_ID_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_TEXT_FIELD_NUMBER: _ClassVar[int]
        HERO_BADGE_TIER_FIELD_NUMBER: _ClassVar[int]
        message_id: int
        emoticon_id: int
        message_text: str
        hero_badge_tier: int
        def __init__(
            self,
            message_id: int | None = ...,
            emoticon_id: int | None = ...,
            message_text: str | None = ...,
            hero_badge_tier: int | None = ...,
        ) -> None: ...

    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PERSONA_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_INVITE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_INVITE_NAME_FIELD_NUMBER: _ClassVar[int]
    FANTASY_DRAFT_OWNER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FANTASY_DRAFT_PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_INVITE_TO_LOBBY_FIELD_NUMBER: _ClassVar[int]
    COIN_FLIP_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    SHARE_PROFILE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    DICE_ROLL_FIELD_NUMBER: _ClassVar[int]
    SHARE_PARTY_ID_FIELD_NUMBER: _ClassVar[int]
    SHARE_LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    SHARE_LOBBY_CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SHARE_LOBBY_PASSKEY_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_CHAT_CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LEGACY_BATTLE_CUP_VICTORY_FIELD_NUMBER: _ClassVar[int]
    BATTLE_CUP_STREAK_FIELD_NUMBER: _ClassVar[int]
    BADGE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_PICK_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_PICK_HERO_ROLE_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_BAN_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    TRIVIA_ANSWER_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    STARTED_FINDING_MATCH_FIELD_NUMBER: _ClassVar[int]
    CTRL_IS_DOWN_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_TEAM_QUALITY_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_PLAYER_DRAFT_PICK_FIELD_NUMBER: _ClassVar[int]
    PLAYER_DRAFT_PICK_FIELD_NUMBER: _ClassVar[int]
    CHAT_WHEEL_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EVENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SUGGEST_PICK_HERO_FACET_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_FACET_KEY_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    channel_id: int
    persona_name: str
    text: str
    timestamp: int
    suggest_invite_account_id: int
    suggest_invite_name: str
    fantasy_draft_owner_account_id: int
    fantasy_draft_player_account_id: int
    event_id: int
    suggest_invite_to_lobby: bool
    coin_flip: bool
    player_id: int
    share_profile_account_id: int
    channel_user_id: int
    dice_roll: CMsgDOTAChatMessage.DiceRoll
    share_party_id: int
    share_lobby_id: int
    share_lobby_custom_game_id: int
    share_lobby_passkey: str
    private_chat_channel_id: int
    status: int
    legacy_battle_cup_victory: bool
    battle_cup_streak: int
    badge_level: int
    suggest_pick_hero_id: int
    suggest_pick_hero_role: str
    suggest_ban_hero_id: int
    trivia_answer: CMsgDOTAChatMessage.TriviaAnswered
    requested_ability_id: int
    chat_flags: int
    started_finding_match: bool
    ctrl_is_down: bool
    favorite_team_id: int
    favorite_team_quality: int
    suggest_player_draft_pick: int
    player_draft_pick: CMsgDOTAChatMessage.PlayerDraftPick
    chat_wheel_message: CMsgDOTAChatMessage.ChatWheelMessage
    event_level: int
    suggest_pick_hero_facet: int
    requested_hero_id: int
    requested_hero_facet_key: int
    def __init__(
        self,
        account_id: int | None = ...,
        channel_id: int | None = ...,
        persona_name: str | None = ...,
        text: str | None = ...,
        timestamp: int | None = ...,
        suggest_invite_account_id: int | None = ...,
        suggest_invite_name: str | None = ...,
        fantasy_draft_owner_account_id: int | None = ...,
        fantasy_draft_player_account_id: int | None = ...,
        event_id: int | None = ...,
        suggest_invite_to_lobby: bool = ...,
        coin_flip: bool = ...,
        player_id: int | None = ...,
        share_profile_account_id: int | None = ...,
        channel_user_id: int | None = ...,
        dice_roll: CMsgDOTAChatMessage.DiceRoll | _Mapping | None = ...,
        share_party_id: int | None = ...,
        share_lobby_id: int | None = ...,
        share_lobby_custom_game_id: int | None = ...,
        share_lobby_passkey: str | None = ...,
        private_chat_channel_id: int | None = ...,
        status: int | None = ...,
        legacy_battle_cup_victory: bool = ...,
        battle_cup_streak: int | None = ...,
        badge_level: int | None = ...,
        suggest_pick_hero_id: int | None = ...,
        suggest_pick_hero_role: str | None = ...,
        suggest_ban_hero_id: int | None = ...,
        trivia_answer: CMsgDOTAChatMessage.TriviaAnswered | _Mapping | None = ...,
        requested_ability_id: int | None = ...,
        chat_flags: int | None = ...,
        started_finding_match: bool = ...,
        ctrl_is_down: bool = ...,
        favorite_team_id: int | None = ...,
        favorite_team_quality: int | None = ...,
        suggest_player_draft_pick: int | None = ...,
        player_draft_pick: CMsgDOTAChatMessage.PlayerDraftPick | _Mapping | None = ...,
        chat_wheel_message: CMsgDOTAChatMessage.ChatWheelMessage | _Mapping | None = ...,
        event_level: int | None = ...,
        suggest_pick_hero_facet: int | None = ...,
        requested_hero_id: int | None = ...,
        requested_hero_facet_key: int | None = ...,
    ) -> None: ...

class CMsgDOTAChatMember(_message.Message):
    __slots__ = ("steam_id", "persona_name", "channel_user_id", "status")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PERSONA_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    persona_name: str
    channel_user_id: int
    status: int
    def __init__(
        self,
        steam_id: int | None = ...,
        persona_name: str | None = ...,
        channel_user_id: int | None = ...,
        status: int | None = ...,
    ) -> None: ...

class CMsgDOTAJoinChatChannelResponse(_message.Message):
    __slots__ = (
        "response",
        "channel_name",
        "channel_id",
        "max_members",
        "members",
        "channel_type",
        "result",
        "gc_initiated_join",
        "channel_user_id",
        "welcome_message",
        "special_privileges",
    )
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        JOIN_SUCCESS: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        INVALID_CHANNEL_TYPE: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        ACCOUNT_NOT_FOUND: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        ACH_FAILED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        USER_IN_TOO_MANY_CHANNELS: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        RATE_LIMIT_EXCEEDED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        CHANNEL_FULL: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        CHANNEL_FULL_OVERFLOWED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        FAILED_TO_ADD_USER: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        CHANNEL_TYPE_DISABLED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        PRIVATE_CHAT_CREATE_FAILED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        PRIVATE_CHAT_NO_PERMISSION: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        PRIVATE_CHAT_CREATE_LOCK_FAILED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        PRIVATE_CHAT_KICKED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        USER_NOT_ALLOWED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        ENSURE_SPECIAL_PRIVILEGES_FAILED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        NEW_PLAYER_USER_NOT_ELIGIBLE: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        SILENT_ERROR: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]
        NEW_PLAYER_USER_BANNED: _ClassVar[CMsgDOTAJoinChatChannelResponse.Result]

    JOIN_SUCCESS: CMsgDOTAJoinChatChannelResponse.Result
    INVALID_CHANNEL_TYPE: CMsgDOTAJoinChatChannelResponse.Result
    ACCOUNT_NOT_FOUND: CMsgDOTAJoinChatChannelResponse.Result
    ACH_FAILED: CMsgDOTAJoinChatChannelResponse.Result
    USER_IN_TOO_MANY_CHANNELS: CMsgDOTAJoinChatChannelResponse.Result
    RATE_LIMIT_EXCEEDED: CMsgDOTAJoinChatChannelResponse.Result
    CHANNEL_FULL: CMsgDOTAJoinChatChannelResponse.Result
    CHANNEL_FULL_OVERFLOWED: CMsgDOTAJoinChatChannelResponse.Result
    FAILED_TO_ADD_USER: CMsgDOTAJoinChatChannelResponse.Result
    CHANNEL_TYPE_DISABLED: CMsgDOTAJoinChatChannelResponse.Result
    PRIVATE_CHAT_CREATE_FAILED: CMsgDOTAJoinChatChannelResponse.Result
    PRIVATE_CHAT_NO_PERMISSION: CMsgDOTAJoinChatChannelResponse.Result
    PRIVATE_CHAT_CREATE_LOCK_FAILED: CMsgDOTAJoinChatChannelResponse.Result
    PRIVATE_CHAT_KICKED: CMsgDOTAJoinChatChannelResponse.Result
    USER_NOT_ALLOWED: CMsgDOTAJoinChatChannelResponse.Result
    ENSURE_SPECIAL_PRIVILEGES_FAILED: CMsgDOTAJoinChatChannelResponse.Result
    NEW_PLAYER_USER_NOT_ELIGIBLE: CMsgDOTAJoinChatChannelResponse.Result
    SILENT_ERROR: CMsgDOTAJoinChatChannelResponse.Result
    NEW_PLAYER_USER_BANNED: CMsgDOTAJoinChatChannelResponse.Result
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    GC_INITIATED_JOIN_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    WELCOME_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
    response: int
    channel_name: str
    channel_id: int
    max_members: int
    members: _containers.RepeatedCompositeFieldContainer[CMsgDOTAChatMember]
    channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t
    result: CMsgDOTAJoinChatChannelResponse.Result
    gc_initiated_join: bool
    channel_user_id: int
    welcome_message: str
    special_privileges: _dota_shared_enums_pb2.EChatSpecialPrivileges
    def __init__(
        self,
        response: int | None = ...,
        channel_name: str | None = ...,
        channel_id: int | None = ...,
        max_members: int | None = ...,
        members: _Iterable[CMsgDOTAChatMember | _Mapping] | None = ...,
        channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t | str | None = ...,
        result: CMsgDOTAJoinChatChannelResponse.Result | str | None = ...,
        gc_initiated_join: bool = ...,
        channel_user_id: int | None = ...,
        welcome_message: str | None = ...,
        special_privileges: _dota_shared_enums_pb2.EChatSpecialPrivileges | str | None = ...,
    ) -> None: ...

class CMsgDOTAOtherJoinedChatChannel(_message.Message):
    __slots__ = ("channel_id", "persona_name", "steam_id", "channel_user_id", "status")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PERSONA_NAME_FIELD_NUMBER: _ClassVar[int]
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    persona_name: str
    steam_id: int
    channel_user_id: int
    status: int
    def __init__(
        self,
        channel_id: int | None = ...,
        persona_name: str | None = ...,
        steam_id: int | None = ...,
        channel_user_id: int | None = ...,
        status: int | None = ...,
    ) -> None: ...

class CMsgDOTAOtherLeftChatChannel(_message.Message):
    __slots__ = ("channel_id", "steam_id", "channel_user_id")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    steam_id: int
    channel_user_id: int
    def __init__(
        self,
        channel_id: int | None = ...,
        steam_id: int | None = ...,
        channel_user_id: int | None = ...,
    ) -> None: ...

class CMsgDOTARequestChatChannelList(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTARequestChatChannelListResponse(_message.Message):
    __slots__ = ("channels",)
    class ChatChannel(_message.Message):
        __slots__ = ("channel_name", "num_members", "channel_type")
        CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
        NUM_MEMBERS_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
        channel_name: str
        num_members: int
        channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t
        def __init__(
            self,
            channel_name: str | None = ...,
            num_members: int | None = ...,
            channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t | str | None = ...,
        ) -> None: ...

    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTARequestChatChannelListResponse.ChatChannel
    ]
    def __init__(
        self,
        channels: _Iterable[CMsgDOTARequestChatChannelListResponse.ChatChannel | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgDOTAChatGetUserListResponse(_message.Message):
    __slots__ = ("channel_id", "members")
    class Member(_message.Message):
        __slots__ = ("steam_id", "persona_name", "channel_user_id", "status")
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        PERSONA_NAME_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_USER_ID_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        steam_id: int
        persona_name: str
        channel_user_id: int
        status: int
        def __init__(
            self,
            steam_id: int | None = ...,
            persona_name: str | None = ...,
            channel_user_id: int | None = ...,
            status: int | None = ...,
        ) -> None: ...

    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    members: _containers.RepeatedCompositeFieldContainer[CMsgDOTAChatGetUserListResponse.Member]
    def __init__(
        self,
        channel_id: int | None = ...,
        members: _Iterable[CMsgDOTAChatGetUserListResponse.Member | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTAChatGetMemberCount(_message.Message):
    __slots__ = ("channel_name", "channel_type")
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    channel_name: str
    channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t
    def __init__(
        self,
        channel_name: str | None = ...,
        channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t | str | None = ...,
    ) -> None: ...

class CMsgDOTAChatGetMemberCountResponse(_message.Message):
    __slots__ = ("channel_name", "channel_type", "member_count")
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    channel_name: str
    channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t
    member_count: int
    def __init__(
        self,
        channel_name: str | None = ...,
        channel_type: _dota_shared_enums_pb2.DOTAChatChannelType_t | str | None = ...,
        member_count: int | None = ...,
    ) -> None: ...

class CMsgDOTAChatRegionsEnabled(_message.Message):
    __slots__ = ("enable_all_regions", "enabled_regions")
    class Region(_message.Message):
        __slots__ = ("min_latitude", "max_latitude", "min_longitude", "max_longitude")
        MIN_LATITUDE_FIELD_NUMBER: _ClassVar[int]
        MAX_LATITUDE_FIELD_NUMBER: _ClassVar[int]
        MIN_LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        MAX_LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        min_latitude: float
        max_latitude: float
        min_longitude: float
        max_longitude: float
        def __init__(
            self,
            min_latitude: float | None = ...,
            max_latitude: float | None = ...,
            min_longitude: float | None = ...,
            max_longitude: float | None = ...,
        ) -> None: ...

    ENABLE_ALL_REGIONS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_REGIONS_FIELD_NUMBER: _ClassVar[int]
    enable_all_regions: bool
    enabled_regions: _containers.RepeatedCompositeFieldContainer[CMsgDOTAChatRegionsEnabled.Region]
    def __init__(
        self,
        enable_all_regions: bool = ...,
        enabled_regions: _Iterable[CMsgDOTAChatRegionsEnabled.Region | _Mapping] | None = ...,
    ) -> None: ...
