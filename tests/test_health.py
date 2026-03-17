from flask.testing import FlaskClient
from http import HTTPStatus

def test_health_status(client:FlaskClient):
    """
    @Brief: Function tests the health status endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """
    url = "/health/ready"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

def test_health(client:FlaskClient):
    """
    @Brief: Function tests the health endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """
    url = "/health/"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
