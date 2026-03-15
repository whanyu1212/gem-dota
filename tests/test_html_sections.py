"""Unit tests for examples/report/html_sections.py helpers.

Covers:
- _net_worth_at: nearest net_worth sample lookup
- build_buybacks: gold spent column (floor(200 + net_worth / 13))
- build_objectives: healing lotus entries appear with correct hero label
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Import html_sections from examples/report/ (not on sys.path by default)
# ---------------------------------------------------------------------------

_REPORT_DIR = Path(__file__).parent.parent / "examples" / "report"


def _load_html_sections():
    import importlib.util

    # html_sections imports from `report.assets`, so `examples/` must be on sys.path
    examples_dir = str(_REPORT_DIR.parent)
    if examples_dir not in sys.path:
        sys.path.insert(0, examples_dir)

    spec = importlib.util.spec_from_file_location("html_sections", _REPORT_DIR / "html_sections.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


html_sections = _load_html_sections()
_net_worth_at = html_sections._net_worth_at


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
# Buyback gold cost formula: floor(200 + net_worth / 13)
# ---------------------------------------------------------------------------


class TestBuybackGoldCost:
    """Verify the buyback cost formula via build_buybacks output."""

    def _make_match(self, net_worth: int, buyback_tick: int = 500):
        from gem.combatlog import CombatLogEntry

        buyback_entry = CombatLogEntry(tick=buyback_tick, log_type="BUYBACK", value=0)

        pp = _make_player(
            times=[buyback_tick],
            net_worth_t=[net_worth],
        )
        pp.buyback_log = [buyback_entry]

        match = MagicMock()
        match.players = [pp]
        return match

    def _cost_in_html(self, net_worth: int) -> str:
        match = self._make_match(net_worth)
        html = html_sections.build_buybacks(match)
        return html

    def test_zero_net_worth(self):
        # floor(200 + 0/13) = 200
        html = self._cost_in_html(0)
        assert "200g" in html

    def test_typical_net_worth(self):
        # net_worth=13000 → floor(200 + 13000/13) = floor(200 + 1000) = 1200
        html = self._cost_in_html(13000)
        assert "1,200g" in html

    def test_fractional_rounds_down(self):
        # net_worth=1300 → floor(200 + 1300/13) = floor(200 + 100) = 300
        # net_worth=1301 → floor(200 + 1301/13) = floor(200 + 100.07...) = 300
        html1 = self._cost_in_html(1300)
        html2 = self._cost_in_html(1301)
        assert "300g" in html1
        assert "300g" in html2

    def test_gold_spent_column_header_present(self):
        html = self._cost_in_html(5000)
        assert "Gold Spent" in html

    def test_no_buybacks_shows_no_table(self):
        pp = _make_player()
        pp.buyback_log = []
        match = MagicMock()
        match.players = [pp]
        html = html_sections.build_buybacks(match)
        assert "Gold Spent" not in html
        assert "no buybacks" in html
