from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List


class EmergencyContactCreate(BaseModel):
    name: str
    phone: str
    relation: Optional[str] = None


class EmergencyContactResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    relation: Optional[str] = None

    class Config:
        from_attributes = True


class EmergencyContactWrappedResponse(BaseModel):
    message: str
    data: EmergencyContactResponse


class EmergencyContactListResponse(BaseModel):
    message: str
    data: List[EmergencyContactResponse]
