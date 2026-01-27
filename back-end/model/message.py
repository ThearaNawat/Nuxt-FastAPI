from sqlmodel import SQLModel, Field
from typing import Optional

class Message(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str
    group_id: Optional[str] = None
    question: str
    answer: str
    chat_type: str
    created_at: str