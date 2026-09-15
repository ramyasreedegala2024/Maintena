from flask import Blueprint, request
from flask_jwt_extended import jwt_required
import joblib
import pandas as pd
from pathlib import Path

from db import get_db


prediction_routes = Blueprint("prediction", __name__)


# Load the trained ML model
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml"
    / "maintenance_model.pkl"
)

model = joblib.load(MODEL_PATH)


@prediction_routes.route("/predict", methods=["POST"])
@jwt_required()
def predict():

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

    # Validate sensor values
    try:
        machine_id = int(machine_id)
        temperature = float(temperature)
        vibration = float(vibration)
        pressure = float(pressure)
    except (ValueError, TypeError):
        return {
            "message": "Sensor values must be valid numbers"
        }, 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

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

        # Save sensor reading
        cursor.execute(
            """
            INSERT INTO sensor_data
            (machine_id, temperature, vibration, pressure)
            VALUES (%s, %s, %s, %s)
            """,
            (machine_id, temperature, vibration, pressure)
        )

        # Prepare data for ML model
        input_data = pd.DataFrame(
            [[temperature, vibration, pressure]],
            columns=[
                "temperature",
                "vibration",
                "pressure"
            ]
        )

        # Predict failure probability
        probability = model.predict_proba(input_data)[0][1]

        failure_probability = round(
            probability * 100,
            2
        )

        # Calculate risk level
        if failure_probability >= 70:
            risk_level = "High"
        elif failure_probability >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Save prediction
        cursor.execute(
            """
            INSERT INTO predictions
            (machine_id, failure_probability, risk_level)
            VALUES (%s, %s, %s)
            """,
            (
                machine_id,
                failure_probability,
                risk_level
            )
        )

        prediction_id = cursor.lastrowid

        ticket_id = None
        technician = None

        # Automatically create ticket for High risk
        if risk_level == "High":

            # Check for an existing Open ticket
            cursor.execute(
                """
                SELECT id, technician
                FROM tickets
                WHERE machine_id = %s
                AND status = 'Open'
                ORDER BY id DESC
                LIMIT 1
                """,
                (machine_id,)
            )

            existing_ticket = cursor.fetchone()

            if existing_ticket:

                # Reuse existing Open ticket
                ticket_id = existing_ticket["id"]
                technician = existing_ticket["technician"]

            else:

                # Find a technician
                cursor.execute(
                    """
                    SELECT name
                    FROM users
                    WHERE role = 'technician'
                    ORDER BY id
                    LIMIT 1
                    """
                )

                technician_user = cursor.fetchone()

                if technician_user:
                    technician = technician_user["name"]

                # Create maintenance ticket
                cursor.execute(
                    """
                    INSERT INTO tickets
                    (machine_id, title, description, priority, technician)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        machine_id,
                        "High Failure Risk Detected",
                        "Machine sensor data indicates a high probability of failure.",
                        "High",
                        technician
                    )
                )

                ticket_id = cursor.lastrowid

        # Save all changes together
        db.commit()

        return {
            "prediction_id": prediction_id,
            "failure_probability": failure_probability,
            "risk_level": risk_level,
            "ticket_id": ticket_id,
            "technician": technician
        }, 201

    finally:
        cursor.close()
        db.close()