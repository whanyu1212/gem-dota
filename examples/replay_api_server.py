"""Minimal API server for the VitePress Replay Parser tab.

Usage:
    uv run python examples/replay_api_server.py --port 8787

Then set the docs parser endpoint to:
    http://127.0.0.1:8787/api/parse
"""

from __future__ import annotations

import argparse
import cgi
import json
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import IO, Any, cast

import gem


class ReplayAPIHandler(BaseHTTPRequestHandler):
    """Handle replay parsing requests."""

    server_version = "GemReplayAPI/0.1"

    def _write_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        """Handle CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        """Parse an uploaded replay and return a compact JSON summary."""
        if self.path != "/api/parse":
            self._write_json(404, {"ok": False, "error": "Route not found"})
            return

        content_type = self.headers.get("Content-Type", "")
        mime, _ = cgi.parse_header(content_type)
        if mime != "multipart/form-data":
            self._write_json(
                400,
                {"ok": False, "error": "Expected multipart/form-data with a 'replay' field"},
            )
            return

        form = cgi.FieldStorage(
            fp=cast(IO[Any], self.rfile),
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": content_type,
            },
        )

        if "replay" not in form:
            self._write_json(400, {"ok": False, "error": "Missing 'replay' file field"})
            return

        replay_part = form["replay"]
        if isinstance(replay_part, list):
            replay_part = replay_part[0]

        if replay_part.file is None:
            self._write_json(400, {"ok": False, "error": "Uploaded file content is empty"})
            return

        raw = replay_part.file.read()
        if not raw:
            self._write_json(400, {"ok": False, "error": "Uploaded file content is empty"})
            return

        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".dem", delete=False) as temp_file:
                temp_file.write(raw)
                temp_path = Path(temp_file.name)

            match = gem.parse(temp_path)
            players = [
                {
                    "slot": player.player_id,
                    "hero": player.hero_name,
                    "kills": player.kills,
                    "deaths": player.deaths,
                    "assists": player.assists,
                }
                for player in match.players
                if player.hero_name
            ]
            payload = {
                "ok": True,
                "summary": {
                    "match_id": match.match_id,
                    "duration_sec": int(match.duration_seconds),
                    "radiant_win": match.radiant_win,
                    "players": players,
                },
            }
            self._write_json(200, payload)
        except Exception as exc:  # pragma: no cover - example server
            self._write_json(500, {"ok": False, "error": f"parse failed: {exc}"})
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run a local replay parse API server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8787, help="Bind port")
    return parser.parse_args()


def main() -> None:
    """Start the HTTP server."""
    args = parse_args()
    server = HTTPServer((args.host, args.port), ReplayAPIHandler)
    print(f"Replay API listening on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
