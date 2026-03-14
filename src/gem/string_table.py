"""String table parser for Dota 2 Source 2 replays.

Handles ``CSVCMsg_CreateStringTable`` and ``CSVCMsg_UpdateStringTable``
messages.  The string table subsystem maintains a set of named key-value
tables that are updated throughout the replay.  The most important table
for entity decoding is ``instancebaseline``, which holds per-class
baseline field values.

Reference: manta/string_table.go
"""

from dataclasses import dataclass, field
from typing import NamedTuple

import snappy

from gem.reader import BitReader

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_KEY_HISTORY_SIZE = 32


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


#: One entry in a string table: (index, key, value).
class StringTableItem(NamedTuple):
    index: int  # type: ignore[assignment]
    key: str
    value: bytes


@dataclass
class StringTable:
    """A named string table with its metadata and current items.

    Attributes:
        index: Table index assigned at creation time.
        name: Table name (e.g. ``"instancebaseline"``).
        items: Mapping of item index → (key, value) tuple.
        user_data_fixed_size: If True, all values have the same bit width.
        user_data_size_bits: Bit width of each value when fixed-size.
        flags: Table flags bitmask.
        varint_bit_counts: If True, value sizes are encoded as ubit_var.
    """

    index: int
    name: str
    items: dict[int, tuple[str, bytes]] = field(default_factory=dict)
    user_data_fixed_size: bool = False
    user_data_size_bits: int = 0
    flags: int = 0
    varint_bit_counts: bool = False


class StringTables:
    """Container for all string tables registered during a replay.

    Attributes:
        tables: Mapping of table index → StringTable.
        name_index: Mapping of table name → table index.
    """

    def __init__(self) -> None:
        self.tables: dict[int, StringTable] = {}
        self.name_index: dict[str, int] = {}
        self._next_index: int = 0

    def add(self, table: StringTable) -> None:
        """Register a StringTable in the container.

        Args:
            table: The StringTable to register.
        """
        self.tables[table.index] = table
        self.name_index[table.name] = table.index

    def get_by_name(self, name: str) -> StringTable | None:
        """Return the table with the given name, or None if not found.

        Args:
            name: The table name to look up.

        Returns:
            The StringTable, or None.
        """
        idx = self.name_index.get(name)
        if idx is None:
            return None
        return self.tables.get(idx)

    def get_by_id(self, table_id: int) -> StringTable | None:
        """Return the table with the given index, or None if not found.

        Args:
            table_id: The integer table index.

        Returns:
            The StringTable, or None.
        """
        return self.tables.get(table_id)


# ---------------------------------------------------------------------------
# Core parser
# ---------------------------------------------------------------------------


def parse_string_table(
    buf: bytes,
    num_updates: int,
    name: str,
    user_data_fixed_size: bool,
    user_data_size_bits: int,
    flags: int,
    varint_bit_counts: bool,
) -> list[StringTableItem]:
    """Parse a string table data blob into a list of item updates.

    Each update contains an index, an optional key, and an optional value.
    Keys may reference a 32-entry history ring buffer for prefix compression.
    Values may be Snappy-compressed when ``flags & 0x1`` and the compression
    bit is set.

    Args:
        buf: Raw bytes from the string table message's ``string_data`` field.
        num_updates: Number of entries to read.
        name: Table name (used only for error messages).
        user_data_fixed_size: If True, values have a fixed bit width.
        user_data_size_bits: Fixed value width in bits (when user_data_fixed_size).
        flags: Table flags; bit 0 enables per-entry compression.
        varint_bit_counts: If True, value byte sizes are encoded as ubit_var.

    Returns:
        List of StringTableItem updates in parse order.
    """
    if not buf:
        return []

    items: list[StringTableItem] = []
    r = BitReader(buf)
    index = -1
    keys: list[str] = []

    for _ in range(num_updates):
        key = ""
        value = b""

        # Index: increment or absolute
        if r.read_boolean():
            index += 1
        else:
            index = r.read_varuint32() + 1

        # Key
        if r.read_boolean():
            if r.read_boolean():
                # History prefix reference
                pos = r.read_bits(5)
                size = r.read_bits(5)
                suffix = r.read_string()
                if pos < len(keys):
                    s = keys[pos]
                    key = (s[:size] if size <= len(s) else s) + suffix
                else:
                    key = suffix
            else:
                key = r.read_string()

            # Maintain ring buffer of last _KEY_HISTORY_SIZE keys
            if len(keys) >= _KEY_HISTORY_SIZE:
                keys.pop(0)
            keys.append(key)

        # Value
        if r.read_boolean():
            is_compressed = False
            if user_data_fixed_size:
                bit_size = user_data_size_bits
            else:
                if flags & 0x1:
                    is_compressed = r.read_boolean()
                bit_size = r.read_ubit_var() * 8 if varint_bit_counts else r.read_bits(17) * 8

            value = r.read_bits_as_bytes(bit_size)
            if is_compressed:
                value = snappy.decompress(value)

        items.append(StringTableItem(index=index, key=key, value=value))

    return items


# ---------------------------------------------------------------------------
# Message handlers
# ---------------------------------------------------------------------------


def handle_create(msg: object, string_tables: StringTables) -> StringTable:
    """Process a CSVCMsg_CreateStringTable message.

    Creates a new StringTable, parses its initial items (decompressing the
    data blob if necessary), and registers it in *string_tables*.

    Args:
        msg: A ``CSVCMsg_CreateStringTable`` protobuf message object.
        string_tables: The StringTables container to update.

    Returns:
        The newly created StringTable.
    """
    name: str = msg.name  # type: ignore[attr-defined]
    user_data_fixed_size: bool = msg.user_data_fixed_size  # type: ignore[attr-defined]
    user_data_size_bits: int = msg.user_data_size_bits  # type: ignore[attr-defined]
    flags_val: int = msg.flags  # type: ignore[attr-defined]
    varint_bit_counts: bool = msg.using_varint_bitcounts  # type: ignore[attr-defined]
    num_entries: int = msg.num_entries  # type: ignore[attr-defined]
    data_compressed: bool = msg.data_compressed  # type: ignore[attr-defined]
    buf: bytes = msg.string_data  # type: ignore[attr-defined]

    # Decompress the entire data blob if flagged
    if data_compressed:
        if buf[:4] == b"LZSS":
            raise NotImplementedError("LZSS decompression not supported (old replay)")
        buf = snappy.decompress(buf)

    table = StringTable(
        index=string_tables._next_index,
        name=name,
        user_data_fixed_size=user_data_fixed_size,
        user_data_size_bits=user_data_size_bits,
        flags=flags_val,
        varint_bit_counts=varint_bit_counts,
    )

    parsed = parse_string_table(
        buf,
        num_entries,
        name,
        user_data_fixed_size,
        user_data_size_bits,
        flags_val,
        varint_bit_counts,
    )
    for item in parsed:
        table.items[item.index] = (item.key, item.value)

    string_tables.tables[table.index] = table
    string_tables.name_index[name] = table.index
    string_tables._next_index += 1

    return table


def handle_update(msg: object, string_tables: StringTables) -> StringTable:
    """Process a CSVCMsg_UpdateStringTable message.

    Merges updated items into the existing table.  Key and value updates
    are applied independently: a blank key leaves the existing key intact.

    Args:
        msg: A ``CSVCMsg_UpdateStringTable`` protobuf message object.
        string_tables: The StringTables container to update.

    Returns:
        The updated StringTable.

    Raises:
        KeyError: If the referenced table index does not exist.
    """
    table_id: int = msg.table_id  # type: ignore[attr-defined]
    num_changed: int = msg.num_changed_entries  # type: ignore[attr-defined]
    buf: bytes = msg.string_data  # type: ignore[attr-defined]

    table = string_tables.get_by_id(table_id)
    if table is None:
        raise KeyError(f"string table {table_id} not found")

    parsed = parse_string_table(
        buf,
        num_changed,
        table.name,
        table.user_data_fixed_size,
        table.user_data_size_bits,
        table.flags,
        table.varint_bit_counts,
    )

    for item in parsed:
        idx = item.index
        if idx in table.items:
            existing_key, existing_value = table.items[idx]
            new_key = item.key if item.key else existing_key
            new_value = item.value if item.value else existing_value
            table.items[idx] = (new_key, new_value)
        else:
            table.items[idx] = (item.key, item.value)

    return table
