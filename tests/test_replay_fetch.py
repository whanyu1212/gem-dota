"""Tests for replay download helpers."""

from __future__ import annotations

import bz2
import contextlib
import io
import json
import ssl
from pathlib import Path

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
