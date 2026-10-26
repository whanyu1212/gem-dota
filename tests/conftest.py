import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from gem.extractors import ObjectivesExtractor, PlayerExtractor, WardsExtractor
    from gem.parser import ReplayParser
    from gem.results.models import NeutralItemFoundEvent, ParsedMatch

FIXTURES_DIR = Path(__file__).parent / "fixtures"
OPENDOTA_FIXTURES_DIR = FIXTURES_DIR / "opendota"
TI2026_SHORT_MATCH_ID = 8868259993
TI2026_MEDIUM_MATCH_ID = 8860187335
TI2026_LONG_MATCH_ID = 8856501050
PERFORMANCE_BASELINE_MATCH_ID = 8822520406
FEATURE_PARITY_MATCH_ID = 8855188139
FIXED8_ENCODER_MATCH_ID = 9039619076
AEGIS_REINCARNATION_MATCH_ID = 9040268873
DEPRECATED_OPENDOTA_REPLAY_IDS = frozenset({8822593932})
DEPRECATED_OPENDOTA_REPLAY_NAMES = frozenset(
    f"{match_id}.dem" for match_id in DEPRECATED_OPENDOTA_REPLAY_IDS
)
PREFERRED_OPENDOTA_REPLAY_IDS = (
    TI2026_SHORT_MATCH_ID,
    TI2026_MEDIUM_MATCH_ID,
    TI2026_LONG_MATCH_ID,
    PERFORMANCE_BASELINE_MATCH_ID,
)
# Session fixtures that parse a whole replay. Tests using one share an xdist
# worker (see pytest_collection_modifyitems), so each replay is parsed once.
SHARED_PARSE_FIXTURES = (
    "canonical_parsed_match",
    "canonical_replay_pass",
    "feature_parity_match",
    "fixed8_encoder_match",
)


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks expensive tests requiring full replay files")
    config.addinivalue_line("markers", "integration: marks integration tests against full replays")
    config.addinivalue_line("markers", "network: marks tests that contact live external services")
    config.addinivalue_line(
        "markers", "corpus: marks slow OpenDota parity checks the parity audit repeats"
    )


def _shared_parse(item: pytest.Item) -> str | None:
    names = set(getattr(item, "fixturenames", ()))
    callspec = getattr(item, "callspec", None)
    if callspec is not None:
        # A test parametrized over fixture names loads them with getfixturevalue.
        names |= {value for value in callspec.params.values() if isinstance(value, str)}
    return next((name for name in SHARED_PARSE_FIXTURES if name in names), None)


# tryfirst: xdist's own hook reads the groups into each test's node id.
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Group tests for ``pytest -n N --dist loadgroup``.

    A test that uses a shared parsed replay joins that replay's group; any other
    test joins its module's group, so a module- or class-scoped parse runs once.
    """
    for item in items:
        group = _shared_parse(item) or item.module.__name__
        item.add_marker(pytest.mark.xdist_group(group))


def available_opendota_replay_paths() -> list[Path]:
    """Return non-deprecated local replay fixtures in stable preferred order."""
    preferred = [
        OPENDOTA_FIXTURES_DIR / f"{match_id}.dem"
        for match_id in PREFERRED_OPENDOTA_REPLAY_IDS
        if (OPENDOTA_FIXTURES_DIR / f"{match_id}.dem").exists()
    ]
    known = {path.name for path in preferred}
    extra = sorted(
        path
        for path in OPENDOTA_FIXTURES_DIR.glob("*.dem")
        if path.name not in known and path.name not in DEPRECATED_OPENDOTA_REPLAY_NAMES
    )
    return preferred + extra


def _required_replay_path(match_id: int, role: str) -> Path:
    path = OPENDOTA_FIXTURES_DIR / f"{match_id}.dem"
    if not path.exists():
        pytest.skip(
            f"{role} replay fixture {match_id}.dem is not available; sync it with: "
            f"uv run python scripts/sync_opendota_fixtures.py --match {match_id}"
        )
    return path


@pytest.fixture(scope="session")
def ti2026_short_replay_path() -> Path:
    """Return the canonical short TI2026 integration replay."""
    return _required_replay_path(TI2026_SHORT_MATCH_ID, "TI2026 short canonical")


@pytest.fixture(scope="session")
def ti2026_medium_replay_path() -> Path:
    """Return the extended medium-length TI2026 replay."""
    return _required_replay_path(TI2026_MEDIUM_MATCH_ID, "TI2026 medium extended")


@pytest.fixture(scope="session")
def ti2026_long_replay_path() -> Path:
    """Return the long TI2026 stress replay."""
    return _required_replay_path(TI2026_LONG_MATCH_ID, "TI2026 long stress")


@pytest.fixture(scope="session")
def performance_baseline_replay_path() -> Path:
    """Return the DreamLeague fixture used by performance baseline issue #143."""
    return _required_replay_path(PERFORMANCE_BASELINE_MATCH_ID, "performance baseline")


@pytest.fixture(scope="session")
def fixed8_encoder_replay_path() -> Path:
    """Return the BLAST SLAM VIII replay whose send tables use the fixed8 encoder."""
    return _required_replay_path(FIXED8_ENCODER_MATCH_ID, "fixed8 encoder regression")


@pytest.fixture(scope="session")
def aegis_reincarnation_replay_path() -> Path:
    """Return the BLAST SLAM VIII replay where Kez reincarnates on two Aegises."""
    return _required_replay_path(AEGIS_REINCARNATION_MATCH_ID, "Aegis reincarnation regression")


@pytest.fixture(scope="session")
def full_replay_path(ti2026_short_replay_path: Path) -> Path:
    """Compatibility alias for the canonical TI2026 integration replay."""
    return ti2026_short_replay_path


@pytest.fixture(scope="session")
def canonical_parsed_match(full_replay_path: Path) -> "ParsedMatch":
    """Parse the canonical replay once; consumers must treat the result as read-only."""
    import gem

    return gem.parse(str(full_replay_path))


@dataclass
class ReplayPass:
    """A finished parser run with the extractors tests read directly."""

    parser: "ReplayParser"
    players: "PlayerExtractor"
    objectives: "ObjectivesExtractor"
    wards: "WardsExtractor"
    neutral_item_finds: "list[NeutralItemFoundEvent]"


@pytest.fixture(scope="session")
def canonical_replay_pass(full_replay_path: Path) -> ReplayPass:
    """Run the parser over the canonical replay once, for tests below ``gem.parse``.

    Consumers must treat the parser, its final entity and string-table state, and
    the extractors as read-only.
    """
    from gem.extractors import ObjectivesExtractor, PlayerExtractor, WardsExtractor
    from gem.parser import ReplayParser

    parser = ReplayParser(str(full_replay_path))
    run = ReplayPass(
        parser, PlayerExtractor(sample_interval=300), ObjectivesExtractor(), WardsExtractor(), []
    )
    run.players.attach(parser)
    run.objectives.attach(parser)
    run.wards.attach(parser)
    parser.on_neutral_item_found(run.neutral_item_finds.append)
    parser.parse()
    return run


@pytest.fixture(scope="session")
def feature_parity_match() -> "ParsedMatch":
    """Share read-only feature parity output independently of the reference JSON."""
    import gem

    path = _required_replay_path(FEATURE_PARITY_MATCH_ID, "feature parity")
    return gem.parse(str(path))


@pytest.fixture(scope="session")
def fixed8_encoder_match(fixed8_encoder_replay_path: Path) -> "ParsedMatch":
    """Share read-only output of the BLAST SLAM VIII build-6956 fixture (9039619076)."""
    import gem

    return gem.parse(str(fixed8_encoder_replay_path))


@pytest.fixture(scope="session")
def fixed8_encoder_reference() -> dict:
    """Load the 9039619076 OpenDota reference (a parse with OpenDota's current rules)."""
    path = OPENDOTA_FIXTURES_DIR / f"{FIXED8_ENCODER_MATCH_ID}.opendota.json"
    if not path.exists():
        pytest.skip(f"OpenDota reference {path.name} not available")
    with path.open() as stream:
        return json.load(stream)


@pytest.fixture(scope="session")
def feature_parity_reference() -> dict:
    """Load the read-only OpenDota reference once, only for tests that need it."""
    path = OPENDOTA_FIXTURES_DIR / f"{FEATURE_PARITY_MATCH_ID}.opendota.json"
    if not path.exists():
        pytest.skip(f"OpenDota reference {path.name} not available")
    with path.open() as stream:
        return json.load(stream)
