#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <version> [--push]"
  echo "Example: $0 0.1.1 --push"
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

VERSION="$1"
PUSH=false
if [[ "${2:-}" == "--push" ]]; then
  PUSH=true
fi

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([a-zA-Z0-9\.\-]+)?$ ]]; then
  echo "Error: version must look like 0.1.1 (optionally with suffix). Got: $VERSION"
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Error: working tree is not clean. Commit/stash changes first."
  exit 1
fi

if [[ ! -f "CHANGELOG.md" ]]; then
  echo "Error: CHANGELOG.md not found."
  exit 1
fi

if ! grep -q "^## \\[$VERSION\\]" CHANGELOG.md; then
  echo "Error: CHANGELOG.md is missing a section for v$VERSION."
  echo "Add a heading like: ## [$VERSION] - YYYY-MM-DD"
  exit 1
fi

VERSION="$VERSION" python - <<'PY'
from pathlib import Path
import os
import re

version = os.environ["VERSION"]
path = Path("pyproject.toml")
text = path.read_text(encoding="utf-8")
new_text, n = re.subn(
    r'^version = ".*"$',
    f'version = "{version}"',
    text,
    count=1,
    flags=re.MULTILINE,
)
if n != 1:
    raise SystemExit("Could not find exactly one version line in pyproject.toml")
path.write_text(new_text, encoding="utf-8")
print(f"Updated pyproject.toml version -> {version}")
PY

echo "Running quick checks..."
uv run ruff check src tests examples scripts
uv run mypy src/gem/
uv run pytest tests/ -m "not integration" -q

echo "Building dist artifacts..."
uv build

git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): v$VERSION"
git tag "v$VERSION"

if [[ "$PUSH" == "true" ]]; then
  git push origin HEAD
  git push origin "v$VERSION"
  echo "Pushed branch and tag v$VERSION."
else
  echo "Release commit and tag created locally."
  echo "To publish via GitHub Actions CD, run:"
  echo "  git push origin HEAD"
  echo "  git push origin v$VERSION"
fi