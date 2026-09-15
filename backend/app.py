import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

from db import get_db
from routes.auth_routes import auth_routes
from routes.machine_routes import machine_routes
from routes.sensor_routes import sensor_routes
from routes.prediction_routes import prediction_routes
from routes.ticket_routes import ticket_routes
from routes.dashboard_routes import dashboard_routes

load_dotenv()

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

JWTManager(app)

app.register_blueprint(auth_routes)
app.register_blueprint(machine_routes)
app.register_blueprint(sensor_routes)
app.register_blueprint(prediction_routes)
app.register_blueprint(ticket_routes)
app.register_blueprint(dashboard_routes)
@app.route("/")
def home():
    return "Maintena API is running"


@app.route("/test-db")
def test_db():

    db = get_db()

    cursor = db.cursor()
    cursor.execute("SELECT 1")

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return {
        "database": "connected",
        "result": result[0]
    }


if __name__ == "__main__":
    app.run(debug=True)