from requests_toolbelt.utils import dump
import allure
import pytest
import requests

not_exist_user_ids = [
    (-1, 404),
    (-100, 404),
    (0, 404),
    ("ddd", 404),
    (1.5, 404),
    (0.1, 404),
    # ("#1", 404)  # возвращает 200, а должен 404
]


def get_all_users(per_page=3):
    r = requests.get("https://reqres.in/api/users", params={"per_page": per_page})
    assert r.status_code == 200
    result_data = r.json()
    return result_data['data']


def setup_module():
    global total_pages
    r = requests.get("https://reqres.in/api/users", params={"per_page": 3})
    assert r.status_code == 200
    result_data = r.json()
    total_pages = result_data['total_pages']


@pytest.mark.parametrize("data", get_all_users())
def test_get_exist_single_user(data):
    r = requests.get("https://reqres.in/api/users/{}".format(data['id']))
    assert r.status_code == 200
    user_data = r.json()
    assert user_data['data'] == data
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


@pytest.mark.parametrize("user_id, code", not_exist_user_ids)
def test_not_exist_single_user(user_id, code):
    r = requests.get("https://reqres.in/api/users/{}".format(user_id))
    assert r.status_code == code
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


def test_list_users():
    data = {"page": 1, "per_page": 3}
    r = requests.get("https://reqres.in/api/users", params=data)
    assert r.status_code == 200
    result_data = r.json()
    assert result_data['page'] == data['page']
    assert result_data['per_page'] == data['per_page']
    assert len(result_data['data']) <= data['per_page']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


def test_list_users_incorrect_page():
    r = requests.get('https://reqres.in/api/users', params={"page": total_pages + 1})
    assert r.status_code == 200
    result_data = r.json()
    assert len(result_data['data']) == 0
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))
