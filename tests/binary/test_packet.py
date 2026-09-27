"""Tests for gem.binary.packet — inner-message framing in CDemoPacket.data.

Reference: dotabuff/manta demo_packet.go (onCDemoPacket)
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from gem.binary.packet import read_inner_messages
from gem.binary.reader import BitReader, BufferReadError
from tests._bitstream import make_inner_blob


class TestReadInnerMessages:
    def test_empty_data_returns_empty_list(self):
        assert read_inner_messages(b"") == []

    def test_single_message(self):
        payload = b"\x01\x02\x03"
        blob = make_inner_blob([(4, payload)])
        result = read_inner_messages(blob)
        assert len(result) == 1
        assert result[0] == (4, payload)

    def test_multiple_messages_in_order(self):
        msgs = [(4, b"tick"), (44, b"create"), (55, b"entities")]
        blob = make_inner_blob(msgs)
        result = read_inner_messages(blob)
        assert len(result) == 3
        assert result[0][0] == 4
        assert result[1][0] == 44
        assert result[2][0] == 55

    def test_payload_content_preserved(self):
        payload = bytes(range(20))
        blob = make_inner_blob([(99, payload)])
        result = read_inner_messages(blob)
        assert result[0][1] == payload

    def test_empty_payload(self):
        blob = make_inner_blob([(4, b"")])
        result = read_inner_messages(blob)
        assert len(result) == 1
        assert result[0] == (4, b"")

    def test_fast_read_bytes_matches_slow_fallback_for_inner_messages(self):
        msgs = [
            (4, b"tick"),
            (44, bytes(range(64))),
            (55, bytes((i * 13 + 7) & 0xFF for i in range(300))),
            (554, b"combat-log-entry"),
        ]
        blob = make_inner_blob(msgs)

        fast_result = read_inner_messages(blob)
        with patch.object(BitReader, "read_bytes", BitReader._read_bytes_slow):
            slow_result = read_inner_messages(blob)

        assert fast_result == slow_result == msgs

    def test_truncated_payload_raises(self):
        blob = make_inner_blob([(4, b"abcdef")])[:-2]
        with pytest.raises(BufferReadError):
            read_inner_messages(blob)
