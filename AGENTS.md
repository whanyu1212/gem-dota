# Repository Guidelines

## Project Structure & Module Organization
`gem` is a Python Source 2 Dota 2 replay parser.
- `src/gem/`: core parser pipeline (`stream.py`, `reader.py`, `sendtable.py`, `entities.py`, `parser.py`) plus extractors and output builders.
- `src/gem/proto/dota2/`: generated protobuf modules (`*_pb2.py`, `*_pb2.pyi`). Do not edit manually.
- `proto_definitions/dota2/`: source `.proto` files.
- `tests/`: unit and integration tests (`-m integration` for replay-backed tests).
- `scripts/`: utility scripts (proto compile, replay fetch, validation, docs API generation).
- `docs/`: VitePress documentation site.
- `refs/`: reference implementations (`manta`, `clarity`, `parser`) used for behavior parity.

## Build, Test, and Development Commands
- `uv sync --group dev`: install project and developer dependencies.
- `uv run python scripts/compile_protos.py`: regenerate protobuf Python modules.
- `uv run ruff check .` / `uv run ruff format .`: lint and format code.
- `uv run mypy src`: static type checking.
- `uv run pytest tests/ -m "not integration"`: fast local test loop.
- `uv run pytest tests/ -m integration`: integration suite (requires replay fixtures).
- `cd docs && npm run docs:dev` / `npm run docs:build`: serve/build docs.

## Coding Style & Naming Conventions
- Python 3.10+, 4-space indentation, type hints on public APIs.
- Use `snake_case` for functions/variables/modules and `PascalCase` for classes/dataclasses.
- Keep parser changes surgical; avoid unrelated refactors.
- Prefer `dataclass` for structured outputs and clear docstrings for public interfaces.
- Never hand-edit generated protobuf files under `src/gem/proto/dota2/`.

## Testing Guidelines
- Framework: `pytest`.
- Naming: files `test_*.py`, tests `test_*`.
- Add focused regression tests with parser changes, especially for string table/entity ordering, combat log normalization, and extractor output shape.
- Run targeted tests for touched modules before opening a PR.

## Commit & Pull Request Guidelines
- Use short, imperative commit messages (e.g., `fix draft hero id normalization`).
- Keep each commit scoped to one concern.
- PRs should include: summary, rationale, test commands run, and results.
- Link issues when relevant; include screenshots for docs/UI changes.

## Security & Configuration Tips
- Keep secrets out of the repo (`STEAM_API_KEY` via environment variables only).
- Do not commit large replay artifacts unless explicitly required for tests.
- For parser logic changes, verify behavior against `refs/manta/`, then cross-check `refs/clarity/` and `refs/parser/`.
