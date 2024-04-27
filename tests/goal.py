import pytest
import requests

from testing_data import *


def test_edit_current_user():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    user_data = requests.patch(
        f"http://0.0.0.0:8000/me",
        json=user_edit,
        headers=headers
    )