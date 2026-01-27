from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from model.category import Category
import database

class Product(SQLModel, table=True):
    __tablename__ = "PRODUCT"
    
    id: Optional[int] = Field(default=None,primary_key=True)
    code: str = Field(index=True)
    name: str = Field(index=True)
    description: str | None = Field(index=True, default= None)
    expire_date: str | None = Field(index=True, default=None)
    package: str | None = Field(index=True)
    stock: int | None = Field(index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="Category.id")
    review: int | None = Field(index=True)