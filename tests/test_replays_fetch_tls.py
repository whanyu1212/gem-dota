"""TLS verification for the OpenDota and replay requests in ``gem.replays.fetch``."""

from __future__ import annotations

import contextlib
import io
import ssl
import sys
import types
import urllib.error
from pathlib import Path

import pytest

from gem.replays import fetch


def test_module_context_verifies_certificates_and_hostnames() -> None:
    assert fetch._SSL_CONTEXT.verify_mode == ssl.CERT_REQUIRED
    assert fetch._SSL_CONTEXT.check_hostname is True


def test_ssl_context_verifies_certificates_and_hostnames() -> None:
    ctx = fetch._ssl_context()

    assert ctx.verify_mode == ssl.CERT_REQUIRED
    assert ctx.check_hostname is True


def test_ssl_context_adds_certifi_roots_when_installed(tmp_path: Path, monkeypatch) -> None:
    cafile = tmp_path / "cacert.pem"
    cafile.write_text("", encoding="utf-8")
    loaded: list[object] = []
    monkeypatch.setitem(sys.modules, "certifi", types.SimpleNamespace(where=lambda: str(cafile)))
    monkeypatch.setattr(
        ssl.SSLContext,
        "load_verify_locations",
        lambda self, cafile=None, capath=None, cadata=None: loaded.append(cafile),
    )

    ctx = fetch._ssl_context()

    assert loaded == [str(cafile)]
    assert ctx.verify_mode == ssl.CERT_REQUIRED
    assert ctx.check_hostname is True


def test_ssl_context_works_without_certifi(monkeypatch) -> None:
    # A None entry makes ``import certifi`` raise ImportError.
    monkeypatch.setitem(sys.modules, "certifi", None)

    ctx = fetch._ssl_context()

    assert ctx.verify_mode == ssl.CERT_REQUIRED
    assert ctx.check_hostname is True


def test_requests_pass_the_verifying_context(monkeypatch) -> None:
    contexts: list[object] = []

    @contextlib.contextmanager
    def fake_urlopen(_req, *, context, timeout):
        contexts.append(context)
        yield io.BytesIO(b'{"replay_url": "http://replay1.valve.net/570/1_2.dem.bz2"}')

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)

    fetch.fetch_replay_url(1)
    fetch.fetch_opendota_match(1)

    assert contexts == [fetch._SSL_CONTEXT, fetch._SSL_CONTEXT]


def _raise_cert_error(*_args, **_kwargs):
    raise urllib.error.URLError(
        ssl.SSLCertVerificationError(1, "certificate verify failed: unable to get local issuer")
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda tmp_path: fetch.fetch_replay_url(1),
        lambda tmp_path: fetch.fetch_opendota_match(1),
        lambda tmp_path: fetch.download_and_decompress(
            1, "https://example.test/1.dem.bz2", tmp_path
        ),
    ],
    ids=["fetch_replay_url", "fetch_opendota_match", "download_and_decompress"],
)
def test_certificate_failure_raises_url_error_with_hint(call, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(fetch.urllib.request, "urlopen", _raise_cert_error)

    with pytest.raises(urllib.error.URLError) as excinfo:
        call(tmp_path)

    message = str(excinfo.value)
    assert "certificate verify failed" in message
    assert "Install Certificates.command" in message
    assert "pip install certifi" in message
    assert isinstance(excinfo.value.__cause__, urllib.error.URLError)
    assert not (tmp_path / "1.dem.bz2").exists()


def test_other_url_errors_propagate_unchanged(monkeypatch) -> None:
    original = urllib.error.URLError("connection refused")

    def fake_urlopen(*_args, **_kwargs):
        raise original

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)

    with pytest.raises(urllib.error.URLError) as excinfo:
        fetch.fetch_replay_url(1)

    assert excinfo.value is original
