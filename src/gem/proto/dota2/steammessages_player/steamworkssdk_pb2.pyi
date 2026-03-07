from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ENotificationSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ENotificationSettingNotifyUseDefault: _ClassVar[ENotificationSetting]
    k_ENotificationSettingAlways: _ClassVar[ENotificationSetting]
    k_ENotificationSettingNever: _ClassVar[ENotificationSetting]

k_ENotificationSettingNotifyUseDefault: ENotificationSetting
k_ENotificationSettingAlways: ENotificationSetting
k_ENotificationSettingNever: ENotificationSetting

class CPlayer_GetMutualFriendsForIncomingInvites_Request(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPlayer_IncomingInviteMutualFriendList(_message.Message):
    __slots__ = ("steamid", "mutual_friend_account_ids")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    MUTUAL_FRIEND_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    mutual_friend_account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, steamid: int | None = ..., mutual_friend_account_ids: _Iterable[int] | None = ...
    ) -> None: ...

class CPlayer_GetMutualFriendsForIncomingInvites_Response(_message.Message):
    __slots__ = ("incoming_invite_mutual_friends_lists",)
    INCOMING_INVITE_MUTUAL_FRIENDS_LISTS_FIELD_NUMBER: _ClassVar[int]
    incoming_invite_mutual_friends_lists: _containers.RepeatedCompositeFieldContainer[
        CPlayer_IncomingInviteMutualFriendList
    ]
    def __init__(
        self,
        incoming_invite_mutual_friends_lists: _Iterable[
            CPlayer_IncomingInviteMutualFriendList | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CPlayer_GetFriendsGameplayInfo_Request(_message.Message):
    __slots__ = ("appid",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appid: int
    def __init__(self, appid: int | None = ...) -> None: ...

class CPlayer_GetFriendsGameplayInfo_Response(_message.Message):
    __slots__ = ("your_info", "in_game", "played_recently", "played_ever", "owns", "in_wishlist")
    class FriendsGameplayInfo(_message.Message):
        __slots__ = ("steamid", "minutes_played", "minutes_played_forever")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        MINUTES_PLAYED_FIELD_NUMBER: _ClassVar[int]
        MINUTES_PLAYED_FOREVER_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        minutes_played: int
        minutes_played_forever: int
        def __init__(
            self,
            steamid: int | None = ...,
            minutes_played: int | None = ...,
            minutes_played_forever: int | None = ...,
        ) -> None: ...

    class OwnGameplayInfo(_message.Message):
        __slots__ = ("steamid", "minutes_played", "minutes_played_forever", "in_wishlist", "owned")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        MINUTES_PLAYED_FIELD_NUMBER: _ClassVar[int]
        MINUTES_PLAYED_FOREVER_FIELD_NUMBER: _ClassVar[int]
        IN_WISHLIST_FIELD_NUMBER: _ClassVar[int]
        OWNED_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        minutes_played: int
        minutes_played_forever: int
        in_wishlist: bool
        owned: bool
        def __init__(
            self,
            steamid: int | None = ...,
            minutes_played: int | None = ...,
            minutes_played_forever: int | None = ...,
            in_wishlist: bool = ...,
            owned: bool = ...,
        ) -> None: ...

    YOUR_INFO_FIELD_NUMBER: _ClassVar[int]
    IN_GAME_FIELD_NUMBER: _ClassVar[int]
    PLAYED_RECENTLY_FIELD_NUMBER: _ClassVar[int]
    PLAYED_EVER_FIELD_NUMBER: _ClassVar[int]
    OWNS_FIELD_NUMBER: _ClassVar[int]
    IN_WISHLIST_FIELD_NUMBER: _ClassVar[int]
    your_info: CPlayer_GetFriendsGameplayInfo_Response.OwnGameplayInfo
    in_game: _containers.RepeatedCompositeFieldContainer[
        CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo
    ]
    played_recently: _containers.RepeatedCompositeFieldContainer[
        CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo
    ]
    played_ever: _containers.RepeatedCompositeFieldContainer[
        CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo
    ]
    owns: _containers.RepeatedCompositeFieldContainer[
        CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo
    ]
    in_wishlist: _containers.RepeatedCompositeFieldContainer[
        CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo
    ]
    def __init__(
        self,
        your_info: CPlayer_GetFriendsGameplayInfo_Response.OwnGameplayInfo | _Mapping | None = ...,
        in_game: _Iterable[CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo | _Mapping]
        | None = ...,
        played_recently: _Iterable[
            CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo | _Mapping
        ]
        | None = ...,
        played_ever: _Iterable[
            CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo | _Mapping
        ]
        | None = ...,
        owns: _Iterable[CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo | _Mapping]
        | None = ...,
        in_wishlist: _Iterable[
            CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CPlayer_GetGameBadgeLevels_Request(_message.Message):
    __slots__ = ("appid",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appid: int
    def __init__(self, appid: int | None = ...) -> None: ...

class CPlayer_GetGameBadgeLevels_Response(_message.Message):
    __slots__ = ("player_level", "badges")
    class Badge(_message.Message):
        __slots__ = ("level", "series", "border_color")
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        SERIES_FIELD_NUMBER: _ClassVar[int]
        BORDER_COLOR_FIELD_NUMBER: _ClassVar[int]
        level: int
        series: int
        border_color: int
        def __init__(
            self, level: int | None = ..., series: int | None = ..., border_color: int | None = ...
        ) -> None: ...

    PLAYER_LEVEL_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    player_level: int
    badges: _containers.RepeatedCompositeFieldContainer[CPlayer_GetGameBadgeLevels_Response.Badge]
    def __init__(
        self,
        player_level: int | None = ...,
        badges: _Iterable[CPlayer_GetGameBadgeLevels_Response.Badge | _Mapping] | None = ...,
    ) -> None: ...

class CPlayer_GetLastPlayedTimes_Request(_message.Message):
    __slots__ = ("min_last_played",)
    MIN_LAST_PLAYED_FIELD_NUMBER: _ClassVar[int]
    min_last_played: int
    def __init__(self, min_last_played: int | None = ...) -> None: ...

class CPlayer_GetLastPlayedTimes_Response(_message.Message):
    __slots__ = ("games",)
    class Game(_message.Message):
        __slots__ = (
            "appid",
            "last_playtime",
            "playtime_2weeks",
            "playtime_forever",
            "first_playtime",
        )
        APPID_FIELD_NUMBER: _ClassVar[int]
        LAST_PLAYTIME_FIELD_NUMBER: _ClassVar[int]
        PLAYTIME_2WEEKS_FIELD_NUMBER: _ClassVar[int]
        PLAYTIME_FOREVER_FIELD_NUMBER: _ClassVar[int]
        FIRST_PLAYTIME_FIELD_NUMBER: _ClassVar[int]
        appid: int
        last_playtime: int
        playtime_2weeks: int
        playtime_forever: int
        first_playtime: int
        def __init__(
            self,
            appid: int | None = ...,
            last_playtime: int | None = ...,
            playtime_2weeks: int | None = ...,
            playtime_forever: int | None = ...,
            first_playtime: int | None = ...,
        ) -> None: ...

    GAMES_FIELD_NUMBER: _ClassVar[int]
    games: _containers.RepeatedCompositeFieldContainer[CPlayer_GetLastPlayedTimes_Response.Game]
    def __init__(
        self, games: _Iterable[CPlayer_GetLastPlayedTimes_Response.Game | _Mapping] | None = ...
    ) -> None: ...

class CPlayer_AcceptSSA_Request(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPlayer_AcceptSSA_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPlayer_GetNicknameList_Request(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPlayer_GetNicknameList_Response(_message.Message):
    __slots__ = ("nicknames",)
    class PlayerNickname(_message.Message):
        __slots__ = ("accountid", "nickname")
        ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        accountid: int
        nickname: str
        def __init__(self, accountid: int | None = ..., nickname: str | None = ...) -> None: ...

    NICKNAMES_FIELD_NUMBER: _ClassVar[int]
    nicknames: _containers.RepeatedCompositeFieldContainer[
        CPlayer_GetNicknameList_Response.PlayerNickname
    ]
    def __init__(
        self,
        nicknames: _Iterable[CPlayer_GetNicknameList_Response.PlayerNickname | _Mapping]
        | None = ...,
    ) -> None: ...

class CPlayer_GetPerFriendPreferences_Request(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PerFriendPreferences(_message.Message):
    __slots__ = (
        "accountid",
        "nickname",
        "notifications_showingame",
        "notifications_showonline",
        "notifications_showmessages",
        "sounds_showingame",
        "sounds_showonline",
        "sounds_showmessages",
        "notifications_sendmobile",
    )
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_SHOWINGAME_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_SHOWONLINE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_SHOWMESSAGES_FIELD_NUMBER: _ClassVar[int]
    SOUNDS_SHOWINGAME_FIELD_NUMBER: _ClassVar[int]
    SOUNDS_SHOWONLINE_FIELD_NUMBER: _ClassVar[int]
    SOUNDS_SHOWMESSAGES_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_SENDMOBILE_FIELD_NUMBER: _ClassVar[int]
    accountid: int
    nickname: str
    notifications_showingame: ENotificationSetting
    notifications_showonline: ENotificationSetting
    notifications_showmessages: ENotificationSetting
    sounds_showingame: ENotificationSetting
    sounds_showonline: ENotificationSetting
    sounds_showmessages: ENotificationSetting
    notifications_sendmobile: ENotificationSetting
    def __init__(
        self,
        accountid: int | None = ...,
        nickname: str | None = ...,
        notifications_showingame: ENotificationSetting | str | None = ...,
        notifications_showonline: ENotificationSetting | str | None = ...,
        notifications_showmessages: ENotificationSetting | str | None = ...,
        sounds_showingame: ENotificationSetting | str | None = ...,
        sounds_showonline: ENotificationSetting | str | None = ...,
        sounds_showmessages: ENotificationSetting | str | None = ...,
        notifications_sendmobile: ENotificationSetting | str | None = ...,
    ) -> None: ...

class CPlayer_GetPerFriendPreferences_Response(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: _containers.RepeatedCompositeFieldContainer[PerFriendPreferences]
    def __init__(
        self, preferences: _Iterable[PerFriendPreferences | _Mapping] | None = ...
    ) -> None: ...

class CPlayer_SetPerFriendPreferences_Request(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: PerFriendPreferences
    def __init__(self, preferences: PerFriendPreferences | _Mapping | None = ...) -> None: ...

class CPlayer_SetPerFriendPreferences_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPlayer_AddFriend_Request(_message.Message):
    __slots__ = ("steamid",)
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    def __init__(self, steamid: int | None = ...) -> None: ...

class CPlayer_AddFriend_Response(_message.Message):
    __slots__ = ("invite_sent", "friend_relationship")
    INVITE_SENT_FIELD_NUMBER: _ClassVar[int]
    FRIEND_RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    invite_sent: bool
    friend_relationship: int
    def __init__(self, invite_sent: bool = ..., friend_relationship: int | None = ...) -> None: ...

class CPlayer_RemoveFriend_Request(_message.Message):
    __slots__ = ("steamid",)
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    def __init__(self, steamid: int | None = ...) -> None: ...

class CPlayer_RemoveFriend_Response(_message.Message):
    __slots__ = ("friend_relationship",)
    FRIEND_RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    friend_relationship: int
    def __init__(self, friend_relationship: int | None = ...) -> None: ...

class CPlayer_IgnoreFriend_Request(_message.Message):
    __slots__ = ("steamid", "unignore")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    UNIGNORE_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    unignore: bool
    def __init__(self, steamid: int | None = ..., unignore: bool = ...) -> None: ...

class CPlayer_IgnoreFriend_Response(_message.Message):
    __slots__ = ("friend_relationship",)
    FRIEND_RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    friend_relationship: int
    def __init__(self, friend_relationship: int | None = ...) -> None: ...

class CPlayer_GetCommunityPreferences_Request(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPlayer_CommunityPreferences(_message.Message):
    __slots__ = (
        "hide_adult_content_violence",
        "hide_adult_content_sex",
        "parenthesize_nicknames",
        "timestamp_updated",
    )
    HIDE_ADULT_CONTENT_VIOLENCE_FIELD_NUMBER: _ClassVar[int]
    HIDE_ADULT_CONTENT_SEX_FIELD_NUMBER: _ClassVar[int]
    PARENTHESIZE_NICKNAMES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_UPDATED_FIELD_NUMBER: _ClassVar[int]
    hide_adult_content_violence: bool
    hide_adult_content_sex: bool
    parenthesize_nicknames: bool
    timestamp_updated: int
    def __init__(
        self,
        hide_adult_content_violence: bool = ...,
        hide_adult_content_sex: bool = ...,
        parenthesize_nicknames: bool = ...,
        timestamp_updated: int | None = ...,
    ) -> None: ...

class CPlayer_GetCommunityPreferences_Response(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: CPlayer_CommunityPreferences
    def __init__(
        self, preferences: CPlayer_CommunityPreferences | _Mapping | None = ...
    ) -> None: ...

class CPlayer_SetCommunityPreferences_Request(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: CPlayer_CommunityPreferences
    def __init__(
        self, preferences: CPlayer_CommunityPreferences | _Mapping | None = ...
    ) -> None: ...

class CPlayer_SetCommunityPreferences_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPlayer_GetNewSteamAnnouncementState_Request(_message.Message):
    __slots__ = ("language",)
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    language: int
    def __init__(self, language: int | None = ...) -> None: ...

class CPlayer_GetNewSteamAnnouncementState_Response(_message.Message):
    __slots__ = (
        "state",
        "announcement_headline",
        "announcement_url",
        "time_posted",
        "announcement_gid",
    )
    STATE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_HEADLINE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_URL_FIELD_NUMBER: _ClassVar[int]
    TIME_POSTED_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_GID_FIELD_NUMBER: _ClassVar[int]
    state: int
    announcement_headline: str
    announcement_url: str
    time_posted: int
    announcement_gid: int
    def __init__(
        self,
        state: int | None = ...,
        announcement_headline: str | None = ...,
        announcement_url: str | None = ...,
        time_posted: int | None = ...,
        announcement_gid: int | None = ...,
    ) -> None: ...

class CPlayer_UpdateSteamAnnouncementLastRead_Request(_message.Message):
    __slots__ = ("announcement_gid", "time_posted")
    ANNOUNCEMENT_GID_FIELD_NUMBER: _ClassVar[int]
    TIME_POSTED_FIELD_NUMBER: _ClassVar[int]
    announcement_gid: int
    time_posted: int
    def __init__(
        self, announcement_gid: int | None = ..., time_posted: int | None = ...
    ) -> None: ...

class CPlayer_UpdateSteamAnnouncementLastRead_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
