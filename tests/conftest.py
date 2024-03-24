from pathlib import Path

import pytest


# Creating the common function for input
@pytest.fixture
def fixture_path():
    return Path(__file__).parent.joinpath("fixtures")
