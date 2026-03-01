from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.sos_event import SOSEvent
from app.services.sos_executor import execute_sos
from app.core.database import get_db
from app.services.sos_detector import detect_missed_checkins


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/detect_sos")
def run_detection(db: Session = Depends(get_db)):
    detect_missed_checkins(db)

    return {"status": "Detection run"}


@router.post("/execute-sos")
def run_sos_execution(db: Session = Depends(get_db)):
    events = db.query(SOSEvent).filter(SOSEvent.status == "triggered").all()

    for event in events:
        execute_sos(db, event)

    return {"status": "sos executed"}
