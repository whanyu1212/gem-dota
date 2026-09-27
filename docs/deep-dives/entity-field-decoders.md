# How Entities Are Decoded, Part 3: Field Decoders

[Part 2](entity-field-paths.md) showed how an entity update says *which* fields
changed. This part covers the rest of the update: the **new value** of each of those
fields. A **field decoder** is the small function that reads one value from the
bitstream. gem's decoders live in `src/gem/schema/field_decoder/`.

This page uses the crash course's sections on
[varints](../cookbook/bits-and-bytes-primer.md#_6-variable-length-integers),
[signed numbers](../cookbook/bits-and-bytes-primer.md#_5-signed-numbers-and-why-python-needs-masks),
and [quantized floats](../cookbook/bits-and-bytes-primer.md#_7-floats-and-how-to-store-them-in-fewer-bits).
Examples come from the committed fixture
`tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem`.

## The same update, with its values

Part 2 decoded the field paths of a game-rules update sent during the draft. After
those 57 bits of paths come the values, one per path, in the same order:

| Field | Type | Decoder | Bits | Value |
|---|---|---|---:|---|
| `m_pGameRules.m_iFoWFrameNumber` | `int32` | signed varint | 8 | 14 |
| `m_pGameRules.m_nHeroPickState` | `DOTA_HeroPickState` | default (unsigned varint) | 8 | 7 |
| `m_pGameRules.m_flHeroPickStateTransitionTime` | `GameTime_t` | raw 32-bit float | 32 | 0.0 |
| `m_pGameRules.m_iPlayerIDsInControl` | `uint64`, encoder `fixed64` | fixed 64-bit integer | 64 | 2 |
| `m_pGameRules.m_iCaptainPlayerIDs.0001` | `PlayerID_t[2]` | default (unsigned varint) | 8 | 16 |

The whole update is 177 bits: 57 bits of paths, then 120 bits of values. Nothing
in the bitstream says where one value ends and the next begins. Each decoder simply
reads as many bits as its format needs, so every decoder must be exactly right, or
all later values in the packet come out wrong.

A detail for readers of raw values: player IDs are stored doubled, so the captain ID
16 is player 8.

## How a decoder is chosen

Each field's decoder is chosen **once**, when the schema is built (part 1), by
`find_decoder()` in `type_resolver.py`. The choice depends on the field's base type,
and for some types also on its encoder name and bit count. The order is:

1. **Types whose settings matter.** A factory looks at the field's metadata:

   | Base type | Decoder |
   |---|---|
   | `float32` | encoder `coord` → coord; `simtime` → simulation time; `runetime` → rune time; no bit count, or 0 or ≥ 32 bits → raw 32-bit float; otherwise → quantized float |
   | `CNetworkedQuantizedFloat` | quantized float |
   | `Vector`, `Vector2D`, `Vector4D`, `VectorWS` | the `float32` decoder above, once per component; a 3-component `Vector` with encoder `normal` → packed unit vector |
   | `QAngle` | see [Angles](#angles-and-vectors) |
   | `uint64`, `CStrongHandle` | encoder `fixed64` → fixed 64-bit; otherwise 64-bit varint |
   | `CHandle`, `CEntityHandle` | unsigned varint |

2. **Types with a fixed decoder:** `bool` → 1 bit; `int8` to `int64` → signed
   varint; `uint8` to `uint32`, `color32`, `Color`, `CUtlStringToken` → unsigned
   varint; `char`, `CUtlString`, `CUtlSymbolLarge` → string; `GameTime_t` → raw
   32-bit float; `HeroFacetKey_t` → 64-bit varint.
3. **Anything else** → unsigned varint. That covers enums such as
   `DOTA_HeroPickState`, and ID types such as `PlayerID_t`, as in the update above.

Elements of variable-length arrays are chosen from the element type alone, using
steps 2 and 3. These tables are identical to Manta's `field_decoder.go`.

## The decoder families

In the fixture's schema, the 1,881 fields that hold values directly use these
decoders:

| Decoder | Fields | Reads |
|---|---:|---|
| Raw 32-bit float | 441 | exactly 32 bits, as an IEEE float |
| Signed varint | 416 | a zigzag varint |
| Boolean | 359 | 1 bit |
| Unsigned varint | 288 | a varint |
| Default (unsigned varint) | 128 | a varint |
| Vector | 78 | 2–4 floats, each with the field's float decoder |
| String | 66 | bytes up to a zero byte, as UTF-8 |
| 64-bit varint | 45 | a varint of up to 10 bytes |
| Quantized float | 42 | a fixed number of bits scaled into a range (below) |
| Fixed 64-bit | 9 | exactly 64 bits, little-endian |
| Angle (coord form) | 4 | 3 presence bits, then a coord per present component |
| Simulation time | 3 | a varint of ticks, × 1/30 to get seconds |
| Coord | 1 | a sign, integer, and 1/32 fraction (below) |
| Rune time | 1 | 4 bits, reinterpreted as float bits (as Manta does) |

### Positions: a cell plus an offset

Positions show how several of these combine. An entity's position lives in its
`CBodyComponent` (part 1) as two parts per axis:

- `m_cellX`: a `uint16` read as an unsigned varint. It picks a 128-unit square of the
  map.
- `m_vecX`: a quantized float, 13 bits over 0–256, giving the offset inside the
  square in steps of 1/32 of a unit.

gem's extractors combine them as `cell × 128 + offset`. At the end of the fixture a
player pawn has cells `(130, 122)` and offsets `(69.1875, 203.84375)`: world position
`(16709.1875, 15819.84375)`. Splitting the position this way means a unit moving
inside its square only sends the small offset.

### Coords

A **coord** (`BitReader.read_coord()`) stores a number as two presence bits (integer
part? fraction part?), then a sign bit, a 14-bit integer part (stored minus one), and
a 5-bit fraction in 1/32 steps. Zero costs just the two presence bits.

### Angles and vectors

A `QAngle` (pitch, yaw, roll in degrees) has three forms:

- encoder `qangle_pitch_yaw`: pitch and yaw as *n*-bit angles, roll = 0
- a bit count *n*: three *n*-bit angles, each `raw × 360 / 2ⁿ`
- otherwise: three presence bits, then a coord for each present component

`m_angRotation` in the fixture uses the third form. Vectors (`Vector`, `Vector2D`,
`Vector4D`) apply the field's float decoder to each component, so a `Vector` field
with 32 bits is three raw floats.

## Quantized floats in detail

A quantized float stores a value in a known range as a whole number of equal steps:

```text
value = low + (high − low) × stored / (2^bits − 1)
```

`m_flMana` is 20 bits over 0–65,536, so each step is about 1/16 of a mana point.

The schema can also set four **flags**. Each of the first three adds one bit before
the value, and if that bit is 1 the value is an exact special number with no further
bits:

| Flag | Extra bit means | Setup effect |
|---|---|---|
| ROUNDDOWN (1) | "exactly `low`" | the top of the range moves down by one step |
| ROUNDUP (2) | "exactly `high`" | the bottom of the range moves up by one step |
| ENCODE_ZERO (4) | "exactly 0" | none |
| ENCODE_INTEGERS (8) | (no extra bit) | range and bit count adjusted so whole numbers are exact |

When the decoder is set up, it drops a flag it doesn't need: if the plain formula
already hits `low`, `high`, or 0 exactly, the extra bit is left out. The position
offset above is an example: it has ROUNDDOWN in the schema, but after its range moves
to 0–255.96875, `low` is already exact, so the flag is dropped and each offset costs
13 bits, not 14.

That setup decides how many bits each value uses, so it must match Valve's encoder
exactly. Manta and Clarity do this arithmetic in 32-bit floats, and gem reproduces
their float32 steps for the flag decisions. It once did them in 64-bit floats, which
dropped a flag for `m_flSpriteFramerate` and would have read one bit too few per value.

The decoded **values** are a different matter: gem computes them in 64-bit floats,
which is at most about 0.0001 more precise than the reference parsers' 32-bit
results. For example, the top of a 0–1,000 range decodes to exactly 1000.0 in gem and
to 1000.00006 in float32.

## How often each decoder runs

Which decoders dominate depends on what's happening in the game. In the fixture,
which ends during the draft, raw 32-bit floats are 51% of the 64,203 decoder calls.
Over a full match (replay `8974053011`, 13.9 million calls), four
decoders make up about 92%: quantized floats 27%, signed varints 25%, unsigned varints
21%, and raw floats 20%. All four are a few bit operations each.

## Try it

This builds the decoders for the position offset and for mana, and decodes values
from hand-packed bits (`to_bytes(..., "little")` puts the lowest bits first, as
`BitReader` reads them).

```python
from gem.binary.reader import BitReader
from gem.schema.field_decoder import QuantizedFloatDecoder

offset = QuantizedFloatDecoder(bit_count=13, flags=1, low_value=None, high_value=256.0)
print(offset.bitcount, offset.flags, offset.high)              # 13 0 255.96875
print(offset.decode(BitReader((2214).to_bytes(2, "little"))))  # 69.1875

mana = QuantizedFloatDecoder(bit_count=20, flags=None, low_value=None, high_value=65536.0)
print(mana.decode(BitReader((8000).to_bytes(3, "little"))))    # 500.00047683761295
```

And the pawn's world position from the fixture:

```python
from gem.parser import ReplayParser

parser = ReplayParser("tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem")
parser.parse()   # logs "Replay stream ended early": the fixture is truncated

pawn = parser.entity_manager.find_by_class_name("CDOTAPlayerPawn")
cell_x = pawn.get_uint32("CBodyComponent.m_cellX")
offset_x = pawn.get_float32("CBodyComponent.m_vecX")
print(cell_x, offset_x, cell_x * 128 + offset_x)   # 130 69.1875 16709.1875
```

## Where to go next

- [Part 4: Field State](entity-field-state.md): where decoded values are stored,
  and how you read them back.
- [Part 2: Field Paths](entity-field-paths.md): how an update names its changed fields.
- [Field Decoders reference](../reference/field_decoder.md): the decoder functions
  and `QuantizedFloatDecoder`.
- Source: `src/gem/schema/field_decoder/` (`type_resolver.py`, `quantized_float.py`,
  `scalar_codecs.py`, `composite_codecs.py`).
