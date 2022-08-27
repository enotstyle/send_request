from send_request.configuration import URL
import pytest


@pytest.fixture
def get_link():
    users_url = URL + "users/"
    return users_url


TEST_USER_ID = 1

TEST_INVALID_USER_ID = 999

