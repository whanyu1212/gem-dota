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
| [How Proto Parsing Works](proto-parsing-pipeline.md) | What protobuf is, and how a replay is layered: outer envelopes, inner messages, and where protobuf stops |
| [The Proto Files gem Uses](proto-files.md) | Where the `.proto` files come from, and what each of the 8 files gem reads carries |
| [Proto Field Atlas](proto-fields/index.md) | Every message and enum in all 84 proto files, field by field, grouped by whether gem uses the file |
