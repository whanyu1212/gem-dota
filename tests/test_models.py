"""Tests for gem.results.models — ParsedPlayer and ParsedMatch dataclasses."""

from __future__ import annotations

from collections import defaultdict

from gem.results.models import ParsedMatch, ParsedPlayer


class TestParsedPlayerLanePos:
    def test_lane_pos_is_defaultdict(self):
        assert isinstance(ParsedPlayer(player_id=0).lane_pos, defaultdict)

    def test_missing_key_returns_zero(self):
        assert ParsedPlayer(player_id=0).lane_pos["100_200"] == 0

    def test_accumulates(self):
        pp = ParsedPlayer(player_id=0)
        pp.lane_pos["50_60"] += 1
        pp.lane_pos["50_60"] += 1
        assert pp.lane_pos["50_60"] == 2

    def test_independent_players(self):
        p1, p2 = ParsedPlayer(player_id=0), ParsedPlayer(player_id=1)
        p1.lane_pos["10_20"] += 5
        assert p2.lane_pos["10_20"] == 0


class TestParsedPlayerRepr:
    def test_slot_hero_team_kda(self):
        pp = ParsedPlayer(
            player_id=3,
            hero_name="npc_dota_hero_axe",
            team=2,
            kills=5,
            deaths=2,
            assists=8,
        )
        r = repr(pp)
        assert "slot=3" in r
        assert "axe" in r
        assert "Radiant" in r
        assert "5/2/8" in r

    def test_dire_team(self):
        assert "Dire" in repr(ParsedPlayer(player_id=7, team=3))

    def test_unknown_team(self):
        assert "team=0" in repr(ParsedPlayer(player_id=0, team=0))

    def test_no_hero_shows_unknown(self):
        assert "unknown" in repr(ParsedPlayer(player_id=0))


class TestParsedPlayerPermanentBuffFlags:
    def test_defaults_distinguish_unavailable_from_confirmed_zero(self):
        pp = ParsedPlayer(player_id=0)

        assert pp.aghanims_scepter is None
        assert pp.aghanims_shard is None
        assert pp.moonshard is None


class TestParsedMatchRepr:
    def test_radiant_win(self):
        r = repr(ParsedMatch(match_id=12345, radiant_win=True))
        assert "12345" in r
        assert "Radiant" in r

    def test_dire_win(self):
        assert "Dire" in repr(ParsedMatch(match_id=99, radiant_win=False))

    def test_unknown_winner(self):
        assert "?" in repr(ParsedMatch(match_id=0, radiant_win=None))

    def test_player_count(self):
        assert "players=10" in repr(ParsedMatch())


class TestParsedMatchFieldOrder:
    """``ParsedMatch`` is a public dataclass that supports positional
    construction, so additive fields must stay at the end of the declaration
    order — inserting one in the middle silently shifts every later positional
    argument by one slot.
    """

    # Released positional order. Append new constructor fields to this list;
    # never insert or reorder, which would silently shift positional callers.
    _POSITIONAL_ORDER = [
        "match_id",
        "game_mode",
        "leagueid",
        "radiant_win",
        "radiant_team_id",
        "radiant_team_name",
        "radiant_team_tag",
        "dire_team_id",
        "dire_team_name",
        "dire_team_tag",
        "game_start_tick",
        "game_end_tick",
        "duration",
        "radiant_score",
        "dire_score",
        "first_blood_time",
        "pre_game_duration",
        "players",
        "towers",
        "barracks",
        "roshans",
        "aegis_events",
        "tormentors",
        "shrines",
        "courier_deaths",
        "objectives",
        "tower_status_radiant",
        "tower_status_dire",
        "barracks_status_radiant",
        "barracks_status_dire",
        "wards",
        "radiant_gold_adv",
        "radiant_xp_adv",
        "combat_log",
        "chat",
        "courier_snapshots",
        "neutral_item_finds",
        "smoke_events",
        "draft",
        "teamfights",
        "opendota_teamfights",
        "vision_modifiers",
        "banner_plants",
        "game_times_min",
        "hero_visibility_events",
        "vision_modifier_pairing_issues",
        "entity_visibility_events",
        "post_game_tick",
        "game_clock",
    ]

    def test_positional_order_is_append_only(self):
        import dataclasses

        fields = [f.name for f in dataclasses.fields(ParsedMatch) if f.init]
        assert fields == self._POSITIONAL_ORDER, (
            "new constructor fields must be appended to preserve positional "
            f"construction; current order: {fields}"
        )

    def test_positional_duration_is_not_shifted(self):
        import dataclasses

        defaults = []
        for f in dataclasses.fields(ParsedMatch):
            if f.name == "duration":
                break
            defaults.append(
                f.default_factory() if f.default_factory is not dataclasses.MISSING else f.default
            )
        match = ParsedMatch(*defaults, 3005)
        assert match.duration == 3005
        assert match.post_game_tick is None

    def test_positional_construction_keeps_objectives_aligned(self):
        # Build positionally through the `objectives` slot and confirm the
        # sentinel lands in `.objectives`, not the trailing `.banner_plants`.
        import dataclasses

        sentinel = [{"sentinel": True}]
        args = []
        for f in dataclasses.fields(ParsedMatch):
            if f.name == "objectives":
                args.append(sentinel)
                break
            if f.default_factory is not dataclasses.MISSING:
                args.append(f.default_factory())
            elif f.default is not dataclasses.MISSING:
                args.append(f.default)
            else:
                args.append(None)
        match = ParsedMatch(*args)
        assert match.objectives == sentinel
        assert match.banner_plants == []


class TestPublicExports:
    """``ParsedMatch.banner_plants`` is a public parse-result field whose value
    type is documented as ``gem.BannerPlant``, so the package must re-export it
    (matching the ``gem.BuybackEvent`` precedent for a parse-result value type).
    """

    def test_banner_plant_is_publicly_exported(self):
        import gem
        from gem.results.models import BannerPlant

        assert "BannerPlant" in gem.__all__
        assert gem.BannerPlant is BannerPlant
