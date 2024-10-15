from typing import Optional, Annotated, List
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, field_validator
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class Todos(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    description: str = Field(...)
    priority: int = Field(...)
    complete: bool = Field(...)
    owner_id: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={"example": {
            "title": "test",
            "description": "test",
            "priority": 1,
            "complete": False,
            "owner_id": "test"
        }
    })

class UpdateTodos(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    priority: int = Field(...)
    complete: bool = Field(...)
    owner_id: str = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={"example": {
            "title": "test",
            "description": "test",
            "priority": 1,
            "complete": False,
            "owner_id": "test"
        }
    })

class TodoCollection(BaseModel):
    todos: List[Todos]