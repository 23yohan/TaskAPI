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

def test_delete_user(client: FlaskClient, test_user: str):
    
    # Now delete user
    deleteUrl = f"/users/delete_user/{test_user}"
    delResponse = client.delete(deleteUrl)
    assert delResponse.status_code == HTTPStatus.OK


