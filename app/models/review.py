from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id', ondelete='CASCADE'), nullable=False, unique=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    booking = relationship('Booking', back_populates='review')
    user = relationship('User', secondary='bookings', back_populates='reviews')
    service = relationship('Service', secondary='bookings', back_populates='reviews')
    # Ensure a user can only review a service they booked
    __table_args__ = (
        # UniqueConstraint('booking_id', name='uix_booking_review'),
    )
    def __repr__(self):
        return f"<Review(id={self.id}, booking_id={self.booking_id}, rating={self.rating})>"
    
