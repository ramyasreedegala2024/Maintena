import requests

BASE_URL = "http://127.0.0.1:5000"

email = input("Enter email: ")
password = input("Enter password: ")

login_response = requests.post(
    f"{BASE_URL}/login",
    json={
        "email": email,
        "password": password
    }
)

print("Login:", login_response.status_code)
print(login_response.json())

if not login_response.ok:
    print("Login failed. Stopping test.")
    exit()

token = login_response.json()["token"]

headers = {
    "Authorization": f"Bearer {token}"
}

data = {
    "machine_id": 6,
    "temperature": 105,
    "vibration": 9,
    "pressure": 85
}

response = requests.post(
    f"{BASE_URL}/predict",
    json=data,
    headers=headers
)

print("\nPrediction:")
print(response.status_code)
print(response.json())