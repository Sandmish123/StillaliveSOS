from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.checkin import Check_In
from app.models.sos_event import SOSEvent
from app.models.safety_setting import SafetySetting

router = APIRouter(prefix="/sos", tags=["SOS"])


def is_checkin_missed(
    last_checkin: datetime, interval_minutes: int, grace_minutes: int
) -> bool:
    allowed_time = last_checkin + timedelta(minutes=interval_minutes + grace_minutes)
    return datetime.now() > allowed_time


@router.get("/status")
def sos_status(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # get safety setting (fallback defaults)
    settings = db.query(SafetySetting).filter(SafetySetting.user_id == user.id).first()

    interval = settings.checkin_interval_minutes if settings else 5
    grace = settings.grace_period_minutes if settings else 2

    # get last check-in
    last_checkin = (
        db.query(Check_In)
        .filter(Check_In.user_id == user.id)
        .order_by(Check_In.checked_in_at.desc())
        .first()
    )

    # NO check-in yet -> safe (first-time user)
    if not last_checkin:
        return {"status": "safe"}

    # Checked if Missed
    missed = is_checkin_missed(last_checkin.checked_in_at, interval, grace)

    if not missed:
        return {"status": "safe"}

    # Missed -> check if SOS already exists

    existing_sos = (
        db.query(SOSEvent)
        .filter(SOSEvent.user_id == user.id, SOSEvent.status == "triggered")
        .first()
    )

    if existing_sos:
        return {
            "status": "sos",
            "triggered_at": existing_sos.triggered_at,
            "contacts_notified": True,
        }

    # create new SOS event
    sos = SOSEvent(
        user_id=user.id,
        triggered_at=datetime.now(),
        status="triggered",
        reason="Missed check-in",
    )
    db.add(sos)
    db.commit()
    db.refresh(sos)

    # Notification sending will come later
    return {
        "status": "sos",
        "triggered_at": sos.triggered_at,
        "contacts_notified": False,
    }
