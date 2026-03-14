from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    dob = Column(Date, nullable=True)
    address = Column(String, nullable=True)
    fcm_token = Column(String, nullable=True)
    
    @property
    def is_partial_completed(self):
        return bool(self.phone and self.email)

    @property
    def is_fully_completed(self):
        return all([
            self.name,
            self.phone,
            self.email,
            self.dob,
            self.address
        ])