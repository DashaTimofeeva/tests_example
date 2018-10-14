from urllib import response

import pytest
import requests
from allure_commons._allure import title, description
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


def test_create_user_with_correct_data(param_json, url):
    data = deepcopy(param_json)
    r = requests.post(url, json=data)
    json = r.json()
    assert 201 == r.status_code
    assert json.get('id') is not None
    assert json['name'] == data['name']
    assert json['job'] == data['job']
    assert json['createdAt']
    data = dump.dump_all(r)
    allure.attach(data.decode('utf-8'))


@title('Валидация.')
@description('Проверяем валидацию в форме создания пользователя')
@pytest.mark.xfail
@pytest.mark.parametrize('key, value, error', wrong_parameters)
def test_create_user_with_incorrect_data(key, value, error, param_json, url):
    with allure.step('копируем данные в json'):
        data = deepcopy(param_json)
        data[key] = value
    with allure.step('отправляем рост запрос на создание пользователя с некорректными данными'):
        r = requests.post(url, json=data)
        json = r.json()
    with allure.step('ассертим результат'):
        assert r.status_code == 400
        assert error in json['error']
        data = dump.dump_all(r)
        allure.attach(data.decode('utf-8'), response.text, type='html')


