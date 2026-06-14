from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
OPENDOTA_FIXTURES_DIR = FIXTURES_DIR / "opendota"
PREFERRED_OPENDOTA_REPLAY_IDS = (
    8822520406,
    8822593932,
    8821954344,
)


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests that require real replay files")
    config.addinivalue_line("markers", "integration: marks integration tests against full replays")


def available_opendota_replay_paths() -> list[Path]:
    """Return local OpenDota replay fixtures in stable preferred order."""
    preferred = [
        OPENDOTA_FIXTURES_DIR / f"{match_id}.dem"
        for match_id in PREFERRED_OPENDOTA_REPLAY_IDS
        if (OPENDOTA_FIXTURES_DIR / f"{match_id}.dem").exists()
    ]
    known = {path.name for path in preferred}
    extra = sorted(path for path in OPENDOTA_FIXTURES_DIR.glob("*.dem") if path.name not in known)
    return preferred + extra


@pytest.fixture(scope="session")
def full_replay_path() -> Path:
    paths = available_opendota_replay_paths()
    if not paths:
        pytest.skip("OpenDota integration replay fixture not available")
    return paths[0]
