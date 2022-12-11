import pytest
from settings import email, password, generate_string, russian_chars, chinese_chars
from api import Petfriends

pf = Petfriends()


def test_get_api_key_correct(email=email, password=password):
    """Тест на получение auth_key с валидными email и password.
     Результатом теста должен быть статус код 200 и ключ в фомате json."""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


@pytest.mark.parametrize('email',[
                         '',
                         generate_string(255),
                         generate_string(1001),
                         russian_chars(),
                        chinese_chars()
                         ], ids= ['empty_string', 'string_len_255', 'string_len_1000', 'russian_chars',
                         'chinese_chars']
                         )
@pytest.mark.parametrize('password', [
    '',
    generate_string(255),
    generate_string(1001),
    russian_chars(),
    chinese_chars()
],                           ids= [
                             'empty_string',
                             'string_len_255',
                             'string_len_1001',
                             'russian_chars',
                             'chinese_chars'
                         ])
def test_api_incorrect(email, password):
    status, result = pf.get_api_key(email, password)
    print(f'Статус код ответа: {status}')
    assert 400 <= status <= 500





