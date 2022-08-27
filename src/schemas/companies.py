from pydantic import BaseModel

from typing import Optional

from send_request.src.enums.company_enums import Status


class Company(BaseModel):
    company_id: int
    company_name: str
    company_address: str
    company_status: Status
    description_lang: Optional[list]
    description: Optional[str]