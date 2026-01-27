from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class base_supplier(BaseModel):
    id: Optional[int] | None
    code: str = Field(min_length=2, unique=True)
    name: str = Field(min_length=2)
    email: EmailStr
    phone: str = Field(min_length=8, unique=True)
    address: Optional[str] | None
    description: Optional[str] | None