import re
from random import randint

NUM_CHECK = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
NUM_F = re.compile(r'((\+7|7|8)+([0-9]){10})$')


def format_phone_number(number):
    return int('7' + ''.join(NUM_F.match(number).groups()))


def check_phone_number(number):
    return bool(NUM_CHECK.match(number))


def generate_sms_code():
    code = randint(1000, 9999)
    return code
