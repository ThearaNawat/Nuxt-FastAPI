from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "USER"
    
    id: int | None = Field(default= None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    password: str = Field(index=True)
    status: bool = Field(default=True, index=True)