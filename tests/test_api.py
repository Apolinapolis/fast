import pytest
import requests
from http import HTTPStatus
from models.User import User

@pytest.fixture()
def users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK

    return response.json()


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK

    users = response.json()
    for user in users:
        User.model_validate(user)


def test_users_doubles(users):
    users_ids = [user['id'] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("user_id", [1000, 13])
def test_user_not_exist_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [0, -1, "road"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY