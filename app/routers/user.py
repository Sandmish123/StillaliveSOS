from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.otp import OTPRequest
from app.models.sos_event import SOSEvent
from app.core.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    exit_user = db.query(User).filter(User.phone == user.phone).first()
    if exit_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(        
        name=user.name,
        phone=user.phone,
        email=user.email,
        dob=user.dob,
        address=user.address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.delete("/me")
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Delete OTP records
    db.query(OTPRequest).filter(
        OTPRequest.phone == current_user.phone
    ).delete()

    # Delete SOS events
    db.query(SOSEvent).filter(
        SOSEvent.user_id == current_user.id
    ).delete()

    # Delete user
    db.delete(current_user)

    db.commit()

    return {"message": "Account permanently deleted"}