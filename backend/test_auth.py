import requests

url = "http://127.0.0.1:5000/login"

data = {
    "email": input("Enter email: "),
    "password": input("Enter password: ")
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())