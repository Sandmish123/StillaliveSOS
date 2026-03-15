from fastapi import APIRouter, Depends, HTTPException ,status
from sqlalchemy.orm import Session
from app.models.otp import OTPRequest
from app.models.sos_event import SOSEvent
from app.core.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.user import UserCreate, UserResponse,UserUpdate
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/me", status_code=200)
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Delete OTP records
        db.query(OTPRequest).filter(
            OTPRequest.phone == current_user.phone
        ).delete(synchronize_session=False)

        # Delete SOS events
        db.query(SOSEvent).filter(
            SOSEvent.user_id == current_user.id
        ).delete(synchronize_session=False)

        # Delete user
        db.delete(current_user)

        # Commit transaction
        db.commit()

        return {
            "success": True,
            "message": "Account permanently deleted"
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )