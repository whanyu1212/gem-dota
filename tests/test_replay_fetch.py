"""Tests for replay download helpers."""

from __future__ import annotations

import bz2
import contextlib
import io
import json
import ssl
import stat
from pathlib import Path

import pytest

from gem.replays import fetch


def test_replay_fetch_tls_context_verifies_certificates() -> None:
    assert fetch._SSL_CONTEXT.verify_mode == ssl.CERT_REQUIRED
    assert fetch._SSL_CONTEXT.check_hostname is True


def test_normalize_replay_url_upgrades_valve_http_urls() -> None:
    assert (
        fetch._normalize_replay_url("http://replay274.valve.net/570/123.dem.bz2")
        == "https://replay274.valve.net/570/123.dem.bz2"
    )


def test_normalize_replay_url_rejects_non_https_non_valve_urls() -> None:
    try:
        fetch._normalize_replay_url("http://example.invalid/123.dem.bz2")
    except ValueError as exc:
        assert "must use HTTPS" in str(exc)
    else:  # pragma: no cover - defensive assertion for readability
        raise AssertionError("expected ValueError")


def test_fetch_replay_url_returns_https_for_opendota_valve_http_url(monkeypatch) -> None:
    body = json.dumps({"replay_url": "http://replay274.valve.net/570/123_456.dem.bz2"}).encode()

    @contextlib.contextmanager
    def fake_urlopen(*_args, **_kwargs):
        yield io.BytesIO(body)

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)

    assert fetch.fetch_replay_url(123) == "https://replay274.valve.net/570/123_456.dem.bz2"


class _ChunkedResponse(io.BytesIO):
    """BytesIO response that records bounded reads from the decompressor."""

    def __init__(self, data: bytes, *, chunk_size: int = 17) -> None:
        super().__init__(data)
        self.chunk_size = chunk_size
        self.read_sizes: list[int] = []

    def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)
        size = self.chunk_size if size < 0 else min(size, self.chunk_size)
        return super().read(size)


def test_download_and_decompress_uses_verified_tls_context(
    tmp_path: Path,
    monkeypatch,
) -> None:
    payload = bz2.compress(b"demo-bytes")
    contexts: list[ssl.SSLContext] = []
    urls: list[str] = []

    @contextlib.contextmanager
    def fake_urlopen(request, **kwargs):
        urls.append(request.full_url)
        contexts.append(kwargs["context"])
        yield io.BytesIO(payload)

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)

    dem_path = fetch.download_and_decompress(
        123,
        "http://replay274.valve.net/570/123.dem.bz2",
        tmp_path,
    )

    assert urls == ["https://replay274.valve.net/570/123.dem.bz2"]

    assert dem_path == tmp_path / "123.dem"
    assert dem_path.read_bytes() == b"demo-bytes"
    assert not (tmp_path / "123.dem.bz2").exists()
    assert len(contexts) == 1
    assert contexts[0].verify_mode == ssl.CERT_REQUIRED
    assert contexts[0].check_hostname is True


def test_download_and_decompress_streams_bz2_response(tmp_path: Path, monkeypatch) -> None:
    payload = bz2.compress(b"demo-bytes" * 4096)
    response = _ChunkedResponse(payload)

    @contextlib.contextmanager
    def fake_urlopen(*_args, **_kwargs):
        yield response

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(fetch, "_default_replay_file_mode", lambda: 0o664)

    dem_path = fetch.download_and_decompress(
        456,
        "https://replay274.valve.net/570/456.dem.bz2",
        tmp_path,
    )

    assert dem_path.read_bytes() == b"demo-bytes" * 4096
    assert response.read_sizes
    assert all(size != -1 for size in response.read_sizes)
    assert stat.S_IMODE(dem_path.stat().st_mode) == 0o664
    assert not (tmp_path / "456.dem.bz2").exists()


def test_download_and_decompress_preserves_existing_file_mode_on_replace(
    tmp_path: Path,
    monkeypatch,
) -> None:
    payload = bz2.compress(b"replacement replay")
    dem_path = tmp_path / "654.dem"
    dem_path.write_bytes(b"existing replay")
    dem_path.chmod(0o640)

    @contextlib.contextmanager
    def fake_urlopen(*_args, **_kwargs):
        yield io.BytesIO(payload)

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)

    result = fetch.download_and_decompress(
        654,
        "https://replay274.valve.net/570/654.dem.bz2",
        tmp_path,
    )

    assert result == dem_path
    assert dem_path.read_bytes() == b"replacement replay"
    assert stat.S_IMODE(dem_path.stat().st_mode) == 0o640


def test_download_and_decompress_cleans_temp_and_preserves_existing_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    dem_path = tmp_path / "789.dem"
    dem_path.write_bytes(b"existing replay")
    dem_path.chmod(0o640)

    @contextlib.contextmanager
    def fake_urlopen(*_args, **_kwargs):
        yield io.BytesIO(b"not a bzip2 stream")

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)

    with pytest.raises((EOFError, OSError)):
        fetch.download_and_decompress(
            789,
            "https://replay274.valve.net/570/789.dem.bz2",
            tmp_path,
        )

    assert dem_path.read_bytes() == b"existing replay"
    assert stat.S_IMODE(dem_path.stat().st_mode) == 0o640
    assert not (tmp_path / "789.dem.bz2").exists()
    assert list(tmp_path.glob(".789.dem.*.tmp")) == []
