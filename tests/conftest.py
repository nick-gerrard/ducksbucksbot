import pytest


@pytest.fixture(autouse=True)
def _data_dir(tmp_path, monkeypatch):
    """Every test gets its own empty storage dir."""
    monkeypatch.delenv("STATE_DIRECTORY", raising=False)
    monkeypatch.setenv("DUCKSY_DATA_DIR", str(tmp_path / "data"))
