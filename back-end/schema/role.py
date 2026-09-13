from __future__ import annotations

from typing import Optional, List

from pydantic import Field, field_validator

from schema.base import EntityReadSchema, EntityWriteSchema


class base_role(EntityWriteSchema):
    role_name: str = Field(min_length=2)
    description: Optional[str] = None
    menu: List[int]


class base_role_read(EntityReadSchema):
    role_name: str = Field(min_length=2)
    description: Optional[str] = None
    menu: List[int]

    @field_validator("menu", mode="before")
    @classmethod
    def convert_set_to_list(cls, v):
        if isinstance(v, set):
            return list(v)
        return v or []

