import pytest

from my_wallet.blueprints.wallet.changers import create_wallet


def test__wallets_list(client, wallet):
    assert wallet.title in client.get("/wallet/").data.decode()


@pytest.mark.parametrize(
    "wallet_obj, expected",
    [
        (pytest.lazy_fixture("wallet"), "Wallet deleted"),
        (
            pytest.lazy_fixture("unauthorized_user_wallet"),
            "Cant delete the wallet since you&#39;re not owner of the wallet",
        ),
    ],
)
def test__wallet_delete(client, wallet_obj, expected):
    response = client.post(f"/wallet/{wallet_obj.id}/delete", follow_redirects=True)
    assert expected in response.data.decode()
    create_wallet(wallet_obj)


def test__transaction_add__true(client, wallet):
    response = client.post(f"/wallet/{wallet.id}/transaction/add", follow_redirects=True)
    assert "Transaction created" in response.data.decode()


def test__transaction_add__false(client, wallet):
    response = client.get(f"/wallet/{wallet.id}/transaction/add", follow_redirects=True)
    assert "My Wallet – New transaction" in response.data.decode()
