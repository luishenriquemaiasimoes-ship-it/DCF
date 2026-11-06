from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]


@pytest.fixture
def backend_dir() -> Path:
    return BACKEND
