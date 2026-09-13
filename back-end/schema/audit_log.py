from __future__ import annotations

from typing import Optional

from pydantic import Field

from schema.base import EntityReadSchema, EntityWriteSchema


class base_audit_log(EntityWriteSchema):
    module: str = Field(min_length=2)
    action: str = Field(min_length=1)
    entity_id: int
    entity_type: str = Field(min_length=1)
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    user_id: Optional[int] = None
    ip_address: Optional[str] = None


class base_audit_log_read(EntityReadSchema):
    module: str = Field(min_length=2)
    action: str = Field(min_length=1)
    entity_id: int
    entity_type: str = Field(min_length=1)
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
