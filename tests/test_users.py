from flask.testing import FlaskClient
from http import HTTPStatus


def test_create_user(client: FlaskClient):

    url = "/users/create"
    data = {
        "first_name": "test",
        "last_name": "user",
        "email": "test_user19@taskapi.com",
        "password": "Ch@ng3Me!"
    }
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.CREATED

def test_delete_user(client: FlaskClient, auth_headers:dict):
    
    # Create a user to delete
    url = "/users/create"
    data = {
        "first_name": "test",
        "last_name": "user",
        "email": "test_user@taskapi.com",
        "password": "T3$tusr123"
    }
    response = client.post(url, json=data)
    testUser = response.get_json().get("email")


    # Now delete user
    deleteUrl = f"/users/delete_user/{testUser}"
    delResponse = client.delete(deleteUrl, headers=auth_headers)
    assert delResponse.status_code == HTTPStatus.OK


