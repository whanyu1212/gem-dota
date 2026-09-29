"""Tests for the per-interpreter protobuf import check."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts import check_proto_imports

_CONFLICT = "TypeError(\"Couldn't build proto file into descriptor pool: duplicate symbol 'x'\")"


def _package(tmp_path: Path, modules: dict[str, str]) -> Path:
    """Write ``src/pkg/proto`` with the given ``*_pb2`` module bodies."""
    proto_root = tmp_path / "src" / "pkg" / "proto"
    (proto_root / "sub").mkdir(parents=True)
    for init in (proto_root.parent, proto_root, proto_root / "sub"):
        (init / "__init__.py").write_text("")
    (proto_root / "helpers.py").write_text("raise RuntimeError('not a binding')\n")
    for name, body in modules.items():
        (proto_root / f"{name}.py").write_text(body)
    return proto_root


def test_discovers_only_generated_modules_including_subpackages(tmp_path):
    proto_root = _package(tmp_path, {"ok_pb2": ""})
    (proto_root / "sub" / "nested_pb2.py").write_text("")

    assert check_proto_imports.discover_modules(proto_root) == [
        "pkg.proto.ok_pb2",
        "pkg.proto.sub.nested_pb2",
    ]


def test_reports_modules_that_fail_to_import(tmp_path):
    proto_root = _package(tmp_path, {"ok_pb2": "", "bad_pb2": "raise ValueError('boom')\n"})

    assert check_proto_imports.check(proto_root) == {"pkg.proto.bad_pb2": "ValueError: boom"}


def test_known_conflict_passes_only_with_its_expected_error(tmp_path, monkeypatch):
    proto_root = _package(
        tmp_path,
        {"conflict_pb2": f"raise {_CONFLICT}\n", "other_pb2": f"raise {_CONFLICT}\n"},
    )
    monkeypatch.setattr(
        check_proto_imports,
        "KNOWN_CONFLICTS",
        {"pkg.proto.conflict_pb2": "Couldn't build proto file into descriptor pool: duplicate"},
    )

    failures = check_proto_imports.check(proto_root)

    assert list(failures) == ["pkg.proto.other_pb2"]


def test_known_conflict_with_a_different_error_still_fails(tmp_path, monkeypatch):
    proto_root = _package(tmp_path, {"conflict_pb2": "raise ImportError('missing dep')\n"})
    monkeypatch.setattr(
        check_proto_imports,
        "KNOWN_CONFLICTS",
        {"pkg.proto.conflict_pb2": "Couldn't build proto file into descriptor pool: duplicate"},
    )

    assert check_proto_imports.check(proto_root) == {
        "pkg.proto.conflict_pb2": "ImportError: missing dep"
    }


def test_main_fails_when_no_bindings_exist(tmp_path, capsys):
    proto_root = _package(tmp_path, {})

    assert check_proto_imports.main(["--proto-root", str(proto_root)]) == 1
    assert "No generated" in capsys.readouterr().err


@pytest.mark.slow
def test_committed_bindings_pass():
    assert check_proto_imports.check(check_proto_imports.DEFAULT_PROTO_ROOT) == {}
