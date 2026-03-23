# Deployment Note: Mode 2 Replay Parser

_Date: March 23, 2026_

## Goal

Support interactive docs replay parsing where users upload `.dem` files and we process them server-side (async job flow).

## Decision (current)

Use **Mode 2** (API-backed parsing), not static pre-generated examples.

## Recommended low-load hosting setup

1. **Docs**: Cloudflare Pages (static VitePress)
2. **Parser API**: Render Free Web Service (Python)
3. **Queue**: Redis (add when moving from sync to async jobs)
4. **Worker**: separate process for parse/report jobs
5. **Artifacts**: object storage (S3/R2/GCS) for report outputs

## Why this setup

- Lowest-cost practical path for Python parser backend + static docs.
- Clean separation: docs frontend remains static, parsing runs on backend.
- Scales from MVP to async architecture without redoing frontend contracts.

## Known tradeoffs

- Free-tier backends can cold-start when idle.
- Full HTML report generation can take minutes on larger replays.
- Need async jobs for better UX once report generation is enabled in UI.

## API direction (v1)

- `POST /api/v1/reports/jobs` (upload replay, create async job)
- `GET /api/v1/reports/jobs/{job_id}` (status/progress)
- `GET /api/v1/reports/jobs/{job_id}/result` (summary + artifact links)
- `GET /api/v1/reports/jobs/{job_id}/artifacts/{name}` (download)

## Effort estimate (rough)

1. MVP API + docs integration: 2-4 days
2. Most tab parity in VitePress: 1-2 weeks
3. Full parity (including heavier visual tabs): 2-4 weeks total

## Deferred checklist

- [ ] Validate up-to-date free-tier limits before provisioning.
- [ ] Define upload size limits and retention TTL.
- [ ] Add rate limits and basic auth if endpoint is public.
- [ ] Implement async worker flow and job persistence.
- [ ] Add monitoring (error logs + job failure metrics).

## References

- `docs/replay-parser.md`
- `docs/guides/replay-api.md`
- `examples/replay_api_server.py`
- `examples/match_report.py`
