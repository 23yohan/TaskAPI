from app import create_app, db
from flask.testing import FlaskClient
from flask import Flask
import pytest
from http import HTTPStatus

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def test_user(client: FlaskClient):
    url = "/users/create"
    data = {
        "first_name" : "admin",
        "last_name" : "user",
        "email" : "admin@taskapi.com",
        "password" : "Ch@ng3Me!"
    }
    res = client.post(url,json=data)
    assert res.status_code == HTTPStatus.CREATED, "Failed to create pyFixure user"
    return {"email": data["email"], "password" : data["password"]}

@pytest.fixture
def auth_headers(client: FlaskClient, test_user: dict):
    token = client.post("/auth/login", json=test_user).get_json().get("access_token")
    return {"Authorization" : f"Bearer {token}"}

@pytest.fixture
def test_task(client: FlaskClient, auth_headers : dict):
    
    createUrl = "/tasks/create"
    title = "test Create"
    description = "testing create task"
    data = {"title" : title, "description": description}
    res = client.post(createUrl, json=data, headers=auth_headers)
    assert res.status_code == HTTPStatus.CREATED, "Failed to create pyFixure user"
    return res.get_json()
