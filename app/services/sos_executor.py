from sqlalchemy.orm import Session

from app.models.sos_event import SOSEvent
from app.models.emergency_contact import EmergencyContacts
from app.models.location import UserLocation
from app.services.notifier import send_sos_notifications


def execute_sos(db: Session, sos_event: SOSEvent):
    """
    Executes SOS actions exactly once per event
    """

    if sos_event.status != "triggered":
        return

    # fetch contacts
    contacts = (
        db.query(EmergencyContacts)
        .filter(EmergencyContacts.user_id == sos_event.user_id)
        .all()
    )

    # FETCH last known location

    location = (
        db.query(UserLocation)
        .filter(UserLocation.user_id == sos_event.user_id)
        .order_by(UserLocation.recorded_at.desc())
        .first()
    )

    location_text = "Location unavailable"
    if location:
        location_text = (
            f"https://maps.google.com/?q=" f"{location.latitude},{location.longitude}"
        )

    message = (
        "🚨 SOS ALERT 🚨\n"
        "User missed check-in.\n"
        f"Last known location: {location_text}"
    )

    send_sos_notifications(contacts, message)

    sos_event.status = "notified"
    db.commit()
