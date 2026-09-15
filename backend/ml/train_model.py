import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


# Sample sensor data
data = {
    "temperature": [60, 65, 70, 75, 80, 85, 90, 95, 100, 105],
    "vibration": [2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9],
    "pressure": [100, 98, 97, 96, 95, 94, 92, 90, 88, 85],
    "failure": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
}


# Create DataFrame
df = pd.DataFrame(data)


# Features and target
X = df[["temperature", "vibration", "pressure"]]
y = df["failure"]


# Create and train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# Save model inside the ml folder
model_path = os.path.join(
    os.path.dirname(__file__),
    "maintenance_model.pkl"
)

joblib.dump(model, model_path)


print("Model trained successfully")
print("Model saved at:", model_path)