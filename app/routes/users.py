from flask import Blueprint, request, jsonify
from datetime import datetime as dt
from datetime import timezone as tz
import re

from sqlalchemy import text, select, delete
from http import HTTPStatus
import bcrypt

from app import db
from app.models.users import Users
from app.models.task import Tasks

users_bp = Blueprint("users", __name__)

@users_bp.route("/add_user", methods=["POST"])
def create_user():

    # We want to get the response
    res = request.get_json()

    firstName = res.get('first_name')
    lastName = res.get('last_name')
    email = res.get ('email')
    password = res.get('password')

    if not firstName:
        return jsonify({"message" : "First name not provided"}), HTTPStatus.BAD_REQUEST
    if not lastName:
        return jsonify({"message" : "Last name not provided"}), HTTPStatus.BAD_REQUEST
    if not email:
        return jsonify({"message" : "Email not provided"}), HTTPStatus.BAD_REQUEST
    if not password:
        return jsonify({"message" : "Password is not provided"}), HTTPStatus.BAD_REQUEST

    if not '@' in email:
        return jsonify({"message" : "Invalid email address"}), HTTPStatus.BAD_REQUEST
    
    if not check_password(password):
        return jsonify({"message" : "Password does not match requirements"}), HTTPStatus.BAD_REQUEST

    if not firstName.isalpha():
        return jsonify({"message" : "first name is invalid"}), HTTPStatus.BAD_REQUEST
    
    if not lastName.isalpha():
        return jsonify({"message" : "Last name is invalid"}), HTTPStatus.BAD_REQUEST
    
    # If we get here we can store values
    # store the password encrypted
    hashPwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    usr = Users(firstName =firstName, lastName=lastName, email=email, password=hashPwd)

    try:
        db.session.add(usr)
        db.session.commit()
        return jsonify(usr.to_dict()), HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : "Error creating user"}), HTTPStatus.SERVICE_UNAVAILABLE

@users_bp.route("/delete_user/<string:email>", methods=["DELETE"])
def delete_user(email):

    usr = db.session.execute(
        select(Users).filter_by(email=email)
        ).scalar_one_or_none()
    if not usr:
        return jsonify({"message" : "unable to find user"}), HTTPStatus.NOT_FOUND
    try:
        usr.firstName = None
        usr.lastName = None
        usr.email = None
        usr.password = None
        usr.active = False
        usr.deleteDate = dt.now(tz.utc)
        db.session.commit()
        return jsonify({"message" : "user deleted"}), HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : "unable to delete user"}), HTTPStatus.SERVICE_UNAVAILABLE



def check_password(pwd):
    """
    @Brief: Function checks password for the requirements
                - 5 Characters long
                - Has a upper case and lower case letter in it
                - Has a special character in it

    @Param: pwd - String of the raw password
    @Return:
            True - The password meets the requirements
            False - The password does not meet the requirements
    """
    # Can use a regex string here
    regex = ("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[-+_!@#$%^&*., ?]).{5,}$")
    p = re.compile(regex)
    return True if re.search(p,pwd) else False