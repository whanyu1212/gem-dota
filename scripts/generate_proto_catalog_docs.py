"""Generate the high-level VitePress catalog for Dota 2 proto declarations."""

from __future__ import annotations

import re
from pathlib import Path

from generate_proto_field_docs import (
    _flatten_enums,
    _flatten_messages,
    _module_leaf,
    _slug,
    parse_proto,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
PROTO_SRC_DIR = REPO_ROOT / "proto_definitions" / "dota2"
PROTO_OUT_DIR = REPO_ROOT / "src" / "gem" / "proto"
OUT_PATH = REPO_ROOT / "docs" / "cookbook" / "proto-dota2-catalog.md"

_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_DECL_RE = re.compile(r"^\s*(message|enum)\s+([A-Za-z_][A-Za-z0-9_]*)\b")


def _strip_block_comments_preserving_lines(text: str) -> str:
    return _BLOCK_COMMENT_RE.sub(lambda match: "\n" * match.group(0).count("\n"), text)


def _source_declarations(text: str) -> list[tuple[int, str, str]]:
    text = _strip_block_comments_preserving_lines(text)
    declarations: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        line = line.split("//", 1)[0]
        match = _DECL_RE.match(line)
        if match:
            kind, name = match.groups()
            declarations.append((lineno, kind, name))
    return declarations


def _render_imports(imports: list[str]) -> str:
    if not imports:
        return "*(none)*"
    return ", ".join(imports)


def main() -> None:
    proto_files = sorted(PROTO_SRC_DIR.glob("*.proto"))
    if not proto_files:
        raise RuntimeError(f"No proto files found under {PROTO_SRC_DIR}")

    generated_modules = sorted(PROTO_OUT_DIR.rglob("*_pb2.py"))

    docs = []
    for proto_path in proto_files:
        text = proto_path.read_text(encoding="utf-8", errors="replace")
        doc = parse_proto(text, proto_path.name)
        messages = _flatten_messages(doc.messages)
        enums = _flatten_enums(doc.enums, doc.messages)
        docs.append((proto_path, doc, messages, enums, _source_declarations(text)))

    lines: list[str] = [
        "# Full Proto Dota2 Catalog",
        "",
        "This page catalogs the full Dota 2 proto surface used by gem.",
        "",
        f"- Source proto files: **{len(proto_files)}**",
        f"- Generated Python protobuf modules (`*_pb2.py`, including subdirectories): **{len(generated_modules)}**",
        "",
        "## Index",
        "",
        "Use this list to jump directly to a file section:",
        "",
    ]

    for proto_path, doc, messages, enums, _declarations in docs:
        lines.append(
            f"- [{proto_path.name}](#{_slug(proto_path.name)}) — imports: {len(doc.imports)}, "
            f"enums: {len(enums)}, messages: {len(messages)}"
        )

    lines.extend(
        [
            "",
            "## Per-file declarations",
            "",
            "Each file is collapsed by default. Expand to view its declarations.",
            "",
        ]
    )

    for proto_path, doc, messages, enums, declarations in docs:
        lines.extend(
            [
                f'<a id="{_slug(proto_path.name)}"></a>',
                f"### {proto_path.name}",
                "",
                "<details>",
                (
                    f"<summary><code>{proto_path.name}</code> — module: "
                    f"<code>{_module_leaf(proto_path.name)}</code>; imports: {len(doc.imports)}; "
                    f"enums: {len(enums)}; messages: {len(messages)}</summary>"
                ),
                "",
                f"- Imports: {_render_imports(doc.imports)}",
                "",
                "```text",
            ]
        )
        for lineno, kind, name in declarations:
            lines.append(f"{lineno}: {kind} {name}")
        lines.extend(["```", "", "</details>", ""])

    OUT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Generated proto catalog at {OUT_PATH}")


if __name__ == "__main__":
    main()
