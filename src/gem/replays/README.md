# gem.replays

`gem.replays` is the *bulk + acquisition* layer. It does not parse the binary
format itself — it sits on top of `gem.parse()` and answers two operational
questions the core parser leaves open:

1. **Where does a replay come from?** (`fetch.py`) — download and decompress a
   `.dem` from the OpenDota / Valve CDN given a match ID, and optionally enrich a
   parsed match with Game-Coordinator scalars from the OpenDota API.
2. **How do I parse many at once?** (`batch.py`) — run `gem.parse()` across a
   directory of replays using a process pool, returning per-replay results or one
   concatenated set of DataFrames.

Everything here is exposed through the public API (`gem.fetch_replay`,
`gem.parse_many`, …); most callers never import `gem.replays` directly.

## Mental Model

```text
fetch_replay(match_id)  ──►  match.dem  ──►  gem.parse(path)  ──►  ParsedMatch
                                                  ▲
parse_many([paths]) ──── ProcessPoolExecutor ─────┘   (one worker per replay)
```

- **`fetch.py`** is I/O over the network: resolve the replay URL, stream-download
  the bz2 blob, decompress to `.dem`. `enrich_with_api_rates` / `apply_api_rates`
  are a separate opt-in step that can overwrite OpenDota's published
  `hero_damage`/`tower_damage`/`hero_healing`/`gpm`/`xpm` scalars on a
  `ParsedMatch`. Complete current replays already provide the same exact values
  in their embedded `CMsgDOTAMatch` postgame summary.
- **`batch.py`** is CPU parallelism: each replay is parsed in its own process
  (`_parse_one`), so a failed replay yields a `ParseResult` with the exception
  rather than aborting the whole run. `parse_many_to_dataframe` /
  `parse_many_to_parquet` add the concat/export step on top.

## What this layer does NOT do

- It does **not** decode the binary format — that is `binary` → `schema` →
  `state` → `parser`. `replays` only orchestrates calls to the finished
  `gem.parse()`.
- It does **not** require network access for `batch.py`. Only `fetch.py` reaches
  the network; bulk parsing of local files is fully offline.
- `apply_api_rates` only overlays the supplied GC scalars, and it is opt-in.
  Plain `gem.parse()` never calls the network.

## Pitfalls

- **Parquet needs an engine.** `parse_many_to_parquet` requires `pyarrow`
  (recommended) or `fastparquet` in the environment.
- **Process-pool pickling.** Workers parse in separate processes, so results are
  pickled back; keep custom post-processing out of the worker path.
- **API enrichment is rate-limited and best-effort.** `fetch_opendota_match`
  hits the public OpenDota API; for private/high-MMR matches it may return
  nothing, which is exactly the case `gem` exists to handle offline.

## When to add code here

Add to `replays/` when the work is about **acquiring** replays or **scaling**
parsing across many of them — not when it is about *how* a single replay is
decoded (that belongs in the core pipeline) or *what* is extracted from one
(that belongs in `extractors` / `analysis`).
