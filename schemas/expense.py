from pydantic import BaseModel, ConfigDict, Field
from datetime import date as Date


class ExpenseCreate(BaseModel):
    description: str | None = None
    amount: float
    date: Date | None = Field(default_factory=Date.today)
    account_id: int


class ExpenseResponse(BaseModel):
    id: int
    description: str | None = None
    amount: float
    date: Date
    account_id: int

    model_config = ConfigDict(from_attributes=True)


class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    date: Date | None = None
