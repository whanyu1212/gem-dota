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

### Docs toolchain stability (maintainers)

We currently pin the docs stack to avoid accidental major-version breakage:
- `mkdocs>=1.6.1,<2.0.0`
- `mkdocs-material>=9.7.4,<10.0.0`
- `mkdocstrings[python]>=1.0.3,<2.0.0`

Please do not perform broad docs dependency upgrades without review (especially major versions).  
If you intentionally upgrade docs tooling, open a dedicated PR that includes:
- updated pins + lockfile,
- `uv run mkdocs build --strict` output,
- any required migration notes in this file.

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
- Google-style docstrings on all public classes and functions (used by mkdocstrings for API docs)
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
        BufferError: If the buffer is exhausted before the varint terminates.
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
uv run pytest tests/test_reader.py

# Single test
uv run pytest tests/test_reader.py::TestVarints::test_varuint32_multibyte

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

- Tests live in `tests/` mirroring the module they cover
- Use synthetic binary fixtures (construct minimal valid byte sequences) rather than real replay files for unit tests
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
- Docs: `uv run mkdocs serve`

## License

By contributing, you agree your contributions will be licensed under the MIT License.
