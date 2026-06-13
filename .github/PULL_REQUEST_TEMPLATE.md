## Summary

- 

## Rationale

- 

## Testing

- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`
- [ ] `uv run mypy src`
- [ ] `uv run pytest tests/ -m "not integration"`
- [ ] Docs build, if docs changed

## Notes

- [ ] Generated protobuf files under `src/gem/proto/` were not edited manually.
- [ ] Large replay artifacts are not committed unless explicitly required for tests.
- [ ] Secrets and local credentials are not included.
