# String Tables

Besides entities, the server keeps a second kind of shared state: **string
tables**. Each one is a numbered list of entries, and each entry has a name and,
optionally, some data. Entities and combat-log lines often refer to "entry 42 of
table X" instead of spelling a name out. gem keeps these tables in
`src/gem/state/string_table.py`.

Examples come from the committed fixture
`tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem`, which ends during the
draft. Larger numbers come from a full 99-minute replay, `8855242704`.

## What's in them

The fixture creates 18 tables; a full match creates about 20. Most are small, and
gem reads three of them:

| Table | Entries (fixture) | What an entry is | gem reads it |
|---|---:|---|---|
| `instancebaseline` | 21 | An entity class's default field values. The name is the class ID, the data an encoded field update ([part 5](entity-lifecycle.md)). | Yes: every new entity starts from it |
| `CombatLogNames` | 1, growing during the match | A name that combat-log entries refer to by number, such as a hero, item, or ability | Yes: to name combat-log entries |
| `EntityNames` | 313 | A unit or ability name, such as `creep_siege` | Yes: to name units |
| `ModifierNames` | 3,237 | The name of a buff or debuff, such as `modifier_lua` | No |
| `ActiveModifiers` | 0 at first; about 1,800 late in a match | One active buff or debuff: which unit has it, what it is, who cast it, how long it lasts | No |
| `userinfo` | 64 slots, 26 in use | A connected player or observer | No |

The rest (`lightstyles`, `EffectDispatch`, `ResponseKeys`, and others) hold
engine details gem doesn't need.

## Creating and updating a table

Three inner messages change the tables:

- **`svc_ClearAllStringTables`** removes every table. Replays send it once, before
  any table exists.
- **`svc_CreateStringTable`** creates a table with all its initial entries. It
  also fixes the table's settings: whether every entry's data has the same size,
  and whether data can be compressed. The whole entry list may be
  Snappy-compressed. Very old replays (game builds up to 962) used LZSS
  compression instead, which gem doesn't support.
- **`svc_UpdateStringTable`** changes some entries of an existing table.

Tables are numbered in the order they're created, and updates refer to them by
that number. All 18 of the fixture's tables are created in the signon packets at
the very start. The full replay sends 57,910 updates; 98% of them are for `ActiveModifiers`, as buffs come
and go.

Replays also contain periodic snapshots of every table. gem skips them, as Manta
does, because the create and update messages already keep the tables current.

## The entry format

Like entity data, a table's entries are packed as bits, not protobuf. Each entry
has three parts:

1. **Which entry.** One bit: either the next entry, or a jump forward. A jump
   gives a varint, and the index moves forward by that number plus two.
2. **Its name**, if present. Either a plain string, or a shorthand that reuses the
   start of a recent name (below).
3. **Its data**, if present. If the table allows compression, one bit says
   whether this entry's data is Snappy-compressed. Then comes the size in bytes
   (a `ubit_var`; tables created without varint sizes use 17 bits instead) and
   the bytes themselves. Tables whose data all has the same size skip the size.

The `instancebaseline` entries hold the most data. The first one, for class 3086
(`CIngameEvent_DotaPlus`), is 918 bytes.

## Name compression

Many names in a table share a beginning: `alpha_wolf_critical_strike` and
`alpha_wolf_command_aura`. So a name can say "take the first *n* characters of one
of the last 32 entries' names, then add this". It gives a position (0 to 31,
oldest first), a length (0 to 31), and the new ending.

From the fixture's `EntityNames` table:

| Entry | Sent | Name |
|---:|---|---|
| 20 | `alpha_wolf_critical_strike` | `alpha_wolf_critical_strike` |
| 21 | position 20, first 12 characters, then `ommand_aura` | `alpha_wolf_command_aura` |

Two details matter:

- **Every entry counts** towards the last 32, including entries whose update
  didn't include a name. Those contribute the name they already have.
- **An entry's name never changes** once it exists. An update only replaces its
  data, and an update without data clears it.

## Getting the rules right

gem originally followed Manta, which treats a jump as an absolute position
(`varint + 1`), counts only entries that sent a name, and keeps old data when an
update sends none. Clarity follows the three rules on this page instead. On a
table's first entry, the two ways of reading a jump agree. After that, they
disagree.

The replay itself settles it. `ActiveModifiers` names each entry by its own
index: entry 289 is named `"289"`. So every entry carries its own answer. In the
99-minute replay, 279 entries were reached by a jump. Clarity's rules put all 279
at the index their name says; Manta's rules put none there.

The error only showed in `ActiveModifiers`. The table was still exact ten minutes
into the match; after that, as buffs expired and the server began jumping between
entries, it fell apart.
By the end, gem's copy held 42 of the 1,774 active modifiers in the right place.
The three tables gem reads never used a jump in the replays checked, so gem's
results were unaffected. gem now uses Clarity's rules, and a test checks every
`ActiveModifiers` entry of a full replay against its name.

## Where the time goes

About 2 seconds of a 110-second parse, nearly all of it `ActiveModifiers`
updates. There is nothing here worth moving to native code.

## Try it

```python
from gem.parser import ReplayParser

parser = ReplayParser("tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem")
parser.parse()   # logs "Replay stream ended early": the fixture is truncated

tables = parser.string_tables
names = tables.get_by_name("EntityNames")
print(len(names.items))                        # 313
print(names.items[20][0])                      # alpha_wolf_critical_strike
print(names.items[21][0])                      # alpha_wolf_command_aura

baselines = tables.get_by_name("instancebaseline")
class_id, defaults = baselines.items[0]
print(class_id, len(defaults))                 # 3086 918
print(parser.entity_manager.classes_by_id[int(class_id)].name)   # CIngameEvent_DotaPlus
```

Each table's `items` maps an entry's index to its `(name, data)` pair.

## Where to go next

- [Part 5: Entity Lifecycle](entity-lifecycle.md): how `instancebaseline` defaults
  are applied to new entities.
- [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md): where these
  messages sit in a replay.
- [String Tables reference](../reference/string_table.md): `StringTables`,
  `StringTable`, `parse_string_table`, `handle_create`, `handle_update`.
- Source: `src/gem/state/string_table.py`.
