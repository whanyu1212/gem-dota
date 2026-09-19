"""Tests for the Dota protobuf upstream watcher."""

from __future__ import annotations

import io
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from scripts import check_proto_updates

OLD_COMMIT = "1" * 40
OLD_TREE = "2" * 40
NEW_COMMIT = "3" * 40
NEW_TREE = "4" * 40


class _Response(io.BytesIO):
    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


def _lock_data() -> dict[str, object]:
    return {
        "schema_version": 1,
        "repository": "SteamTracking/Protobufs",
        "branch": "master",
        "path": "dota2",
        "commit": OLD_COMMIT,
        "tree": OLD_TREE,
    }


def _write_lock(lock_path: Path, **overrides: object) -> None:
    data = _lock_data()
    data.update(overrides)
    lock_path.write_text(json.dumps(data), encoding="utf-8")


def _mock_api(monkeypatch: pytest.MonkeyPatch, tree: str) -> list[object]:
    requests: list[object] = []

    def fake_urlopen(request: object, timeout: int) -> _Response:
        requests.append(request)
        assert timeout == 30
        url = request.full_url  # type: ignore[attr-defined]
        if "/commits?" in url:
            query = parse_qs(urlparse(url).query)
            assert query == {"sha": ["master"], "path": ["dota2"], "per_page": ["1"]}
            payload: object = [{"sha": NEW_COMMIT}]
        else:
            assert url.endswith(f"/git/trees/{NEW_COMMIT}")
            payload = {"truncated": False, "tree": [{"path": "dota2", "type": "tree", "sha": tree}]}
        return _Response(json.dumps(payload).encode())

    monkeypatch.setattr(check_proto_updates, "urlopen", fake_urlopen)
    return requests


def test_check_reports_unchanged_and_writes_outputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lock_path = tmp_path / "lock.json"
    output_path = tmp_path / "github-output"
    _write_lock(lock_path)
    requests = _mock_api(monkeypatch, OLD_TREE)
    monkeypatch.setenv("GITHUB_OUTPUT", str(output_path))
    monkeypatch.setenv("GITHUB_TOKEN", "secret-token")

    assert check_proto_updates.main(["--lock", str(lock_path), "--github-output"]) == 0

    outputs = dict(line.split("=", 1) for line in output_path.read_text().splitlines())
    assert outputs["changed"] == "false"
    assert outputs["commit"] == NEW_COMMIT
    assert outputs["tree"] == OLD_TREE
    assert outputs["compare_url"].endswith(f"/{OLD_COMMIT}...{NEW_COMMIT}")
    assert outputs["source_url"].endswith(f"/tree/{NEW_COMMIT}/dota2")
    assert len(requests) == 2
    assert requests[0].headers["Authorization"] == "Bearer secret-token"  # type: ignore[attr-defined]


def test_check_reports_changed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    lock_path = tmp_path / "lock.json"
    _write_lock(lock_path)
    _mock_api(monkeypatch, NEW_TREE)

    lock = check_proto_updates.load_lock(lock_path)
    upstream = check_proto_updates.resolve_upstream(lock)
    outputs = check_proto_updates.build_outputs(lock, upstream)

    assert outputs["changed"] == "true"
    assert outputs["old_commit"] == OLD_COMMIT
    assert outputs["old_tree"] == OLD_TREE
    assert outputs["commit_url"].endswith(f"/commit/{NEW_COMMIT}")


def test_update_lock_preserves_configuration(tmp_path: Path) -> None:
    lock_path = tmp_path / "lock.json"
    _write_lock(lock_path)

    assert (
        check_proto_updates.main(
            [
                "--lock",
                str(lock_path),
                "--update-lock",
                "--commit",
                NEW_COMMIT,
                "--tree",
                NEW_TREE,
            ]
        )
        == 0
    )

    updated = json.loads(lock_path.read_text())
    assert updated == {**_lock_data(), "commit": NEW_COMMIT, "tree": NEW_TREE}
    assert lock_path.read_text().endswith("\n")


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"schema_version": 2}, "schema_version"),
        ({"commit": "short"}, "40-character SHA"),
        ({"path": "../dota2"}, "normalized repository-relative path"),
        ({"repository": "missing-owner"}, "owner/name"),
    ],
)
def test_load_lock_rejects_malformed_values(
    tmp_path: Path, overrides: dict[str, object], message: str
) -> None:
    lock_path = tmp_path / "lock.json"
    _write_lock(lock_path, **overrides)

    with pytest.raises(check_proto_updates.ProtoUpdateError, match=message):
        check_proto_updates.load_lock(lock_path)


def test_resolve_upstream_rejects_truncated_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lock_path = tmp_path / "lock.json"
    _write_lock(lock_path)

    responses = iter(
        [
            [{"sha": NEW_COMMIT}],
            {"truncated": True, "tree": [{"path": "dota2", "type": "tree", "sha": NEW_TREE}]},
        ]
    )

    def fake_urlopen(request: object, timeout: int) -> _Response:
        return _Response(json.dumps(next(responses)).encode())

    monkeypatch.setattr(check_proto_updates, "urlopen", fake_urlopen)

    with pytest.raises(check_proto_updates.ProtoUpdateError, match="truncated"):
        check_proto_updates.resolve_upstream(check_proto_updates.load_lock(lock_path))


def test_github_outputs_reject_multiline_values(tmp_path: Path) -> None:
    with pytest.raises(check_proto_updates.ProtoUpdateError, match="single line"):
        check_proto_updates.write_github_outputs(tmp_path / "output", {"commit": "bad\nvalue"})
