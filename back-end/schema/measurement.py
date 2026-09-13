from typing import Optional
from pydantic import BaseModel, Field
from schema.base import EntityReadSchema, EntityWriteSchema

class CreateMeasurement(EntityWriteSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: Optional[str] = None


class ReadMeasure(EntityReadSchema):
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    description: Optional[str] = None
    status: bool = True