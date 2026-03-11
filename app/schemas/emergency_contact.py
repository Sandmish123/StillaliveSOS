from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List


class EmergencyContactCreate(BaseModel):
    name: str
    phone: List[str]
    relation: Optional[str] = None


class EmergencyContactBulkCreate(BaseModel):
    list_contacts: List[EmergencyContactCreate]


class EmergencyContactResponse(BaseModel):
    id: UUID
    name: str
    phone: List[str]
    relation: Optional[str] = None

    class Config:
        from_attributes = True


class EmergencyContactWrappedResponse(BaseModel):
    message: str
    data: List[EmergencyContactResponse]


class EmergencyContactListResponse(BaseModel):
    message: str
    data: List[EmergencyContactResponse]