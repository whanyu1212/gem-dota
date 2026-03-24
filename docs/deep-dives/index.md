# Deep Dives

Implementation-focused walkthroughs of gem replay internals.

Read these in order for full parser internals:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Stream Layer](stream-layer.md)
3. [Parser Layer](parser-layer.md)
4. [SendTable Layer](sendtable-layer.md)
5. [State Reconstruction Layer](state-layer.md)
6. [Event Normalization Layer](event-layer.md)
7. [Extractors Layer](extractors-layer.md)
8. [Match Assembly Layer](match-assembly-layer.md)
9. [Replay Edge Cases](replay-edge-cases.md)

---

| Layer | What it covers |
|---|---|
| [Stream Layer](stream-layer.md) | Outer replay container framing, ticks, compression handling |
| [Parser Layer](parser-layer.md) | Outer/inner dispatch orchestration and ordering guarantees |
| [SendTable Layer](sendtable-layer.md) | Serializer schema build, field models, decoder wiring |
| [State Reconstruction Layer](state-layer.md) | String tables, baselines, entity lifecycle and state mutation |
| [Event Normalization Layer](event-layer.md) | Game-event schema dispatch and S1/S2 combat-log normalization |
| [Extractors Layer](extractors-layer.md) | Domain-specific timelines/time-series: players, objectives, wards, draft, courier, teamfights |
| [Match Assembly Layer](match-assembly-layer.md) | Merge extractor outputs into ParsedMatch and project to DataFrames |

Cross-cutting reference:

1. [Replay Edge Cases](replay-edge-cases.md): duplicate hero entities, within-tick sampling, truncated replays, schema drift, and heuristic limits
