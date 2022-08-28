import requests
from send_request.src.enums.company_enums import Status
import pytest
from send_request.src.baseclasses.response import Response
from send_request.src.schemas.companies import Company
from send_request.tests.issues.conftest import TEST_COMPANY_ID, TEST_USER_ID
from send_request.src.schemas.users import User
from send_request.src.generators.user import UserGenerator


# Проблема этого эндпоинта в том, что постоянно применяется фильтр CLOSED вне зависимости от переданного значения.
@pytest.mark.parametrize('status', Status.list())
def test_filter_companies_by_status(get_companies_link, status):
    link = get_companies_link + f"?status={status}"
    r = requests.get(link)
    response = Response(r)
    for i in response.response_json_data:
        company = Company.parse_obj(i)
        assert company.company_status.value == status, f'Фильтруем по {status}, получено {company.company_status.value}'


# В этом случае вы можете проверить кейс, когда ваш сервис возвращает данные очень долго. В данном случае, вы получите ответ спустя 5 секунд.
def test_get_company_by_id(get_companies_link):
    link = get_companies_link + str(TEST_COMPANY_ID)
    r = requests.get(link)

    assert r.elapsed.total_seconds() < 5, 'Время ответа больше 5 сек'

    response = Response(r)
    company = Company.parse_obj(response.response_json_data)
    assert company.company_id == TEST_COMPANY_ID


# Обратите внимание на статус код и какие поля возвращает бекенд. Ничего вы не увидите, кроме "user_id" и "company_id".
def test_get_user_by_id(get_users_link):
    link = get_users_link + str(TEST_USER_ID)
    r = requests.get(link)
    response = Response(r)
    response.asser_status_code(200).validate(User)


# Проблема заключается в том, что юзер всегда будет создан не из тех данных, которые вы отправили, а из других :)
def test_send_data(get_users_link):
    data = UserGenerator().set_last_name('x').set_first_name('x').set_company_id('1').build()
    r = requests.post(get_users_link, data=data)
    print(r.json())
    print(data)
    for key, val in data.items():
        assert r.json()[key] == val, f'Не совпадают значения key-val, с отправленным'
