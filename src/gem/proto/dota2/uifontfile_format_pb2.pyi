from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CUIFontFilePB(_message.Message):
    __slots__ = ("font_file_name", "opentype_font_data")
    FONT_FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    OPENTYPE_FONT_DATA_FIELD_NUMBER: _ClassVar[int]
    font_file_name: str
    opentype_font_data: bytes
    def __init__(
        self, font_file_name: str | None = ..., opentype_font_data: bytes | None = ...
    ) -> None: ...

class CUIFontFilePackagePB(_message.Message):
    __slots__ = ("package_version", "encrypted_font_files")
    class CUIEncryptedFontFilePB(_message.Message):
        __slots__ = ("encrypted_contents",)
        ENCRYPTED_CONTENTS_FIELD_NUMBER: _ClassVar[int]
        encrypted_contents: bytes
        def __init__(self, encrypted_contents: bytes | None = ...) -> None: ...

    PACKAGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FONT_FILES_FIELD_NUMBER: _ClassVar[int]
    package_version: int
    encrypted_font_files: _containers.RepeatedCompositeFieldContainer[
        CUIFontFilePackagePB.CUIEncryptedFontFilePB
    ]
    def __init__(
        self,
        package_version: int | None = ...,
        encrypted_font_files: _Iterable[CUIFontFilePackagePB.CUIEncryptedFontFilePB | _Mapping]
        | None = ...,
    ) -> None: ...
