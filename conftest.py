import pytest

from faker import Faker
fake = Faker()


@pytest.fixture(scope="function")
def param_json():
    return {
      "name": fake.name(),
      "job": fake.job()
    }


@pytest.fixture(scope="module")
def url():
    return 'https://reqres.in/api/users'

