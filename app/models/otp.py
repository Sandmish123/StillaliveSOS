from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime, timedelta
from app.core.database import Base


class OTPRequest(Base):
    __tablename__ = "otp_requests"
#need to update this OTPRequest
    phone = Column(String, primary_key=True)
    otp = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)

    @staticmethod
    def expiry_time():
        return datetime.utcnow() + timedelta(minutes=5)
