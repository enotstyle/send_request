from send_request.configuration import URL
import pytest


@pytest.fixture
def get_companies_link():
    link = URL + "issues/companies/"
    return link

@pytest.fixture
def get_users_link():
    link = URL + "issues/users/"
    return link


TEST_COMPANY_ID = 1
TEST_USER_ID = 1