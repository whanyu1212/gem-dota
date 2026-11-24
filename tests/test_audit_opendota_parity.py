"""Tests for the offline OpenDota parity audit."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import gem
from gem.combat.log import CombatLogEntry, CombatLogType
from gem.results.models import ChatEntry, ParsedMatch, ParsedPlayer
from scripts import audit_opendota_parity as audit

_START = 900  # game_start_tick; the fallback clock is floor((tick - start) / 30)


def _match() -> ParsedMatch:
    player = ParsedPlayer(
        player_id=6,
        kills=5,
        deaths=2,
        game_times_min=[0, 60],
        gold_t_min=[0, 400],
        gold_t=[600, 610, 650],  # dense samples; OpenDota's gold_t is per minute
        item_uses={"item_tango": 2},
        max_hero_hit={"key": "npc_dota_hero_axe", "value": 300},
        lane_pos={"100": {"160": 3, "161": 1}},
    )
    player.purchase_log = [
        CombatLogEntry(
            tick=_START - 90 * 30, log_type=CombatLogType.PURCHASE, value_name="item_tango"
        )
    ]
    return ParsedMatch(
        match_id=1,
        game_start_tick=_START,
        radiant_score=10,
        players=[player],
        chat=[ChatEntry(tick=1, player_slot=6, channel="all", text="gg")],
    )


def _opendota() -> dict:
    return {
        "match_id": 1,
        "radiant_score": 10,
        "radiant_gold_adv": [0],
        "chat": [{"type": "chat", "key": "gg", "slot": 6}],
        "players": [
            {
                "player_slot": 129,
                "kills": 5,
                "deaths": 3,
                "gold_t": [0, 400],
                "times": [0, 60],
                "item_uses": {"tango": 2},
                "max_hero_hit": {
                    "key": "npc_dota_hero_axe",
                    "value": 300,
                    "slot": 6,
                    "player_slot": 129,
                },
                "purchase_log": [{"key": "tango", "time": -90}],
                "lane_pos": {"100": {"160": 3, "161": 1}},
                "only_in_opendota": 1,
            }
        ],
    }


def _audit() -> dict[str, audit.FieldResult]:
    results: dict[str, audit.FieldResult] = {}
    audit.audit_match("1", _match(), _opendota(), results)
    return results


class TestAuditMatch:
    def test_format_differences_are_normalized_away(self):
        results = _audit()

        for name in (
            "player.gold_t",
            "player.times",
            "player.item_uses",
            "player.max_hero_hit",
            "player.purchase_log",
            "player.lane_pos",
            "player.kills",
            "match.radiant_score",
            "match.chat",
        ):
            assert (results[name].matched, results[name].total) == (1, 1), name

    def test_first_blood_victim_slot_is_added_to_older_reference_json(self):
        # odota/core adds victim_player_slot when serving a match; reference
        # JSON fetched before that lacks it.
        od = {
            "players": [{"player_slot": s} for s in (0, 1, 2, 3, 4, 128, 129, 130, 131, 132)],
            "objectives": [
                {"type": "CHAT_MESSAGE_FIRSTBLOOD", "key": "6", "slot": 2},
                {"type": "building_kill", "key": "npc_dota_badguys_fort"},
            ],
        }
        objectives = audit._annotated_objectives(od)

        assert objectives[0]["victim_player_slot"] == 129
        assert "victim_player_slot" not in objectives[1]
        assert "victim_player_slot" not in od["objectives"][0]  # input left alone

    def test_teamfights_compare_the_opendota_shaped_view(self):
        from gem.extractors.fights import OpenDotaTeamfight

        fight = OpenDotaTeamfight(start=85, end=125, last_death=110, deaths=3)
        match = ParsedMatch(match_id=1, opendota_teamfights=[fight])
        match.fights = [object()] * 5  # gem's own fights are not compared
        # ParsedMatch has no ``teamfights`` field; the audit must still compare it.
        od = {"players": [], "teamfights": [audit._plain(fight)]}
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results)

        assert (results["match.teamfights"].matched, results["match.teamfights"].total) == (1, 1)

    def test_value_differences_are_recorded_with_an_example(self):
        deaths = _audit()["player.deaths"]

        assert (deaths.matched, deaths.total) == (0, 1)
        assert deaths.mismatches == {"1": 1}
        assert deaths.example == ("1", 2, 3)

    def test_only_fields_both_sides_have_are_compared(self):
        results = _audit()

        assert "player.only_in_opendota" not in results
        assert "player.gold_ledger" not in results
        assert "match.game_clock" not in results

    def test_log_times_prefer_the_entrys_own_game_time(self):
        match = _match()
        player = match.players[0]
        base = {"log_type": CombatLogType.PICKUP_RUNE, "value": 6, "rune_type": 5}
        player.runes_log = [
            CombatLogEntry(tick=_START + 30 * 10, game_time_s=9, **base),  # own time wins
            CombatLogEntry(tick=_START + 30 * 20, game_time_s=0, **base),  # zero is a time
            CombatLogEntry(tick=_START - 30 * 5, game_time_s=-6, **base),  # so is a negative
            CombatLogEntry(tick=_START + 30 * 40, **base),  # none: the tick clock
        ]
        od = _opendota()
        od["players"][0]["runes_log"] = [
            {"key": "5", "time": 9},
            {"key": "5", "time": 0},
            {"key": "5", "time": -6},
            {"key": "5", "time": 40},
        ]
        results: dict[str, audit.FieldResult] = {}

        audit.audit_match("1", match, od, results)

        assert results["player.runes_log"].matched == 1

    def test_player_slots_map_to_opendota(self):
        assert [audit.od_player_slot(i) for i in (0, 4, 5, 9)] == [0, 4, 128, 132]


class TestStaleReference:
    def test_mismatch_counts_apart_from_the_total(self):
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", _match(), _opendota(), results, frozenset({"player.deaths"}))

        deaths = results["player.deaths"]
        assert (deaths.total, deaths.mismatches, deaths.stale) == (0, {}, {"1": 1})
        assert "player.deaths: OpenDota JSON predates a rule change on 1×1" in (
            audit.format_report(results)
        )

    def test_fields_come_from_the_manifest(self, tmp_path):
        (tmp_path / "manifest.json").write_text(
            json.dumps({"matches": [{"match_id": 1, "opendota_json_predates": ["efe5794b"]}]})
        )

        assert audit.stale_fields(tmp_path, "1") == audit.RULE_CHANGES["efe5794b"]
        assert audit.stale_fields(tmp_path, "2") == frozenset()


_KNOWN_BUG = (
    audit.KnownOpenDotaBug(
        bug="meepo-aegis-reincarnation",
        killer="npc_dota_hero_dragon_knight",
        victim="npc_dota_hero_meepo",
        time=1733,
    ),
)


class TestKnownOpenDotaBug:
    def _meepo_aegis_match(self) -> tuple[ParsedMatch, dict]:
        dk = ParsedPlayer(
            player_id=2,
            hero_name="npc_dota_hero_dragon_knight",
            killed={"npc_dota_hero_meepo": 1},
            kills_log=[
                CombatLogEntry(
                    tick=_START + 30 * 1437,
                    log_type=CombatLogType.DEATH,
                    target_name="npc_dota_hero_meepo",
                    target_is_hero=True,
                )
            ],
        )
        meepo = ParsedPlayer(
            player_id=5,
            hero_name="npc_dota_hero_meepo",
            killed_by={"npc_dota_hero_dragon_knight": 1},
        )
        match = ParsedMatch(
            match_id=1,
            game_start_tick=_START,
            players=[dk, meepo],
        )
        od = {
            "match_id": 1,
            "players": [
                {
                    "player_slot": 2,
                    "hero_id": 49,
                    "killed": {"npc_dota_hero_meepo": 2},
                    "killed_by": {},
                    "kills_log": [
                        {"key": "npc_dota_hero_meepo", "time": 1437},
                        {"key": "npc_dota_hero_meepo", "time": 1733},
                    ],
                },
                {
                    "player_slot": 128,
                    "hero_id": 82,
                    "killed": {},
                    "killed_by": {"npc_dota_hero_dragon_knight": 2},
                    "kills_log": [],
                },
            ],
        }
        return match, od

    def test_strips_only_the_pinned_meepo_aegis_kill(self):
        match, od = self._meepo_aegis_match()
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results, known_bug_entries=_KNOWN_BUG)

        expected_bug = {
            "1": ["meepo-aegis-reincarnation:npc_dota_hero_dragon_knight->npc_dota_hero_meepo@1733"]
        }
        for field_name in ("player.killed", "player.killed_by", "player.kills_log"):
            res = results[field_name]
            assert (res.matched, res.total, res.mismatches, res.known_bug) == (
                2,
                2,
                {},
                expected_bug,
            )
            assert f"{field_name}: known OpenDota parser bug on 1×1" in audit.format_report(results)

    def test_slot_resolution_uses_opendota_hero_ids_not_gem_players(self):
        match, od = self._meepo_aegis_match()
        # Corrupt gem's hero_name assignment; OpenDota's reference stripping must
        # still target hero_id 49 -> 82 rather than letting gem shift it.
        match.players[0].hero_name = "npc_dota_hero_axe"
        match.players[1].hero_name = "npc_dota_hero_crystal_maiden"
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results, known_bug_entries=_KNOWN_BUG)

        for field_name in ("player.killed", "player.killed_by", "player.kills_log"):
            res = results[field_name]
            assert (res.matched, res.total, res.mismatches) == (2, 2, {})

    def test_real_kill_is_not_stripped_if_gem_drops_it(self):
        match, od = self._meepo_aegis_match()
        # Simulate gem mislabeling the real 1437 s kill as will_reincarnate=True.
        match.players[0].killed = {}
        match.players[0].kills_log = []
        match.players[1].killed_by = {}
        match.combat_log = [
            CombatLogEntry(
                tick=_START + 30 * 1437,
                log_type=CombatLogType.DEATH,
                attacker_name="npc_dota_hero_dragon_knight",
                damage_source_name="npc_dota_hero_dragon_knight",
                target_name="npc_dota_hero_meepo",
                target_is_hero=True,
                will_reincarnate=True,
            )
        ]
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results, known_bug_entries=_KNOWN_BUG)

        for field_name in ("player.killed", "player.killed_by", "player.kills_log"):
            res = results[field_name]
            assert (res.matched, res.total, res.mismatches) == (1, 2, {"1": 1})

    def test_unrelated_mismatch_on_same_player_is_still_caught(self):
        match, od = self._meepo_aegis_match()
        od["players"][0]["killed"]["npc_dota_hero_axe"] = 1  # unrelated regression
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results, known_bug_entries=_KNOWN_BUG)

        killed = results["player.killed"]
        assert (killed.matched, killed.total, killed.mismatches) == (1, 2, {"1": 1})

    def test_partial_reference_preserves_unrelated_fields(self):
        match, od = self._meepo_aegis_match()
        od["players"][0]["killed_by"] = None
        del od["players"][1]["kills_log"]
        del od["players"][1]["killed"]
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results, known_bug_entries=_KNOWN_BUG)

        assert (results["player.killed"].matched, results["player.killed"].total) == (1, 1)
        assert (results["player.kills_log"].matched, results["player.kills_log"].total) == (1, 1)
        assert (results["player.killed_by"].matched, results["player.killed_by"].total) == (1, 2)
        assert results["player.killed_by"].mismatches == {"1": 1}

    def test_normalizes_available_summaries_when_killed_by_is_absent(self):
        match, od = self._meepo_aegis_match()
        del od["players"][1]["killed_by"]
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results, known_bug_entries=_KNOWN_BUG)

        assert (results["player.kills_log"].matched, results["player.kills_log"].total) == (2, 2)
        assert (results["player.killed"].matched, results["player.killed"].total) == (2, 2)
        assert (results["player.killed_by"].matched, results["player.killed_by"].total) == (1, 1)
        assert results["player.kills_log"].known_bug == {
            "1": ["meepo-aegis-reincarnation:npc_dota_hero_dragon_knight->npc_dota_hero_meepo@1733"]
        }
        assert results["player.killed"].known_bug == {
            "1": ["meepo-aegis-reincarnation:npc_dota_hero_dragon_knight->npc_dota_hero_meepo@1733"]
        }
        assert results["player.killed_by"].known_bug == {}

    def test_entries_come_from_the_manifest(self, tmp_path):
        (tmp_path / "manifest.json").write_text(
            json.dumps(
                {
                    "matches": [
                        {
                            "match_id": 1,
                            "opendota_known_bugs": [
                                {
                                    "bug": "meepo-aegis-reincarnation",
                                    "killer": "npc_dota_hero_dragon_knight",
                                    "victim": "npc_dota_hero_meepo",
                                    "time": 1733,
                                }
                            ],
                        }
                    ]
                }
            )
        )

        assert audit.known_bugs(tmp_path, "1") == _KNOWN_BUG
        assert audit.known_bugs(tmp_path, "2") == ()

    def test_empty_gem_players_preserves_known_bug_metadata(self):
        match, od = self._meepo_aegis_match()
        match.players = []
        results: dict[str, audit.FieldResult] = {}
        audit.audit_match("1", match, od, results, known_bug_entries=_KNOWN_BUG)

        expected_bug = {
            "1": ["meepo-aegis-reincarnation:npc_dota_hero_dragon_knight->npc_dota_hero_meepo@1733"]
        }
        for field_name in ("player.killed", "player.killed_by", "player.kills_log"):
            assert results[field_name].known_bug == expected_bug
            assert results[field_name].total == 0

        report = audit.format_report(results)
        assert "1 of 4 fields match exactly: match.match_id" in report
        assert (
            "Untested (0 comparisons): player.killed, player.killed_by, player.kills_log" in report
        )

        baseline = {
            "player.killed": {"matched": 0, "total": 2, "known_bug": expected_bug},
            "player.killed_by": {"matched": 0, "total": 2, "known_bug": expected_bug},
            "player.kills_log": {"matched": 0, "total": 2, "known_bug": expected_bug},
        }
        assert audit.missing_fields(results, baseline) == [
            "player.killed",
            "player.killed_by",
            "player.kills_log",
        ]
        assert audit.regressed(results, baseline) is True

    @pytest.mark.parametrize("bad_time", [1733.75, "1733", True, None])
    def test_fractional_or_non_int_known_bug_time_raises(self, tmp_path, bad_time):
        (tmp_path / "manifest.json").write_text(
            json.dumps(
                {
                    "matches": [
                        {
                            "match_id": 99,
                            "opendota_known_bugs": [
                                {
                                    "bug": "meepo-aegis-reincarnation",
                                    "killer": "npc_dota_hero_dragon_knight",
                                    "victim": "npc_dota_hero_meepo",
                                    "time": bad_time,
                                }
                            ],
                        }
                    ]
                }
            )
        )

        with pytest.raises(ValueError, match="99"):
            audit.known_bugs(tmp_path, "99")


class TestReport:
    def test_merge_adds_counts_and_keeps_the_first_example(self):
        total = {"player.kills": audit.FieldResult(1, 2, {"a": 1}, ("a", 1, 2))}
        audit.merge_results(total, {"player.kills": audit.FieldResult(0, 1, {"b": 1}, ("b", 3, 4))})

        merged = total["player.kills"]
        assert (merged.matched, merged.total, merged.mismatches) == (1, 3, {"a": 1, "b": 1})
        assert merged.example == ("a", 1, 2)

    def test_compare_reports_improved_worse_and_newly_exact_fields(self):
        results = {
            "player.a": audit.FieldResult(5, 10, {"m": 5}),
            "player.b": audit.FieldResult(3, 10, {"m": 7}),
            "player.c": audit.FieldResult(10, 10),
        }
        baseline = {
            "player.a": {"matched": 4, "total": 10},
            "player.b": {"matched": 6, "total": 10},
            "player.c": {"matched": 9, "total": 10},
        }

        report = audit.format_report(results, baseline=baseline)

        assert "player.a" in report and "(+1)" in report
        assert "(-3)" in report
        assert "player.c" in report and "now exact (was 9/10)" in report
        assert "2 improved, 1 worse" in report


class TestCommandLine:
    def _fixtures(self, tmp_path: Path) -> tuple[Path, Path]:
        fixtures, cache = tmp_path / "fixtures", tmp_path / "gem-json"
        fixtures.mkdir()
        cache.mkdir()
        (fixtures / "1.dem").write_bytes(b"")
        (fixtures / "1.opendota.json").write_text(json.dumps(_opendota()))
        # Known only from Steam: OpenDota has no parsed data, so it is skipped.
        (fixtures / "2.dem").write_bytes(b"")
        (fixtures / "2.opendota.json").write_text(json.dumps({"radiant_gold_adv": None}))
        (cache / "1.json").write_text(gem.to_json(_match()))
        return fixtures, cache

    def test_fixture_ids_skip_matches_opendota_did_not_parse(self, tmp_path):
        fixtures, _ = self._fixtures(tmp_path)

        assert audit.fixture_ids(fixtures) == ["1"]

    def test_runs_from_cached_gem_json_and_writes_a_summary(self, tmp_path, capsys):
        fixtures, cache = self._fixtures(tmp_path)
        summary = tmp_path / "summary.json"

        code = audit.main(
            [
                "--fixtures-dir",
                str(fixtures),
                "--gem-json-dir",
                str(cache),
                "--workers",
                "1",
                "--json-out",
                str(summary),
            ]
        )

        assert code == 0
        assert "player.deaths" in capsys.readouterr().out
        assert json.loads(summary.read_text())["player.deaths"] == {
            "matched": 0,
            "total": 1,
            "mismatches": {"1": 1},
            "stale": {},
            "known_bug": {},
        }

    def test_compare_fails_when_a_field_got_worse(self, tmp_path):
        fixtures, cache = self._fixtures(tmp_path)
        baseline = tmp_path / "baseline.json"
        baseline.write_text(json.dumps({"player.deaths": {"matched": 1, "total": 1}}))

        code = audit.main(
            [
                "--fixtures-dir",
                str(fixtures),
                "--gem-json-dir",
                str(cache),
                "--workers",
                "1",
                "--compare",
                str(baseline),
            ]
        )

        assert code == 1

    def test_compare_fails_when_a_baseline_field_disappears(self, tmp_path, capsys):
        fixtures, cache = self._fixtures(tmp_path)
        baseline = tmp_path / "baseline.json"
        baseline.write_text(json.dumps({"player.renamed_away": {"matched": 1, "total": 1}}))

        code = audit.main(
            [
                "--fixtures-dir",
                str(fixtures),
                "--gem-json-dir",
                str(cache),
                "--workers",
                "1",
                "--compare",
                str(baseline),
            ]
        )

        assert code == 1
        assert "player.renamed_away" in capsys.readouterr().out

    def test_no_parsed_fixtures_is_an_error(self, tmp_path):
        assert audit.main(["--fixtures-dir", str(tmp_path)]) == 1

    def test_compare_rejects_incompatible_known_bug_baseline(self, tmp_path, capsys):
        fixtures, cache = tmp_path / "fixtures", tmp_path / "gem-json"
        fixtures.mkdir()
        cache.mkdir()
        match, od = TestKnownOpenDotaBug()._meepo_aegis_match()
        od["radiant_gold_adv"] = [0]
        (fixtures / "1.dem").write_bytes(b"")
        (fixtures / "1.opendota.json").write_text(json.dumps(od))
        (fixtures / "manifest.json").write_text(
            json.dumps(
                {
                    "matches": [
                        {
                            "match_id": 1,
                            "opendota_known_bugs": [
                                {
                                    "bug": "meepo-aegis-reincarnation",
                                    "killer": "npc_dota_hero_dragon_knight",
                                    "victim": "npc_dota_hero_meepo",
                                    "time": 1733,
                                }
                            ],
                        }
                    ]
                }
            )
        )
        (cache / "1.json").write_text(gem.to_json(match))
        # Simulate a baseline from before known_bug normalization was applied.
        baseline = tmp_path / "baseline.json"
        baseline.write_text(
            json.dumps(
                {
                    "player.killed": {"matched": 1, "total": 2},
                    "player.killed_by": {"matched": 1, "total": 2},
                    "player.kills_log": {"matched": 1, "total": 2},
                }
            )
        )

        code = audit.main(
            [
                "--fixtures-dir",
                str(fixtures),
                "--gem-json-dir",
                str(cache),
                "--workers",
                "1",
                "--compare",
                str(baseline),
            ]
        )

        assert code == 1
        captured = capsys.readouterr()
        assert "Incompatible --compare baseline" in captured.err
        assert "now exact" not in captured.out
        assert "0 improved, 0 worse" in captured.out

    def test_compare_rejects_baseline_with_different_stripped_event_identity(self):
        results = {
            "player.killed": audit.FieldResult(
                matched=2,
                total=2,
                known_bug={
                    "1": [
                        "meepo-aegis-reincarnation:npc_dota_hero_dragon_knight->npc_dota_hero_meepo@1733"
                    ]
                },
            )
        }
        baseline = {
            "player.killed": {
                "matched": 2,
                "total": 2,
                "known_bug": {
                    "1": [
                        "meepo-aegis-reincarnation:npc_dota_hero_dragon_knight->npc_dota_hero_meepo@1437"
                    ]
                },
            }
        }

        assert audit.incompatible_baseline_fields(results, baseline) == ["player.killed"]
        assert audit.regressed(results, baseline) is True
