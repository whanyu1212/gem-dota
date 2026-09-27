"""Inner net-message framing inside a ``CDemoPacket``.

``DEM_Packet``, ``DEM_SignonPacket``, and ``DEM_FullPacket`` envelopes each carry
a ``CDemoPacket`` whose ``data`` field is not one protobuf message but a packed
run of inner messages:

    ubit_var   message type ID (SVC_Messages / NET_Messages / user messages ...)
    varuint32  payload length in bytes
    bytes      protobuf payload

This module only splits that run into ``(type_id, payload)`` pairs. Choosing a
protobuf class per type ID, and ordering messages within a packet, is the
parser's job.

Reference: dotabuff/manta demo_packet.go (``onCDemoPacket``; pinned revision in
CLAUDE.md)
"""

from __future__ import annotations

from gem.binary.reader import BitReader


def read_inner_messages(data: bytes) -> list[tuple[int, bytes]]:
    """Split a ``CDemoPacket.data`` blob into its inner messages.

    Args:
        data: The raw bytes of ``CDemoPacket.data``.

    Returns:
        ``(type_id, payload)`` pairs in stream order.

    Raises:
        BufferReadError: If the blob ends in the middle of a message.
    """
    r = BitReader(data)
    messages: list[tuple[int, bytes]] = []
    while r.rem_bits() >= 8:
        type_id = r.read_ubit_var()
        size = r.read_varuint32()
        payload = r.read_bytes(size)
        messages.append((type_id, payload))
    return messages
