import uuid
from datetime import datetime, timezone
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Check_In(Base):
    __tablename__ = "checkins"

    id = Column(UUID(as_uuid=True),
                primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),
                     ForeignKey("users.id"), nullable=False)
    checked_in_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
