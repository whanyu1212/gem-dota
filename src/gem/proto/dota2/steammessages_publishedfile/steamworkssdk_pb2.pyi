from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CPublishedFile_Subscribe_Request(_message.Message):
    __slots__ = ("publishedfileid", "list_type", "appid", "notify_client")
    PUBLISHEDFILEID_FIELD_NUMBER: _ClassVar[int]
    LIST_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_CLIENT_FIELD_NUMBER: _ClassVar[int]
    publishedfileid: int
    list_type: int
    appid: int
    notify_client: bool
    def __init__(
        self,
        publishedfileid: int | None = ...,
        list_type: int | None = ...,
        appid: int | None = ...,
        notify_client: bool = ...,
    ) -> None: ...

class CPublishedFile_Subscribe_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPublishedFile_Unsubscribe_Request(_message.Message):
    __slots__ = ("publishedfileid", "list_type", "appid", "notify_client")
    PUBLISHEDFILEID_FIELD_NUMBER: _ClassVar[int]
    LIST_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_CLIENT_FIELD_NUMBER: _ClassVar[int]
    publishedfileid: int
    list_type: int
    appid: int
    notify_client: bool
    def __init__(
        self,
        publishedfileid: int | None = ...,
        list_type: int | None = ...,
        appid: int | None = ...,
        notify_client: bool = ...,
    ) -> None: ...

class CPublishedFile_Unsubscribe_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPublishedFile_Publish_Request(_message.Message):
    __slots__ = (
        "appid",
        "consumer_appid",
        "cloudfilename",
        "preview_cloudfilename",
        "title",
        "file_description",
        "file_type",
        "consumer_shortcut_name",
        "youtube_username",
        "youtube_videoid",
        "visibility",
        "redirect_uri",
        "tags",
        "collection_type",
        "game_type",
        "url",
    )
    APPID_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_APPID_FIELD_NUMBER: _ClassVar[int]
    CLOUDFILENAME_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_CLOUDFILENAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    FILE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_SHORTCUT_NAME_FIELD_NUMBER: _ClassVar[int]
    YOUTUBE_USERNAME_FIELD_NUMBER: _ClassVar[int]
    YOUTUBE_VIDEOID_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    appid: int
    consumer_appid: int
    cloudfilename: str
    preview_cloudfilename: str
    title: str
    file_description: str
    file_type: int
    consumer_shortcut_name: str
    youtube_username: str
    youtube_videoid: str
    visibility: int
    redirect_uri: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    collection_type: str
    game_type: str
    url: str
    def __init__(
        self,
        appid: int | None = ...,
        consumer_appid: int | None = ...,
        cloudfilename: str | None = ...,
        preview_cloudfilename: str | None = ...,
        title: str | None = ...,
        file_description: str | None = ...,
        file_type: int | None = ...,
        consumer_shortcut_name: str | None = ...,
        youtube_username: str | None = ...,
        youtube_videoid: str | None = ...,
        visibility: int | None = ...,
        redirect_uri: str | None = ...,
        tags: _Iterable[str] | None = ...,
        collection_type: str | None = ...,
        game_type: str | None = ...,
        url: str | None = ...,
    ) -> None: ...

class CPublishedFile_Publish_Response(_message.Message):
    __slots__ = ("publishedfileid", "redirect_uri")
    PUBLISHEDFILEID_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    publishedfileid: int
    redirect_uri: str
    def __init__(
        self, publishedfileid: int | None = ..., redirect_uri: str | None = ...
    ) -> None: ...

class CPublishedFile_GetDetails_Request(_message.Message):
    __slots__ = (
        "publishedfileids",
        "includetags",
        "includeadditionalpreviews",
        "includechildren",
        "includekvtags",
        "includevotes",
        "short_description",
    )
    PUBLISHEDFILEIDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDETAGS_FIELD_NUMBER: _ClassVar[int]
    INCLUDEADDITIONALPREVIEWS_FIELD_NUMBER: _ClassVar[int]
    INCLUDECHILDREN_FIELD_NUMBER: _ClassVar[int]
    INCLUDEKVTAGS_FIELD_NUMBER: _ClassVar[int]
    INCLUDEVOTES_FIELD_NUMBER: _ClassVar[int]
    SHORT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    publishedfileids: _containers.RepeatedScalarFieldContainer[int]
    includetags: bool
    includeadditionalpreviews: bool
    includechildren: bool
    includekvtags: bool
    includevotes: bool
    short_description: bool
    def __init__(
        self,
        publishedfileids: _Iterable[int] | None = ...,
        includetags: bool = ...,
        includeadditionalpreviews: bool = ...,
        includechildren: bool = ...,
        includekvtags: bool = ...,
        includevotes: bool = ...,
        short_description: bool = ...,
    ) -> None: ...

class PublishedFileDetails(_message.Message):
    __slots__ = (
        "result",
        "publishedfileid",
        "creator",
        "creator_appid",
        "consumer_appid",
        "consumer_shortcutid",
        "filename",
        "file_size",
        "preview_file_size",
        "file_url",
        "preview_url",
        "youtubevideoid",
        "url",
        "hcontent_file",
        "hcontent_preview",
        "title",
        "file_description",
        "short_description",
        "time_created",
        "time_updated",
        "visibility",
        "flags",
        "workshop_file",
        "workshop_accepted",
        "show_subscribe_all",
        "num_comments_developer",
        "num_comments_public",
        "banned",
        "ban_reason",
        "banner",
        "can_be_deleted",
        "incompatible",
        "app_name",
        "file_type",
        "can_subscribe",
        "subscriptions",
        "favorited",
        "followers",
        "lifetime_subscriptions",
        "lifetime_favorited",
        "lifetime_followers",
        "views",
        "image_width",
        "image_height",
        "image_url",
        "spoiler_tag",
        "shortcutid",
        "shortcutname",
        "num_children",
        "num_reports",
        "previews",
        "tags",
        "children",
        "kvtags",
        "vote_data",
        "time_subscribed",
    )
    class Tag(_message.Message):
        __slots__ = ("tag", "adminonly")
        TAG_FIELD_NUMBER: _ClassVar[int]
        ADMINONLY_FIELD_NUMBER: _ClassVar[int]
        tag: str
        adminonly: bool
        def __init__(self, tag: str | None = ..., adminonly: bool = ...) -> None: ...

    class Preview(_message.Message):
        __slots__ = ("previewid", "sortorder", "url", "size", "filename", "youtubevideoid")
        PREVIEWID_FIELD_NUMBER: _ClassVar[int]
        SORTORDER_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        FILENAME_FIELD_NUMBER: _ClassVar[int]
        YOUTUBEVIDEOID_FIELD_NUMBER: _ClassVar[int]
        previewid: int
        sortorder: int
        url: str
        size: int
        filename: str
        youtubevideoid: str
        def __init__(
            self,
            previewid: int | None = ...,
            sortorder: int | None = ...,
            url: str | None = ...,
            size: int | None = ...,
            filename: str | None = ...,
            youtubevideoid: str | None = ...,
        ) -> None: ...

    class Child(_message.Message):
        __slots__ = ("publishedfileid", "sortorder", "file_type")
        PUBLISHEDFILEID_FIELD_NUMBER: _ClassVar[int]
        SORTORDER_FIELD_NUMBER: _ClassVar[int]
        FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
        publishedfileid: int
        sortorder: int
        file_type: int
        def __init__(
            self,
            publishedfileid: int | None = ...,
            sortorder: int | None = ...,
            file_type: int | None = ...,
        ) -> None: ...

    class KVTag(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: str | None = ..., value: str | None = ...) -> None: ...

    class VoteData(_message.Message):
        __slots__ = ("score", "votes_up", "votes_down")
        SCORE_FIELD_NUMBER: _ClassVar[int]
        VOTES_UP_FIELD_NUMBER: _ClassVar[int]
        VOTES_DOWN_FIELD_NUMBER: _ClassVar[int]
        score: float
        votes_up: int
        votes_down: int
        def __init__(
            self,
            score: float | None = ...,
            votes_up: int | None = ...,
            votes_down: int | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    PUBLISHEDFILEID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    CREATOR_APPID_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_APPID_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_SHORTCUTID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILE_URL_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_URL_FIELD_NUMBER: _ClassVar[int]
    YOUTUBEVIDEOID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    HCONTENT_FILE_FIELD_NUMBER: _ClassVar[int]
    HCONTENT_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    FILE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SHORT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TIME_CREATED_FIELD_NUMBER: _ClassVar[int]
    TIME_UPDATED_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    WORKSHOP_FILE_FIELD_NUMBER: _ClassVar[int]
    WORKSHOP_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    SHOW_SUBSCRIBE_ALL_FIELD_NUMBER: _ClassVar[int]
    NUM_COMMENTS_DEVELOPER_FIELD_NUMBER: _ClassVar[int]
    NUM_COMMENTS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    BANNED_FIELD_NUMBER: _ClassVar[int]
    BAN_REASON_FIELD_NUMBER: _ClassVar[int]
    BANNER_FIELD_NUMBER: _ClassVar[int]
    CAN_BE_DELETED_FIELD_NUMBER: _ClassVar[int]
    INCOMPATIBLE_FIELD_NUMBER: _ClassVar[int]
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CAN_SUBSCRIBE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    FAVORITED_FIELD_NUMBER: _ClassVar[int]
    FOLLOWERS_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_FAVORITED_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_FOLLOWERS_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    IMAGE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    SPOILER_TAG_FIELD_NUMBER: _ClassVar[int]
    SHORTCUTID_FIELD_NUMBER: _ClassVar[int]
    SHORTCUTNAME_FIELD_NUMBER: _ClassVar[int]
    NUM_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    NUM_REPORTS_FIELD_NUMBER: _ClassVar[int]
    PREVIEWS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    KVTAGS_FIELD_NUMBER: _ClassVar[int]
    VOTE_DATA_FIELD_NUMBER: _ClassVar[int]
    TIME_SUBSCRIBED_FIELD_NUMBER: _ClassVar[int]
    result: int
    publishedfileid: int
    creator: int
    creator_appid: int
    consumer_appid: int
    consumer_shortcutid: int
    filename: str
    file_size: int
    preview_file_size: int
    file_url: str
    preview_url: str
    youtubevideoid: str
    url: str
    hcontent_file: int
    hcontent_preview: int
    title: str
    file_description: str
    short_description: str
    time_created: int
    time_updated: int
    visibility: int
    flags: int
    workshop_file: bool
    workshop_accepted: bool
    show_subscribe_all: bool
    num_comments_developer: int
    num_comments_public: int
    banned: bool
    ban_reason: str
    banner: int
    can_be_deleted: bool
    incompatible: bool
    app_name: str
    file_type: int
    can_subscribe: bool
    subscriptions: int
    favorited: int
    followers: int
    lifetime_subscriptions: int
    lifetime_favorited: int
    lifetime_followers: int
    views: int
    image_width: int
    image_height: int
    image_url: str
    spoiler_tag: bool
    shortcutid: int
    shortcutname: str
    num_children: int
    num_reports: int
    previews: _containers.RepeatedCompositeFieldContainer[PublishedFileDetails.Preview]
    tags: _containers.RepeatedCompositeFieldContainer[PublishedFileDetails.Tag]
    children: _containers.RepeatedCompositeFieldContainer[PublishedFileDetails.Child]
    kvtags: _containers.RepeatedCompositeFieldContainer[PublishedFileDetails.KVTag]
    vote_data: PublishedFileDetails.VoteData
    time_subscribed: int
    def __init__(
        self,
        result: int | None = ...,
        publishedfileid: int | None = ...,
        creator: int | None = ...,
        creator_appid: int | None = ...,
        consumer_appid: int | None = ...,
        consumer_shortcutid: int | None = ...,
        filename: str | None = ...,
        file_size: int | None = ...,
        preview_file_size: int | None = ...,
        file_url: str | None = ...,
        preview_url: str | None = ...,
        youtubevideoid: str | None = ...,
        url: str | None = ...,
        hcontent_file: int | None = ...,
        hcontent_preview: int | None = ...,
        title: str | None = ...,
        file_description: str | None = ...,
        short_description: str | None = ...,
        time_created: int | None = ...,
        time_updated: int | None = ...,
        visibility: int | None = ...,
        flags: int | None = ...,
        workshop_file: bool = ...,
        workshop_accepted: bool = ...,
        show_subscribe_all: bool = ...,
        num_comments_developer: int | None = ...,
        num_comments_public: int | None = ...,
        banned: bool = ...,
        ban_reason: str | None = ...,
        banner: int | None = ...,
        can_be_deleted: bool = ...,
        incompatible: bool = ...,
        app_name: str | None = ...,
        file_type: int | None = ...,
        can_subscribe: bool = ...,
        subscriptions: int | None = ...,
        favorited: int | None = ...,
        followers: int | None = ...,
        lifetime_subscriptions: int | None = ...,
        lifetime_favorited: int | None = ...,
        lifetime_followers: int | None = ...,
        views: int | None = ...,
        image_width: int | None = ...,
        image_height: int | None = ...,
        image_url: str | None = ...,
        spoiler_tag: bool = ...,
        shortcutid: int | None = ...,
        shortcutname: str | None = ...,
        num_children: int | None = ...,
        num_reports: int | None = ...,
        previews: _Iterable[PublishedFileDetails.Preview | _Mapping] | None = ...,
        tags: _Iterable[PublishedFileDetails.Tag | _Mapping] | None = ...,
        children: _Iterable[PublishedFileDetails.Child | _Mapping] | None = ...,
        kvtags: _Iterable[PublishedFileDetails.KVTag | _Mapping] | None = ...,
        vote_data: PublishedFileDetails.VoteData | _Mapping | None = ...,
        time_subscribed: int | None = ...,
    ) -> None: ...

class CPublishedFile_GetDetails_Response(_message.Message):
    __slots__ = ("publishedfiledetails",)
    PUBLISHEDFILEDETAILS_FIELD_NUMBER: _ClassVar[int]
    publishedfiledetails: _containers.RepeatedCompositeFieldContainer[PublishedFileDetails]
    def __init__(
        self, publishedfiledetails: _Iterable[PublishedFileDetails | _Mapping] | None = ...
    ) -> None: ...

class CPublishedFile_GetUserFiles_Request(_message.Message):
    __slots__ = (
        "appid",
        "page",
        "numperpage",
        "sortmethod",
        "totalonly",
        "privacy",
        "ids_only",
        "requiredtags",
        "excludedtags",
    )
    APPID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    NUMPERPAGE_FIELD_NUMBER: _ClassVar[int]
    SORTMETHOD_FIELD_NUMBER: _ClassVar[int]
    TOTALONLY_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_FIELD_NUMBER: _ClassVar[int]
    IDS_ONLY_FIELD_NUMBER: _ClassVar[int]
    REQUIREDTAGS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDEDTAGS_FIELD_NUMBER: _ClassVar[int]
    appid: int
    page: int
    numperpage: int
    sortmethod: str
    totalonly: bool
    privacy: int
    ids_only: bool
    requiredtags: _containers.RepeatedScalarFieldContainer[str]
    excludedtags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        appid: int | None = ...,
        page: int | None = ...,
        numperpage: int | None = ...,
        sortmethod: str | None = ...,
        totalonly: bool = ...,
        privacy: int | None = ...,
        ids_only: bool = ...,
        requiredtags: _Iterable[str] | None = ...,
        excludedtags: _Iterable[str] | None = ...,
    ) -> None: ...

class CPublishedFile_GetUserFiles_Response(_message.Message):
    __slots__ = ("total", "startindex", "publishedfiledetails", "apps")
    class App(_message.Message):
        __slots__ = ("appid", "name", "shortcutid", "private")
        APPID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SHORTCUTID_FIELD_NUMBER: _ClassVar[int]
        PRIVATE_FIELD_NUMBER: _ClassVar[int]
        appid: int
        name: str
        shortcutid: int
        private: bool
        def __init__(
            self,
            appid: int | None = ...,
            name: str | None = ...,
            shortcutid: int | None = ...,
            private: bool = ...,
        ) -> None: ...

    TOTAL_FIELD_NUMBER: _ClassVar[int]
    STARTINDEX_FIELD_NUMBER: _ClassVar[int]
    PUBLISHEDFILEDETAILS_FIELD_NUMBER: _ClassVar[int]
    APPS_FIELD_NUMBER: _ClassVar[int]
    total: int
    startindex: int
    publishedfiledetails: _containers.RepeatedCompositeFieldContainer[PublishedFileDetails]
    apps: _containers.RepeatedCompositeFieldContainer[CPublishedFile_GetUserFiles_Response.App]
    def __init__(
        self,
        total: int | None = ...,
        startindex: int | None = ...,
        publishedfiledetails: _Iterable[PublishedFileDetails | _Mapping] | None = ...,
        apps: _Iterable[CPublishedFile_GetUserFiles_Response.App | _Mapping] | None = ...,
    ) -> None: ...

class CPublishedFile_Update_Request(_message.Message):
    __slots__ = (
        "appid",
        "publishedfileid",
        "title",
        "file_description",
        "visibility",
        "tags",
        "filename",
        "preview_filename",
    )
    APPID_FIELD_NUMBER: _ClassVar[int]
    PUBLISHEDFILEID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    FILE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FILENAME_FIELD_NUMBER: _ClassVar[int]
    appid: int
    publishedfileid: int
    title: str
    file_description: str
    visibility: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    filename: str
    preview_filename: str
    def __init__(
        self,
        appid: int | None = ...,
        publishedfileid: int | None = ...,
        title: str | None = ...,
        file_description: str | None = ...,
        visibility: int | None = ...,
        tags: _Iterable[str] | None = ...,
        filename: str | None = ...,
        preview_filename: str | None = ...,
    ) -> None: ...

class CPublishedFile_Update_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CPublishedFile_RefreshVotingQueue_Request(_message.Message):
    __slots__ = (
        "appid",
        "matching_file_type",
        "tags",
        "match_all_tags",
        "excluded_tags",
        "desired_queue_size",
    )
    APPID_FIELD_NUMBER: _ClassVar[int]
    MATCHING_FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    MATCH_ALL_TAGS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_TAGS_FIELD_NUMBER: _ClassVar[int]
    DESIRED_QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    appid: int
    matching_file_type: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    match_all_tags: bool
    excluded_tags: _containers.RepeatedScalarFieldContainer[str]
    desired_queue_size: int
    def __init__(
        self,
        appid: int | None = ...,
        matching_file_type: int | None = ...,
        tags: _Iterable[str] | None = ...,
        match_all_tags: bool = ...,
        excluded_tags: _Iterable[str] | None = ...,
        desired_queue_size: int | None = ...,
    ) -> None: ...

class CPublishedFile_RefreshVotingQueue_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
