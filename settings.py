email = 'solomonslava1991@gmail.com'
password = 'solomon0204'

def russian_chars():
    string = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    return string.encode('utf8')

def generate_string(n):
    return 'x' * n

def chinese_chars():
    string = '的一是不了人我在有他这为之大来以个中上们'
    return string.encode('utf8')

def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'