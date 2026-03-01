from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.safety_setting import SafetySetting
from app.models.user import User


router = APIRouter(prefix="/safety", tags=["Safety"])


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
