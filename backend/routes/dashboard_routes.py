from flask import Blueprint
from flask_jwt_extended import jwt_required

from db import get_db


dashboard_routes = Blueprint("dashboard", __name__)


@dashboard_routes.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        # Total machines
        cursor.execute(
            "SELECT COUNT(*) AS total FROM machines"
        )
        total_machines = cursor.fetchone()["total"]

        # Current high-risk machines
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM predictions p
            INNER JOIN (
                SELECT machine_id, MAX(id) AS latest_id
                FROM predictions
                GROUP BY machine_id
            ) latest
            ON p.id = latest.latest_id
            WHERE p.risk_level = 'High'
        """)

        high_risk_machines = cursor.fetchone()["total"]

        # Total tickets
        cursor.execute(
            "SELECT COUNT(*) AS total FROM tickets"
        )
        total_tickets = cursor.fetchone()["total"]

        return {
            "total_machines": total_machines,
            "high_risk_machines": high_risk_machines,
            "total_tickets": total_tickets
        }

    finally:
        cursor.close()
        db.close()