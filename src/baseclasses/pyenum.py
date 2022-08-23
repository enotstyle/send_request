from enum import Enum

class PyEnum(Enum):

    @classmethod
    def list(cls):
        return [c.value for c in cls]
