from send_request.src.baseclasses.response import Response
from send_request.src.enums.company_enums import Status
import requests
from send_request.src.schemas.companies import Company

URL = "https://send-request.me/api/"


def get_not_working_company():
    company_list = []
    link = "https://send-request.me/api/companies/?limit=100&offset=0"
    r = requests.get(link)
    response = Response(r)
    data = response.response_json_data
    for item in data:
        company = Company.parse_obj(item)
        if company.company_status.value == Status.ACTIVE.value:
            company_list.append(company.company_id)
    return company_list
