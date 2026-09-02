"""Tests for protobuf binding generation helpers."""

from pathlib import Path

from scripts.compile_protos import fix_relative_imports


def test_fix_relative_imports_rewrites_public_imports_at_each_depth(tmp_path: Path) -> None:
    """Public imports must resolve from generated modules inside ``gem.proto``."""
    top_level = tmp_path / "dota_shared_enums_pb2.py"
    top_level.write_text("from events_pb2 import *\n", encoding="utf-8")

    subpackage = tmp_path / "nested"
    subpackage.mkdir()
    nested = subpackage / "consumer_pb2.pyi"
    nested.write_text("from events_pb2 import *\n", encoding="utf-8")

    assert fix_relative_imports(tmp_path) == 2
    assert top_level.read_text(encoding="utf-8") == "from .events_pb2 import *\n"
    assert nested.read_text(encoding="utf-8") == "from ..events_pb2 import *\n"

    assert fix_relative_imports(tmp_path) == 0


def test_shared_enums_reexports_moved_event_enum() -> None:
    """The upstream public import preserves the historical generated API path."""
    from gem.proto import dota_shared_enums_pb2, events_pb2

    assert dota_shared_enums_pb2.EEvent is events_pb2.EEvent
    assert (
        dota_shared_enums_pb2.EVENT_ID_INTERNATIONAL_2026 == events_pb2.EVENT_ID_INTERNATIONAL_2026
    )
