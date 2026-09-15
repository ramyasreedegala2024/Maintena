from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

from db import get_db


auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {
            "message": "Name, email, and password are required"
        }, 400

    db = get_db()
    cursor = db.cursor()

    try:
        # Check whether email already exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return {
                "message": "Email already registered"
            }, 409

        hashed_password = generate_password_hash(password)

        query = """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (name, email, hashed_password)
        )

        db.commit()

        return {
            "message": "User registered successfully"
        }, 201

    finally:
        cursor.close()
        db.close()


@auth_routes.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "message": "Email and password are required"
        }, 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        query = "SELECT * FROM users WHERE email = %s"

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

    finally:
        cursor.close()
        db.close()

    if user is None:
        return {
            "message": "Invalid email or password"
        }, 401

    if not check_password_hash(
        user["password"],
        password
    ):
        return {
            "message": "Invalid email or password"
        }, 401

    token = create_access_token(
        identity=str(user["id"])
    )

    return {
        "message": "Login successful",
        "token": token
    }, 200