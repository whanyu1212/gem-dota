# API Reference

Auto-generated from source docstrings. All public classes and functions
in gem follow [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

| Module | Contents |
|---|---|
| [BitReader](reader.md) | Low-level bit/byte/varint reader |
| [DemoStream](stream.md) | Outer message stream iterator |
| [parse\_send\_tables](sendtable.md) | Send table parser — Serializer, Field, FieldType |
| [find\_decoder](field_decoder.md) | Field type → decoder dispatch, QuantizedFloatDecoder |
| [read\_field\_paths](field_path.md) | Huffman field path decoder, FieldPath |
| [StringTables](string_table.md) | String table creation, updates, key-history decoder |
| [EntityManager](entities.md) | Entity lifecycle, EntityOp, typed field accessors |
| [ReplayParser](parser.md) | High-level parse driver — wires all subsystems |
| [GameEventManager](game_events.md) | Game event schema registration and typed dispatch |
| [CombatLogProcessor](combatlog.md) | Combat log entry decoding and dispatch |
