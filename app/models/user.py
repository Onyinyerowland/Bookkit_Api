from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    # other fields...
    role = Column(String(50), nullable=False, server_default='user')  # e.g., 'admin', 'user'
    is_active = Column(Boolean, nullable=False, server_default='true')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    bookings = relationship('Booking', back_populates='user')
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role})>"
    
