from datetime import timedelta
from unittest import mock

from django.utils.timezone import now

from shareapp.main.models import (
    make_expire_timestamp,
    SharedItem,
    make_file_path,
    make_random_password,
)


@mock.patch("shareapp.main.models.time")
def test_make_file_path(mocked_time, create_user):
    mocked_time.return_value = 12345
    user = create_user(username="test")
    instance = SharedItem(owner=user)

    assert make_file_path(instance, "test.txt") == "test/12345/test.txt"


def test_make_random_password():
    password = make_random_password()

    assert password.isalnum()
    assert len(password) >= 8


def test_make_expire_timestamp():
    timestamp_1 = now() + timedelta(days=1)
    expire_timestamp = make_expire_timestamp()
    timestamp_2 = now() + timedelta(days=1)

    assert timestamp_1 <= expire_timestamp <= timestamp_2
