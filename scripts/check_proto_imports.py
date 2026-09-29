"""Check that every generated protobuf binding imports, each in a fresh interpreter.

Upstream ships variant headers that declare the same custom options:
``steammessages.proto`` and ``steammessages_base.proto`` both define
``msgpool_soft_limit`` and friends. Importing every generated module into one
process therefore always collides in protobuf's global descriptor pool
(``duplicate symbol 'msgpool_soft_limit'``). Importing each module on its own
checks what matters: every binding gem can use loads.

``steammessages_base_pb2`` is the one exception. Nothing imports it, and it
cannot load wherever gem is loaded, because importing ``gem`` already loads
``steammessages_pb2``. It is listed in ``KNOWN_CONFLICTS`` and must fail with
exactly its expected error line. Importing cleanly fails the check too (the
exemption is stale and should be removed), as does any other error, or a
conflict in any other module.

Usage:
    uv run python scripts/check_proto_imports.py
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROTO_ROOT = REPO_ROOT / "src" / "gem" / "proto"
# Variant headers that cannot load alongside the headers gem uses, mapped to
# the exact last stderr line their import must end with.
KNOWN_CONFLICTS: dict[str, str] = {
    "gem.proto.steammessages_base_pb2": (
        "TypeError: Couldn't build proto file into descriptor pool: duplicate extension entry"
    ),
}


def discover_modules(proto_root: Path) -> list[str]:
    """Return the dotted names of every ``*_pb2`` module under ``proto_root``.

    Args:
        proto_root: The generated package directory, e.g. ``src/gem/proto``.

    Returns:
        Sorted module names, relative to the directory that contains the
        top-level package (``gem.proto.demo_pb2`` for ``src/gem/proto``).
    """
    source_root = proto_root.parent.parent
    return sorted(
        ".".join(path.relative_to(source_root).with_suffix("").parts)
        for path in proto_root.rglob("*_pb2.py")
    )


def import_failure(module: str, source_root: Path) -> str | None:
    """Import ``module`` in a fresh interpreter and return its error, if any.

    Args:
        module: Dotted module name.
        source_root: Directory to put first on ``sys.path``.

    Returns:
        The last line of the interpreter's stderr on failure, else ``None``.
    """
    result = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        capture_output=True,
        text=True,
        cwd=source_root,
        check=False,
    )
    if result.returncode == 0:
        return None
    lines = result.stderr.strip().splitlines()
    return lines[-1] if lines else f"exit code {result.returncode}"


def check(proto_root: Path, *, workers: int = 8) -> dict[str, str]:
    """Import every generated module separately and collect the failures.

    Args:
        proto_root: The generated package directory.
        workers: How many interpreters to run at once.

    Returns:
        Failing module name -> error line. Empty when every module imports and
        every known conflict fails with exactly its expected error.
    """
    source_root = proto_root.parent.parent
    modules = discover_modules(proto_root)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        errors = list(pool.map(lambda module: import_failure(module, source_root), modules))
    failures = {}
    for module, error in zip(modules, errors, strict=True):
        if module in KNOWN_CONFLICTS:
            expected = KNOWN_CONFLICTS[module]
            if error is None:
                failures[module] = "imported cleanly; remove it from KNOWN_CONFLICTS"
            elif error != expected:
                failures[module] = f"expected {expected!r}, got {error!r}"
        elif error is not None:
            failures[module] = error
    return failures


def main(argv: list[str] | None = None) -> int:
    """Run the check and report the result.

    Args:
        argv: Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns:
        ``0`` when every module imports, else ``1``.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--proto-root", type=Path, default=DEFAULT_PROTO_ROOT)
    args = parser.parse_args(argv)

    modules = discover_modules(args.proto_root)
    if not modules:
        print(f"No generated *_pb2.py modules under {args.proto_root}.", file=sys.stderr)
        return 1
    failures = check(args.proto_root)
    for module, error in failures.items():
        print(f"FAILED {module}: {error}", file=sys.stderr)
    if failures:
        return 1
    print(
        f"Imported {len(modules)} generated protobuf modules, each in its own interpreter "
        f"({len(KNOWN_CONFLICTS)} known variant-header conflict allowed)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
