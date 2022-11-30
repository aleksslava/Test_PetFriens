import json.decoder

import requests as re
from settings import email, password


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


