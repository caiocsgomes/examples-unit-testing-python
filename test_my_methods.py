from datetime import datetime
from unittest.mock import patch, MagicMock

from my_methods import sum, is_user_birthday, get_user_age


def test_sum():
    assert sum(1, 2) == 3


@patch('my_methods.requests')
def test_is_user_birthday(mock_requests):
    today = datetime.today().strftime('%Y-%m-%d')
    mock_requests.get.return_value = {'birthday': today}
    assert is_user_birthday(1) == True


@patch('my_methods.requests')
def test_user_age(mock_requests):
    mock_requests.get.return_value = MagicMock(json=lambda: {'age': 10})
    assert get_user_age(1) == 10
