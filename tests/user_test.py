import pytest
import requests

from testing_data import *


def test_change_user_password(get_token):
    change_password = requests.post(
        "http://0.0.0.0:8000/change_password",
        json=user_change_password,
        headers=get_token
    )

    assert change_password.status_code == 200

    login_old_password = requests.post(
        "http://0.0.0.0:8000/login",
        data=user_login
    )

    assert login_old_password.status_code == 401


    user_login["password"] = "2"
    login_new_password = requests.post(
        "http://0.0.0.0:8000/login",
        data=user_login
    )

    assert login_new_password.status_code == 200


@pytest.mark.parametrize(
    "id, expected_code",
    [
        (1, 200),
        (100, 404)
    ]
)
def test_get_user_by_id(id, expected_code):
    user_data = requests.get(
        f"http://0.0.0.0:8000/profile/{id}",
    )

    assert user_data.status_code == expected_code


def test_get_current_user(get_token):
    user_data = requests.get(
        f"http://0.0.0.0:8000/me",
        headers=get_token
    )

    assert user_data.status_code == 200


def test_edit_current_user(get_token):
    user_data = requests.patch(
        f"http://0.0.0.0:8000/me",
        json=user_edit,
        headers=get_token
    )

    assert user_data.status_code == 200



