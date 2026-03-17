from flask.testing import FlaskClient
from http import HTTPStatus

def test_health_status(client:FlaskClient):

    url = "health/ready"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

def test_health(client:FlaskClient):
    url = "health/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
