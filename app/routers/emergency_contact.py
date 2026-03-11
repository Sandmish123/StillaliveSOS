from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from fastapi import HTTPException
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.emergency_contact import EmergencyContacts
from app.models.user import User
from app.schemas.emergency_contact import (
    EmergencyContactWrappedResponse,
    EmergencyContactBulkCreate,
    EmergencyContactListResponse,
)


router = APIRouter(
    prefix="/emergency-contacts",
    tags=["Emergency Contacts"],
)


@router.post("/", response_model=EmergencyContactWrappedResponse)
def add_contacts(
    data: EmergencyContactBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    contacts = []

    for item in data.list_contacts:
        contact = EmergencyContacts(
            user_id=current_user.id,
            name=item.name,
            phone=item.phone,
            relation=item.relation,
        )

        db.add(contact)
        contacts.append(contact)

    db.commit()

    for c in contacts:
        db.refresh(c)

    return {
        "message": "Contacts added successfully",
        "data": contacts
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



@router.delete("/{contact_id}")
def delete_contact(
    contact_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    contact = (
        db.query(EmergencyContacts)
        .filter(
            EmergencyContacts.id == contact_id,
            EmergencyContacts.user_id == current_user.id,
        )
        .first()
    )

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(contact)
    db.commit()

    return {"message": "Contact deleted successfully"}