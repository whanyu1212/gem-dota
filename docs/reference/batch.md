# Batch Processing

Parallel multi-replay parsing via `ProcessPoolExecutor`.
Each worker process parses one replay independently, so performance scales with CPU cores.

!!! note "Memory"
    `parse_many_to_parquet` writes and discards each replay immediately, keeping memory
    usage flat regardless of batch size. `parse_many_to_dataframe` holds all results in
    memory until concatenation — prefer `parse_many_to_parquet` for large batches.

!!! tip "Parquet dependency"
    Parquet output requires an optional engine. Install `pyarrow` (recommended):
    ```bash
    pip install pyarrow
    ```

---

::: gem.batch
    options:
      members:
        - ParseResult
        - parse_many
        - parse_many_to_dataframe
        - parse_many_to_parquet
      show_source: true
