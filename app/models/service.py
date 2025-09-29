from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10,2), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='true')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookings = relationship('Booking', back_populates='service')
    def __repr__(self):
        return f"<Service(id={self.id}, title={self.title}, price={self.price})>"
