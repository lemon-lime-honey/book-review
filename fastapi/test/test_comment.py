from fastapi.encoders import jsonable_encoder
from models import Account, Comment, Review


def create_review(login_header, client):
    client.post(
        "/api/review/create",
        json={"subject": "title", "book": "book", "content": "content"},
        headers=login_header,
    )


def create_comment(login_header, client, session):
    review = jsonable_encoder(session.get(Review, 1))
    author = jsonable_encoder(session.get(Account, 1))
    review["author"] = author

    client.post(
        "/api/comment/create/1",
        json={"content": "comment", "review": review},
        headers=login_header,
    )


def test_comment_create(login_header, client, session):
    create_review(login_header, client)

    review = jsonable_encoder(session.get(Review, 1))
    author = jsonable_encoder(session.get(Account, 1))
    review["author"] = author

    response = client.post(
        "/api/comment/create/1",
        json={"content": "comment", "review": review},
        headers=login_header,
    )

    comment = session.get(Comment, 1)

    assert response.status_code == 204
    assert comment.content == "comment"


def test_comment_update(login_header, client, session):
    create_review(login_header, client)
    create_comment(login_header, client, session)

    review = jsonable_encoder(session.get(Review, 1))
    author = jsonable_encoder(session.get(Account, 1))
    review["author"] = author

    response = client.put(
        "/api/comment/update",
        json={"comment_id": 1, "content": "comment-1", "review": review},
        headers=login_header,
    )

    assert response.status_code == 204

    comment = session.get(Comment, 1)

    assert comment.content == "comment-1"


def test_comment_get(login_header, client, session):
    create_review(login_header, client)
    create_comment(login_header, client, session)

    response = client.get("/api/comment/detail/1")

    assert response.status_code == 200

    comment = response.json()

    assert comment.get("content") == "comment"
    assert comment.get("review_id") == 1
    assert comment.get("author").get("id") == 1


def test_comment_list(login_header, client, session):
    create_review(login_header, client)
    create_comment(login_header, client, session)
    create_comment(login_header, client, session)

    response = client.get("/api/comment/list/1")
    data = response.json()

    assert response.status_code == 200
    assert data.get("total") == 2
    assert data.get("comment_list")[0].get("content") == "comment"


def test_comment_delete(login_header, client, session):
    create_review(login_header, client)
    create_comment(login_header, client, session)

    response = client.delete_with_payload(
        url="/api/comment/delete", json={"comment_id": 1}, headers=login_header
    )

    assert response.status_code == 204

    comment = session.get(Comment, 1)

    assert comment is None


def test_comment_like(login_header, client, session):
    create_review(login_header, client)
    create_comment(login_header, client, session)

    response = client.post(
        "api/comment/like", headers=login_header, json={"comment_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Comment, 1).like_accounts) == 1

    response = client.post(
        "api/comment/like", headers=login_header, json={"comment_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Comment, 1).like_accounts) == 0


def test_comment_dislike(login_header, client, session):
    create_review(login_header, client)
    create_comment(login_header, client, session)

    response = client.post(
        "api/comment/dislike", headers=login_header, json={"comment_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Comment, 1).dislike_accounts) == 1

    response = client.post(
        "api/comment/dislike", headers=login_header, json={"comment_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Comment, 1).dislike_accounts) == 0
