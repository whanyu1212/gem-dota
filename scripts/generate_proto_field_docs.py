"""Generate field-level VitePress docs for all Dota 2 proto files.

This parser reads source .proto files directly (not generated Python descriptors),
then writes readable docs with collapsible message/enum sections.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROTO_SRC_DIR = REPO_ROOT / "proto_definitions" / "dota2"
OUT_DIR = REPO_ROOT / "docs" / "cookbook" / "proto-fields"


@dataclass
class ProtoField:
    name: str
    type_name: str
    tag: int
    label: str
    oneof: str = ""
    notes: str = ""


@dataclass
class ProtoEnumValue:
    name: str
    number: int


@dataclass
class ProtoEnum:
    name: str
    full_name: str
    values: list[ProtoEnumValue] = field(default_factory=list)
    parent: str = ""


@dataclass
class ProtoMessage:
    name: str
    full_name: str
    fields: list[ProtoField] = field(default_factory=list)
    nested_messages: list[ProtoMessage] = field(default_factory=list)
    nested_enums: list[ProtoEnum] = field(default_factory=list)
    oneofs: list[str] = field(default_factory=list)
    parent: str = ""


@dataclass
class ProtoDoc:
    file_name: str
    syntax: str
    package: str
    imports: list[str]
    messages: list[ProtoMessage]
    enums: list[ProtoEnum]


_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_SYNTAX_RE = re.compile(r'^syntax\s*=\s*"([^"]+)"\s*;')
_PACKAGE_RE = re.compile(r"^package\s+([A-Za-z0-9_.]+)\s*;")
_IMPORT_RE = re.compile(r'^import\s+"([^"]+)"\s*;')
_DECL_RE = re.compile(r"^(message|enum|oneof)\s+([A-Za-z_][A-Za-z0-9_]*)\b")
_FIELD_RE = re.compile(
    r"^(?:(optional|required|repeated)\s+)?([A-Za-z0-9_.]+(?:\s*<[^>]+>)?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(-?\d+)"
)
_ENUM_VALUE_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(-?\d+)")


def _slug(text: str) -> str:
    return text.lower().replace(".", "-").replace("_", "-")


def _module_leaf(proto_name: str) -> str:
    return proto_name[: -len(".proto")] + "_pb2"


def _markdown_escape(text: str) -> str:
    return text.replace("|", "\\|")


def _strip_line_comment(line: str) -> str:
    # Good enough for current proto style (no inline URL literals).
    idx = line.find("//")
    if idx == -1:
        return line
    return line[:idx]


def _flatten_messages(messages: list[ProtoMessage]) -> list[ProtoMessage]:
    out: list[ProtoMessage] = []
    for msg in messages:
        out.append(msg)
        out.extend(_flatten_messages(msg.nested_messages))
    return out


def _flatten_enums(top_enums: list[ProtoEnum], messages: list[ProtoMessage]) -> list[ProtoEnum]:
    out = list(top_enums)
    for msg in messages:
        out.extend(msg.nested_enums)
        out.extend(_flatten_enums([], msg.nested_messages))
    return out


def parse_proto(text: str, file_name: str) -> ProtoDoc:
    text = _BLOCK_COMMENT_RE.sub("", text)
    lines = text.splitlines()

    syntax = ""
    package = ""
    imports: list[str] = []
    top_messages: list[ProtoMessage] = []
    top_enums: list[ProtoEnum] = []

    # Stack entries: ("message", ProtoMessage) | ("enum", ProtoEnum) | ("oneof", str)
    stack: list[tuple[str, object]] = []
    pending: tuple[str, str] | None = None

    def current_message() -> ProtoMessage | None:
        for kind, node in reversed(stack):
            if kind == "message":
                return node  # type: ignore[return-value]
        return None

    for raw in lines:
        line = _strip_line_comment(raw).strip()
        if not line:
            continue

        if not syntax:
            m = _SYNTAX_RE.match(line)
            if m:
                syntax = m.group(1)
                continue
        if not package:
            m = _PACKAGE_RE.match(line)
            if m:
                package = m.group(1)
                continue
        m = _IMPORT_RE.match(line)
        if m:
            imports.append(m.group(1))
            continue

        # Direct declaration on this line.
        d = _DECL_RE.match(line)
        if d:
            decl_kind, name = d.groups()
            has_open = "{" in line

            if has_open:
                parent_msg = current_message()
                if decl_kind == "message":
                    full = name if parent_msg is None else f"{parent_msg.full_name}.{name}"
                    msg = ProtoMessage(
                        name=name,
                        full_name=full,
                        parent="" if parent_msg is None else parent_msg.full_name,
                    )
                    if parent_msg is None:
                        top_messages.append(msg)
                    else:
                        parent_msg.nested_messages.append(msg)
                    stack.append(("message", msg))
                elif decl_kind == "enum":
                    parent = current_message()
                    full = name if parent is None else f"{parent.full_name}.{name}"
                    enum = ProtoEnum(
                        name=name, full_name=full, parent="" if parent is None else parent.full_name
                    )
                    if parent is None:
                        top_enums.append(enum)
                    else:
                        parent.nested_enums.append(enum)
                    stack.append(("enum", enum))
                else:  # oneof
                    parent = current_message()
                    if parent is not None and name not in parent.oneofs:
                        parent.oneofs.append(name)
                    stack.append(("oneof", name))
            else:
                pending = (decl_kind, name)
            # handle closing braces that may appear on same line
            close_count = line.count("}")
            for _ in range(close_count):
                if stack:
                    stack.pop()
            continue

        # Open brace for pending declaration.
        if line == "{" and pending is not None:
            decl_kind, name = pending
            pending = None
            parent_msg = current_message()
            if decl_kind == "message":
                full = name if parent_msg is None else f"{parent_msg.full_name}.{name}"
                msg = ProtoMessage(
                    name=name,
                    full_name=full,
                    parent="" if parent_msg is None else parent_msg.full_name,
                )
                if parent_msg is None:
                    top_messages.append(msg)
                else:
                    parent_msg.nested_messages.append(msg)
                stack.append(("message", msg))
            elif decl_kind == "enum":
                parent = current_message()
                full = name if parent is None else f"{parent.full_name}.{name}"
                enum = ProtoEnum(
                    name=name, full_name=full, parent="" if parent is None else parent.full_name
                )
                if parent is None:
                    top_enums.append(enum)
                else:
                    parent.nested_enums.append(enum)
                stack.append(("enum", enum))
            else:
                parent = current_message()
                if parent is not None and name not in parent.oneofs:
                    parent.oneofs.append(name)
                stack.append(("oneof", name))
            continue

        # Closing braces.
        if "}" in line:
            for _ in range(line.count("}")):
                if stack:
                    stack.pop()
            continue

        if not stack:
            continue

        top_kind, top_node = stack[-1]

        if top_kind == "enum":
            # Enum value line.
            if line.startswith(("option ", "reserved ")):
                continue
            ev = _ENUM_VALUE_RE.match(line)
            if ev:
                name, number = ev.groups()
                enum = top_node  # type: ignore[assignment]
                enum.values.append(ProtoEnumValue(name=name, number=int(number)))
            continue

        # Message field line or oneof field line.
        if line.startswith(("option ", "reserved ", "extensions ", "extend ")):
            continue

        oneof_name = ""
        if top_kind == "oneof":
            oneof_name = str(top_node)

        field_match = _FIELD_RE.match(line)
        if not field_match:
            continue

        label, type_name, field_name, tag_str = field_match.groups()
        current_msg = current_message()
        if current_msg is None:
            continue

        notes: list[str] = []
        if type_name.strip().startswith("map<"):
            notes.append("map field")
        if "[" in line and "]" in line:
            opt = line[line.find("[") + 1 : line.rfind("]")].strip()
            if opt:
                notes.append(opt)

        if oneof_name and not label:
            label = "oneof"
        elif not label:
            label = "unlabeled"

        current_msg.fields.append(
            ProtoField(
                name=field_name,
                type_name=type_name.strip(),
                tag=int(tag_str),
                label=label,
                oneof=oneof_name,
                notes=", ".join(notes),
            )
        )

    return ProtoDoc(
        file_name=file_name,
        syntax=syntax or "unknown",
        package=package or "(none)",
        imports=imports,
        messages=top_messages,
        enums=top_enums,
    )


def render_proto_page(doc: ProtoDoc, out_path: Path) -> tuple[int, int]:
    messages = _flatten_messages(doc.messages)
    enums = _flatten_enums(doc.enums, doc.messages)

    lines: list[str] = []
    lines.append(f"# {doc.file_name}")
    lines.append("")
    lines.append(f"- Module: `{_module_leaf(doc.file_name)}`")
    lines.append(f"- Syntax: `{doc.syntax}`")
    lines.append(f"- Package: `{doc.package}`")
    lines.append(f"- Imports: **{len(doc.imports)}**")
    lines.append(f"- Messages: **{len(messages)}** (top-level: {len(doc.messages)})")
    lines.append(f"- Enums: **{len(enums)}** (top-level: {len(doc.enums)})")
    lines.append("")

    if doc.imports:
        lines.append("## Imports")
        lines.append("")
        for imp in doc.imports:
            lines.append(f"- `{imp}`")
        lines.append("")

    lines.append("## Messages")
    lines.append("")
    lines.append("Expand any message to inspect all fields.")
    lines.append("")
    if not messages:
        lines.append("*(No messages in this proto file.)*")
        lines.append("")
    else:
        for msg in messages:
            lines.append("<details>")
            lines.append(
                f"<summary><code>{_markdown_escape(msg.full_name)}</code> — fields: {len(msg.fields)}; oneofs: {len(msg.oneofs)}; nested messages: {len(msg.nested_messages)}; nested enums: {len(msg.nested_enums)}</summary>"
            )
            lines.append("")
            if msg.parent:
                lines.append(f"- Parent: `{_markdown_escape(msg.parent)}`")
            else:
                lines.append("- Parent: *(top-level)*")
            if msg.oneofs:
                lines.append("- Oneofs: " + ", ".join(f"`{o}`" for o in msg.oneofs))
            else:
                lines.append("- Oneofs: *(none)*")
            lines.append("")
            lines.append("| Tag | Field | Type | Label | Oneof | Notes |")
            lines.append("|---:|---|---|---|---|---|")
            if not msg.fields:
                lines.append("| - | *(none)* |  |  |  |  |")
            else:
                for f in sorted(msg.fields, key=lambda x: x.tag):
                    lines.append(
                        f"| {f.tag} | `{_markdown_escape(f.name)}` | `{_markdown_escape(f.type_name)}` | `{_markdown_escape(f.label)}` | `{_markdown_escape(f.oneof)}` | {_markdown_escape(f.notes)} |"
                    )
            lines.append("")
            lines.append("</details>")
            lines.append("")

    lines.append("## Enums")
    lines.append("")
    lines.append("Expand any enum to inspect all values.")
    lines.append("")
    if not enums:
        lines.append("*(No enums in this proto file.)*")
        lines.append("")
    else:
        for enum in enums:
            lines.append("<details>")
            lines.append(
                f"<summary><code>{_markdown_escape(enum.full_name)}</code> — values: {len(enum.values)}</summary>"
            )
            lines.append("")
            if enum.parent:
                lines.append(f"- Parent: `{_markdown_escape(enum.parent)}`")
            else:
                lines.append("- Parent: *(top-level)*")
            lines.append("")
            lines.append("| Name | Number |")
            lines.append("|---|---:|")
            if enum.values:
                for v in enum.values:
                    lines.append(f"| `{_markdown_escape(v.name)}` | {v.number} |")
            else:
                lines.append("| *(none)* | - |")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return len(messages), len(enums)


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    proto_files = sorted(PROTO_SRC_DIR.glob("*.proto"))
    if not proto_files:
        raise RuntimeError(f"No proto files found under {PROTO_SRC_DIR}")

    index_lines: list[str] = []
    index_lines.append("# Proto Field Atlas")
    index_lines.append("")
    index_lines.append(
        "Field-level catalog for every Dota 2 proto file. Each file page contains collapsible"
    )
    index_lines.append("message and enum sections with declaration details.")
    index_lines.append("")
    index_lines.append(f"- Source proto files: **{len(proto_files)}**")
    index_lines.append("")
    index_lines.append("## Files")
    index_lines.append("")

    written = 0
    for proto_path in proto_files:
        proto_text = proto_path.read_text(encoding="utf-8", errors="replace")
        proto_doc = parse_proto(proto_text, proto_path.name)
        page_name = f"{_slug(proto_path.stem)}.md"
        msg_count, enum_count = render_proto_page(proto_doc, OUT_DIR / page_name)
        index_lines.append(
            f"- [{proto_path.name}]({page_name}) — messages: {msg_count}, enums: {enum_count}"
        )
        written += 1

    (OUT_DIR / "index.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    print(f"Generated {written} proto field pages in {OUT_DIR}")


if __name__ == "__main__":
    main()
