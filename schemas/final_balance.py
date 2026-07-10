from pydantic import BaseModel, ConfigDict

class FinalBalanceResponse(BaseModel):
    id: int
    balance: float
    month: int
    year: int
    account_id: int

    model_config = ConfigDict(from_attributes=True)