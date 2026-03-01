import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class SOSEvent(Base):
    __tablename__ = "sos_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    trigger_at = Column(DateTime, default=datetime.now(), nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="triggered")
