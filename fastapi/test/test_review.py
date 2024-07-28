from models import Review


def create_review(login_header, client):
    client.post(
        "/api/review/create",
        json={"subject": "title", "book": "book", "content": "content"},
        headers=login_header,
    )


def test_review_create(login_header, client, session):
    response = client.post(
        "/api/review/create",
        json={
            "book": "test-book",
            "subject": "test-title",
            "content": "test-content",
        },
        headers=login_header,
    )

    review = session.get(Review, 1)

    assert response.status_code == 204
    assert review.book == "test-book"
    assert review.subject == "test-title"
    assert review.content == "test-content"


def test_review_list(login_header, client):
    create_review(login_header, client)
    create_review(login_header, client)

    response = client.get("/api/review/list")
    data = response.json()

    assert response.status_code == 200
    assert data.get("total") == 2
    assert len(data.get("review_list")) == 2
    assert data.get("review_list")[0].get("book") == "book"


def test_review_detail(login_header, client):
    create_review(login_header, client)

    response = client.get("/api/review/detail/1")
    review = response.json()

    assert response.status_code == 200
    assert review.get("book") == "book"
    assert review.get("subject") == "title"
    assert review.get("content") == "content"


def test_review_update(login_header, client, session):
    client.post(
        "/api/review/create",
        json={
            "book": "test-book",
            "subject": "test-title",
            "content": "test-content",
        },
        headers=login_header,
    )

    response = client.put(
        "/api/review/update/1",
        json={
            "review_id": "1",
            "book": "test-book-1",
            "subject": "test-title-1",
            "content": "test-content-1",
        },
        headers=login_header,
    )

    review = session.get(Review, 1)

    assert response.status_code == 204
    assert review.book == "test-book-1"
    assert review.subject == "test-title-1"
    assert review.content == "test-content-1"


def test_review_delete(login_header, client):
    client.post(
        "/api/review/create",
        json={
            "book": "test-book",
            "subject": "test-title",
            "content": "test-content",
        },
        headers=login_header,
    )

    response = client.delete_with_payload(
        url="/api/review/delete",
        headers=login_header,
        json={"review_id": 1},
    )

    assert response.status_code == 204

    response = client.get("/api/review/detail/1")

    assert response.status_code == 404


def test_review_delete_cascade(review_comment_like_follow, login_header_first, client):
    response = client.delete_with_payload(
        url="/api/review/delete", headers=login_header_first, json={"review_id": 1}
    )

    assert response.status_code == 204

    response = client.get("/api/review/detail/1")

    assert response.status_code == 404


def test_review_like(login_header, client, session):
    create_review(login_header, client)

    response = client.post(
        "/api/review/like", headers=login_header, json={"review_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Review, 1).like_accounts) == 1

    response = client.post(
        "/api/review/like", headers=login_header, json={"review_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Review, 1).like_accounts) == 0


def test_review_dislike(login_header, client, session):
    create_review(login_header, client)

    response = client.post(
        "/api/review/dislike", headers=login_header, json={"review_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Review, 1).dislike_accounts) == 1

    response = client.post(
        "/api/review/dislike", headers=login_header, json={"review_id": 1}
    )

    assert response.status_code == 204
    assert len(session.get(Review, 1).dislike_accounts) == 0
