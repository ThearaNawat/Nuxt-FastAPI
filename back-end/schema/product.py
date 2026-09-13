from __future__ import annotations

from typing import Optional

from fastapi import File, UploadFile
from pydantic import Field, field_validator
from datetime import datetime, date
from schema.base import EntityReadSchema, EntityWriteSchema


class Product(EntityWriteSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: Optional[str] = None
    expire_date: Optional[date] = None
    package: Optional[str] = None
    stock: Optional[int] = None
    category_id: int = Field(..., description="The field category is required")
    review: Optional[int] = None
    images: Optional[list[UploadFile]] = File(default=None)
    measurement_id: Optional[int] = None


class ProductRead(EntityReadSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: Optional[str] = None
    expire_date: Optional[date] = None
    package: Optional[str] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None
    review: Optional[int] = None
    category_name: Optional[str] = None
    measurement_id: Optional[int] = None
    measurement_name: Optional[str] = None

    # @field_validator("expire_date", mode="before")
    # @classmethod
    # def format_date(cls, v: Optional[str]) -> Optional[str]:
    #     if v and len(v) >= 10:
    #         # Takes '2027-07-29' from '2027-07-29T17:00:00.000Z'
    #         date_part = v[:10] 
    #         year, month, day = date_part.split("-")
    #         return f"{day}/{month}/{year}"
    #     return v
    

