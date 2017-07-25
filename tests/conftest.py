import pytest
import os

@pytest.fixture(scope="session")
def set_librato_credentials():
    os.environ["METRICS_LIBRATO_USER"]="test@example.com"
    os.environ["METRICS_LIBRATO_TOKEN"]="123"
