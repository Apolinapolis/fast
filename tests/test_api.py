import json
import pytest
import random
import requests
from http import HTTPStatus
from app.models.User import User



@pytest.fixture(scope='module')
def fill_test_data(app_url):
    with open('users.json') as f:
        test_data_users = json.load(f)
    test_users_list = []
    for user in test_data_users:
        response = requests.post(f'{app_url}/api/users', json=user)
        test_users_list.append(response.json())
    user_ids = [user['id'] for user in test_users_list]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f'{app_url}/api/users/{user_id}')


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    return response.json()


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        User.model_validate(user)


def test_users_doubles(users):
    users_ids = [user['id'] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_user(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [999999, random.randint(100000, 999999)])
def test_user_not_exist_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [0, -1, "road"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY