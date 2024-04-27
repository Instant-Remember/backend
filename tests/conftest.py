import pytest
import requests

from testing_data import *


@pytest.fixture(scope="session", autouse=True)
def get_token():
    register = requests.post(
        "http://0.0.0.0:8000/signup",
        json=user_registration
    )

    if register.status_code != 200:
        raise Exception("Register is unsuccessful")


    login = requests.post(
        "http://0.0.0.0:8000/login",
        data=user_login
    )

    if login.status_code != 200:
        raise Exception("Login is unsuccessful")

    token = login.json().get("access_token")

    yield {"Authorization": f"Bearer {token}"}

    requests.delete(
        f"http://0.0.0.0:8000/me",
        headers={"Authorization": f"Bearer {token}"}
    )

@pytest.fixture(scope="session", autouse=True)
def prepare_data():
    #register_users
    for user_n in range(1, 3):
        register_data = user_registration.copy()
        register_data.update({
            "username": f"TestUser{user_n}",
            "email": f"user{user_n}@test.com",
        })
        register = requests.post(
            "http://0.0.0.0:8000/signup",
            json=register_data
        )

        if register.status_code != 200:
            raise Exception("Register is unsuccessful")

        login_data = {
            "username": register_data["email"],
            "password": "1"
        }
        login = requests.post(
            "http://0.0.0.0:8000/login",
            data=login_data
        )

        if login.status_code != 200:
            raise Exception("Login is unsuccessful")

        user_token = login.json().get("access_token")
        headers = {"Authorization": f"Bearer {user_token}"}

        for goal_n in range(2):
            goal_data = goal_create.copy()
            goal_data.update({"name": f"Цель {user_n} {goal_n}"})
            goal = requests.post(
                "http://0.0.0.0:8000/goal",
                json=goal_data,
                headers=headers
            )

            if goal.status_code != 200:
                raise Exception("Goal can't create")
                #raise Exception(goal_data)

            for post_n in range(5):
                post_data = post_create.copy()
                post_data.update({
                    "text": f"Пост {goal_n} {post_n}",
                    "goal_id": goal.json().get("id")
                })
                post = requests.post(
                    "http://0.0.0.0:8000/post",
                    json=post_data,
                    headers=headers
                )
                if post.status_code != 200:
                    #raise Exception("Goal can't create")
                    raise Exception(post.text)

