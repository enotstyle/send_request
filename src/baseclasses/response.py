from pydantic.error_wrappers import ValidationError


class Response:

    def __init__(self, response):
        self.response = response
        self.response_json_data = None
        self.response_json_meta = None
        self.response_status = response.status_code
        self.parsed_object = None

        if self.response.json().get('data'):
            self.response_json_data = response.json().get('data')
        else:
            self.response_json_data = response.json()
        if self.response.json().get('meta'):
            self.response_json_meta = response.json().get('meta')

    def validate(self, schema):
        try:
            if isinstance(self.response_json_data, list):
                for item in self.response_json_data:
                    parsed_object = schema.parse_obj(item)
                    self.parsed_object = parsed_object
            else:
                schema.parse_obj(self.response_json_data)
        except ValidationError:
            raise AssertionError(
                "Could not map received object to pydantic schema"
            )

    def asser_status_code(self, status_code):
        """
        Метод для валидации статус кода. Из объекта респонса,
        который мы получили, мы берём статус и сравниваем с тем, который
        нам был передан как параметр.
        """
        if isinstance(status_code, list):
            assert self.response_status in status_code, self
        else:
            assert self.response_status == status_code, self
        return self

    def get_parsed_object(self):
        return self.parsed_object


    def get_object_with_param(self, param):
        for i in self.response_json_data:
            item_list = []
            if param in i.value():
                item_list.append(i)

            return item_list

    def __str__(self):
        """
        Метод отвечает за строковое представление нашего объекта. Что весьма
        удобно, ведь в случае срабатывания валидации, мы получаем полную картину
        всего происходящего и все параметры которые нам нужны для определения
        ошибки.
        """
        return \
            f'\nStatus code: {self.response_status} \n' \
            f'Requested: {self.response.url} \n' \
            f'Response body: {self.response_json}'
