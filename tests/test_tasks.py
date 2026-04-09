from flask.testing import FlaskClient
from http import HTTPStatus


def test_create_task(client:FlaskClient, auth_headers: dict):
    """
    @Brief: Function tests the create task endpoint
    @Param: client - FlaskClient object
    @Assert: 201 - CREATED
    """

    url = "/tasks/create"
    title = "test Create"
    description = "testing create task"
    data = {"title" : title, "description": description}

    response = client.post(url, json=data, headers=auth_headers)
    assert response.status_code == HTTPStatus.CREATED

def test_get_task_list(client:FlaskClient, auth_headers:dict):
    """
    @Brief: Function tests the health endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """
    
    url = "/tasks/"
    response = client.get(url, headers=auth_headers)
    assert response.status_code == HTTPStatus.OK

def test_modify_test_record(client:FlaskClient, test_task: dict, auth_headers:dict):
    """
    @Brief: Function tests the task completed endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """

    taskID = test_task.get("id")

    # Modify the test record - completion status
    url = f"/tasks/{taskID}"
    response = client.patch(url, headers=auth_headers)
    assert response.status_code == HTTPStatus.OK

def test_delete_record(client:FlaskClient, test_task: dict, auth_headers: dict):
    """
    @Brief: Function tests the task delete endpoint
    @Param: client - FlaskClient object
    @Assert: 200 - OK
    """
    print(test_task)
    taskID = test_task.get("id")

    deleteUrl = f"/tasks/delete/{taskID}"
    response = client.delete(deleteUrl, headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
