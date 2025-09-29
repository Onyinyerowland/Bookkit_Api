from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy.orm import relationship


class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE'), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=False, server_default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='bookings')
    service = relationship('Service', back_populates='bookings')
    review = relationship('Review', back_populates='booking', uselist=False)
