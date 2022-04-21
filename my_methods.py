import datetime
from datetime import datetime

import requests


def sum(a, b):
    return a + b


def is_user_birthday(id: int) -> bool:
    user = requests.get(f"fakeapi.com/{id}")
    today = datetime.today().strftime('%Y-%m-%d')
    return user['birthday'] == today


def get_user_age(id: int) -> str:
    user = requests.get(f"fakeapi.com/{id}")
    return user.json()['age']
