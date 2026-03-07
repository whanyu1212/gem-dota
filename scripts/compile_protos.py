"""
Compile all .proto files in proto_definitions/dota2 into Python bindings.

Uses the protoc binary bundled with protoc-wheel-0 (installed via uv) so there
is no dependency on a system-level protoc installation.

Output layout:
    src/gem/proto/
        dota2/
            <name>_pb2.py      # generated message classes
            <name>_pb2.pyi     # type stubs (for IDE support)
        __init__.py

Usage:
    uv run python scripts/compile_protos.py
    uv run python scripts/compile_protos.py --force   # recompile even if up to date
    uv run python scripts/compile_protos.py --verbose # show each protoc invocation
"""

import argparse
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
PROTO_SRC_DIR = REPO_ROOT / "proto_definitions" / "dota2"
PROTO_OUT_DIR = REPO_ROOT / "src" / "gem" / "proto" / "dota2"


def find_protoc() -> Path:
    """Return the protoc binary from protoc-wheel-0 (preferred) or system PATH."""
    try:
        import protoc  # provided by protoc-wheel-0

        exe = Path(protoc.PROTOC_EXE)
        if exe.exists():
            return exe
    except ImportError:
        pass

    # Fall back to system protoc
    import shutil

    system_protoc = shutil.which("protoc")
    if system_protoc:
        print(
            "Warning: protoc-wheel-0 not found, falling back to system protoc.",
            file=sys.stderr,
        )
        return Path(system_protoc)

    print(
        "Error: protoc not found. Run `uv add protoc-wheel-0` or install protoc.",
        file=sys.stderr,
    )
    sys.exit(1)


def get_protoc_include(protoc_exe: Path) -> Path | None:
    """Return the bundled include dir if using protoc-wheel-0, else None."""
    try:
        import protoc

        include = Path(protoc.PROTOC_INCLUDE_DIR)
        return include if include.exists() else None
    except ImportError:
        return None


def is_up_to_date(proto_file: Path, out_dir: Path) -> bool:
    """Return True if the generated _pb2.py is newer than the .proto source."""
    pb2 = out_dir / (proto_file.stem + "_pb2.py")
    if not pb2.exists():
        return False
    return pb2.stat().st_mtime >= proto_file.stat().st_mtime


def ensure_init_files(out_dir: Path) -> None:
    """Create __init__.py in the output dir and its parent so it's importable."""
    for directory in (out_dir.parent, out_dir):
        init = directory / "__init__.py"
        if not init.exists():
            init.touch()
            print(f"  Created {init.relative_to(REPO_ROOT)}")


def compile_proto(
    proto_file: Path,
    proto_src_dir: Path,
    out_dir: Path,
    protoc_exe: Path,
    protoc_include: Path | None,
    verbose: bool,
) -> bool:
    """Compile a single .proto file. Returns True on success."""
    cmd = [
        str(protoc_exe),
        f"--proto_path={proto_src_dir}",
        f"--python_out={out_dir}",
        f"--pyi_out={out_dir}",
    ]
    if protoc_include:
        cmd.append(f"--proto_path={protoc_include}")
    cmd.append(str(proto_file))

    if verbose:
        print("  $", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {proto_file.name}", file=sys.stderr)
        print(result.stderr.strip(), file=sys.stderr)
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile Dota 2 .proto files to Python.")
    parser.add_argument("--force", action="store_true", help="Recompile even if up to date.")
    parser.add_argument("--verbose", action="store_true", help="Print each protoc invocation.")
    args = parser.parse_args()

    if not PROTO_SRC_DIR.exists():
        print(
            f"Error: proto source directory not found: {PROTO_SRC_DIR}\n"
            "Run `bash scripts/download_protos.sh` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    proto_files = sorted(PROTO_SRC_DIR.glob("*.proto"))
    if not proto_files:
        print(f"Error: no .proto files found in {PROTO_SRC_DIR}", file=sys.stderr)
        sys.exit(1)

    PROTO_OUT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_init_files(PROTO_OUT_DIR)

    protoc_exe = find_protoc()
    protoc_include = get_protoc_include(protoc_exe)
    print(f"Using protoc: {protoc_exe}")
    print(f"Source:       {PROTO_SRC_DIR}  ({len(proto_files)} files)")
    print(f"Output:       {PROTO_OUT_DIR}")
    print()

    compiled = 0
    skipped = 0
    failed = 0

    for proto_file in proto_files:
        if not args.force and is_up_to_date(proto_file, PROTO_OUT_DIR):
            if args.verbose:
                print(f"  {proto_file.name} ... up to date")
            skipped += 1
            continue

        print(f"  {proto_file.name} ... ", end="", flush=True)
        if compile_proto(
            proto_file, PROTO_SRC_DIR, PROTO_OUT_DIR, protoc_exe, protoc_include, args.verbose
        ):
            print("ok")
            compiled += 1
        else:
            failed += 1

    print()
    print(f"Compiled: {compiled}  Skipped: {skipped}  Failed: {failed}")

    if failed:
        sys.exit(1)

    print()
    print("Next step:")
    print("  uv run python -c \"from gem.proto.dota2 import demo_pb2; print('OK')\"")


if __name__ == "__main__":
    main()
