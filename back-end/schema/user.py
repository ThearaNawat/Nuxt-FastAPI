from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class user_create(BaseModel):
    int: Optional[int] = None
    username: str = Field(min_length=2)
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=6)
    confirm_password: str
    status: bool = Field(default=True)
    
    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, v, info):
        if v != info.data.get("password"):
            raise ValueError("Password do not match")
        return v
        
    
class user_read(BaseModel):
    int: Optional[int] = None
    username: str
    email: str
    password: str
    status: bool = Field(default=True)
    
class user_login(BaseModel):
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=6)