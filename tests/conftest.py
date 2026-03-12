import pytest
from pathlib import Path


@pytest.fixture
def tmp_config_dir(tmp_path):
    """Provides a temporary config directory instead of ~/.mautic-cli/."""
    return tmp_path / ".mautic-cli"
