import uuid
from sqlalchemy import Column, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class UserLocation(Base):
    __tablename__ = "user_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    recorded_at = Column(DateTime, default=datetime.now(), nullable=False)
