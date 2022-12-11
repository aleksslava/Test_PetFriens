import pytest
from settings import email, password, russian_chars, chinese_chars, generate_string
from api import Petfriends
pf = Petfriends()

@pytest.fixture(scope='session')
def get_api():
    status, result = pf.get_api_key(email, password)
    assert status == 200
    return result


@pytest.mark.parametrize('filter', [
    '',
    'my_pets'
], ids= [
    'all pets',
    'my_pets'
])
def test_get_list_of_pets_correct(get_api, filter):
    status, result = pf.get_list_of_pets(api_key=get_api, filter=filter)
    assert status == 200

@pytest.mark.parametrize('filter', [
    generate_string(255),
    generate_string(1001),
    russian_chars(),
    chinese_chars()
], ids= [
    '255 chars',
    '1001 chars',
    'russian chars',
    'chinese chars'
])
def test_get_list_of_pets_incorrect(get_api, filter):
    status, result = pf.get_list_of_pets(api_key=get_api, filter=filter)
    assert 400 <= status <= 500

