import re
from random import randint
from datetime import datetime
from datetime import timedelta

NUM_F = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
NUM_CHECK = re.compile(r'((\+7|7|8)+([0-9]){10})$')


def format_phone_number(number):
    return int('7' + ''.join(NUM_F.match(number).groups()))


def check_phone_number(number):
    return bool(NUM_CHECK.match(number))


def generate_sms_code():
    code = randint(1000, 9999)
    code = 1234
    return code


def check_sms_code(code, expiries_at, u_code):
    if code is None or u_code is None:
        return False
    if code != u_code:
        return False
    if datetime.utcnow() > expiries_at:
        return False
    return True


def get_first_and_last_month_day(year, month):
    d = datetime.utcnow().replace(year=year, month=month, day=1, hour=0, minute=0, microsecond=0, second=0)
    first = d + timedelta()
    next_month = d.replace(day=28) + timedelta(days=4)
    next_month = next_month - timedelta(days=next_month.day)
    next_month = next_month.replace(hour=23, minute=59, second=59, microsecond=999999)
    return first, next_month

