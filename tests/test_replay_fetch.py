"""Tests for replay archive decompression (gem/replays/fetch.py)."""

from __future__ import annotations

import bz2

import pytest
import zstandard

from gem.replays.fetch import _decompress_replay

PAYLOAD = b"PBDEMS2\x00" + b"replay bytes" * 1000


def test_decompresses_bzip2_archive():
    assert _decompress_replay(bz2.compress(PAYLOAD)) == PAYLOAD


def test_decompresses_zstandard_archive():
    """Valve serves zstd under the .bz2 extension for post-July-2026 replays (#137)."""
    assert _decompress_replay(zstandard.ZstdCompressor().compress(PAYLOAD)) == PAYLOAD


def test_rejects_unknown_format():
    with pytest.raises(RuntimeError, match="neither bzip2 nor Zstandard"):
        _decompress_replay(b"not a compressed archive at all")
