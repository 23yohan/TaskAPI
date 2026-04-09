from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime as dt
from datetime import timezone as tz

from sqlalchemy import text, select, delete, or_
from http import HTTPStatus

from app import db
from app.models.task import Tasks
from app.models.users import Users

crud_bp = Blueprint("tasks", __name__)

@crud_bp.route("/create", methods=["POST"])
@jwt_required()
def create_task():
    """
    @Brief: Function creates a task
    @Params: Expects a body with
                    title (str): Required - Name of the task
                    Description (str): Optional - Task details
                    completed (bool): Optional - defaults to false
    @Returns: tuple - JSON message and return code

    """
    currUsrId = get_jwt_identity() # Returns the userID associated

    data = request.get_json()
    if data is None:
        return jsonify({"message": "Invalid JSON"}), HTTPStatus.BAD_REQUEST

    title = data.get('title')
    if not title: 
        return jsonify({"message" : "Title is required"}), HTTPStatus.BAD_REQUEST

    try:
        tsk = Tasks(
            title=title, 
            description=data.get('description'), 
            completed=data.get('completed', False), 
            created_at=dt.now(tz.utc), 
            created_by=currUsrId)

        db.session.add(tsk)
        db.session.commit()
        return jsonify(tsk.to_dict()), HTTPStatus.CREATED
    except Exception as e:
        # Log something 
        db.session.rollback()
        return jsonify({"message" : "Error logging to db"}), HTTPStatus.SERVICE_UNAVAILABLE


@crud_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    @Brief: Function gets all of the tasks in the database
    @Param: None
    @Return: A list of all tasks with a JSON body with 
                title - Title of the task
                description - description of the task
                completed - Whether the task has been completed
                created_at - date in UTC of creation
                updated_at - date in UTC of last updated
            or
                message - error message associated with request
    """
    currUsr = int(get_jwt_identity())
    try:

        # Check if the user is an admin user
        usr = db.session.get(Users, currUsr)

        if usr.admin:
            tsk = db.session.execute(select(Tasks)).scalars().all()
        else:
            tsk = db.session.execute(
                select(Tasks).where(
                    or_(
                        Tasks.created_by == currUsr,
                        Tasks.assigned_to == currUsr
                    )
                )
            ).scalars().all()
        # tsk is going to be a list of Tasks objects so we can decode
        tskList = []
        for t in tsk: 
            tskList.append(t.to_dict())

        return jsonify(tskList), HTTPStatus.OK
    except Exception as e:
        print(e)
        return jsonify({"message" : "Unable to get all tasks"}), HTTPStatus.INTERNAL_SERVER_ERROR


@crud_bp.route("/<int:task_id>", methods=["GET"])
def get_single_task(task_id):
    """
    @Brief: Function gets a task based on the ID
    @Param: task_id - The task id that is requested
    @Return: A JSON body with 
                title - Title of the task
                description - description of the task
                completed - Whether the task has been completed
                created_at - date in UTC of creation
                updated_at - date in UTC of last updated
    """
    try:
        tsk = db.session.get(Tasks, task_id)
        return jsonify(tsk.to_dict()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message" : "Unable to process request"}), HTTPStatus.INTERNAL_SERVER_ERROR

@crud_bp.route("/<int:task_id>", methods=["PATCH"])
@jwt_required()
def mark_task_complete(task_id):
    """
    @Brief: Function Marks a task complete
    @Param: task_id - The task id that is requested
    @Return: A JSON body with 
                title - Title of the task
                description - description of the task
                completed - Whether the task has been completed
                created_at - date in UTC of creation
                updated_at - date in UTC of last updated
            or
                message - error message associated with request
    """
    currUsr = int(get_jwt_identity())
    try:
        tsk = db.session.get(Tasks, task_id)
        if tsk is None:
            return jsonify({"message": "Task not found"}), HTTPStatus.NOT_FOUND
        if currUsr != tsk.created_by and currUsr != tsk.assigned_to:
            return jsonify({"message" : "user cannot modify task"}), HTTPStatus.FORBIDDEN
        tsk.completed = True
        db.session.commit()

        return jsonify(tsk.to_dict()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message" : "Unable to change complete status"}), HTTPStatus.INTERNAL_SERVER_ERROR


@crud_bp.route("/delete/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    @Brief: Function deletes a task based on the task ID.
    @Param: task_id: Int the task id to be deleted
    @Return: JSON string with success message
    """

    currUsr = int(get_jwt_identity())

    try:
        print(f"User is: {currUsr}")
        # Get the user
        usrAdmin = db.session.get(Users, currUsr).admin
        tsk = db.session.get(Tasks, task_id)
        
        if tsk is None:
            return jsonify({"message" : "No task id found"}), HTTPStatus.BAD_REQUEST
        
        if tsk.created_by != currUsr and not usrAdmin:
            return jsonify({"message" : "Unable to delete task"}), HTTPStatus.FORBIDDEN

        db.session.delete(tsk)
        db.session.commit()
        return jsonify({"message" : "deleted task"}), HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), HTTPStatus.INTERNAL_SERVER_ERROR

@crud_bp.route("/assign/<int:task_id>/<string:user_email>", methods=["PATCH"])
def assign_task(task_id: int, user_email: str):

    # First we need to get the userId we are trying to assign
    usr = db.session.execute(
        select(Users).filter_by(email=user_email)
        ).scalar_one_or_none()
    tsk = db.session.get(Tasks, task_id)

    if not usr:
        return jsonify({"message" : "unable to find user"}), HTTPStatus.NOT_FOUND
    
    if not tsk:
        return jsonify({"message" : "unable to find task"}), HTTPStatus.NOT_FOUND

    try:
        tsk.assigned_to = usr.userId
        db.session.commit()
        return jsonify(tsk.to_dict()), HTTPStatus.OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : "Unable to assign task"}), HTTPStatus.SERVICE_UNAVAILABLE
