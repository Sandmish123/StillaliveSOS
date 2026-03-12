from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.safety_setting import SafetySetting
from datetime import timezone
import pytz
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.checkin import Check_In
from app.models.user import User
from datetime import datetime, timezone

router = APIRouter(
    prefix="/checkin",
    tags=["Check-In"],
)



@router.post("/")
def check_in(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)
    # Get user safety settings
    settings = (
        db.query(SafetySetting)
        .filter(SafetySetting.user_id == current_user.id)
        .first()
    )

    # interval_hours = settings.checkin_interval_hour if settings and settings.checkin_interval_hour else 1
    # interval_minutes = interval_hours * 60

    # Get last check-in
    last_checkin = (
        db.query(Check_In)
        .filter(Check_In.user_id == current_user.id)
        .order_by(Check_In.checked_in_at.desc())
        .first()
    )

    if last_checkin:
        last_time = last_checkin.checked_in_at

        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=timezone.utc)

        next_allowed = last_time + timedelta(minutes=5)

        if now < next_allowed:
            remaining = next_allowed - now
            return {
                "allowed": False,
                "message": "Check-in not allowed yet",
                "next_allowed_at": next_allowed,
                "remaining_minutes": int(remaining.total_seconds() / 60)
            }
    # Allow check-in
    new_checkin = Check_In(user_id=current_user.id)
    db.add(new_checkin)
    db.commit()

    return {"allowed": True, "message": "Check-in successful"}



@router.get("/last")
def last_checkin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checkin = (
        db.query(Check_In)
        .filter(Check_In.user_id == current_user.id)
        .order_by(Check_In.checked_in_at.desc())
        .first()
    )

    if not checkin:
        return {"last_checkin": None}

    # Convert UTC to IST
    ist = pytz.timezone("Asia/Kolkata")
    local_time = checkin.checked_in_at.astimezone(ist)

    return {"last_checkin": local_time}