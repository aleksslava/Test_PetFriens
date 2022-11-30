from api import Petfriends
from settings import email, password

pf = Petfriends()

def test_get_api_key(email=email, password=password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_list_of_pets(filter=''):
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0