import json.decoder
import requests as re
from requests_toolbelt.multipart.encoder import MultipartEncoder


class Petfriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Функция принимает на вход валидные email и пароль и возвращает
        api ключ!"""
        headers = {
            'email': email,
            'password': password,
        }
        res = re.get(self.base_url + '/api/key', headers= headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, api_key: json, filter: str) -> json:
        """Функция принимает на вход api ключ и значение фильтра
         и возвращает статус-код ответа и список питомцев."""
        headers = {'auth_key': api_key['key']}
        filter = {'filter': filter}

        res = re.get(self.base_url + '/api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Функция принимает на вход параметры нового питомца и добавляет новую запись в список питомцев.
        На выходе фукция возвращает статус-код и словарь со значениями нового питомца."""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = re.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def del_pet(self,auth_key: json, pet_id: str) -> int:
        """Фукция принимает на вход api ключ и id питомца, которого необходимо удалить из списка.
        На выходе фукция возвращает статус-код."""
        headers = {'auth_key': auth_key['key']}

        res = re.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code

        return status

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age:str) -> json:
        """Функция принимает на вход api ключ, id питомца, параметры которого нужно изменить, имя, тип животного и возраст.
        Функция возвращает статус-код и словарь с новыми значениями питомца"""
        data = MultipartEncoder(
            {
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = re.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Функция добавляет нового питомца в список питомцев на сайте, без добавления фото.
        На выходе функуия возвращает словарь с параметрами нового питомца."""
        data = MultipartEncoder(
            {
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        )

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = re.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_photo(self, auth_key: json, pet_id: str, pet_photo) -> json:
        """Функция позволяет изменить фото питомца на сайте. Возвращает статус-код."""
        data = MultipartEncoder(
            {
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg'),
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = re.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_animal_type(self, auth_key: json, name: str, age: str, pet_photo: str) -> json:
        """Функция принимает на вход параметры нового питомца и добавляет новую запись в список питомцев.
        На выходе фукция возвращает статус-код и словарь со значениями нового питомца."""
        data = MultipartEncoder(
            fields={
                'name': name,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = re.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_age(self, auth_key: json, name: str, animal_type: str, pet_photo: str) -> json:
        """Функция принимает на вход параметры нового питомца и добавляет новую запись в список питомцев.
        На выходе фукция возвращает статус-код и словарь со значениями нового питомца."""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = re.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result