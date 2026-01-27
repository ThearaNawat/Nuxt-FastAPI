from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import UploadFile, File

class Product(BaseModel):
    id: Optional[int] | None
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: Optional[str] = None
    expire_date: Optional[str] = None
    package: Optional[str] = None
    stock: Optional[int] = None
    category_id: int = Field(..., description="The field category is required")
    review: Optional[int] = None
    images: Optional[List[UploadFile]] = File(None)
    

