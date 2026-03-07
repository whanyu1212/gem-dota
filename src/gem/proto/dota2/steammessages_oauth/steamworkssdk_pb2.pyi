from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class COAuthToken_ImplicitGrantNoPrompt_Request(_message.Message):
    __slots__ = ("clientid",)
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    clientid: str
    def __init__(self, clientid: str | None = ...) -> None: ...

class COAuthToken_ImplicitGrantNoPrompt_Response(_message.Message):
    __slots__ = ("access_token", "redirect_uri")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    redirect_uri: str
    def __init__(self, access_token: str | None = ..., redirect_uri: str | None = ...) -> None: ...
