"""Generate VitePress API reference pages from src/gem.

The generator keeps each page's narrative markdown (in docs/reference/*.md),
removes any previously generated API section, and appends a freshly generated
API section from source AST/docstrings.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_REF_ROOT = REPO_ROOT / "docs" / "reference"
DST_REF_ROOT = REPO_ROOT / "docs" / "reference"
SRC_CODE_ROOT = REPO_ROOT / "src" / "gem"
GITHUB_SOURCE_PREFIX = "https://github.com/whanyu1212/gem-dota/blob/main/"

DIRECTIVE_RE = re.compile(r"^\s*:::\s*(gem\.[\w.]+)\s*$")
ADMONITION_RE = re.compile(r'^!!!\s+(\w+)(?:\s+"([^"]+)")?\s*$')
GENERATED_API_HEADING_RE = re.compile(r"^## Generated API\s*$", re.MULTILINE)
TARGET_HEADING_RE = re.compile(r"^##\s+`(gem\.[^`]+)`\s*$")
MODULE_TARGET_HEADING_RE = re.compile(r"^##\s+Module\s+`(gem\.[^`]+)`\s*$")

# Canonical API targets by reference page (relative to docs/reference).
TARGETS_BY_PAGE: dict[str, list[str]] = {
    "analysis.md": ["gem.analysis"],
    "batch.md": ["gem.batch"],
    "combat_aggregator.md": ["gem.combat_aggregator"],
    "combatlog.md": ["gem.combatlog.CombatLogProcessor", "gem.combatlog.CombatLogEntry"],
    "constants.md": ["gem.constants"],
    "dataframes.md": ["gem.dataframes"],
    "entities.md": ["gem.entities.EntityOp", "gem.entities.Entity", "gem.entities.EntityManager"],
    "field_decoder.md": [
        "gem.field_decoder.find_decoder",
        "gem.field_decoder.find_decoder_by_base_type",
        "gem.field_decoder.QuantizedFloatDecoder",
    ],
    "field_path.md": [
        "gem.field_path.read_field_paths",
        "gem.field_path.FieldPath",
        "gem.field_path.FieldPathOp",
    ],
    "game_events.md": [
        "gem.game_events.GameEventManager",
        "gem.game_events.GameEvent",
        "gem.game_events.GameEventSchema",
    ],
    "match_builder.md": ["gem.match_builder"],
    "models.md": ["gem.models"],
    "parser.md": ["gem.parser.ReplayParser"],
    "reader.md": ["gem.reader.BitReader"],
    "sendtable.md": [
        "gem.sendtable.parse_send_tables",
        "gem.sendtable.Serializer",
        "gem.sendtable.Field",
        "gem.sendtable.FieldType",
    ],
    "stream.md": ["gem.stream.DemoStream", "gem.stream.OuterMessage"],
    "string_table.md": [
        "gem.string_table.StringTables",
        "gem.string_table.StringTable",
        "gem.string_table.StringTableItem",
        "gem.string_table.parse_string_table",
        "gem.string_table.handle_create",
        "gem.string_table.handle_update",
    ],
    "extractors/courier.md": ["gem.extractors.courier"],
    "extractors/draft.md": ["gem.extractors.draft"],
    "extractors/lane.md": ["gem.extractors.lane"],
    "extractors/objectives.md": ["gem.extractors.objectives"],
    "extractors/players.md": ["gem.extractors.players"],
    "extractors/teamfights.md": ["gem.extractors.teamfights"],
    "extractors/wards.md": ["gem.extractors.wards"],
}


@dataclass
class ModuleContext:
    module_name: str
    file_path: Path
    source: str
    tree: ast.Module


MODULE_CACHE: dict[str, ModuleContext] = {}


def _module_to_file(module_name: str) -> Path | None:
    if not module_name.startswith("gem"):
        return None
    parts = module_name.split(".")[1:]
    if not parts:
        path = SRC_CODE_ROOT / "__init__.py"
        return path if path.exists() else None
    py_path = SRC_CODE_ROOT.joinpath(*parts).with_suffix(".py")
    if py_path.exists():
        return py_path
    init_path = SRC_CODE_ROOT.joinpath(*parts) / "__init__.py"
    if init_path.exists():
        return init_path
    return None


def _resolve_object_path(path: str) -> tuple[ModuleContext, list[str]]:
    parts = path.split(".")
    if parts[0] != "gem":
        raise ValueError(f"Unsupported directive target: {path}")

    for i in range(len(parts), 0, -1):
        module_name = ".".join(parts[:i])
        module_file = _module_to_file(module_name)
        if module_file is None:
            continue

        context = MODULE_CACHE.get(module_name)
        if context is None:
            source = module_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
            context = ModuleContext(
                module_name=module_name, file_path=module_file, source=source, tree=tree
            )
            MODULE_CACHE[module_name] = context

        remainder = parts[i:]
        return context, remainder

    raise ValueError(f"Could not resolve module for directive target: {path}")


def _first_paragraph(doc: str | None) -> str:
    if not doc:
        return "No docstring available."
    text = doc.strip()
    if not text:
        return "No docstring available."
    first = text.split("\n\n", 1)[0].strip().replace("\n", " ")
    if len(first) > 650:
        return first[:647].rstrip() + "..."
    return first


def _expr(node: ast.AST | None) -> str:
    if node is None:
        return ""
    return ast.unparse(node)


def _format_args(args: ast.arguments) -> str:
    rendered: list[str] = []

    pos = list(args.posonlyargs) + list(args.args)
    defaults: list[ast.AST | None] = [None] * (len(pos) - len(args.defaults)) + list(args.defaults)

    for idx, (arg, default) in enumerate(zip(pos, defaults, strict=True)):
        part = arg.arg
        if arg.annotation is not None:
            part += f": {_expr(arg.annotation)}"
        if default is not None:
            part += f" = {_expr(default)}"
        rendered.append(part)
        if args.posonlyargs and idx == len(args.posonlyargs) - 1:
            rendered.append("/")

    if args.vararg is not None:
        var = f"*{args.vararg.arg}"
        if args.vararg.annotation is not None:
            var += f": {_expr(args.vararg.annotation)}"
        rendered.append(var)
    elif args.kwonlyargs:
        rendered.append("*")

    for kwarg, default in zip(args.kwonlyargs, args.kw_defaults, strict=True):
        part = kwarg.arg
        if kwarg.annotation is not None:
            part += f": {_expr(kwarg.annotation)}"
        if default is not None:
            part += f" = {_expr(default)}"
        rendered.append(part)

    if args.kwarg is not None:
        kw = f"**{args.kwarg.arg}"
        if args.kwarg.annotation is not None:
            kw += f": {_expr(args.kwarg.annotation)}"
        rendered.append(kw)

    return ", ".join(rendered)


def _func_signature(
    node: ast.FunctionDef | ast.AsyncFunctionDef, class_name: str | None = None
) -> str:
    args = _format_args(node.args)
    name = f"{class_name}.{node.name}" if class_name else node.name
    ret = f" -> {_expr(node.returns)}" if node.returns is not None else ""
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    return f"{prefix} {name}({args}){ret}"


def _class_signature(node: ast.ClassDef) -> str:
    if node.bases:
        bases = ", ".join(_expr(base) for base in node.bases)
        return f"class {node.name}({bases})"
    return f"class {node.name}"


def _gh_link(path: Path, lineno: int) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    return f"{GITHUB_SOURCE_PREFIX}{rel}#L{lineno}"


def _top_level_functions(tree: ast.Module) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    out: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith(
            "_"
        ):
            out.append(node)
    return out


def _top_level_classes(tree: ast.Module) -> list[ast.ClassDef]:
    out: list[ast.ClassDef] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            out.append(node)
    return out


def _find_class(tree: ast.Module, class_name: str) -> ast.ClassDef | None:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    return None


def _find_function(
    tree: ast.Module, func_name: str
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
            return node
    return None


def _public_methods(cls: ast.ClassDef) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    methods: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    for node in cls.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _is_property(node):
                continue
            if node.name == "__init__" and ast.get_docstring(node, clean=True) is None:
                continue
            if node.name.startswith("_"):
                continue
            methods.append(node)
    return methods


def _properties(cls: ast.ClassDef) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    props: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    for node in cls.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_property(node):
            props.append(node)
    return props


def _is_property(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(isinstance(deco, ast.Name) and deco.id == "property" for deco in node.decorator_list)


def _is_dataclass(cls: ast.ClassDef) -> bool:
    for deco in cls.decorator_list:
        if isinstance(deco, ast.Name) and deco.id == "dataclass":
            return True
        if (
            isinstance(deco, ast.Call)
            and isinstance(deco.func, ast.Name)
            and deco.func.id == "dataclass"
        ):
            return True
    return False


def _compact_expr(node: ast.AST | None) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "field":
        return "field(...)"
    text = _expr(node)
    if len(text) > 80:
        return text[:77].rstrip() + "..."
    return text


def _dataclass_fields(cls: ast.ClassDef) -> list[tuple[str, str, str]]:
    fields: list[tuple[str, str, str]] = []
    for node in cls.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id.startswith("_"):
                continue
            name = node.target.id
            ann = _expr(node.annotation) if node.annotation is not None else ""
            default = _compact_expr(node.value) if node.value is not None else ""
            fields.append((name, ann, default))
    return fields


def _render_function(
    func: ast.FunctionDef | ast.AsyncFunctionDef, context: ModuleContext
) -> list[str]:
    sig = _func_signature(func)
    doc = _first_paragraph(ast.get_docstring(func, clean=True))
    source = _gh_link(context.file_path, func.lineno)

    return [
        f"### `{func.name}`",
        "",
        "```python",
        sig,
        "```",
        "",
        doc,
        "",
        f"Source: [{context.file_path.relative_to(REPO_ROOT)}:{func.lineno}]({source})",
        "",
    ]


def _render_class(cls: ast.ClassDef, context: ModuleContext) -> list[str]:
    sig = _class_signature(cls)
    doc = _first_paragraph(ast.get_docstring(cls, clean=True))
    source = _gh_link(context.file_path, cls.lineno)

    out = [
        f"### `{cls.name}`",
        "",
        "```python",
        sig,
        "```",
        "",
        doc,
        "",
        f"Source: [{context.file_path.relative_to(REPO_ROOT)}:{cls.lineno}]({source})",
        "",
    ]

    if _is_dataclass(cls):
        fields = _dataclass_fields(cls)
        if fields:
            out.append("#### Dataclass fields")
            out.append("")
            out.append("| Name | Type | Default |")
            out.append("|---|---|---|")
            for name, ann, default in fields:
                ann_text = ann or "-"
                default_text = default or "-"
                out.append(f"| `{name}` | `{ann_text}` | `{default_text}` |")
            out.append("")

    properties = _properties(cls)
    if properties:
        out.append("#### Properties")
        out.append("")
        for prop in properties:
            prop_sig = _func_signature(prop, cls.name)
            prop_doc = _first_paragraph(ast.get_docstring(prop, clean=True))
            prop_source = _gh_link(context.file_path, prop.lineno)
            out.extend(
                [
                    f"##### `{prop.name}`",
                    "",
                    f"Signature: `{prop_sig}`",
                    "",
                    prop_doc,
                    "",
                    f"Source: [{context.file_path.relative_to(REPO_ROOT)}:{prop.lineno}]({prop_source})",
                    "",
                ]
            )

    methods = _public_methods(cls)
    if methods:
        out.append("#### Methods")
        out.append("")
        for method in methods:
            method_sig = _func_signature(method, cls.name)
            method_doc = _first_paragraph(ast.get_docstring(method, clean=True))
            method_source = _gh_link(context.file_path, method.lineno)
            out.extend(
                [
                    f"##### `{method.name}`",
                    "",
                    f"Signature: `{method_sig}`",
                    "",
                    method_doc,
                    "",
                    f"Source: [{context.file_path.relative_to(REPO_ROOT)}:{method.lineno}]({method_source})",
                    "",
                ]
            )

    return out


def _render_module(context: ModuleContext) -> list[str]:
    module_doc = _first_paragraph(ast.get_docstring(context.tree, clean=True))
    source = _gh_link(context.file_path, 1)

    out = [
        f"## Module `{context.module_name}`",
        "",
        module_doc,
        "",
        f"Source: [{context.file_path.relative_to(REPO_ROOT)}]({source})",
        "",
    ]

    functions = _top_level_functions(context.tree)
    classes = _top_level_classes(context.tree)

    if functions:
        out.append("### Top-level functions")
        out.append("")
        for func in functions:
            out.extend(_render_function(func, context))

    if classes:
        out.append("### Top-level classes")
        out.append("")
        for cls in classes:
            out.extend(_render_class(cls, context))

    if not functions and not classes:
        out.extend(["No public top-level classes or functions found.", ""])

    return out


def _render_target(target: str) -> list[str]:
    context, remainder = _resolve_object_path(target)
    if not remainder:
        return _render_module(context)

    # Class or function under module.
    if len(remainder) == 1:
        name = remainder[0]
        cls = _find_class(context.tree, name)
        if cls is not None:
            return [f"## `{target}`", ""] + _render_class(cls, context)

        func = _find_function(context.tree, name)
        if func is not None:
            return [f"## `{target}`", ""] + _render_function(func, context)

        return [f"## `{target}`", "", "Unable to resolve this symbol from source.", ""]

    # Class method path.
    if len(remainder) == 2:
        cls_name, meth_name = remainder
        cls = _find_class(context.tree, cls_name)
        if cls is None:
            return [f"## `{target}`", "", "Unable to resolve class for this symbol.", ""]

        method = None
        for node in cls.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == meth_name:
                method = node
                break
        if method is None:
            return [f"## `{target}`", "", "Unable to resolve method for this symbol.", ""]

        sig = _func_signature(method, cls_name)
        doc = _first_paragraph(ast.get_docstring(method, clean=True))
        source = _gh_link(context.file_path, method.lineno)
        return [
            f"## `{target}`",
            "",
            "```python",
            sig,
            "```",
            "",
            doc,
            "",
            f"Source: [{context.file_path.relative_to(REPO_ROOT)}:{method.lineno}]({source})",
            "",
        ]

    return [f"## `{target}`", "", "Unsupported symbol depth for generator.", ""]


def _convert_admonitions(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = ADMONITION_RE.match(line)
        if not match:
            out.append(line)
            i += 1
            continue

        kind = match.group(1).lower()
        if kind == "note":
            kind = "info"
        title = match.group(2)

        head = f"::: {kind}"
        if title:
            head += f" {title}"
        out.append(head)

        i += 1
        body: list[str] = []
        while i < len(lines):
            cur = lines[i]
            if cur.startswith("    "):
                body.append(cur[4:])
                i += 1
                continue
            if cur.startswith("\t"):
                body.append(cur[1:])
                i += 1
                continue
            if cur == "":
                body.append("")
                i += 1
                continue
            break

        while body and body[-1] == "":
            body.pop()

        out.extend(body)
        out.append(":::")
        out.append("")

    return out


def _strip_generated_api(md_text: str) -> str:
    match = GENERATED_API_HEADING_RE.search(md_text)
    if match is None:
        return md_text
    return md_text[: match.start()]


def _infer_targets_from_generated(md_text: str) -> list[str]:
    targets: list[str] = []
    for line in md_text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = line.strip()
        match = TARGET_HEADING_RE.match(line) or MODULE_TARGET_HEADING_RE.match(line)
        if match:
            target = match.group(1).strip()
            if target not in targets:
                targets.append(target)
    return targets


def _clean_source_markdown(md_text: str) -> tuple[str, list[str]]:
    lines = _strip_generated_api(md_text).replace("\r\n", "\n").replace("\r", "\n").split("\n")
    directives: list[str] = []
    kept: list[str] = []

    for line in lines:
        m = DIRECTIVE_RE.match(line)
        if m:
            directives.append(m.group(1))
            continue
        kept.append(line)

    kept = _convert_admonitions(kept)
    text = "\n".join(kept).rstrip() + "\n"
    return text, directives


def _iter_reference_pages() -> Iterable[Path]:
    yield from sorted(SRC_REF_ROOT.rglob("*.md"))


def generate() -> None:
    written = 0
    for src_page in _iter_reference_pages():
        rel = src_page.relative_to(SRC_REF_ROOT)
        dst_page = DST_REF_ROOT / rel
        dst_page.parent.mkdir(parents=True, exist_ok=True)

        source_md = src_page.read_text(encoding="utf-8")
        static_md, directives = _clean_source_markdown(source_md)
        rel_key = rel.as_posix()
        if not directives:
            directives = TARGETS_BY_PAGE.get(rel_key, _infer_targets_from_generated(source_md))

        static_clean = static_md.rstrip()
        out_lines: list[str] = [static_clean, ""]
        if directives:
            if not static_clean.endswith("---"):
                out_lines.extend(["---", ""])
            out_lines.extend(["## Generated API", ""])
            for directive in directives:
                out_lines.extend(_render_target(directive))

        text = "\n".join(line for line in out_lines).rstrip() + "\n"
        dst_page.write_text(text, encoding="utf-8")
        written += 1

    print(f"Generated {written} reference pages into {DST_REF_ROOT}")


if __name__ == "__main__":
    generate()
