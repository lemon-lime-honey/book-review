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


def test_get_account(client, session, create_account):
    response = client.get("/api/account/get/test")
    account = response.json()

    assert response.status_code == 200
    assert account.get("username") == "test"
    assert account.get("email") == "test@example.com"


def test_login(client, create_account):
    response = client.post(
        "/api/account/login", data={"username": "test", "password": "test"}
    )

    assert response.status_code == 200
    assert response.json().get("username") == "test"


def test_follow(login_header_second, create_two_accounts, session, client):
    response = client.post(
        "/api/account/follow", json={"account_id": 2}, headers=login_header_second
    )

    current_account = session.get(Account, 1)
    target_account = session.get(Account, 2)

    assert response.status_code == 204
    assert current_account.following[0].id == 2
    assert target_account.followers[0].id == 1

    response = client.post(
        "/api/account/follow", json={"account_id": 2}, headers=login_header_second
    )

    current_account = session.get(Account, 1)
    target_account = session.get(Account, 2)

    assert response.status_code == 204
    assert len(current_account.following) == 0
    assert len(target_account.followers) == 0
