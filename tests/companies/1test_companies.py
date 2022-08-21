# Здесь вам нужно научиться работать со списком компаний и фильтрами. Попробуйте покрыть следующие кейсы:
#
# 1. Получить список компаний, проверить структуру объектов, проверить статус код.
# 2. Проверить фильтрацию по статусу, действительно ли фильтруются данные.
# 3. Проверить фильтрацию с использованием лимита и оффсета.

import requests

from send_request.src.baseclasses.response import Response
from send_request.src.schemas.company import Company


link = "https://send-request.me/api/companies/"

def test_data_structure():
    r = requests.get(link)
    response = Response(r)
    response.asser_status_code(200).validate(Company)

def test_filters():
    r = requests.get(link)
    response = Response(r)
    print(response.response_json)
    print(len(response.response_json))

test_filters()
