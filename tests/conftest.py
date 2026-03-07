from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests that require real replay files")
    config.addinivalue_line("markers", "integration: marks integration tests against full replays")
