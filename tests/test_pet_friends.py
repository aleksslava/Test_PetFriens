from api import Petfriends
from settings import email, password


pf = Petfriends()

def test_get_api_key_correct(email=email, password=password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_filed(email='asdff@mail.ru', password='asdffa'):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' not in result

def test_get_list_of_pets(filter=''):
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_correct(name='storm', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg'):
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_del_pet_correct():
    _, auth_key = pf.get_api_key(email=email, password=password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='')
    if len(list_of_pets['pets']) == 0:
        pf.add_new_pet(auth_key, name='vasya', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg')
        _, list_of_pets = pf.get_list_of_pets(auth_key, filter='')
    pet_id = list_of_pets['pets'][0]['id']
    status = pf.del_pet(auth_key, pet_id)
    assert status == 200
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='')
    assert list_of_pets['pets'][0]['id'] != pet_id



def test_update_pet_info_correct(name='lion', animal_type='bear', age='3'):
    _, auth_key = pf.get_api_key(email, password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='')
    if len(list_of_pets['pets']) > 0:
        pet_id = list_of_pets['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
    else:
        raise Exception('There is no my pets')

def test_create_pet_simple(name='laizi', animal_type='dog', age='5'):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_update_pet_photo_correct(pet_photo='images/britanskaya.jpg'):
    _, auth_key = pf.get_api_key(email, password)
    _, my_pet_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = my_pet_list['pets'][-1]['id']
    status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 200

