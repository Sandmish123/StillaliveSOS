from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.safety_setting import SafetySetting
from app.models.user import User

router = APIRouter(prefix="/safety", tags=["Safety"])

class IntervalUpdate(BaseModel):
    checkin_interval_minutes: int
    grace_period_minutes: int | None = None

@router.get("/")
def get_settings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    settings = (
        db.query(SafetySetting).filter(SafetySetting.user_id == current_user.id).first()
    )

    if not settings:
        settings = SafetySetting(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


@router.put("/")
def update_settings(
    payload: IntervalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    settings = (
        db.query(SafetySetting)
        .filter(SafetySetting.user_id == current_user.id)
        .first()
    )

    if not settings:
        settings = SafetySetting(user_id=current_user.id)
        db.add(settings)

    settings.checkin_interval_minutes = payload.checkin_interval_minutes

    if payload.grace_period_minutes is not None:
        settings.grace_period_minutes = payload.grace_period_minutes

    db.commit()
    db.refresh(settings)

    return {"message": "Safety settings updated", "settings": settings}