"""Check the pinned Dota 2 protobuf snapshot against its GitHub upstream."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOCK_PATH = REPO_ROOT / "proto-upstream.lock.json"
_SHA_RE = re.compile(r"[0-9a-f]{40}")
_REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
_REQUIRED_KEYS = ("repository", "branch", "path", "commit", "tree")


class ProtoUpdateError(RuntimeError):
    """Raised when the lock or upstream response cannot be trusted."""


@dataclass(frozen=True)
class UpstreamState:
    """Resolved upstream commit and directory tree."""

    commit: str
    tree: str


def _require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ProtoUpdateError(f"lock field {key!r} must be a non-empty string")
    return value


def _validate_sha(value: str, field: str) -> str:
    if not _SHA_RE.fullmatch(value):
        raise ProtoUpdateError(f"lock field {field!r} must be a lowercase 40-character SHA")
    return value


def load_lock(path: Path) -> dict[str, Any]:
    """Read and validate an upstream lock file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProtoUpdateError(f"lock file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProtoUpdateError(f"lock file is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ProtoUpdateError("lock file must contain a JSON object")
    if data.get("schema_version") != 1:
        raise ProtoUpdateError("lock field 'schema_version' must be 1")

    for key in _REQUIRED_KEYS:
        _require_string(data, key)

    repository = data["repository"]
    if not _REPOSITORY_RE.fullmatch(repository):
        raise ProtoUpdateError("lock field 'repository' must use the owner/name form")

    upstream_path = data["path"]
    if (
        upstream_path.startswith("/")
        or upstream_path.endswith("/")
        or any(part in {"", ".", ".."} for part in upstream_path.split("/"))
    ):
        raise ProtoUpdateError("lock field 'path' must be a normalized repository-relative path")

    _validate_sha(data["commit"], "commit")
    _validate_sha(data["tree"], "tree")
    return data


def _api_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "gem-dota-proto-watcher",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        raise ProtoUpdateError(f"GitHub API returned HTTP {exc.code} for {url}") from exc
    except URLError as exc:
        raise ProtoUpdateError(f"GitHub API request failed for {url}: {exc.reason}") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ProtoUpdateError(f"GitHub API returned invalid JSON for {url}") from exc


def resolve_upstream(lock: dict[str, Any], token: str | None = None) -> UpstreamState:
    """Resolve the newest commit touching the configured path and its tree SHA."""
    repository = lock["repository"]
    params = urlencode({"sha": lock["branch"], "path": lock["path"], "per_page": 1})
    commits_url = f"https://api.github.com/repos/{repository}/commits?{params}"
    commits = _api_json(commits_url, token)
    if not isinstance(commits, list) or not commits:
        raise ProtoUpdateError("GitHub API returned no commits for the configured path")
    first_commit = commits[0]
    if not isinstance(first_commit, dict) or not isinstance(first_commit.get("sha"), str):
        raise ProtoUpdateError("GitHub commits response did not contain a commit SHA")
    commit = _validate_sha(first_commit["sha"], "upstream commit")

    current_tree = commit
    traversed: list[str] = []
    for component in lock["path"].split("/"):
        tree_url = f"https://api.github.com/repos/{repository}/git/trees/{current_tree}"
        tree_listing = _api_json(tree_url, token)
        if not isinstance(tree_listing, dict) or not isinstance(tree_listing.get("tree"), list):
            raise ProtoUpdateError("GitHub tree response did not contain a tree listing")
        if tree_listing.get("truncated") is True:
            raise ProtoUpdateError(
                "GitHub tree response was truncated; refusing an incomplete result"
            )

        matches = [
            entry
            for entry in tree_listing["tree"]
            if isinstance(entry, dict)
            and entry.get("path") == component
            and entry.get("type") == "tree"
        ]
        traversed.append(component)
        if len(matches) != 1 or not isinstance(matches[0].get("sha"), str):
            partial_path = "/".join(traversed)
            raise ProtoUpdateError(f"configured path {partial_path!r} was not found as a directory")
        current_tree = _validate_sha(matches[0]["sha"], "upstream tree")

    tree = current_tree
    return UpstreamState(commit=commit, tree=tree)


def build_outputs(lock: dict[str, Any], upstream: UpstreamState) -> dict[str, str]:
    """Build stable GitHub Actions outputs for a resolved state."""
    repository_url = f"https://github.com/{lock['repository']}"
    old_commit = lock["commit"]
    return {
        "changed": str(upstream.tree != lock["tree"]).lower(),
        "old_commit": old_commit,
        "old_tree": lock["tree"],
        "commit": upstream.commit,
        "tree": upstream.tree,
        "old_commit_url": f"{repository_url}/commit/{old_commit}",
        "commit_url": f"{repository_url}/commit/{upstream.commit}",
        "compare_url": f"{repository_url}/compare/{old_commit}...{upstream.commit}",
        "source_url": f"{repository_url}/tree/{upstream.commit}/{quote(lock['path'], safe='/')}",
    }


def write_github_outputs(path: Path, outputs: dict[str, str]) -> None:
    """Append trusted single-line values to a GitHub Actions output file."""
    lines: list[str] = []
    for key, value in outputs.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ProtoUpdateError(f"unsafe GitHub output name: {key!r}")
        if "\n" in value or "\r" in value:
            raise ProtoUpdateError(f"GitHub output {key!r} must be a single line")
        lines.append(f"{key}={value}\n")
    with path.open("a", encoding="utf-8") as output_file:
        output_file.writelines(lines)


def update_lock(path: Path, commit: str, tree: str) -> None:
    """Atomically update the pinned commit and tree in a validated lock file."""
    data = load_lock(path)
    data["commit"] = _validate_sha(commit, "commit")
    data["tree"] = _validate_sha(tree, "tree")

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as temporary_file:
            temporary_name = temporary_file.name
            json.dump(data, temporary_file, indent=2)
            temporary_file.write("\n")
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK_PATH, help="upstream lock path")
    parser.add_argument(
        "--github-output",
        action="store_true",
        help="write single-line values to the file named by GITHUB_OUTPUT",
    )
    parser.add_argument(
        "--update-lock",
        action="store_true",
        help="update the lock after generation and tests have succeeded",
    )
    parser.add_argument("--commit", help="40-character commit SHA for --update-lock")
    parser.add_argument("--tree", help="40-character directory tree SHA for --update-lock")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        if args.update_lock:
            if not args.commit or not args.tree:
                raise ProtoUpdateError("--update-lock requires both --commit and --tree")
            update_lock(args.lock, args.commit, args.tree)
            print(f"Updated {args.lock} to commit {args.commit} (tree {args.tree}).")
            return 0
        if args.commit or args.tree:
            raise ProtoUpdateError("--commit and --tree are only valid with --update-lock")

        lock = load_lock(args.lock)
        upstream = resolve_upstream(lock, os.environ.get("GITHUB_TOKEN"))
        outputs = build_outputs(lock, upstream)
        status = "changed" if outputs["changed"] == "true" else "unchanged"
        print(
            f"Dota proto subtree is {status}: {lock['tree']} -> {upstream.tree} "
            f"(commit {upstream.commit})."
        )

        if args.github_output:
            output_path = os.environ.get("GITHUB_OUTPUT")
            if not output_path:
                raise ProtoUpdateError(
                    "--github-output requires the GITHUB_OUTPUT environment variable"
                )
            write_github_outputs(Path(output_path), outputs)
        return 0
    except (OSError, ProtoUpdateError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
