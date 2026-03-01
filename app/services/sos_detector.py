from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.checkin import Check_In
from app.models.safety_setting import SafetySetting
from app.models.sos_event import SOSEvent
from app.models.user import User


def detect_missed_checkins(db: Session):
    users = db.query(User).all()
    now = datetime.now()

    for user in users:
        settings = (
            db.query(SafetySetting).filter(SafetySetting.user_id == user.id).first()
        )

        if not settings:
            continue

        last_checkin = (
            db.query(Check_In)
            .filter(Check_In.user_id == user.id)
            .order_by(Check_In.checked_in_at.desc())
            .first()
        )

        if not last_checkin:
            continue

        deadline = (
            last_checkin.checked_in_at
            + timedelta(hours=settings.checkin_interval_hour)
            + timedelta(minutes=settings.grace_period_minutes)
        )

        if now > deadline:
            already_triggered = (
                db.query(SOSEvent)
                .filter(SOSEvent.user_id == user.id, SOSEvent.status == "triggered")
                .first()
            )

            if not already_triggered:
                event = SOSEvent(user_id=user.id, reason="Missed check-in")
                db.add(event)
    db.commit()
