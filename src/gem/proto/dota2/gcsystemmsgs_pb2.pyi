from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ESOMsg(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ESOMsg_Create: _ClassVar[ESOMsg]
    k_ESOMsg_Update: _ClassVar[ESOMsg]
    k_ESOMsg_Destroy: _ClassVar[ESOMsg]
    k_ESOMsg_CacheSubscribed: _ClassVar[ESOMsg]
    k_ESOMsg_CacheUnsubscribed: _ClassVar[ESOMsg]
    k_ESOMsg_UpdateMultiple: _ClassVar[ESOMsg]
    k_ESOMsg_CacheSubscriptionRefresh: _ClassVar[ESOMsg]
    k_ESOMsg_CacheSubscribedUpToDate: _ClassVar[ESOMsg]

class EGCBaseClientMsg(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMsgGCPingRequest: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCPingResponse: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCToClientPollConvarRequest: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCToClientPollConvarResponse: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCCompressedMsgToClient: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCCompressedMsgToClient_Legacy: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCToClientRequestDropped: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCClientWelcome: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCServerWelcome: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCClientHello: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCServerHello: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCClientConnectionStatus: _ClassVar[EGCBaseClientMsg]
    k_EMsgGCServerConnectionStatus: _ClassVar[EGCBaseClientMsg]

k_ESOMsg_Create: ESOMsg
k_ESOMsg_Update: ESOMsg
k_ESOMsg_Destroy: ESOMsg
k_ESOMsg_CacheSubscribed: ESOMsg
k_ESOMsg_CacheUnsubscribed: ESOMsg
k_ESOMsg_UpdateMultiple: ESOMsg
k_ESOMsg_CacheSubscriptionRefresh: ESOMsg
k_ESOMsg_CacheSubscribedUpToDate: ESOMsg
k_EMsgGCPingRequest: EGCBaseClientMsg
k_EMsgGCPingResponse: EGCBaseClientMsg
k_EMsgGCToClientPollConvarRequest: EGCBaseClientMsg
k_EMsgGCToClientPollConvarResponse: EGCBaseClientMsg
k_EMsgGCCompressedMsgToClient: EGCBaseClientMsg
k_EMsgGCCompressedMsgToClient_Legacy: EGCBaseClientMsg
k_EMsgGCToClientRequestDropped: EGCBaseClientMsg
k_EMsgGCClientWelcome: EGCBaseClientMsg
k_EMsgGCServerWelcome: EGCBaseClientMsg
k_EMsgGCClientHello: EGCBaseClientMsg
k_EMsgGCServerHello: EGCBaseClientMsg
k_EMsgGCClientConnectionStatus: EGCBaseClientMsg
k_EMsgGCServerConnectionStatus: EGCBaseClientMsg
