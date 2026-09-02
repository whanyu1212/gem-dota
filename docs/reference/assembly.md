# Results Assembly

Assembles extractor output into a `ParsedMatch`.

---

## Generated API

## Module `gem.results.assembly`

Match assembly — wires extractor outputs into a :class:`ParsedMatch`.

Source: [src/gem/results/assembly.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/assembly.py#L1)

### Top-level functions

### `build_parsed_match`

```python
def build_parsed_match(parser: ReplayParser, player_ext: PlayerExtractor, obj_ext: ObjectivesExtractor, ward_ext: WardsExtractor, courier_ext: CourierExtractor, draft_ext: DraftExtractor, combat_agg: _CombatAggregator, all_entries: list[CombatLogEntry], chat_entries: list[ChatEntry], smoke_events: list[SmokeEvent] | None = None, vision_modifier_events: list[VisionModifierEvent] | None = None, neutral_item_finds: list[NeutralItemFoundEvent] | None = None, interval_ext: IntervalExtractor | None = None) -> ParsedMatch
```

Assemble a :class:`ParsedMatch` from extractor state after a completed parse.

Source: [src/gem/results/assembly.py:815](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/assembly.py#L815)
