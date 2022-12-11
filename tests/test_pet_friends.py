import pytest
import requests as re
from api import Petfriends
from settings import email, password
from datetime import datetime

base_url = 'https://petfriends.skillfactory.ru'
pf = Petfriends()


@pytest.fixture(scope='session')
def get_key():
    headers = {'email': email, 'password': password}
    res = re.get(base_url + '/api/key', headers=headers)
    assert res.status_code == 200
    result = res.json()
    return result

@pytest.fixture(autouse=True, scope='function')
def request_fixture(request):
    print(request.fixturename)
    print(request.scope)
    print(request.function.__name__)
    print(request.cls)
    print(request.module.__name__)
    print(request.fspath)


@pytest.fixture(autouse=True, scope='session')
def timedelta():
    time_old = datetime.now()
    yield
    time_last = datetime.now()
    print(f'\nНа выполнение теста потребовалось: {time_last-time_old}')


def test_add_new_pet_correct(get_key,name='storm', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца на сайт с корректными входными данными.
    На выходе должны получить статус код 200 и словарь с данными нового питомца."""
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

@pytest.mark.skip
def test_add_new_pet_incorrect_auth_key(name='Лола', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца с некорректным auth_key.
    На выходе ожидается ответ от сервера со статус кодом 403."""
    auth_key = {'key': 'asafd548dsf84ds21f6ds8'}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403


def test_add_new_pet_without_animal_type(get_key, name='izum', age='hg', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца без значения 'animal_type'.
    На выходе ожидается ответ от сервера со статус кодом 400."""
    status, result = pf.add_new_pet_without_animal_type(get_key, name, age, pet_photo)
    assert status == 400


def test_add_new_pet_without_age(get_key, name='cat', animal_type='cat', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца без значения 'age'.
    На выходе ожидается ответ от сервера со статус кодом 400."""
    status, result = pf.add_new_pet_without_age(auth_key=get_key, name=name, animal_type=animal_type, pet_photo=pet_photo)
    assert status == 400


def test_del_my_pet_correct(get_key):
    """Тест на удаление питомца из списка питомцев из списка пользователя на сайте по id питомца.
    В ответе от сервера ожидается статус код 200, удаленный питомец отсутствует в списке."""
    _, list_of_pets = pf.get_list_of_pets(get_key, filter='my_pets')
    if len(list_of_pets['pets']) == 0:
        pf.add_new_pet(get_key, name='vasya', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg')
        _, list_of_pets = pf.get_list_of_pets(get_key, filter='my_pets')
    pet_id = list_of_pets['pets'][0]['id']
    status = pf.del_pet(get_key, pet_id)
    assert status == 200
    _, list_of_pets = pf.get_list_of_pets(get_key, filter='my_pets')
    assert list_of_pets['pets'][0]['id'] != pet_id

def test_del_enemy_pet_correct(get_key):
    """Тест на удаление питомца из полного списка питомцев на сайте по id питомца.
    В ответе от сервера ожидается статус код 200, удаленный питомец отсутствует в списке.
    Данный тест показывает, что пользователь может удалить чужих питомцев. Такого быть не должно!"""
    _, list_of_pets = pf.get_list_of_pets(get_key, filter='')
    if len(list_of_pets['pets']) == 0:
        pf.add_new_pet(get_key, name='vasya', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg')
        _, list_of_pets = pf.get_list_of_pets(get_key, filter='')
    pet_id = list_of_pets['pets'][0]['id']
    status = pf.del_pet(get_key, pet_id)
    assert status == 200
    _, list_of_pets = pf.get_list_of_pets(get_key, filter='')
    assert list_of_pets['pets'][0]['id'] != pet_id


def test_update_pet_info_correct(get_key, name='lion', animal_type='bear', age='3'):
    """Тест на обновление информации о питомце с корректными данными.
    На выходе ожидается ответ от сервера со статус кодом 200 и словарь с новыми значениями питомца. """
    _, list_of_pets = pf.get_list_of_pets(get_key, filter='my_pets')
    if len(list_of_pets['pets']) > 0:
        pet_id = list_of_pets['pets'][0]['id']
        status, result = pf.update_pet_info(get_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
    else:
        raise Exception('There is no my pets')

def test_create_pet_simple(get_key, name='laizi', animal_type='dog', age='5'):
    """Тест на создание нового питомца, без фото питомца.
     На выходе ожидается статус код 200 и словарь с данными нового питомца. """
    status, result = pf.create_pet_simple(get_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_update_pet_photo_correct(get_key, pet_photo='images/britanskaya.jpg'):
    """Тест на обновление фото действующей записи питомца.
    На выходе ожидается статус код 200"""
    _, my_pet_list = pf.get_list_of_pets(get_key, filter='my_pets')
    pet_id = my_pet_list['pets'][0]['id']
    status, result = pf.update_pet_photo(get_key, pet_id, pet_photo)
    assert status == 200

def test_update_pet_photo_incorrect_auth_key(get_key, pet_photo='images/britanskaya.jpg'):
    """Тест на обновление фото действующей записи питомца.
    На выходе ожидается статус код 200"""
    _, auth_key = pf.get_api_key(email, password)
    _, my_pet_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = my_pet_list['pets'][0]['id']
    auth_key = {'key': 'asafd548dsf84ds21f6ds8'}
    status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 403
