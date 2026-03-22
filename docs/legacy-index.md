---
hide:
  - navigation
  - toc
---

# Gem

<div class="hero-tagline" markdown>
**Gem** reads Dota 2 `.dem` replay files and turns them into structured Python objects —
named after the *Gem of True Sight*, which reveals what is hidden.
</div>

<div class="hero-actions" markdown>
<a class="VPButton medium brand" href="guides/01_quickstart.md">Get started</a>
<a class="VPButton medium alt" href="reference/index.md">API Reference</a>
</div>

---

## What you can do

<div class="grid cards" markdown>

-   **Parse in seconds**

    ---

    A typical 45-minute replay parses in 2–4 seconds in pure Python — no compiled
    extensions required.

    ```python
    import gem
    match = gem.parse("my_replay.dem")
    ```

-   **Full match data**

    ---

    Players, draft, combat log, wards, objectives, teamfights, couriers, smoke events,
    aegis, chat — everything in one call.

    [Full Match Data →](guides/04_match_data.md)

-   **Export anywhere**

    ---

    Convert to pandas DataFrames, JSON, or Parquet with a single function.

    ```python
    gem.parse_to_dataframe("replay.dem")
    gem.parse_to_json("replay.dem", indent=2)
    gem.parse_to_parquet("replay.dem", "./out")
    ```

-   **Batch processing**

    ---

    Parse hundreds of replays in parallel using all CPU cores.
    Failed replays are captured, not raised.

    ```python
    gem.parse_many_to_parquet("replays/", "./out", workers=8)
    ```

-   **Exact ward coordinates**

    ---

    Ward placements carry precise map coordinates extracted from the entity stream —
    not approximations.

    [Ward extractor →](reference/extractors/wards.md)

-   **CLI included**

    ---

    Parse, export, and batch-process replays directly from the terminal —
    no Python code needed.

    ```bash
    python -m gem batch replays/ --format parquet --output ./out
    ```

</div>

---

## Where to start

::: tabs
== I want to use it

Jump to the [Guides](guides/index.md) — start with the
[Quickstart](guides/01_quickstart.md) for install-to-KDA in 10 lines, or go
straight to [Full Match Data](guides/04_match_data.md) for a walkthrough of
everything in `ParsedMatch`.


== I want to understand the format

Read [Understanding the Format](understanding/index.md). It explains the Dota 2
replay binary format from scratch — magic bytes, outer message framing, protobuf
payloads, the entity delta system, field path Huffman coding, string tables, and
the combat log. Each page builds on the previous.


== I need the API

Go to the [API Reference](reference/index.md). Every public class and function
has a Google-style docstring.
:::

---

## Install

::: tabs
== pip

```bash
pip install gem-dota
```


== uv

```bash
uv add gem-dota
```
:::

Python 3.10 or later required.
