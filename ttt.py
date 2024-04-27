import requests

user_login = {
    "username": "user1@test.com",
    "password": "1"
}

response = requests.post(
    "http://0.0.0.0:8000/login",
    data=user_login
)

print(response.status_code)
