from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import generate_proto_field_docs as gen


def _proto_imports() -> dict[str, list[str]]:
    return {
        path.name: gen.parse_proto(path.read_text(encoding="utf-8"), path.name).imports
        for path in sorted(gen.PROTO_SRC_DIR.glob("*.proto"))
    }


def test_used_and_loaded_sets_match_runtime_imports() -> None:
    """The atlas's used/loaded labels must match what Python actually loads."""
    imports = _proto_imports()
    used = gen.used_proto_files() & imports.keys()
    loaded = gen.loaded_proto_files(used, imports)

    # Import the used modules in a fresh interpreter so other tests' imports
    # don't leak into sys.modules.
    modules = [f"gem.proto.{name.removesuffix('.proto')}_pb2" for name in sorted(used)]
    code = (
        "import importlib, json, sys\n"
        f"for m in {modules!r}: importlib.import_module(m)\n"
        "print(json.dumps(sorted(m.DESCRIPTOR.name for n, m in sys.modules.items()"
        " if n.startswith('gem.proto.') and n.endswith('_pb2'))))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    runtime = set(json.loads(result.stdout))

    assert used, "expected gem to import at least one generated proto module"
    assert runtime == used | loaded.keys()


def test_parse_proto_reads_public_imports() -> None:
    doc = gen.parse_proto('import public "events.proto";\nimport "a.proto";\n', "x.proto")
    assert doc.imports == ["events.proto", "a.proto"]


def test_render_omits_missing_syntax_and_package(tmp_path: Path) -> None:
    doc = gen.parse_proto("message M {\n\toptional int32 a = 1;\n}\n", "x.proto")
    out = tmp_path / "x.md"
    gen.render_proto_page(doc, out, used={"x.proto"}, loaded={})
    text = out.read_text(encoding="utf-8")
    assert "Syntax:" not in text
    assert "Package:" not in text
    assert "**Used by gem**" in text


def test_loaded_files_record_their_importers() -> None:
    imports = {
        "used.proto": ["dep.proto"],
        "dep.proto": ["deeper.proto"],
        "deeper.proto": [],
        "other.proto": ["deeper.proto"],
    }
    assert gen.loaded_proto_files({"used.proto"}, imports) == {
        "dep.proto": ["used.proto"],
        "deeper.proto": ["dep.proto"],
    }
