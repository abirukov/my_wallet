import pytest
from typing import Any, Mapping

from my_wallet.utils.config import get_connection_dsn


@pytest.fixture
def config():
    return {
        "POSTGRES_DBNAME": "dev",
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "devpass",
    }


def test_get_connection_dsn(config: Mapping[str, Any]) -> None:
    assert get_connection_dsn(config) == "postgresql://postgres:devpass@localhost:5432/dev"
