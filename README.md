# Maintena — Predictive Maintenance Ticket Platform

Maintena is a full-stack predictive maintenance platform that monitors machine sensor data, predicts equipment failure risk using Machine Learning, and automatically creates maintenance tickets for high-risk machines.

## Features

- User authentication with JWT
- Machine management
- Sensor data collection
- Machine failure risk prediction
- Automatic maintenance ticket creation for high-risk machines
- Technician assignment
- Maintenance ticket tracking
- React dashboard
- MySQL database
- Flask REST APIs

## System Flow

React Frontend  
↓  
Flask REST API  
↓  
MySQL Database + Machine Learning Model  
↓  
Sensor Data Analysis  
↓  
Failure Risk Prediction  
↓  
High Risk  
↓  
Maintenance Ticket + Technician Assignments

## Technology Stack

### Backend

- Python
- Flask
- Flask REST APIs
- Flask-JWT-Extended
- MySQL
- Python-dotenv

### Machine Learning

- Scikit-learn
- Random Forest Classifier
- Pandas
- Joblib

### Frontend

- React
- Vite
- JavaScript
- CSS

## Machine Learning

For this project prototype, a Random Forest classifier is trained using sensor features:

- Temperature
- Vibration
- Pressure

The model predicts the probability of machine failure.

Risk levels are calculated as:

- Low: below 30%
- Medium: 30%–69.99%
- High: 70% and above

When a machine reaches High risk, Maintena automatically creates a maintenance ticket if there is no existing open ticket for that machine.

## Project Structure

```text
Maintena/
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── requirements.txt
│   ├── ml/
│   │   ├── maintenance_model.pkl
│   │   └── train_model.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── machine_routes.py
│   │   ├── prediction_routes.py
│   │   ├── sensor_routes.py
│   │   └── ticket_routes.py
│   └── test_*.py
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
└── README.md
```
