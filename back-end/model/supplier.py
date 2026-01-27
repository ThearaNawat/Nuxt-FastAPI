from sqlmodel import SQLModel, Field

class Supplier(SQLModel, table= True):
    id: int = Field(primary_key=True, index=True)
    code: str = Field(index=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    phone: str = Field(index=True)
    address: str | None = Field(default=None, index=True)
    description: str | None = Field(default=None, index=True)