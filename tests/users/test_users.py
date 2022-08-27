import pytest
import requests
from send_request.src.baseclasses.response import Response
from send_request.src.schemas.users import User
from send_request.src.generators.user import UserGenerator
from send_request.configuration import get_not_working_company
from send_request.tests.users.conftest import TEST_USER_ID, TEST_INVALID_USER_ID


# Проверка структуры компании.
def test_data_structure(get_link):
    r = requests.get(get_link)
    response = Response(r)
    response.asser_status_code(200).validate(User)


# Создание с привязкой к компании.
def test_create_user_with_company(get_link):
    data = UserGenerator().set_last_name().set_company_id(1).build()
    r = requests.post(url=get_link, json=data)
    Response(r).asser_status_code(201).validate(User)


# Создание без привязки к компании.
def test_create_user_without_company(get_link):
    data = UserGenerator().set_last_name('Karamba').build()
    r = requests.post(url=get_link, json=data)
    Response(r).asser_status_code(201).validate(User)


# Создание без обязательного поля.
def test_create_user_without_required_field(get_link):
    data = UserGenerator().set_first_name().build()
    r = requests.post(url=get_link, json=data)
    Response(r).asser_status_code(201).validate(User)


# Пробуем создать пользователя с привязкой к неактивной компании.
@pytest.mark.parametrize("company", get_not_working_company())
def test_create_user_with_inactive_company(get_link, company):
    data = UserGenerator().set_last_name('ural').set_company_id(company).build()
    r = requests.post(url=get_link, json=data)
    Response(r).asser_status_code(201).validate(User)


# Пробуем получить нашего юзера и проверить что всё окей, как и статус код.
def test_get_user_by_id(get_link):
    link = get_link + str(TEST_USER_ID)
    r = requests.get(link)
    response = Response(r)
    response.asser_status_code(200).validate(User)


# Делаем запрос по невалидным юзерам.
def test_get_invalid_user_by_id(get_link):
    link = get_link + str(999)
    r = requests.get(link)
    response = Response(r)
    response.asser_status_code(200).validate(User)


# Пробуем обновить поля у юзера.
def test_update_user_with_id(get_link):
    link = get_link + str(TEST_USER_ID)
    data = UserGenerator().set_first_name('igor').set_last_name('igor').build()
    r = requests.put(link, json=data)
    Response(r).asser_status_code(200)


# Пробуем привязать его к неактивной компании.
def test_bound_user_with_invalid_company(get_link):
    link = get_link + str(TEST_USER_ID)
    data = UserGenerator().set_company_id(5).set_last_name('x').build()
    r = requests.put(link, json=data)
    Response(r).asser_status_code(400)


# Пробуем обновить несуществующего юзера.
def test_update_user_with_invalid_id(get_link):
    link = get_link + str(TEST_INVALID_USER_ID)
    data = UserGenerator().set_last_name('x').build()
    r = requests.put(link, json=data)
    Response(r).asser_status_code(404)


# Удаляем существующего юзера.
def test_delete_user(get_link):
    link = get_link + str(TEST_USER_ID)
    r = requests.delete(link, data=UserGenerator().set_first_name('igor').set_last_name('igor').build())
    Response(r).asser_status_code(202)


# Пробуем удалить несуществующего юзера.
def test_delete_user_with_wrong_id(get_link):
    link = get_link + str(TEST_INVALID_USER_ID)
    r = requests.delete(link, data=UserGenerator().set_first_name('igor').set_last_name('igor').build())
    Response(r).asser_status_code(404)
