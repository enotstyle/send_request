from faker import Faker

fake = Faker()


class UserGenerator:

    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.company_id = None

    def set_first_name(self, first_name=fake.name()):
        self.first_name = first_name
        return self

    def set_last_name(self, last_name=fake.first_name()):
        self.last_name = last_name
        return self

    def set_company_id(self, company_id):
        self.company_id = company_id
        return self

    def clear(self):
        self.set_last_name()
        return self

    def build(self):
        # self.clear()
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company_id": self.company_id
        }


a = UserGenerator()
print(a.__dict__)
print(a.set_first_name().set_last_name().set_company_id(1).build())