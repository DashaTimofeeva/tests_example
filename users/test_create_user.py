import pytest
import requests
from requests_toolbelt.utils import dump
import allure
from copy import deepcopy
from faker import Faker

fake = Faker()

wrong_parameters = [
    ('name', '', 'Missing name or job'),
    ('name', 'Øèðîêàÿ', 'Incorrect name or job'),
    ('name', fake.text(max_nb_chars=20000), 'Incorrect name or job'),
    ('name', '123', 'Incorrect name or job'),

    ('job', '', 'Missing name or job'),
    ('job', 'Øèðîêàÿ', 'Incorrect name or job'),
    ('job', fake.text(max_nb_chars=20000), 'Incorrect name or job'),
    ('job', '123', 'Incorrect name or job')
]


def setup_module():
    global param_json, url
    url = 'https://reqres.in/api/users'
    param_json = {
        "name": fake.name(),
        "job": fake.job()
    }


def test_create_user_with_correct_data():
    data = deepcopy(param_json)
    r = requests.post(url, json=data)
    json = r.json()
    assert r.status_code == 201
    assert json['id']
    assert json['name'] == data['name']
    assert json['job'] == data['job']
    assert json['createdAt']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


@pytest.mark.future_task
@pytest.mark.parametrize('key, value, error', wrong_parameters)
def test_create_user_with_incorrect_data(key, value, error):
    data = deepcopy(param_json)
    data[key] = value
    r = requests.post(url, json=data)
    json = r.json()
    assert r.status_code == 400
    assert error in json['error']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))
