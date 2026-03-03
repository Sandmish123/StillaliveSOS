import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.models.otp import OTPRequest
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
            OTPRequest.verified == False,  # noqa
        )
        .first()
    )

    if not record or record.expires_at < record.expires_at.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    record.verified = True

    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    token = create_access_token(
        subject=user.phone,
        user_id=user.id,
    )

    db.commit()

    return {"access_token": token}
