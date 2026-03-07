# examples/

Each script in this directory corresponds to an implementation phase from `STRATEGY.md`.
As more phases are completed, new examples unlock progressively deeper replay data.

Run any example from the project root (with the venv activated):

```bash
python examples/phase1_stream.py                          # uses default fixture
python examples/phase1_stream.py path/to/your.dem        # or supply your own
```

## Progress

| Script | Phase | What it demonstrates | Status |
|---|---|---|---|
| `phase1_stream.py` | 1 | Header validation, message type breakdown, tick range, throughput | ✅ |
| `phase2_schema.py` | 2 | SendTable parsing, serializer/field tree, decoder resolution | 🔜 |
| `phase3_entities.py` | 3 | Entity create/update/delete, reading hero HP/position/gold per tick | 🔜 |
| `phase4_events.py` | 4 | Game events, combat log entries (damage, kills, abilities) | 🔜 |
| `phase5_extract.py` | 5 | Per-player time-series: gold, XP, LH/DN, ward placements | 🔜 |
| `phase6_output.py` | 6 | Full `ParsedMatch` → DataFrame, JSON export | 🔜 |
