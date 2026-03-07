"""
Tests for gem.stream — outer message reading and magic validation.

Reference: manta/parser.go (NewStreamParser, readOuterMessage)
"""

import pytest

MAGIC_S2 = b"PBDEMS2\x00"
MAGIC_S1 = b"PUFDEMSM\x00"  # intentionally wrong length, just for test


def _pack_varuint32(value: int) -> bytes:
    out = []
    while True:
        bits = value & 0x7F
        value >>= 7
        if value:
            out.append(bits | 0x80)
        else:
            out.append(bits)
            break
    return bytes(out)


def _build_dem(messages: list[tuple[int, int, bytes]]) -> bytes:
    """
    Build a minimal .dem binary blob.

    messages: list of (msg_type, tick, payload)
    """
    buf = bytearray()
    buf += MAGIC_S2
    buf += b"\x00" * 8  # size metadata

    for msg_type, tick, payload in messages:
        buf += _pack_varuint32(msg_type)
        buf += _pack_varuint32(tick)
        buf += _pack_varuint32(len(payload))
        buf += payload

    return bytes(buf)


@pytest.fixture
def stream_cls():
    from gem.stream import DemoStream

    return DemoStream


class TestMagicValidation:
    def test_valid_magic_accepted(self, stream_cls):
        data = _build_dem([])
        stream_cls(data)  # should not raise

    def test_invalid_magic_raises(self, stream_cls):
        bad = b"BADMAGIC" + b"\x00" * 8
        with pytest.raises(Exception, match="magic"):
            stream_cls(bad)

    def test_source1_magic_raises(self, stream_cls):
        bad = b"PUFDEMSM" + b"\x00" * 8
        with pytest.raises(Exception, match="magic"):
            stream_cls(bad)


class TestOuterMessages:
    def test_empty_stream_yields_nothing(self, stream_cls):
        data = _build_dem([])
        s = stream_cls(data)
        messages = list(s)
        assert messages == []

    def test_single_message_tick_and_type(self, stream_cls):
        payload = b"\x01\x02\x03"
        data = _build_dem([(5, 100, payload)])
        s = stream_cls(data)
        messages = list(s)
        assert len(messages) == 1
        tick, msg_type, msg_data = messages[0]
        assert tick == 100
        assert msg_type == 5
        assert msg_data == payload

    def test_multiple_messages_ordered(self, stream_cls):
        data = _build_dem(
            [
                (1, 0, b"\xaa"),
                (2, 10, b"\xbb"),
                (3, 20, b"\xcc"),
            ]
        )
        s = stream_cls(data)
        messages = list(s)
        assert len(messages) == 3
        assert messages[0][0] == 0  # tick
        assert messages[1][0] == 10
        assert messages[2][0] == 20

    def test_pregame_tick_treated_as_zero(self, stream_cls):
        # tick 0xFFFFFFFF is pre-game, should be returned as 0
        data = _build_dem([(1, 0xFFFFFFFF, b"\x00")])
        s = stream_cls(data)
        messages = list(s)
        tick, _, _ = messages[0]
        assert tick == 0

    def test_empty_payload(self, stream_cls):
        data = _build_dem([(7, 5, b"")])
        s = stream_cls(data)
        messages = list(s)
        assert len(messages) == 1
        _, _, msg_data = messages[0]
        assert msg_data == b""


class TestSnappyDecompression:
    def test_uncompressed_message(self, stream_cls):
        payload = b"hello world"
        data = _build_dem([(1, 0, payload)])
        s = stream_cls(data)
        _, _, msg_data = list(s)[0]
        assert msg_data == payload

    def test_snappy_compressed_message(self, stream_cls):
        try:
            import snappy as _snappy
        except ImportError:
            pytest.skip("python-snappy not installed")

        payload = b"hello world" * 100
        compressed = _snappy.compress(payload)

        # DEM_IsCompressed flag = 64 (0x40) ORed into msg_type
        DEM_IsCompressed = 64
        msg_type = 1 | DEM_IsCompressed

        buf = bytearray()
        buf += MAGIC_S2
        buf += b"\x00" * 8
        buf += _pack_varuint32(msg_type)
        buf += _pack_varuint32(0)
        buf += _pack_varuint32(len(compressed))
        buf += compressed

        s = stream_cls(bytes(buf))
        _, _, msg_data = list(s)[0]
        assert msg_data == payload
