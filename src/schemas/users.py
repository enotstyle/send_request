from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    first_name: Optional[str]
    last_name: str
    company_id: Optional[int]
    user_id: int

