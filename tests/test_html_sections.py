"""Unit tests for HTML report section helpers.

Covers:
- _net_worth_at: nearest net_worth sample lookup
- build_buybacks: renders ParsedPlayer.buybacks cost (formula tested in
  tests/test_derived_kills.py::TestBuybackCost)
- build_objectives: healing lotus entries appear with correct hero label
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from gem.analysis.smoke import (
    SmokeAnalysis,
    SmokeGroupStatus,
    SmokeLifecycleStatus,
    SmokeMemberAnalysis,
)
from gem.reports import _sections
from gem.reports.sections.economy import _net_worth_at
from gem.results.models import SmokeEvent, SmokeParticipant, VisibilityState

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_player(
    player_id: int = 0,
    hero_name: str = "npc_dota_hero_axe",
    team: int = 2,
    times: list[int] | None = None,
    net_worth_t: list[int] | None = None,
) -> MagicMock:
    pp = MagicMock()
    pp.player_id = player_id
    pp.hero_name = hero_name
    pp.team = team
    pp.times = times or []
    pp.net_worth_t = net_worth_t or []
    pp.buyback_log = []
    pp.runes_log = []
    return pp


# ---------------------------------------------------------------------------
# _net_worth_at
# ---------------------------------------------------------------------------


class TestNetWorthAt:
    def test_empty_times_returns_zero(self):
        pp = _make_player(times=[], net_worth_t=[])
        assert _net_worth_at(pp, tick=500) == 0

    def test_exact_tick_match(self):
        pp = _make_player(times=[100, 200, 300], net_worth_t=[1000, 2000, 3000])
        assert _net_worth_at(pp, tick=200) == 2000

    def test_nearest_tick_before(self):
        pp = _make_player(times=[100, 300, 500], net_worth_t=[1000, 3000, 5000])
        # tick=150 is closer to 100 than 300
        assert _net_worth_at(pp, tick=150) == 1000

    def test_nearest_tick_after(self):
        pp = _make_player(times=[100, 300, 500], net_worth_t=[1000, 3000, 5000])
        # tick=250 is closer to 300 than 100
        assert _net_worth_at(pp, tick=250) == 3000

    def test_single_sample_always_returned(self):
        pp = _make_player(times=[9999], net_worth_t=[7777])
        assert _net_worth_at(pp, tick=0) == 7777

    def test_returns_last_sample_when_beyond_range(self):
        pp = _make_player(times=[100, 200], net_worth_t=[500, 1000])
        assert _net_worth_at(pp, tick=99999) == 1000


# ---------------------------------------------------------------------------
# build_buybacks renders the model's BuybackEvent cost (the formula itself is
# tested in tests/test_derived_kills.py::TestBuybackCost).
# ---------------------------------------------------------------------------


class TestBuybackReport:
    """Verify build_buybacks renders BuybackEvent cost and never hides a buyback."""

    def _make_match(self, cost: int, buyback_tick: int = 500):
        from gem.combat.log import CombatLogEntry
        from gem.results.models import BuybackEvent

        pp = _make_player()
        pp.buyback_log = [CombatLogEntry(tick=buyback_tick, log_type="BUYBACK", value=0)]
        pp.buybacks = [BuybackEvent(tick=buyback_tick, player_slot=0, cost=cost, net_worth=0)]

        match = MagicMock()
        match.players = [pp]
        return match

    def _cost_in_html(self, cost: int) -> str:
        return _sections.build_buybacks(self._make_match(cost))

    def test_renders_cost_value(self):
        assert "200g" in self._cost_in_html(200)

    def test_renders_thousands_separator(self):
        assert "1,200g" in self._cost_in_html(1200)

    def test_gold_spent_column_header_present(self):
        assert "Gold Spent" in self._cost_in_html(5000)

    def test_no_buybacks_shows_no_table(self):
        pp = _make_player()
        pp.buyback_log = []
        pp.buybacks = []
        match = MagicMock()
        match.players = [pp]
        html = _sections.build_buybacks(match)
        assert "Gold Spent" not in html

    def test_buyback_log_without_buybacks_is_still_shown(self):
        # Codex P2: a match with buyback_log populated but buybacks empty (manually
        # assembled / older serialized data) must still render the buyback, with the
        # cost derived from the formula fallback rather than being hidden.
        from gem.combat.log import CombatLogEntry

        pp = _make_player(times=[500], net_worth_t=[13000])
        pp.buyback_log = [CombatLogEntry(tick=500, log_type="BUYBACK", value=0)]
        pp.buybacks = []  # not populated
        match = MagicMock()
        match.players = [pp]
        html = _sections.build_buybacks(match)
        assert "Gold Spent" in html  # table rendered, not hidden
        assert "Total buybacks: 1" in html
        # formula fallback: 200 + 13000 // 13 = 1200
        assert "1,200g" in html


# ---------------------------------------------------------------------------
# build_wards: data crosses the Python -> JS boundary via an inert
# <script type="application/json"> tag (the build_farming pattern), so the
# executable <script> stays a plain string with no doubled-brace escaping.
# ---------------------------------------------------------------------------


class TestBuildWardsDataTag:
    """Lock in the JSON-data-tag contract introduced for issue #106 item #6."""

    def _make_ward(
        self,
        *,
        ward_type: str = "observer",
        team: int = 2,
        tick: int = 900,
        x: float = 1000.0,
        y: float = -2000.0,
        killed_tick: int | None = 1800,
        expires_tick: int | None = None,
    ) -> MagicMock:
        w = MagicMock()
        w.ward_type = ward_type
        w.team = team
        w.tick = tick
        w.x = x
        w.y = y
        w.killed_tick = killed_tick
        w.expires_tick = expires_tick
        w.placer = "npc_dota_hero_axe"
        w.killer = "npc_dota_hero_lina"
        return w

    def _make_match(self) -> MagicMock:
        match = MagicMock()
        match.wards = [
            self._make_ward(ward_type="observer", team=2),
            self._make_ward(ward_type="sentry", team=3, killed_tick=None, expires_tick=2000),
        ]
        match.smoke_events = []
        match.game_start_tick = 900
        match.game_end_tick = 3000
        match.players = []
        return match

    def _data_tag_payload(self, html: str) -> dict:
        import json
        import re

        m = re.search(
            r'<script type="application/json" id="ward-data">(.*?)</script>',
            html,
            re.S,
        )
        assert m is not None, "ward-data JSON tag missing"
        return json.loads(m.group(1))

    def test_data_tag_present_and_parses(self):
        html = _sections.build_wards(self._make_match(), None)
        cfg = self._data_tag_payload(html)
        assert len(cfg["wards"]) == 2
        assert "smokes" not in cfg
        assert cfg["gameStartTick"] == 900
        assert cfg["sliderMin"] is not None
        assert cfg["sliderMax"] is not None

    def test_exactly_one_json_data_tag(self):
        html = _sections.build_wards(self._make_match(), None)
        assert html.count('type="application/json"') == 1

    def test_no_doubled_braces_in_output(self):
        # The whole point of the refactor: no f-string brace escaping survives.
        html = _sections.build_wards(self._make_match(), None)
        assert "{{" not in html
        assert "}}" not in html

    def test_script_reads_the_data_tag(self):
        html = _sections.build_wards(self._make_match(), None)
        assert "JSON.parse(document.getElementById('ward-data')" in html

    def test_has_map_flag_reflects_map_b64(self):
        without = self._data_tag_payload(_sections.build_wards(self._make_match(), None))
        with_map = self._data_tag_payload(_sections.build_wards(self._make_match(), "ZmFrZWI2NA=="))
        assert without["hasMap"] is False
        assert with_map["hasMap"] is True

    def test_empty_wards_returns_placeholder_card(self):
        match = MagicMock()
        match.wards = []
        match.smoke_events = []
        match.game_start_tick = 0
        match.game_end_tick = 0
        match.players = []
        html = _sections.build_wards(match, None)
        assert "(no ward placement data)" in html
        assert 'type="application/json"' not in html


class TestBuildSmokes:
    """Smoke reporting keeps lifecycle, visibility, and spatial evidence separate."""

    @staticmethod
    def _smoke_config(html: str) -> dict:
        import json
        import re

        match = re.search(
            r'<script type="application/json" id="smoke-data">(.*?)</script>',
            html,
            re.S,
        )
        assert match is not None
        return json.loads(match.group(1))

    def test_renders_exact_early_removal_without_guessing_detection(self, monkeypatch):
        participant = SmokeParticipant(
            hero_name="npc_dota_hero_axe",
            player_id=0,
            applied_tick=1_002,
            removed_tick=1_452,
            modifier_duration_s=45.0,
            modifier_elapsed_duration_s=15.0,
            applied_x=100.0,
            applied_y=200.0,
            removed_x=300.0,
            removed_y=400.0,
        )
        smoke = SmokeEvent(
            tick=1_000,
            activator="npc_dota_hero_axe",
            team=2,
            smoked=[participant.hero_name],
            activation_x=50.0,
            activation_y=75.0,
            participants=[participant],
        )
        member = SmokeMemberAnalysis(
            hero_name=participant.hero_name,
            player_id=0,
            applied_tick=1_002,
            removed_tick=1_452,
            lifecycle_status=SmokeLifecycleStatus.EARLY,
            visibility_at_apply=VisibilityState.HIDDEN,
            visibility_at_remove=VisibilityState.HIDDEN,
            nearest_enemy_hero="npc_dota_hero_lina",
            nearest_enemy_player_id=5,
            nearest_enemy_distance=1_046.4,
            same_tick_actions=[MagicMock()],
        )
        analysis = SmokeAnalysis(
            activation_tick=1_000,
            activator=smoke.activator,
            team=2,
            status=SmokeGroupStatus.EARLY_REMOVAL,
            activation_x=50.0,
            activation_y=75.0,
            member_centroid_x=100.0,
            member_centroid_y=200.0,
            members=[member],
        )
        match = MagicMock()
        match.smoke_events = [smoke]
        player = _make_player(player_id=0, team=2)
        player.position_log = [(1_000, 50.0, 75.0), (1_452, 300.0, 400.0)]
        match.players = [player]

        from gem.reports.sections import vision as vision_section

        monkeypatch.setattr(vision_section, "build_smoke_analysis", lambda _: [analysis])
        html = _sections.build_smokes(match, None)

        assert "Smoke Operations" in html
        assert "Early removal" in html
        assert "+15.07s" in html
        assert "Hidden from enemy" in html
        assert "1,046u sampled" in html
        assert "action at same tick" in html
        assert "Enemy had vision" not in html
        assert "Undetected" not in html

    def test_empty_unlocated_smoke_renders_without_wards_or_map(self, monkeypatch):
        smoke = SmokeEvent(tick=2_000, activator="npc_dota_hero_riki", team=0)
        analysis = SmokeAnalysis(
            activation_tick=2_000,
            activator=smoke.activator,
            team=0,
            status=SmokeGroupStatus.NO_MEMBERS_OBSERVED,
            activation_x=None,
            activation_y=None,
            member_centroid_x=None,
            member_centroid_y=None,
        )
        match = MagicMock(smoke_events=[smoke], players=[], wards=[])

        from gem.reports.sections import vision as vision_section

        monkeypatch.setattr(vision_section, "build_smoke_analysis", lambda _: [analysis])
        html = _sections.build_smokes(match, None)

        assert "Smoke Operations" in html
        assert "No members observed" in html
        assert "No smoke members observed" in html
        assert "smokeCanvas" not in html

    def test_route_centroid_uses_only_each_members_observed_lifecycle(self):
        from gem.reports._formatting import MAP_XMAX, MAP_XMIN
        from gem.reports.sections.vision import _smoke_route

        first = SmokeParticipant(
            hero_name="first",
            player_id=0,
            applied_tick=100,
            removed_tick=130,
        )
        late = SmokeParticipant(
            hero_name="late",
            player_id=1,
            applied_tick=130,
            removed_tick=160,
        )
        smoke = SmokeEvent(
            tick=100,
            activator="first",
            team=2,
            participants=[first, late],
        )
        first_player = _make_player(player_id=0, hero_name="first")
        first_player.position_log = [(100, 0.0, 0.0), (130, 30.0, 0.0), (160, 60.0, 0.0)]
        late_player = _make_player(player_id=1, hero_name="late")
        late_player.position_log = [(100, 100.0, 0.0), (130, 130.0, 0.0), (160, 160.0, 0.0)]
        match = MagicMock(players=[first_player, late_player])

        route = _smoke_route(match, smoke)
        world_x = [point["fx"] * (MAP_XMAX - MAP_XMIN) + MAP_XMIN for point in route]

        assert [point["tick"] for point in route] == [100, 130, 160]
        assert world_x == pytest.approx([0.0, 80.0, 160.0], abs=0.1)

    def test_missing_activation_position_is_not_replaced_by_member_centroid(self, monkeypatch):
        participant = SmokeParticipant(
            hero_name="npc_dota_hero_axe",
            player_id=0,
            applied_tick=101,
            removed_tick=130,
            modifier_duration_s=45.0,
        )
        smoke = SmokeEvent(
            tick=100,
            activator=participant.hero_name,
            team=2,
            x=500.0,
            y=600.0,
            participants=[participant],
        )
        member = SmokeMemberAnalysis(
            hero_name=participant.hero_name,
            player_id=0,
            applied_tick=101,
            removed_tick=130,
            lifecycle_status=SmokeLifecycleStatus.EARLY,
            visibility_at_apply=VisibilityState.HIDDEN,
            visibility_at_remove=VisibilityState.HIDDEN,
        )
        analysis = SmokeAnalysis(
            activation_tick=100,
            activator=participant.hero_name,
            team=2,
            status=SmokeGroupStatus.EARLY_REMOVAL,
            activation_x=None,
            activation_y=None,
            member_centroid_x=500.0,
            member_centroid_y=600.0,
            members=[member],
        )
        player = _make_player(player_id=0, hero_name=participant.hero_name)
        player.position_log = [(101, 500.0, 600.0), (130, 700.0, 800.0)]
        match = MagicMock(smoke_events=[smoke], players=[player])

        from gem.reports.sections import vision as vision_section

        monkeypatch.setattr(vision_section, "build_smoke_analysis", lambda _: [analysis])
        config = self._smoke_config(_sections.build_smokes(match, None))

        assert config["events"][0]["start"] is None
        assert config["events"][0]["route"]

    def test_same_tick_same_activator_events_keep_their_own_raw_lifecycles(self, monkeypatch):
        raw_events = []
        analyses = []
        for duration in (10.0, 20.0):
            participant = SmokeParticipant(
                hero_name="npc_dota_hero_axe",
                player_id=0,
                applied_tick=101,
                removed_tick=130,
                modifier_duration_s=duration,
            )
            raw_events.append(
                SmokeEvent(
                    tick=100,
                    activator=participant.hero_name,
                    team=2,
                    participants=[participant],
                )
            )
            analyses.append(
                SmokeAnalysis(
                    activation_tick=100,
                    activator=participant.hero_name,
                    team=2,
                    status=SmokeGroupStatus.EARLY_REMOVAL,
                    activation_x=None,
                    activation_y=None,
                    member_centroid_x=None,
                    member_centroid_y=None,
                    members=[
                        SmokeMemberAnalysis(
                            hero_name=participant.hero_name,
                            player_id=0,
                            applied_tick=101,
                            removed_tick=130,
                            lifecycle_status=SmokeLifecycleStatus.EARLY,
                            visibility_at_apply=VisibilityState.UNKNOWN,
                            visibility_at_remove=VisibilityState.UNKNOWN,
                        )
                    ],
                )
            )
        match = MagicMock(smoke_events=raw_events, players=[])

        from gem.reports.sections import vision as vision_section

        monkeypatch.setattr(vision_section, "build_smoke_analysis", lambda _: analyses)
        html = _sections.build_smokes(match, None)

        assert html.count("10.00s") == 1
        assert html.count("20.00s") == 1
        assert html.index("10.00s") < html.index("20.00s")
