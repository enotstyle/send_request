import pytest

from send_request.configuration import URL

TEST_COMPANY_ID = 1
WRONG_PARAMETERS = [
    123123123,
    "asdasd",
    "!@413aaa"
]


@pytest.fixture
def get_link():
    company_url = URL + "companies/"
    return company_url
