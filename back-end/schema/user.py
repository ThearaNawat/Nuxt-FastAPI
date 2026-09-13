from __future__ import annotations

from pydantic import EmailStr, Field, field_validator, BaseModel, model_validator
from typing import Optional
from schema.base import EntityReadSchema, EntityWriteSchema, SchemaBase


class user_create(EntityWriteSchema):
    username: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)
    role_id: Optional[int] = None
    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, value, info):
        if value != info.data.get("password"):
            raise ValueError("Password do not match")
        return value


class user_update(BaseModel):
    username: str = Field(min_length=2)
    email: EmailStr
    password: Optional[str] = Field(default=None, min_length=6)
    
    confirm_password: Optional[str] = None
    role_id: Optional[int] = None
    status: bool
    # @field_validator("confirm_password")
    # @classmethod
    # def password_match(cls, value, info):
    #     if value != info.data.get("password"):
    #         raise ValueError("Password do not match")
    #     return value
    @model_validator(mode="after")
    def validate_password(self):
        if self.password is not None:
            if self.confirm_password is None:
                raise ValueError("Confirm password is required.")

            if self.password != self.confirm_password:
                raise ValueError("Passwords do not match.")

        return self


class user_read(EntityReadSchema):
    username: str = Field(min_length=2)
    email: EmailStr


class user_login(SchemaBase):
    email: EmailStr
    password: str = Field(min_length=6)
