import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID , ARRAY
from app.core.database import Base


class EmergencyContacts(Base):
    __tablename__ = "emergency_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),
                     ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    phone = Column(ARRAY(String), nullable=False)
    relation = Column(String, nullable=False)
