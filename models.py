from pydantic import BaseModel
class LoanRequest(BaseModel):
    request_id: str