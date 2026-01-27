from sqlmodel import Field, SQLModel
from typing import Optional

class GroupBot(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str
    group_name: str
    created_at: str
    updated_at: str
    is_active: bool = True
    description: Optional[str] = None
    created_by: Optional[str] = None
    