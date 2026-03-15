"""Tests for parquet export helpers in gem public API."""

from __future__ import annotations

from pathlib import Path

import pytest

import gem
from gem.models import ParsedMatch


def _has_parquet_engine() -> bool:
    try:
        import pyarrow  # noqa: F401

        return True
    except ImportError:
        try:
            import fastparquet  # noqa: F401

            return True
        except ImportError:
            return False


class TestParquetExport:
    def test_to_parquet_raises_helpful_error_when_engine_missing(self, monkeypatch, tmp_path):
        import pandas as pd

        def _raise_import_error(self, path, index=False):  # noqa: ANN001, ARG001
            raise ImportError("no parquet engine")

        monkeypatch.setattr(pd.DataFrame, "to_parquet", _raise_import_error)

        with pytest.raises(ImportError, match="Install 'pyarrow' or 'fastparquet'"):
            gem.to_parquet(ParsedMatch(), tmp_path)

    def test_parse_to_parquet_delegates_to_parse_and_to_parquet(self, monkeypatch, tmp_path):
        fake_match = ParsedMatch(match_id=123)

        monkeypatch.setattr(gem, "parse", lambda path: fake_match)

        def _fake_to_parquet(match, output_dir, *, index=False):
            assert match is fake_match
            assert Path(output_dir) == tmp_path
            assert index is True
            return [tmp_path / "players.parquet"]

        monkeypatch.setattr(gem, "to_parquet", _fake_to_parquet)

        written = gem.parse_to_parquet("dummy.dem", tmp_path, index=True)
        assert written == [tmp_path / "players.parquet"]

    @pytest.mark.skipif(not _has_parquet_engine(), reason="No parquet engine installed")
    def test_to_parquet_writes_files(self, tmp_path):
        written = gem.to_parquet(ParsedMatch(), tmp_path)

        assert written
        assert all(p.suffix == ".parquet" for p in written)
        assert all(p.exists() for p in written)
