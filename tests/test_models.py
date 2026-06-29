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

    def test_append_only_fields_are_last(self):
        import dataclasses

        fields = [f.name for f in dataclasses.fields(ParsedMatch)]
        assert fields[-3:] == ["banner_plants", "parse_error", "truncated_at_tick"], (
            "new ParsedMatch fields must be appended to preserve positional "
            f"construction; current order tail: {fields[-3:]}"
        )

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
    """Parse-result value types should be available from public packages."""

    def test_parse_result_value_types_are_publicly_exported(self):
        import gem
        import gem.results as results
        from gem.combat.log import CombatLogEntry, CombatLogType
        from gem.extractors.courier import CourierSnapshot
        from gem.extractors.draft import DraftEvent
        from gem.extractors.objectives import (
            AegisEvent,
            BannerPlant,
            BarracksKill,
            CourierDeath,
            RoshanKill,
            ShrineKill,
            TormentorKill,
            TowerKill,
        )
        from gem.extractors.teamfights import (
            OpenDotaTeamfight,
            OpenDotaTeamfightPlayer,
            Teamfight,
            TeamfightPlayer,
        )
        from gem.extractors.wards import WardEvent
        from gem.results.models import (
            BuybackEvent,
            ChatEntry,
            NeutralItemFoundEvent,
            ParsedMatch,
            ParsedPlayer,
            SmokeEvent,
            VisionModifierEvent,
        )

        expected = {
            "CombatLogEntry": CombatLogEntry,
            "CombatLogType": CombatLogType,
            "TowerKill": TowerKill,
            "BarracksKill": BarracksKill,
            "RoshanKill": RoshanKill,
            "AegisEvent": AegisEvent,
            "TormentorKill": TormentorKill,
            "ShrineKill": ShrineKill,
            "CourierDeath": CourierDeath,
            "BannerPlant": BannerPlant,
            "WardEvent": WardEvent,
            "CourierSnapshot": CourierSnapshot,
            "DraftEvent": DraftEvent,
            "Teamfight": Teamfight,
            "TeamfightPlayer": TeamfightPlayer,
            "OpenDotaTeamfight": OpenDotaTeamfight,
            "OpenDotaTeamfightPlayer": OpenDotaTeamfightPlayer,
            "ChatEntry": ChatEntry,
            "NeutralItemFoundEvent": NeutralItemFoundEvent,
            "BuybackEvent": BuybackEvent,
            "ParsedMatch": ParsedMatch,
            "ParsedPlayer": ParsedPlayer,
            "SmokeEvent": SmokeEvent,
            "VisionModifierEvent": VisionModifierEvent,
        }

        for name, obj in expected.items():
            assert name in gem.__all__
            assert getattr(gem, name) is obj
            assert name in results.__all__
            assert getattr(results, name) is obj
