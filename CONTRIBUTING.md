# Contributing to gem-dota

Thank you for your interest in contributing! This document covers everything you need to get started.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Getting Help](#getting-help)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [`uv`](https://github.com/astral-sh/uv) for dependency management
- Git

### Areas Where You Can Contribute

- **Bug fixes** — fix issues reported in the issue tracker
- **New features** — implement new parsing capabilities (new entity types, field decoders, output formats)
- **Documentation** — improve concept guides, tutorials, or API docs
- **Tests** — add coverage or improve existing tests
- **Performance** — profiling and optimisation of hot paths (bit reader, entity decode loop)
- **Ideas** — propose features or improvements in discussions

## Development Setup

1. **Fork and clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/gem-dota.git
   cd gem-dota
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/whanyu1212/gem-dota.git
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

6. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

### Docs toolchain (maintainers)

Documentation is a [VitePress](https://vitepress.dev/) site under `docs/` (Node-based).
The API reference is generated from source docstrings by
`scripts/generate_vitepress_api_reference.py` (run automatically before the dev/build steps).

```bash
cd docs
npm install
npm run docs:dev      # local dev server (regenerates the API reference first)
npm run docs:build    # production build -> docs/.vitepress/dist
```

CI builds the site via `.github/workflows/docs.yml`. If you upgrade docs tooling,
open a dedicated PR with the updated `docs/package.json` / lockfile and a successful
`npm run docs:build`.

### Cutting a release (maintainers)

`scripts/release.sh <version> [--push]` automates a release. It refuses to run
unless the working tree is clean and `CHANGELOG.md` already has a `## [<version>]`
section, so add the changelog entry first. It then:

1. Rewrites the `version` field in `pyproject.toml`.
2. Runs the pre-flight checks (`ruff check`, `mypy src/gem/`, the non-integration test suite).
3. Builds the distribution artifacts (`uv build`).
4. Commits `chore(release): v<version>` and creates the `v<version>` git tag.

```bash
# Stage the release locally (commit + tag, no push)
bash scripts/release.sh 0.3.1

# Or cut and push in one step (pushes the branch and the tag)
bash scripts/release.sh 0.3.1 --push
```

Publishing to PyPI is driven by `.github/workflows/cd.yml`, which triggers on a
pushed `v*` tag. So without `--push` the script leaves the commit and tag local;
push them (`git push origin HEAD && git push origin v<version>`) when you are ready
to publish.

## How to Contribute

### Reporting Bugs

Before filing a bug report:
1. Check the [issue tracker](https://github.com/whanyu1212/gem-dota/issues) for existing reports
2. Try to reproduce with the latest version
3. If the bug involves a specific replay file, include the match ID and salt if possible (not the file itself)

A good bug report includes:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behaviour
- Error messages and tracebacks
- Python version and OS

### Suggesting Enhancements

Open a GitHub issue with:
- What you want to be able to do
- Why it's useful
- A sketch of the API if relevant

### Pull Requests

- **Discuss first** for large changes — open an issue before writing code
- **One thing per PR** — don't mix a bug fix with a refactor
- **Keep commits clean** — use imperative mood, explain the why not the what

## Coding Standards

### Style

- Formatted and linted by `ruff` (runs automatically via pre-commit)
- Type-annotated: all public functions and methods must have full annotations
- Google-style docstrings on all public classes and functions (the VitePress API reference is generated from them)
- No direct translation from Go/Java reference parsers — write idiomatic Python

### Docstring format

```python
def read_varuint32(self) -> int:
    """Read a variable-length unsigned 32-bit integer.

    Uses the standard 7-bits-per-byte continuation scheme:
    the MSB of each byte signals whether more bytes follow.

    Returns:
        Decoded unsigned integer value.

    Raises:
        BufferReadError: If the buffer is exhausted before the varint terminates.
    """
```

### Running checks manually

```bash
# Lint + autofix
uv run ruff check --fix src/ tests/

# Format
uv run ruff format src/ tests/

# Type check (src only)
uv run mypy src/gem/
```

## Testing

### Running tests

```bash
# Full suite
uv run pytest

# Single file
uv run pytest tests/binary/test_reader.py

# Single test
uv run pytest tests/binary/test_reader.py::TestReadVarUint32::test_two_bytes

# With coverage report
uv run pytest --cov=gem --cov-report=html
```

### Test markers

- `@pytest.mark.slow` — tests that require a real `.dem` file (not run in CI by default)
- `@pytest.mark.integration` — full-replay integration tests

Skip slow tests during development:
```bash
uv run pytest -m "not slow and not integration"
```

### Writing tests

- Tests live in `tests/` mirroring the module they cover; low-level binary tests
  are grouped under `tests/binary/`
- Use synthetic binary fixtures (construct minimal valid byte sequences) rather than real replay files for unit tests
- Keep committed replay fixtures truncated. Full replay fixtures stay ignored/local
  under `tests/fixtures/opendota/`; synchronize the canonical TI2026 replay with
  `uv run python scripts/sync_opendota_fixtures.py`. Use `--tier extended`,
  `--tier stress`, or `--match <id>` for broader and feature-specific coverage.
- Treat `tests/fixtures/opendota/manifest.json` as the source of truth for replay
  lifecycle, tiers, capabilities, integrity metadata, and replacements. Deprecate
  entries in the manifest instead of deleting their metadata.
- Keep map/reference images for examples, reports, and camp-zone tooling under `assets/maps/`, not `tests/fixtures/`.
- Real replay tests go in a `slow`/`integration` marked class
- Test both the happy path and error conditions

## Submitting Changes

### Before submitting

- [ ] Pre-commit hooks pass (`pre-commit run --all-files`)
- [ ] All tests pass (`uv run pytest`)
- [ ] New behaviour has test coverage
- [ ] Public API changes have updated docstrings
- [ ] Branch is up to date with `main`

### Pull request process

1. **Sync with upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open the PR on GitHub**
   - Reference related issues (`Fixes #123`)
   - Describe what changed and why
   - Note any breaking changes

4. **Respond to review feedback** — make changes, push to the same branch, the PR updates automatically

5. Once approved, a maintainer will merge

## Getting Help

- [Issue tracker](https://github.com/whanyu1212/gem-dota/issues) — bugs and feature requests
- [Discussions](https://github.com/whanyu1212/gem-dota/discussions) — questions and ideas
- Docs: `cd docs && npm install && npm run docs:dev`

## License

By contributing, you agree your contributions will be licensed under the MIT License.
