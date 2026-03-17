from flask import Blueprint
from flask import jsonify
from app import db
from sqlalchemy import text
from http import HTTPStatus

health_bp = Blueprint("health", __name__)

@health_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status" : "ok"})

@health_bp.route("/ready", methods=["GET"])
def get_db_health_status():
    # we want to check the db health status
    try:
        db.session.execute(text("SELECT 1"))
        res = {
            "status" : "ready",
            "database" : "connected"
        }
        return jsonify(res), HTTPStatus.OK
    except Exception as e:
        # TODO: We should have a backend logger to log this error. Maybe just a python logging file
        res = {
            "status" : "not ready",
            "database" : "disconnected"
        }
        return jsonify(res), HTTPStatus.SERVICE_UNAVAILABLE