from typing import Optional, Annotated, List
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, field_validator
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class Users(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str = Field(...)
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    hashed_password: str = Field(...)
    is_active: bool = Field(...)
    role: str = Field(...)
    phone_number: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={"example": {
            "email": "test@test.com",
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "hashed_password": "test",
            "is_active": True,
            "role": "test",
            "phone_number": "test"
        }
    })

class UpdateUsers(BaseModel):
    email: str = Field(...)
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    hashed_password: str = Field(...)
    is_active: bool = Field(...)
    role: str = Field(...)
    phone_number: str = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={"example": {
            "email": "test@test.com",
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "hashed_password": "test",
            "is_active": True,
            "role": "test",
            "phone_number": "test"
        }
    })  

class UserCollection(BaseModel):
    users: List[Users]