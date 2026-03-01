from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.checkin import Check_In
from app.models.user import User


router = APIRouter(
    prefix="/checkin",
    tags=["Check-In"],
)


@router.post("/")
def check_in(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_in = Check_In(user_id=current_user.id)
    db.add(check_in)
    db.commit()
    return {"message": "Check-in successful"}

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

    if not check_in:
        return {"last_checkin": None}
    return {"last_checkin": checkin.checked_in_at}
