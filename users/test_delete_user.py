import requests
from requests_toolbelt.utils import dump
import allure
from faker import Faker

fake = Faker()


def setup_module():
    global param_json, user_id
    param_json = {
        "name": fake.name(),
        "job": fake.job()
    }
    r = requests.post('https://reqres.in/api/users', json=param_json)
    data_json = r.json()
    user_id = data_json['id']


def test_delete_user():
    r = requests.delete("https://reqres.in/api/users/{}".format(user_id))
    assert r.status_code == 204
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


def test_search_delete_user():
    r = requests.get("https://reqres.in/api/users/{}".format(user_id))
    assert r.status_code == 404
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))
