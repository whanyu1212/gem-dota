"""Tests for replay download helpers."""

from __future__ import annotations

import bz2
import contextlib
import io
import ssl
from pathlib import Path

from gem.replays import fetch


def test_replay_fetch_tls_context_verifies_certificates() -> None:
    assert fetch._SSL_CONTEXT.verify_mode == ssl.CERT_REQUIRED
    assert fetch._SSL_CONTEXT.check_hostname is True


def test_download_and_decompress_uses_verified_tls_context(
    tmp_path: Path,
    monkeypatch,
) -> None:
    payload = bz2.compress(b"demo-bytes")
    contexts: list[ssl.SSLContext] = []

    @contextlib.contextmanager
    def fake_urlopen(*_args, **kwargs):
        contexts.append(kwargs["context"])
        yield io.BytesIO(payload)

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)

    dem_path = fetch.download_and_decompress(123, "https://example.invalid/123.dem.bz2", tmp_path)

    assert dem_path == tmp_path / "123.dem"
    assert dem_path.read_bytes() == b"demo-bytes"
    assert not (tmp_path / "123.dem.bz2").exists()
    assert len(contexts) == 1
    assert contexts[0].verify_mode == ssl.CERT_REQUIRED
    assert contexts[0].check_hostname is True
