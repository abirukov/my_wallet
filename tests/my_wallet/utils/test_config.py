from typing import Any, Mapping

from my_wallet.utils.config import get_connection_dsn


def test_get_connection_dsn(config: Mapping[str, Any]) -> None:
    assert get_connection_dsn(config) == "postgresql://postgres:devpass@localhost:5432/dev"
