from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from db import get_db


machine_routes = Blueprint("machines", __name__)


@machine_routes.route("/machines", methods=["POST"])
@jwt_required()
def add_machine():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    name = data.get("name")
    location = data.get("location")

    if not name or not location:
        return {
            "message": "Machine name and location are required"
        }, 400

    db = get_db()
    cursor = db.cursor()

    try:
        query = """
            INSERT INTO machines (name, location)
            VALUES (%s, %s)
        """

        cursor.execute(query, (name, location))
        db.commit()

        machine_id = cursor.lastrowid

        return {
            "message": "Machine added successfully",
            "machine_id": machine_id
        }, 201

    finally:
        cursor.close()
        db.close()


@machine_routes.route("/machines", methods=["GET"])
@jwt_required()
def get_machines():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        query = "SELECT * FROM machines ORDER BY id DESC"

        cursor.execute(query)

        machines = cursor.fetchall()

        return machines

    finally:
        cursor.close()
        db.close()


@machine_routes.route("/machines/<int:machine_id>", methods=["GET"])
@jwt_required()
def get_machine(machine_id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        query = "SELECT * FROM machines WHERE id = %s"

        cursor.execute(query, (machine_id,))

        machine = cursor.fetchone()

    finally:
        cursor.close()
        db.close()

    if machine is None:
        return {
            "message": "Machine not found"
        }, 404

    return machine