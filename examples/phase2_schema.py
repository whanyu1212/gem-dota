"""Phase 2 example — inspect the entity schema from a replay.

Demonstrates what is available after Phase 2 (sendtable.py, field_decoder.py,
field_path.py):

- Parse CDemoSendTables from the replay stream
- List all entity class serializers
- Inspect fields of a specific entity class
- Show field types, models, and assigned decoders

Usage:
    python examples/phase2_schema.py path/to/replay.dem
    python examples/phase2_schema.py path/to/replay.dem --class CDOTA_Unit_Hero_Axe
    python examples/phase2_schema.py path/to/replay.dem --list
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# EDemoCommands value for CDemoSendTables
# ---------------------------------------------------------------------------
DEM_SEND_TABLES = 4
DEM_IS_COMPRESSED = 0x40


def find_send_tables(path: Path) -> bytes:
    """Scan the stream for the CDemoSendTables payload.

    Args:
        path: Path to a .dem replay file.

    Returns:
        Raw bytes of the CDemoSendTables outer message payload.

    Raises:
        RuntimeError: If CDemoSendTables is not found in the stream.
    """
    from gem.stream import DemoStream

    with DemoStream(path) as stream:
        for _tick, msg_type, data in stream:
            if (msg_type & ~DEM_IS_COMPRESSED) == DEM_SEND_TABLES:
                return data
    raise RuntimeError("CDemoSendTables not found in replay")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replay", type=Path, help="Path to .dem replay file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true", help="List all serializer names")
    group.add_argument(
        "--class",
        dest="entity_class",
        metavar="NAME",
        default="CDOTAGamerulesProxy",
        help="Entity class to inspect (default: CDOTAGamerulesProxy)",
    )
    args = parser.parse_args()

    if not args.replay.exists():
        print(f"Error: file not found: {args.replay}", file=sys.stderr)
        sys.exit(1)

    print(f"Replay : {args.replay.name}")
    print(f"Size   : {args.replay.stat().st_size / 1e6:.1f} MB")
    print()

    print("Scanning for CDemoSendTables...", flush=True)
    raw = find_send_tables(args.replay)

    from gem.sendtable import (
        FIELD_MODEL_FIXED_ARRAY,
        FIELD_MODEL_FIXED_TABLE,
        FIELD_MODEL_VARIABLE_ARRAY,
        FIELD_MODEL_VARIABLE_TABLE,
        parse_send_tables,
    )

    serializers = parse_send_tables(raw)
    print(f"Found {len(serializers)} entity class serializers.")
    print()

    if args.list:
        # Print all serializer names sorted
        for name in sorted(serializers):
            s = serializers[name]
            print(f"  {name}  ({len(s.fields)} fields)")
        return

    # Inspect a specific class
    name = args.entity_class
    if name not in serializers:
        # Fuzzy search
        matches = [n for n in serializers if name.lower() in n.lower()]
        if not matches:
            print(f"No serializer found for {name!r}.", file=sys.stderr)
            sys.exit(1)
        name = matches[0]
        print(f"(No exact match, showing {name!r})\n")

    s = serializers[name]
    print(f"Serializer: {s.name}  (version {s.version})")
    print(f"Fields    : {len(s.fields)}")
    print()

    header = f"  {'#':>4}  {'Name':<40}  {'Type':<35}  {'Model':<15}  Encoder"
    print(header)
    print("  " + "-" * (len(header) - 2))

    for i, f in enumerate(s.fields):
        model = f.model_name()
        encoder = f.encoder or ""
        # Annotate sub-serializer references
        if f.model in (FIELD_MODEL_FIXED_TABLE, FIELD_MODEL_VARIABLE_TABLE):
            model_display = f"{model} → {f.serializer_name}"
        elif f.model in (FIELD_MODEL_FIXED_ARRAY, FIELD_MODEL_VARIABLE_ARRAY):
            model_display = f"{model}[{f.field_type.count}]"
        else:
            model_display = model

        print(f"  {i:>4}  {f.var_name:<40}  {f.var_type:<35}  {model_display:<15}  {encoder}")

    print()
    print("Field path decoder: ready (Huffman tree pre-built at import)")
    print("Next step — Phase 3: string tables + entity lifecycle decoding")


if __name__ == "__main__":
    main()
