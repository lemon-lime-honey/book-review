import json, pytest
from datetime import date, datetime, timedelta, UTC
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app
from models import Review

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TEST_KEY = "quigonobiwananakinahsoka"
TEST_ACCOUNT = {
    "username": "test",
    "password": "test",
    "email": "test@test.example.com",
}
TEST_ACCESS_TOKEN = jwt.encode(
    {"sub": "test", "exp": datetime.now(UTC) + timedelta(minutes=60)}, TEST_KEY, "HS256"
)


class CustomTestClient(TestClient):
    def delete_with_payload(self, **kwargs):
        return self.request(method="DELETE", **kwargs)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield CustomTestClient(app)


@pytest.fixture
def create_account(client):
    client.post(
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


@pytest.fixture
def login_header(client, create_account):
    res = json.loads(
        client.post(
            "/api/account/login", data={"username": "test", "password": "test"}
        ).text
    )
    headers = {
        "Authorization": f"Bearer {res['access_token']}",
        "user_id": f"{res["user_id"]}",
    }
    return headers


@pytest.fixture
def create_two_accounts(client):
    client.post(
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

    client.post(
        "/api/account/create",
        json={
            "username": "test2",
            "password1": "test2",
            "password2": "test2",
            "email": "test2@example.com",
            "birthday": jsonable_encoder(date.today()),
            "summary": "test2",
        },
    )


@pytest.fixture
def login_header_first(client, create_two_accounts):
    res = client.post(
            "/api/account/login", data={"username": "test", "password": "test"}
        ).json()

    headers = {
        "Authorization": f"Bearer {res['access_token']}",
        "user_id": f"{res["user_id"]}",
    }

    return headers


@pytest.fixture
def login_header_second(client, create_two_accounts):
    res = client.post(
        "/api/account/login", data={"username": "test2", "password": "test2"}
    ).json()

    headers = {
        "Authorization": f"Bearer {res['access_token']}",
        "user_id": f"{res["user_id"]}"
    }

    return headers


@pytest.fixture
def review_comment_like_follow(client, session, create_two_accounts, login_header_first, login_header_second):
    client.post("/api/review/create", json={"subject": "title1", "book": "book1", "content": "content1"}, headers=login_header_first)
    client.post("/api/review/like", json={"review_id": 1}, headers=login_header_second)
    client.post("/api/comment/create/1", json={"content": "comment1", "review": jsonable_encoder(session.get(Review, 1))}, headers=login_header_first)
    client.post("/api/comment/like", json={"comment_id": 1}, headers=login_header_second)
    client.post("/api/")
    client.post("/api/account/follow", json={"account_id": 1}, headers=login_header_second)
