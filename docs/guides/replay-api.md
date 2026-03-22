# Replay API Contract

The `Replay Parser` tab posts `multipart/form-data` to your parser backend.

## Request

- Method: `POST`
- Content type: `multipart/form-data`
- Form field: `replay` (`.dem` file)

## Expected response

```json
{
  "ok": true,
  "summary": {
    "match_id": 8234567890,
    "duration_sec": 2718,
    "radiant_win": false,
    "players": [
      {"slot": 0, "hero": "npc_dota_hero_axe", "kills": 4, "deaths": 8, "assists": 17}
    ]
  }
}
```

On failure:

```json
{
  "ok": false,
  "error": "parse failed: truncated replay"
}
```

## Suggested backend choices

- Python API service that uses `gem.parse()` and returns a compact JSON summary.
- Queue-based parser worker if replay files are large and parse latency spikes.
- Pre-signed upload + async parse for production-scale usage.

## Local development server

```bash
uv run python examples/replay_api_server.py --port 8787
```

The VitePress parser page can then point to `http://127.0.0.1:8787/api/parse`.
