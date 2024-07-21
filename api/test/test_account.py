from models import Account


def test_create_account(client, session):
    response = client.post(
        "/api/account/create",
        json={
            "username": "test",
            "password1": "test",
            "password2": "test",
            "email": "test@example.com",
        },
    )

    account = session.get(Account, 1)

    assert response.status_code == 204
    assert account.username == "test"
    assert account.email == "test@example.com"
    assert account.password != "test"


def test_login(client, create_account):
    response = client.post(
        "/api/account/login", data={"username": "test", "password": "test"}
    )

    assert response.status_code == 200
    assert response.json().get("username") == "test"
