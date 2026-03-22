# Replay Parser

This page answers your question directly: yes, a frontend framework docs site can host a real parser tab.

<ReplayParserPanel />

## How this works

1. Select a `.dem` replay file.
2. The docs frontend uploads it to your parser API endpoint.
3. The endpoint parses with `gem` and returns a JSON summary.
4. This page renders the response directly.

## Notes

- Browser-only parsing is possible in theory but not practical right now for this Python stack.
- API-backed parsing is the shortest path to a production-ready docs-integrated tool.

## Local backend for this page

```bash
uv run python examples/replay_api_server.py --port 8787
```

Then set the endpoint field to `http://127.0.0.1:8787/api/parse`.
