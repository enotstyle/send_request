"""
Здесь вам нужно научиться работать со списком компаний и фильтрами. Попробуйте покрыть следующие кейсы:

1. Получить список компаний, проверить структуру объектов, проверить статус код.
2. Проверить фильтрацию по статусу, действительно ли фильтруются данные.
3. Проверить фильтрацию с использованием лимита и оффсета.
"""

import requests
import pytest

from send_request.src.baseclasses.response import Response
from send_request.src.schemas.company import Company
from send_request.src.schemas.project import Meta
from send_request.src.enums.company_enums import Status
from send_request.tests.companies.conftest import TEST_COMPANY_ID, WRONG_PARAMETERS


# Получить список компаний, проверить структуру объектов, проверить статус код.
def test_data_structure(get_link):
    r = requests.get(get_link)
    response = Response(r)
    response.asser_status_code(200).validate(Company)


# Проверить фильтрацию по статусу, действительно ли фильтруются данные.
@pytest.mark.parametrize("status", Status.list())
def test_filters(get_link, status):
    link = get_link + f"?status={status}"
    r = requests.get(link)
    response = Response(r)
    for i in response.response_json:
        company = Company.parse_obj(i)
        status_compony = company.company_status.value
        assert status_compony == status, \
            f"Получен статус {status_compony}, ожидается {status}"


# Проверить фильтрацию с использованием лимита и оффсета.
@pytest.mark.parametrize('limit, offset', [
    (1, 2),
    (3, 4),
    (0, 3),
    (4, 2),
    (1, 1),
    (3, 1)
])
def test_meta_filters(get_link, limit, offset):
    link = get_link + f"?limit={limit}&offset={offset}"
    r = requests.get(link)
    response = Response(r)
    response_limit = Meta.parse_obj(response.response_json_meta).limit
    response_offset = Meta.parse_obj(response.response_json_meta).offset

    assert response_limit == limit, f'Получен лимит {response_limit}, ожидается лимит {limit}'
    assert response_offset == offset, f"Получен оффсет {response_offset}, ожидается оффсет {offset}"

    assert len(response.response_json) == limit, \
        f'Получено количество компаний {len(response.response_json)}, при лимите {limit}'


"""
Проверяем:
1. Структуру компании и статус код.
2. Делаем запрос с Accept-Language хедером, передав доступную локализацию. (Учитывайте негативные кейсы)
3. Проверяем запрос по несуществующей компании.
"""


# Проверяем структуру компании и статус код.
def test_single_company(get_link):
    link = get_link + str(TEST_COMPANY_ID)
    r = requests.get(link)
    response = Response(r)
    response.asser_status_code(200).validate(Company)


# Проверяем структуру компании и статус код (статус и id не валидный).
@pytest.mark.parametrize('company_id', WRONG_PARAMETERS)
def test_single_company_negative(get_link, company_id):
    link = get_link + str(company_id)
    r = requests.get(link)
    response = Response(r)
    response.asser_status_code(300).validate(Company)

# НЕ ГОТОВ!
# Делаем запрос с Accept-Language хедером, передав доступную локализацию. (Учитывайте негативные кейсы)
@pytest.mark.parametrize('lang', [
    "en-us",
    'en'
])
def test_request_with_lang(get_link, lang):
    headers = {"Content-Type": "text"}
    link = get_link + str(TEST_COMPANY_ID)
    r = requests.get(url=link, headers=headers)
    print(r.headers)
    response = Response(r).asser_status_code(200)
    pars = Company.parse_obj(response.response_body)
    print(pars)
