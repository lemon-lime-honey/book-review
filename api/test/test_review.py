from models import Review


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
