from datetime import date
from fastapi.encoders import jsonable_encoder
from domain.account.crud import verify_password
from models import Account, Comment, Review


def test_create_account(client, session):
    response = client.post(
        "/api/account/create",
        json={
            "username": "test",
            "password1": "test",
            "password2": "test",
            "email": "test@example.com",
            "birthday": jsonable_encoder(date.today()),
            "summary": "test",
        },
    )

    account = session.get(Account, 1)

    assert response.status_code == 204
    assert account.username == "test"
    assert account.email == "test@example.com"
    assert account.birthday == date.today()
    assert account.summary == "test"


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
    assert response.json().get("user_id") == 1


def test_update_account(client, session, create_account, login_header):
    response = client.put(
        "/api/account/update",
        json={
            "id": 1,
            "username": "test1",
            "email": "test1@example.com",
            "birthday": jsonable_encoder(date(2000, 1, 1)),
            "summary": "test1",
        },
        headers=login_header,
    )

    account = session.get(Account, 1)

    assert response.status_code == 204
    assert account.username == "test1"
    assert account.email == "test1@example.com"
    assert account.birthday == date(2000, 1, 1)
    assert account.summary == "test1"


def test_delete_acount(client, session, login_header):
    response = client.delete("/api/account/delete", headers=login_header)

    assert response.status_code == 204

    response = client.get("/api/account/test")

    assert response.status_code == 404


def test_delete_account_cascade(
    client, session, review_comment_like_follow, login_header_first
):
    response = client.delete("/api/account/delete", headers=login_header_first)
    account = session.get(Account, 1)
    review = session.get(Review, 1)
    comment = session.get(Comment, 1)

    assert response.status_code == 204
    assert account is None
    assert review is None
    assert comment is None


def test_match_account(client, session, create_account):
    response = client.post(
        "/api/account/match", json={"username": "test", "email": "test@example.com"}
    )
    print(dir(response))

    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.post(
        "api/account/match", json={"username": "test", "email": "test1@example.com"}
    )

    assert response.status_code == 404


def test_reset_password(login_header, client, session):
    response = client.post(
        "/api/account/reset",
        json={"account_id": 1, "password1": "newPw", "password2": "newPw"},
        headers=login_header,
    )

    account = session.get(Account, 1)

    assert response.status_code == 204
    assert verify_password("newPw", account.password)


def test_change_password(login_header, client, session):
    response = client.post(
        "api/account/change",
        json={"account_id": 1, "password": "test", "password1": "newPw", "password2": "newPw"},
        headers=login_header,
    )

    account = session.get(Account, 1)

    assert response.status_code == 204
    assert verify_password("newPw", account.password)


def test_follow(login_header_first, session, client):
    response = client.post(
        "/api/account/follow", json={"account_id": 2}, headers=login_header_first
    )

    current_account = session.get(Account, 1)
    target_account = session.get(Account, 2)

    assert response.status_code == 204
    assert current_account.following[0].id == 2
    assert target_account.followers[0].id == 1

    response = client.post(
        "/api/account/follow", json={"account_id": 2}, headers=login_header_first
    )

    current_account = session.get(Account, 1)
    target_account = session.get(Account, 2)

    assert response.status_code == 204
    assert len(current_account.following) == 0
    assert len(target_account.followers) == 0


def test_find_review_by_account(client, session, review_comment_like_follow):
    response = client.get("/api/account/reviews", params={"account_id": 1})

    assert response.status_code == 200
    assert response.json().get("total") == 1
    assert len(session.query(Review).all()) == 2


def test_find_comment_by_account(client, session, review_comment_like_follow):
    response = client.get("/api/account/comments", params={"account_id": 1})

    assert response.status_code == 200
    assert response.json().get("total") == 1
    assert len(session.query(Comment).all()) == 2
