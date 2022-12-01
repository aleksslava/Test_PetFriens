import json.decoder
import os
import requests as re
from settings import email, password
from requests_toolbelt.multipart.encoder import MultipartEncoder


class Petfriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
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

    def del_pet(self,auth_key, pet_id):
        headers = {'auth_key': auth_key['key']}

        res = re.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code

        return status

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
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
