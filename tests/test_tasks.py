from flask.testing import FlaskClient
from http import HTTPStatus


def test_create_task(client:FlaskClient, test_user: str):
    """
    @Brief: Function tests the create task endpoint
    @Param: client - FlaskClient object
    @Assert: 201 - CREATED
    """

    url = "/tasks/create"
    title = "test Create"
    description = "testing create task"
    data = {"title" : title, "description": description, "user" : test_user}

    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.CREATED

def test_get_task_list(client:FlaskClient):
    """
    @Brief: Function tests the health endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """
    
    url = "/tasks/"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

def test_modify_test_record(client:FlaskClient, test_user: str):
    """
    @Brief: Function tests the task completed endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """

    # Create a record to change
    createUrl = "/tasks/create"
    title = "test Create"
    description = "testing create task"
    data = {"title" : title, "description": description, "user" : test_user}
    clientResponse = client.post(createUrl, json=data)
    taskID = clientResponse.get_json().get("id")

    # Modify the test record - completion status
    url = f"/tasks/{taskID}"
    response = client.patch(url)
    assert response.status_code == HTTPStatus.OK

def test_delete_record(client:FlaskClient, test_user: str):
    """
    @Brief: Function tests the task delete endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """

    #Create something to delete
    createUrl = "/tasks/create"
    title = "test Create"
    description = "testing create task"
    data = {"title" : title, "description": description, "user" : test_user}
    clientResponse = client.post(createUrl, json=data)
    taskID = clientResponse.get_json().get("id")

    deleteUrl = f"/tasks/{taskID}"
    response = client.delete(deleteUrl)
    assert response.status_code == HTTPStatus.OK
