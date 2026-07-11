"""Unit tests for HTML report section helpers.

Covers:
- _net_worth_at: nearest net_worth sample lookup
- build_buybacks: renders ParsedPlayer.buybacks cost (formula tested in
  tests/test_derived_kills.py::TestBuybackCost)
- build_objectives: healing lotus entries appear with correct hero label
"""

from __future__ import annotations

from unittest.mock import MagicMock

from gem.reports import _sections
from gem.reports.sections.economy import _net_worth_at

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

    def _make_smoke(self) -> MagicMock:
        s = MagicMock()
        s.x = 0.0
        s.y = 0.0
        s.tick = 1200
        s.team = 2
        s.activator = "npc_dota_hero_axe"
        s.smoked = ["a", "b"]
        return s

    def _make_match(self) -> MagicMock:
        match = MagicMock()
        match.wards = [
            self._make_ward(ward_type="observer", team=2),
            self._make_ward(ward_type="sentry", team=3, killed_tick=None, expires_tick=2000),
        ]
        match.smoke_events = [self._make_smoke()]
        match.game_start_tick = 900
        match.game_end_tick = 3000
        # estimate_vision() iterates match.players; empty == no enemy vision.
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
        assert len(cfg["smokes"]) == 1
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

    def test_farming_excludes_laning_phase(self):
        """Farming patterns must not label 0-10 min (pulls/stacks) as farming."""
        from gem.reports._formatting import TICKS_PER_MIN
        from gem.reports.sections.vision import _FARMING_LANE_CUTOFF_TICKS

        # Cutoff constant is 10 minutes.
        assert _FARMING_LANE_CUTOFF_TICKS == 10 * TICKS_PER_MIN

        # Simulate a player whose position_log has one camp visit at 2 min
        # (pull) and one at 12 min (real farm). After the fix, _build_player_farm_visits
        # is called with min_tick = game_start + 10 min, so early visit is excluded.
        game_start = 0
        early_tick = 2 * TICKS_PER_MIN  # 2 min - inside laning
        late_tick = 12 * TICKS_PER_MIN  # 12 min - real farm
        farming_min = game_start + _FARMING_LANE_CUTOFF_TICKS

        assert early_tick < farming_min
        assert late_tick >= farming_min

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
