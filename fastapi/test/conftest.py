import json, pytest
from datetime import datetime, timedelta, UTC
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app

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
        "username": res["username"],
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
        },
    )

    client.post(
        "/api/account/create",
        json={
            "username": "test2",
            "password1": "test2",
            "password2": "test2",
            "email": "test2@example.com",
        },
    )


@pytest.fixture
def login_header_second(client, create_two_accounts):
    res = json.loads(
        client.post(
            "/api/account/login", data={"username": "test", "password": "test"}
        ).text
    )
    headers = {
        "Authorization": f"Bearer {res['access_token']}",
        "username": res["username"],
    }
    return headers
