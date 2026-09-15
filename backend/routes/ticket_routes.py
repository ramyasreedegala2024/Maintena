from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from db import get_db


ticket_routes = Blueprint("tickets", __name__)


@ticket_routes.route("/tickets", methods=["POST"])
@jwt_required()
def create_ticket():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    machine_id = data.get("machine_id")
    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority")
    technician = data.get("technician")

    if not machine_id or not title or not description or not priority:
        return {
            "message": "Machine ID, title, description, and priority are required"
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
            INSERT INTO tickets
            (machine_id, title, description, priority, technician)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (machine_id, title, description, priority, technician)
        )

        db.commit()

        ticket_id = cursor.lastrowid

        return {
            "message": "Maintenance ticket created successfully",
            "ticket_id": ticket_id
        }, 201

    finally:
        cursor.close()
        db.close()


@ticket_routes.route("/tickets", methods=["GET"])
@jwt_required()
def get_tickets():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
            SELECT
                tickets.id,
                tickets.machine_id,
                machines.name AS machine_name,
                tickets.title,
                tickets.description,
                tickets.priority,
                tickets.status,
                tickets.technician,
                tickets.created_at
            FROM tickets
            JOIN machines
            ON tickets.machine_id = machines.id
            ORDER BY tickets.id DESC
        """

        cursor.execute(query)

        tickets = cursor.fetchall()

        return tickets

    finally:
        cursor.close()
        db.close()