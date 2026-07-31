from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    type: str
    interest: float


class AccountResponse(BaseModel):
    id: int
    type: str
    interest: float
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class AccountUpdate(BaseModel):
    type: str | None = None
    interest: float | None = None