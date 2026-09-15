from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from db import get_db


sensor_routes = Blueprint("sensor", __name__)


@sensor_routes.route("/sensor-data", methods=["POST"])
@jwt_required()
def add_sensor_data():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    machine_id = data.get("machine_id")
    temperature = data.get("temperature")
    vibration = data.get("vibration")
    pressure = data.get("pressure")

    if (
        machine_id is None
        or temperature is None
        or vibration is None
        or pressure is None
    ):
        return {
            "message": "Machine ID, temperature, vibration, and pressure are required"
        }, 400

    db = get_db()
    cursor = db.cursor()

    try:
        # Check whether the machine exists
        cursor.execute(
            "SELECT id FROM machines WHERE id = %s",
            (machine_id,)
        )

        machine = cursor.fetchone()

        if machine is None:
            return {
                "message": "Machine not found"
            }, 404

        query = """
            INSERT INTO sensor_data
            (machine_id, temperature, vibration, pressure)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (machine_id, temperature, vibration, pressure)
        )

        db.commit()

        sensor_id = cursor.lastrowid

        return {
            "message": "Sensor data added successfully",
            "sensor_id": sensor_id
        }, 201

    finally:
        cursor.close()
        db.close()


@sensor_routes.route("/sensor-data/<int:machine_id>", methods=["GET"])
@jwt_required()
def get_sensor_data(machine_id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM sensor_data
            WHERE machine_id = %s
            ORDER BY recorded_at DESC
        """

        cursor.execute(query, (machine_id,))

        sensor_data = cursor.fetchall()

        return sensor_data

    finally:
        cursor.close()
        db.close()