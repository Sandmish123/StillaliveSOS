from pydantic import BaseModel
from uuid import UUID


class UserCreate(BaseModel):
    phone: str
    name: str | None = None


class UserResponse(BaseModel):
    id: UUID
    phone: str
    name: str | None = None

    class Config:
        from_attributes = True
