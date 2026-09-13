from __future__ import annotations

from typing import Optional

from pydantic import Field

from schema.base import EntityReadSchema, EntityWriteSchema


class base_category(EntityWriteSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: Optional[str] = None


class base_category_read(EntityReadSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: Optional[str] = None
