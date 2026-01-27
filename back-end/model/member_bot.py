from sqlmodel import SQLModel, Field
from typing import Optional

class MemberBot(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    member_name: str
    remark: Optional[str] = None
    is_active: bool = True