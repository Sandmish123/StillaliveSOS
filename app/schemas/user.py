from pydantic import BaseModel,EmailStr
from uuid import UUID
from datetime import date


class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    dob: date
    address: str


class UserResponse(BaseModel):
    id: UUID
    phone: str
    name: str | None = None
    email: EmailStr | None = None
    dob: date | None = None
    address: str | None = None

    class Config:
        from_attributes = True