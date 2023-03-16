import datetime

import pytest
from flask_login import login_user

from my_wallet.app import compose_app
from my_wallet.blueprints.user.models import User
from my_wallet.blueprints.wallet.changers import create_wallet
from my_wallet.blueprints.wallet.enums import WalletStatus
from my_wallet.blueprints.wallet.models import Wallet, Transaction


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
def user():
    return User(
        id=1,
        first_name="Test",
        last_name="Testov",
        email="test@example.com",
        mobile="79998887766",
    )


@pytest.fixture
def unauthorized_user():
    return User(
        id=2,
        first_name="Petr",
        last_name="Petrov",
        email="petr@example.com",
        mobile="79991112233",
    )


@pytest.fixture
def wallet(user):
    return Wallet(
        id=1,
        title="test_wallet",
        status=WalletStatus.ACTIVE,
        owned_by_user_id=user.id,
    )


@pytest.fixture
def unauthorized_user_wallet(unauthorized_user):
    return Wallet(
        id=2,
        title="test_unauthorized_user_wallet",
        status=WalletStatus.ACTIVE,
        owned_by_user_id=unauthorized_user.id,
    )


@pytest.fixture
def app(
    user,
    unauthorized_user,
    wallet,
    unauthorized_user_wallet,
):
    app = compose_app()
    app.config.update({
        "TESTING": True,
        "SERVER_NAME": 'localhost',
    })
    with (
        app.app_context(),
        app.test_request_context(),
        app.test_client(),
    ):
        app.session.add(user)
        app.session.add(unauthorized_user)
        app.session.commit()
        login_user(user)
        create_wallet(wallet)
        create_wallet(unauthorized_user_wallet)
        yield app
        app.session.query(Transaction).delete()
        app.session.query(Wallet).delete()
        app.session.query(User).delete()
        app.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()
