"""Generate field-level VitePress docs for all Dota 2 proto files.

This parser reads source .proto files directly (not generated Python descriptors),
then writes readable docs with collapsible message/enum sections.

Each page is also marked with how gem uses the file:

- used: gem source imports classes or constants from the generated module
- loaded: a used file imports it, directly or transitively, so it loads anyway
- unused: not needed for replays

Both sets are derived from source (gem's ``from gem.proto.X_pb2 import`` lines and
the ``.proto`` import graph), so the generator does not need gem installed.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROTO_SRC_DIR = REPO_ROOT / "proto_definitions" / "dota2"
GEM_SRC_DIR = REPO_ROOT / "src" / "gem"
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
_IMPORT_RE = re.compile(r'^import\s+(?:public\s+|weak\s+)?"([^"]+)"\s*;')
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


def _code_cell(text: str) -> str:
    """Format a value as an inline-code table cell.

    Returns an empty string for empty values so absent fields render as a
    blank cell rather than a stray empty code span (the literal ``````).
    """
    if not text:
        return ""
    return f"`{_markdown_escape(text)}`"


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


_GEM_PROTO_IMPORT_RE = re.compile(r"^\s*from\s+gem\.proto\.([\w.]+)_pb2\s+import\b", re.MULTILINE)


def used_proto_files(gem_src_dir: Path = GEM_SRC_DIR) -> set[str]:
    """Return the ``.proto`` files whose generated modules gem imports names from.

    Bare module imports kept only for side effects (``from gem.proto import x_pb2``)
    do not count: they appear in the loaded set anyway.
    """
    proto_pkg = gem_src_dir / "proto"
    used: set[str] = set()
    for path in gem_src_dir.rglob("*.py"):
        if proto_pkg in path.parents:
            continue
        text = path.read_text(encoding="utf-8")
        used.update(f"{module}.proto" for module in _GEM_PROTO_IMPORT_RE.findall(text))
    return used


def loaded_proto_files(used: set[str], imports: dict[str, list[str]]) -> dict[str, list[str]]:
    """Return files loaded only through imports, mapped to the loaded files importing them.

    Args:
        used: File names from :func:`used_proto_files`.
        imports: Each proto file name mapped to the proto files it imports.

    Returns:
        Each loaded-but-unused file name mapped to the sorted names of the used or
        loaded files that import it directly.
    """
    reachable: set[str] = set()
    queue = sorted(used)
    while queue:
        name = queue.pop()
        for dep in imports.get(name, []):
            if dep in imports and dep not in reachable and dep not in used:
                reachable.add(dep)
                queue.append(dep)
    loaded_or_used = reachable | used
    return {
        name: sorted(src for src in loaded_or_used if name in imports.get(src, []))
        for name in sorted(reachable)
    }


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
        syntax=syntax,
        package=package,
        imports=imports,
        messages=top_messages,
        enums=top_enums,
    )


def _usage_line(file_name: str, used: set[str], loaded: dict[str, list[str]]) -> str:
    if file_name in used:
        return (
            "**Used by gem**: gem decodes messages from this file. See "
            "[The Proto Files gem Uses](../proto-files.md) for what it reads and why."
        )
    if file_name in loaded:
        importers = ", ".join(f"`{name}`" for name in loaded[file_name])
        return (
            f"**Loaded, not used**: gem doesn't use this file, but it is imported by "
            f"{importers}, so Python loads it anyway."
        )
    return (
        "**Not used by gem**: nothing in this file is needed to parse a replay. See "
        "[the map of all 84 files](../proto-files.md#the-map-all-84-files) for what it "
        "belongs to."
    )


def render_proto_page(
    doc: ProtoDoc,
    out_path: Path,
    used: set[str] | None = None,
    loaded: dict[str, list[str]] | None = None,
) -> tuple[int, int]:
    messages = _flatten_messages(doc.messages)
    enums = _flatten_enums(doc.enums, doc.messages)

    lines: list[str] = []
    lines.append(f"# {doc.file_name}")
    lines.append("")
    if used is not None and loaded is not None:
        lines.append(_usage_line(doc.file_name, used, loaded))
        lines.append("")
    lines.append(f"- Module: `{_module_leaf(doc.file_name)}`")
    if doc.syntax:
        lines.append(f"- Syntax: `{doc.syntax}`")
    if doc.package:
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
                        f"| {f.tag} | {_code_cell(f.name)} | {_code_cell(f.type_name)} "
                        f"| {_code_cell(f.label)} | {_code_cell(f.oneof)} | {_markdown_escape(f.notes)} |"
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

    docs = {
        path.name: parse_proto(path.read_text(encoding="utf-8", errors="replace"), path.name)
        for path in proto_files
    }
    used = used_proto_files() & docs.keys()
    loaded = loaded_proto_files(used, {name: doc.imports for name, doc in docs.items()})

    entries: dict[str, list[str]] = {"used": [], "loaded": [], "unused": []}
    for proto_path in proto_files:
        doc = docs[proto_path.name]
        page_name = f"{_slug(proto_path.stem)}.md"
        msg_count, enum_count = render_proto_page(doc, OUT_DIR / page_name, used, loaded)
        group = (
            "used" if doc.file_name in used else "loaded" if doc.file_name in loaded else "unused"
        )
        entries[group].append(
            f"- [{proto_path.name}]({page_name}) — messages: {msg_count}, enums: {enum_count}"
        )

    index_lines = [
        "# Proto Field Atlas",
        "",
        f"Every message and enum in all {len(proto_files)} Dota 2 proto files, with each "
        "field's tag, type, and label. Each file has its own page with collapsible sections.",
        "",
        "Only a few of these files matter for replays. For what they carry and how gem uses "
        "them, read [The Proto Files gem Uses](../proto-files.md) first.",
        "",
        "These pages are generated by `scripts/generate_proto_field_docs.py`. Don't edit "
        "them by hand.",
        "",
        f"## Used by gem ({len(entries['used'])})",
        "",
        "gem decodes messages from these files.",
        "",
        *entries["used"],
        "",
        f"## Loaded, not used ({len(entries['loaded'])})",
        "",
        "gem doesn't use these files, but the files above import them, so Python loads them.",
        "",
        *entries["loaded"],
        "",
        f"## Not used ({len(entries['unused'])})",
        "",
        "Not needed to parse a replay: mostly Valve's backend and Steam platform messages.",
        "",
        *entries["unused"],
    ]
    (OUT_DIR / "index.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    print(
        f"Generated {len(proto_files)} proto field pages in {OUT_DIR} "
        f"({len(used)} used, {len(loaded)} loaded, {len(entries['unused'])} unused)"
    )


if __name__ == "__main__":
    main()
