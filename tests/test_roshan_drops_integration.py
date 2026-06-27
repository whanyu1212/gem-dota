"""Integration test: Roshan drops populate from the entity stream.

Roshan's non-Aegis drops (Cheese, Refresher Shard, Roshan's Banner) are not in
the combat log; they are recovered from the entity stream by snapshotting the
``CDOTA_Item_*`` entities alive at Roshan's death tick (see
``extractors/objectives.py``). The unit tests for ``ObjectivesExtractor`` use
synthetic combat-log entries and therefore never exercise that entity-driven
populate path, so this end-to-end check guards it against regression.

It also confirms the drops thread through to the post-parse Roshan conversion
analysis (``drops`` / ``had_high_value_drop`` on ``RoshConversion``).

Marked ``slow`` + ``integration`` — needs a real ``.dem``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import gem
from gem.analysis.roshan import _HIGH_VALUE_DROPS, build_rosh_conversions

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
_MATCH_ID = 8855188139


@pytest.mark.slow
@pytest.mark.integration
class TestRoshanDropsPopulate:
    @pytest.fixture(scope="class")
    def match(self):
        """Parse the fixture once for the whole class."""
        dem = FIXTURES_DIR / f"{_MATCH_ID}.dem"
        if not dem.exists():
            pytest.skip(f"OpenDota fixture {_MATCH_ID}.dem not available")
        return gem.parse(str(dem))

    def test_has_roshan_kills(self, match):
        assert match.roshans, "fixture expected to contain at least one Roshan kill"

    def test_every_kill_drops_aegis(self, match):
        # Aegis always drops on a Roshan kill; it is the load-bearing invariant
        # of the entity-snapshot approach.
        for r in match.roshans:
            assert "aegis" in r.drops, f"Roshan #{r.kill_number} drops missing aegis: {r.drops}"

    def test_non_aegis_drops_present_somewhere(self, match):
        # This fixture's entity stream is known to contain Cheese, Refresher
        # Shard, and Roshan's Banner item entities. If the populate path breaks
        # (e.g. wrong class names, or the DELETED removal bug returns), the only
        # drop that would survive is "aegis" — so a non-Aegis drop appearing is
        # the meaningful regression signal.
        all_drops = {drop for r in match.roshans for drop in r.drops}
        non_aegis = all_drops - {"aegis"}
        assert non_aegis, f"no non-Aegis Roshan drops captured; got only {all_drops}"

    def test_drops_have_no_unexpected_tokens(self, match):
        # Guards against a stale/typo class name leaking an unmapped token.
        known = {"aegis", "cheese", "refresher_shard", "banner"}
        for r in match.roshans:
            unknown = set(r.drops) - known
            assert not unknown, f"unexpected drop token(s) {unknown} in {r.drops}"

    def test_banner_plants_populate_with_position(self, match):
        # This fixture is known to contain planted Roshan's Banner units. The
        # planted-unit entity path (CDOTA_Unit_Roshans_Banner) is exercised only
        # end-to-end, so confirm at least one plant is captured and that it
        # carries a readable world position + team — the prerequisites for the
        # banner→rax conversion signal.
        assert match.banner_plants, "fixture expected to contain at least one banner plant"
        for plant in match.banner_plants:
            assert plant.team in (2, 3), f"banner plant has invalid team {plant.team}"
            assert plant.x is not None and plant.y is not None, (
                f"banner plant at tick {plant.tick} missing world position"
            )


@pytest.mark.slow
@pytest.mark.integration
class TestRoshConversionDrops:
    @pytest.fixture(scope="class")
    def conversions(self):
        dem = FIXTURES_DIR / f"{_MATCH_ID}.dem"
        if not dem.exists():
            pytest.skip(f"OpenDota fixture {_MATCH_ID}.dem not available")
        return build_rosh_conversions(gem.parse(str(dem)))

    def test_conversions_built(self, conversions):
        assert conversions

    def test_drops_threaded_into_conversion(self, conversions):
        # Each conversion mirrors its RoshanKill.drops and always includes aegis.
        for conv in conversions:
            assert "aegis" in conv.drops, f"conversion #{conv.rosh_number} drops: {conv.drops}"

    def test_high_value_flag_matches_drops(self, conversions):
        # had_high_value_drop is purely derived from drops; verify the contract.
        for conv in conversions:
            expected = any(drop in _HIGH_VALUE_DROPS for drop in conv.drops)
            assert conv.had_high_value_drop is expected, (
                f"conversion #{conv.rosh_number}: had_high_value_drop="
                f"{conv.had_high_value_drop} but drops={conv.drops}"
            )
