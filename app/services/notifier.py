from typing import List
from app.models.emergency_contact import EmergencyContacts


def send_sos_notifications(contacts: List[EmergencyContacts], message: str):
    """Mock notification hai , bad me update karenge isko real sms se"""

    for contact in contacts:
        print(f"[SOS] sending to {contact.phone}: {message}")
