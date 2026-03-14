from datetime import datetime, timedelta
from sqlalchemy.orm import Session


from app.core.database import SessionLocal
from app.models.user import User
from app.models.checkin import Check_In
from app.models.safety_setting import SafetySetting
from app.models.sos_event import SOSEvent
from app.services.sos_detector import detect_missed_checkins


def test_sos_triggered_for_missed_checkin():
    db: Session = SessionLocal()

    user = User(phone="8273182399")
    db.add(user)
    db.commit()
    db.refresh(user)

    settings = SafetySetting(
        user_id=user.id, checkin_interval_minutes=1, grace_period_minutes=0
    )
    db.add(settings)

    old_checkin = Check_In(
        user_id=user.id, checked_in_at=datetime.now() - timedelta(minutes=2)
    )
    db.add(old_checkin)
    db.commit()

    detect_missed_checkins(db)

    sos = db.query(SOSEvent).filter(SOSEvent.user_id == user.id).first()
    assert sos is not None
    assert sos.reason == "Missed check-in"

    db.close()
