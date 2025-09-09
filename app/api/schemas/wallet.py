import uuid
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class OperationIn(BaseModel):
    operation_type: OperationType
    amount: Decimal = Field(..., gt=0)

    @field_validator("amount")
    @classmethod
    def quantize_two_places(cls, v: Decimal) -> Decimal:
        return v.quantize(Decimal("0.01"))


class WalletCreate(BaseModel):
    id: uuid.UUID


class WalletOut(BaseModel):
    id: int
    balance: Decimal
    user_id: int
