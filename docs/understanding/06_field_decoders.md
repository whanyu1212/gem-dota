# Field Decoders

Once a field path has been decoded (see [Field Paths](05_field_paths.md)), the next bits
in the stream encode the field's **value**. Each field type has a corresponding
**decoder** — a callable `(BitReader) -> value` that reads exactly the right number of
bits and returns a typed Python object.

---

## Decoder assignment

Decoders are resolved **once** at send-table parse time and stored directly on each
`Field` object. The hot path — applying entity deltas tick after tick — just calls
`field.decoder(reader)` with no dispatch overhead.

The resolution logic is in `src/gem/field_decoder.py`.

---

## Dispatch chain

`find_decoder(field)` resolves a decoder using the following priority order:

1. **Type factories** — for types that carry parameters (quantized floats, arrays,
   vectors). Checked first because they need the field's metadata.
2. **Name overrides** — for specific `var_name` values that require non-default
   decoding regardless of type (e.g. `m_flSimulationTime` uses a coord float).
3. **Type table** — for simple type strings like `bool`, `int32`, `uint32`, etc.
4. **Default** — `varuint32` for any unrecognised type.

---

## Simple decoders

| Field type | Decoder | Bits read |
|---|---|---|
| `bool` | 1 bit | `reader.read_bit()` |
| `uint8`, `uint32`, `uint64` | varuint | variable |
| `int8`, `int32`, `int64` | zigzag varuint | variable |
| `float32` (noscale) | 32-bit IEEE 754 | 32 |
| `CUtlString`, `CUtlStringToken` | null-terminated | variable |
| `char` | null-terminated | variable |

---

## Quantized floats

`CNetworkedQuantizedFloat` is the most important float type in the replay. It encodes
a float in a fixed number of bits, mapped to a `[low_value, high_value]` range.

The field's `bit_count`, `low_value`, `high_value`, and `encode_flags` control the
exact encoding. The decoder is built at schema-parse time by `QuantizedFloatDecoder`:

```
resolution = (high_value - low_value) / ((1 << bit_count) - 1)
decoded_value = low_value + (raw_integer * resolution)
```

`encode_flags` can add special round-up, round-down, or zero-is-special behaviour.

The mana field for heroes, `m_flMana`, is a `CNetworkedQuantizedFloat`. So is
`m_flAttackSpeed`, `m_flCooldown` on abilities, and many position components.

---

## Coord floats

The `coord` encoder (set via `field.encoder == "coord"`) uses Source 2's coordinate
encoding, which is neither IEEE 754 nor quantized. It encodes:

```
1 bit:  has integer part?
1 bit:  has fractional part?
1 bit:  sign bit

if has integer part: read 14 bits (integer component)
if has fractional part: read 5 bits (fractional component, scale = 1/32)
```

This encoding is efficient for small coordinate values (typical Dota map positions are
in the range -9000 to 9000 in game units).

---

## QAngle (rotation angles)

`QAngle` fields encode pitch, yaw, and roll as three floats. Three encoding variants
exist, selected by the `encoder` and `bit_count` on the field:

- **Fixed bits**: all three components read as fixed-bit-width values.
- **Coord**: all three components decoded as coord floats.
- **Pitch+yaw only**: only pitch and yaw are sent; roll is always 0.

---

## Vector types

`Vector`, `Vector2D`, and `Vector4D` encode 2, 3, or 4 float components respectively.
The component decoder is the float factory applied to each component — it may be a
coord float, a quantized float, or a noscale float depending on the field's encoder.

Example: `CBodyComponent.m_vecX`, `.m_vecY`, `.m_vecZ` are 3-component Vectors where
each component uses the coord encoder.

---

## Handle fields

`CHandle< T >` and `CGameSceneNodeHandle` fields encode entity handles — 32-bit
integers that reference another entity by its (index, serial) pair:

```
handle = (serial << 14) | index
```

To resolve a handle to an entity:

```python
entity = entity_manager.get_by_handle(handle)
```

Returns `None` if the entity does not exist or the serial does not match the current
occupant of that slot.

---

## Array and sub-serialiser fields

For `FIXED_ARRAY` and `VARIABLE_ARRAY` fields, the decoder is applied per element. The
element count for variable arrays is maintained in the entity's field state — the path
`[array_field_index, 65535]` stores the current length.

For `FIXED_TABLE` / `VARIABLE_TABLE` fields (sub-serialisers), the field path descends
into the sub-serialiser's field list and each sub-field has its own decoder.

---

## gem implementation

Source: `src/gem/field_decoder.py`

The public API is:

```python
from gem.field_decoder import find_decoder

decoder = find_decoder(field)   # called once at schema-parse time
value   = decoder(bit_reader)   # called on every entity update
```

Reference: `refs/manta/field_decoder.go`
