from fastapi.testclient import TestClient
from app.db import get_session
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.db import get_session
from app.oauth2 import create_access_token
from app import models
import pytest

# SQLALCHEMY_DATABASE_URL = "postgresqlL//postgres:password@localhost:5432/social_media_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def client(session):
    def override_get_session():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)

@pytest.fixture()
def test_user2(client):
    user_data = {"email":"test_user2@gmail.com", "password":"password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def test_user(client):
    user_data = {"email":"test_user@gmail.com", "password":"password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture()
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "First title",
        "content": "First content",
        "owner_id": test_user["id"]
    },
    {
        "title": "Second title",
        "content": "Second content",
        "owner_id": test_user["id"]
    },
    {
        "title": "Third title",
        "content": "Third content",
        "owner_id": test_user["id"]
    },
    {
        "title": "Fourth title",
        "content": "Fourth content",
        "owner_id": test_user2["id"]
    }]
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts