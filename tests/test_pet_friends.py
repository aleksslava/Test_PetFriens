from api import Petfriends
from settings import email, password


pf = Petfriends()

def test_get_api_key_correct(email=email, password=password):
    """Тест на получение auth_key с валидными email и password.
     Результатом теста должен быть статус код 200 и ключ в фомате json."""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_incorrect_password(email=email, password='asdffa'):
    """Тест на получение auth_key с валидным email и неверным password.
     Результатом теста должен быть статус код 403. Ключа в ответе быть не должно."""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_incorrect_email(email='asheqwr.ru', password='asdffa'):
    """Тест на получение auth_key с неверным email и валидным password.
     Результатом теста должен быть статус код 403. Ключа в ответе быть не должно."""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_list_of_pets_all(filter=''):
    """Тест на получение списка всех животных на сайте. На выходе должен быть статус код 200 и список всех
    животных на сайте."""
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_list_of_pets_my_pets(filter='my_pets'):
    """Тест на получение списка животных пользователя на сайте. На выходе должен быть статус код 200
     и список всех животных пользователя на сайте."""
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_list_of_pets_all_incorrect_auth_key(filter=''):
    """Тест на получение списка всех животных на сайте с некорректным auth_key.
    На выходе должен быть статус код 403"""
    auth_key = {'key': 'asafd548dsf84ds21f6ds8'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403



def test_add_new_pet_correct(name='storm', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца на сайт с корректными входными данными.
    На выходе должны получить статус код 200 и словарь с данными нового питомца."""
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_incorrect_auth_key(name='Лола', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца с некорректным auth_key.
    На выходе ожидается ответ от сервера со статус кодом 403."""
    auth_key = {'key': 'asafd548dsf84ds21f6ds8'}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403


def test_add_new_pet_without_animal_type(name='izum', age='hg', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца без значения 'animal_type'.
    На выходе ожидается ответ от сервера со статус кодом 400."""
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.add_new_pet_without_animal_type(auth_key, name, age, pet_photo)
    assert status == 400


def test_add_new_pet_without_age(name='cat', animal_type='cat', pet_photo='images/britanskaya.jpg'):
    """Тест на добавление нового питомца без значения 'age'.
    На выходе ожидается ответ от сервера со статус кодом 400."""
    _, auth_key = pf.get_api_key(email=email, password=password)
    status, result = pf.add_new_pet_without_age(auth_key=auth_key, name=name, animal_type=animal_type, pet_photo=pet_photo)
    assert status == 400


def test_del_my_pet_correct():
    """Тест на удаление питомца из списка питомцев из списка пользователя на сайте по id питомца.
    В ответе от сервера ожидается статус код 200, удаленный питомец отсутствует в списке."""
    _, auth_key = pf.get_api_key(email=email, password=password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(list_of_pets['pets']) == 0:
        pf.add_new_pet(auth_key, name='vasya', animal_type='cat', age='10', pet_photo='images/britanskaya.jpg')
        _, list_of_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = list_of_pets['pets'][0]['id']
    status = pf.del_pet(auth_key, pet_id)
    assert status == 200
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    assert list_of_pets['pets'][0]['id'] != pet_id

def test_del_enemy_pet_correct():
    """Тест на удаление питомца из полного списка питомцев на сайте по id питомца.
    В ответе от сервера ожидается статус код 200, удаленный питомец отсутствует в списке.
    Данный тест показывает, что пользователь может удалить чужих питомцев. Такого быть не должно!"""
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
    """Тест на обновление информации о питомце с корректными данными.
    На выходе ожидается ответ от сервера со статус кодом 200 и словарь с новыми значениями питомца. """
    _, auth_key = pf.get_api_key(email, password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
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
    """Тест на создание нового питомца, без фото питомца.
     На выходе ожидается статус код 200 и словарь с данными нового питомца. """
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_update_pet_photo_correct(pet_photo='images/britanskaya.jpg'):
    """Тест на обновление фото действующей записи питомца.
    На выходе ожидается статус код 200"""
    _, auth_key = pf.get_api_key(email, password)
    _, my_pet_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = my_pet_list['pets'][0]['id']
    status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 200

def test_update_pet_photo_incorrect_auth_key(pet_photo='images/britanskaya.jpg'):
    """Тест на обновление фото действующей записи питомца.
    На выходе ожидается статус код 200"""
    _, auth_key = pf.get_api_key(email, password)
    _, my_pet_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = my_pet_list['pets'][0]['id']
    auth_key = {'key': 'asafd548dsf84ds21f6ds8'}
    status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 403
