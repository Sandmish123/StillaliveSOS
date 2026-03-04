import random
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Body
from app.models.refresh_token import RefreshToken
from uuid import UUID
from app.core.security import create_access_token, create_refresh_token
from app.models.refresh_token import RefreshToken
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.models.otp import OTPRequest
from app.schemas.auth import OTPVerifyIn, OTPRequestIn, TokenOut
from app.services.phone_verification import verify_phone_number
from uuid import UUID
from datetime import datetime
import secrets

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from app.models.user import User
from app.models.otp import OTPRequest
from app.models.refresh_token import RefreshToken
from app.schemas.auth import OTPVerifyIn, OTPRequestIn, TokenOut
from app.services.phone_verification import verify_phone_number


router = APIRouter(prefix="/auth", tags=["Auth"])

#need to change the flow of request otp and verify otp
@router.post("/request_otp")
def request_otp(data: OTPRequestIn, db: Session = Depends(get_db)):

    #  Step 1 — Verify phone number first
    verify_phone_number(data.phone)

    #  Step 2 — Generate secure OTP
    import secrets
    otp = str(secrets.randbelow(900000) + 100000)

    record = db.query(OTPRequest).filter(
        OTPRequest.phone == data.phone
    ).first()

    if record:
        record.otp = otp
        record.expires_at = OTPRequest.expiry_time()
        record.verified = False
    else:
        record = OTPRequest(
            phone=data.phone,
            otp=otp,
            expires_at=OTPRequest.expiry_time(),
        )
        db.add(record)

    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        user = User(phone=data.phone)
        db.add(user)

    db.commit()

    # MOCK OTP RESPONSE (for learning only)
    return {"message": "OTP sent", "otp": otp}


@router.post("/verify_otp", response_model=TokenOut)
def verify_otp(data: OTPVerifyIn, db: Session = Depends(get_db)):

    record = (
        db.query(OTPRequest)
        .filter(
            OTPRequest.phone == data.phone,
            OTPRequest.otp == data.otp,
            OTPRequest.verified == False,
        )
        .first()
    )

    if not record or record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    record.verified = True

    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    #  Create tokens
    access_token = create_access_token(
        subject=user.phone,
        user_id=user.id,
    )

    refresh_token = create_refresh_token(
        subject=user.phone,
        user_id=user.id,
    )


    # 💾 Save refresh token in DB
    db_refresh = RefreshToken(
        token=refresh_token,
        user_id=str(user.id),
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_access_token(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db)
):

    payload = decode_access_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token_in_db = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not token_in_db:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    new_access_token = create_access_token(
        subject=payload["sub"],
        user_id=UUID(payload["user_id"])
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db)
):

    db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).delete()

    db.commit()

    return {"message": "Logged out successfully"}


