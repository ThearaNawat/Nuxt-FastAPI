from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Category(SQLModel, table=True):
    __tablename__ = 'Category'
    
    id: int = Field(primary_key=True, default=None)
    code: str = Field(index=True)
    name: str = Field(index=True)
    description: str | None = Field(index=True, default=None)