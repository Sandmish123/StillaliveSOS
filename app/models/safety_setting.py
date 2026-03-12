from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class SafetySetting(Base):
    __tablename__ = "safety_setting"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

    checkin_interval_minutes  = Column(Integer, default=5)
    grace_period_minutes = Column(Integer, default=2)
