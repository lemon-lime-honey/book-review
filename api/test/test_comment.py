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
        "/api/comment/create",
        params={"review_id": 1},
        json={"content": "comment", "review": review},
        headers=login_header,
    )


def test_comment_create(login_header, client, session):
    create_review(login_header, client)

    review = jsonable_encoder(session.get(Review, 1))
    author = jsonable_encoder(session.get(Account, 1))
    review["author"] = author

    response = client.post(
        "/api/comment/create",
        params={"review_id": 1},
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
        "/api/comment/update/1",
        json={"comment_id": 1, "content": "comment-1", "review": review},
        headers=login_header,
    )

    assert response.status_code == 204

    comment = session.get(Comment, 1)

    assert comment.content == "comment-1"


def test_comment_delete(login_header, client, session):
    create_review(login_header, client)
    create_comment(login_header, client, session)

    response = client.delete_with_payload(
        url="/api/comment/delete", json={"comment_id": 1}, headers=login_header
    )

    assert response.status_code == 204
    
    comment = session.get(Comment, 1)
    
    assert comment is None
