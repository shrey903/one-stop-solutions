from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(160), nullable=False)
    service = Column(String(120), nullable=False)
    message = Column(Text, nullable=True)

    # Travel-booking-only details (populated when service is Flight/Bus/Train Tickets)
    from_station = Column(String(120), nullable=True)
    to_station = Column(String(120), nullable=True)
    journey_date = Column(String(20), nullable=True)
    return_date = Column(String(20), nullable=True)
    passengers = Column(String(10), nullable=True)

    email_sent = Column(String(10), default="no")
    whatsapp_sent = Column(String(10), default="no")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    service = Column(String(60), nullable=False)  # Accounting Services / PAN Card and Other Services / Travel Booking Services
    rating = Column(Integer, nullable=False)       # 1-5
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
