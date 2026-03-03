from sqlalchemy import Column, String, Boolean, DateTime
from app.core.database import Base
from datetime import datetime, timedelta, timezone

class OTPRequest(Base):
    __tablename__ = "otp_requests"
#need to update this OTPRequest
    phone = Column(String, primary_key=True)
    otp = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    @staticmethod
    def expiry_time():
        return datetime.now(timezone.utc) + timedelta(minutes=5)
