from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tables import Base
from gateway import app, get_db


def test1():
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    def test_create_user():
        response = client.get("/health/")
        data = response.json()
        assert data["status"] == "green"

        response = client.post(
            "/users/",
            json={"username": "mock_username", "password": "1234"},
        )

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["username"] == "mock_username"
        assert "id" in data

        user_id = data["id"]
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["username"] == "mock_username"
        assert data["id"] == user_id

    test_create_user()
