from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.location import UserLocation
from app.models.user import User


router = APIRouter(prefix="/location", tags=["Location"])


@router.post("/")
def update_location(
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loc = UserLocation(user_id=current_user.id, latitude=latitude, longitude=longitude)
    db.add(loc)
    db.commit()
    return {"status": "Location updated"}
