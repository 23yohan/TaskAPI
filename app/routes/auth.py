from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from app import db
from app.models.users import Users
from http import HTTPStatus
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", None)
    pwd = data.get("password", None)

    if not email:
        return jsonify({"message" : "No email provided"}), HTTPStatus.BAD_REQUEST
    if not pwd:
        return jsonify({"message" : "No password provided"}), HTTPStatus.BAD_REQUEST

    try:
        # Now check if the email that is provided exists
        usr = db.session.execute(
            select(Users).filter_by(email=email)
        ).scalar_one_or_none()

    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : "Unable to access database"}), HTTPStatus.SERVICE_UNAVAILABLE
    
    if not usr:
        return jsonify({"message" : "Invalid Credentials"}), HTTPStatus.UNAUTHORIZED
    
    if not usr.active:
        return jsonify({"message" : "Account is inactive"}), HTTPStatus.UNAUTHORIZED
    
    # Now we check password
    if bcrypt.checkpw(pwd.encode("utf-8"), usr.password.encode("utf-8")):
        # Generate Auth keys
        token = create_access_token(identity=str(usr.userId))
        return jsonify({"access_token" : token}), HTTPStatus.OK
    else:
        return jsonify({"message" : "Invalid Credentials"}), HTTPStatus.UNAUTHORIZED

