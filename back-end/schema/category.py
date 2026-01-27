from pydantic import BaseModel, Field
from typing import Optional

class base_category(BaseModel):
    id: Optional[int] = None
    code: str = Field(min_length=2, unique=True)
    name: str = Field(min_length=2)
    description: str = Field(default=None)