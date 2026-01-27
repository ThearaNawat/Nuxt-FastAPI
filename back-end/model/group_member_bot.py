from sqlmodel import Field, SQLModel
from typing import Optional
class GroupMemberBot(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    member_id: str
    group_id: Optional[str] = None
    created_at: str