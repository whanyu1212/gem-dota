# Proto Cookbook

Concept-first walkthroughs for readers who want to understand how replay parsing works,
without starting from bit-level implementation details.

Proto Cookbook pages focus on practical mental models:

- What each stage does.
- Why each stage exists.
- What data shape enters and exits each stage.

---

| Recipe | What you will learn |
|---|---|
| [How Proto Parsing Works](proto-parsing-pipeline.md) | End-to-end parse flow, inner/outer protobuf boundaries, and what each outer message contains |
| [Full Proto Dota2 Catalog](proto-dota2-catalog.md) | Exhaustive inventory of every `proto_definitions/dota2/*.proto` file and all `message`/`enum` declarations |
| [Proto Field Atlas](proto-fields/index.md) | One page per proto file with collapsible message/enum sections and per-field breakdown (tag, type, label, oneof, notes) |
