import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------------------------------------------------------------------------
# Expense schemas (Day 6)
# ---------------------------------------------------------------------------

class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1)
    date: datetime.date
    description: Optional[str] = None


class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=1)
    date: Optional[datetime.date] = None
    description: Optional[str] = None

    @model_validator(mode="after")
    def reject_explicit_null_on_required_fields(self) -> "ExpenseUpdate":
        """Prevent callers from explicitly nulling amount, category, or date."""
        for field_name in ("amount", "category", "date"):
            if field_name in self.model_fields_set and getattr(self, field_name) is None:
                raise ValueError(f"{field_name} may not be set to null")
        return self


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    amount: Decimal
    category: str
    date: datetime.date
    description: Optional[str] = None
