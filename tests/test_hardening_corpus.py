"""Unit tests for the GCS hardening corpus helpers, collector, and runner."""

from __future__ import annotations

import bz2
import hashlib
import io
import json
import subprocess
import sys
import urllib.error
from pathlib import Path
from typing import Any

import pytest

import gem
from gem.results.models import ParsedMatch, ParsedPlayer
from gem.state.game_clock import GameClock, GamePause
from scripts import collect_hardening_corpus as collector, run_hardening_corpus as runner

_SCRIPTS_DIR = str(Path(__file__).resolve().parent.parent / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import _hardening_gcs as gcs_mod  # noqa: E402


class FakeGcsClient(gcs_mod.GcsClient):
    """In-memory GCS fake keyed by full ``gs://`` URI."""

    def __init__(self, initial: dict[str, bytes] | None = None) -> None:
        super().__init__()
        self.objects: dict[str, bytes] = dict(initial or {})
        self.bucket_info: dict[str, Any] = {
            "location": "US-CENTRAL1",
            "storage_class": "STANDARD",
        }

    def check_access(self, bucket_uri: str) -> dict[str, Any]:
        gcs_mod.normalize_bucket_uri(bucket_uri)
        return dict(self.bucket_info)

    def exists(self, uri: str) -> bool:
        return uri in self.objects

    def download(self, uri: str, dest: Path) -> Path:
        if uri not in self.objects:
            raise gcs_mod.GcsError(f"missing object: {uri}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(self.objects[uri])
        return dest

    def upload(self, src: Path, uri: str) -> None:
        self.objects[uri] = src.read_bytes()

    def read_json(self, uri: str) -> Any:
        if uri not in self.objects:
            raise gcs_mod.GcsError(f"missing object: {uri}")
        return json.loads(self.objects[uri].decode("utf-8"))

    def write_json(self, uri: str, payload: Any) -> None:
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        self.objects[uri] = text.encode("utf-8")


class FakeOpenDotaClient(collector.OpenDotaClient):
    """In-memory OpenDota API fake."""

    def __init__(self, matches: dict[int, dict[str, Any]]) -> None:
        super().__init__(request_delay=0.0)
        self._matches = matches

    def fetch_match(self, match_id: int) -> dict[str, Any]:
        if match_id not in self._matches:
            raise collector.OpenDotaApiError(f"match {match_id} not found")
        return self._matches[match_id]


def _make_entry(
    match_id: int = 1001,
    *,
    source: str = "league-20208",
    tags: tuple[str, ...] = ("cm", "patch-61", "pro"),
    patch: int | None = 61,
    hero_ids: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
    archive_bytes: bytes | None = None,
    dem_bytes: bytes | None = None,
    opendota_bytes: bytes | None = None,
    opendota_parsed: bool = True,
) -> gcs_mod.CorpusEntry:
    raw_dem = dem_bytes if dem_bytes is not None else b"dem-payload"
    raw_archive = archive_bytes if archive_bytes is not None else bz2.compress(raw_dem)
    return gcs_mod.CorpusEntry(
        match_id=match_id,
        source=source,
        tags=tags,
        patch=patch,
        lobby_type=1 if "pro" in tags else 7,
        game_mode=23 if "turbo" in tags else (2 if "cm" in tags else 22),
        duration=2100,
        has_abandon="abandon" in tags,
        hero_ids=hero_ids,
        archive_object=f"matches/{match_id}.dem.bz2",
        opendota_object=f"matches/{match_id}.opendota.json",
        archive_size_bytes=len(raw_archive),
        archive_sha256=hashlib.sha256(raw_archive).hexdigest(),
        dem_size_bytes=len(raw_dem),
        dem_sha256=hashlib.sha256(raw_dem).hexdigest(),
        opendota_size_bytes=len(opendota_bytes) if opendota_bytes is not None else None,
        opendota_sha256=(
            hashlib.sha256(opendota_bytes).hexdigest() if opendota_bytes is not None else None
        ),
        opendota_parsed=opendota_parsed,
        fetched_at="2026-11-25T00:00:00Z",
    )


def _sample_parsed_match(match_id: int = 1001) -> ParsedMatch:
    players = [
        ParsedPlayer(
            player_id=slot,
            team=2 if slot < 5 else 3,
            hero_name=f"npc_dota_hero_hero_{slot}",
            kills=slot,
            deaths=1,
            assists=2,
            last_hits=50,
            denies=5,
            net_worth=10000,
            hero_damage=5000,
            tower_damage=500,
            hero_healing=0,
            game_times_min=[0, 60],
            gold_t_min=[0, 500],
            xp_t_min=[0, 400],
            lh_t_min=[0, 5],
            dn_t_min=[0, 1],
        )
        for slot in range(10)
    ]
    return ParsedMatch(
        match_id=match_id,
        game_start_tick=900,
        game_end_tick=2700,
        radiant_win=True,
        radiant_score=10,
        dire_score=5,
        players=players,
        game_clock=GameClock(game_start_tick=900, pauses=()),
    )


def _sample_opendota_payload(
    match_id: int = 1001,
    *,
    lobby_type: int = 1,
    game_mode: int = 2,
    duration: int = 2100,
    patch: int = 61,
    leaver_status: int = 0,
    replay_url: str | None = "http://replay.example/1001.dem.bz2",
) -> dict[str, Any]:
    players = [
        {
            "player_slot": i if i < 5 else 128 + (i - 5),
            "hero_id": i + 1,
            "kills": i,
            "deaths": 1,
            "assists": 2,
            "leaver_status": leaver_status if i == 0 else 0,
            "gold_t": [0, 500],
            "xp_t": [0, 400],
            "lh_t": [0, 5],
            "dn_t": [0, 1],
            "times": [0, 60],
        }
        for i in range(10)
    ]
    payload: dict[str, Any] = {
        "match_id": match_id,
        "duration": duration,
        "lobby_type": lobby_type,
        "game_mode": game_mode,
        "patch": patch,
        "radiant_score": 10,
        "dire_score": 5,
        "radiant_gold_adv": [0, 100],
        "players": players,
    }
    if replay_url is not None:
        payload["replay_url"] = replay_url
    return payload


class TestGcsHelpers:
    @pytest.mark.parametrize(
        ("raw", "expected", "expected_root"),
        [
            ("my-bucket", "gs://my-bucket", "gs://my-bucket"),
            ("gs://my-bucket/", "gs://my-bucket", "gs://my-bucket"),
            ("gs://my-bucket/prefix/sub/", "gs://my-bucket/prefix/sub", "gs://my-bucket"),
        ],
    )
    def test_normalize_valid_uris(self, raw: str, expected: str, expected_root: str) -> None:
        assert gcs_mod.normalize_bucket_uri(raw) == expected
        assert gcs_mod.bucket_root_uri(raw) == expected_root

    @pytest.mark.parametrize(
        "raw", ["", "   ", "s3://bucket", "https://bucket", "gs://a b", "gs://"]
    )
    def test_reject_invalid_uris(self, raw: str) -> None:
        with pytest.raises(ValueError):
            gcs_mod.normalize_bucket_uri(raw)

    def test_resolve_bucket_uses_env_fallback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(gcs_mod.CORPUS_BUCKET_ENV, "gem-test-bucket/")
        assert gcs_mod.resolve_bucket(None) == "gs://gem-test-bucket"
        assert gcs_mod.resolve_bucket("gs://override") == "gs://override"

    def test_resolve_bucket_raises_when_unset(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(gcs_mod.CORPUS_BUCKET_ENV, raising=False)
        with pytest.raises(ValueError, match="GEM_CORPUS_BUCKET"):
            gcs_mod.resolve_bucket(None)

    def test_gcs_client_ignores_stderr_warnings_on_json(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(
                cmd,
                returncode=0,
                stdout='{"location": "US-CENTRAL1"}',
                stderr="FutureWarning: Python 3.11 warning\n",
            )

        monkeypatch.setattr(subprocess, "run", fake_run)
        client = gcs_mod.GcsClient()
        assert client.check_access("gs://my-bucket/sub") == {"location": "US-CENTRAL1"}

    def test_gcs_client_exists_distinguishes_missing_from_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        responses = iter(
            [
                subprocess.CompletedProcess([], 0, stdout="gs://b/a\n", stderr=""),
                subprocess.CompletedProcess([], 1, stdout="", stderr="ERROR: matched no objects."),
                subprocess.CompletedProcess(
                    [], 1, stdout="", stderr="ERROR: 403 permission denied"
                ),
            ]
        )
        monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: next(responses))
        client = gcs_mod.GcsClient()

        assert client.exists("gs://b/a") is True
        assert client.exists("gs://b/missing") is False
        with pytest.raises(gcs_mod.GcsError, match="403 permission denied"):
            client.exists("gs://b/forbidden")

    def test_gcs_client_download_cleans_up_temp_on_failure(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="network reset")

        monkeypatch.setattr(subprocess, "run", fake_run)
        dest = tmp_path / "out.dem.bz2"
        with pytest.raises(gcs_mod.GcsError, match="network reset"):
            gcs_mod.GcsClient().download("gs://b/out.dem.bz2", dest)
        assert not dest.exists()
        assert list(tmp_path.iterdir()) == []


class TestCorpusIndex:
    def test_roundtrip_upsert_and_filters(self) -> None:
        pro = _make_entry(200, tags=("cm", "patch-61", "pro"), patch=61, hero_ids=(1, 2))
        ranked = _make_entry(100, tags=("ap", "patch-61", "ranked"), patch=61, hero_ids=(2, 3))
        turbo = _make_entry(
            300,
            tags=("patch-61", "smoke-only", "turbo"),
            patch=61,
            hero_ids=(4,),
            opendota_parsed=True,
        )

        index = gcs_mod.CorpusIndex().upsert(pro).upsert(ranked).upsert(turbo)
        reloaded = gcs_mod.CorpusIndex.from_dict(index.to_dict())

        assert [e.match_id for e in reloaded.matches] == [100, 200, 300]
        assert reloaded.covered_hero_ids() == {1, 2, 3, 4}
        assert pro.parity_eligible is True
        assert turbo.parity_eligible is False

        assert [e.match_id for e in reloaded.filter_entries(tags=["ranked"])] == [100]
        assert [e.match_id for e in reloaded.filter_entries(exclude_tags=["smoke-only"])] == [
            100,
            200,
        ]
        assert [e.match_id for e in reloaded.filter_entries(limit=2)] == [100, 200]

    def test_rejects_bad_schema_version(self) -> None:
        with pytest.raises(gcs_mod.CorpusIndexError, match="schema_version"):
            gcs_mod.CorpusIndex.from_dict({"schema_version": 99, "matches": []})


class TestCollector:
    @pytest.mark.parametrize(
        ("lobby_type", "game_mode", "duration", "leaver_status", "expected_subset"),
        [
            (1, 2, 1200, 0, {"pro", "cm", "short", "patch-61"}),
            (7, 22, 4000, 2, {"ranked", "ap", "long", "abandon", "patch-61"}),
            (0, 23, 1600, 0, {"unranked", "turbo", "smoke-only", "patch-61"}),
        ],
    )
    def test_derive_match_tags(
        self,
        lobby_type: int,
        game_mode: int,
        duration: int,
        leaver_status: int,
        expected_subset: set[str],
    ) -> None:
        payload = _sample_opendota_payload(
            lobby_type=lobby_type,
            game_mode=game_mode,
            duration=duration,
            leaver_status=leaver_status,
        )
        tags = set(collector.derive_match_tags(payload))
        assert expected_subset.issubset(tags)

    def test_greedy_selection_maximizes_heroes_and_extremes(self) -> None:
        pool = [
            collector.CandidateMatch(
                1, "s", (), duration=1000, lobby_type=7, game_mode=22, hero_ids=(1, 2)
            ),
            collector.CandidateMatch(
                2, "s", (), duration=4500, lobby_type=7, game_mode=22, hero_ids=(1, 3)
            ),
            collector.CandidateMatch(
                3,
                "s",
                (),
                duration=2200,
                lobby_type=7,
                game_mode=22,
                hero_ids=(4, 5),
                has_abandon=True,
            ),
            collector.CandidateMatch(
                4, "s", (), duration=2100, lobby_type=7, game_mode=22, hero_ids=(1, 2)
            ),
            collector.CandidateMatch(
                5, "s", (), duration=2000, lobby_type=7, game_mode=22, hero_ids=(6, 7, 8)
            ),
        ]
        chosen = collector.select_diverse_candidates(
            pool,
            limit=4,
            existing_match_ids={999},
            covered_heroes={1},
        )
        # Picks shortest (1), longest (2), abandon (3), then highest unseen hero count (5 over 4).
        assert [c.match_id for c in chosen] == [1, 2, 3, 5]

    def test_collect_match_verifies_and_uploads(self) -> None:
        dem_bytes = b"PBDEMS2\x00test-replay-bytes"
        archive_bytes = bz2.compress(dem_bytes)
        gcs = FakeGcsClient()
        opendota = FakeOpenDotaClient(
            {1001: _sample_opendota_payload(1001, lobby_type=7, game_mode=22)}
        )
        candidate = collector.CandidateMatch(
            1001, "ranked-ap", ("ranked", "ap"), 2100, 7, 22, (1, 2, 3)
        )

        outcome = collector.collect_match(
            candidate,
            bucket_uri="gs://my-bucket",
            gcs=gcs,
            opendota=opendota,
            existing_index=gcs_mod.CorpusIndex(),
            archive_downloader=lambda _url: archive_bytes,
        )

        assert outcome.status == "uploaded"
        assert outcome.entry is not None
        assert outcome.entry.archive_sha256 == hashlib.sha256(archive_bytes).hexdigest()
        assert outcome.entry.dem_sha256 == hashlib.sha256(dem_bytes).hexdigest()
        assert "gs://my-bucket/corpus/matches/1001.dem.bz2" in gcs.objects
        uploaded_od = gcs.objects["gs://my-bucket/corpus/matches/1001.opendota.json"]
        assert outcome.entry.opendota_size_bytes == len(uploaded_od)
        assert outcome.entry.opendota_sha256 == hashlib.sha256(uploaded_od).hexdigest()

    def test_collect_match_handles_corrupt_archive_without_crashing(self) -> None:
        gcs = FakeGcsClient()
        opendota = FakeOpenDotaClient({1002: _sample_opendota_payload(1002)})
        candidate = collector.CandidateMatch(1002, "manual", (), None, None, None, ())

        outcome = collector.collect_match(
            candidate,
            bucket_uri="gs://my-bucket",
            gcs=gcs,
            opendota=opendota,
            existing_index=gcs_mod.CorpusIndex(),
            archive_downloader=lambda _url: b"not-a-valid-archive",
        )

        assert outcome.status == "failed"
        assert "decompression failed" in outcome.detail
        assert gcs.objects == {}

    def test_api_key_never_leaks_in_http_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def fail_urlopen(req: Any, **kwargs: Any) -> Any:
            raise urllib.error.HTTPError(
                req.full_url,
                404,
                "Not Found",
                hdrs=None,
                fp=io.BytesIO(b""),  # type: ignore[arg-type]
            )

        monkeypatch.setattr(collector.urllib.request, "urlopen", fail_urlopen)
        client = collector.OpenDotaClient(
            api_key="super-secret-token", request_delay=0.0, max_retries=0
        )
        with pytest.raises(collector.OpenDotaApiError) as exc_info:
            client.fetch_match(12345)
        assert "super-secret-token" not in str(exc_info.value)

    def test_mirror_manifest_checks_decompressed_sha(self, tmp_path: Path) -> None:
        dem_bytes = b"verified-dem-content"
        archive_bytes = bz2.compress(dem_bytes)
        manifest_path = tmp_path / "manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "matches": [
                        {
                            "match_id": 5001,
                            "name": "active-one",
                            "dem": "5001.dem",
                            "status": "active",
                            "tier": "canonical",
                            "capabilities": ["short-match"],
                            "replay_url": "http://replay.example/5001.dem.bz2",
                            "artifact_url": None,
                            "dem_size_bytes": len(dem_bytes),
                            "dem_sha256": hashlib.sha256(dem_bytes).hexdigest(),
                            "replaced_by": None,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        gcs = FakeGcsClient()
        outcomes = collector.mirror_manifest_fixtures(
            bucket_uri="gs://my-bucket",
            gcs=gcs,
            manifest_path=manifest_path,
            archive_downloader=lambda _url: archive_bytes,
        )
        assert len(outcomes) == 1
        assert outcomes[0].status == "uploaded"
        assert gcs.objects["gs://my-bucket/fixtures/5001.dem.bz2"] == archive_bytes

        # Second call skips because object already exists in GCS.
        second = collector.mirror_manifest_fixtures(
            bucket_uri="gs://my-bucket",
            gcs=gcs,
            manifest_path=manifest_path,
            archive_downloader=lambda _url: b"should-not-be-called",
        )
        assert second[0].status == "skipped"

    def test_discover_parsed_public_matches_classifies_modes(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        client = collector.OpenDotaClient(request_delay=0.0)
        responses = iter(
            [
                [{"match_id": 500}, {"match_id": 499}, {"match_id": 498}],
                {
                    "rows": [
                        {
                            "match_id": 500,
                            "duration": 2100,
                            "lobby_type": 7,
                            "game_mode": 22,
                            "radiant_team": [1, 2],
                            "dire_team": [3, 4],
                        },
                        {
                            "match_id": 499,
                            "duration": 1400,
                            "lobby_type": 0,
                            "game_mode": 23,
                            "radiant_team": [5],
                            "dire_team": [6],
                        },
                        {
                            "match_id": 498,
                            "duration": 1500,
                            "lobby_type": 4,
                            "game_mode": 1,
                            "radiant_team": [7],
                            "dire_team": [8],
                        },
                    ]
                },
            ]
        )
        monkeypatch.setattr(client, "get_json", lambda _url: next(responses))
        found = client.discover_parsed_public_matches(pages=1)
        assert [(c.match_id, c.source, c.tags, c.hero_ids) for c in found] == [
            (500, "ranked-ap", ("ranked", "ap"), (1, 2, 3, 4)),
            (499, "turbo", ("turbo", "smoke-only"), (5, 6)),
        ]

    def test_collector_main_check_bucket_and_dry_run(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        fake_gcs = FakeGcsClient()
        monkeypatch.setattr(collector, "GcsClient", lambda: fake_gcs)

        assert collector.main(["--bucket", "gs://my-bucket", "--check-bucket"]) == 0
        assert "GCS OK: gs://my-bucket" in capsys.readouterr().out

        fake_od = FakeOpenDotaClient({})
        monkeypatch.setattr(
            fake_od,
            "discover_league_matches",
            lambda _league_id: [
                collector.CandidateMatch(10, "league-20208", ("pro", "cm"), 1800, 1, 2, (1, 2, 3))
            ],
        )
        monkeypatch.setattr(collector, "OpenDotaClient", lambda **_kwargs: fake_od)

        assert (
            collector.main(
                [
                    "--bucket",
                    "gs://my-bucket",
                    "--league",
                    "20208",
                    "--league-limit",
                    "5",
                    "--dry-run",
                ]
            )
            == 0
        )
        out = capsys.readouterr().out
        assert "Selected 1 match(es)" in out
        assert "Hero coverage: 0 existing -> 3 (+3 new)" in out


class TestRunner:
    def test_invariants_pass_on_clean_match_and_catch_violations(self) -> None:
        entry = _make_entry(1001)
        clean = _sample_parsed_match(1001)
        assert runner.check_match_invariants(clean, entry) == []

        broken = _sample_parsed_match(9999)
        broken.players[0].kills = -3
        broken.players[1].game_times_min = [60, 0]
        broken.game_clock = GameClock(game_start_tick=900, pauses=(GamePause(950, 900),))
        issues = runner.check_match_invariants(broken, entry)
        assert any("match_id mismatch" in issue for issue in issues)
        assert any("negative kills" in issue for issue in issues)
        assert any("non-monotonic game_times_min" in issue for issue in issues)

    def test_sync_corpus_entry_uses_cache_and_repairs_corruption(self, tmp_path: Path) -> None:
        dem_bytes = b"sample-dem"
        archive_bytes = bz2.compress(dem_bytes)
        stale_od = b'{"match_id": 1001}'
        fresh_od = b'{"match_id": 1001, "radiant_gold_adv": [0, 100]}'
        entry = _make_entry(
            1001,
            archive_bytes=archive_bytes,
            dem_bytes=dem_bytes,
            opendota_bytes=stale_od,
            opendota_parsed=False,
        )
        gcs = FakeGcsClient(
            {
                "gs://b/corpus/matches/1001.dem.bz2": archive_bytes,
                "gs://b/corpus/matches/1001.opendota.json": stale_od,
            }
        )
        corpus_dir = tmp_path / "corpus"

        archive_path, od_path = runner.sync_corpus_entry(
            entry, corpus_dir=corpus_dir, bucket_uri="gs://b", gcs=gcs
        )
        assert archive_path.read_bytes() == archive_bytes
        assert od_path.read_bytes() == stale_od

        # Corrupt local archive cache and verify sync re-downloads cleanly.
        archive_path.write_bytes(b"corrupted")
        runner.sync_corpus_entry(entry, corpus_dir=corpus_dir, bucket_uri="gs://b", gcs=gcs)
        assert archive_path.read_bytes() == archive_bytes

        # Re-collecting with --force updates GCS JSON + index metadata -> cache refreshes.
        gcs.objects["gs://b/corpus/matches/1001.opendota.json"] = fresh_od
        refreshed_entry = _make_entry(
            1001,
            archive_bytes=archive_bytes,
            dem_bytes=dem_bytes,
            opendota_bytes=fresh_od,
            opendota_parsed=True,
        )
        runner.sync_corpus_entry(
            refreshed_entry, corpus_dir=corpus_dir, bucket_uri="gs://b", gcs=gcs
        )
        assert od_path.read_bytes() == fresh_od

        # Legacy entry (no opendota_sha256) still refreshes when cached JSON is unparsed.
        od_path.write_bytes(stale_od)
        legacy_entry = _make_entry(
            1001,
            archive_bytes=archive_bytes,
            dem_bytes=dem_bytes,
            opendota_bytes=None,
            opendota_parsed=True,
        )
        runner.sync_corpus_entry(legacy_entry, corpus_dir=corpus_dir, bucket_uri="gs://b", gcs=gcs)
        assert od_path.read_bytes() == fresh_od

    def test_evaluate_match_runs_api_checks_and_parity(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        dem_bytes = b"fake-dem-bytes"
        archive_bytes = bz2.compress(dem_bytes)
        entry = _make_entry(1001, archive_bytes=archive_bytes, dem_bytes=dem_bytes)

        archive_path = tmp_path / "1001.dem.bz2"
        archive_path.write_bytes(archive_bytes)
        od_path = tmp_path / "1001.opendota.json"
        od_path.write_text(json.dumps(_sample_opendota_payload(1001)), encoding="utf-8")

        monkeypatch.setattr(gem, "parse", lambda _path: _sample_parsed_match(1001))

        outcome = runner.evaluate_match(entry, archive_path, od_path, run_api_checks=True)
        assert outcome.ok is True, (outcome.stage_errors, outcome.invariants)
        assert outcome.parity_audited is True
        assert outcome.parity_results["match.radiant_score"].matched == 1
        assert outcome.parity_results["player.kills"].matched == 10

    def test_evaluate_match_skips_parity_for_smoke_only_turbo(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        dem_bytes = b"fake-turbo-dem"
        archive_bytes = bz2.compress(dem_bytes)
        entry = _make_entry(
            2002,
            tags=("patch-61", "smoke-only", "turbo"),
            archive_bytes=archive_bytes,
            dem_bytes=dem_bytes,
        )
        archive_path = tmp_path / "2002.dem.bz2"
        archive_path.write_bytes(archive_bytes)
        od_path = tmp_path / "2002.opendota.json"
        od_path.write_text(
            json.dumps(_sample_opendota_payload(2002, game_mode=23)), encoding="utf-8"
        )

        monkeypatch.setattr(gem, "parse", lambda _path: _sample_parsed_match(2002))

        outcome = runner.evaluate_match(entry, archive_path, od_path, run_api_checks=False)
        assert outcome.ok is True
        assert outcome.parity_audited is False
        assert outcome.parity_results == {}

    def test_main_local_offline_run_and_regression_exit_code(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        dem_bytes = b"offline-dem"
        archive_bytes = bz2.compress(dem_bytes)
        entry = _make_entry(1001, archive_bytes=archive_bytes, dem_bytes=dem_bytes)
        corpus_dir = tmp_path / "corpus"
        (corpus_dir / "matches").mkdir(parents=True)
        (corpus_dir / "matches" / "1001.dem.bz2").write_bytes(archive_bytes)
        (corpus_dir / "matches" / "1001.opendota.json").write_text(
            json.dumps(_sample_opendota_payload(1001)), encoding="utf-8"
        )
        (corpus_dir / "index.json").write_text(
            json.dumps(gcs_mod.CorpusIndex(matches=(entry,)).to_dict()),
            encoding="utf-8",
        )

        monkeypatch.setattr(gem, "parse", lambda _path: _sample_parsed_match(1001))

        out_dir = tmp_path / "out"
        rc = runner.main(
            [
                "--local-corpus-dir",
                str(corpus_dir),
                "--workers",
                "1",
                "--out-dir",
                str(out_dir),
            ]
        )
        assert rc == 0
        summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
        assert summary["matches_passed"] == 1
        assert (out_dir / "parity.json").exists()
        assert (out_dir / "report.txt").exists()

        # Simulate a baseline with a higher match count -> --compare must return 1.
        baseline_path = tmp_path / "baseline.json"
        parity = json.loads((out_dir / "parity.json").read_text(encoding="utf-8"))
        parity["match.radiant_score"]["matched"] = 2
        baseline_path.write_text(json.dumps(parity), encoding="utf-8")

        rc_regressed = runner.main(
            [
                "--local-corpus-dir",
                str(corpus_dir),
                "--workers",
                "1",
                "--skip-api-checks",
                "--compare",
                str(baseline_path),
            ]
        )
        assert rc_regressed == 1

    def test_batch_check_exception_still_persists_run_artifacts(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        dem_bytes = b"offline-dem"
        archive_bytes = bz2.compress(dem_bytes)
        od_bytes = json.dumps(_sample_opendota_payload(1001)).encode("utf-8")
        entry = _make_entry(
            1001,
            archive_bytes=archive_bytes,
            dem_bytes=dem_bytes,
            opendota_bytes=od_bytes,
        )
        corpus_dir = tmp_path / "corpus"
        (corpus_dir / "matches").mkdir(parents=True)
        (corpus_dir / "matches" / "1001.dem.bz2").write_bytes(archive_bytes)
        (corpus_dir / "matches" / "1001.opendota.json").write_bytes(od_bytes)
        (corpus_dir / "index.json").write_text(
            json.dumps(gcs_mod.CorpusIndex(matches=(entry,)).to_dict()),
            encoding="utf-8",
        )

        monkeypatch.setattr(gem, "parse", lambda _path: _sample_parsed_match(1001))
        monkeypatch.setattr(
            gem,
            "parse_many_to_parquet",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(FileNotFoundError("no parquet")),
        )

        out_dir = tmp_path / "out-batch-fail"
        rc = runner.main(
            [
                "--local-corpus-dir",
                str(corpus_dir),
                "--workers",
                "1",
                "--skip-api-checks",
                "--batch-check",
                "1",
                "--out-dir",
                str(out_dir),
            ]
        )
        assert rc == 1
        summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
        assert summary["matches_passed"] == 1
        assert summary["batch_check_ok"] is False
        assert "FileNotFoundError" in summary["batch_check_note"]
        assert (out_dir / "parity.json").exists()
        assert (out_dir / "report.txt").exists()
