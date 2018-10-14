import pytest
import requests
from requests_toolbelt.utils import dump
import allure
from faker import Faker

fake = Faker()

params = [
    ({"name": fake.name(), "job": ''}, 'Incorrect parameter Name or Job', 'put'),
    ({"name": '', "job": fake.job()}, 'Incorrect parameter Name or Job', 'put'),
    ({"name": 'Øèðîêàÿ', "job": fake.job()}, 'Incorrect parameter Name or Job', 'put'),
    ({"name": fake.text(max_nb_chars=20000), "job": 'Øèðîêàÿ'}, 'Incorrect parameter Name or Job', 'put'),
    ({"name": fake.name(), "job": fake.text(max_nb_chars=20000)}, 'Incorrect parameter Name or Job', 'put'),

    ({"name": fake.text(max_nb_chars=20000)}, 'Incorrect parameter Name or Job', 'patch'),
    ({"name": 'Øèðîêàÿ'}, 'Incorrect parameter Name or Job', 'patch'),
    ({"job": ''}, 'Incorrect parameter Name or Job', 'patch'),
    ({"job": '123'}, 'Incorrect parameter Name or Job', 'patch')
]


def setup_module():
    global param_json, user_id, url
    url = 'https://reqres.in/api/users'
    param_json = {
        "name": fake.name(),
        "job": fake.job()
    }
    r = requests.post(url, json=param_json)
    data_json = r.json()
    user_id = data_json['id']


def test_update_user():
    new_param_json = {
        "name": fake.name(),
        "job": fake.job()
    }
    r = requests.put("https://reqres.in/api/users/{}".format(user_id), data=new_param_json)
    json = r.json()
    assert r.status_code == 200
    assert json['name'] == new_param_json['name']
    assert json['job'] == new_param_json['job']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


def test_update_user_name():
    new_param_json = {
        "name": fake.name()
    }
    r = requests.patch("https://reqres.in/api/users/{}".format(user_id), data=new_param_json)
    json = r.json()
    assert r.status_code == 200
    assert json['name'] == new_param_json['name']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


def test_update_user_job():
    new_param_json = {
        "job": fake.job()
    }
    r = requests.patch("https://reqres.in/api/users/{}".format(user_id), data=new_param_json)
    json = r.json()
    assert r.status_code == 200
    assert json['job'] == new_param_json['job']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


@pytest.mark.xfail
@pytest.mark.parametrize("data, error, method", params)
def test_update_user_with_incorrect_data(data, error, method):
    if method == 'put':
        r = requests.put("https://reqres.in/api/users/{}".format(user_id), data=data)
    else:
        r = requests.patch("https://reqres.in/api/users/{}".format(user_id), data=data)
    json = r.json()
    assert r.status_code == 400
    assert error in json['error']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))
