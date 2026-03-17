from flask.testing import FlaskClient
from http import HTTPStatus


def test_create_task(client:FlaskClient):
    url = "/api/tasks"
    title = "test Create"
    description = "testing create task"
    data = {"title" : title, "description": description}

    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.CREATED

def test_get_task_list(client:FlaskClient):
    url = "api/tasks"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

def test_modify_test_record(client:FlaskClient):
    
    # Create a record to change
    createUrl = "api/tasks"
    title = "test procedure"
    description = "test the modify function"
    data = {"title" : title, "description" : description}
    clientResponse = client.post(createUrl, json=data)
    taskID = clientResponse.get_json().get("id")

    # Modify the test record - completion status
    url = f"api/tasks/{taskID}"
    response = client.patch(url)
    assert response.status_code == HTTPStatus.OK

def test_delete_record(client:FlaskClient):

    #Create something to delete
    createUrl = "api/tasks"
    title = "test procedure"
    description = "test the delete function"
    data = {"title" : title, "description" : description}
    clientResponse = client.post(createUrl, json=data)
    taskID = clientResponse.get_json().get("id")

    deleteUrl = f"api/tasks/{taskID}"
    response = client.delete(deleteUrl)
    assert response.status_code == HTTPStatus.OK
    