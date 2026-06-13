from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CUIFontFilePB(_message.Message):
    __slots__ = ("font_file_name", "opentype_font_data")
    FONT_FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    OPENTYPE_FONT_DATA_FIELD_NUMBER: _ClassVar[int]
    font_file_name: str
    opentype_font_data: bytes
    def __init__(self, font_file_name: _Optional[str] = ..., opentype_font_data: _Optional[bytes] = ...) -> None: ...

class CUIFontFilePackagePB(_message.Message):
    __slots__ = ("package_version", "encrypted_font_files")
    class CUIEncryptedFontFilePB(_message.Message):
        __slots__ = ("encrypted_contents",)
        ENCRYPTED_CONTENTS_FIELD_NUMBER: _ClassVar[int]
        encrypted_contents: bytes
        def __init__(self, encrypted_contents: _Optional[bytes] = ...) -> None: ...
    PACKAGE_VERSION_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FONT_FILES_FIELD_NUMBER: _ClassVar[int]
    package_version: int
    encrypted_font_files: _containers.RepeatedCompositeFieldContainer[CUIFontFilePackagePB.CUIEncryptedFontFilePB]
    def __init__(self, package_version: _Optional[int] = ..., encrypted_font_files: _Optional[_Iterable[_Union[CUIFontFilePackagePB.CUIEncryptedFontFilePB, _Mapping]]] = ...) -> None: ...
