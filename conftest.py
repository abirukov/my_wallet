import datetime

import pytest

from my_wallet.app import compose_app


@pytest.fixture
def config():
    return {
        "POSTGRES_DBNAME": "dev",
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "devpass",
    }


@pytest.fixture
def date_from():
    return datetime.datetime(2023, 2, 12, 23, 00)


@pytest.fixture
def date_to():
    return datetime.datetime(2023, 2, 12, 20, 00)


@pytest.fixture
def app():
    app = compose_app()
    app.config.update({
        "TESTING": True,
        "SERVER_NAME": 'localhost',
    })
    with app.app_context():
        with app.test_request_context():
            yield
