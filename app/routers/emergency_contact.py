from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.emergency_contact import EmergencyContacts
from app.models.user import User
from app.schemas.emergency_contact import (
    EmergencyContactWrappedResponse,
    EmergencyContactCreate,
    EmergencyContactListResponse,
)


router = APIRouter(
    prefix="/emergency-contacts",
    tags=["Emergency Contacts"],
)


@router.post("/", response_model=EmergencyContactWrappedResponse)
def add_contacts(
    data: EmergencyContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = EmergencyContacts(
        user_id=current_user.id,
        name=data.name,
        phone=data.phone,
        relation=data.relation,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return {
        "message": "contact add successfully",
        "data": contact
        }


@router.get("/", response_model=EmergencyContactListResponse)
def list_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contacts = (
        db.query(EmergencyContacts)
        .filter(
            EmergencyContacts.user_id == current_user.id)
        .all()
    )
    return {
        "message": "Contact retrieve successfully",
        "data": contacts,
    }
